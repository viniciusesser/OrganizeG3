"""Request audit context definitions."""

from __future__ import annotations

from dataclasses import dataclass
import uuid


@dataclass(frozen=True, slots=True)
class AuditContext:
    """Represent trusted actor and request identifiers for auditing."""

    correlation_id: str
    tenant_id: uuid.UUID
    branch_id: uuid.UUID | None
    user_id: uuid.UUID
    membership_id: uuid.UUID
    auth_user_id: uuid.UUID
    device_id: str | None
