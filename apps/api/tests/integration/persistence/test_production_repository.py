"""Integration tests for production persistence repositories."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy.orm import Session

from organizeg3_api.domain.production.event import (
    ProductionEvent,
    ProductionEventType,
)
from organizeg3_api.domain.production.execution import (
    ProductionExecution,
)
from organizeg3_api.domain.production.operation import (
    ProductionOperation,
)
from organizeg3_api.domain.production.order import (
    ProductionOrder,
)
from organizeg3_api.domain.production.pause import (
    ProductionPause,
)
from organizeg3_api.infrastructure.persistence.models.branch import (
    BranchModel,
)
from organizeg3_api.infrastructure.persistence.models.employee import (
    EmployeeModel,
)
from organizeg3_api.infrastructure.persistence.models.machine import (
    MachineModel,
)
from organizeg3_api.infrastructure.persistence.models.service import (
    ServiceModel,
)
from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories.production_repository import (
    SQLAlchemyProductionEventRepository,
    SQLAlchemyProductionExecutionRepository,
    SQLAlchemyProductionOperationRepository,
    SQLAlchemyProductionOrderRepository,
    SQLAlchemyProductionPauseRepository,
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
    code: str = "BR-001",
) -> BranchModel:
    branch = BranchModel(
        tenant_id=tenant_id,
        code=code,
        name=f"Filial {code}",
        is_headquarters=False,
        is_active=True,
    )

    session.add(branch)
    session.flush()

    return branch


def create_employee(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "EMP-001",
) -> EmployeeModel:
    employee = EmployeeModel(
        tenant_id=tenant_id,
        code=code,
        full_name=f"Funcionário {code}",
        status="ACTIVE",
        is_active=True,
    )

    session.add(employee)
    session.flush()

    return employee


def create_service(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "SRV-001",
) -> ServiceModel:
    service = ServiceModel(
        tenant_id=tenant_id,
        code=code,
        name=f"Serviço {code}",
        category="PRODUCTION",
        unit="SERVICE",
        execution_mode="INTERNAL",
        estimated_duration_minutes=30,
        is_active=True,
    )

    session.add(service)
    session.flush()

    return service


def create_machine(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "MAQ-001",
) -> MachineModel:
    machine = MachineModel(
        tenant_id=tenant_id,
        code=code,
        name=f"Máquina {code}",
        machine_type="CUTTING",
        status="AVAILABLE",
        is_active=True,
    )

    session.add(machine)
    session.flush()

    return machine


def create_order(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "OP-001",
    branch_id: uuid.UUID | None = None,
) -> ProductionOrder:
    repository = SQLAlchemyProductionOrderRepository(
        session
    )

    order = ProductionOrder.create(
        tenant_id=tenant_id,
        branch_id=branch_id,
        code=code,
        title=f"Produção {code}",
    )

    return repository.add(
        order
    )


def create_operation(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    production_order_id: uuid.UUID,
    sequence: int = 1,
    service_id: uuid.UUID | None = None,
    machine_id: uuid.UUID | None = None,
) -> ProductionOperation:
    repository = (
        SQLAlchemyProductionOperationRepository(
            session
        )
    )

    operation = ProductionOperation.create(
        tenant_id=tenant_id,
        production_order_id=production_order_id,
        sequence=sequence,
        name=f"Operação {sequence}",
        service_id=service_id,
        machine_id=machine_id,
    )

    return repository.add(
        operation
    )


def create_execution(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    operation_id: uuid.UUID,
    employee_id: uuid.UUID,
) -> ProductionExecution:
    repository = (
        SQLAlchemyProductionExecutionRepository(
            session
        )
    )

    execution = ProductionExecution.start(
        tenant_id=tenant_id,
        operation_id=operation_id,
        employee_id=employee_id,
    )

    return repository.add(
        execution
    )


def test_persists_and_loads_production_order(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Produção",
    )

    repository = SQLAlchemyProductionOrderRepository(
        session
    )

    saved = create_order(
        session,
        tenant_id=tenant_id,
    )

    assert saved.id is not None

    loaded = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        production_order_id=saved.id,
    )

    assert loaded is not None
    assert loaded.id == saved.id
    assert loaded.code == "OP-001"
    assert loaded.title == "Produção OP-001"


def test_get_order_by_code_is_tenant_scoped(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()

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

    create_order(
        session,
        tenant_id=tenant_id,
        code="OP-001",
    )

    repository = SQLAlchemyProductionOrderRepository(
        session
    )

    assert (
        repository.get_by_code_for_tenant(
            tenant_id=tenant_id,
            code=" op-001 ",
        )
        is not None
    )

    assert (
        repository.get_by_code_for_tenant(
            tenant_id=other_tenant_id,
            code="OP-001",
        )
        is None
    )


def test_rejects_order_with_cross_tenant_branch(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()

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

    branch = create_branch(
        session,
        tenant_id=other_tenant_id,
    )

    order = ProductionOrder.create(
        tenant_id=tenant_id,
        branch_id=branch.id,
        code="OP-001",
        title="Produção",
    )

    repository = SQLAlchemyProductionOrderRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="filial",
    ):
        repository.add(
            order
        )


def test_persists_operation_with_service_and_machine(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Produção",
    )

    service = create_service(
        session,
        tenant_id=tenant_id,
    )

    machine = create_machine(
        session,
        tenant_id=tenant_id,
    )

    order = create_order(
        session,
        tenant_id=tenant_id,
    )

    assert order.id is not None

    operation = create_operation(
        session,
        tenant_id=tenant_id,
        production_order_id=order.id,
        service_id=service.id,
        machine_id=machine.id,
    )

    assert operation.id is not None
    assert operation.service_id == service.id
    assert operation.machine_id == machine.id


def test_rejects_operation_with_cross_tenant_service(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()

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

    service = create_service(
        session,
        tenant_id=other_tenant_id,
    )

    order = create_order(
        session,
        tenant_id=tenant_id,
    )

    assert order.id is not None

    operation = ProductionOperation.create(
        tenant_id=tenant_id,
        production_order_id=order.id,
        sequence=1,
        name="Corte",
        service_id=service.id,
    )

    repository = (
        SQLAlchemyProductionOperationRepository(
            session
        )
    )

    with pytest.raises(
        ValueError,
        match="serviço",
    ):
        repository.add(
            operation
        )


def test_rejects_operation_with_cross_tenant_machine(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()

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

    machine = create_machine(
        session,
        tenant_id=other_tenant_id,
    )

    order = create_order(
        session,
        tenant_id=tenant_id,
    )

    assert order.id is not None

    operation = ProductionOperation.create(
        tenant_id=tenant_id,
        production_order_id=order.id,
        sequence=1,
        name="Corte",
        machine_id=machine.id,
    )

    repository = (
        SQLAlchemyProductionOperationRepository(
            session
        )
    )

    with pytest.raises(
        ValueError,
        match="máquina",
    ):
        repository.add(
            operation
        )


def test_persists_multiple_executions_for_same_operation(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Produção",
    )

    first_employee = create_employee(
        session,
        tenant_id=tenant_id,
        code="EMP-001",
    )

    second_employee = create_employee(
        session,
        tenant_id=tenant_id,
        code="EMP-002",
    )

    order = create_order(
        session,
        tenant_id=tenant_id,
    )

    assert order.id is not None

    operation = create_operation(
        session,
        tenant_id=tenant_id,
        production_order_id=order.id,
    )

    assert operation.id is not None

    first = create_execution(
        session,
        tenant_id=tenant_id,
        operation_id=operation.id,
        employee_id=first_employee.id,
    )

    second = create_execution(
        session,
        tenant_id=tenant_id,
        operation_id=operation.id,
        employee_id=second_employee.id,
    )

    assert first.id != second.id
    assert first.operation_id == second.operation_id
    assert first.employee_id != second.employee_id


def test_rejects_execution_with_cross_tenant_employee(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()

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

    employee = create_employee(
        session,
        tenant_id=other_tenant_id,
    )

    order = create_order(
        session,
        tenant_id=tenant_id,
    )

    assert order.id is not None

    operation = create_operation(
        session,
        tenant_id=tenant_id,
        production_order_id=order.id,
    )

    assert operation.id is not None

    execution = ProductionExecution.start(
        tenant_id=tenant_id,
        operation_id=operation.id,
        employee_id=employee.id,
    )

    repository = (
        SQLAlchemyProductionExecutionRepository(
            session
        )
    )

    with pytest.raises(
        ValueError,
        match="funcionário",
    ):
        repository.add(
            execution
        )


def test_persists_production_pause(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Produção",
    )

    employee = create_employee(
        session,
        tenant_id=tenant_id,
    )

    order = create_order(
        session,
        tenant_id=tenant_id,
    )

    assert order.id is not None

    operation = create_operation(
        session,
        tenant_id=tenant_id,
        production_order_id=order.id,
    )

    assert operation.id is not None

    execution = create_execution(
        session,
        tenant_id=tenant_id,
        operation_id=operation.id,
        employee_id=employee.id,
    )

    assert execution.id is not None

    pause = ProductionPause.start(
        tenant_id=tenant_id,
        execution_id=execution.id,
        reason_code=" falta_material ",
        notes=" Aguardando chapa ",
    )

    repository = SQLAlchemyProductionPauseRepository(
        session
    )

    saved = repository.add(
        pause
    )

    assert saved.id is not None
    assert saved.reason_code == "FALTA_MATERIAL"
    assert saved.notes == "Aguardando chapa"

    loaded = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        pause_id=saved.id,
    )

    assert loaded is not None
    assert loaded.execution_id == execution.id


def test_rejects_pause_for_cross_tenant_execution(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()

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

    employee = create_employee(
        session,
        tenant_id=tenant_id,
    )

    order = create_order(
        session,
        tenant_id=tenant_id,
    )

    assert order.id is not None

    operation = create_operation(
        session,
        tenant_id=tenant_id,
        production_order_id=order.id,
    )

    assert operation.id is not None

    execution = create_execution(
        session,
        tenant_id=tenant_id,
        operation_id=operation.id,
        employee_id=employee.id,
    )

    assert execution.id is not None

    pause = ProductionPause.start(
        tenant_id=other_tenant_id,
        execution_id=execution.id,
        reason_code="AJUDA_OUTRO_SERVICO",
    )

    repository = SQLAlchemyProductionPauseRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="execução",
    ):
        repository.add(
            pause
        )


def test_persists_production_event_with_full_context(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Produção",
    )

    employee = create_employee(
        session,
        tenant_id=tenant_id,
    )

    order = create_order(
        session,
        tenant_id=tenant_id,
    )

    assert order.id is not None

    operation = create_operation(
        session,
        tenant_id=tenant_id,
        production_order_id=order.id,
    )

    assert operation.id is not None

    execution = create_execution(
        session,
        tenant_id=tenant_id,
        operation_id=operation.id,
        employee_id=employee.id,
    )

    assert execution.id is not None

    event = ProductionEvent.create(
        tenant_id=tenant_id,
        production_order_id=order.id,
        operation_id=operation.id,
        execution_id=execution.id,
        employee_id=employee.id,
        event_type=(
            ProductionEventType.MATERIAL_SHORTAGE
        ),
        reason_code=" falta_mdf ",
        notes=" MDF branco indisponível ",
    )

    repository = SQLAlchemyProductionEventRepository(
        session
    )

    saved = repository.add(
        event
    )

    assert saved.id is not None
    assert (
        saved.event_type
        is ProductionEventType.MATERIAL_SHORTAGE
    )
    assert saved.reason_code == "FALTA_MDF"
    assert saved.notes == "MDF branco indisponível"

    loaded = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        event_id=saved.id,
    )

    assert loaded is not None
    assert loaded.production_order_id == order.id
    assert loaded.operation_id == operation.id
    assert loaded.execution_id == execution.id
    assert loaded.employee_id == employee.id


def test_rejects_event_with_operation_from_other_order(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Produção",
    )

    first_order = create_order(
        session,
        tenant_id=tenant_id,
        code="OP-001",
    )

    second_order = create_order(
        session,
        tenant_id=tenant_id,
        code="OP-002",
    )

    assert first_order.id is not None
    assert second_order.id is not None

    operation = create_operation(
        session,
        tenant_id=tenant_id,
        production_order_id=first_order.id,
    )

    assert operation.id is not None

    event = ProductionEvent.create(
        tenant_id=tenant_id,
        production_order_id=second_order.id,
        operation_id=operation.id,
        event_type=ProductionEventType.REWORK,
        notes="Retorno para correção.",
    )

    repository = SQLAlchemyProductionEventRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="operação",
    ):
        repository.add(
            event
        )


def test_event_is_tenant_scoped_on_read(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()

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

    order = create_order(
        session,
        tenant_id=tenant_id,
    )

    assert order.id is not None

    event = ProductionEvent.create(
        tenant_id=tenant_id,
        production_order_id=order.id,
        event_type=ProductionEventType.NOTE,
        notes="Observação de produção.",
    )

    repository = SQLAlchemyProductionEventRepository(
        session
    )

    saved = repository.add(
        event
    )

    assert saved.id is not None

    assert (
        repository.get_by_id_for_tenant(
            tenant_id=other_tenant_id,
            event_id=saved.id,
        )
        is None
    )
