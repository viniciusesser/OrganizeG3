"""Company DTOs used by the application and HTTP layers."""

from __future__ import annotations

from typing import Self
import uuid

from pydantic import BaseModel, ConfigDict, Field, model_validator

from organizeg3_api.domain.company.value_objects import (
    CompanyDocument,
    CompanyEmail,
    CompanyPhone,
    PostalCode,
)

_STATE_CODE_LENGTH = 2


class CompanyContactFields(BaseModel):
    """Shared company identity, contact and address fields."""

    document_number: str | None = Field(
        default=None,
        max_length=30,
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
        max_length=50,
    )
    website: str | None = Field(
        default=None,
        max_length=500,
    )
    logo_path: str | None = Field(
        default=None,
        max_length=1024,
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
        max_length=_STATE_CODE_LENGTH,
    )
    postal_code: str | None = Field(
        default=None,
        max_length=20,
    )

    @model_validator(mode="after")
    def normalize_domain_values(
        self,
    ) -> Self:
        """Normalize fields using canonical domain value objects."""

        if self.document_number is not None:
            normalized = self.document_number.strip()
            self.document_number = (
                CompanyDocument(normalized).value
                if normalized
                else None
            )

        if self.email is not None:
            normalized = self.email.strip()
            self.email = (
                CompanyEmail(normalized).value
                if normalized
                else None
            )

        if self.phone is not None:
            normalized = self.phone.strip()
            self.phone = (
                CompanyPhone(normalized).value
                if normalized
                else None
            )

        if self.postal_code is not None:
            normalized = self.postal_code.strip()
            self.postal_code = (
                PostalCode(normalized).value
                if normalized
                else None
            )

        if self.state is not None:
            normalized_state = self.state.strip().upper()

            if (
                normalized_state
                and len(normalized_state)
                != _STATE_CODE_LENGTH
            ):
                raise ValueError(
                    "O estado da empresa deve utilizar a sigla UF."
                )

            self.state = normalized_state or None

        return self


class CompanyCreate(CompanyContactFields):
    """Payload accepted when creating the tenant company."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    trade_name: str = Field(
        min_length=1,
        max_length=255,
    )
    legal_name: str | None = Field(
        default=None,
        max_length=255,
    )


class CompanyUpdate(CompanyContactFields):
    """Partial payload accepted when updating the tenant company."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    trade_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    legal_name: str | None = Field(
        default=None,
        max_length=255,
    )


class CompanyResponse(BaseModel):
    """Response contract for the company owned by the tenant."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: uuid.UUID
    tenant_id: uuid.UUID

    trade_name: str
    legal_name: str | None
    document_number: str | None
    state_registration: str | None

    email: str | None
    phone: str | None
    website: str | None
    logo_path: str | None

    street: str | None
    number: str | None
    district: str | None
    city: str | None
    state: str | None
    postal_code: str | None

    is_active: bool
