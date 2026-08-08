"""Unit tests for machine domain behavior."""

from __future__ import annotations

import uuid

import pytest

from organizeg3_api.domain.machine.entity import (
    Machine,
)
from organizeg3_api.domain.machine.value_objects import (
    MachineStatus,
)


def test_creates_and_normalizes_machine() -> None:
    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()

    machine = Machine.create(
        tenant_id=tenant_id,
        branch_id=branch_id,
        code=" maq-001 ",
        name="  Seccionadora  ",
        machine_type="  Seccionadora  ",
        manufacturer="  Homag  ",
        model="  SAWTEQ  ",
        serial_number="  ABC-123  ",
    )

    assert machine.id is not None
    assert machine.tenant_id == tenant_id
    assert machine.branch_id == branch_id
    assert machine.code == "MAQ-001"
    assert machine.name == "Seccionadora"
    assert machine.machine_type == "Seccionadora"
    assert machine.manufacturer == "Homag"
    assert machine.model == "SAWTEQ"
    assert machine.serial_number == "ABC-123"
    assert machine.status is MachineStatus.AVAILABLE
    assert machine.is_active is True
    assert machine.created_at is not None
    assert machine.updated_at is not None


def test_allows_machine_without_branch() -> None:
    machine = Machine.create(
        tenant_id=uuid.uuid4(),
        code="MAQ-001",
        name="Coladeira",
        machine_type="Coladeira de borda",
    )

    assert machine.branch_id is None


def test_normalizes_blank_optional_text_to_none() -> None:
    machine = Machine.create(
        tenant_id=uuid.uuid4(),
        code="MAQ-001",
        name="Furadeira",
        machine_type="Furadeira",
        manufacturer="   ",
        model="",
        serial_number="   ",
    )

    assert machine.manufacturer is None
    assert machine.model is None
    assert machine.serial_number is None


@pytest.mark.parametrize(
    "code",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_machine_code(
    code: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="código",
    ):
        Machine.create(
            tenant_id=uuid.uuid4(),
            code=code,
            name="Máquina",
            machine_type="Tipo",
        )


@pytest.mark.parametrize(
    "name",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_machine_name(
    name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="nome",
    ):
        Machine.create(
            tenant_id=uuid.uuid4(),
            code="MAQ-001",
            name=name,
            machine_type="Tipo",
        )


@pytest.mark.parametrize(
    "machine_type",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_machine_type(
    machine_type: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="tipo",
    ):
        Machine.create(
            tenant_id=uuid.uuid4(),
            code="MAQ-001",
            name="Máquina",
            machine_type=machine_type,
        )


def test_rejects_null_tenant_uuid() -> None:
    with pytest.raises(
        ValueError,
        match="UUID nulo",
    ):
        Machine.create(
            tenant_id=uuid.UUID(int=0),
            code="MAQ-001",
            name="Máquina",
            machine_type="Tipo",
        )


def test_rejects_invalid_tenant_type() -> None:
    with pytest.raises(
        TypeError,
        match="tenant",
    ):
        Machine.create(  # type: ignore[arg-type]
            tenant_id="tenant",
            code="MAQ-001",
            name="Máquina",
            machine_type="Tipo",
        )


def test_rejects_null_branch_uuid() -> None:
    with pytest.raises(
        ValueError,
        match="UUID nulo",
    ):
        Machine.create(
            tenant_id=uuid.uuid4(),
            branch_id=uuid.UUID(int=0),
            code="MAQ-001",
            name="Máquina",
            machine_type="Tipo",
        )


def test_assigns_branch() -> None:
    machine = Machine.create(
        tenant_id=uuid.uuid4(),
        code="MAQ-001",
        name="Máquina",
        machine_type="Tipo",
    )

    branch_id = uuid.uuid4()

    machine.assign_branch(
        branch_id
    )

    assert machine.branch_id == branch_id


def test_removes_branch() -> None:
    branch_id = uuid.uuid4()

    machine = Machine.create(
        tenant_id=uuid.uuid4(),
        branch_id=branch_id,
        code="MAQ-001",
        name="Máquina",
        machine_type="Tipo",
    )

    machine.remove_branch()

    assert machine.branch_id is None


def test_marks_machine_in_use() -> None:
    machine = Machine.create(
        tenant_id=uuid.uuid4(),
        code="MAQ-001",
        name="Máquina",
        machine_type="Tipo",
    )

    machine.mark_in_use()

    assert machine.status is MachineStatus.IN_USE


def test_sends_machine_to_maintenance() -> None:
    machine = Machine.create(
        tenant_id=uuid.uuid4(),
        code="MAQ-001",
        name="Máquina",
        machine_type="Tipo",
    )

    machine.send_to_maintenance()

    assert machine.status is MachineStatus.MAINTENANCE


def test_marks_machine_out_of_service() -> None:
    machine = Machine.create(
        tenant_id=uuid.uuid4(),
        code="MAQ-001",
        name="Máquina",
        machine_type="Tipo",
    )

    machine.mark_out_of_service()

    assert machine.status is MachineStatus.OUT_OF_SERVICE


def test_returns_machine_to_available() -> None:
    machine = Machine.create(
        tenant_id=uuid.uuid4(),
        code="MAQ-001",
        name="Máquina",
        machine_type="Tipo",
    )

    machine.send_to_maintenance()
    machine.mark_available()

    assert machine.status is MachineStatus.AVAILABLE


def test_rejects_invalid_machine_status() -> None:
    with pytest.raises(
        TypeError,
        match="status",
    ):
        Machine(  # type: ignore[arg-type]
            tenant_id=uuid.uuid4(),
            code="MAQ-001",
            name="Máquina",
            machine_type="Tipo",
            status="AVAILABLE",
        )


def test_deactivates_machine() -> None:
    machine = Machine.create(
        tenant_id=uuid.uuid4(),
        code="MAQ-001",
        name="Máquina",
        machine_type="Tipo",
    )

    machine.deactivate()

    assert machine.is_active is False


def test_reactivates_machine() -> None:
    machine = Machine.create(
        tenant_id=uuid.uuid4(),
        code="MAQ-001",
        name="Máquina",
        machine_type="Tipo",
    )

    machine.deactivate()
    machine.activate()

    assert machine.is_active is True
