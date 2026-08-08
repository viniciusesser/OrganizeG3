"""SQLAlchemy ORM mapping for tenant materials."""

from __future__ import annotations

import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
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


class MaterialModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Represent a material catalog item belonging to one tenant."""

    __tablename__ = "materials"

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
        UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_materials_tenant_code",
        ),
        UniqueConstraint(
            "tenant_id",
            "legacy_material_id",
            name="uq_materials_tenant_legacy_material_id",
        ),
        ForeignKeyConstraint(
            [
                "brand_id",
                "tenant_id",
            ],
            [
                "brands.id",
                "brands.tenant_id",
            ],
            name="fk_materials_brand_tenant",
        ),
        Index(
            "ix_materials_tenant_active",
            "tenant_id",
            "is_active",
        ),
        Index(
            "ix_materials_tenant_name",
            "tenant_id",
            "name",
        ),
        Index(
            "ix_materials_tenant_category",
            "tenant_id",
            "category",
        ),
        Index(
            "ix_materials_tenant_brand",
            "tenant_id",
            "brand_id",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_materials_id_tenant",
        ),
    )

    legacy_material_id: Mapped[int | None] = mapped_column(
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

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    unit: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    brand_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
