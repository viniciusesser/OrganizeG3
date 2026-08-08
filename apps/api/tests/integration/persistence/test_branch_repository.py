"""Integration tests for branch persistence."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from organizeg3_api.infrastructure.persistence.models import (
    BranchModel,
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories import (
    SQLAlchemyBranchRepository,
)


def create_tenant(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    name: str,
) -> TenantRecordModel:
    """Create one active tenant."""

    tenant = TenantRecordModel(
        id=tenant_id,
        name=name,
        status="ACTIVE",
        is_active=True,
    )

    session.add(tenant)
    session.flush()

    return tenant


def create_branch(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    branch_id: uuid.UUID,
    code: str,
    is_active: bool = True,
) -> BranchModel:
    """Create one branch."""

    branch = BranchModel(
        id=branch_id,
        tenant_id=tenant_id,
        code=code,
        name=f"Filial {code}",
        is_active=is_active,
    )

    session.add(branch)
    session.flush()

    return branch


def test_finds_active_branch_for_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    create_branch(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
        code="MATRIZ",
    )

    repository = SQLAlchemyBranchRepository(
        session
    )

    assert repository.exists_active_for_tenant(
        tenant_id=tenant_id,
        branch_id=branch_id,
    )


def test_rejects_inactive_branch(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    create_branch(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
        code="INATIVA",
        is_active=False,
    )

    repository = SQLAlchemyBranchRepository(
        session
    )

    assert not repository.exists_active_for_tenant(
        tenant_id=tenant_id,
        branch_id=branch_id,
    )


def test_rejects_branch_from_other_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=other_tenant_id,
        name="Tenant B",
    )

    create_branch(
        session,
        tenant_id=other_tenant_id,
        branch_id=branch_id,
        code="OUTRA",
    )

    repository = SQLAlchemyBranchRepository(
        session
    )

    assert not repository.exists_active_for_tenant(
        tenant_id=tenant_id,
        branch_id=branch_id,
    )


def test_rejects_unknown_branch(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    repository = SQLAlchemyBranchRepository(
        session
    )

    assert not repository.exists_active_for_tenant(
        tenant_id=tenant_id,
        branch_id=uuid.uuid4(),
    )
