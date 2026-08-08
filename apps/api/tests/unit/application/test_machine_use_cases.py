"""Unit tests for machine application use cases."""

from __future__ import annotations

import uuid

from pydantic import ValidationError as PydanticValidationError
import pytest

from organizeg3_api.application.machine.schemas import (
    MachineCreate,
    MachineStatusUpdate,
    MachineUpdate,
)
from organizeg3_api.application.machine.use_cases import (
    ChangeMachineStatusUseCase,
    CreateMachineUseCase,
    DeactivateMachineUseCase,
    GetMachineUseCase,
    ListMachinesUseCase,
    ReactivateMachineUseCase,
    UpdateMachineUseCase,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.machine.entity import (
    Machine,
)
from organizeg3_api.domain.machine.value_objects import (
    MachineStatus,
)


class FakeMachineRepository:
    """In-memory repository used by machine application tests."""

    def __init__(self) -> None:
        self.items: list[Machine] = []

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        machine_id: uuid.UUID,
    ) -> Machine | None:
        for machine in self.items:
            if (
                machine.tenant_id == tenant_id
                and machine.id == machine_id
            ):
                return machine

        return None

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> Machine | None:
        normalized = code.strip().upper()

        for machine in self.items:
            if (
                machine.tenant_id == tenant_id
                and machine.code == normalized
            ):
                return machine

        return None

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        machine_type: str | None = None,
        status: MachineStatus | None = None,
        branch_id: uuid.UUID | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Machine]:
        machines = [
            machine
            for machine in self.items
            if machine.tenant_id == tenant_id
        ]

        if not include_inactive:
            machines = [
                machine
                for machine in machines
                if machine.is_active
            ]

        if search is not None:
            needle = search.casefold()

            machines = [
                machine
                for machine in machines
                if any(
                    needle in value.casefold()
                    for value in (
                        machine.code,
                        machine.name,
                        machine.machine_type,
                        machine.manufacturer or "",
                        machine.model or "",
                        machine.serial_number or "",
                    )
                )
            ]

        if machine_type is not None:
            machines = [
                machine
                for machine in machines
                if machine.machine_type == machine_type
            ]

        if status is not None:
            machines = [
                machine
                for machine in machines
                if machine.status is status
            ]

        if branch_id is not None:
            machines = [
                machine
                for machine in machines
                if machine.branch_id == branch_id
            ]

        machines.sort(
            key=lambda machine: (
                machine.name,
                machine.code,
                str(machine.id),
            )
        )

        return machines[
            offset : offset + limit
        ]

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_machine_id: uuid.UUID | None = None,
    ) -> bool:
        normalized = code.strip().upper()

        return any(
            machine.tenant_id == tenant_id
            and machine.code == normalized
            and machine.id != exclude_machine_id
            for machine in self.items
        )

    def add(
        self,
        machine: Machine,
    ) -> Machine:
        self.items.append(
            machine
        )
        return machine

    def save(
        self,
        machine: Machine,
    ) -> Machine:
        return machine


def make_machine(
    *,
    tenant_id: uuid.UUID,
    code: str,
    name: str,
    machine_type: str = "Seccionadora",
    branch_id: uuid.UUID | None = None,
    manufacturer: str | None = None,
    model: str | None = None,
    serial_number: str | None = None,
) -> Machine:
    """Create one valid machine used by tests."""

    return Machine.create(
        tenant_id=tenant_id,
        code=code,
        name=name,
        machine_type=machine_type,
        branch_id=branch_id,
        manufacturer=manufacturer,
        model=model,
        serial_number=serial_number,
    )

def require_machine_id(
    machine: Machine,
) -> uuid.UUID:
    """Return the required identifier of a created machine."""

    if machine.id is None:
        raise RuntimeError(
            "A mÃ¡quina de teste deveria possuir identificador."
        )

    return machine.id

def test_create_machine_normalizes_data() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = CreateMachineUseCase(
        repository
    ).execute(
        tenant_id,
        MachineCreate(
            code=" maq-001 ",
            name=" Seccionadora ",
            machine_type=" Corte ",
            manufacturer=" Homag ",
            model=" Sawteq ",
            serial_number=" ABC-123 ",
        ),
    )

    assert machine.tenant_id == tenant_id
    assert machine.code == "MAQ-001"
    assert machine.name == "Seccionadora"
    assert machine.machine_type == "Corte"
    assert machine.manufacturer == "Homag"
    assert machine.model == "Sawteq"
    assert machine.serial_number == "ABC-123"
    assert machine.status is MachineStatus.AVAILABLE
    assert machine.is_active is True


def test_create_machine_allows_optional_branch() -> None:
    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = CreateMachineUseCase(
        repository
    ).execute(
        tenant_id,
        MachineCreate(
            code="MAQ-001",
            name="MÃ¡quina",
            machine_type="Tipo",
            branch_id=branch_id,
        ),
    )

    assert machine.branch_id == branch_id


