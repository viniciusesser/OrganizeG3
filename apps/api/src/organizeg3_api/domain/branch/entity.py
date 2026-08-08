"""Branch domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import uuid

from organizeg3_api.domain.branch.value_objects import (
    BranchCode,
    BranchDocument,
    BranchEmail,
    BranchPhone,
    BranchPostalCode,
    BranchState,
    normalize_optional_text,
)


@dataclass(slots=True)
class Branch:
    """Represent one optional operational unit of a tenant."""

    tenant_id: uuid.UUID
    code: str
    name: str

    id: uuid.UUID | None = None

    legal_name: str | None = None
    document_number: str | None = None
    state_registration: str | None = None

    email: str | None = None
    phone: str | None = None
    website: str | None = None

    street: str | None = None
    number: str | None = None
    district: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None

    is_headquarters: bool = False
    is_active: bool = True

    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        """Validate and normalize branch state."""

        if not isinstance(
            self.tenant_id,
            uuid.UUID,
        ):
            raise TypeError(
                "O tenant da filial deve ser um UUID."
            )

        if self.tenant_id.int == 0:
            raise ValueError(
                "O tenant da filial não pode possuir UUID nulo."
            )

        if (
            self.id is not None
            and not isinstance(
                self.id,
                uuid.UUID,
            )
        ):
            raise TypeError(
                "O identificador da filial deve ser um UUID."
            )

        if (
            self.id is not None
            and self.id.int == 0
        ):
            raise ValueError(
                "O identificador da filial não pode "
                "possuir UUID nulo."
            )

        self.code = BranchCode(
            self.code
        ).value

        self.name = self.name.strip()

        if not self.name:
            raise ValueError(
                "O nome da filial é obrigatório."
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

        if self.document_number is not None:
            normalized_document = (
                normalize_optional_text(
                    self.document_number
                )
            )

            self.document_number = (
                BranchDocument(
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
                BranchEmail(
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
                BranchPhone(
                    normalized_phone
                ).value
                if normalized_phone
                is not None
                else None
            )

        if self.state is not None:
            normalized_state = (
                normalize_optional_text(
                    self.state
                )
            )

            self.state = (
                BranchState(
                    normalized_state
                ).value
                if normalized_state
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
                BranchPostalCode(
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
        code: str,
        name: str,
        legal_name: str | None = None,
        document_number: str | None = None,
        state_registration: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        website: str | None = None,
        street: str | None = None,
        number: str | None = None,
        district: str | None = None,
        city: str | None = None,
        state: str | None = None,
        postal_code: str | None = None,
        is_headquarters: bool = False,
    ) -> Branch:
        """Create a new active branch."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            code=code,
            name=name,
            legal_name=legal_name,
            document_number=document_number,
            state_registration=state_registration,
            email=email,
            phone=phone,
            website=website,
            street=street,
            number=number,
            district=district,
            city=city,
            state=state,
            postal_code=postal_code,
            is_headquarters=is_headquarters,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def deactivate(self) -> None:
        """Deactivate the branch."""

        if not self.is_active:
            return

        self.is_active = False
        self.updated_at = datetime.now(UTC)

    def activate(self) -> None:
        """Reactivate the branch."""

        if self.is_active:
            return

        self.is_active = True
        self.updated_at = datetime.now(UTC)
