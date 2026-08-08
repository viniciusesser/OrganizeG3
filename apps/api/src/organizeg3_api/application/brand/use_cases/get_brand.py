"""Get brand use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.brand.schemas import (
    BrandResponse,
)
from organizeg3_api.core.exceptions import (
    NotFoundError,
)
from organizeg3_api.domain.brand.repository import (
    BrandRepository,
)


class GetBrand:
    """Return one tenant-scoped brand."""

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
    ) -> BrandResponse:
        """Return one brand or fail if it does not exist."""

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

        return BrandResponse.from_entity(
            brand
        )
