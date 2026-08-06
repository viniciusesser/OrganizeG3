"""Application service for resolving an active tenant context."""

from __future__ import annotations

from dataclasses import dataclass
import uuid

from organizeg3_api.core.exceptions import TenantUnavailableError
from organizeg3_api.domain.tenant.repository import ITenantRepository


@dataclass(slots=True)
class ResolveActiveTenant:
    """Ensure that a tenant exists and can access the platform."""

    repository: ITenantRepository

    def execute(
        self,
        tenant_id: uuid.UUID,
    ) -> uuid.UUID:
        """Return the tenant identifier after availability validation."""

        if not self.repository.is_active(tenant_id):
            raise TenantUnavailableError(
                "A empresa informada não existe ou não está ativa."
            )

        return tenant_id
