"""Get-customer use case."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import NotFoundError
from organizeg3_api.domain.customer.entity import Customer
from organizeg3_api.domain.customer.repository import ICustomerRepository


class GetCustomerUseCase:
    """Return one customer from the authenticated tenant."""

    def __init__(self, repository: ICustomerRepository) -> None:
        self._repository = repository

    def execute(self, tenant_id: uuid.UUID, customer_id: int) -> Customer:
        """Fetch one non-archived customer or raise a controlled error."""

        customer = self._repository.get_by_id(tenant_id, customer_id)
        if customer is None:
            raise NotFoundError("Cliente não encontrado.")
        return customer
