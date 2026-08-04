"""SQLAlchemy declarative base and persistence mixins.

This module contains only persistence infrastructure. Domain entities must not
inherit from these classes or depend on SQLAlchemy.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import ClassVar
import uuid

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


metadata = MetaData(naming_convention=NAMING_CONVENTION)


def utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(UTC)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy persistence models."""

    metadata = metadata


class UUIDPrimaryKeyMixin:
    """Provide a UUID primary key."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


class TenantScopedMixin:
    """Associate a persistence record with exactly one tenant."""

    @declared_attr.directive
    def tenant_id(self) -> Mapped[uuid.UUID]:
        """Return the tenant foreign-key column."""

        return mapped_column(
            UUID(as_uuid=True),
            ForeignKey(
                "tenants.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            index=True,
        )


class TimestampMixin:
    """Provide creation and update timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )


class ActorAuditMixin:
    """Record the users responsible for creating and updating a record."""

    @declared_attr.directive
    def created_by_user_id(self) -> Mapped[uuid.UUID | None]:
        """Return the creator user foreign-key column."""

        return mapped_column(
            UUID(as_uuid=True),
            ForeignKey(
                "users.id",
                ondelete="SET NULL",
            ),
            nullable=True,
        )

    @declared_attr.directive
    def updated_by_user_id(self) -> Mapped[uuid.UUID | None]:
        """Return the updater user foreign-key column."""

        return mapped_column(
            UUID(as_uuid=True),
            ForeignKey(
                "users.id",
                ondelete="SET NULL",
            ),
            nullable=True,
        )


class ArchivableMixin:
    """Provide logical archival without destroying business history."""

    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class SoftDeleteMixin:
    """Provide logical deletion for records that support it."""

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class OptimisticLockMixin:
    """Provide a version column for optimistic concurrency control."""

    row_version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    __mapper_args__: ClassVar[dict[str, object]] = {
        "version_id_col": row_version,
    }


class ActiveStatusMixin:
    """Provide a simple active/inactive flag for configurable records."""

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )


class CodeMixin:
    """Provide a reusable internal business code."""

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


class TenantModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    ActorAuditMixin,
    ArchivableMixin,
    SoftDeleteMixin,
    OptimisticLockMixin,
    ActiveStatusMixin,
):
    """Base mixin composition for ordinary tenant-owned records."""

    __abstract__ = True
