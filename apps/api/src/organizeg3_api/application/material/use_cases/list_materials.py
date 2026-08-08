"""List-materials use case."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import (
    ValidationError,
)
from organizeg3_api.domain.material.entity import (
    Material,
)
from organizeg3_api.domain.material.repository import (
    MaterialRepository,
)

_MAX_LIST_LIMIT = 200


class ListMaterialsUseCase:
    """List materials belonging to the authenticated tenant."""

    def __init__(
        self,
        repository: MaterialRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        *,
        include_inactive: bool = False,
        search: str | None = None,
        category: str | None = None,
        brand_id: uuid.UUID | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Material]:
        """Execute tenant-scoped listing with explicit filters."""

        if limit <= 0:
            raise ValidationError(
                "O limite deve ser maior que zero."
            )

        if limit > _MAX_LIST_LIMIT:
            raise ValidationError(
                f"O limite máximo é {_MAX_LIST_LIMIT}."
            )

        if offset < 0:
            raise ValidationError(
                "O offset não pode ser negativo."
            )

        normalized_search = (
            search.strip()
            if search is not None
            else None
        )

        normalized_category = (
            category.strip()
            if category is not None
            else None
        )

        try:
            return self._repository.list_all(
                tenant_id=tenant_id,
                include_inactive=include_inactive,
                search=normalized_search or None,
                category=normalized_category or None,
                brand_id=brand_id,
                limit=limit,
                offset=offset,
            )
        except (
            TypeError,
            ValueError,
        ) as exception:
            raise ValidationError(
                str(exception)
            ) from exception
