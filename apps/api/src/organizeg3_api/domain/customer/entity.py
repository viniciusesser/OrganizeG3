"""Customer domain entity and customer classification."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
import uuid

from organizeg3_api.domain.customer.value_objects import (
    DocumentNumber,
    EmailAddress,
    PhoneNumber,
    optional_document,
    optional_email,
    optional_phone,
)


class CustomerType(StrEnum):
    """Customer classification type."""

    INDIVIDUAL = "INDIVIDUAL"
    CORPORATE = "CORPORATE"


@dataclass
class Customer:
    """Pure domain entity representing a customer."""

    tenant_id: uuid.UUID
    code: str
    name: str
    customer_type: CustomerType
    id: int | None = None
    document_number: DocumentNumber | str | None = None
    email: EmailAddress | str | None = None
    phone: PhoneNumber | str | None = None
    is_active: bool = True
    row_version: int = 1
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    deleted_at: datetime | None = None
    _allow_legacy_contacts: bool = field(
        default=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        """Normalize primitive values and enforce current invariants."""

        raw_tenant_id: object = self.tenant_id

        if not isinstance(raw_tenant_id, uuid.UUID):
            raise TypeError(
                "tenant_id deve ser um UUID válido."
            )

        if raw_tenant_id.int == 0:
            raise ValueError(
                "tenant_id não pode ser o UUID nulo."
            )

        self.code = self.code.strip()
        self.name = self.name.strip()
        self.customer_type = self._coerce_customer_type(
            self.customer_type
        )

        if self._allow_legacy_contacts:
            self.document_number = (
                self._normalize_legacy_document(
                    self.document_number
                )
            )
            self.email = self._normalize_legacy_email(
                self.email
            )
            self.phone = self._normalize_legacy_phone(
                self.phone
            )
        else:
            self.document_number = optional_document(
                self.document_number
            )
            self.email = optional_email(self.email)
            self.phone = optional_phone(self.phone)

        if not self.code:
            raise ValueError(
                "O código do cliente é obrigatório."
            )

        if not self.name:
            raise ValueError(
                "O nome do cliente é obrigatório."
            )

        if self.row_version < 1:
            raise ValueError(
                "row_version deve ser maior ou igual a 1."
            )

        self._validate_document_compatibility()

    def update_profile(
        self,
        *,
        name: str,
        customer_type: CustomerType,
        document_number: DocumentNumber | str | None,
        email: EmailAddress | str | None,
        phone: PhoneNumber | str | None,
    ) -> None:
        """Update editable data while preserving invariants."""

        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError(
                "O nome do cliente é obrigatório."
            )

        previous_customer_type = self.customer_type

        self.name = normalized_name
        self.customer_type = self._coerce_customer_type(
            customer_type
        )

        document_changed = (
            document_number != self.document_number
        )
        email_changed = email != self.email
        phone_changed = phone != self.phone
        type_changed = (
            self.customer_type
            is not previous_customer_type
        )

        if (
            document_changed
            or type_changed
            or not self._allow_legacy_contacts
        ):
            self.document_number = optional_document(
                document_number
            )

        if (
            email_changed
            or not self._allow_legacy_contacts
        ):
            self.email = optional_email(email)

        if (
            phone_changed
            or not self._allow_legacy_contacts
        ):
            self.phone = optional_phone(phone)

        self._validate_document_compatibility()
        self._touch()

    def activate(self) -> None:
        """Activate the customer without changing archival state."""

        self.is_active = True
        self._touch()

    def deactivate(self) -> None:
        """Deactivate the customer without archiving it."""

        self.is_active = False
        self._touch()

    def archive(self) -> None:
        """Archive the customer using logical deletion."""

        if self.deleted_at is not None:
            raise ValueError(
                "O cliente já está arquivado."
            )

        now = datetime.now(UTC)

        self.deleted_at = now
        self.updated_at = now
        self.is_active = False

    def reactivate(self) -> None:
        """Restore an archived customer and make it active."""

        if self.deleted_at is None:
            raise ValueError(
                "O cliente não está arquivado."
            )

        self.deleted_at = None
        self.is_active = True
        self._touch()

    def mark_as_deleted(self) -> None:
        """Compatibility alias for the archival operation."""

        self.archive()

    def _validate_document_compatibility(
        self,
    ) -> None:
        if (
            self.document_number is None
            or not isinstance(
                self.document_number,
                DocumentNumber,
            )
        ):
            return

        if (
            self.customer_type
            is CustomerType.INDIVIDUAL
            and not self.document_number.is_cpf
        ):
            raise ValueError(
                "Cliente pessoa física deve utilizar CPF."
            )

        if (
            self.customer_type
            is CustomerType.CORPORATE
            and not self.document_number.is_cnpj
        ):
            raise ValueError(
                "Cliente pessoa jurídica deve utilizar CNPJ."
            )

    @staticmethod
    def _normalize_legacy_document(
        value: DocumentNumber | str | None,
    ) -> DocumentNumber | str | None:
        if (
            value is None
            or not str(value).strip()
        ):
            return None

        try:
            return optional_document(value)
        except (TypeError, ValueError):
            return str(value).strip()

    @staticmethod
    def _normalize_legacy_email(
        value: EmailAddress | str | None,
    ) -> EmailAddress | str | None:
        if (
            value is None
            or not str(value).strip()
        ):
            return None

        try:
            return optional_email(value)
        except (TypeError, ValueError):
            return str(value).strip().lower()

    @staticmethod
    def _normalize_legacy_phone(
        value: PhoneNumber | str | None,
    ) -> PhoneNumber | str | None:
        if (
            value is None
            or not str(value).strip()
        ):
            return None

        try:
            return optional_phone(value)
        except (TypeError, ValueError):
            return str(value).strip()

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)

    @staticmethod
    def _coerce_customer_type(
        value: object,
    ) -> CustomerType:
        if isinstance(value, CustomerType):
            return value

        if not isinstance(value, str):
            raise TypeError(
                "O tipo de cliente deve ser informado como texto."
            )

        try:
            return CustomerType(value)
        except ValueError as exception:
            raise ValueError(
                "O tipo de cliente é inválido."
            ) from exception
