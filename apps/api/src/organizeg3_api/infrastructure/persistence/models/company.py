"""SQLAlchemy ORM mapping for tenant companies."""

from __future__ import annotations

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Index,
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


class CompanyModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Represent the business company owned by one tenant."""

    __tablename__ = "companies"

    __table_args__ = (
        CheckConstraint(
            "TRIM(trade_name) <> ''",
            name="trade_name_not_blank",
        ),
        UniqueConstraint(
            "tenant_id",
            name="uq_companies_tenant_id",
        ),
        Index(
            "uq_companies_document_number_normalized",
            text("NULLIF(TRIM(BOTH FROM document_number), '')"),
            unique=True,
        ).ddl_if(
            dialect="postgresql"
        ),
        Index(
            "ix_companies_tenant_active",
            "tenant_id",
            "is_active",
        ),
    )

    trade_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
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

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    logo_path: Mapped[str | None] = mapped_column(
        String(1024),
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

    postal_code: Mapped[str | None] = mapped_column(
        String(8),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
