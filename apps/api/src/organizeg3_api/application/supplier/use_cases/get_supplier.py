"""Get supplier application use case."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import (
    NotFoundError,
)
from organizeg3_api.domain.supplier import (
    Supplier,
    SupplierRepository,
)


class GetSupplierUseCase:
    """Get one supplier from the authenticated tenant."""

    def __init__(
        self,
        repository: SupplierRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        supplier_id: uuid.UUID,
    ) -> Supplier:
        """Return one tenant-scoped supplier."""

        supplier = (
            self._repository.get_by_id_for_tenant(
                tenant_id=tenant_id,
                supplier_id=supplier_id,
            )
        )

        if supplier is None:
            raise NotFoundError(
                "Fornecedor não encontrado."
            )

        return supplier
