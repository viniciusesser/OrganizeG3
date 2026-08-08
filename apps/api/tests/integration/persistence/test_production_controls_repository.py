"""Integration tests for production assignment and checklist repositories."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import uuid

import pytest
from sqlalchemy.orm import Session

from organizeg3_api.domain.production import (
    ProductionAssignment,
    ProductionChecklistItem,
    ProductionOperation,
    ProductionOrder,
)
from organizeg3_api.infrastructure.persistence.models.employee import (
    EmployeeModel,
)
from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories.production_controls_repository import (
    SQLAlchemyProductionAssignmentRepository,
    SQLAlchemyProductionChecklistItemRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.production_repository import (
    SQLAlchemyProductionOperationRepository,
    SQLAlchemyProductionOrderRepository,
)


def fixed_time() -> datetime:
    return datetime(
        2026,
        8,
        8,
        12,
        0,
        tzinfo=UTC,
    )


def create_tenant(
    session: Session,
    *,
    name: str,
) -> TenantRecordModel:
    tenant = TenantRecordModel(
        id=uuid.uuid4(),
        name=name,
        status="ACTIVE",
        is_active=True,
    )

    session.add(tenant)
    session.flush()

    return tenant


def create_employee(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str,
) -> EmployeeModel:
    employee = EmployeeModel(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        code=code,
        full_name=f"Funcionário {code}",
        status="ACTIVE",
        is_active=True,
    )

    session.add(employee)
    session.flush()

    return employee


def create_operation(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str,
) -> ProductionOperation:
    order_repository = SQLAlchemyProductionOrderRepository(
        session
    )

    order = order_repository.add(
        ProductionOrder.create(
            tenant_id=tenant_id,
            code=code,
            title=f"Ordem {code}",
        )
    )

    assert order.id is not None

    operation_repository = SQLAlchemyProductionOperationRepository(
        session
    )

    operation = operation_repository.add(
        ProductionOperation.create(
            tenant_id=tenant_id,
            production_order_id=order.id,
            sequence=1,
            name="Corte",
        )
    )

    assert operation.id is not None

    return operation


def test_persists_production_assignment(
    session: Session,
) -> None:
    tenant = create_tenant(
        session,
        name="Tenant Assignment",
    )

    employee = create_employee(
        session,
        tenant_id=tenant.id,
        code="EMP-001",
    )

    operation = create_operation(
        session,
        tenant_id=tenant.id,
        code="OP-ASSIGN-001",
    )

    repository = SQLAlchemyProductionAssignmentRepository(
        session
    )

    assignment = repository.add(
        ProductionAssignment.create(
            tenant_id=tenant.id,
            production_operation_id=operation.id,
            employee_id=employee.id,
            assigned_at=fixed_time(),
        )
    )

    assert assignment.id is not None
    assert assignment.employee_id == employee.id
    assert assignment.is_active is True


def test_rejects_assignment_with_cross_tenant_operation(
    session: Session,
) -> None:
    tenant_a = create_tenant(
        session,
        name="Tenant A",
    )
    tenant_b = create_tenant(
        session,
        name="Tenant B",
    )

    employee = create_employee(
        session,
        tenant_id=tenant_a.id,
        code="EMP-A",
    )

    operation_b = create_operation(
        session,
        tenant_id=tenant_b.id,
        code="OP-B",
    )

    repository = SQLAlchemyProductionAssignmentRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="operação de produção não pertence",
    ):
        repository.add(
            ProductionAssignment.create(
                tenant_id=tenant_a.id,
                production_operation_id=operation_b.id,
                employee_id=employee.id,
                assigned_at=fixed_time(),
            )
        )


def test_rejects_assignment_with_cross_tenant_employee(
    session: Session,
) -> None:
    tenant_a = create_tenant(
        session,
        name="Tenant A",
    )
    tenant_b = create_tenant(
        session,
        name="Tenant B",
    )

    employee_b = create_employee(
        session,
        tenant_id=tenant_b.id,
        code="EMP-B",
    )

    operation_a = create_operation(
        session,
        tenant_id=tenant_a.id,
        code="OP-A",
    )

    repository = SQLAlchemyProductionAssignmentRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="funcionário não pertence",
    ):
        repository.add(
            ProductionAssignment.create(
                tenant_id=tenant_a.id,
                production_operation_id=operation_a.id,
                employee_id=employee_b.id,
                assigned_at=fixed_time(),
            )
        )


def test_rejects_duplicate_active_assignment(
    session: Session,
) -> None:
    tenant = create_tenant(
        session,
        name="Tenant Duplicate",
    )

    employee = create_employee(
        session,
        tenant_id=tenant.id,
        code="EMP-DUP",
    )

    operation = create_operation(
        session,
        tenant_id=tenant.id,
        code="OP-DUP",
    )

    repository = SQLAlchemyProductionAssignmentRepository(
        session
    )

    repository.add(
        ProductionAssignment.create(
            tenant_id=tenant.id,
            production_operation_id=operation.id,
            employee_id=employee.id,
            assigned_at=fixed_time(),
        )
    )

    with pytest.raises(
        ValueError,
        match="já possui uma atribuição ativa",
    ):
        repository.add(
            ProductionAssignment.create(
                tenant_id=tenant.id,
                production_operation_id=operation.id,
                employee_id=employee.id,
                assigned_at=fixed_time()
                + timedelta(
                    minutes=10
                ),
            )
        )


def test_unassign_and_reassign_preserves_history(
    session: Session,
) -> None:
    tenant = create_tenant(
        session,
        name="Tenant History",
    )

    employee = create_employee(
        session,
        tenant_id=tenant.id,
        code="EMP-HIST",
    )

    operation = create_operation(
        session,
        tenant_id=tenant.id,
        code="OP-HIST",
    )

    repository = SQLAlchemyProductionAssignmentRepository(
        session
    )

    assignment = repository.add(
        ProductionAssignment.create(
            tenant_id=tenant.id,
            production_operation_id=operation.id,
            employee_id=employee.id,
            assigned_at=fixed_time(),
        )
    )

    assignment.unassign(
        at=fixed_time()
        + timedelta(
            hours=1
        )
    )

    repository.save(
        assignment
    )

    second = repository.add(
        ProductionAssignment.create(
            tenant_id=tenant.id,
            production_operation_id=operation.id,
            employee_id=employee.id,
            assigned_at=fixed_time()
            + timedelta(
                hours=2
            ),
        )
    )

    assignments = repository.list_by_operation_for_tenant(
        tenant_id=tenant.id,
        production_operation_id=operation.id,
    )

    assert len(assignments) == 2
    assert assignments[0].is_active is False
    assert assignments[1].id == second.id
    assert assignments[1].is_active is True


def test_lists_only_active_assignments(
    session: Session,
) -> None:
    tenant = create_tenant(
        session,
        name="Tenant Active",
    )

    employee_a = create_employee(
        session,
        tenant_id=tenant.id,
        code="EMP-ACT-A",
    )
    employee_b = create_employee(
        session,
        tenant_id=tenant.id,
        code="EMP-ACT-B",
    )

    operation = create_operation(
        session,
        tenant_id=tenant.id,
        code="OP-ACT",
    )

    repository = SQLAlchemyProductionAssignmentRepository(
        session
    )

    inactive = repository.add(
        ProductionAssignment.create(
            tenant_id=tenant.id,
            production_operation_id=operation.id,
            employee_id=employee_a.id,
            assigned_at=fixed_time(),
        )
    )

    inactive.unassign(
        at=fixed_time()
        + timedelta(
            minutes=30
        )
    )

    repository.save(
        inactive
    )

    active = repository.add(
        ProductionAssignment.create(
            tenant_id=tenant.id,
            production_operation_id=operation.id,
            employee_id=employee_b.id,
            assigned_at=fixed_time()
            + timedelta(
                hours=1
            ),
        )
    )

    assignments = repository.list_by_operation_for_tenant(
        tenant_id=tenant.id,
        production_operation_id=operation.id,
        active_only=True,
    )

    assert len(assignments) == 1
    assert assignments[0].id == active.id


def test_persists_checklist_item(
    session: Session,
) -> None:
    tenant = create_tenant(
        session,
        name="Tenant Checklist",
    )

    operation = create_operation(
        session,
        tenant_id=tenant.id,
        code="OP-CHK-001",
    )

    repository = SQLAlchemyProductionChecklistItemRepository(
        session
    )

    item = repository.add(
        ProductionChecklistItem.create(
            tenant_id=tenant.id,
            production_operation_id=operation.id,
            sequence=1,
            title="Conferir medidas",
        )
    )

    assert item.id is not None
    assert item.title == "Conferir medidas"
    assert item.is_pending is True


def test_rejects_checklist_with_cross_tenant_operation(
    session: Session,
) -> None:
    tenant_a = create_tenant(
        session,
        name="Tenant Checklist A",
    )
    tenant_b = create_tenant(
        session,
        name="Tenant Checklist B",
    )

    operation_b = create_operation(
        session,
        tenant_id=tenant_b.id,
        code="OP-CHK-B",
    )

    repository = SQLAlchemyProductionChecklistItemRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="operação de produção não pertence",
    ):
        repository.add(
            ProductionChecklistItem.create(
                tenant_id=tenant_a.id,
                production_operation_id=operation_b.id,
                sequence=1,
                title="Teste",
            )
        )


def test_completed_checklist_validates_employee_tenant(
    session: Session,
) -> None:
    tenant_a = create_tenant(
        session,
        name="Tenant Complete A",
    )
    tenant_b = create_tenant(
        session,
        name="Tenant Complete B",
    )

    operation = create_operation(
        session,
        tenant_id=tenant_a.id,
        code="OP-COMPLETE",
    )

    employee_b = create_employee(
        session,
        tenant_id=tenant_b.id,
        code="EMP-COMP-B",
    )

    item = ProductionChecklistItem.create(
        tenant_id=tenant_a.id,
        production_operation_id=operation.id,
        sequence=1,
        title="Conferência",
    )

    item.complete(
        employee_id=employee_b.id,
        completed_at=fixed_time(),
    )

    repository = SQLAlchemyProductionChecklistItemRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="funcionário não pertence",
    ):
        repository.add(
            item
        )


def test_checklist_completion_is_persisted(
    session: Session,
) -> None:
    tenant = create_tenant(
        session,
        name="Tenant Complete",
    )

    employee = create_employee(
        session,
        tenant_id=tenant.id,
        code="EMP-COMP",
    )

    operation = create_operation(
        session,
        tenant_id=tenant.id,
        code="OP-COMP",
    )

    repository = SQLAlchemyProductionChecklistItemRepository(
        session
    )

    item = repository.add(
        ProductionChecklistItem.create(
            tenant_id=tenant.id,
            production_operation_id=operation.id,
            sequence=1,
            title="Conferência",
        )
    )

    item.complete(
        employee_id=employee.id,
        completed_at=fixed_time(),
    )

    saved = repository.save(
        item
    )

    assert saved.is_completed is True
    assert saved.completed_by_employee_id == employee.id
    assert saved.completed_at == fixed_time()


def test_checklist_reopen_is_persisted(
    session: Session,
) -> None:
    tenant = create_tenant(
        session,
        name="Tenant Reopen",
    )

    operation = create_operation(
        session,
        tenant_id=tenant.id,
        code="OP-REOPEN",
    )

    repository = SQLAlchemyProductionChecklistItemRepository(
        session
    )

    item = repository.add(
        ProductionChecklistItem.create(
            tenant_id=tenant.id,
            production_operation_id=operation.id,
            sequence=1,
            title="Reabrir",
        )
    )

    item.complete(
        completed_at=fixed_time(),
    )

    item = repository.save(
        item
    )

    item.reopen()

    reopened = repository.save(
        item
    )

    assert reopened.is_pending is True
    assert reopened.completed_at is None


def test_checklist_not_applicable_is_persisted(
    session: Session,
) -> None:
    tenant = create_tenant(
        session,
        name="Tenant N/A",
    )

    operation = create_operation(
        session,
        tenant_id=tenant.id,
        code="OP-NA",
    )

    repository = SQLAlchemyProductionChecklistItemRepository(
        session
    )

    item = repository.add(
        ProductionChecklistItem.create(
            tenant_id=tenant.id,
            production_operation_id=operation.id,
            sequence=1,
            title="Instalar puxador",
        )
    )

    item.mark_not_applicable(
        notes="Não se aplica ao projeto."
    )

    saved = repository.save(
        item
    )

    assert saved.is_applicable is False
    assert saved.is_pending is False
    assert saved.notes == "Não se aplica ao projeto."


def test_checklist_items_are_ordered_by_sequence(
    session: Session,
) -> None:
    tenant = create_tenant(
        session,
        name="Tenant Order",
    )

    operation = create_operation(
        session,
        tenant_id=tenant.id,
        code="OP-ORDER",
    )

    repository = SQLAlchemyProductionChecklistItemRepository(
        session
    )

    repository.add(
        ProductionChecklistItem.create(
            tenant_id=tenant.id,
            production_operation_id=operation.id,
            sequence=2,
            title="Segundo",
        )
    )

    repository.add(
        ProductionChecklistItem.create(
            tenant_id=tenant.id,
            production_operation_id=operation.id,
            sequence=1,
            title="Primeiro",
        )
    )

    items = repository.list_by_operation_for_tenant(
        tenant_id=tenant.id,
        production_operation_id=operation.id,
    )

    assert [
        item.sequence
        for item in items
    ] == [
        1,
        2,
    ]