def test_create_machine_rejects_duplicate_code() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    repository.add(
        make_machine(
            tenant_id=tenant_id,
            code="MAQ-001",
            name="Primeira",
        )
    )

    with pytest.raises(
        ConflictError
    ):
        CreateMachineUseCase(
            repository
        ).execute(
            tenant_id,
            MachineCreate(
                code=" maq-001 ",
                name="Segunda",
                machine_type="Tipo",
            ),
        )


def test_create_allows_same_code_other_tenant() -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    repository.add(
        make_machine(
            tenant_id=other_tenant_id,
            code="MAQ-001",
            name="Outro tenant",
        )
    )

    machine = CreateMachineUseCase(
        repository
    ).execute(
        tenant_id,
        MachineCreate(
            code="MAQ-001",
            name="Tenant atual",
            machine_type="Tipo",
        ),
    )

    assert machine.tenant_id == tenant_id


def test_get_machine() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="MÃ¡quina",
    )

    repository.add(
        machine
    )

    result = GetMachineUseCase(
        repository
    ).execute(
        tenant_id,
        require_machine_id(machine),
    )

    assert result is machine


def test_get_machine_is_tenant_scoped() -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="MÃ¡quina",
    )

    repository.add(
        machine
    )

    with pytest.raises(
        NotFoundError
    ):
        GetMachineUseCase(
            repository
        ).execute(
            other_tenant_id,
            require_machine_id(machine),
        )


def test_get_unknown_machine() -> None:
    with pytest.raises(
        NotFoundError
    ):
        GetMachineUseCase(
            FakeMachineRepository()
        ).execute(
            uuid.uuid4(),
            uuid.uuid4(),
        )


def test_list_is_tenant_scoped() -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    repository.add(
        make_machine(
            tenant_id=tenant_id,
            code="MAQ-A",
            name="MÃ¡quina A",
        )
    )

    repository.add(
        make_machine(
            tenant_id=other_tenant_id,
            code="MAQ-B",
            name="MÃ¡quina B",
        )
    )

    result = ListMachinesUseCase(
        repository
    ).execute(
        tenant_id
    )

    assert [
        machine.code
        for machine in result
    ] == [
        "MAQ-A"
    ]


@pytest.mark.parametrize(
    "search",
    [
        "MAQ-001",
        "Seccionadora",
        "Corte",
        "Homag",
        "Sawteq",
        "ABC-123",
    ],
)
def test_list_searches_machine_fields(
    search: str,
) -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    repository.add(
        make_machine(
            tenant_id=tenant_id,
            code="MAQ-001",
            name="Seccionadora",
            machine_type="Corte",
            manufacturer="Homag",
            model="Sawteq",
            serial_number="ABC-123",
        )
    )

    repository.add(
        make_machine(
            tenant_id=tenant_id,
            code="MAQ-002",
            name="Coladeira",
            machine_type="Borda",
        )
    )

    result = ListMachinesUseCase(
        repository
    ).execute(
        tenant_id,
        search=search,
    )

    assert len(result) == 1
    assert result[0].code == "MAQ-001"


def test_list_filters_machine_type() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    repository.add(
        make_machine(
            tenant_id=tenant_id,
            code="MAQ-001",
            name="Seccionadora",
            machine_type="Corte",
        )
    )

    repository.add(
        make_machine(
            tenant_id=tenant_id,
            code="MAQ-002",
            name="Coladeira",
            machine_type="Borda",
        )
    )

    result = ListMachinesUseCase(
        repository
    ).execute(
        tenant_id,
        machine_type=" Corte ",
    )

    assert len(result) == 1
    assert result[0].code == "MAQ-001"


def test_list_filters_status() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    available = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="DisponÃ­vel",
    )

    maintenance = make_machine(
        tenant_id=tenant_id,
        code="MAQ-002",
        name="ManutenÃ§Ã£o",
    )
    maintenance.send_to_maintenance()

    repository.add(
        available
    )
    repository.add(
        maintenance
    )

    result = ListMachinesUseCase(
        repository
    ).execute(
        tenant_id,
        status=MachineStatus.MAINTENANCE,
    )

    assert result == [
        maintenance
    ]


def test_list_filters_branch() -> None:
    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()
    other_branch_id = uuid.uuid4()
    repository = FakeMachineRepository()

    expected = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="Filial A",
        branch_id=branch_id,
    )

    repository.add(
        expected
    )

    repository.add(
        make_machine(
            tenant_id=tenant_id,
            code="MAQ-002",
            name="Filial B",
            branch_id=other_branch_id,
        )
    )

    result = ListMachinesUseCase(
        repository
    ).execute(
        tenant_id,
        branch_id=branch_id,
    )

    assert result == [
        expected
    ]


