"""Application schemas for industrial machines."""

from __future__ import annotations

from datetime import datetime
import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from organizeg3_api.domain.machine.value_objects import (
    MachineStatus,
)


class MachineCreate(BaseModel):
    """Input used to create a tenant machine."""

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
    machine_type: str = Field(
        min_length=1,
        max_length=100,
    )

    branch_id: uuid.UUID | None = None

    manufacturer: str | None = Field(
        default=None,
        max_length=255,
    )
    model: str | None = Field(
        default=None,
        max_length=255,
    )
    serial_number: str | None = Field(
        default=None,
        max_length=255,
    )


class MachineUpdate(BaseModel):
    """Input used to update machine registration data."""

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
    machine_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    branch_id: uuid.UUID | None = None

    manufacturer: str | None = Field(
        default=None,
        max_length=255,
    )
    model: str | None = Field(
        default=None,
        max_length=255,
    )
    serial_number: str | None = Field(
        default=None,
        max_length=255,
    )


class MachineStatusUpdate(BaseModel):
    """Input used to change operational machine status."""

    model_config = ConfigDict(
        extra="forbid",
    )

    status: MachineStatus


class MachineResponse(BaseModel):
    """Public machine representation."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: uuid.UUID
    tenant_id: uuid.UUID

    code: str
    name: str
    machine_type: str

    status: MachineStatus

    branch_id: uuid.UUID | None

    manufacturer: str | None
    model: str | None
    serial_number: str | None

    is_active: bool

    created_at: datetime
    updated_at: datetime


__all__ = [
    "MachineCreate",
    "MachineResponse",
    "MachineStatusUpdate",
    "MachineUpdate",
]
