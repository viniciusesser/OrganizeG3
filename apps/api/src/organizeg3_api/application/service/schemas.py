"""Application schemas for tenant services."""

from __future__ import annotations

from datetime import datetime
import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from organizeg3_api.domain.service.value_objects import (
    ServiceExecutionMode,
)


class ServiceCreate(BaseModel):
    """Payload accepted when creating a service."""

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

    execution_mode: ServiceExecutionMode

    estimated_duration_minutes: int | None = Field(
        default=None,
        gt=0,
    )


class ServiceUpdate(BaseModel):
    """Partial service update payload."""

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

    execution_mode: ServiceExecutionMode | None = None

    estimated_duration_minutes: int | None = Field(
        default=None,
        gt=0,
    )


class ServiceResponse(BaseModel):
    """Response payload for one service."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: uuid.UUID
    tenant_id: uuid.UUID

    code: str
    name: str
    category: str
    unit: str

    execution_mode: ServiceExecutionMode

    estimated_duration_minutes: int | None

    is_active: bool

    created_at: datetime
    updated_at: datetime


__all__ = [
    "ServiceCreate",
    "ServiceResponse",
    "ServiceUpdate",
]
