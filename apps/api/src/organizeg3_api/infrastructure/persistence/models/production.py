"""SQLAlchemy ORM mappings for production core."""

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


class ProductionOrderModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one tenant-scoped production order."""

    __tablename__ = "production_orders"

    __table_args__ = (
        CheckConstraint(
            "TRIM(code) <> ''",
            name="code_not_blank",
        ),
        CheckConstraint(
            "TRIM(title) <> ''",
            name="title_not_blank",
        ),
        CheckConstraint(
            (
                "status IN ("
                "'PLANNED', "
                "'RELEASED', "
                "'IN_PROGRESS', "
                "'PAUSED', "
                "'COMPLETED', "
                "'CANCELLED'"
                ")"
            ),
            name="status_valid",
        ),
        CheckConstraint(
            (
                "priority IN ("
                "'LOW', "
                "'NORMAL', "
                "'HIGH', "
                "'URGENT'"
                ")"
            ),
            name="priority_valid",
        ),
        CheckConstraint(
            (
                "planned_end_at IS NULL "
                "OR planned_start_at IS NULL "
                "OR planned_end_at >= planned_start_at"
            ),
            name="planning_dates_valid",
        ),
        UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_production_orders_tenant_code",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_production_orders_id_tenant",
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
            name="fk_production_orders_branch_tenant",
        ),
        Index(
            "ix_production_orders_tenant_active",
            "tenant_id",
            "is_active",
        ),
        Index(
            "ix_production_orders_tenant_branch",
            "tenant_id",
            "branch_id",
        ),
        Index(
            "ix_production_orders_tenant_status",
            "tenant_id",
            "status",
        ),
        Index(
            "ix_production_orders_tenant_priority",
            "tenant_id",
            "priority",
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

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="PLANNED",
        server_default=text("'PLANNED'"),
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="NORMAL",
        server_default=text("'NORMAL'"),
    )

    planned_start_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    planned_end_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )


class ProductionOperationModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one operation of a production order."""

    __tablename__ = "production_operations"

    __table_args__ = (
        CheckConstraint(
            "sequence > 0",
            name="sequence_positive",
        ),
        CheckConstraint(
            "TRIM(name) <> ''",
            name="name_not_blank",
        ),
        CheckConstraint(
            (
                "status IN ("
                "'PENDING', "
                "'READY', "
                "'IN_PROGRESS', "
                "'PAUSED', "
                "'COMPLETED', "
                "'NOT_APPLICABLE', "
                "'CANCELLED'"
                ")"
            ),
            name="status_valid",
        ),
        CheckConstraint(
            (
                "(is_applicable = true "
                "AND status <> 'NOT_APPLICABLE') "
                "OR "
                "(is_applicable = false "
                "AND status = 'NOT_APPLICABLE')"
            ),
            name="applicability_status_consistent",
        ),
        UniqueConstraint(
            "production_order_id",
            "sequence",
            name="uq_production_operations_order_sequence",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_production_operations_id_tenant",
        ),
        UniqueConstraint(
            "id",
            "production_order_id",
            "tenant_id",
            name="uq_production_operations_id_order_tenant",
        ),
        ForeignKeyConstraint(
            [
                "production_order_id",
                "tenant_id",
            ],
            [
                "production_orders.id",
                "production_orders.tenant_id",
            ],
            name="fk_production_operations_order_tenant",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            [
                "service_id",
                "tenant_id",
            ],
            [
                "services.id",
                "services.tenant_id",
            ],
            name="fk_production_operations_service_tenant",
        ),
        ForeignKeyConstraint(
            [
                "machine_id",
                "tenant_id",
            ],
            [
                "machines.id",
                "machines.tenant_id",
            ],
            name="fk_production_operations_machine_tenant",
        ),
        Index(
            "ix_production_operations_tenant_order",
            "tenant_id",
            "production_order_id",
        ),
        Index(
            "ix_production_operations_tenant_status",
            "tenant_id",
            "status",
        ),
        Index(
            "ix_production_operations_tenant_service",
            "tenant_id",
            "service_id",
        ),
        Index(
            "ix_production_operations_tenant_machine",
            "tenant_id",
            "machine_id",
        ),
    )

    production_order_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    service_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )

    machine_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="PENDING",
        server_default=text("'PENDING'"),
    )

    is_applicable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )


class ProductionExecutionModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one employee execution of an operation."""

    __tablename__ = "production_executions"

    __table_args__ = (
        CheckConstraint(
            (
                "status IN ("
                "'RUNNING', "
                "'PAUSED', "
                "'COMPLETED', "
                "'CANCELLED'"
                ")"
            ),
            name="status_valid",
        ),
        CheckConstraint(
            (
                "finished_at IS NULL "
                "OR finished_at >= started_at"
            ),
            name="execution_dates_valid",
        ),
        CheckConstraint(
            (
                "(status = 'COMPLETED' "
                "AND finished_at IS NOT NULL) "
                "OR "
                "(status <> 'COMPLETED')"
            ),
            name="completed_has_finished_at",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_production_executions_id_tenant",
        ),
        UniqueConstraint(
            "id",
            "operation_id",
            "tenant_id",
            name="uq_production_executions_id_operation_tenant",
        ),
        ForeignKeyConstraint(
            [
                "operation_id",
                "tenant_id",
            ],
            [
                "production_operations.id",
                "production_operations.tenant_id",
            ],
            name="fk_production_executions_operation_tenant",
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
            name="fk_production_executions_employee_tenant",
        ),
        Index(
            "ix_production_executions_tenant_operation",
            "tenant_id",
            "operation_id",
        ),
        Index(
            "ix_production_executions_tenant_employee",
            "tenant_id",
            "employee_id",
        ),
        Index(
            "ix_production_executions_tenant_status",
            "tenant_id",
            "status",
        ),
        Index(
            "ix_production_executions_tenant_started",
            "tenant_id",
            "started_at",
        ),
    )

    operation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    employee_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="RUNNING",
        server_default=text("'RUNNING'"),
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class ProductionPauseModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one measurable pause during an execution."""

    __tablename__ = "production_pauses"

    __table_args__ = (
        CheckConstraint(
            "TRIM(reason_code) <> ''",
            name="reason_code_not_blank",
        ),
        CheckConstraint(
            (
                "ended_at IS NULL "
                "OR ended_at >= started_at"
            ),
            name="pause_dates_valid",
        ),
        ForeignKeyConstraint(
            [
                "execution_id",
                "tenant_id",
            ],
            [
                "production_executions.id",
                "production_executions.tenant_id",
            ],
            name="fk_production_pauses_execution_tenant",
            ondelete="CASCADE",
        ),
        Index(
            "ix_production_pauses_tenant_execution",
            "tenant_id",
            "execution_id",
        ),
        Index(
            "ix_production_pauses_tenant_reason",
            "tenant_id",
            "reason_code",
        ),
        Index(
            "ix_production_pauses_tenant_started",
            "tenant_id",
            "started_at",
        ),
    )

    execution_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    reason_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class ProductionEventModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one operational production event."""

    __tablename__ = "production_events"

    __table_args__ = (
        CheckConstraint(
            "TRIM(event_type) <> ''",
            name="event_type_not_blank",
        ),
        CheckConstraint(
            (
                "execution_id IS NULL "
                "OR operation_id IS NOT NULL"
            ),
            name="execution_requires_operation",
        ),
        ForeignKeyConstraint(
            [
                "production_order_id",
                "tenant_id",
            ],
            [
                "production_orders.id",
                "production_orders.tenant_id",
            ],
            name="fk_production_events_order_tenant",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            [
                "operation_id",
                "production_order_id",
                "tenant_id",
            ],
            [
                "production_operations.id",
                "production_operations.production_order_id",
                "production_operations.tenant_id",
            ],
            name="fk_production_events_operation_order_tenant",
        ),
        ForeignKeyConstraint(
            [
                "execution_id",
                "operation_id",
                "tenant_id",
            ],
            [
                "production_executions.id",
                "production_executions.operation_id",
                "production_executions.tenant_id",
            ],
            name="fk_production_events_execution_operation_tenant",
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
            name="fk_production_events_employee_tenant",
        ),
        Index(
            "ix_production_events_tenant_order",
            "tenant_id",
            "production_order_id",
        ),
        Index(
            "ix_production_events_tenant_operation",
            "tenant_id",
            "operation_id",
        ),
        Index(
            "ix_production_events_tenant_execution",
            "tenant_id",
            "execution_id",
        ),
        Index(
            "ix_production_events_tenant_employee",
            "tenant_id",
            "employee_id",
        ),
        Index(
            "ix_production_events_tenant_type",
            "tenant_id",
            "event_type",
        ),
        Index(
            "ix_production_events_tenant_occurred",
            "tenant_id",
            "occurred_at",
        ),
    )

    production_order_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    operation_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )

    execution_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )

    employee_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    reason_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
