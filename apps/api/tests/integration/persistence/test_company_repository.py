"""Integration tests for company persistence."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from organizeg3_api.domain.company.entity import (
    Company,
)
from organizeg3_api.infrastructure.persistence.models import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories import (
    SQLAlchemyCompanyRepository,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.database,
]


def create_tenant(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    name: str,
) -> TenantRecordModel:
    """Create one tenant for company tests."""

    tenant = TenantRecordModel(
        id=tenant_id,
        name=name,
        status="ACTIVE",
        is_active=True,
    )

    session.add(
        tenant
    )
    session.flush()

    return tenant


def test_adds_and_recovers_company(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Teste",
    )

    company = Company.create(
        tenant_id=tenant_id,
        trade_name="Empresa Teste",
        legal_name="Empresa Teste LTDA",
        document_number="12.345.678/0001-90",
        email="contato@example.com",
        phone="(18) 3222-1234",
        city="Rosana",
        state="SP",
        postal_code="19273-000",
    )

    repository = SQLAlchemyCompanyRepository(
        session
    )

    saved = repository.add(
        company
    )

    recovered = repository.get_by_tenant(
        tenant_id
    )

    assert saved.id == company.id
    assert recovered is not None
    assert recovered.id == company.id
    assert recovered.tenant_id == tenant_id
    assert recovered.trade_name == "Empresa Teste"
    assert (
        recovered.document_number
        == "12345678000190"
    )
    assert recovered.city == "Rosana"
    assert recovered.state == "SP"


def test_returns_none_for_unknown_tenant(
    session: Session,
) -> None:
    repository = SQLAlchemyCompanyRepository(
        session
    )

    assert (
        repository.get_by_tenant(
            uuid.uuid4()
        )
        is None
    )


def test_company_is_tenant_scoped(
    session: Session,
) -> None:
    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_a_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=tenant_b_id,
        name="Tenant B",
    )

    repository = SQLAlchemyCompanyRepository(
        session
    )

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


def test_rejects_second_company_for_same_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Único",
    )

    repository = SQLAlchemyCompanyRepository(
        session
    )

    repository.add(
        Company.create(
            tenant_id=tenant_id,
            trade_name="Empresa A",
        )
    )

    with pytest.raises(
        IntegrityError
    ):
        repository.add(
            Company.create(
                tenant_id=tenant_id,
                trade_name="Empresa B",
            )
        )
