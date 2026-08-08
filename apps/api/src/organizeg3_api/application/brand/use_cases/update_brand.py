"""Update brand use case."""

from __future__ import annotations

from typing import TypeVar, cast
import uuid

from pydantic import BaseModel

from organizeg3_api.application.brand.schemas import (
    BrandResponse,
    BrandUpdate,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.brand.repository import (
    BrandRepository,
)

T = TypeVar(
    "T"
)


class UpdateBrand:
    """Update one tenant-scoped brand."""

    def __init__(
        self,
        repository: BrandRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        *,
        tenant_id: uuid.UUID,
        brand_id: uuid.UUID,
        data: BrandUpdate,
    ) -> BrandResponse:
        """Apply a partial update to one brand."""

        if not data.model_fields_set:
            raise ValidationError(
                "Informe ao menos um campo para atualização."
            )

        brand = self._repository.get_by_id_for_tenant(
            tenant_id=tenant_id,
            brand_id=brand_id,
        )

        if brand is None:
            raise NotFoundError(
                "Marca não encontrada.",
                details={
                    "brand_id": str(
                        brand_id
                    ),
                },
            )

        code = self._resolve_required(
            data=data,
            field_name="code",
            current=brand.code,
        )

        name = self._resolve_required(
            data=data,
            field_name="name",
            current=brand.name,
        )

        self._ensure_code_available(
            tenant_id=tenant_id,
            brand_id=brand_id,
            code=code,
        )

        self._ensure_name_available(
            tenant_id=tenant_id,
            brand_id=brand_id,
            name=name,
        )

        brand.update_details(
            code=code,
            name=name,
        )

        saved = self._repository.save(
            brand
        )

        return BrandResponse.from_entity(
            saved
        )

    @staticmethod
    def _resolve_required(
        *,
        data: BaseModel,
        field_name: str,
        current: T,
    ) -> T:
        if field_name not in data.model_fields_set:
            return current

        value = cast(
            T | None,
            getattr(
                data,
                field_name,
            ),
        )

        if value is None:
            raise ValidationError(
                "O campo não pode ser nulo.",
                details={
                    "field": field_name,
                },
            )

        return value

    def _ensure_code_available(
        self,
        *,
        tenant_id: uuid.UUID,
        brand_id: uuid.UUID,
        code: str,
    ) -> None:
        if self._repository.exists_by_code(
            tenant_id=tenant_id,
            code=code,
            exclude_brand_id=brand_id,
        ):
            raise ConflictError(
                "Já existe uma marca com este código.",
                details={
                    "field": "code",
                    "value": code,
                },
            )

    def _ensure_name_available(
        self,
        *,
        tenant_id: uuid.UUID,
        brand_id: uuid.UUID,
        name: str,
    ) -> None:
        if self._repository.exists_by_name(
            tenant_id=tenant_id,
            name=name,
            exclude_brand_id=brand_id,
        ):
            raise ConflictError(
                "Já existe uma marca com este nome.",
                details={
                    "field": "name",
                    "value": name,
                },
            )
