"""Unit tests for the create-customer use case."""

from collections.abc import Sequence
import uuid

import pytest

from organizeg3_api.application.customer.schemas import CustomerCreate
from organizeg3_api.application.customer.use_cases.create_customer import (
    CreateCustomerUseCase,
)
from organizeg3_api.domain.customer.entity import Customer, CustomerType
from organizeg3_api.domain.customer.repository import ICustomerRepository

pytestmark = pytest.mark.unit


class FakeCustomerRepository(ICustomerRepository):
    def __init__(self) -> None:
        self.saved_customer: Customer | None = None

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
        customer.id = 10
        self.saved_customer = customer
        return customer


def test_creates_customer_for_context_tenant() -> None:
    repository = FakeCustomerRepository()
    tenant_id = uuid.uuid4()

    payload = CustomerCreate(
        name="Indústria Teste",
        customer_type=CustomerType.CORPORATE,
        email="contato@example.com",
    )

    result = CreateCustomerUseCase(repository).execute(
        tenant_id,
        payload,
    )

    assert result.id == 10
    assert result.tenant_id == tenant_id
    assert result.code.startswith("CUST-")
    assert len(result.code) == 13
    assert repository.saved_customer is result


def test_payload_does_not_define_tenant() -> None:
    with pytest.raises(ValueError):
        CustomerCreate.model_validate(
            {
                "tenant_id": str(uuid.uuid4()),
                "name": "Cliente",
            }
        )
