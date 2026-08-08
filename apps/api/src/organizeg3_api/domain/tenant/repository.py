"""Repository contract for tenant access validation."""

from __future__ import annotations

from abc import ABC, abstractmethod
import uuid


class ITenantRepository(ABC):
    """Expose tenant queries required by the application layer."""

    @abstractmethod
    def exists_active(
        self,
        tenant_id: uuid.UUID,
    ) -> bool:
        """Return whether the tenant exists and can access the platform."""
