"""List-customers use case."""

from __future__ import annotations

from collections.abc import Sequence
import uuid

from organizeg3_api.domain.customer.entity import Customer, CustomerType
from organizeg3_api.domain.customer.repository import ICustomerRepository


class ListCustomersUseCase:
    """List and search customers within the authenticated tenant."""

    def __init__(self, repository: ICustomerRepository) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        *,
        include_inactive: bool = False,
        search: str | None = None,
        customer_type: CustomerType | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Customer]:
        """Execute tenant-scoped listing with explicit filters."""

        normalized_search = search.strip() if search is not None else None

        return self._repository.list_all(
            tenant_id=tenant_id,
            include_inactive=include_inactive,
            search=normalized_search or None,
            customer_type=customer_type,
            limit=limit,
            offset=offset,
        )
