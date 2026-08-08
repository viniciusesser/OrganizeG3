"""Unit tests for company application use cases."""

from __future__ import annotations

import uuid

import pytest

from organizeg3_api.application.company.schemas import (
    CompanyCreate,
    CompanyUpdate,
)
from organizeg3_api.application.company.use_cases import (
    CreateCompanyUseCase,
    GetCompanyUseCase,
    UpdateCompanyUseCase,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.company.entity import Company
from organizeg3_api.domain.company.repository import (
    ICompanyRepository,
)


class FakeCompanyRepository(
    ICompanyRepository
):
    """In-memory repository used by company application tests."""

    def __init__(self) -> None:
        self._companies: dict[
            uuid.UUID,
            Company,
        ] = {}

    def get_by_tenant(
        self,
        tenant_id: uuid.UUID,
    ) -> Company | None:
        return self._companies.get(
            tenant_id
        )

    def add(
        self,
        company: Company,
    ) -> Company:
        self._companies[
            company.tenant_id
        ] = company

        return company

    def save(
        self,
        company: Company,
    ) -> Company:
        self._companies[
            company.tenant_id
        ] = company

        return company


def test_creates_company_for_tenant() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeCompanyRepository()

    payload = CompanyCreate(
        trade_name="  Empresa Teste  ",
        legal_name="  Empresa Teste LTDA  ",
        document_number="12.345.678/0001-90",
        email=" CONTATO@EXAMPLE.COM ",
        phone="(18) 3222-1234",
        city="  Rosana  ",
        state=" sp ",
        postal_code="19273-000",
    )

    company = CreateCompanyUseCase(
        repository
    ).execute(
        tenant_id,
        payload,
    )

    assert company.id is not None
    assert company.tenant_id == tenant_id
    assert company.trade_name == "Empresa Teste"
    assert (
        company.legal_name
        == "Empresa Teste LTDA"
    )
    assert (
        company.document_number
        == "12345678000190"
    )
    assert (
        company.email
        == "contato@example.com"
    )
    assert company.phone == "1832221234"
    assert company.city == "Rosana"
    assert company.state == "SP"
    assert company.postal_code == "19273000"


def test_rejects_second_company_for_tenant() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeCompanyRepository()

    repository.add(
        Company.create(
            tenant_id=tenant_id,
            trade_name="Empresa Existente",
        )
    )

    use_case = CreateCompanyUseCase(
        repository
    )

    with pytest.raises(
        ConflictError,
        match="já possui",
    ):
        use_case.execute(
            tenant_id,
            CompanyCreate(
                trade_name="Outra Empresa",
            ),
        )


def test_gets_company_for_tenant() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeCompanyRepository()

    expected = repository.add(
        Company.create(
            tenant_id=tenant_id,
            trade_name="Empresa Teste",
        )
    )

    company = GetCompanyUseCase(
        repository
    ).execute(
        tenant_id
    )

    assert company is expected


def test_get_rejects_missing_company() -> None:
    repository = FakeCompanyRepository()

    with pytest.raises(
        NotFoundError,
        match="Empresa não encontrada",
    ):
        GetCompanyUseCase(
            repository
        ).execute(
            uuid.uuid4()
        )


def test_updates_company_partially() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeCompanyRepository()

    original = repository.add(
        Company.create(
            tenant_id=tenant_id,
            trade_name="Empresa Antiga",
            email="antigo@example.com",
            city="Rosana",
            state="SP",
        )
    )

    company = UpdateCompanyUseCase(
        repository
    ).execute(
        tenant_id,
        CompanyUpdate(
            trade_name=" Empresa Nova ",
            email=" NOVO@EXAMPLE.COM ",
        ),
    )

    assert company.id == original.id
    assert company.tenant_id == tenant_id
    assert company.trade_name == "Empresa Nova"
    assert company.email == "novo@example.com"

    assert company.city == "Rosana"
    assert company.state == "SP"
    assert company.updated_at is not None


def test_update_can_clear_optional_field() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeCompanyRepository()

    repository.add(
        Company.create(
            tenant_id=tenant_id,
            trade_name="Empresa",
            legal_name="Empresa LTDA",
        )
    )

    company = UpdateCompanyUseCase(
        repository
    ).execute(
        tenant_id,
        CompanyUpdate(
            legal_name=None,
        ),
    )

    assert company.legal_name is None


def test_update_rejects_empty_payload() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeCompanyRepository()

    repository.add(
        Company.create(
            tenant_id=tenant_id,
            trade_name="Empresa",
        )
    )

    with pytest.raises(
        ValidationError,
        match="ao menos um campo",
    ):
        UpdateCompanyUseCase(
            repository
        ).execute(
            tenant_id,
            CompanyUpdate(),
        )


def test_update_rejects_missing_company() -> None:
    repository = FakeCompanyRepository()

    with pytest.raises(
        NotFoundError,
        match="Empresa não encontrada",
    ):
        UpdateCompanyUseCase(
            repository
        ).execute(
            uuid.uuid4(),
            CompanyUpdate(
                trade_name="Empresa",
            ),
        )


def test_repository_scope_does_not_cross_tenants() -> None:
    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    repository = FakeCompanyRepository()

    repository.add(
        Company.create(
            tenant_id=tenant_a_id,
            trade_name="Empresa A",
        )
    )

    assert (
        repository.get_by_tenant(
            tenant_b_id
        )
        is None
    )
