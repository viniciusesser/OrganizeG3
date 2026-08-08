"""List brands use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.brand.schemas import (
    BrandResponse,
)
from organizeg3_api.core.exceptions import (
    ValidationError,
)
from organizeg3_api.domain.brand.repository import (
    BrandRepository,
)


class ListBrands:
    """List tenant-scoped brands."""

    MAX_LIMIT = 200

    def __init__(
        self,
        repository: BrandRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[BrandResponse]:
        """List brands using tenant-safe filters."""

        if limit < 1:
            raise ValidationError(
                "O limite deve ser maior que zero.",
                details={
                    "field": "limit",
                },
            )

        if limit > self.MAX_LIMIT:
            raise ValidationError(
                "O limite máximo é 200.",
                details={
                    "field": "limit",
                    "maximum": self.MAX_LIMIT,
                },
            )

        if offset < 0:
            raise ValidationError(
                "O deslocamento não pode ser negativo.",
                details={
                    "field": "offset",
                },
            )

        normalized_search = (
            search.strip()
            if search is not None
            else None
        )

        if (
            search is not None
            and not normalized_search
        ):
            raise ValidationError(
                "A busca não pode ser vazia.",
                details={
                    "field": "search",
                },
            )

        brands = self._repository.list_all(
            tenant_id=tenant_id,
            include_inactive=include_inactive,
            search=normalized_search,
            limit=limit,
            offset=offset,
        )

        return [
            BrandResponse.from_entity(
                brand
            )
            for brand in brands
        ]
