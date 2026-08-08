"""Create brand use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.brand.schemas import (
    BrandCreate,
    BrandResponse,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
)
from organizeg3_api.domain.brand.entity import (
    Brand,
)
from organizeg3_api.domain.brand.repository import (
    BrandRepository,
)


class CreateBrand:
    """Create one tenant-scoped brand."""

    def __init__(
        self,
        repository: BrandRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        *,
        tenant_id: uuid.UUID,
        data: BrandCreate,
    ) -> BrandResponse:
        """Create and persist one brand."""

        self._ensure_code_available(
            tenant_id=tenant_id,
            code=data.code,
        )

        self._ensure_name_available(
            tenant_id=tenant_id,
            name=data.name,
        )

        brand = Brand.create(
            tenant_id=tenant_id,
            code=data.code,
            name=data.name,
        )

        saved = self._repository.add(
            brand
        )

        return BrandResponse.from_entity(
            saved
        )

    def _ensure_code_available(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> None:
        if self._repository.exists_by_code(
            tenant_id=tenant_id,
            code=code,
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
        name: str,
    ) -> None:
        if self._repository.exists_by_name(
            tenant_id=tenant_id,
            name=name,
        ):
            raise ConflictError(
                "Já existe uma marca com este nome.",
                details={
                    "field": "name",
                    "value": name,
                },
            )
