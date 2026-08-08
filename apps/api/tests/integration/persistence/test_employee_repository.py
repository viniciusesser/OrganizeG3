"""Integration tests for employee persistence."""

from __future__ import annotations

from datetime import date
import uuid

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from organizeg3_api.domain.employee.entity import (
    Employee,
)
from organizeg3_api.infrastructure.persistence.models import (
    BranchModel,
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories import (
    SQLAlchemyEmployeeRepository,
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
    """Create one active tenant."""

    tenant = TenantRecordModel(
        id=tenant_id,
        name=name,
        status="ACTIVE",
        is_active=True,
    )

    session.add(
        tenant
    )
    session.flush()

    return tenant


def create_branch(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    branch_id: uuid.UUID,
    code: str,
) -> BranchModel:
    """Create one active branch."""

    branch = BranchModel(
        id=branch_id,
        tenant_id=tenant_id,
        code=code,
        name=f"Filial {code}",
        is_active=True,
    )

    session.add(
        branch
    )
    session.flush()

    return branch


def test_adds_and_recovers_complete_employee(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Employee",
    )

    create_branch(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
        code="MATRIZ",
    )

    employee = Employee.create(
        tenant_id=tenant_id,
        branch_id=branch_id,
        code="FUNC-001",
        full_name="Funcionário Teste",
        document_number="529.982.247-25",
        email="funcionario@example.com",
        phone="(18) 99999-1234",
        job_title="Marceneiro",
        contract_type="CLT",
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

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    saved = repository.add(
        employee
    )

    assert saved.id is not None

    recovered = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        employee_id=saved.id,
    )

    assert recovered is not None

    assert recovered.id == employee.id
    assert recovered.tenant_id == tenant_id
    assert recovered.branch_id == branch_id
    assert recovered.code == "FUNC-001"

    assert (
        recovered.full_name
        == "Funcionário Teste"
    )

    assert (
        recovered.document_number
        == "52998224725"
    )

    assert (
        recovered.email
        == "funcionario@example.com"
    )

    assert recovered.phone == "18999991234"
    assert recovered.job_title == "Marceneiro"
    assert recovered.contract_type == "CLT"

    assert (
        recovered.birth_date
        == date(
            1990,
            1,
            1,
        )
    )

    assert (
        recovered.admission_date
        == date(
            2025,
            1,
            10,
        )
    )

    assert recovered.is_active is True


def test_allows_employee_without_branch(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    saved = repository.add(
        Employee.create(
            tenant_id=tenant_id,
            code="FUNC-001",
            full_name="Funcionário",
        )
    )

    assert saved.branch_id is None


def test_employee_lookup_is_tenant_scoped(
    session: Session,
) -> None:
    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_a_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=tenant_b_id,
        name="Tenant B",
    )

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    saved = repository.add(
        Employee.create(
            tenant_id=tenant_a_id,
            code="FUNC-A",
            full_name="Funcionário A",
        )
    )

    assert saved.id is not None

    result = repository.get_by_id_for_tenant(
        tenant_id=tenant_b_id,
        employee_id=saved.id,
    )

    assert result is None


def test_finds_employee_by_normalized_document(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    repository.add(
        Employee.create(
            tenant_id=tenant_id,
            code="FUNC-001",
            full_name="Funcionário",
            document_number="529.982.247-25",
        )
    )

    recovered = (
        repository.get_by_document_for_tenant(
            tenant_id=tenant_id,
            document_number="529.982.247-25",
        )
    )

    assert recovered is not None

    assert (
        recovered.document_number
        == "52998224725"
    )


def test_document_lookup_is_tenant_scoped(
    session: Session,
) -> None:
    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_a_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=tenant_b_id,
        name="Tenant B",
    )

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    repository.add(
        Employee.create(
            tenant_id=tenant_a_id,
            code="FUNC-A",
            full_name="Funcionário A",
            document_number="529.982.247-25",
        )
    )

    result = (
        repository.get_by_document_for_tenant(
            tenant_id=tenant_b_id,
            document_number="529.982.247-25",
        )
    )

    assert result is None


def test_allows_same_code_in_different_tenants(
    session: Session,
) -> None:
    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_a_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=tenant_b_id,
        name="Tenant B",
    )

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    repository.add(
        Employee.create(
            tenant_id=tenant_a_id,
            code="FUNC-001",
            full_name="Funcionário A",
        )
    )

    repository.add(
        Employee.create(
            tenant_id=tenant_b_id,
            code="FUNC-001",
            full_name="Funcionário B",
        )
    )


def test_rejects_duplicate_code_in_same_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    repository.add(
        Employee.create(
            tenant_id=tenant_id,
            code="FUNC-001",
            full_name="Funcionário A",
        )
    )

    with pytest.raises(
        IntegrityError
    ):
        repository.add(
            Employee.create(
                tenant_id=tenant_id,
                code="func-001",
                full_name="Funcionário B",
            )
        )


def test_rejects_duplicate_document_in_same_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant",
    )

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    repository.add(
        Employee.create(
            tenant_id=tenant_id,
            code="FUNC-001",
            full_name="Funcionário A",
            document_number="529.982.247-25",
        )
    )

    with pytest.raises(
        IntegrityError
    ):
        repository.add(
            Employee.create(
                tenant_id=tenant_id,
                code="FUNC-002",
                full_name="Funcionário B",
                document_number="52998224725",
            )
        )


def test_allows_same_document_in_different_tenants(
    session: Session,
) -> None:
    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_a_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=tenant_b_id,
        name="Tenant B",
    )

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    repository.add(
        Employee.create(
            tenant_id=tenant_a_id,
            code="FUNC-A",
            full_name="Funcionário A",
            document_number="529.982.247-25",
        )
    )

    repository.add(
        Employee.create(
            tenant_id=tenant_b_id,
            code="FUNC-B",
            full_name="Funcionário B",
            document_number="529.982.247-25",
        )
    )


def test_rejects_branch_from_another_tenant(
    session: Session,
) -> None:
    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    branch_b_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_a_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=tenant_b_id,
        name="Tenant B",
    )

    create_branch(
        session,
        tenant_id=tenant_b_id,
        branch_id=branch_b_id,
        code="FILIAL-B",
    )

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="não pertence",
    ):
        repository.add(
            Employee.create(
                tenant_id=tenant_a_id,
                branch_id=branch_b_id,
                code="FUNC-A",
                full_name="Funcionário A",
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

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="não pertence",
    ):
        repository.add(
            Employee.create(
                tenant_id=tenant_id,
                branch_id=uuid.uuid4(),
                code="FUNC-001",
                full_name="Funcionário",
            )
        )
