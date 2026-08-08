"""SQLAlchemy ORM mapping for tenant services."""

from __future__ import annotations

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Index,
    Integer,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from organizeg3_api.infrastructure.database.base import (
    Base,
    TenantScopedMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class ServiceModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Represent a service catalog item belonging to one tenant."""

    __tablename__ = "services"

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
            "TRIM(category) <> ''",
            name="category_not_blank",
        ),
        CheckConstraint(
            "TRIM(unit) <> ''",
            name="unit_not_blank",
        ),
        CheckConstraint(
            (
                "execution_mode IN "
                "('INTERNAL', 'EXTERNAL', 'BOTH')"
            ),
            name="execution_mode_valid",
        ),
        CheckConstraint(
            (
                "estimated_duration_minutes IS NULL "
                "OR estimated_duration_minutes > 0"
            ),
            name="estimated_duration_positive",
        ),
        UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_services_tenant_code",
        ),
        Index(
            "ix_services_tenant_active",
            "tenant_id",
            "is_active",
        ),
        Index(
            "ix_services_tenant_name",
            "tenant_id",
            "name",
        ),
        Index(
            "ix_services_tenant_category",
            "tenant_id",
            "category",
        ),
        Index(
            "ix_services_tenant_execution_mode",
            "tenant_id",
            "execution_mode",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_services_id_tenant",
        ),
    )

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    unit: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    execution_mode: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    estimated_duration_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
