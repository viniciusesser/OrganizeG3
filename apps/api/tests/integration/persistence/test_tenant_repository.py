"""Integration tests for tenant persistence queries."""

import uuid

import pytest
from sqlalchemy.orm import Session

from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories.tenant_repository import (
    SQLAlchemyTenantRepository,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.database,
]


def test_finds_active_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    session.add(
        TenantRecordModel(
            id=tenant_id,
            name="Empresa Ativa",
            status="ACTIVE",
            is_active=True,
        )
    )

    session.flush()

    repository = SQLAlchemyTenantRepository(
        session
    )

    assert repository.exists_active(
        tenant_id
    )


def test_rejects_inactive_flag(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    session.add(
        TenantRecordModel(
            id=tenant_id,
            name="Empresa Inativa",
            status="ACTIVE",
            is_active=False,
        )
    )

    session.flush()

    repository = SQLAlchemyTenantRepository(
        session
    )

    assert not repository.exists_active(
        tenant_id
    )


def test_rejects_non_active_status(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    session.add(
        TenantRecordModel(
            id=tenant_id,
            name="Empresa Suspensa",
            status="SUSPENDED",
            is_active=True,
        )
    )

    session.flush()

    repository = SQLAlchemyTenantRepository(
        session
    )

    assert not repository.exists_active(
        tenant_id
    )


def test_rejects_unknown_tenant(
    session: Session,
) -> None:
    repository = SQLAlchemyTenantRepository(
        session
    )

    assert not repository.exists_active(
        uuid.uuid4()
    )
