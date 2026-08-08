"""Reactivate-material use case."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import (
    NotFoundError,
)
from organizeg3_api.domain.material.entity import (
    Material,
)
from organizeg3_api.domain.material.repository import (
    MaterialRepository,
)


class ReactivateMaterialUseCase:
    """Reactivate one tenant material."""

    def __init__(
        self,
        repository: MaterialRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        material_id: uuid.UUID,
    ) -> Material:
        """Reactivate a material idempotently."""

        material = (
            self._repository.get_by_id_for_tenant(
                tenant_id=tenant_id,
                material_id=material_id,
            )
        )

        if material is None:
            raise NotFoundError(
                "Material não encontrado."
            )

        material.activate()

        return self._repository.save(
            material
        )
