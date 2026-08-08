"""SQLAlchemy ORM mapping for tenant employees."""

from __future__ import annotations

from datetime import date
import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from organizeg3_api.infrastructure.database.base import (
    Base,
    TenantScopedMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class EmployeeModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Represent an employee belonging to one tenant."""

    __tablename__ = "employees"

    __table_args__ = (
        CheckConstraint(
            "TRIM(code) <> ''",
            name="code_not_blank",
        ),
        CheckConstraint(
            "TRIM(full_name) <> ''",
            name="full_name_not_blank",
        ),
        CheckConstraint(
            (
                "status IN ("
                "'ACTIVE', "
                "'ON_LEAVE', "
                "'INACTIVE', "
                "'TERMINATED'"
                ")"
            ),
            name="status_valid",
        ),
        UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_employees_tenant_code",
        ),
        UniqueConstraint(
            "tenant_id",
            "document_number",
            name="uq_employees_tenant_document_number",
        ),
        UniqueConstraint(
            "tenant_id",
            "legacy_employee_id",
            name="uq_employees_tenant_legacy_employee_id",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_employees_id_tenant",
        ),
        ForeignKeyConstraint(
            [
                "branch_id",
                "tenant_id",
            ],
            [
                "branches.id",
                "branches.tenant_id",
            ],
            name="fk_employees_branch_tenant",
        ),
        Index(
            "ix_employees_tenant_active",
            "tenant_id",
            "is_active",
        ),
        Index(
            "ix_employees_tenant_status",
            "tenant_id",
            "status",
        ),
        Index(
            "ix_employees_tenant_branch",
            "tenant_id",
            "branch_id",
        ),
    )

    legacy_employee_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    document_number: Mapped[str | None] = mapped_column(
        String(11),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    job_title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    contract_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="ACTIVE",
        server_default=text("'ACTIVE'"),
    )

    birth_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    admission_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    termination_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