def test_list_excludes_inactive_by_default() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    active = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="Ativa",
    )

    inactive = make_machine(
        tenant_id=tenant_id,
        code="MAQ-002",
        name="Inativa",
    )
    inactive.deactivate()

    repository.add(
        active
    )
    repository.add(
        inactive
    )

    result = ListMachinesUseCase(
        repository
    ).execute(
        tenant_id
    )

    assert result == [
        active
    ]


def test_list_can_include_inactive() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="MÃ¡quina",
    )
    machine.deactivate()

    repository.add(
        machine
    )

    result = ListMachinesUseCase(
        repository
    ).execute(
        tenant_id,
        include_inactive=True,
    )

    assert machine in result


def test_list_paginates() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    for code, name in (
        ("MAQ-001", "Alfa"),
        ("MAQ-002", "Beta"),
        ("MAQ-003", "Gama"),
    ):
        repository.add(
            make_machine(
                tenant_id=tenant_id,
                code=code,
                name=name,
            )
        )

    result = ListMachinesUseCase(
        repository
    ).execute(
        tenant_id,
        limit=1,
        offset=1,
    )

    assert [
        machine.name
        for machine in result
    ] == [
        "Beta"
    ]


@pytest.mark.parametrize(
    ("limit", "offset"),
    [
        (0, 0),
        (201, 0),
        (100, -1),
    ],
)
def test_list_rejects_invalid_pagination(
    limit: int,
    offset: int,
) -> None:
    with pytest.raises(
        ValidationError
    ):
        ListMachinesUseCase(
            FakeMachineRepository()
        ).execute(
            uuid.uuid4(),
            limit=limit,
            offset=offset,
        )


def test_list_rejects_blank_search() -> None:
    with pytest.raises(
        ValidationError
    ):
        ListMachinesUseCase(
            FakeMachineRepository()
        ).execute(
            uuid.uuid4(),
            search="   ",
        )


def test_list_rejects_blank_machine_type() -> None:
    with pytest.raises(
        ValidationError
    ):
        ListMachinesUseCase(
            FakeMachineRepository()
        ).execute(
            uuid.uuid4(),
            machine_type="   ",
        )


def test_update_machine_all_fields() -> None:
    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="Antiga",
    )

    repository.add(
        machine
    )

    result = UpdateMachineUseCase(
        repository
    ).execute(
        tenant_id,
        require_machine_id(machine),
        MachineUpdate(
            code=" maq-002 ",
            name=" Nova ",
            machine_type=" Novo tipo ",
            branch_id=branch_id,
            manufacturer=" Fabricante ",
            model=" Modelo ",
            serial_number=" SERIAL ",
        ),
    )

    assert result.code == "MAQ-002"
    assert result.name == "Nova"
    assert result.machine_type == "Novo tipo"
    assert result.branch_id == branch_id
    assert result.manufacturer == "Fabricante"
    assert result.model == "Modelo"
    assert result.serial_number == "SERIAL"


def test_update_preserves_unspecified_fields() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="Original",
        manufacturer="Homag",
    )

    repository.add(
        machine
    )

    result = UpdateMachineUseCase(
        repository
    ).execute(
        tenant_id,
        require_machine_id(machine),
        MachineUpdate(
            name="Atualizada"
        ),
    )

    assert result.code == "MAQ-001"
    assert result.name == "Atualizada"
    assert result.manufacturer == "Homag"


def test_update_can_clear_optional_fields() -> None:
    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = make_machine(
        tenant_id=tenant_id,
        branch_id=branch_id,
        code="MAQ-001",
        name="MÃ¡quina",
        manufacturer="Homag",
        model="Modelo",
        serial_number="123",
    )

    repository.add(
        machine
    )

    result = UpdateMachineUseCase(
        repository
    ).execute(
        tenant_id,
        require_machine_id(machine),
        MachineUpdate(
            branch_id=None,
            manufacturer=None,
            model=None,
            serial_number=None,
        ),
    )

    assert result.branch_id is None
    assert result.manufacturer is None
    assert result.model is None
    assert result.serial_number is None


def test_update_rejects_empty_payload() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="MÃ¡quina",
    )

    repository.add(
        machine
    )

    with pytest.raises(
        ValidationError
    ):
        UpdateMachineUseCase(
            repository
        ).execute(
            tenant_id,
            require_machine_id(machine),
            MachineUpdate(),
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "code",
        "name",
        "machine_type",
    ],
)
def test_update_rejects_null_required_field(
    field_name: str,
) -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="MÃ¡quina",
    )

    repository.add(
        machine
    )

    payload = MachineUpdate.model_construct(
        **{
            field_name: None,
        }
    )

    payload.__pydantic_fields_set__ = {
        field_name
    }

    with pytest.raises(
        ValidationError
    ):
        UpdateMachineUseCase(
            repository
        ).execute(
            tenant_id,
            require_machine_id(machine),
            payload,
        )


