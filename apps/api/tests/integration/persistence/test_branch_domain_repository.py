"""Integration tests for complete branch persistence."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from organizeg3_api.domain.branch.entity import (
    Branch,
)
from organizeg3_api.infrastructure.persistence.models import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories import (
    SQLAlchemyBranchRepository,
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
    """Create an active tenant."""

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


def test_adds_and_recovers_complete_branch(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Branch",
    )

    branch = Branch.create(
        tenant_id=tenant_id,
        code=" matriz ",
        name="Matriz",
        legal_name="Empresa Matriz LTDA",
        document_number="12.345.678/0001-90",
        state_registration="123456789",
        email="matriz@example.com",
        phone="(18) 3222-1234",
        website="https://example.com",
        street="Rua Teste",
        number="100",
        district="Centro",
        city="Rosana",
        state="SP",
        postal_code="19273-000",
        is_headquarters=True,
    )

    repository = SQLAlchemyBranchRepository(
        session
    )

    saved = repository.add(
        branch
    )

    recovered = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        branch_id=saved.id,
    )

    assert recovered is not None

    assert recovered.id == branch.id
    assert recovered.tenant_id == tenant_id
    assert recovered.code == "MATRIZ"
    assert recovered.name == "Matriz"

    assert (
        recovered.legal_name
        == "Empresa Matriz LTDA"
    )

    assert (
        recovered.document_number
        == "12345678000190"
    )

    assert (
        recovered.state_registration
        == "123456789"
    )

    assert (
        recovered.email
        == "matriz@example.com"
    )

    assert recovered.phone == "1832221234"

    assert (
        recovered.website
        == "https://example.com"
    )

    assert recovered.street == "Rua Teste"
    assert recovered.number == "100"
    assert recovered.district == "Centro"
    assert recovered.city == "Rosana"
    assert recovered.state == "SP"
    assert recovered.postal_code == "19273000"

    assert recovered.is_headquarters is True
    assert recovered.is_active is True


def test_get_by_id_is_tenant_scoped(
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

    branch = Branch.create(
        tenant_id=tenant_a_id,
        code="FILIAL-A",
        name="Filial A",
    )

    repository = SQLAlchemyBranchRepository(
        session
    )

    saved = repository.add(
        branch
    )

    result = repository.get_by_id_for_tenant(
        tenant_id=tenant_b_id,
        branch_id=saved.id,
    )

    assert result is None


def test_get_by_id_returns_inactive_branch(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    branch = Branch.create(
        tenant_id=tenant_id,
        code="INATIVA",
        name="Filial Inativa",
    )

    branch.deactivate()

    repository = SQLAlchemyBranchRepository(
        session
    )

    saved = repository.add(
        branch
    )

    result = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        branch_id=saved.id,
    )

    assert result is not None
    assert result.is_active is False

    assert not repository.exists_active_for_tenant(
        tenant_id=tenant_id,
        branch_id=saved.id,
    )


def test_allows_multiple_non_headquarters_branches(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyBranchRepository(
        session
    )

    repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="FILIAL-01",
            name="Filial 01",
        )
    )

    repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="FILIAL-02",
            name="Filial 02",
        )
    )


def test_rejects_second_headquarters_for_same_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyBranchRepository(
        session
    )

    repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="MATRIZ-01",
            name="Matriz",
            is_headquarters=True,
        )
    )

    with pytest.raises(
        IntegrityError
    ):
        repository.add(
            Branch.create(
                tenant_id=tenant_id,
                code="MATRIZ-02",
                name="Outra Matriz",
                is_headquarters=True,
            )
        )


def test_allows_one_headquarters_per_different_tenant(
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

    repository = SQLAlchemyBranchRepository(
        session
    )

    repository.add(
        Branch.create(
            tenant_id=tenant_a_id,
            code="MATRIZ",
            name="Matriz A",
            is_headquarters=True,
        )
    )

    repository.add(
        Branch.create(
            tenant_id=tenant_b_id,
            code="MATRIZ",
            name="Matriz B",
            is_headquarters=True,
        )
    )
