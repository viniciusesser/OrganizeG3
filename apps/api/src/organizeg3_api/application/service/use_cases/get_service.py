"""Get-service use case."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import (
    NotFoundError,
)
from organizeg3_api.domain.service.entity import (
    Service,
)
from organizeg3_api.domain.service.repository import (
    ServiceRepository,
)


class GetServiceUseCase:
    """Return one tenant-scoped service."""

    def __init__(
        self,
        repository: ServiceRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        *,
        tenant_id: uuid.UUID,
        service_id: uuid.UUID,
    ) -> Service:
        """Return one service or raise a controlled not-found error."""

        service = (
            self._repository.get_by_id_for_tenant(
                tenant_id=tenant_id,
                service_id=service_id,
            )
        )

        if service is None:
            raise NotFoundError(
                "Serviço não encontrado."
            )

        return service


__all__ = [
    "GetServiceUseCase",
]
