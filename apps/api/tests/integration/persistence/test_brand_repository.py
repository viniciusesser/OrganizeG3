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


def create_brand(
    repository: SQLAlchemyBrandRepository,
    *,
    tenant_id: uuid.UUID,
    code: str,
    name: str,
) -> Brand:
    """Create and persist one brand."""

    return repository.add(
        Brand.create(
            tenant_id=tenant_id,
            code=code,
            name=name,
        )
    )


def require_brand_id(
    brand: Brand,
) -> uuid.UUID:
    """Return a persisted brand identifier."""

    if brand.id is None:
        raise RuntimeError(
            "A marca de teste deveria possuir "
            "identificador."
        )

    return brand.id


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

    saved = create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    recovered = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        brand_id=require_brand_id(
            saved
        ),
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

    saved = create_brand(
        repository,
        tenant_id=tenant_a,
        code="MARCA-001",
        name="Duratex",
    )

    result = repository.get_by_id_for_tenant(
        tenant_id=tenant_b,
        brand_id=require_brand_id(
            saved
        ),
    )

    assert result is None


def test_finds_brand_by_code(
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

    create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    recovered = repository.get_by_code_for_tenant(
        tenant_id=tenant_id,
        code=" marca-001 ",
    )

    assert recovered is not None
    assert recovered.code == "MARCA-001"


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

    create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    recovered = repository.get_by_name_for_tenant(
        tenant_id=tenant_id,
        name=" Duratex ",
    )

    assert recovered is not None
    assert recovered.name == "Duratex"


def test_lists_only_requested_tenant(
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

    create_brand(
        repository,
        tenant_id=tenant_a,
        code="MARCA-A",
        name="Arauco",
    )

    create_brand(
        repository,
        tenant_id=tenant_b,
        code="MARCA-B",
        name="Duratex",
    )

    result = repository.list_all(
        tenant_id=tenant_a
    )

    assert len(
        result
    ) == 1
    assert result[0].code == "MARCA-A"


def test_list_excludes_inactive_by_default(
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

    active = create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Arauco",
    )

    inactive = create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-002",
        name="Duratex",
    )

    inactive.deactivate()
    repository.save(
        inactive
    )

    result = repository.list_all(
        tenant_id=tenant_id
    )

    ids = {
        brand.id
        for brand in result
    }

    assert active.id in ids
    assert inactive.id not in ids


def test_list_can_include_inactive(
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

    first = create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Arauco",
    )

    second = create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-002",
        name="Duratex",
    )

    second.deactivate()
    repository.save(
        second
    )

    result = repository.list_all(
        tenant_id=tenant_id,
        include_inactive=True,
    )

    ids = {
        brand.id
        for brand in result
    }

    assert first.id in ids
    assert second.id in ids


@pytest.mark.parametrize(
    "search",
    [
        "MARCA-001",
        "marca-001",
        "Duratex",
        "duratex",
    ],
)
def test_searches_brand_by_code_or_name(
    session: Session,
    search: str,
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

    create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-002",
        name="Arauco",
    )

    result = repository.list_all(
        tenant_id=tenant_id,
        search=search,
    )

    assert len(
        result
    ) == 1
    assert result[0].code == "MARCA-001"


def test_list_paginates(
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

    create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Arauco",
    )

    create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-002",
        name="Duratex",
    )

    create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-003",
        name="Guararapes",
    )

    result = repository.list_all(
        tenant_id=tenant_id,
        limit=1,
        offset=1,
    )

    assert len(
        result
    ) == 1
    assert result[0].name == "Duratex"


def test_exists_by_code(
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

    saved = create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    assert repository.exists_by_code(
        tenant_id=tenant_id,
        code="marca-001",
    )

    assert not repository.exists_by_code(
        tenant_id=tenant_id,
        code="MARCA-001",
        exclude_brand_id=require_brand_id(
            saved
        ),
    )


def test_exists_by_name(
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

    saved = create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    assert repository.exists_by_name(
        tenant_id=tenant_id,
        name=" Duratex ",
    )

    assert not repository.exists_by_name(
        tenant_id=tenant_id,
        name="Duratex",
        exclude_brand_id=require_brand_id(
            saved
        ),
    )


def test_saves_brand_changes(
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

    saved = create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    saved.update_details(
        code="MARCA-002",
        name="Arauco",
    )

    updated = repository.save(
        saved
    )

    assert updated.code == "MARCA-002"
    assert updated.name == "Arauco"

    recovered = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        brand_id=require_brand_id(
            saved
        ),
    )

    assert recovered is not None
    assert recovered.code == "MARCA-002"
    assert recovered.name == "Arauco"


def test_save_preserves_tenant_isolation(
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

    saved = create_brand(
        repository,
        tenant_id=tenant_a,
        code="MARCA-001",
        name="Duratex",
    )

    foreign_brand = Brand(
        id=require_brand_id(
            saved
        ),
        tenant_id=tenant_b,
        code="MARCA-002",
        name="Arauco",
        is_active=True,
        created_at=saved.created_at,
        updated_at=saved.updated_at,
    )

    with pytest.raises(
        ValueError,
        match="não foi encontrada",
    ):
        repository.save(
            foreign_brand
        )


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

    create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    with pytest.raises(
        IntegrityError
    ):
        create_brand(
            repository,
            tenant_id=tenant_id,
            code="marca-001",
            name="Arauco",
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

    create_brand(
        repository,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    with pytest.raises(
        IntegrityError
    ):
        create_brand(
            repository,
            tenant_id=tenant_id,
            code="MARCA-002",
            name="Duratex",
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

    create_brand(
        repository,
        tenant_id=tenant_a,
        code="MARCA-001",
        name="Duratex",
    )

    create_brand(
        repository,
        tenant_id=tenant_b,
        code="MARCA-001",
        name="Duratex",
    )
