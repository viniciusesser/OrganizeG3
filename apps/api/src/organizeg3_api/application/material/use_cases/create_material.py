"""Create-material use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.material.schemas import (
    MaterialCreate,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    ValidationError,
)
from organizeg3_api.domain.material.entity import (
    Material,
)
from organizeg3_api.domain.material.repository import (
    MaterialRepository,
)


class CreateMaterialUseCase:
    """Create one material inside the authenticated tenant."""

    def __init__(
        self,
        repository: MaterialRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        payload: MaterialCreate,
    ) -> Material:
        """Create and persist one tenant-scoped material."""

        try:
            material = Material.create(
                tenant_id=tenant_id,
                code=payload.code,
                name=payload.name,
                category=payload.category,
                unit=payload.unit,
                brand_id=payload.brand_id,
            )
        except (
            TypeError,
            ValueError,
        ) as exception:
            raise ValidationError(
                str(exception)
            ) from exception

        try:
            code_exists = (
                self._repository.exists_by_code(
                    tenant_id=tenant_id,
                    code=material.code,
                )
            )
        except (
            TypeError,
            ValueError,
        ) as exception:
            raise ValidationError(
                str(exception)
            ) from exception

        if code_exists:
            raise ConflictError(
                "Já existe um material com este código."
            )

        try:
            return self._repository.add(
                material
            )
        except (
            TypeError,
            ValueError,
        ) as exception:
            raise ValidationError(
                str(exception)
            ) from exception
