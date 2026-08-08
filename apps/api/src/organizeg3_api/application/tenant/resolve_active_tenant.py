"""Resolve and authorize the tenant selected for one request."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import PermissionDeniedError
from organizeg3_api.domain.tenant.repository import ITenantRepository


class ResolveActiveTenant:
    """Confirm that a request tenant exists and is active."""

    def __init__(
        self,
        tenant_repository: ITenantRepository,
    ) -> None:
        self._tenant_repository = tenant_repository

    def execute(
        self,
        tenant_id: uuid.UUID,
    ) -> uuid.UUID:
        """Return the tenant identifier when access is allowed."""

        if tenant_id.int == 0:
            raise ValueError(
                "tenant_id não pode ser o UUID nulo."
            )

        if not self._tenant_repository.exists_active(
            tenant_id
        ):
            raise PermissionDeniedError(
                "A empresa informada não está disponível para acesso.",
                details={
                    "reason": "tenant_unavailable",
                },
            )

        return tenant_id
