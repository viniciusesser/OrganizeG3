"""Deactivate-service use case."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import (
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.service.entity import (
    Service,
)
from organizeg3_api.domain.service.repository import (
    ServiceRepository,
)


class DeactivateServiceUseCase:
    """Deactivate one tenant-scoped service."""

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
        """Deactivate and persist one service."""

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

        service.deactivate()

        try:
            return self._repository.save(
                service
            )
        except ValueError as exc:
            raise ValidationError(
                str(exc)
            ) from exc


__all__ = [
    "DeactivateServiceUseCase",
]
