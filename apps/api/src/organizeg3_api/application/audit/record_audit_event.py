"""Application use case for recording one business audit event."""

from __future__ import annotations

from collections.abc import Mapping

from pydantic import BaseModel

from organizeg3_api.application.audit.factory import (
    AuditEventFactory,
)
from organizeg3_api.domain.audit import (
    AuditAction,
    AuditContext,
    AuditEvent,
    AuditEventRepository,
)


class RecordAuditEvent:
    """Record one sanitized append-only business audit event."""

    def __init__(
        self,
        repository: AuditEventRepository,
        *,
        factory: AuditEventFactory | None = None,
    ) -> None:
        self._repository = repository
        self._factory = (
            factory
            if factory is not None
            else AuditEventFactory()
        )

    def execute(
        self,
        *,
        context: AuditContext,
        action: AuditAction,
        resource: str,
        resource_id: object,
        before: Mapping[str, object] | BaseModel | None = None,
        after: Mapping[str, object] | BaseModel | None = None,
        metadata: Mapping[str, object] | BaseModel | None = None,
    ) -> AuditEvent:
        """Create, sanitize and append one audit event."""

        event = self._factory.create(
            context=context,
            action=action,
            resource=resource,
            resource_id=resource_id,
            before=before,
            after=after,
            metadata=metadata,
        )

        return self._repository.append(
            event
        )


__all__ = [
    "RecordAuditEvent",
]
