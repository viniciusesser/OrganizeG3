"""Integration tests for service persistence."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from organizeg3_api.domain.service.entity import (
    Service,
)
from organizeg3_api.domain.service.value_objects import (
    ServiceExecutionMode,
)
from organizeg3_api.infrastructure.persistence.models import (
    ServiceModel,
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories import (
    SQLAlchemyServiceRepository,
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


def test_adds_and_recovers_complete_service(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyServiceRepository(
        session
    )

    saved = repository.add(
        Service.create(
            tenant_id=tenant_id,
            code="SERV-001",
            name="Corte de MDF",
            category="Corte",
            unit="H",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
            estimated_duration_minutes=45,
        )
    )

    assert saved.id is not None

    recovered = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        service_id=saved.id,
    )

    assert recovered is not None
    assert recovered.code == "SERV-001"
    assert recovered.name == "Corte de MDF"
    assert recovered.category == "Corte"
    assert recovered.unit == "H"

    assert (
        recovered.execution_mode
        is ServiceExecutionMode.INTERNAL
    )

    assert (
        recovered.estimated_duration_minutes
        == 45
    )

    assert recovered.is_active is True


def test_allows_service_without_duration(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyServiceRepository(
        session
    )

    saved = repository.add(
        Service.create(
            tenant_id=tenant_id,
            code="SERV-001",
            name="Instalação",
            category="Instalação",
            unit="UN",
            execution_mode=ServiceExecutionMode.BOTH,
        )
    )

    assert (
        saved.estimated_duration_minutes
        is None
    )


def test_service_lookup_is_tenant_scoped(
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

    repository = SQLAlchemyServiceRepository(
        session
    )

    saved = repository.add(
        Service.create(
            tenant_id=tenant_a,
            code="SERV-001",
            name="Corte",
            category="Corte",
            unit="H",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
        )
    )

    assert saved.id is not None

    result = repository.get_by_id_for_tenant(
        tenant_id=tenant_b,
        service_id=saved.id,
    )

    assert result is None


def test_finds_service_by_normalized_code(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyServiceRepository(
        session
    )

    repository.add(
        Service.create(
            tenant_id=tenant_id,
            code="SERV-001",
            name="Corte",
            category="Corte",
            unit="H",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
        )
    )

    recovered = repository.get_by_code_for_tenant(
        tenant_id=tenant_id,
        code=" serv-001 ",
    )

    assert recovered is not None
    assert recovered.code == "SERV-001"


def test_rejects_duplicate_code_in_same_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyServiceRepository(
        session
    )

    repository.add(
        Service.create(
            tenant_id=tenant_id,
            code="SERV-001",
            name="Corte",
            category="Corte",
            unit="H",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
        )
    )

    with pytest.raises(
        IntegrityError
    ):
        repository.add(
            Service.create(
                tenant_id=tenant_id,
                code="serv-001",
                name="Montagem",
                category="Montagem",
                unit="H",
                execution_mode=(
                    ServiceExecutionMode.INTERNAL
                ),
            )
        )


def test_allows_same_code_in_different_tenants(
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

    repository = SQLAlchemyServiceRepository(
        session
    )

    repository.add(
        Service.create(
            tenant_id=tenant_a,
            code="SERV-001",
            name="Corte A",
            category="Corte",
            unit="H",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
        )
    )

    repository.add(
        Service.create(
            tenant_id=tenant_b,
            code="SERV-001",
            name="Corte B",
            category="Corte",
            unit="H",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
        )
    )


def test_persists_external_execution_mode(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyServiceRepository(
        session
    )

    saved = repository.add(
        Service.create(
            tenant_id=tenant_id,
            code="SERV-001",
            name="Pintura Terceirizada",
            category="Terceirizado",
            unit="UN",
            execution_mode=(
                ServiceExecutionMode.EXTERNAL
            ),
        )
    )

    assert (
        saved.execution_mode
        is ServiceExecutionMode.EXTERNAL
    )


def test_database_rejects_invalid_execution_mode(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    model = ServiceModel(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        code="SERV-001",
        name="Serviço",
        category="Categoria",
        unit="UN",
        execution_mode="INVALID",
        estimated_duration_minutes=None,
        is_active=True,
    )

    session.add(
        model
    )

    with pytest.raises(
        IntegrityError
    ):
        session.flush()


def test_database_rejects_non_positive_duration(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    model = ServiceModel(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        code="SERV-001",
        name="Serviço",
        category="Categoria",
        unit="UN",
        execution_mode="INTERNAL",
        estimated_duration_minutes=0,
        is_active=True,
    )

    session.add(
        model
    )

    with pytest.raises(
        IntegrityError
    ):
        session.flush()
