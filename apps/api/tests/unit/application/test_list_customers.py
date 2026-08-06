"""Unit tests for the list-customers use case."""

from collections.abc import Sequence
import uuid

import pytest

from organizeg3_api.application.customer.use_cases.list_customers import (
    ListCustomersUseCase,
)
from organizeg3_api.domain.customer.entity import Customer, CustomerType
from organizeg3_api.domain.customer.repository import ICustomerRepository

pytestmark = pytest.mark.unit


class RecordingCustomerRepository(ICustomerRepository):
    def __init__(self, customers: Sequence[Customer]) -> None:
        self.customers = customers
        self.received_arguments: dict[str, object] = {}

    def get_by_id(
        self,
        tenant_id: uuid.UUID,
        customer_id: int,
    ) -> Customer | None:
        del tenant_id, customer_id
        return None

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
        self.received_arguments = {
            "tenant_id": tenant_id,
            "include_inactive": include_inactive,
            "search": search,
            "customer_type": customer_type,
            "limit": limit,
            "offset": offset,
        }

        return self.customers

    def save(self, customer: Customer) -> Customer:
        return customer


def test_forwards_tenant_and_default_filters() -> None:
    tenant_id = uuid.uuid4()
    repository = RecordingCustomerRepository([])

    result = ListCustomersUseCase(repository).execute(
        tenant_id,
    )

    assert result == []

    assert repository.received_arguments == {
        "tenant_id": tenant_id,
        "include_inactive": False,
        "search": None,
        "customer_type": None,
        "limit": 100,
        "offset": 0,
    }


def test_forwards_search_filters_and_pagination() -> None:
    tenant_id = uuid.uuid4()

    customer = Customer(
        tenant_id=tenant_id,
        code="CUST-0001",
        name="Cliente",
        customer_type=CustomerType.CORPORATE,
        is_active=False,
    )

    repository = RecordingCustomerRepository([customer])

    result = ListCustomersUseCase(repository).execute(
        tenant_id,
        include_inactive=True,
        search="  metal  ",
        customer_type=CustomerType.CORPORATE,
        limit=20,
        offset=10,
    )

    assert result == [customer]

    assert repository.received_arguments == {
        "tenant_id": tenant_id,
        "include_inactive": True,
        "search": "metal",
        "customer_type": CustomerType.CORPORATE,
        "limit": 20,
        "offset": 10,
    }
