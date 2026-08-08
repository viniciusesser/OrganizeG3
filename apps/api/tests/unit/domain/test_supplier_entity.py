"""Unit tests for supplier domain behavior."""

from __future__ import annotations

import uuid

import pytest

from organizeg3_api.domain.supplier.entity import (
    Supplier,
)


def test_creates_and_normalizes_supplier() -> None:
    tenant_id = uuid.uuid4()

    supplier = Supplier.create(
        tenant_id=tenant_id,
        code=" forn-001 ",
        name="  Fornecedor Teste  ",
        trade_name=" Loja Teste ",
        legal_name=" Fornecedor Teste Ltda ",
        document_number="04.252.011/0001-10",
        state_registration=" 123456 ",
        email=" COMERCIAL@EXAMPLE.COM ",
        invoice_email=" NFE@EXAMPLE.COM ",
        phone="(18) 99999-1234",
        secondary_phone="(18) 3222-1234",
        website=" https://example.com ",
        contact_name=" Contato ",
        postal_code="19200-000",
        street=" Rua Teste ",
        number=" 100 ",
        district=" Centro ",
        city=" Rosana ",
        state=" sp ",
    )

    assert supplier.id is not None

    assert supplier.tenant_id == tenant_id
    assert supplier.code == "FORN-001"
    assert supplier.name == "Fornecedor Teste"
    assert supplier.trade_name == "Loja Teste"

    assert (
        supplier.legal_name
        == "Fornecedor Teste Ltda"
    )

    assert (
        supplier.document_number
        == "04252011000110"
    )

    assert supplier.state_registration == "123456"

    assert (
        supplier.email
        == "comercial@example.com"
    )

    assert (
        supplier.invoice_email
        == "nfe@example.com"
    )

    assert supplier.phone == "18999991234"
    assert supplier.secondary_phone == "1832221234"

    assert (
        supplier.website
        == "https://example.com"
    )

    assert supplier.contact_name == "Contato"

    assert supplier.postal_code == "19200000"
    assert supplier.street == "Rua Teste"
    assert supplier.number == "100"
    assert supplier.district == "Centro"
    assert supplier.city == "Rosana"
    assert supplier.state == "SP"

    assert supplier.is_active is True
    assert supplier.created_at is not None
    assert supplier.updated_at is not None


def test_allows_minimal_supplier() -> None:
    supplier = Supplier.create(
        tenant_id=uuid.uuid4(),
        code="FORN-001",
        name="Fornecedor",
    )

    assert supplier.document_number is None
    assert supplier.email is None
    assert supplier.phone is None
    assert supplier.is_active is True


@pytest.mark.parametrize(
    "code",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_code(
    code: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="código",
    ):
        Supplier.create(
            tenant_id=uuid.uuid4(),
            code=code,
            name="Fornecedor",
        )


@pytest.mark.parametrize(
    "name",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_name(
    name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="nome",
    ):
        Supplier.create(
            tenant_id=uuid.uuid4(),
            code="FORN-001",
            name=name,
        )


def test_rejects_null_tenant_uuid() -> None:
    with pytest.raises(
        ValueError,
        match="UUID nulo",
    ):
        Supplier.create(
            tenant_id=uuid.UUID(int=0),
            code="FORN-001",
            name="Fornecedor",
        )


def test_rejects_invalid_tenant_type() -> None:
    with pytest.raises(
        TypeError,
        match="tenant",
    ):
        Supplier.create(  # type: ignore[arg-type]
            tenant_id="tenant",
            code="FORN-001",
            name="Fornecedor",
        )


@pytest.mark.parametrize(
    "document_number",
    [
        "123",
        "111.111.111-11",
        "11.111.111/1111-11",
        "529.982.247-24",
        "04.252.011/0001-11",
    ],
)
def test_rejects_invalid_document(
    document_number: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="fornecedor",
    ):
        Supplier.create(
            tenant_id=uuid.uuid4(),
            code="FORN-001",
            name="Fornecedor",
            document_number=document_number,
        )


def test_accepts_valid_cpf() -> None:
    supplier = Supplier.create(
        tenant_id=uuid.uuid4(),
        code="FORN-001",
        name="Prestador",
        document_number="529.982.247-25",
    )

    assert (
        supplier.document_number
        == "52998224725"
    )


def test_accepts_valid_cnpj() -> None:
    supplier = Supplier.create(
        tenant_id=uuid.uuid4(),
        code="FORN-001",
        name="Empresa",
        document_number="04.252.011/0001-10",
    )

    assert (
        supplier.document_number
        == "04252011000110"
    )


def test_rejects_invalid_email() -> None:
    with pytest.raises(
        ValueError,
        match="e-mail",
    ):
        Supplier.create(
            tenant_id=uuid.uuid4(),
            code="FORN-001",
            name="Fornecedor",
            email="email-invalido",
        )


def test_rejects_invalid_invoice_email() -> None:
    with pytest.raises(
        ValueError,
        match="e-mail",
    ):
        Supplier.create(
            tenant_id=uuid.uuid4(),
            code="FORN-001",
            name="Fornecedor",
            invoice_email="email-invalido",
        )


def test_rejects_invalid_phone() -> None:
    with pytest.raises(
        ValueError,
        match="telefone",
    ):
        Supplier.create(
            tenant_id=uuid.uuid4(),
            code="FORN-001",
            name="Fornecedor",
            phone="123",
        )


def test_rejects_invalid_secondary_phone() -> None:
    with pytest.raises(
        ValueError,
        match="telefone",
    ):
        Supplier.create(
            tenant_id=uuid.uuid4(),
            code="FORN-001",
            name="Fornecedor",
            secondary_phone="123",
        )


def test_rejects_invalid_postal_code() -> None:
    with pytest.raises(
        ValueError,
        match="CEP",
    ):
        Supplier.create(
            tenant_id=uuid.uuid4(),
            code="FORN-001",
            name="Fornecedor",
            postal_code="123",
        )


def test_rejects_invalid_state() -> None:
    with pytest.raises(
        ValueError,
        match="estado",
    ):
        Supplier.create(
            tenant_id=uuid.uuid4(),
            code="FORN-001",
            name="Fornecedor",
            state="SPO",
        )


def test_deactivates_supplier() -> None:
    supplier = Supplier.create(
        tenant_id=uuid.uuid4(),
        code="FORN-001",
        name="Fornecedor",
    )

    supplier.deactivate()

    assert supplier.is_active is False


def test_reactivates_supplier() -> None:
    supplier = Supplier.create(
        tenant_id=uuid.uuid4(),
        code="FORN-001",
        name="Fornecedor",
    )

    supplier.deactivate()
    supplier.activate()

    assert supplier.is_active is True
