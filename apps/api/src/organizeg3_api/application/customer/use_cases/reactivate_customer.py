"""Reactivate-customer use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.customer.concurrency import (
    ensure_customer_version,
)
from organizeg3_api.core.exceptions import (
    InvalidTransitionError,
    NotFoundError,
)
from organizeg3_api.domain.customer.entity import Customer
from organizeg3_api.domain.customer.repository import (
    ICustomerRepository,
)


class ReactivateCustomerUseCase:
    """Restore an archived customer to active use."""

    def __init__(
        self,
        repository: ICustomerRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        customer_id: int,
        expected_version: int,
    ) -> Customer:
        """Reactivate an archived tenant-owned customer."""

        customer = self._repository.get_by_id(
            tenant_id,
            customer_id,
            include_archived=True,
        )

        if customer is None:
            raise NotFoundError(
                "Cliente não encontrado."
            )

        if customer.deleted_at is None:
            raise InvalidTransitionError(
                "O cliente não está arquivado."
            )

        ensure_customer_version(
            customer,
            expected_version,
        )

        customer.reactivate()

        return self._repository.save(
            customer,
            include_archived=True,
        )
