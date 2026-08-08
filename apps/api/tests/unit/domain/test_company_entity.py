"""Unit tests for the company domain entity."""

from __future__ import annotations

import uuid

import pytest

from organizeg3_api.domain.company.entity import (
    Company,
)


def test_creates_company_and_normalizes_data() -> None:
    tenant_id = uuid.uuid4()

    company = Company.create(
        tenant_id=tenant_id,
        trade_name="  Empresa Teste  ",
        legal_name="  Empresa Teste LTDA  ",
        document_number="12.345.678/0001-90",
        state_registration="  123456789  ",
        email=" CONTATO@EXAMPLE.COM ",
        phone="(18) 3222-1234",
        website="  https://example.com  ",
        street="  Rua Teste  ",
        number="  123  ",
        district="  Centro  ",
        city="  Rosana  ",
        state=" sp ",
        postal_code="19273-000",
    )

    assert company.id is not None
    assert company.tenant_id == tenant_id
    assert company.trade_name == "Empresa Teste"
    assert company.legal_name == "Empresa Teste LTDA"
    assert company.document_number == "12345678000190"
    assert company.state_registration == "123456789"
    assert company.email == "contato@example.com"
    assert company.phone == "1832221234"
    assert company.website == "https://example.com"
    assert company.street == "Rua Teste"
    assert company.number == "123"
    assert company.district == "Centro"
    assert company.city == "Rosana"
    assert company.state == "SP"
    assert company.postal_code == "19273000"
    assert company.is_active is True
    assert company.created_at is not None
    assert company.updated_at is not None


def test_allows_minimal_company() -> None:
    company = Company.create(
        tenant_id=uuid.uuid4(),
        trade_name="Empresa",
    )

    assert company.trade_name == "Empresa"
    assert company.document_number is None
    assert company.email is None
    assert company.phone is None
    assert company.postal_code is None


@pytest.mark.parametrize(
    "trade_name",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_trade_name(
    trade_name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="nome fantasia",
    ):
        Company.create(
            tenant_id=uuid.uuid4(),
            trade_name=trade_name,
        )


def test_rejects_null_tenant_uuid() -> None:
    with pytest.raises(
        ValueError,
        match="UUID nulo",
    ):
        Company.create(
            tenant_id=uuid.UUID(int=0),
            trade_name="Empresa",
        )


def test_rejects_invalid_tenant_type() -> None:
    with pytest.raises(
        TypeError,
        match="tenant",
    ):
        Company.create(  # type: ignore[arg-type]
            tenant_id="tenant",
            trade_name="Empresa",
        )


def test_rejects_invalid_document() -> None:
    with pytest.raises(
        ValueError,
        match="documento",
    ):
        Company.create(
            tenant_id=uuid.uuid4(),
            trade_name="Empresa",
            document_number="123",
        )


def test_rejects_repeated_document_digits() -> None:
    with pytest.raises(
        ValueError,
        match="dígitos repetidos",
    ):
        Company.create(
            tenant_id=uuid.uuid4(),
            trade_name="Empresa",
            document_number="11.111.111/1111-11",
        )


def test_rejects_invalid_email() -> None:
    with pytest.raises(
        ValueError,
        match="e-mail",
    ):
        Company.create(
            tenant_id=uuid.uuid4(),
            trade_name="Empresa",
            email="email-invalido",
        )


def test_rejects_invalid_phone() -> None:
    with pytest.raises(
        ValueError,
        match="telefone",
    ):
        Company.create(
            tenant_id=uuid.uuid4(),
            trade_name="Empresa",
            phone="123",
        )


def test_rejects_invalid_state() -> None:
    with pytest.raises(
        ValueError,
        match="UF",
    ):
        Company.create(
            tenant_id=uuid.uuid4(),
            trade_name="Empresa",
            state="São Paulo",
        )


def test_rejects_invalid_postal_code() -> None:
    with pytest.raises(
        ValueError,
        match="CEP",
    ):
        Company.create(
            tenant_id=uuid.uuid4(),
            trade_name="Empresa",
            postal_code="123",
        )
