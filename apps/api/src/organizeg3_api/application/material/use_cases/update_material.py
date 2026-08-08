"""Update-material use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.material.schemas import (
    MaterialUpdate,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.material.entity import (
    Material,
)
from organizeg3_api.domain.material.repository import (
    MaterialRepository,
)


class UpdateMaterialUseCase:
    """Update one material inside the authenticated tenant."""

    def __init__(
        self,
        repository: MaterialRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        material_id: uuid.UUID,
        payload: MaterialUpdate,
    ) -> Material:
        """Apply a partial tenant-scoped material update."""

        supplied_fields = payload.model_fields_set

        if not supplied_fields:
            raise ValidationError(
                "Nenhum campo foi informado para atualização."
            )

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

        code = (
            payload.code
            if "code" in supplied_fields
            else material.code
        )
        name = (
            payload.name
            if "name" in supplied_fields
            else material.name
        )
        category = (
            payload.category
            if "category" in supplied_fields
            else material.category
        )
        unit = (
            payload.unit
            if "unit" in supplied_fields
            else material.unit
        )
        brand_id = (
            payload.brand_id
            if "brand_id" in supplied_fields
            else material.brand_id
        )

        if code is None:
            raise ValidationError(
                "O código do material é obrigatório."
            )

        if name is None:
            raise ValidationError(
                "O nome do material é obrigatório."
            )

        if category is None:
            raise ValidationError(
                "A categoria do material é obrigatória."
            )

        if unit is None:
            raise ValidationError(
                "A unidade do material é obrigatória."
            )

        try:
            material.update_details(
                code=code,
                name=name,
                category=category,
                unit=unit,
                brand_id=brand_id,
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
                    exclude_material_id=material.id,
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
            return self._repository.save(
                material
            )
        except (
            TypeError,
            ValueError,
        ) as exception:
            raise ValidationError(
                str(exception)
            ) from exception
