"""Repository contract for tenant availability queries."""

from __future__ import annotations

from typing import Protocol
import uuid


class ITenantRepository(Protocol):
    """Expose tenant queries required by the application layer."""

    def is_active(
        self,
        tenant_id: uuid.UUID,
    ) -> bool:
        """Return whether the tenant exists and can use the platform."""
