"""SQLAlchemy ORM mapping for industrial machines."""

from __future__ import annotations

import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKeyConstraint,
    Index,
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


class MachineModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Represent an industrial machine belonging to one tenant."""

    __tablename__ = "machines"

    __table_args__ = (
        CheckConstraint(
            "TRIM(code) <> ''",
            name="code_not_blank",
        ),
        CheckConstraint(
            "TRIM(name) <> ''",
            name="name_not_blank",
        ),
        CheckConstraint(
            "TRIM(machine_type) <> ''",
            name="machine_type_not_blank",
        ),
        CheckConstraint(
            (
                "status IN "
                "('AVAILABLE', 'IN_USE', "
                "'MAINTENANCE', 'OUT_OF_SERVICE')"
            ),
            name="status_valid",
        ),
        UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_machines_tenant_code",
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
            name="fk_machines_branch_tenant",
        ),
        Index(
            "ix_machines_tenant_active",
            "tenant_id",
            "is_active",
        ),
        Index(
            "ix_machines_tenant_branch",
            "tenant_id",
            "branch_id",
        ),
        Index(
            "ix_machines_tenant_name",
            "tenant_id",
            "name",
        ),
        Index(
            "ix_machines_tenant_type",
            "tenant_id",
            "machine_type",
        ),
        Index(
            "ix_machines_tenant_status",
            "tenant_id",
            "status",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_machines_id_tenant",
        ),
    )

    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    machine_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    manufacturer: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    model: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    serial_number: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="AVAILABLE",
        server_default=text("'AVAILABLE'"),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
