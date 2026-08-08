"""SQLAlchemy ORM mapping for the platform tenant table."""

from __future__ import annotations

from datetime import UTC, datetime
import uuid

from sqlalchemy import (
    Boolean,
    DateTime,
    Index,
    Integer,
    String,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from organizeg3_api.infrastructure.database.base import Base


class TenantRecordModel(Base):
    """Map an organization registered in the OrganizeG3 platform."""

    __tablename__ = "tenants"

    __table_args__ = (
        UniqueConstraint(
            "legacy_config_id",
            name="uq_tenants_legacy_config_id",
        ),
        UniqueConstraint(
            "document_number",
            name="uq_tenants_document_number",
        ),
        Index(
            "ix_tenants_is_active",
            "is_active",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    legacy_config_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
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
        String(14),
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

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="ACTIVE",
        server_default=text("'ACTIVE'"),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        server_default=text("CURRENT_TIMESTAMP"),
    )
