"""Unit tests for the get-customer use case."""

from collections.abc import Sequence
import uuid

import pytest

from organizeg3_api.application.customer.use_cases.get_customer import (
    GetCustomerUseCase,
)
from organizeg3_api.core.exceptions import NotFoundError
from organizeg3_api.domain.customer.entity import Customer, CustomerType
from organizeg3_api.domain.customer.repository import ICustomerRepository

pytestmark = pytest.mark.unit


class CustomerLookupRepository(ICustomerRepository):
    def __init__(self, customer: Customer | None) -> None:
        self.customer = customer
        self.received_tenant: uuid.UUID | None = None
        self.received_customer_id: int | None = None

    def get_by_id(
        self,
        tenant_id: uuid.UUID,
        customer_id: int,
    ) -> Customer | None:
        self.received_tenant = tenant_id
        self.received_customer_id = customer_id
        return self.customer

    def list_all(
        self,
        tenant_id: uuid.UUID,
        *,
        include_inactive: bool = False,
        search: str | None = None,
        customer_type: CustomerType | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Customer]:
        del (
            tenant_id,
            include_inactive,
            search,
            customer_type,
            limit,
            offset,
        )
        return []

    def save(self, customer: Customer) -> Customer:
        return customer


def test_returns_customer_from_context_tenant() -> None:
    tenant_id = uuid.uuid4()

    customer = Customer(
        id=10,
        tenant_id=tenant_id,
        code="CUST-0001",
        name="Cliente",
        customer_type=CustomerType.INDIVIDUAL,
    )

    repository = CustomerLookupRepository(customer)

    result = GetCustomerUseCase(repository).execute(
        tenant_id,
        10,
    )

    assert result is customer
    assert repository.received_tenant == tenant_id
    assert repository.received_customer_id == 10


def test_raises_not_found_when_customer_does_not_exist() -> None:
    repository = CustomerLookupRepository(None)

    with pytest.raises(
        NotFoundError,
        match="Cliente não encontrado",
    ):
        GetCustomerUseCase(repository).execute(
            uuid.uuid4(),
            99,
        )
