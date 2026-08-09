"""Identity repository contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
import uuid


@dataclass(frozen=True, slots=True)
class IdentityAccess:
    """Represent active local access for one user and tenant."""

    user_id: uuid.UUID
    membership_id: uuid.UUID
    auth_user_id: uuid.UUID
    email: str
    display_name: str
    permission_codes: frozenset[str]


@dataclass(frozen=True, slots=True)
class AccessibleTenant:
    """Represent one tenant available to an authenticated user."""

    tenant_id: uuid.UUID
    membership_id: uuid.UUID
    name: str


class IdentityRepository(Protocol):
    """Resolve local identity and authorization information."""

    def resolve_active_access(
        self,
        *,
        auth_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> IdentityAccess | None:
        """Resolve active user access inside one tenant."""

    def list_accessible_tenants(
        self,
        *,
        auth_user_id: uuid.UUID,
    ) -> tuple[AccessibleTenant, ...]:
        """List active tenants available to one authenticated user."""

