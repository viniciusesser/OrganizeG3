"""Unit tests for the update-customer use case."""

from collections.abc import Sequence
import uuid

import pytest

from organizeg3_api.application.customer.schemas import (
    CustomerUpdate,
)
from organizeg3_api.application.customer.use_cases.update_customer import (
    UpdateCustomerUseCase,
)
from organizeg3_api.core.exceptions import (
    ConcurrencyError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.customer.entity import (
    Customer,
    CustomerType,
)
from organizeg3_api.domain.customer.repository import (
    ICustomerRepository,
)

pytestmark = pytest.mark.unit


class UpdateCustomerRepository(
    ICustomerRepository
):
    def __init__(
        self,
        customer: Customer | None,
    ) -> None:
        self.customer = customer
        self.saved_customer: Customer | None = None

    def get_by_id(
        self,
        tenant_id: uuid.UUID,
        customer_id: int,
        *,
        include_archived: bool = False,
    ) -> Customer | None:
        del tenant_id
        del customer_id
        del include_archived

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
        del tenant_id
        del include_inactive
        del search
        del customer_type
        del limit
        del offset

        return []

    def save(
        self,
        customer: Customer,
        *,
        include_archived: bool = False,
    ) -> Customer:
        del include_archived

        customer.row_version += 1
        self.saved_customer = customer

        return customer


def make_customer() -> Customer:
    return Customer(
        id=10,
        tenant_id=uuid.uuid4(),
        code="CUST-0001",
        name="Cliente Antigo",
        customer_type=CustomerType.INDIVIDUAL,
        email="antigo@example.com",
        row_version=3,
    )


def test_updates_only_submitted_fields() -> None:
    customer = make_customer()
    repository = UpdateCustomerRepository(customer)

    payload = CustomerUpdate(
        row_version=3,
        name="  Cliente Atualizado  ",
        customer_type=CustomerType.CORPORATE,
        email=None,
    )

    result = UpdateCustomerUseCase(
        repository
    ).execute(
        customer.tenant_id,
        customer.id or 0,
        payload,
    )

    assert result.name == "Cliente Atualizado"
    assert (
        result.customer_type
        is CustomerType.CORPORATE
    )
    assert result.email is None
    assert result.phone is None
    assert result.row_version == 4
    assert repository.saved_customer is result


def test_rejects_outdated_version() -> None:
    customer = make_customer()
    repository = UpdateCustomerRepository(customer)

    with pytest.raises(ConcurrencyError):
        UpdateCustomerUseCase(
            repository
        ).execute(
            customer.tenant_id,
            customer.id or 0,
            CustomerUpdate(
                row_version=2,
                name="Tentativa antiga",
            ),
        )


def test_rejects_payload_without_changes() -> None:
    customer = make_customer()
    repository = UpdateCustomerRepository(customer)

    with pytest.raises(
        ValidationError,
        match="ao menos um campo",
    ):
        UpdateCustomerUseCase(
            repository
        ).execute(
            customer.tenant_id,
            customer.id or 0,
            CustomerUpdate(
                row_version=customer.row_version
            ),
        )


def test_rejects_null_required_field() -> None:
    customer = make_customer()
    repository = UpdateCustomerRepository(customer)

    with pytest.raises(
        ValidationError,
        match="nome",
    ):
        UpdateCustomerUseCase(
            repository
        ).execute(
            customer.tenant_id,
            customer.id or 0,
            CustomerUpdate(
                row_version=customer.row_version,
                name=None,
            ),
        )


def test_raises_not_found() -> None:
    repository = UpdateCustomerRepository(None)

    with pytest.raises(NotFoundError):
        UpdateCustomerUseCase(
            repository
        ).execute(
            uuid.uuid4(),
            99,
            CustomerUpdate(
                row_version=1,
                name="Cliente",
            ),
        )
