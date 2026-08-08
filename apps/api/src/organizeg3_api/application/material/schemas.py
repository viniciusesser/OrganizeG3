"""Material DTOs used by the application and HTTP layers."""

from __future__ import annotations

from datetime import datetime
import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class MaterialFields(BaseModel):
    """Shared writable material fields."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

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
    category: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    unit: str | None = Field(
        default=None,
        min_length=1,
        max_length=30,
    )
    brand_id: uuid.UUID | None = None


class MaterialCreate(BaseModel):
    """Payload accepted when creating a material."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    code: str = Field(
        min_length=1,
        max_length=100,
    )
    name: str = Field(
        min_length=1,
        max_length=255,
    )
    category: str = Field(
        min_length=1,
        max_length=100,
    )
    unit: str = Field(
        min_length=1,
        max_length=30,
    )
    brand_id: uuid.UUID | None = None


class MaterialUpdate(MaterialFields):
    """Partial material update payload."""


class MaterialResponse(BaseModel):
    """Material data exposed outside the application layer."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: uuid.UUID
    tenant_id: uuid.UUID

    code: str
    name: str
    category: str
    unit: str

    brand_id: uuid.UUID | None

    is_active: bool

    created_at: datetime
    updated_at: datetime
