"""Unit tests for employee application use cases."""

from __future__ import annotations

from datetime import date
import uuid

import pytest

from organizeg3_api.application.employee import (
    CreateEmployeeUseCase,
    DeactivateEmployeeUseCase,
    EmployeeCreate,
    EmployeeUpdate,
    GetEmployeeUseCase,
    ListEmployeesUseCase,
    ReactivateEmployeeUseCase,
    UpdateEmployeeUseCase,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.employee import (
    Employee,
    EmployeeRepository,
    EmploymentStatus,
)


class InMemoryEmployeeRepository(
    EmployeeRepository
):
    """Small deterministic repository used by application tests."""

    def __init__(self) -> None:
        self.employees: dict[
            uuid.UUID,
            Employee,
        ] = {}

        self.branch_ids: set[
            tuple[
                uuid.UUID,
                uuid.UUID,
            ]
        ] = set()

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        employee_id: uuid.UUID,
    ) -> Employee | None:
        employee = self.employees.get(
            employee_id
        )

        if employee is None:
            return None

        if employee.tenant_id != tenant_id:
            return None

        return employee

    def get_by_document_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        document_number: str,
    ) -> Employee | None:
        normalized_document = "".join(
            character
            for character in document_number
            if character.isdigit()
        )

        for employee in self.employees.values():
            if (
                employee.tenant_id == tenant_id
                and employee.document_number
                == normalized_document
            ):
                return employee

        return None

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        branch_id: uuid.UUID | None = None,
        status: EmploymentStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Employee]:
        employees = [
            employee
            for employee in self.employees.values()
            if employee.tenant_id == tenant_id
        ]

        if not include_inactive:
            employees = [
                employee
                for employee in employees
                if employee.is_active
            ]

        if branch_id is not None:
            employees = [
                employee
                for employee in employees
                if employee.branch_id
                == branch_id
            ]

        if status is not None:
            employees = [
                employee
                for employee in employees
                if employee.status == status
            ]

        if search is not None:
            normalized_search = (
                search.strip().lower()
            )

            if normalized_search:
                employees = [
                    employee
                    for employee in employees
                    if (
                        normalized_search
                        in employee.code.lower()
                        or normalized_search
                        in employee.full_name.lower()
                        or (
                            employee.email is not None
                            and normalized_search
                            in employee.email.lower()
                        )
                        or (
                            employee.document_number
                            is not None
                            and normalized_search
                            in employee.document_number
                        )
                    )
                ]

        employees.sort(
            key=lambda employee: (
                employee.full_name,
                employee.code,
            )
        )

        return employees[
            offset : offset + limit
        ]

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_employee_id: uuid.UUID | None = None,
    ) -> bool:
        normalized_code = (
            code.strip().upper()
        )

        return any(
            employee.tenant_id == tenant_id
            and employee.code == normalized_code
            and employee.id
            != exclude_employee_id
            for employee in self.employees.values()
        )

    def exists_by_document(
        self,
        *,
        tenant_id: uuid.UUID,
        document_number: str,
        exclude_employee_id: uuid.UUID | None = None,
    ) -> bool:
        normalized_document = "".join(
            character
            for character in document_number
            if character.isdigit()
        )

        return any(
            employee.tenant_id == tenant_id
            and employee.document_number
            == normalized_document
            and employee.id
            != exclude_employee_id
            for employee in self.employees.values()
        )

    def branch_exists_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID,
    ) -> bool:
        return (
            tenant_id,
            branch_id,
        ) in self.branch_ids

    def add(
        self,
        employee: Employee,
    ) -> Employee:
        if employee.id is None:
            raise ValueError(
                "Funcionário deve possuir identificador."
            )

        self.employees[
            employee.id
        ] = employee

        return employee

    def save(
        self,
        employee: Employee,
    ) -> Employee:
        if employee.id is None:
            raise ValueError(
                "Funcionário deve possuir identificador."
            )

        self.employees[
            employee.id
        ] = employee

        return employee

    def register_branch(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID,
    ) -> None:
        """Register one branch available to a tenant."""

        self.branch_ids.add(
            (
                tenant_id,
                branch_id,
            )
        )


