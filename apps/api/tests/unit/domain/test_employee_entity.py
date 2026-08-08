"""Unit tests for employee domain behavior."""

from __future__ import annotations

from datetime import UTC, date, datetime
import uuid

import pytest

from organizeg3_api.domain.employee.entity import (
    Employee,
)
from organizeg3_api.domain.employee.value_objects import (
    EmploymentStatus,
)


def test_creates_and_normalizes_employee() -> None:
    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()

    employee = Employee.create(
        tenant_id=tenant_id,
        branch_id=branch_id,
        code=" func-001 ",
        full_name="  Funcionário Teste  ",
        document_number="529.982.247-25",
        email=" FUNCIONARIO@EXAMPLE.COM ",
        phone="(18) 99999-1234",
        job_title=" Marceneiro ",
        contract_type=" CLT ",
        birth_date=date(
            1990,
            1,
            1,
        ),
        admission_date=date(
            2025,
            1,
            10,
        ),
    )

    assert employee.id is not None

    assert employee.tenant_id == tenant_id
    assert employee.branch_id == branch_id

    assert employee.code == "FUNC-001"

    assert (
        employee.full_name
        == "Funcionário Teste"
    )

    assert (
        employee.document_number
        == "52998224725"
    )

    assert (
        employee.email
        == "funcionario@example.com"
    )

    assert employee.phone == "18999991234"

    assert employee.job_title == "Marceneiro"
    assert employee.contract_type == "CLT"

    assert (
        employee.status
        == EmploymentStatus.ACTIVE
    )

    assert employee.is_active is True

    assert employee.created_at is not None
    assert employee.updated_at is not None


def test_allows_employee_without_branch() -> None:
    employee = Employee.create(
        tenant_id=uuid.uuid4(),
        code="FUNC-001",
        full_name="Funcionário",
    )

    assert employee.branch_id is None


@pytest.mark.parametrize(
    "code",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_code(
    code: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="código",
    ):
        Employee.create(
            tenant_id=uuid.uuid4(),
            code=code,
            full_name="Funcionário",
        )


@pytest.mark.parametrize(
    "full_name",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_name(
    full_name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="nome",
    ):
        Employee.create(
            tenant_id=uuid.uuid4(),
            code="FUNC",
            full_name=full_name,
        )


def test_rejects_null_tenant_uuid() -> None:
    with pytest.raises(
        ValueError,
        match="UUID nulo",
    ):
        Employee.create(
            tenant_id=uuid.UUID(int=0),
            code="FUNC",
            full_name="Funcionário",
        )


def test_rejects_invalid_tenant_type() -> None:
    with pytest.raises(
        TypeError,
        match="tenant",
    ):
        Employee.create(  # type: ignore[arg-type]
            tenant_id="tenant",
            code="FUNC",
            full_name="Funcionário",
        )


def test_rejects_null_branch_uuid() -> None:
    with pytest.raises(
        ValueError,
        match="UUID nulo",
    ):
        Employee.create(
            tenant_id=uuid.uuid4(),
            branch_id=uuid.UUID(int=0),
            code="FUNC",
            full_name="Funcionário",
        )


@pytest.mark.parametrize(
    "document_number",
    [
        "123",
        "111.111.111-11",
        "529.982.247-24",
    ],
)
def test_rejects_invalid_cpf(
    document_number: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="CPF",
    ):
        Employee.create(
            tenant_id=uuid.uuid4(),
            code="FUNC",
            full_name="Funcionário",
            document_number=document_number,
        )


def test_rejects_invalid_email() -> None:
    with pytest.raises(
        ValueError,
        match="e-mail",
    ):
        Employee.create(
            tenant_id=uuid.uuid4(),
            code="FUNC",
            full_name="Funcionário",
            email="email-invalido",
        )


def test_rejects_invalid_phone() -> None:
    with pytest.raises(
        ValueError,
        match="telefone",
    ):
        Employee.create(
            tenant_id=uuid.uuid4(),
            code="FUNC",
            full_name="Funcionário",
            phone="123",
        )


def test_assigns_branch() -> None:
    employee = Employee.create(
        tenant_id=uuid.uuid4(),
        code="FUNC",
        full_name="Funcionário",
    )

    branch_id = uuid.uuid4()

    employee.assign_branch(
        branch_id
    )

    assert employee.branch_id == branch_id


def test_removes_branch_assignment() -> None:
    employee = Employee.create(
        tenant_id=uuid.uuid4(),
        branch_id=uuid.uuid4(),
        code="FUNC",
        full_name="Funcionário",
    )

    employee.assign_branch(
        None
    )

    assert employee.branch_id is None


def test_puts_employee_on_leave() -> None:
    employee = Employee.create(
        tenant_id=uuid.uuid4(),
        code="FUNC",
        full_name="Funcionário",
    )

    employee.put_on_leave()

    assert (
        employee.status
        == EmploymentStatus.ON_LEAVE
    )

    assert employee.is_active is True


def test_deactivates_employee() -> None:
    employee = Employee.create(
        tenant_id=uuid.uuid4(),
        code="FUNC",
        full_name="Funcionário",
    )

    employee.deactivate()

    assert (
        employee.status
        == EmploymentStatus.INACTIVE
    )

    assert employee.is_active is False


def test_reactivates_inactive_employee() -> None:
    employee = Employee.create(
        tenant_id=uuid.uuid4(),
        code="FUNC",
        full_name="Funcionário",
    )

    employee.deactivate()
    employee.reactivate()

    assert (
        employee.status
        == EmploymentStatus.ACTIVE
    )

    assert employee.is_active is True


def test_terminates_employee() -> None:
    employee = Employee.create(
        tenant_id=uuid.uuid4(),
        code="FUNC",
        full_name="Funcionário",
        admission_date=date(
            2025,
            1,
            1,
        ),
    )

    employee.terminate(
        termination_date=date(
            2026,
            1,
            1,
        )
    )

    assert (
        employee.status
        == EmploymentStatus.TERMINATED
    )

    assert (
        employee.termination_date
        == date(
            2026,
            1,
            1,
        )
    )

    assert employee.is_active is False


def test_rejects_termination_before_admission() -> None:
    employee = Employee.create(
        tenant_id=uuid.uuid4(),
        code="FUNC",
        full_name="Funcionário",
        admission_date=date(
            2025,
            1,
            10,
        ),
    )

    with pytest.raises(
        ValueError,
        match="anterior à admissão",
    ):
        employee.terminate(
            termination_date=date(
                2025,
                1,
                9,
            )
        )


def test_rejects_birth_date_after_admission() -> None:
    with pytest.raises(
        ValueError,
        match="nascimento",
    ):
        Employee.create(
            tenant_id=uuid.uuid4(),
            code="FUNC",
            full_name="Funcionário",
            birth_date=date(
                2025,
                1,
                10,
            ),
            admission_date=date(
                2025,
                1,
                1,
            ),
        )


def test_rejects_reactivation_after_termination() -> None:
    employee = Employee.create(
        tenant_id=uuid.uuid4(),
        code="FUNC",
        full_name="Funcionário",
    )

    employee.terminate(
        termination_date=datetime.now(
            UTC
        ).date()
    )

    with pytest.raises(
        ValueError,
        match="novo vínculo",
    ):
        employee.reactivate()
