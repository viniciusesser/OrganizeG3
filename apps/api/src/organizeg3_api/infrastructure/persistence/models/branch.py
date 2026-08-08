"""SQLAlchemy ORM mapping for tenant branches."""

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


class BranchModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Represent an optional operational branch of one tenant."""

    __tablename__ = "branches"

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
            name="uq_branches_id_tenant",
        ),
        Index(
            "uq_branches_tenant_code_normalized",
            "tenant_id",
            text(
                "lower("
                "TRIM(BOTH FROM code)"
                ")"
            ),
            unique=True,
        ).ddl_if(
            dialect="postgresql"
        ),
        Index(
            "uq_branches_tenant_headquarters",
            "tenant_id",
            unique=True,
            postgresql_where=text(
                "is_headquarters = true"
            ),
            sqlite_where=text(
                "is_headquarters = 1"
            ),
        ),
        Index(
            "ix_branches_tenant_active",
            "tenant_id",
            "is_active",
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

    legal_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    document_number: Mapped[str | None] = mapped_column(
        String(20),
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

    is_headquarters: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