def create_existing_employee(
    repository: InMemoryEmployeeRepository,
    *,
    tenant_id: uuid.UUID,
    code: str = "FUNC-001",
    full_name: str = "Funcionário Teste",
    branch_id: uuid.UUID | None = None,
    document_number: str | None = None,
    email: str | None = None,
) -> Employee:
    """Create and persist an employee used by tests."""

    employee = Employee.create(
        tenant_id=tenant_id,
        code=code,
        full_name=full_name,
        branch_id=branch_id,
        document_number=document_number,
        email=email,
    )

    repository.add(
        employee
    )

    return employee


def employee_id_of(
    employee: Employee,
) -> uuid.UUID:
    """Return the identifier of a persisted test employee."""

    if employee.id is None:
        raise AssertionError(
            "Funcionário de teste deveria possuir ID."
        )

    return employee.id


def test_creates_employee() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    result = CreateEmployeeUseCase(
        repository
    ).execute(
        tenant_id,
        EmployeeCreate(
            code=" func-001 ",
            full_name=" Funcionário Teste ",
            document_number="529.982.247-25",
            email="FUNCIONARIO@EXAMPLE.COM",
            phone="(18) 99999-1234",
            job_title=" Marceneiro ",
            contract_type=" CLT ",
        ),
    )

    assert result.tenant_id == tenant_id
    assert result.code == "FUNC-001"
    assert (
        result.full_name
        == "Funcionário Teste"
    )
    assert (
        result.document_number
        == "52998224725"
    )
    assert (
        result.email
        == "funcionario@example.com"
    )
    assert result.phone == "18999991234"
    assert result.job_title == "Marceneiro"
    assert result.contract_type == "CLT"
    assert (
        result.status
        == EmploymentStatus.ACTIVE
    )
    assert result.is_active is True


