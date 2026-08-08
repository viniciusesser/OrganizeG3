"""SQLAlchemy mappings for production assignments and checklists."""

from __future__ import annotations

from datetime import datetime
import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
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


class ProductionAssignmentModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one employee assignment to a production operation."""

    __tablename__ = "production_assignments"

    __table_args__ = (
        CheckConstraint(
            (
                "unassigned_at IS NULL "
                "OR unassigned_at >= assigned_at"
            ),
            name="assignment_dates_valid",
        ),
        CheckConstraint(
            (
                "(is_active = true AND unassigned_at IS NULL) "
                "OR "
                "(is_active = false AND unassigned_at IS NOT NULL)"
            ),
            name="active_state_valid",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_production_assignments_id_tenant",
        ),
        ForeignKeyConstraint(
            [
                "production_operation_id",
                "tenant_id",
            ],
            [
                "production_operations.id",
                "production_operations.tenant_id",
            ],
            name=(
                "fk_production_assignments_"
                "operation_tenant"
            ),
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            [
                "employee_id",
                "tenant_id",
            ],
            [
                "employees.id",
                "employees.tenant_id",
            ],
            name=(
                "fk_production_assignments_"
                "employee_tenant"
            ),
        ),
        ForeignKeyConstraint(
            [
                "assigned_by_user_id",
            ],
            [
                "users.id",
            ],
            name=(
                "fk_production_assignments_"
                "assigned_by_user"
            ),
        ),
        Index(
            "ix_production_assignments_tenant_operation",
            "tenant_id",
            "production_operation_id",
        ),
        Index(
            "ix_production_assignments_tenant_employee",
            "tenant_id",
            "employee_id",
        ),
        Index(
            "ix_production_assignments_tenant_active",
            "tenant_id",
            "is_active",
        ),
        Index(
            "ix_production_assignments_tenant_assigned",
            "tenant_id",
            "assigned_at",
        ),
        Index(
            "uq_production_assignments_active_employee",
            "tenant_id",
            "production_operation_id",
            "employee_id",
            unique=True,
            postgresql_where=text("is_active = true"),
            sqlite_where=text("is_active = 1"),
        ),
    )

    production_operation_id: Mapped[
        uuid.UUID
    ] = mapped_column(
        Uuid,
        nullable=False,
    )

    employee_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    assigned_by_user_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    unassigned_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )


class ProductionChecklistItemModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one checklist item of a production operation."""

    __tablename__ = "production_checklist_items"

    __table_args__ = (
        CheckConstraint(
            "sequence > 0",
            name="sequence_positive",
        ),
        CheckConstraint(
            "TRIM(title) <> ''",
            name="title_not_blank",
        ),
        CheckConstraint(
            (
                "completed_by_employee_id IS NULL "
                "OR completed_at IS NOT NULL"
            ),
            name="completion_employee_requires_date",
        ),
        CheckConstraint(
            (
                "is_applicable = true "
                "OR "
                "("
                "completed_at IS NULL "
                "AND completed_by_employee_id IS NULL"
                ")"
            ),
            name="not_applicable_not_completed",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_production_checklist_items_id_tenant",
        ),
        UniqueConstraint(
            "production_operation_id",
            "sequence",
            name=(
                "uq_production_checklist_items_"
                "operation_sequence"
            ),
        ),
        ForeignKeyConstraint(
            [
                "production_operation_id",
                "tenant_id",
            ],
            [
                "production_operations.id",
                "production_operations.tenant_id",
            ],
            name=(
                "fk_production_checklist_items_"
                "operation_tenant"
            ),
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            [
                "completed_by_employee_id",
                "tenant_id",
            ],
            [
                "employees.id",
                "employees.tenant_id",
            ],
            name=(
                "fk_production_checklist_items_"
                "employee_tenant"
            ),
        ),
        Index(
            "ix_production_checklist_items_tenant_operation",
            "tenant_id",
            "production_operation_id",
        ),
        Index(
            "ix_production_checklist_items_tenant_completed_by",
            "tenant_id",
            "completed_by_employee_id",
        ),
        Index(
            "ix_production_checklist_items_tenant_applicable",
            "tenant_id",
            "is_applicable",
        ),
    )

    production_operation_id: Mapped[
        uuid.UUID
    ] = mapped_column(
        Uuid,
        nullable=False,
    )

    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    is_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )

    is_applicable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )

    completed_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_by_employee_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        String(4000),
        nullable=True,
    )
