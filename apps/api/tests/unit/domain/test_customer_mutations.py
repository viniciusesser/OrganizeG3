"""Tests for customer profile changes and lifecycle."""

import uuid

import pytest

from organizeg3_api.domain.customer.entity import (
    Customer,
    CustomerType,
)

pytestmark = pytest.mark.unit


def make_customer(
    **changes: object,
) -> Customer:
    values: dict[str, object] = {
        "tenant_id": uuid.uuid4(),
        "code": "CUST-0001",
        "name": "Cliente Teste",
        "customer_type": (
            CustomerType.INDIVIDUAL
        ),
    }

    values.update(changes)

    return Customer(
        **values
    )  # type: ignore[arg-type]


def test_update_profile_normalizes_and_clears_optional_values() -> None:
    customer = make_customer(
        document_number="529.982.247-25",
        email="old@example.com",
        phone="18999990000",
    )

    previous_timestamp = (
        customer.updated_at
    )

    customer.update_profile(
        name="  Empresa Atualizada  ",
        customer_type=(
            CustomerType.CORPORATE
        ),
        document_number=(
            "11.222.333/0001-81"
        ),
        email="   ",
        phone=None,
    )

    assert (
        customer.name
        == "Empresa Atualizada"
    )
    assert (
        customer.customer_type
        is CustomerType.CORPORATE
    )
    assert (
        customer.document_number
        == "11222333000181"
    )
    assert customer.email is None
    assert customer.phone is None
    assert (
        customer.updated_at
        >= previous_timestamp
    )


def test_archive_rejects_second_archival() -> None:
    customer = make_customer()

    customer.archive()

    with pytest.raises(
        ValueError,
        match="já está arquivado",
    ):
        customer.archive()


def test_reactivate_restores_archived_customer() -> None:
    customer = make_customer()

    customer.archive()

    archived_at = customer.deleted_at

    customer.reactivate()

    assert archived_at is not None
    assert customer.deleted_at is None
    assert customer.is_active is True
    assert (
        customer.updated_at
        >= archived_at
    )


def test_reactivate_rejects_customer_that_is_not_archived() -> None:
    customer = make_customer()

    with pytest.raises(
        ValueError,
        match="não está arquivado",
    ):
        customer.reactivate()
