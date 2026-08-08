"""Create-service use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.service.schemas import (
    ServiceCreate,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    ValidationError,
)
from organizeg3_api.domain.service.entity import (
    Service,
)
from organizeg3_api.domain.service.repository import (
    ServiceRepository,
)
from organizeg3_api.domain.service.value_objects import (
    ServiceCode,
)


class CreateServiceUseCase:
    """Create one service for a tenant."""

    def __init__(
        self,
        repository: ServiceRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        *,
        tenant_id: uuid.UUID,
        data: ServiceCreate,
    ) -> Service:
        """Create and persist one tenant-scoped service."""

        try:
            normalized_code = ServiceCode(
                data.code
            ).value
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise ValidationError(
                str(exc)
            ) from exc

        if self._repository.exists_by_code(
            tenant_id=tenant_id,
            code=normalized_code,
        ):
            raise ConflictError(
                "Já existe um serviço com este código.",
                details={
                    "field": "code",
                    "value": normalized_code,
                },
            )

        try:
            service = Service.create(
                tenant_id=tenant_id,
                code=data.code,
                name=data.name,
                category=data.category,
                unit=data.unit,
                execution_mode=data.execution_mode,
                estimated_duration_minutes=(
                    data.estimated_duration_minutes
                ),
            )

            return self._repository.add(
                service
            )
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise ValidationError(
                str(exc)
            ) from exc


__all__ = [
    "CreateServiceUseCase",
]
