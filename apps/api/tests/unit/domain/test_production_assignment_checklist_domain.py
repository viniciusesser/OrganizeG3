"""Unit tests for production assignments and checklist items."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import uuid

import pytest

from organizeg3_api.domain.production import (
    ProductionAssignment,
    ProductionChecklistItem,
)


def utc_now() -> datetime:
    return datetime(
        2026,
        8,
        8,
        12,
        0,
        tzinfo=UTC,
    )


def test_creates_active_production_assignment() -> None:
    tenant_id = uuid.uuid4()
    operation_id = uuid.uuid4()
    employee_id = uuid.uuid4()

    assignment = ProductionAssignment.create(
        tenant_id=tenant_id,
        production_operation_id=operation_id,
        employee_id=employee_id,
        assigned_at=utc_now(),
    )

    assert assignment.id is not None
    assert assignment.tenant_id == tenant_id
    assert assignment.production_operation_id == operation_id
    assert assignment.employee_id == employee_id
    assert assignment.is_active is True
    assert assignment.unassigned_at is None


def test_assignment_can_be_unassigned() -> None:
    assignment = ProductionAssignment.create(
        tenant_id=uuid.uuid4(),
        production_operation_id=uuid.uuid4(),
        employee_id=uuid.uuid4(),
        assigned_at=utc_now(),
    )

    unassigned_at = utc_now() + timedelta(
        hours=2
    )

    assignment.unassign(
        at=unassigned_at
    )

    assert assignment.is_active is False
    assert assignment.unassigned_at == unassigned_at


def test_assignment_rejects_unassignment_before_assignment() -> None:
    assignment = ProductionAssignment.create(
        tenant_id=uuid.uuid4(),
        production_operation_id=uuid.uuid4(),
        employee_id=uuid.uuid4(),
        assigned_at=utc_now(),
    )

    with pytest.raises(
        ValueError,
        match="não pode anteceder",
    ):
        assignment.unassign(
            at=utc_now()
            - timedelta(
                minutes=1
            )
        )


def test_assignment_rejects_second_unassignment() -> None:
    assignment = ProductionAssignment.create(
        tenant_id=uuid.uuid4(),
        production_operation_id=uuid.uuid4(),
        employee_id=uuid.uuid4(),
        assigned_at=utc_now(),
    )

    assignment.unassign(
        at=utc_now()
        + timedelta(
            minutes=10
        )
    )

    with pytest.raises(
        ValueError,
        match="já está inativa",
    ):
        assignment.unassign(
            at=utc_now()
            + timedelta(
                minutes=20
            )
        )


def test_assignment_requires_timezone() -> None:
    naive_datetime = datetime.fromisoformat(
        "2026-08-08T12:00:00"
    )

    with pytest.raises(
        ValueError,
        match="timezone",
    ):
        ProductionAssignment.create(
            tenant_id=uuid.uuid4(),
            production_operation_id=uuid.uuid4(),
            employee_id=uuid.uuid4(),
            assigned_at=naive_datetime,
        )


def test_creates_pending_checklist_item() -> None:
    item = ProductionChecklistItem.create(
        tenant_id=uuid.uuid4(),
        production_operation_id=uuid.uuid4(),
        sequence=1,
        title="  Conferir medidas  ",
    )

    assert item.id is not None
    assert item.sequence == 1
    assert item.title == "Conferir medidas"
    assert item.is_required is True
    assert item.is_applicable is True
    assert item.is_pending is True
    assert item.is_completed is False


def test_checklist_item_can_be_completed() -> None:
    employee_id = uuid.uuid4()

    item = ProductionChecklistItem.create(
        tenant_id=uuid.uuid4(),
        production_operation_id=uuid.uuid4(),
        sequence=1,
        title="Conferir peças",
    )

    item.complete(
        employee_id=employee_id,
        completed_at=utc_now(),
    )

    assert item.is_completed is True
    assert item.is_pending is False
    assert item.completed_at == utc_now()
    assert (
        item.completed_by_employee_id
        == employee_id
    )


def test_checklist_item_can_be_completed_without_employee() -> None:
    item = ProductionChecklistItem.create(
        tenant_id=uuid.uuid4(),
        production_operation_id=uuid.uuid4(),
        sequence=1,
        title="Limpeza final",
    )

    item.complete(
        completed_at=utc_now(),
    )

    assert item.is_completed is True
    assert item.completed_by_employee_id is None


def test_completed_checklist_item_can_be_reopened() -> None:
    item = ProductionChecklistItem.create(
        tenant_id=uuid.uuid4(),
        production_operation_id=uuid.uuid4(),
        sequence=1,
        title="Conferência",
    )

    item.complete(
        employee_id=uuid.uuid4(),
        completed_at=utc_now(),
    )

    item.reopen()

    assert item.completed_at is None
    assert item.completed_by_employee_id is None
    assert item.is_pending is True


def test_checklist_item_can_be_marked_not_applicable() -> None:
    item = ProductionChecklistItem.create(
        tenant_id=uuid.uuid4(),
        production_operation_id=uuid.uuid4(),
        sequence=1,
        title="Instalar puxadores",
    )

    item.mark_not_applicable(
        notes="Projeto sem puxadores."
    )

    assert item.is_applicable is False
    assert item.is_pending is False
    assert item.is_completed is False
    assert item.notes == "Projeto sem puxadores."


def test_non_applicable_item_can_restore_applicability() -> None:
    item = ProductionChecklistItem.create(
        tenant_id=uuid.uuid4(),
        production_operation_id=uuid.uuid4(),
        sequence=1,
        title="Instalar ferragem",
    )

    item.mark_not_applicable()
    item.restore_applicability()

    assert item.is_applicable is True
    assert item.is_pending is True


def test_non_applicable_item_cannot_be_completed() -> None:
    item = ProductionChecklistItem.create(
        tenant_id=uuid.uuid4(),
        production_operation_id=uuid.uuid4(),
        sequence=1,
        title="Teste",
    )

    item.mark_not_applicable()

    with pytest.raises(
        ValueError,
        match="não aplicável",
    ):
        item.complete(
            completed_at=utc_now()
        )


def test_completed_item_must_reopen_before_not_applicable() -> None:
    item = ProductionChecklistItem.create(
        tenant_id=uuid.uuid4(),
        production_operation_id=uuid.uuid4(),
        sequence=1,
        title="Teste",
    )

    item.complete(
        completed_at=utc_now()
    )

    with pytest.raises(
        ValueError,
        match="deve ser reaberto",
    ):
        item.mark_not_applicable()


@pytest.mark.parametrize(
    "sequence",
    [
        0,
        -1,
    ],
)
def test_checklist_rejects_non_positive_sequence(
    sequence: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        ProductionChecklistItem.create(
            tenant_id=uuid.uuid4(),
            production_operation_id=uuid.uuid4(),
            sequence=sequence,
            title="Teste",
        )


def test_checklist_rejects_boolean_sequence() -> None:
    with pytest.raises(
        TypeError,
        match="deve ser inteira",
    ):
        ProductionChecklistItem.create(
            tenant_id=uuid.uuid4(),
            production_operation_id=uuid.uuid4(),
            sequence=True,
            title="Teste",
        )


def test_checklist_rejects_blank_title() -> None:
    with pytest.raises(
        ValueError,
        match="obrigatório",
    ):
        ProductionChecklistItem.create(
            tenant_id=uuid.uuid4(),
            production_operation_id=uuid.uuid4(),
            sequence=1,
            title="   ",
        )
