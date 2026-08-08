"""Supplier domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import uuid

from organizeg3_api.domain.supplier.value_objects import (
    SupplierCode,
    SupplierDocument,
    SupplierEmail,
    SupplierPhone,
    SupplierPostalCode,
    SupplierState,
    normalize_optional_text,
)


@dataclass(slots=True)
class Supplier:
    """Represent a supplier belonging to one tenant."""

    tenant_id: uuid.UUID
    code: str
    name: str

    id: uuid.UUID | None = None

    trade_name: str | None = None
    legal_name: str | None = None

    document_number: str | None = None
    state_registration: str | None = None

    email: str | None = None
    invoice_email: str | None = None

    phone: str | None = None
    secondary_phone: str | None = None

    website: str | None = None
    contact_name: str | None = None

    postal_code: str | None = None
    street: str | None = None
    number: str | None = None
    district: str | None = None
    city: str | None = None
    state: str | None = None

    is_active: bool = True

    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        """Validate and normalize supplier state."""

        self._validate_uuid(
            self.tenant_id,
            field_name="tenant",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                field_name="identificador",
            )

        self.code = SupplierCode(
            self.code
        ).value

        self.name = self.name.strip()

        if not self.name:
            raise ValueError(
                "O nome do fornecedor é obrigatório."
            )

        self.trade_name = normalize_optional_text(
            self.trade_name
        )

        self.legal_name = normalize_optional_text(
            self.legal_name
        )

        self.state_registration = (
            normalize_optional_text(
                self.state_registration
            )
        )

        self.website = normalize_optional_text(
            self.website
        )

        self.contact_name = normalize_optional_text(
            self.contact_name
        )

        self.street = normalize_optional_text(
            self.street
        )

        self.number = normalize_optional_text(
            self.number
        )

        self.district = normalize_optional_text(
            self.district
        )

        self.city = normalize_optional_text(
            self.city
        )

        self.document_number = (
            self._normalize_document(
                self.document_number
            )
        )

        self.email = self._normalize_email(
            self.email
        )

        self.invoice_email = self._normalize_email(
            self.invoice_email
        )

        self.phone = self._normalize_phone(
            self.phone
        )

        self.secondary_phone = (
            self._normalize_phone(
                self.secondary_phone
            )
        )

        self.postal_code = (
            self._normalize_postal_code(
                self.postal_code
            )
        )

        self.state = self._normalize_state(
            self.state
        )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        code: str,
        name: str,
        trade_name: str | None = None,
        legal_name: str | None = None,
        document_number: str | None = None,
        state_registration: str | None = None,
        email: str | None = None,
        invoice_email: str | None = None,
        phone: str | None = None,
        secondary_phone: str | None = None,
        website: str | None = None,
        contact_name: str | None = None,
        postal_code: str | None = None,
        street: str | None = None,
        number: str | None = None,
        district: str | None = None,
        city: str | None = None,
        state: str | None = None,
    ) -> Supplier:
        """Create a new active supplier."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            code=code,
            name=name,
            trade_name=trade_name,
            legal_name=legal_name,
            document_number=document_number,
            state_registration=state_registration,
            email=email,
            invoice_email=invoice_email,
            phone=phone,
            secondary_phone=secondary_phone,
            website=website,
            contact_name=contact_name,
            postal_code=postal_code,
            street=street,
            number=number,
            district=district,
            city=city,
            state=state,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def deactivate(self) -> None:
        """Deactivate the supplier."""

        if not self.is_active:
            return

        self.is_active = False
        self._touch()

    def activate(self) -> None:
        """Reactivate the supplier."""

        if self.is_active:
            return

        self.is_active = True
        self._touch()

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
                f"O {field_name} do fornecedor "
                "deve ser um UUID."
            )

        if value.int == 0:
            raise ValueError(
                f"O {field_name} do fornecedor "
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

        return SupplierDocument(
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

        return SupplierEmail(
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

        return SupplierPhone(
            normalized
        ).value

    @staticmethod
    def _normalize_postal_code(
        value: str | None,
    ) -> str | None:
        normalized = normalize_optional_text(
            value
        )

        if normalized is None:
            return None

        return SupplierPostalCode(
            normalized
        ).value

    @staticmethod
    def _normalize_state(
        value: str | None,
    ) -> str | None:
        normalized = normalize_optional_text(
            value
        )

        if normalized is None:
            return None

        return SupplierState(
            normalized
        ).value

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)
