"""Integration tests for brand persistence."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from organizeg3_api.domain.brand.entity import (
    Brand,
)
from organizeg3_api.infrastructure.persistence.models import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories import (
    SQLAlchemyBrandRepository,
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
) -> None:
    """Create one active tenant."""

    session.add(
        TenantRecordModel(
            id=tenant_id,
            name=name,
            status="ACTIVE",
            is_active=True,
        )
    )
    session.flush()


def test_adds_and_recovers_brand(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyBrandRepository(
        session
    )

    saved = repository.add(
        Brand.create(
            tenant_id=tenant_id,
            code="MARCA-001",
            name="Duratex",
        )
    )

    assert saved.id is not None

    recovered = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        brand_id=saved.id,
    )

    assert recovered is not None
    assert recovered.code == "MARCA-001"
    assert recovered.name == "Duratex"


def test_brand_lookup_is_tenant_scoped(
    session: Session,
) -> None:
    tenant_a = uuid.uuid4()
    tenant_b = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_a,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=tenant_b,
        name="Tenant B",
    )

    repository = SQLAlchemyBrandRepository(
        session
    )

    saved = repository.add(
        Brand.create(
            tenant_id=tenant_a,
            code="MARCA-001",
            name="Duratex",
        )
    )

    assert saved.id is not None

    result = repository.get_by_id_for_tenant(
        tenant_id=tenant_b,
        brand_id=saved.id,
    )

    assert result is None


def test_finds_brand_by_name(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyBrandRepository(
        session
    )

    repository.add(
        Brand.create(
            tenant_id=tenant_id,
            code="MARCA-001",
            name="Duratex",
        )
    )

    recovered = repository.get_by_name_for_tenant(
        tenant_id=tenant_id,
        name=" Duratex ",
    )

    assert recovered is not None
    assert recovered.name == "Duratex"


def test_rejects_duplicate_brand_code_in_same_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyBrandRepository(
        session
    )

    repository.add(
        Brand.create(
            tenant_id=tenant_id,
            code="MARCA-001",
            name="Duratex",
        )
    )

    with pytest.raises(
        IntegrityError
    ):
        repository.add(
            Brand.create(
                tenant_id=tenant_id,
                code="marca-001",
                name="Arauco",
            )
        )


def test_rejects_duplicate_brand_name_in_same_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyBrandRepository(
        session
    )

    repository.add(
        Brand.create(
            tenant_id=tenant_id,
            code="MARCA-001",
            name="Duratex",
        )
    )

    with pytest.raises(
        IntegrityError
    ):
        repository.add(
            Brand.create(
                tenant_id=tenant_id,
                code="MARCA-002",
                name="Duratex",
            )
        )


def test_allows_same_brand_data_in_different_tenants(
    session: Session,
) -> None:
    tenant_a = uuid.uuid4()
    tenant_b = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_a,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=tenant_b,
        name="Tenant B",
    )

    repository = SQLAlchemyBrandRepository(
        session
    )

    repository.add(
        Brand.create(
            tenant_id=tenant_a,
            code="MARCA-001",
            name="Duratex",
        )
    )

    repository.add(
        Brand.create(
            tenant_id=tenant_b,
            code="MARCA-001",
            name="Duratex",
        )
    )
