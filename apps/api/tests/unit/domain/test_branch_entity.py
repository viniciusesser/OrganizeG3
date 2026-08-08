"""Unit tests for the branch domain entity."""

from __future__ import annotations

import uuid

import pytest

from organizeg3_api.domain.branch.entity import (
    Branch,
)


def test_creates_and_normalizes_branch() -> None:
    tenant_id = uuid.uuid4()

    branch = Branch.create(
        tenant_id=tenant_id,
        code=" matriz ",
        name="  Matriz  ",
        legal_name="  Empresa Matriz LTDA  ",
        document_number="12.345.678/0001-90",
        state_registration=" 123456789 ",
        email=" FILIAL@EXAMPLE.COM ",
        phone="(18) 3222-1234",
        website=" https://example.com ",
        street=" Rua Teste ",
        number=" 100 ",
        district=" Centro ",
        city=" Rosana ",
        state=" sp ",
        postal_code="19273-000",
        is_headquarters=True,
    )

    assert branch.id is not None
    assert branch.tenant_id == tenant_id
    assert branch.code == "MATRIZ"
    assert branch.name == "Matriz"
    assert branch.legal_name == "Empresa Matriz LTDA"
    assert branch.document_number == "12345678000190"
    assert branch.state_registration == "123456789"
    assert branch.email == "filial@example.com"
    assert branch.phone == "1832221234"
    assert branch.website == "https://example.com"
    assert branch.street == "Rua Teste"
    assert branch.number == "100"
    assert branch.district == "Centro"
    assert branch.city == "Rosana"
    assert branch.state == "SP"
    assert branch.postal_code == "19273000"
    assert branch.is_headquarters is True
    assert branch.is_active is True
    assert branch.created_at is not None
    assert branch.updated_at is not None


def test_allows_minimal_branch() -> None:
    branch = Branch.create(
        tenant_id=uuid.uuid4(),
        code="FILIAL-01",
        name="Filial 01",
    )

    assert branch.code == "FILIAL-01"
    assert branch.name == "Filial 01"
    assert branch.document_number is None
    assert branch.is_headquarters is False


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
        Branch.create(
            tenant_id=uuid.uuid4(),
            code=code,
            name="Filial",
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
        Branch.create(
            tenant_id=uuid.uuid4(),
            code="FILIAL",
            name=name,
        )


def test_rejects_null_tenant_uuid() -> None:
    with pytest.raises(
        ValueError,
        match="UUID nulo",
    ):
        Branch.create(
            tenant_id=uuid.UUID(int=0),
            code="FILIAL",
            name="Filial",
        )


def test_rejects_invalid_tenant_type() -> None:
    with pytest.raises(
        TypeError,
        match="tenant",
    ):
        Branch.create(  # type: ignore[arg-type]
            tenant_id="tenant",
            code="FILIAL",
            name="Filial",
        )


def test_rejects_invalid_document() -> None:
    with pytest.raises(
        ValueError,
        match="documento",
    ):
        Branch.create(
            tenant_id=uuid.uuid4(),
            code="FILIAL",
            name="Filial",
            document_number="123",
        )


def test_rejects_invalid_email() -> None:
    with pytest.raises(
        ValueError,
        match="e-mail",
    ):
        Branch.create(
            tenant_id=uuid.uuid4(),
            code="FILIAL",
            name="Filial",
            email="email-invalido",
        )


def test_rejects_invalid_phone() -> None:
    with pytest.raises(
        ValueError,
        match="telefone",
    ):
        Branch.create(
            tenant_id=uuid.uuid4(),
            code="FILIAL",
            name="Filial",
            phone="123",
        )


def test_rejects_invalid_state() -> None:
    with pytest.raises(
        ValueError,
        match="UF",
    ):
        Branch.create(
            tenant_id=uuid.uuid4(),
            code="FILIAL",
            name="Filial",
            state="São Paulo",
        )


def test_rejects_invalid_postal_code() -> None:
    with pytest.raises(
        ValueError,
        match="CEP",
    ):
        Branch.create(
            tenant_id=uuid.uuid4(),
            code="FILIAL",
            name="Filial",
            postal_code="123",
        )


def test_deactivates_branch() -> None:
    branch = Branch.create(
        tenant_id=uuid.uuid4(),
        code="FILIAL",
        name="Filial",
    )

    previous_updated_at = branch.updated_at

    branch.deactivate()

    assert branch.is_active is False
    assert branch.updated_at is not None
    assert branch.updated_at != previous_updated_at


def test_reactivates_branch() -> None:
    branch = Branch.create(
        tenant_id=uuid.uuid4(),
        code="FILIAL",
        name="Filial",
    )

    branch.deactivate()
    deactivated_at = branch.updated_at

    branch.activate()

    assert branch.is_active is True
    assert branch.updated_at is not None
    assert branch.updated_at != deactivated_at
