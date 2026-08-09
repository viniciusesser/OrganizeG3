"""Repository contract for append-only business audit events."""

from __future__ import annotations

from typing import Protocol
import uuid

from organizeg3_api.domain.audit.event import (
    AuditEvent,
)


class AuditEventRepository(Protocol):
    """Persistence port for the append-only audit trail."""

    def append(
        self,
        event: AuditEvent,
    ) -> AuditEvent:
        """Persist one immutable audit event."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        event_id: uuid.UUID,
    ) -> AuditEvent | None:
        """Return one event within its tenant boundary."""

    def list_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        resource: str | None = None,
        resource_id: str | None = None,
        correlation_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[AuditEvent]:
        """List audit events without exposing cross-tenant data."""


__all__ = [
    "AuditEventRepository",
]
