"""Integration tests for machine persistence."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from organizeg3_api.domain.machine.entity import (
    Machine,
)
from organizeg3_api.domain.machine.value_objects import (
    MachineStatus,
)
from organizeg3_api.infrastructure.persistence.models import (
    BranchModel,
    MachineModel,
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories import (
    SQLAlchemyMachineRepository,
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


def create_branch(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    branch_id: uuid.UUID,
    code: str,
    name: str,
) -> None:
    """Create one branch for persistence tests."""

    session.add(
        BranchModel(
            id=branch_id,
            tenant_id=tenant_id,
            code=code,
            name=name,
            is_headquarters=False,
            is_active=True,
        )
    )
    session.flush()


def test_adds_and_recovers_complete_machine(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    create_branch(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
        code="FIL-001",
        name="Fábrica",
    )

    repository = SQLAlchemyMachineRepository(
        session
    )

    saved = repository.add(
        Machine.create(
            tenant_id=tenant_id,
            branch_id=branch_id,
            code="MAQ-001",
            name="Seccionadora",
            machine_type="Seccionadora",
            manufacturer="Homag",
            model="SAWTEQ",
            serial_number="ABC-123",
        )
    )

    assert saved.id is not None

    recovered = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        machine_id=saved.id,
    )

    assert recovered is not None
    assert recovered.branch_id == branch_id
    assert recovered.code == "MAQ-001"
    assert recovered.name == "Seccionadora"
    assert recovered.machine_type == "Seccionadora"
    assert recovered.manufacturer == "Homag"
    assert recovered.model == "SAWTEQ"
    assert recovered.serial_number == "ABC-123"
    assert recovered.status is MachineStatus.AVAILABLE
    assert recovered.is_active is True


def test_allows_machine_without_branch(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyMachineRepository(
        session
    )

    saved = repository.add(
        Machine.create(
            tenant_id=tenant_id,
            code="MAQ-001",
            name="Coladeira",
            machine_type="Coladeira",
        )
    )

    assert saved.branch_id is None


def test_machine_lookup_is_tenant_scoped(
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

    repository = SQLAlchemyMachineRepository(
        session
    )

    saved = repository.add(
        Machine.create(
            tenant_id=tenant_a,
            code="MAQ-001",
            name="Seccionadora",
            machine_type="Seccionadora",
        )
    )

    assert saved.id is not None

    result = repository.get_by_id_for_tenant(
        tenant_id=tenant_b,
        machine_id=saved.id,
    )

    assert result is None


def test_finds_machine_by_normalized_code(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyMachineRepository(
        session
    )

    repository.add(
        Machine.create(
            tenant_id=tenant_id,
            code="MAQ-001",
            name="Seccionadora",
            machine_type="Seccionadora",
        )
    )

    recovered = repository.get_by_code_for_tenant(
        tenant_id=tenant_id,
        code=" maq-001 ",
    )

    assert recovered is not None
    assert recovered.code == "MAQ-001"


def test_rejects_duplicate_code_in_same_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyMachineRepository(
        session
    )

    repository.add(
        Machine.create(
            tenant_id=tenant_id,
            code="MAQ-001",
            name="Seccionadora",
            machine_type="Seccionadora",
        )
    )

    with pytest.raises(
        IntegrityError
    ):
        repository.add(
            Machine.create(
                tenant_id=tenant_id,
                code="maq-001",
                name="Coladeira",
                machine_type="Coladeira",
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

    repository = SQLAlchemyMachineRepository(
        session
    )

    repository.add(
        Machine.create(
            tenant_id=tenant_a,
            code="MAQ-001",
            name="Máquina A",
            machine_type="Seccionadora",
        )
    )

    repository.add(
        Machine.create(
            tenant_id=tenant_b,
            code="MAQ-001",
            name="Máquina B",
            machine_type="Seccionadora",
        )
    )


def test_rejects_branch_from_another_tenant(
    session: Session,
) -> None:
    tenant_a = uuid.uuid4()
    tenant_b = uuid.uuid4()
    branch_b = uuid.uuid4()

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

    create_branch(
        session,
        tenant_id=tenant_b,
        branch_id=branch_b,
        code="FIL-B",
        name="Filial B",
    )

    repository = SQLAlchemyMachineRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="não pertence",
    ):
        repository.add(
            Machine.create(
                tenant_id=tenant_a,
                branch_id=branch_b,
                code="MAQ-001",
                name="Seccionadora",
                machine_type="Seccionadora",
            )
        )


def test_rejects_unknown_branch(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyMachineRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="não pertence",
    ):
        repository.add(
            Machine.create(
                tenant_id=tenant_id,
                branch_id=uuid.uuid4(),
                code="MAQ-001",
                name="Seccionadora",
                machine_type="Seccionadora",
            )
        )


def test_database_rejects_invalid_status(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    session.add(
        MachineModel(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            branch_id=None,
            code="MAQ-001",
            name="Máquina",
            machine_type="Tipo",
            status="INVALID",
            is_active=True,
        )
    )

    with pytest.raises(
        IntegrityError
    ):
        session.flush()


def test_database_rejects_blank_machine_type(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    session.add(
        MachineModel(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            branch_id=None,
            code="MAQ-001",
            name="Máquina",
            machine_type="   ",
            status="AVAILABLE",
            is_active=True,
        )
    )

    with pytest.raises(
        IntegrityError
    ):
        session.flush()
