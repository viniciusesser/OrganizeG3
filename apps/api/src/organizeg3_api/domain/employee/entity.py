"""Employee domain entity."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, date, datetime, timedelta
import uuid

from organizeg3_api.domain.employee.value_objects import (
    EmployeeCode,
    EmployeeDocument,
    EmployeeEmail,
    EmployeePhone,
    EmploymentStatus,
    normalize_optional_text,
)


def _next_timestamp(
    previous: datetime | None,
) -> datetime:
    """Return a UTC timestamp strictly newer than the previous value."""

    now = datetime.now(UTC)

    if previous is None:
        return now

    comparable_previous = previous

    if comparable_previous.tzinfo is None:
        comparable_previous = comparable_previous.replace(
            tzinfo=UTC
        )

    if now <= comparable_previous:
        return comparable_previous + timedelta(
            microseconds=1
        )

    return now


@dataclass(slots=True)
class Employee:
    """Represent an employee belonging to one tenant."""

    tenant_id: uuid.UUID
    code: str
    full_name: str

    id: uuid.UUID | None = None
    branch_id: uuid.UUID | None = None

    document_number: str | None = None
    email: str | None = None
    phone: str | None = None

    job_title: str | None = None
    contract_type: str | None = None

    status: EmploymentStatus = EmploymentStatus.ACTIVE

    birth_date: date | None = None
    admission_date: date | None = None
    termination_date: date | None = None

    is_active: bool = True

    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        """Validate and normalize employee state."""

        self._validate_uuid(
            self.tenant_id,
            field_name="tenant",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                field_name="identificador",
            )

        if self.branch_id is not None:
            self._validate_uuid(
                self.branch_id,
                field_name="filial",
            )

        self.code = EmployeeCode(
            self.code
        ).value

        self.full_name = self.full_name.strip()

        if not self.full_name:
            raise ValueError(
                "O nome do funcionário é obrigatório."
            )

        self.job_title = normalize_optional_text(
            self.job_title
        )

        self.contract_type = normalize_optional_text(
            self.contract_type
        )

        self.document_number = self._normalize_document(
            self.document_number
        )

        self.email = self._normalize_email(
            self.email
        )

        self.phone = self._normalize_phone(
            self.phone
        )

        self._validate_dates()

        if (
            self.status == EmploymentStatus.TERMINATED
            and self.termination_date is None
        ):
            raise ValueError(
                "Funcionário desligado deve possuir "
                "data de desligamento."
            )

        if (
            self.termination_date is not None
            and self.status
            != EmploymentStatus.TERMINATED
        ):
            raise ValueError(
                "Funcionário com data de desligamento "
                "deve possuir status TERMINATED."
            )

        if self.status == EmploymentStatus.TERMINATED:
            self.is_active = False

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        code: str,
        full_name: str,
        branch_id: uuid.UUID | None = None,
        document_number: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        job_title: str | None = None,
        contract_type: str | None = None,
        birth_date: date | None = None,
        admission_date: date | None = None,
    ) -> Employee:
        """Create a new active employee."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            branch_id=branch_id,
            code=code,
            full_name=full_name,
            document_number=document_number,
            email=email,
            phone=phone,
            job_title=job_title,
            contract_type=contract_type,
            status=EmploymentStatus.ACTIVE,
            birth_date=birth_date,
            admission_date=admission_date,
            termination_date=None,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def update_details(
        self,
        *,
        code: str,
        full_name: str,
        branch_id: uuid.UUID | None,
        document_number: str | None,
        email: str | None,
        phone: str | None,
        job_title: str | None,
        contract_type: str | None,
        birth_date: date | None,
        admission_date: date | None,
    ) -> None:
        """Update editable employee details atomically."""

        candidate = replace(
            self,
            code=code,
            full_name=full_name,
            branch_id=branch_id,
            document_number=document_number,
            email=email,
            phone=phone,
            job_title=job_title,
            contract_type=contract_type,
            birth_date=birth_date,
            admission_date=admission_date,
            updated_at=_next_timestamp(
                self.updated_at
            ),
        )

        self.code = candidate.code
        self.full_name = candidate.full_name
        self.branch_id = candidate.branch_id
        self.document_number = (
            candidate.document_number
        )
        self.email = candidate.email
        self.phone = candidate.phone
        self.job_title = candidate.job_title
        self.contract_type = (
            candidate.contract_type
        )
        self.birth_date = candidate.birth_date
        self.admission_date = (
            candidate.admission_date
        )
        self.updated_at = candidate.updated_at

    def assign_branch(
        self,
        branch_id: uuid.UUID | None,
    ) -> None:
        """Assign or remove the employee branch."""

        if branch_id is not None:
            self._validate_uuid(
                branch_id,
                field_name="filial",
            )

        if self.branch_id == branch_id:
            return

        self.branch_id = branch_id
        self._touch()

    def put_on_leave(self) -> None:
        """Mark the employee as temporarily on leave."""

        if self.status == EmploymentStatus.TERMINATED:
            raise ValueError(
                "Funcionário desligado não pode "
                "ser afastado."
            )

        if self.status == EmploymentStatus.ON_LEAVE:
            return

        self.status = EmploymentStatus.ON_LEAVE
        self.is_active = True
        self._touch()

    def reactivate(self) -> None:
        """Return an employee to active employment."""

        if self.status == EmploymentStatus.TERMINATED:
            raise ValueError(
                "Funcionário desligado não pode "
                "ser reativado sem novo vínculo."
            )

        if (
            self.status == EmploymentStatus.ACTIVE
            and self.is_active
        ):
            return

        self.status = EmploymentStatus.ACTIVE
        self.is_active = True
        self._touch()

    def deactivate(self) -> None:
        """Disable an employee without recording termination."""

        if self.status == EmploymentStatus.TERMINATED:
            return

        if (
            self.status == EmploymentStatus.INACTIVE
            and not self.is_active
        ):
            return

        self.status = EmploymentStatus.INACTIVE
        self.is_active = False
        self._touch()

    def terminate(
        self,
        *,
        termination_date: date,
    ) -> None:
        """Terminate the employee employment relationship."""

        if (
            self.admission_date is not None
            and termination_date
            < self.admission_date
        ):
            raise ValueError(
                "A data de desligamento não pode ser "
                "anterior à admissão."
            )

        self.termination_date = termination_date
        self.status = EmploymentStatus.TERMINATED
        self.is_active = False
        self._touch()

    def _validate_dates(self) -> None:
        if (
            self.birth_date is not None
            and self.admission_date is not None
            and self.birth_date
            >= self.admission_date
        ):
            raise ValueError(
                "A data de nascimento deve ser "
                "anterior à admissão."
            )

        if (
            self.admission_date is not None
            and self.termination_date is not None
            and self.termination_date
            < self.admission_date
        ):
            raise ValueError(
                "A data de desligamento não pode ser "
                "anterior à admissão."
            )

    @staticmethod
    def _validate_uuid(
        value: object,
        *,
        field_name: str,
    ) -> None:
        if not isinstance(
            value,
            uuid.UUID,
        ):
            raise TypeError(
                f"O {field_name} do funcionário "
                "deve ser um UUID."
            )

        if value.int == 0:
            raise ValueError(
                f"O {field_name} do funcionário "
                "não pode possuir UUID nulo."
            )

    @staticmethod
    def _normalize_document(
        value: str | None,
    ) -> str | None:
        normalized = normalize_optional_text(
            value
        )

        if normalized is None:
            return None

        return EmployeeDocument(
            normalized
        ).value

    @staticmethod
    def _normalize_email(
        value: str | None,
    ) -> str | None:
        normalized = normalize_optional_text(
            value
        )

        if normalized is None:
            return None

        return EmployeeEmail(
            normalized
        ).value

    @staticmethod
    def _normalize_phone(
        value: str | None,
    ) -> str | None:
        normalized = normalize_optional_text(
            value
        )

        if normalized is None:
            return None

        return EmployeePhone(
            normalized
        ).value

    def _touch(self) -> None:
        self.updated_at = _next_timestamp(
            self.updated_at
        )
