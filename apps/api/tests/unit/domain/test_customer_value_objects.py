"""Unit tests for customer value objects."""

import pytest

from organizeg3_api.domain.customer.value_objects import (
    DocumentNumber,
    EmailAddress,
    PhoneNumber,
)

pytestmark = pytest.mark.unit


def test_normalizes_valid_cpf() -> None:
    document = DocumentNumber(
        "529.982.247-25"
    )

    assert document == "52998224725"
    assert document.is_cpf is True
    assert document.is_cnpj is False


def test_rejects_invalid_cpf() -> None:
    with pytest.raises(
        ValueError,
        match="CPF inválido",
    ):
        DocumentNumber(
            "529.982.247-24"
        )


def test_normalizes_valid_cnpj() -> None:
    document = DocumentNumber(
        "11.222.333/0001-81"
    )

    assert document == "11222333000181"
    assert document.is_cnpj is True
    assert document.is_cpf is False


def test_rejects_invalid_cnpj() -> None:
    with pytest.raises(
        ValueError,
        match="CNPJ inválido",
    ):
        DocumentNumber(
            "11.222.333/0001-82"
        )


def test_rejects_repeated_document_digits() -> None:
    with pytest.raises(ValueError):
        DocumentNumber(
            "111.111.111-11"
        )


def test_normalizes_email() -> None:
    email = EmailAddress(
        "  CONTATO@EXAMPLE.COM  "
    )

    assert email == "contato@example.com"


@pytest.mark.parametrize(
    "value",
    [
        "sem-arroba.example.com",
        "duplo@@example.com",
        ".inicio@example.com",
        "fim.@example.com",
        "nome@example",
        "nome@-example.com",
    ],
)
def test_rejects_invalid_email(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="E-mail inválido",
    ):
        EmailAddress(value)


def test_normalizes_mobile_phone_with_country_code() -> None:
    phone = PhoneNumber(
        "+55 (18) 99999-0000"
    )

    assert phone == "18999990000"


def test_normalizes_landline_phone() -> None:
    phone = PhoneNumber(
        "(18) 3222-4455"
    )

    assert phone == "1832224455"


@pytest.mark.parametrize(
    "value",
    [
        "9999-0000",
        "(00) 99999-0000",
        "(18) 89999-0000",
        "(18) 9999-0000",
    ],
)
def test_rejects_invalid_phone(
    value: str,
) -> None:
    with pytest.raises(ValueError):
        PhoneNumber(value)
