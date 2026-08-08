"""Application schemas for supplier operations."""

from __future__ import annotations

from datetime import datetime
import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class SupplierFields(BaseModel):
    """Reusable writable supplier fields."""

    trade_name: str | None = Field(
        default=None,
        max_length=255,
    )

    legal_name: str | None = Field(
        default=None,
        max_length=255,
    )

    document_number: str | None = Field(
        default=None,
        max_length=32,
    )

    state_registration: str | None = Field(
        default=None,
        max_length=50,
    )

    email: str | None = Field(
        default=None,
        max_length=255,
    )

    invoice_email: str | None = Field(
        default=None,
        max_length=255,
    )

    phone: str | None = Field(
        default=None,
        max_length=32,
    )

    secondary_phone: str | None = Field(
        default=None,
        max_length=32,
    )

    website: str | None = Field(
        default=None,
        max_length=500,
    )

    contact_name: str | None = Field(
        default=None,
        max_length=255,
    )

    postal_code: str | None = Field(
        default=None,
        max_length=16,
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


class SupplierCreate(SupplierFields):
    """Payload used to create a supplier."""

    code: str = Field(
        min_length=1,
        max_length=100,
    )

    name: str = Field(
        min_length=1,
        max_length=255,
    )


class SupplierUpdate(BaseModel):
    """Partial supplier update payload."""

    code: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    trade_name: str | None = Field(
        default=None,
        max_length=255,
    )

    legal_name: str | None = Field(
        default=None,
        max_length=255,
    )

    document_number: str | None = Field(
        default=None,
        max_length=32,
    )

    state_registration: str | None = Field(
        default=None,
        max_length=50,
    )

    email: str | None = Field(
        default=None,
        max_length=255,
    )

    invoice_email: str | None = Field(
        default=None,
        max_length=255,
    )

    phone: str | None = Field(
        default=None,
        max_length=32,
    )

    secondary_phone: str | None = Field(
        default=None,
        max_length=32,
    )

    website: str | None = Field(
        default=None,
        max_length=500,
    )

    contact_name: str | None = Field(
        default=None,
        max_length=255,
    )

    postal_code: str | None = Field(
        default=None,
        max_length=16,
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


class SupplierResponse(BaseModel):
    """Serialized supplier representation."""

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID
    tenant_id: uuid.UUID

    code: str
    name: str

    trade_name: str | None
    legal_name: str | None

    document_number: str | None
    state_registration: str | None

    email: str | None
    invoice_email: str | None

    phone: str | None
    secondary_phone: str | None

    website: str | None
    contact_name: str | None

    postal_code: str | None
    street: str | None
    number: str | None
    district: str | None
    city: str | None
    state: str | None

    is_active: bool

    created_at: datetime
    updated_at: datetime
