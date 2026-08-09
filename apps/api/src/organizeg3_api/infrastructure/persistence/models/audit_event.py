"""SQLAlchemy mapping for immutable business audit events."""

from __future__ import annotations

from datetime import datetime
from typing import Any
import uuid

from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from organizeg3_api.infrastructure.database.base import (
    Base,
    UUIDPrimaryKeyMixin,
)


class AuditEventModel(
    UUIDPrimaryKeyMixin,
    Base,
):
    """Persist one append-only business audit event."""

    __tablename__ = "audit_events"

    __table_args__ = (
        CheckConstraint(
            "TRIM(action) <> ''",
            name="action_not_blank",
        ),
        CheckConstraint(
            "TRIM(resource) <> ''",
            name="resource_not_blank",
        ),
        CheckConstraint(
            "TRIM(resource_id) <> ''",
            name="resource_id_not_blank",
        ),
        CheckConstraint(
            "TRIM(correlation_id) <> ''",
            name="correlation_id_not_blank",
        ),
        Index(
            "ix_audit_events_tenant_occurred",
            "tenant_id",
            "occurred_at",
        ),
        Index(
            "ix_audit_events_tenant_resource",
            "tenant_id",
            "resource",
            "resource_id",
        ),
        Index(
            "ix_audit_events_tenant_actor",
            "tenant_id",
            "actor_user_id",
            "occurred_at",
        ),
        Index(
            "ix_audit_events_tenant_correlation",
            "tenant_id",
            "correlation_id",
        ),
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "tenants.id",
        ),
        nullable=False,
        index=True,
    )

    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    actor_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    membership_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    auth_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    resource: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    resource_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    correlation_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    device_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    before_snapshot: Mapped[dict[str, Any] | None] = mapped_column(
        "before",
        JSON,
        nullable=True,
    )

    after_snapshot: Mapped[dict[str, Any] | None] = mapped_column(
        "after",
        JSON,
        nullable=True,
    )

    event_metadata: Mapped[dict[str, Any] | None] = mapped_column(
        "metadata",
        JSON,
        nullable=True,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
