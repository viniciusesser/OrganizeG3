"""Unit tests for production core domain."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import uuid

import pytest

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
from organizeg3_api.domain.production.value_objects import (
    ProductionExecutionStatus,
    ProductionOperationStatus,
    ProductionOrderStatus,
    ProductionPriority,
)


def test_creates_production_order() -> None:
    order = ProductionOrder.create(
        tenant_id=uuid.uuid4(),
        code=" op-001 ",
        title=" Cozinha Cliente A ",
        priority=ProductionPriority.HIGH,
    )

    assert order.id is not None
    assert order.code == "OP-001"
    assert order.title == "Cozinha Cliente A"
    assert order.status is ProductionOrderStatus.PLANNED
    assert order.priority is ProductionPriority.HIGH
    assert order.is_active is True


def test_production_order_lifecycle() -> None:
    order = ProductionOrder.create(
        tenant_id=uuid.uuid4(),
        code="OP-001",
        title="Projeto",
    )

    order.release()
    assert order.status is ProductionOrderStatus.RELEASED

    order.start()
    assert order.status is ProductionOrderStatus.IN_PROGRESS

    order.pause()
    assert order.status is ProductionOrderStatus.PAUSED

    order.start()
    order.complete()

    assert order.status is ProductionOrderStatus.COMPLETED


def test_rejects_invalid_planning_dates() -> None:
    start = datetime.now(UTC)

    with pytest.raises(
        ValueError,
        match="término planejado",
    ):
        ProductionOrder.create(
            tenant_id=uuid.uuid4(),
            code="OP-001",
            title="Projeto",
            planned_start_at=start,
            planned_end_at=(
                start
                - timedelta(hours=1)
            ),
        )


def test_allows_order_without_branch() -> None:
    order = ProductionOrder.create(
        tenant_id=uuid.uuid4(),
        code="OP-001",
        title="Projeto",
    )

    assert order.branch_id is None


def test_creates_production_operation() -> None:
    operation = ProductionOperation.create(
        tenant_id=uuid.uuid4(),
        production_order_id=uuid.uuid4(),
        sequence=1,
        name="Corte",
        service_id=uuid.uuid4(),
        machine_id=uuid.uuid4(),
    )

    assert operation.id is not None
    assert operation.sequence == 1
    assert operation.name == "Corte"
    assert (
        operation.status
        is ProductionOperationStatus.PENDING
    )
    assert operation.is_applicable is True


def test_operation_lifecycle() -> None:
    operation = ProductionOperation.create(
        tenant_id=uuid.uuid4(),
        production_order_id=uuid.uuid4(),
        sequence=1,
        name="Montagem",
    )

    operation.mark_ready()
    operation.start()
    operation.pause()
    operation.start()
    operation.complete()

    assert (
        operation.status
        is ProductionOperationStatus.COMPLETED
    )


def test_operation_can_be_not_applicable() -> None:
    operation = ProductionOperation.create(
        tenant_id=uuid.uuid4(),
        production_order_id=uuid.uuid4(),
        sequence=1,
        name="Fitagem",
    )

    operation.mark_not_applicable()

    assert operation.is_applicable is False

    assert (
        operation.status
        is ProductionOperationStatus.NOT_APPLICABLE
    )


def test_completed_operation_can_be_reopened_for_rework() -> None:
    operation = ProductionOperation.create(
        tenant_id=uuid.uuid4(),
        production_order_id=uuid.uuid4(),
        sequence=1,
        name="Montagem",
    )

    operation.mark_ready()
    operation.start()
    operation.complete()
    operation.reopen()

    assert operation.is_applicable is True

    assert (
        operation.status
        is ProductionOperationStatus.READY
    )


def test_creates_execution() -> None:
    execution = ProductionExecution.start(
        tenant_id=uuid.uuid4(),
        operation_id=uuid.uuid4(),
        employee_id=uuid.uuid4(),
    )

    assert execution.id is not None

    assert (
        execution.status
        is ProductionExecutionStatus.RUNNING
    )

    assert execution.finished_at is None


def test_execution_can_pause_and_resume() -> None:
    execution = ProductionExecution.start(
        tenant_id=uuid.uuid4(),
        operation_id=uuid.uuid4(),
        employee_id=uuid.uuid4(),
    )

    execution.pause()

    assert (
        execution.status
        is ProductionExecutionStatus.PAUSED
    )

    execution.resume()

    assert (
        execution.status
        is ProductionExecutionStatus.RUNNING
    )


def test_execution_can_complete() -> None:
    started_at = datetime.now(UTC)

    execution = ProductionExecution.start(
        tenant_id=uuid.uuid4(),
        operation_id=uuid.uuid4(),
        employee_id=uuid.uuid4(),
        started_at=started_at,
    )

    execution.complete(
        finished_at=(
            started_at
            + timedelta(minutes=30)
        )
    )

    assert (
        execution.status
        is ProductionExecutionStatus.COMPLETED
    )

    assert execution.finished_at is not None


def test_rejects_execution_finish_before_start() -> None:
    started_at = datetime.now(UTC)

    execution = ProductionExecution.start(
        tenant_id=uuid.uuid4(),
        operation_id=uuid.uuid4(),
        employee_id=uuid.uuid4(),
        started_at=started_at,
    )

    with pytest.raises(
        ValueError,
        match="não pode anteceder",
    ):
        execution.complete(
            finished_at=(
                started_at
                - timedelta(minutes=1)
            )
        )


def test_multiple_employees_can_execute_same_operation() -> None:
    tenant_id = uuid.uuid4()
    operation_id = uuid.uuid4()

    first = ProductionExecution.start(
        tenant_id=tenant_id,
        operation_id=operation_id,
        employee_id=uuid.uuid4(),
    )

    second = ProductionExecution.start(
        tenant_id=tenant_id,
        operation_id=operation_id,
        employee_id=uuid.uuid4(),
    )

    assert first.operation_id == second.operation_id
    assert first.employee_id != second.employee_id


def test_operation_can_change_machine() -> None:
    operation = ProductionOperation.create(
        tenant_id=uuid.uuid4(),
        production_order_id=uuid.uuid4(),
        sequence=1,
        name="Corte",
    )

    machine_id = uuid.uuid4()

    operation.assign_machine(
        machine_id
    )

    assert operation.machine_id == machine_id

    operation.remove_machine()

    assert operation.machine_id is None


def test_rejects_non_positive_operation_sequence() -> None:
    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        ProductionOperation.create(
            tenant_id=uuid.uuid4(),
            production_order_id=uuid.uuid4(),
            sequence=0,
            name="Corte",
        )


def test_creates_open_pause_and_normalizes_reason() -> None:
    pause = ProductionPause.start(
        tenant_id=uuid.uuid4(),
        execution_id=uuid.uuid4(),
        reason_code=" falta_material ",
        notes=" aguardando compra ",
    )

    assert pause.id is not None
    assert pause.reason_code == "FALTA_MATERIAL"
    assert pause.notes == "aguardando compra"
    assert pause.is_open is True


def test_pause_can_be_finished() -> None:
    started_at = datetime.now(UTC)

    pause = ProductionPause.start(
        tenant_id=uuid.uuid4(),
        execution_id=uuid.uuid4(),
        reason_code="MANUTENCAO_MAQUINA",
        started_at=started_at,
    )

    ended_at = (
        started_at
        + timedelta(minutes=20)
    )

    pause.finish(
        ended_at=ended_at
    )

    assert pause.is_open is False
    assert pause.ended_at == ended_at


def test_rejects_pause_finish_before_start() -> None:
    started_at = datetime.now(UTC)

    pause = ProductionPause.start(
        tenant_id=uuid.uuid4(),
        execution_id=uuid.uuid4(),
        reason_code="OUTRO",
        started_at=started_at,
    )

    with pytest.raises(
        ValueError,
        match="não pode anteceder",
    ):
        pause.finish(
            ended_at=(
                started_at
                - timedelta(minutes=1)
            )
        )


def test_creates_production_event() -> None:
    event = ProductionEvent.create(
        tenant_id=uuid.uuid4(),
        production_order_id=uuid.uuid4(),
        event_type=ProductionEventType.REWORK,
        reason_code=" erro_medida ",
        notes=" retornar para corte ",
    )

    assert event.id is not None
    assert event.event_type is ProductionEventType.REWORK
    assert event.reason_code == "ERRO_MEDIDA"
    assert event.notes == "retornar para corte"


def test_event_execution_requires_operation() -> None:
    with pytest.raises(
        ValueError,
        match="deve informar a operação",
    ):
        ProductionEvent.create(
            tenant_id=uuid.uuid4(),
            production_order_id=uuid.uuid4(),
            execution_id=uuid.uuid4(),
            event_type=(
                ProductionEventType.EXECUTION_STARTED
            ),
        )


def test_event_can_record_material_shortage() -> None:
    order_id = uuid.uuid4()
    operation_id = uuid.uuid4()
    employee_id = uuid.uuid4()

    event = ProductionEvent.create(
        tenant_id=uuid.uuid4(),
        production_order_id=order_id,
        operation_id=operation_id,
        employee_id=employee_id,
        event_type=(
            ProductionEventType.MATERIAL_SHORTAGE
        ),
        reason_code="SEM_CHAPA",
        notes="MDF indisponível.",
    )

    assert event.production_order_id == order_id
    assert event.operation_id == operation_id
    assert event.employee_id == employee_id
    assert (
        event.event_type
        is ProductionEventType.MATERIAL_SHORTAGE
    )
