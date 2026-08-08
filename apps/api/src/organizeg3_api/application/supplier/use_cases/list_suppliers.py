"""List suppliers application use case."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import ValidationError
from organizeg3_api.domain.supplier import Supplier, SupplierRepository

MAX_PAGE_SIZE = 200


class ListSuppliersUseCase:
    """List suppliers belonging to one tenant."""

    def __init__(
        self,
        repository: SupplierRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        *,
        include_inactive: bool = False,
        search: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Supplier]:
        """Return filtered tenant suppliers."""

        if limit < 1:
            raise ValidationError(
                "O limite deve ser maior que zero."
            )

        if limit > MAX_PAGE_SIZE:
            raise ValidationError(
                f"O limite máximo é {MAX_PAGE_SIZE}."
            )

        if offset < 0:
            raise ValidationError(
                "O offset não pode ser negativo."
            )

        return self._repository.list_all(
            tenant_id=tenant_id,
            include_inactive=include_inactive,
            search=search,
            limit=limit,
            offset=offset,
        )