def test_creates_employee_with_valid_branch() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()

    repository.register_branch(
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    employee = CreateEmployeeUseCase(
        repository
    ).execute(
        tenant_id,
        EmployeeCreate(
            code="FUNC-001",
            full_name="Funcionário",
            branch_id=branch_id,
        ),
    )

    assert employee.branch_id == branch_id


def test_rejects_employee_branch_from_other_tenant() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()

    repository.register_branch(
        tenant_id=other_tenant_id,
        branch_id=branch_id,
    )

    with pytest.raises(
        ValidationError,
        match="filial",
    ):
        CreateEmployeeUseCase(
            repository
        ).execute(
            tenant_id,
            EmployeeCreate(
                code="FUNC-001",
                full_name="Funcionário",
                branch_id=branch_id,
            ),
        )


def test_rejects_duplicate_employee_code() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    create_existing_employee(
        repository,
        tenant_id=tenant_id,
        code="FUNC-001",
    )

    with pytest.raises(
        ConflictError,
        match="código",
    ):
        CreateEmployeeUseCase(
            repository
        ).execute(
            tenant_id,
            EmployeeCreate(
                code=" func-001 ",
                full_name="Outro Funcionário",
            ),
        )


def test_allows_same_code_in_different_tenants() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    first_tenant_id = uuid.uuid4()
    second_tenant_id = uuid.uuid4()

    create_existing_employee(
        repository,
        tenant_id=first_tenant_id,
        code="FUNC-001",
    )

    result = CreateEmployeeUseCase(
        repository
    ).execute(
        second_tenant_id,
        EmployeeCreate(
            code="FUNC-001",
            full_name="Outro Funcionário",
        ),
    )

    assert (
        result.tenant_id
        == second_tenant_id
    )


def test_rejects_duplicate_employee_document() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    create_existing_employee(
        repository,
        tenant_id=tenant_id,
        document_number="529.982.247-25",
    )

    with pytest.raises(
        ConflictError,
        match="CPF",
    ):
        CreateEmployeeUseCase(
            repository
        ).execute(
            tenant_id,
            EmployeeCreate(
                code="FUNC-002",
                full_name="Outro Funcionário",
                document_number="52998224725",
            ),
        )


def test_rejects_invalid_create_payload_at_domain_boundary() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    with pytest.raises(
        ValidationError,
        match="CPF",
    ):
        CreateEmployeeUseCase(
            repository
        ).execute(
            uuid.uuid4(),
            EmployeeCreate(
                code="FUNC-001",
                full_name="Funcionário",
                document_number="123",
            ),
        )


def test_gets_employee_for_tenant() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    employee = create_existing_employee(
        repository,
        tenant_id=tenant_id,
    )

    result = GetEmployeeUseCase(
        repository
    ).execute(
        tenant_id,
        employee_id_of(
            employee
        ),
    )

    assert result is employee


def test_get_does_not_cross_tenant_boundary() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    employee = create_existing_employee(
        repository,
        tenant_id=uuid.uuid4(),
    )

    with pytest.raises(
        NotFoundError,
        match="não encontrado",
    ):
        GetEmployeeUseCase(
            repository
        ).execute(
            uuid.uuid4(),
            employee_id_of(
                employee
            ),
        )


def test_lists_only_tenant_employees() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    create_existing_employee(
        repository,
        tenant_id=tenant_id,
        code="FUNC-001",
        full_name="Ana",
    )

    create_existing_employee(
        repository,
        tenant_id=tenant_id,
        code="FUNC-002",
        full_name="Bruno",
    )

    create_existing_employee(
        repository,
        tenant_id=uuid.uuid4(),
        code="FUNC-003",
        full_name="Carlos",
    )

    results = ListEmployeesUseCase(
        repository
    ).execute(
        tenant_id
    )

    assert [
        employee.full_name
        for employee in results
    ] == [
        "Ana",
        "Bruno",
    ]


def test_list_hides_inactive_by_default() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    active = create_existing_employee(
        repository,
        tenant_id=tenant_id,
        code="FUNC-A",
        full_name="Ativo",
    )

    inactive = create_existing_employee(
        repository,
        tenant_id=tenant_id,
        code="FUNC-I",
        full_name="Inativo",
    )

    inactive.deactivate()

    results = ListEmployeesUseCase(
        repository
    ).execute(
        tenant_id
    )

    assert active in results
    assert inactive not in results


def test_list_can_include_inactive() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    inactive = create_existing_employee(
        repository,
        tenant_id=tenant_id,
    )

    inactive.deactivate()

    results = ListEmployeesUseCase(
        repository
    ).execute(
        tenant_id,
        include_inactive=True,
    )

    assert inactive in results


def test_list_filters_by_branch_and_status() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()
    other_branch_id = uuid.uuid4()

    first = create_existing_employee(
        repository,
        tenant_id=tenant_id,
        code="FUNC-A",
        full_name="Ana",
        branch_id=branch_id,
    )

    first.put_on_leave()

    create_existing_employee(
        repository,
        tenant_id=tenant_id,
        code="FUNC-B",
        full_name="Bruno",
        branch_id=other_branch_id,
    )

    results = ListEmployeesUseCase(
        repository
    ).execute(
        tenant_id,
        branch_id=branch_id,
        status=EmploymentStatus.ON_LEAVE,
    )

    assert results == [
        first
    ]


def test_list_searches_employee() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    expected = create_existing_employee(
        repository,
        tenant_id=tenant_id,
        code="MARC-001",
        full_name="João da Silva",
        email="joao@example.com",
    )

    create_existing_employee(
        repository,
        tenant_id=tenant_id,
        code="ADM-001",
        full_name="Maria Souza",
    )

    results = ListEmployeesUseCase(
        repository
    ).execute(
        tenant_id,
        search="JOÃO",
    )

    assert results == [
        expected
    ]


def test_list_applies_pagination() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    for index, name in enumerate(
        [
            "Ana",
            "Bruno",
            "Carlos",
        ],
        start=1,
    ):
        create_existing_employee(
            repository,
            tenant_id=tenant_id,
            code=f"FUNC-{index}",
            full_name=name,
        )

    results = ListEmployeesUseCase(
        repository
    ).execute(
        tenant_id,
        limit=1,
        offset=1,
    )

    assert len(results) == 1
    assert (
        results[0].full_name
        == "Bruno"
    )


def test_updates_employee_details() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    employee = create_existing_employee(
        repository,
        tenant_id=tenant_id,
        code="FUNC-001",
        full_name="Nome Antigo",
    )

    old_updated_at = employee.updated_at

    result = UpdateEmployeeUseCase(
        repository
    ).execute(
        tenant_id,
        employee_id_of(
            employee
        ),
        EmployeeUpdate(
            code=" func-002 ",
            full_name=" Nome Novo ",
            email="NOVO@EXAMPLE.COM",
            job_title=" Marceneiro ",
        ),
    )

    assert result.code == "FUNC-002"
    assert result.full_name == "Nome Novo"
    assert result.email == "novo@example.com"
    assert result.job_title == "Marceneiro"
    assert result.updated_at is not None

    if old_updated_at is not None:
        assert (
            result.updated_at
            > old_updated_at
        )


def test_update_allows_clearing_optional_fields() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    employee = create_existing_employee(
        repository,
        tenant_id=tenant_id,
        email="funcionario@example.com",
    )

    employee.phone = "18999991234"
    employee.job_title = "Marceneiro"

    result = UpdateEmployeeUseCase(
        repository
    ).execute(
        tenant_id,
        employee_id_of(
            employee
        ),
        EmployeeUpdate(
            email=None,
            phone=None,
            job_title=None,
        ),
    )

    assert result.email is None
    assert result.phone is None
    assert result.job_title is None


def test_update_can_assign_valid_branch() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()

    repository.register_branch(
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    employee = create_existing_employee(
        repository,
        tenant_id=tenant_id,
    )

    result = UpdateEmployeeUseCase(
        repository
    ).execute(
        tenant_id,
        employee_id_of(
            employee
        ),
        EmployeeUpdate(
            branch_id=branch_id
        ),
    )

    assert result.branch_id == branch_id


def test_update_rejects_foreign_branch() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()
    foreign_tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()

    repository.register_branch(
        tenant_id=foreign_tenant_id,
        branch_id=branch_id,
    )

    employee = create_existing_employee(
        repository,
        tenant_id=tenant_id,
    )

    with pytest.raises(
        ValidationError,
        match="filial",
    ):
        UpdateEmployeeUseCase(
            repository
        ).execute(
            tenant_id,
            employee_id_of(
                employee
            ),
            EmployeeUpdate(
                branch_id=branch_id
            ),
        )


def test_update_rejects_empty_payload() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    employee = create_existing_employee(
        repository,
        tenant_id=tenant_id,
    )

    with pytest.raises(
        ValidationError,
        match="ao menos um campo",
    ):
        UpdateEmployeeUseCase(
            repository
        ).execute(
            tenant_id,
            employee_id_of(
                employee
            ),
            EmployeeUpdate(),
        )


def test_update_rejects_null_required_code() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    employee = create_existing_employee(
        repository,
        tenant_id=tenant_id,
    )

    with pytest.raises(
        ValidationError,
        match="código",
    ):
        UpdateEmployeeUseCase(
            repository
        ).execute(
            tenant_id,
            employee_id_of(
                employee
            ),
            EmployeeUpdate(
                code=None
            ),
        )


def test_update_rejects_null_required_name() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    employee = create_existing_employee(
        repository,
        tenant_id=tenant_id,
    )

    with pytest.raises(
        ValidationError,
        match="nome",
    ):
        UpdateEmployeeUseCase(
            repository
        ).execute(
            tenant_id,
            employee_id_of(
                employee
            ),
            EmployeeUpdate(
                full_name=None
            ),
        )


def test_update_rejects_duplicate_code() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    first = create_existing_employee(
        repository,
        tenant_id=tenant_id,
        code="FUNC-001",
    )

    create_existing_employee(
        repository,
        tenant_id=tenant_id,
        code="FUNC-002",
        full_name="Segundo",
    )

    with pytest.raises(
        ConflictError,
        match="código",
    ):
        UpdateEmployeeUseCase(
            repository
        ).execute(
            tenant_id,
            employee_id_of(
                first
            ),
            EmployeeUpdate(
                code="FUNC-002"
            ),
        )


def test_update_rejects_duplicate_document() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    first = create_existing_employee(
        repository,
        tenant_id=tenant_id,
        code="FUNC-001",
    )

    create_existing_employee(
        repository,
        tenant_id=tenant_id,
        code="FUNC-002",
        full_name="Segundo",
        document_number="529.982.247-25",
    )

    with pytest.raises(
        ConflictError,
        match="CPF",
    ):
        UpdateEmployeeUseCase(
            repository
        ).execute(
            tenant_id,
            employee_id_of(
                first
            ),
            EmployeeUpdate(
                document_number="52998224725"
            ),
        )


def test_update_rejects_cross_tenant_employee() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    employee = create_existing_employee(
        repository,
        tenant_id=uuid.uuid4(),
    )

    with pytest.raises(
        NotFoundError,
    ):
        UpdateEmployeeUseCase(
            repository
        ).execute(
            uuid.uuid4(),
            employee_id_of(
                employee
            ),
            EmployeeUpdate(
                full_name="Novo Nome"
            ),
        )


def test_deactivates_employee() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    employee = create_existing_employee(
        repository,
        tenant_id=tenant_id,
    )

    result = DeactivateEmployeeUseCase(
        repository
    ).execute(
        tenant_id,
        employee_id_of(
            employee
        ),
    )

    assert (
        result.status
        == EmploymentStatus.INACTIVE
    )
    assert result.is_active is False


def test_deactivation_is_idempotent() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    employee = create_existing_employee(
        repository,
        tenant_id=tenant_id,
    )

    use_case = DeactivateEmployeeUseCase(
        repository
    )

    first = use_case.execute(
        tenant_id,
        employee_id_of(
            employee
        ),
    )

    first_updated_at = first.updated_at

    second = use_case.execute(
        tenant_id,
        employee_id_of(
            employee
        ),
    )

    assert second.is_active is False
    assert (
        second.status
        == EmploymentStatus.INACTIVE
    )
    assert (
        second.updated_at
        == first_updated_at
    )


def test_reactivates_inactive_employee() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    employee = create_existing_employee(
        repository,
        tenant_id=tenant_id,
    )

    employee.deactivate()

    deactivated_at = employee.updated_at

    result = ReactivateEmployeeUseCase(
        repository
    ).execute(
        tenant_id,
        employee_id_of(
            employee
        ),
    )

    assert (
        result.status
        == EmploymentStatus.ACTIVE
    )
    assert result.is_active is True
    assert result.updated_at is not None

    if deactivated_at is not None:
        assert (
            result.updated_at
            > deactivated_at
        )


def test_reactivation_is_idempotent_when_active() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    employee = create_existing_employee(
        repository,
        tenant_id=tenant_id,
    )

    original_updated_at = (
        employee.updated_at
    )

    result = ReactivateEmployeeUseCase(
        repository
    ).execute(
        tenant_id,
        employee_id_of(
            employee
        ),
    )

    assert result.is_active is True
    assert (
        result.updated_at
        == original_updated_at
    )


def test_rejects_reactivation_after_termination() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()

    employee = create_existing_employee(
        repository,
        tenant_id=tenant_id,
    )

    employee.terminate(
        termination_date=date(
            2026,
            8,
            8,
        )
    )

    with pytest.raises(
        ValidationError,
        match="novo vínculo",
    ):
        ReactivateEmployeeUseCase(
            repository
        ).execute(
            tenant_id,
            employee_id_of(
                employee
            ),
        )


def test_lifecycle_actions_reject_unknown_employee() -> None:
    repository = (
        InMemoryEmployeeRepository()
    )

    tenant_id = uuid.uuid4()
    employee_id = uuid.uuid4()

    with pytest.raises(
        NotFoundError,
    ):
        DeactivateEmployeeUseCase(
            repository
        ).execute(
            tenant_id,
            employee_id,
        )

    with pytest.raises(
        NotFoundError,
    ):
        ReactivateEmployeeUseCase(
            repository
        ).execute(
            tenant_id,
            employee_id,
        )
