"""Unit tests for the customer domain entity."""

from datetime import UTC
import uuid

import pytest

from organizeg3_api.domain.customer.entity import Customer, CustomerType

pytestmark = pytest.mark.unit


def make_customer(**changes: object) -> Customer:
    values: dict[str, object] = {
        "tenant_id": uuid.uuid4(),
        "code": "CUST-0001",
        "name": "Cliente Teste",
        "customer_type": CustomerType.INDIVIDUAL,
    }
    values.update(changes)
    return Customer(**values)  # type: ignore[arg-type]


def test_creates_valid_customer_and_normalizes_text() -> None:
    customer = make_customer(code="  CUST-0001  ", name="  Cliente Teste  ")

    assert customer.code == "CUST-0001"
    assert customer.name == "Cliente Teste"
    assert customer.is_active is True
    assert customer.row_version == 1
    assert customer.created_at.tzinfo is UTC


def test_activate_updates_status_and_timestamp() -> None:
    customer = make_customer(is_active=False)
    previous_timestamp = customer.updated_at

    customer.activate()

    assert customer.is_active is True
    assert customer.updated_at >= previous_timestamp


def test_deactivate_updates_status_and_timestamp() -> None:
    customer = make_customer()
    previous_timestamp = customer.updated_at

    customer.deactivate()

    assert customer.is_active is False
    assert customer.updated_at >= previous_timestamp


def test_mark_as_deleted_deactivates_and_updates_timestamps() -> None:
    customer = make_customer()
    previous_timestamp = customer.updated_at

    customer.mark_as_deleted()

    assert customer.deleted_at is not None
    assert customer.is_active is False
    assert customer.updated_at >= previous_timestamp
    assert customer.updated_at == customer.deleted_at


@pytest.mark.parametrize("tenant", [None, "not-a-uuid"])
def test_rejects_invalid_tenant_type(tenant: object) -> None:
    with pytest.raises(TypeError, match="tenant_id"):
        make_customer(tenant_id=tenant)


def test_rejects_null_tenant_uuid() -> None:
    with pytest.raises(ValueError, match="tenant_id"):
        make_customer(tenant_id=uuid.UUID(int=0))


@pytest.mark.parametrize("name", ["", "   "])
def test_rejects_empty_name(name: str) -> None:
    with pytest.raises(ValueError, match="nome"):
        make_customer(name=name)


def test_rejects_invalid_customer_type() -> None:
    with pytest.raises(ValueError, match="tipo de cliente"):
        make_customer(customer_type="INVALID")


def test_accepts_valid_customer_type_string() -> None:
    customer = make_customer(customer_type="CORPORATE")

    assert customer.customer_type is CustomerType.CORPORATE


def test_rejects_non_positive_row_version() -> None:
    with pytest.raises(ValueError, match="row_version"):
        make_customer(row_version=0)
