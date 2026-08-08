"""SQLAlchemy ORM mapping for tenant suppliers."""

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


class SupplierModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Represent a supplier belonging to one tenant."""

    __tablename__ = "suppliers"

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
            "tenant_id",
            "code",
            name="uq_suppliers_tenant_code",
        ),
        UniqueConstraint(
            "tenant_id",
            "document_number",
            name="uq_suppliers_tenant_document_number",
        ),
        UniqueConstraint(
            "tenant_id",
            "legacy_supplier_id",
            name="uq_suppliers_tenant_legacy_supplier_id",
        ),
        Index(
            "ix_suppliers_tenant_active",
            "tenant_id",
            "is_active",
        ),
        Index(
            "ix_suppliers_tenant_name",
            "tenant_id",
            "name",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_suppliers_id_tenant",
        ),
    )

    legacy_supplier_id: Mapped[int | None] = mapped_column(
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

    trade_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    legal_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    document_number: Mapped[str | None] = mapped_column(
        String(14),
        nullable=True,
    )

    state_registration: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    invoice_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    secondary_phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    contact_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    postal_code: Mapped[str | None] = mapped_column(
        String(8),
        nullable=True,
    )

    street: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    district: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    state: Mapped[str | None] = mapped_column(
        String(2),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
