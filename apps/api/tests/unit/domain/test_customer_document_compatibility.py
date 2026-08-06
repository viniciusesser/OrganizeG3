"""Unit tests for customer type and document compatibility."""

import uuid

import pytest

from organizeg3_api.domain.customer.entity import (
    Customer,
    CustomerType,
)

pytestmark = pytest.mark.unit


def test_individual_customer_accepts_cpf() -> None:
    customer = Customer(
        tenant_id=uuid.uuid4(),
        code="CUST-0001",
        name="Pessoa Física",
        customer_type=CustomerType.INDIVIDUAL,
        document_number="529.982.247-25",
    )

    assert (
        customer.document_number
        == "52998224725"
    )


def test_corporate_customer_accepts_cnpj() -> None:
    customer = Customer(
        tenant_id=uuid.uuid4(),
        code="CUST-0002",
        name="Pessoa Jurídica",
        customer_type=CustomerType.CORPORATE,
        document_number="11.222.333/0001-81",
    )

    assert (
        customer.document_number
        == "11222333000181"
    )


def test_individual_customer_rejects_cnpj() -> None:
    with pytest.raises(
        ValueError,
        match="pessoa física",
    ):
        Customer(
            tenant_id=uuid.uuid4(),
            code="CUST-0003",
            name="Pessoa Física",
            customer_type=CustomerType.INDIVIDUAL,
            document_number="11.222.333/0001-81",
        )


def test_corporate_customer_rejects_cpf() -> None:
    with pytest.raises(
        ValueError,
        match="pessoa jurídica",
    ):
        Customer(
            tenant_id=uuid.uuid4(),
            code="CUST-0004",
            name="Pessoa Jurídica",
            customer_type=CustomerType.CORPORATE,
            document_number="529.982.247-25",
        )


def test_legacy_invalid_contact_data_can_be_loaded() -> None:
    customer = Customer(
        tenant_id=uuid.uuid4(),
        code="CUST-LEGACY",
        name="Cliente Legado",
        customer_type=CustomerType.INDIVIDUAL,
        document_number="123",
        email="EMAIL LEGADO",
        phone="SEM TELEFONE",
        _allow_legacy_contacts=True,
    )

    assert customer.document_number == "123"
    assert customer.email == "email legado"
    assert customer.phone == "SEM TELEFONE"


def test_unrelated_update_preserves_legacy_contact_data() -> None:
    customer = Customer(
        tenant_id=uuid.uuid4(),
        code="CUST-LEGACY",
        name="Cliente Legado",
        customer_type=CustomerType.INDIVIDUAL,
        document_number="123",
        email="EMAIL LEGADO",
        phone="SEM TELEFONE",
        _allow_legacy_contacts=True,
    )

    customer.update_profile(
        name="Cliente Legado Atualizado",
        customer_type=CustomerType.INDIVIDUAL,
        document_number=customer.document_number,
        email=customer.email,
        phone=customer.phone,
    )

    assert (
        customer.name
        == "Cliente Legado Atualizado"
    )
    assert customer.document_number == "123"
