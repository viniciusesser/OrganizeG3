"""Read-only audit of legacy customer data."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from organizeg3_api.domain.customer.entity import (
    CustomerType,
)
from organizeg3_api.domain.customer.value_objects import (
    DocumentNumber,
    EmailAddress,
    PhoneNumber,
)

_DUPLICATE_GROUP_MIN_SIZE = 2
_NULL_TENANT_ID = "00000000-0000-0000-0000-000000000000"

class AuditSeverity(StrEnum):
    """Severity assigned to one audit finding."""

    ERROR = "ERROR"
    WARNING = "WARNING"


class AuditIssueCode(StrEnum):
    """Stable identifiers for customer audit findings."""

    MISSING_TENANT_ID = "customer.missing_tenant_id"
    MISSING_CODE = "customer.missing_code"
    MISSING_NAME = "customer.missing_name"
    INVALID_CUSTOMER_TYPE = "customer.invalid_type"

    INVALID_DOCUMENT = "customer.invalid_document"
    DOCUMENT_TYPE_MISMATCH = (
        "customer.document_type_mismatch"
    )
    NON_NORMALIZED_DOCUMENT = (
        "customer.non_normalized_document"
    )
    DUPLICATE_DOCUMENT = "customer.duplicate_document"

    INVALID_EMAIL = "customer.invalid_email"
    NON_NORMALIZED_EMAIL = (
        "customer.non_normalized_email"
    )
    DUPLICATE_EMAIL = "customer.duplicate_email"

    INVALID_PHONE = "customer.invalid_phone"
    NON_NORMALIZED_PHONE = (
        "customer.non_normalized_phone"
    )


@dataclass(
    frozen=True,
    slots=True,
)
class CustomerAuditRecord:
    """Raw customer data required by the auditor."""

    customer_id: int
    tenant_id: str | None
    code: str | None
    name: str | None
    customer_type: str | None
    document_number: str | None
    email: str | None
    phone: str | None
    is_archived: bool


@dataclass(
    frozen=True,
    slots=True,
)
class CustomerAuditIssue:
    """One customer-data problem found by the audit."""

    code: AuditIssueCode
    severity: AuditSeverity
    message: str
    customer_ids: tuple[int, ...]
    tenant_id: str | None = None
    field: str | None = None
    raw_value: str | None = None
    normalized_value: str | None = None
    blocks_unique_index: bool = False

    def to_dict(self) -> dict[str, object]:
        """Serialize the finding for JSON output."""

        return {
            "code": self.code.value,
            "severity": self.severity.value,
            "message": self.message,
            "customer_ids": list(
                self.customer_ids
            ),
            "tenant_id": self.tenant_id,
            "field": self.field,
            "raw_value": self.raw_value,
            "normalized_value": (
                self.normalized_value
            ),
            "blocks_unique_index": (
                self.blocks_unique_index
            ),
        }


@dataclass(
    frozen=True,
    slots=True,
)
class CustomerAuditReport:
    """Complete immutable customer audit report."""

    generated_at: datetime
    records_scanned: int
    active_records: int
    archived_records: int
    issues: tuple[CustomerAuditIssue, ...]

    @property
    def error_count(self) -> int:
        """Return the number of error findings."""

        return sum(
            issue.severity
            is AuditSeverity.ERROR
            for issue in self.issues
        )

    @property
    def warning_count(self) -> int:
        """Return the number of warning findings."""

        return sum(
            issue.severity
            is AuditSeverity.WARNING
            for issue in self.issues
        )

    @property
    def blocking_issue_count(self) -> int:
        """Return findings blocking a safe unique index."""

        return sum(
            issue.blocks_unique_index
            for issue in self.issues
        )

    @property
    def duplicate_document_groups(self) -> int:
        """Return duplicate CPF/CNPJ group count."""

        return sum(
            issue.code
            is AuditIssueCode.DUPLICATE_DOCUMENT
            for issue in self.issues
        )

    @property
    def duplicate_email_groups(self) -> int:
        """Return duplicate email group count."""

        return sum(
            issue.code
            is AuditIssueCode.DUPLICATE_EMAIL
            for issue in self.issues
        )

    def summary(self) -> dict[str, int]:
        """Return the numeric report summary."""

        return {
            "records_scanned": (
                self.records_scanned
            ),
            "active_records": (
                self.active_records
            ),
            "archived_records": (
                self.archived_records
            ),
            "issue_count": len(self.issues),
            "error_count": self.error_count,
            "warning_count": (
                self.warning_count
            ),
            "blocking_issue_count": (
                self.blocking_issue_count
            ),
            "duplicate_document_groups": (
                self.duplicate_document_groups
            ),
            "duplicate_email_groups": (
                self.duplicate_email_groups
            ),
        }

    def to_dict(self) -> dict[str, object]:
        """Serialize the report for JSON output."""

        return {
            "generated_at": (
                self.generated_at.isoformat()
            ),
            "summary": self.summary(),
            "issues": [
                issue.to_dict()
                for issue in self.issues
            ],
        }


class CustomerDataAuditor:
    """Inspect legacy customer records without mutation."""

    def audit(
        self,
        records: Sequence[
            CustomerAuditRecord
        ],
    ) -> CustomerAuditReport:
        """Audit all supplied records deterministically."""

        record_list = tuple(records)
        issues: list[CustomerAuditIssue] = []

        document_groups: dict[
            tuple[str, str],
            list[int],
        ] = {}

        email_groups: dict[
            tuple[str, str],
            list[int],
        ] = {}

        for record in record_list:
            self._audit_required_fields(
                record,
                issues,
            )

            customer_type = (
                self._audit_customer_type(
                    record,
                    issues,
                )
            )

            normalized_document = (
                self._audit_document(
                    record,
                    customer_type,
                    issues,
                )
            )

            normalized_email = (
                self._audit_email(
                    record,
                    issues,
                )
            )

            self._audit_phone(
                record,
                issues,
            )

            if (
                record.tenant_id is not None
                and normalized_document
                is not None
            ):
                document_groups.setdefault(
                    (
                        record.tenant_id,
                        normalized_document,
                    ),
                    [],
                ).append(record.customer_id)

            if (
                record.tenant_id is not None
                and normalized_email
                is not None
            ):
                email_groups.setdefault(
                    (
                        record.tenant_id,
                        normalized_email,
                    ),
                    [],
                ).append(record.customer_id)

        self._append_duplicate_issues(
            document_groups=document_groups,
            email_groups=email_groups,
            issues=issues,
        )

        sorted_issues = tuple(
            sorted(
                issues,
                key=lambda issue: (
                    issue.code.value,
                    issue.tenant_id or "",
                    issue.customer_ids,
                ),
            )
        )

        archived_records = sum(
            record.is_archived
            for record in record_list
        )

        return CustomerAuditReport(
            generated_at=datetime.now(UTC),
            records_scanned=len(record_list),
            active_records=(
                len(record_list)
                - archived_records
            ),
            archived_records=archived_records,
            issues=sorted_issues,
        )

    @staticmethod
    def _audit_required_fields(
        record: CustomerAuditRecord,
        issues: list[CustomerAuditIssue],
    ) -> None:
        normalized_tenant_id = (
            record.tenant_id.strip()
            if record.tenant_id is not None
            else ""
        )

        if (
            not normalized_tenant_id
            or normalized_tenant_id
            == _NULL_TENANT_ID
        ):
            issues.append(
                CustomerAuditIssue(
                    code=(
                        AuditIssueCode
                        .MISSING_TENANT_ID
                    ),
                    severity=AuditSeverity.ERROR,
                    message=(
                        "Cliente sem tenant_id."
                    ),
                    customer_ids=(
                        record.customer_id,
                    ),
                    field="tenant_id",
                    blocks_unique_index=True,
                )
            )

        if (
            record.code is None
            or not record.code.strip()
        ):
            issues.append(
                CustomerAuditIssue(
                    code=(
                        AuditIssueCode
                        .MISSING_CODE
                    ),
                    severity=AuditSeverity.ERROR,
                    message=(
                        "Cliente sem cÃ³digo vÃ¡lido."
                    ),
                    customer_ids=(
                        record.customer_id,
                    ),
                    tenant_id=record.tenant_id,
                    field="code",
                    raw_value=record.code,
                )
            )

        if (
            record.name is None
            or not record.name.strip()
        ):
            issues.append(
                CustomerAuditIssue(
                    code=(
                        AuditIssueCode
                        .MISSING_NAME
                    ),
                    severity=AuditSeverity.ERROR,
                    message=(
                        "Cliente sem nome vÃ¡lido."
                    ),
                    customer_ids=(
                        record.customer_id,
                    ),
                    tenant_id=record.tenant_id,
                    field="name",
                    raw_value=record.name,
                )
            )

    @staticmethod
    def _audit_customer_type(
        record: CustomerAuditRecord,
        issues: list[CustomerAuditIssue],
    ) -> CustomerType | None:
        raw_value = (
            record.customer_type.strip()
            if record.customer_type
            is not None
            else ""
        )

        try:
            return CustomerType(raw_value)
        except ValueError:
            issues.append(
                CustomerAuditIssue(
                    code=(
                        AuditIssueCode
                        .INVALID_CUSTOMER_TYPE
                    ),
                    severity=AuditSeverity.ERROR,
                    message=(
                        "Tipo de cliente invÃ¡lido."
                    ),
                    customer_ids=(
                        record.customer_id,
                    ),
                    tenant_id=record.tenant_id,
                    field="customer_type",
                    raw_value=(
                        record.customer_type
                    ),
                )
            )

            return None

    @staticmethod
    def _audit_document(
        record: CustomerAuditRecord,
        customer_type: CustomerType | None,
        issues: list[CustomerAuditIssue],
    ) -> str | None:
        raw_value = record.document_number

        if (
            raw_value is None
            or not raw_value.strip()
        ):
            return None

        try:
            document = DocumentNumber(raw_value)
        except (TypeError, ValueError) as exception:
            issues.append(
                CustomerAuditIssue(
                    code=(
                        AuditIssueCode
                        .INVALID_DOCUMENT
                    ),
                    severity=AuditSeverity.ERROR,
                    message=str(exception),
                    customer_ids=(
                        record.customer_id,
                    ),
                    tenant_id=record.tenant_id,
                    field="document_number",
                    raw_value=raw_value,
                )
            )

            return None

        normalized = str(document)

        if raw_value.strip() != normalized:
            issues.append(
                CustomerAuditIssue(
                    code=(
                        AuditIssueCode
                        .NON_NORMALIZED_DOCUMENT
                    ),
                    severity=(
                        AuditSeverity.WARNING
                    ),
                    message=(
                        "CPF/CNPJ estÃ¡ vÃ¡lido, mas "
                        "nÃ£o estÃ¡ normalizado."
                    ),
                    customer_ids=(
                        record.customer_id,
                    ),
                    tenant_id=record.tenant_id,
                    field="document_number",
                    raw_value=raw_value,
                    normalized_value=normalized,
                )
            )

        if (
            customer_type
            is CustomerType.INDIVIDUAL
            and not document.is_cpf
        ):
            issues.append(
                CustomerAuditIssue(
                    code=(
                        AuditIssueCode
                        .DOCUMENT_TYPE_MISMATCH
                    ),
                    severity=AuditSeverity.ERROR,
                    message=(
                        "Cliente pessoa fÃ­sica "
                        "estÃ¡ associado a CNPJ."
                    ),
                    customer_ids=(
                        record.customer_id,
                    ),
                    tenant_id=record.tenant_id,
                    field="document_number",
                    raw_value=raw_value,
                    normalized_value=normalized,
                )
            )

        if (
            customer_type
            is CustomerType.CORPORATE
            and not document.is_cnpj
        ):
            issues.append(
                CustomerAuditIssue(
                    code=(
                        AuditIssueCode
                        .DOCUMENT_TYPE_MISMATCH
                    ),
                    severity=AuditSeverity.ERROR,
                    message=(
                        "Cliente pessoa jurÃ­dica "
                        "estÃ¡ associado a CPF."
                    ),
                    customer_ids=(
                        record.customer_id,
                    ),
                    tenant_id=record.tenant_id,
                    field="document_number",
                    raw_value=raw_value,
                    normalized_value=normalized,
                )
            )

        return normalized

    @staticmethod
    def _audit_email(
        record: CustomerAuditRecord,
        issues: list[CustomerAuditIssue],
    ) -> str | None:
        raw_value = record.email

        if (
            raw_value is None
            or not raw_value.strip()
        ):
            return None

        try:
            email = EmailAddress(raw_value)
        except (TypeError, ValueError) as exception:
            issues.append(
                CustomerAuditIssue(
                    code=(
                        AuditIssueCode
                        .INVALID_EMAIL
                    ),
                    severity=AuditSeverity.ERROR,
                    message=str(exception),
                    customer_ids=(
                        record.customer_id,
                    ),
                    tenant_id=record.tenant_id,
                    field="email",
                    raw_value=raw_value,
                )
            )

            return None

        normalized = str(email)

        if raw_value.strip() != normalized:
            issues.append(
                CustomerAuditIssue(
                    code=(
                        AuditIssueCode
                        .NON_NORMALIZED_EMAIL
                    ),
                    severity=(
                        AuditSeverity.WARNING
                    ),
                    message=(
                        "E-mail estÃ¡ vÃ¡lido, mas "
                        "nÃ£o estÃ¡ normalizado."
                    ),
                    customer_ids=(
                        record.customer_id,
                    ),
                    tenant_id=record.tenant_id,
                    field="email",
                    raw_value=raw_value,
                    normalized_value=normalized,
                )
            )

        return normalized

    @staticmethod
    def _audit_phone(
        record: CustomerAuditRecord,
        issues: list[CustomerAuditIssue],
    ) -> None:
        raw_value = record.phone

        if (
            raw_value is None
            or not raw_value.strip()
        ):
            return

        try:
            phone = PhoneNumber(raw_value)
        except (TypeError, ValueError) as exception:
            issues.append(
                CustomerAuditIssue(
                    code=(
                        AuditIssueCode
                        .INVALID_PHONE
                    ),
                    severity=AuditSeverity.ERROR,
                    message=str(exception),
                    customer_ids=(
                        record.customer_id,
                    ),
                    tenant_id=record.tenant_id,
                    field="phone",
                    raw_value=raw_value,
                )
            )

            return

        normalized = str(phone)

        if raw_value.strip() != normalized:
            issues.append(
                CustomerAuditIssue(
                    code=(
                        AuditIssueCode
                        .NON_NORMALIZED_PHONE
                    ),
                    severity=(
                        AuditSeverity.WARNING
                    ),
                    message=(
                        "Telefone estÃ¡ vÃ¡lido, mas "
                        "nÃ£o estÃ¡ normalizado."
                    ),
                    customer_ids=(
                        record.customer_id,
                    ),
                    tenant_id=record.tenant_id,
                    field="phone",
                    raw_value=raw_value,
                    normalized_value=normalized,
                )
            )

    @staticmethod
    def _append_duplicate_issues(
        *,
        document_groups: dict[
            tuple[str, str],
            list[int],
        ],
        email_groups: dict[
            tuple[str, str],
            list[int],
        ],
        issues: list[CustomerAuditIssue],
    ) -> None:
        for (
            tenant_id,
            normalized_document,
        ), customer_ids in document_groups.items():
            if len(customer_ids) < _DUPLICATE_GROUP_MIN_SIZE:
                continue

            sorted_ids = tuple(
                sorted(customer_ids)
            )

            issues.append(
                CustomerAuditIssue(
                    code=(
                        AuditIssueCode
                        .DUPLICATE_DOCUMENT
                    ),
                    severity=AuditSeverity.ERROR,
                    message=(
                        "CPF/CNPJ duplicado dentro "
                        "do mesmo tenant."
                    ),
                    customer_ids=sorted_ids,
                    tenant_id=tenant_id,
                    field="document_number",
                    normalized_value=(
                        normalized_document
                    ),
                    blocks_unique_index=True,
                )
            )

        for (
            tenant_id,
            normalized_email,
        ), customer_ids in email_groups.items():
            if len(customer_ids) < _DUPLICATE_GROUP_MIN_SIZE:
                continue

            sorted_ids = tuple(
                sorted(customer_ids)
            )

            issues.append(
                CustomerAuditIssue(
                    code=(
                        AuditIssueCode
                        .DUPLICATE_EMAIL
                    ),
                    severity=AuditSeverity.ERROR,
                    message=(
                        "E-mail duplicado dentro "
                        "do mesmo tenant."
                    ),
                    customer_ids=sorted_ids,
                    tenant_id=tenant_id,
                    field="email",
                    normalized_value=(
                        normalized_email
                    ),
                    blocks_unique_index=True,
                )
            )

