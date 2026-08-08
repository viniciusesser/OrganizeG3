"""Company domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import uuid

from organizeg3_api.domain.company.value_objects import (
    CompanyDocument,
    CompanyEmail,
    CompanyPhone,
    PostalCode,
    normalize_optional_text,
)

_STATE_CODE_LENGTH = 2


@dataclass(slots=True)
class Company:
    """Represent the business organization owned by one tenant."""

    tenant_id: uuid.UUID
    trade_name: str
    id: uuid.UUID | None = None

    legal_name: str | None = None
    document_number: str | None = None
    state_registration: str | None = None

    email: str | None = None
    phone: str | None = None
    website: str | None = None
    logo_path: str | None = None

    street: str | None = None
    number: str | None = None
    district: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None

    is_active: bool = True

    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        """Validate and normalize company state."""

        if not isinstance(
            self.tenant_id,
            uuid.UUID,
        ):
            raise TypeError(
                "O tenant da empresa deve ser um UUID."
            )

        if self.tenant_id.int == 0:
            raise ValueError(
                "O tenant da empresa não pode possuir UUID nulo."
            )

        if (
            self.id is not None
            and not isinstance(
                self.id,
                uuid.UUID,
            )
        ):
            raise TypeError(
                "O identificador da empresa deve ser um UUID."
            )

        if (
            self.id is not None
            and self.id.int == 0
        ):
            raise ValueError(
                "O identificador da empresa não pode possuir UUID nulo."
            )

        self.trade_name = self.trade_name.strip()

        if not self.trade_name:
            raise ValueError(
                "O nome fantasia da empresa é obrigatório."
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

        self.logo_path = normalize_optional_text(
            self.logo_path
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

        normalized_state = normalize_optional_text(
            self.state
        )

        if normalized_state is not None:
            normalized_state = normalized_state.upper()

            if (
                len(normalized_state)
                != _STATE_CODE_LENGTH
            ):
                raise ValueError(
                    "O estado da empresa deve utilizar a sigla UF."
                )

        self.state = normalized_state

        if self.document_number is not None:
            normalized_document = (
                normalize_optional_text(
                    self.document_number
                )
            )

            self.document_number = (
                CompanyDocument(
                    normalized_document
                ).value
                if normalized_document
                is not None
                else None
            )

        if self.email is not None:
            normalized_email = (
                normalize_optional_text(
                    self.email
                )
            )

            self.email = (
                CompanyEmail(
                    normalized_email
                ).value
                if normalized_email
                is not None
                else None
            )

        if self.phone is not None:
            normalized_phone = (
                normalize_optional_text(
                    self.phone
                )
            )

            self.phone = (
                CompanyPhone(
                    normalized_phone
                ).value
                if normalized_phone
                is not None
                else None
            )

        if self.postal_code is not None:
            normalized_postal_code = (
                normalize_optional_text(
                    self.postal_code
                )
            )

            self.postal_code = (
                PostalCode(
                    normalized_postal_code
                ).value
                if normalized_postal_code
                is not None
                else None
            )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        trade_name: str,
        legal_name: str | None = None,
        document_number: str | None = None,
        state_registration: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        website: str | None = None,
        logo_path: str | None = None,
        street: str | None = None,
        number: str | None = None,
        district: str | None = None,
        city: str | None = None,
        state: str | None = None,
        postal_code: str | None = None,
    ) -> Company:
        """Create a new active company."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            trade_name=trade_name,
            legal_name=legal_name,
            document_number=document_number,
            state_registration=state_registration,
            email=email,
            phone=phone,
            website=website,
            logo_path=logo_path,
            street=street,
            number=number,
            district=district,
            city=city,
            state=state,
            postal_code=postal_code,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
