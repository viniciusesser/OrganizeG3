"""Application schemas for branch operations."""

from __future__ import annotations

from datetime import datetime
import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from organizeg3_api.domain.branch.value_objects import (
    BranchCode,
    BranchDocument,
    BranchEmail,
    BranchPhone,
    BranchPostalCode,
    BranchState,
    normalize_optional_text,
)


class BranchFields(BaseModel):
    """Fields shared by branch create and update requests."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    code: str | None = Field(
        default=None,
        max_length=100,
    )
    name: str | None = Field(
        default=None,
        max_length=255,
    )

    legal_name: str | None = Field(
        default=None,
        max_length=255,
    )
    document_number: str | None = Field(
        default=None,
        max_length=20,
    )
    state_registration: str | None = Field(
        default=None,
        max_length=50,
    )

    email: str | None = Field(
        default=None,
        max_length=255,
    )
    phone: str | None = Field(
        default=None,
        max_length=20,
    )
    website: str | None = Field(
        default=None,
        max_length=500,
    )

    street: str | None = Field(
        default=None,
        max_length=255,
    )
    number: str | None = Field(
        default=None,
        max_length=50,
    )
    district: str | None = Field(
        default=None,
        max_length=255,
    )
    city: str | None = Field(
        default=None,
        max_length=255,
    )
    state: str | None = Field(
        default=None,
        max_length=2,
    )
    postal_code: str | None = Field(
        default=None,
        max_length=20,
    )

    is_headquarters: bool | None = None

    @field_validator(
        "code",
    )
    @classmethod
    def normalize_code(
        cls,
        value: str | None,
    ) -> str | None:
        """Normalize an optional branch code."""

        normalized = normalize_optional_text(
            value
        )

        if normalized is None:
            return None

        return BranchCode(
            normalized
        ).value

    @field_validator(
        "name",
        "legal_name",
        "state_registration",
        "website",
        "street",
        "number",
        "district",
        "city",
    )
    @classmethod
    def normalize_text(
        cls,
        value: str | None,
    ) -> str | None:
        """Normalize optional textual values."""

        return normalize_optional_text(
            value
        )

    @field_validator(
        "document_number",
    )
    @classmethod
    def normalize_document(
        cls,
        value: str | None,
    ) -> str | None:
        """Normalize an optional branch document."""

        normalized = normalize_optional_text(
            value
        )

        if normalized is None:
            return None

        return BranchDocument(
            normalized
        ).value

    @field_validator(
        "email",
    )
    @classmethod
    def normalize_email(
        cls,
        value: str | None,
    ) -> str | None:
        """Normalize an optional branch e-mail."""

        normalized = normalize_optional_text(
            value
        )

        if normalized is None:
            return None

        return BranchEmail(
            normalized
        ).value

    @field_validator(
        "phone",
    )
    @classmethod
    def normalize_phone(
        cls,
        value: str | None,
    ) -> str | None:
        """Normalize an optional branch phone."""

        normalized = normalize_optional_text(
            value
        )

        if normalized is None:
            return None

        return BranchPhone(
            normalized
        ).value

    @field_validator(
        "state",
    )
    @classmethod
    def normalize_state(
        cls,
        value: str | None,
    ) -> str | None:
        """Normalize an optional state code."""

        normalized = normalize_optional_text(
            value
        )

        if normalized is None:
            return None

        return BranchState(
            normalized
        ).value

    @field_validator(
        "postal_code",
    )
    @classmethod
    def normalize_postal_code(
        cls,
        value: str | None,
    ) -> str | None:
        """Normalize an optional postal code."""

        normalized = normalize_optional_text(
            value
        )

        if normalized is None:
            return None

        return BranchPostalCode(
            normalized
        ).value


class BranchCreate(BranchFields):
    """Payload used to create a branch."""

    code: str = Field(
        min_length=1,
        max_length=100,
    )
    name: str = Field(
        min_length=1,
        max_length=255,
    )
    is_headquarters: bool = False


class BranchUpdate(BranchFields):
    """Payload used for partial branch updates."""


class BranchResponse(BaseModel):
    """Public representation of one branch."""

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID
    tenant_id: uuid.UUID

    code: str
    name: str

    legal_name: str | None
    document_number: str | None
    state_registration: str | None

    email: str | None
    phone: str | None
    website: str | None

    street: str | None
    number: str | None
    district: str | None
    city: str | None
    state: str | None
    postal_code: str | None

    is_headquarters: bool
    is_active: bool

    created_at: datetime | None
    updated_at: datetime | None
