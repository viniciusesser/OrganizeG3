"""Application schemas for employee operations."""

from __future__ import annotations

from datetime import date, datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field

from organizeg3_api.domain.employee.value_objects import (
    EmploymentStatus,
)


class EmployeeFields(BaseModel):
    """Shared employee input fields."""

    code: str = Field(
        min_length=1,
        max_length=100,
    )
    full_name: str = Field(
        min_length=1,
        max_length=255,
    )

    branch_id: uuid.UUID | None = None

    document_number: str | None = Field(
        default=None,
        max_length=30,
    )
    email: str | None = Field(
        default=None,
        max_length=255,
    )
    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    job_title: str | None = Field(
        default=None,
        max_length=255,
    )
    contract_type: str | None = Field(
        default=None,
        max_length=100,
    )

    birth_date: date | None = None
    admission_date: date | None = None


class EmployeeCreate(EmployeeFields):
    """Input used to create an employee."""


class EmployeeUpdate(BaseModel):
    """Partial employee update input."""

    code: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    full_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    branch_id: uuid.UUID | None = None

    document_number: str | None = Field(
        default=None,
        max_length=30,
    )

    email: str | None = Field(
        default=None,
        max_length=255,
    )

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    job_title: str | None = Field(
        default=None,
        max_length=255,
    )

    contract_type: str | None = Field(
        default=None,
        max_length=100,
    )

    birth_date: date | None = None
    admission_date: date | None = None


class EmployeeResponse(BaseModel):
    """Serialized employee representation."""

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID
    tenant_id: uuid.UUID
    branch_id: uuid.UUID | None

    code: str
    full_name: str

    document_number: str | None
    email: str | None
    phone: str | None

    job_title: str | None
    contract_type: str | None

    status: EmploymentStatus

    birth_date: date | None
    admission_date: date | None
    termination_date: date | None

    is_active: bool

    created_at: datetime | None
    updated_at: datetime | None
