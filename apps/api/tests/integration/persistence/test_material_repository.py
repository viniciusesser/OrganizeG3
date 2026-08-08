"""Integration tests for material persistence."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from organizeg3_api.domain.brand.entity import (
    Brand,
)
from organizeg3_api.domain.material.entity import (
    Material,
)
from organizeg3_api.infrastructure.persistence.models import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories import (
    SQLAlchemyBrandRepository,
    SQLAlchemyMaterialRepository,
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


def test_adds_and_recovers_complete_material(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    brand_repository = SQLAlchemyBrandRepository(
        session
    )

    brand = brand_repository.add(
        Brand.create(
            tenant_id=tenant_id,
            code="MARCA-001",
            name="Duratex",
        )
    )

    assert brand.id is not None

    repository = SQLAlchemyMaterialRepository(
        session
    )

    saved = repository.add(
        Material.create(
            tenant_id=tenant_id,
            code="MAT-001",
            name="MDF Branco TX 15mm",
            category="Chapas",
            unit="UN",
            brand_id=brand.id,
        )
    )

    assert saved.id is not None

    recovered = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        material_id=saved.id,
    )

    assert recovered is not None
    assert recovered.code == "MAT-001"
    assert recovered.name == "MDF Branco TX 15mm"
    assert recovered.category == "Chapas"
    assert recovered.unit == "UN"
    assert recovered.brand_id == brand.id


def test_allows_material_without_brand(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyMaterialRepository(
        session
    )

    saved = repository.add(
        Material.create(
            tenant_id=tenant_id,
            code="MAT-001",
            name="Fita",
            category="Fitas",
            unit="M",
        )
    )

    assert saved.brand_id is None


def test_material_lookup_is_tenant_scoped(
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

    repository = SQLAlchemyMaterialRepository(
        session
    )

    saved = repository.add(
        Material.create(
            tenant_id=tenant_a,
            code="MAT-001",
            name="Material",
            category="Categoria",
            unit="UN",
        )
    )

    assert saved.id is not None

    result = repository.get_by_id_for_tenant(
        tenant_id=tenant_b,
        material_id=saved.id,
    )

    assert result is None


def test_finds_material_by_normalized_code(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyMaterialRepository(
        session
    )

    repository.add(
        Material.create(
            tenant_id=tenant_id,
            code="MAT-001",
            name="Material",
            category="Categoria",
            unit="UN",
        )
    )

    recovered = repository.get_by_code_for_tenant(
        tenant_id=tenant_id,
        code=" mat-001 ",
    )

    assert recovered is not None
    assert recovered.code == "MAT-001"


def test_rejects_duplicate_material_code_in_same_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyMaterialRepository(
        session
    )

    repository.add(
        Material.create(
            tenant_id=tenant_id,
            code="MAT-001",
            name="Material A",
            category="Categoria",
            unit="UN",
        )
    )

    with pytest.raises(
        IntegrityError
    ):
        repository.add(
            Material.create(
                tenant_id=tenant_id,
                code="mat-001",
                name="Material B",
                category="Categoria",
                unit="UN",
            )
        )


def test_allows_same_material_code_in_different_tenants(
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

    repository = SQLAlchemyMaterialRepository(
        session
    )

    repository.add(
        Material.create(
            tenant_id=tenant_a,
            code="MAT-001",
            name="Material A",
            category="Categoria",
            unit="UN",
        )
    )

    repository.add(
        Material.create(
            tenant_id=tenant_b,
            code="MAT-001",
            name="Material B",
            category="Categoria",
            unit="UN",
        )
    )


def test_rejects_brand_from_another_tenant(
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

    brand_repository = SQLAlchemyBrandRepository(
        session
    )

    foreign_brand = brand_repository.add(
        Brand.create(
            tenant_id=tenant_b,
            code="MARCA-001",
            name="Duratex",
        )
    )

    assert foreign_brand.id is not None

    repository = SQLAlchemyMaterialRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="marca",
    ):
        repository.add(
            Material.create(
                tenant_id=tenant_a,
                code="MAT-001",
                name="Material",
                category="Categoria",
                unit="UN",
                brand_id=foreign_brand.id,
            )
        )


def test_rejects_unknown_brand(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyMaterialRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="marca",
    ):
        repository.add(
            Material.create(
                tenant_id=tenant_id,
                code="MAT-001",
                name="Material",
                category="Categoria",
                unit="UN",
                brand_id=uuid.uuid4(),
            )
        )