def test_update_rejects_duplicate_code() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    first = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="Primeira",
    )

    second = make_machine(
        tenant_id=tenant_id,
        code="MAQ-002",
        name="Segunda",
    )

    repository.add(
        first
    )
    repository.add(
        second
    )

    with pytest.raises(
        ConflictError
    ):
        UpdateMachineUseCase(
            repository
        ).execute(
            tenant_id,
            require_machine_id(second),
            MachineUpdate(
                code="maq-001"
            ),
        )


def test_update_unknown_machine() -> None:
    with pytest.raises(
        NotFoundError
    ):
        UpdateMachineUseCase(
            FakeMachineRepository()
        ).execute(
            uuid.uuid4(),
            uuid.uuid4(),
            MachineUpdate(
                name="Atualizada"
            ),
        )


@pytest.mark.parametrize(
    "status",
    [
        MachineStatus.AVAILABLE,
        MachineStatus.IN_USE,
        MachineStatus.MAINTENANCE,
        MachineStatus.OUT_OF_SERVICE,
    ],
)
def test_changes_machine_status(
    status: MachineStatus,
) -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="MÃ¡quina",
    )

    repository.add(
        machine
    )

    result = ChangeMachineStatusUseCase(
        repository
    ).execute(
        tenant_id,
        require_machine_id(machine),
        status,
    )

    assert result.status is status


def test_change_status_is_idempotent() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="MÃ¡quina",
    )

    repository.add(
        machine
    )

    first_updated_at = machine.updated_at

    result = ChangeMachineStatusUseCase(
        repository
    ).execute(
        tenant_id,
        require_machine_id(machine),
        MachineStatus.AVAILABLE,
    )

    assert result.status is MachineStatus.AVAILABLE
    assert result.updated_at == first_updated_at


def test_change_status_unknown_machine() -> None:
    with pytest.raises(
        NotFoundError
    ):
        ChangeMachineStatusUseCase(
            FakeMachineRepository()
        ).execute(
            uuid.uuid4(),
            uuid.uuid4(),
            MachineStatus.MAINTENANCE,
        )


def test_machine_status_schema_rejects_invalid_status() -> None:
    with pytest.raises(
        PydanticValidationError
    ):
        MachineStatusUpdate(
            status="INVALID"  # type: ignore[arg-type]
        )


def test_deactivates_machine() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="MÃ¡quina",
    )

    repository.add(
        machine
    )

    result = DeactivateMachineUseCase(
        repository
    ).execute(
        tenant_id,
        require_machine_id(machine),
    )

    assert result.is_active is False


def test_deactivate_is_idempotent() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="MÃ¡quina",
    )

    machine.deactivate()
    previous_updated_at = machine.updated_at

    repository.add(
        machine
    )

    result = DeactivateMachineUseCase(
        repository
    ).execute(
        tenant_id,
        require_machine_id(machine),
    )

    assert result.is_active is False
    assert result.updated_at == previous_updated_at


def test_deactivate_unknown_machine() -> None:
    with pytest.raises(
        NotFoundError
    ):
        DeactivateMachineUseCase(
            FakeMachineRepository()
        ).execute(
            uuid.uuid4(),
            uuid.uuid4(),
        )


def test_reactivates_machine() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="MÃ¡quina",
    )
    machine.deactivate()

    repository.add(
        machine
    )

    result = ReactivateMachineUseCase(
        repository
    ).execute(
        tenant_id,
        require_machine_id(machine),
    )

    assert result.is_active is True


def test_reactivate_is_idempotent() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeMachineRepository()

    machine = make_machine(
        tenant_id=tenant_id,
        code="MAQ-001",
        name="MÃ¡quina",
    )

    previous_updated_at = machine.updated_at

    repository.add(
        machine
    )

    result = ReactivateMachineUseCase(
        repository
    ).execute(
        tenant_id,
        require_machine_id(machine),
    )

    assert result.is_active is True
    assert result.updated_at == previous_updated_at


def test_reactivate_unknown_machine() -> None:
    with pytest.raises(
        NotFoundError
    ):
        ReactivateMachineUseCase(
            FakeMachineRepository()
        ).execute(
            uuid.uuid4(),
            uuid.uuid4(),
        )


def test_schemas_forbid_extra_fields() -> None:
    with pytest.raises(
        PydanticValidationError
    ):
        MachineCreate(
            code="MAQ-001",
            name="MÃ¡quina",
            machine_type="Tipo",
            unexpected="value",  # type: ignore[call-arg]
        )

