"""SQLAlchemy ORM mapping for tenant material brands."""

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


class BrandModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Represent a material brand belonging to one tenant."""

    __tablename__ = "brands"

    __table_args__ = (
        CheckConstraint(
            "TRIM(code) <> ''",
            name="code_not_blank",
        ),
        CheckConstraint(
            "TRIM(name) <> ''",
            name="name_not_blank",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_brands_id_tenant",
        ),
        UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_brands_tenant_code",
        ),
        UniqueConstraint(
            "tenant_id",
            "name",
            name="uq_brands_tenant_name",
        ),
        UniqueConstraint(
            "tenant_id",
            "legacy_brand_id",
            name="uq_brands_tenant_legacy_brand_id",
        ),
        Index(
            "ix_brands_tenant_active",
            "tenant_id",
            "is_active",
        ),
    )

    legacy_brand_id: Mapped[int | None] = mapped_column(
        Integer,
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

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
