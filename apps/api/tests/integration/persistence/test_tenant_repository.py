"""Integration tests for the SQLAlchemy tenant repository."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantModel,
)
from organizeg3_api.infrastructure.persistence.repositories.tenant_repository import (
    SQLAlchemyTenantRepository,
)


def test_reports_active_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    session.add(
        TenantModel(
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

    assert repository.is_active(
        tenant_id
    )


def test_rejects_missing_tenant(
    session: Session,
) -> None:
    repository = SQLAlchemyTenantRepository(
        session
    )

    assert not repository.is_active(
        uuid.uuid4()
    )


def test_rejects_disabled_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    session.add(
        TenantModel(
            id=tenant_id,
            name="Empresa Desativada",
            status="ACTIVE",
            is_active=False,
        )
    )

    session.flush()

    repository = SQLAlchemyTenantRepository(
        session
    )

    assert not repository.is_active(
        tenant_id
    )


def test_rejects_non_active_status(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    session.add(
        TenantModel(
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

    assert not repository.is_active(
        tenant_id
    )
