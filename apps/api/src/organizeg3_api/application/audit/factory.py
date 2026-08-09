"""Standardized factory for trusted business audit events."""

from __future__ import annotations

from collections.abc import Mapping

from pydantic import BaseModel

from organizeg3_api.application.audit.sanitization import (
    sanitize_audit_mapping,
)
from organizeg3_api.domain.audit import (
    AuditAction,
    AuditContext,
    AuditEvent,
)


class AuditEventFactory:
    """Build audit events exclusively from trusted request context."""

    def create(
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
        """Create one sanitized immutable audit event."""

        return AuditEvent(
            tenant_id=context.tenant_id,
            branch_id=context.branch_id,
            actor_user_id=context.user_id,
            membership_id=context.membership_id,
            auth_user_id=context.auth_user_id,
            action=action,
            resource=resource,
            resource_id=str(
                resource_id
            ),
            correlation_id=context.correlation_id,
            device_id=context.device_id,
            before=sanitize_audit_mapping(
                before
            ),
            after=sanitize_audit_mapping(
                after
            ),
            metadata=sanitize_audit_mapping(
                metadata
            ),
        )


__all__ = [
    "AuditEventFactory",
]
