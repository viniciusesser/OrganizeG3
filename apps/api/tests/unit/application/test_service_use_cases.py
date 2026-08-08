"""Unit tests for service application use cases."""

from __future__ import annotations

import uuid

from pydantic import ValidationError as PydanticValidationError
import pytest

from organizeg3_api.application.service.schemas import (
    ServiceCreate,
    ServiceUpdate,
)
from organizeg3_api.application.service.use_cases import (
    CreateServiceUseCase,
    DeactivateServiceUseCase,
    GetServiceUseCase,
    ListServicesUseCase,
    ReactivateServiceUseCase,
    UpdateServiceUseCase,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.service.entity import (
    Service,
)
from organizeg3_api.domain.service.value_objects import (
    ServiceExecutionMode,
)


class FakeServiceRepository:
    """In-memory service repository used by application tests."""

    def __init__(self) -> None:
        self.items: list[Service] = []

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        service_id: uuid.UUID,
    ) -> Service | None:
        for service in self.items:
            if (
                service.tenant_id == tenant_id
                and service.id == service_id
            ):
                return service

        return None

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> Service | None:
        normalized = code.strip().upper()

        for service in self.items:
            if (
                service.tenant_id == tenant_id
                and service.code == normalized
            ):
                return service

        return None

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        category: str | None = None,
        execution_mode: ServiceExecutionMode | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Service]:
        result = [
            service
            for service in self.items
            if service.tenant_id == tenant_id
        ]

        if not include_inactive:
            result = [
                service
                for service in result
                if service.is_active
            ]

        if search is not None:
            normalized_search = search.lower()

            result = [
                service
                for service in result
                if (
                    normalized_search
                    in service.code.lower()
                    or normalized_search
                    in service.name.lower()
                    or normalized_search
                    in service.category.lower()
                    or normalized_search
                    in service.unit.lower()
                )
            ]

        if category is not None:
            result = [
                service
                for service in result
                if service.category == category
            ]

        if execution_mode is not None:
            result = [
                service
                for service in result
                if (
                    service.execution_mode
                    is execution_mode
                )
            ]

        result.sort(
            key=lambda service: (
                service.name,
                service.code,
                str(service.id),
            )
        )

        return result[
            offset : offset + limit
        ]

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_service_id: uuid.UUID | None = None,
    ) -> bool:
        normalized = code.strip().upper()

        return any(
            service.tenant_id == tenant_id
            and service.code == normalized
            and service.id != exclude_service_id
            for service in self.items
        )

    def add(
        self,
        service: Service,
    ) -> Service:
        self.items.append(
            service
        )

        return service

    def save(
        self,
        service: Service,
    ) -> Service:
        if service.id is None:
            raise ValueError(
                "Serviço sem identificador."
            )

        for index, current in enumerate(
            self.items
        ):
            if (
                current.id == service.id
                and current.tenant_id
                == service.tenant_id
            ):
                self.items[index] = service
                return service

        raise ValueError(
            "Serviço não encontrado."
        )


def make_service(
    *,
    tenant_id: uuid.UUID | None = None,
    code: str = "SERV-001",
    name: str = "Corte de MDF",
    category: str = "Corte",
    unit: str = "H",
    execution_mode: ServiceExecutionMode = (
        ServiceExecutionMode.INTERNAL
    ),
    estimated_duration_minutes: int | None = 45,
) -> Service:
    """Create a valid service for tests."""

    return Service.create(
        tenant_id=(
            tenant_id
            or uuid.uuid4()
        ),
        code=code,
        name=name,
        category=category,
        unit=unit,
        execution_mode=execution_mode,
        estimated_duration_minutes=(
            estimated_duration_minutes
        ),
    )


def test_create_service() -> None:
    repository = FakeServiceRepository()
    tenant_id = uuid.uuid4()

    use_case = CreateServiceUseCase(
        repository
    )

    result = use_case.execute(
        tenant_id=tenant_id,
        data=ServiceCreate(
            code=" serv-001 ",
            name=" Corte de MDF ",
            category=" Corte ",
            unit=" h ",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
            estimated_duration_minutes=45,
        ),
    )

    assert result.tenant_id == tenant_id
    assert result.code == "SERV-001"
    assert result.name == "Corte de MDF"
    assert result.category == "Corte"
    assert result.unit == "H"

    assert (
        result.execution_mode
        is ServiceExecutionMode.INTERNAL
    )

    assert (
        result.estimated_duration_minutes
        == 45
    )


def test_create_service_without_duration() -> None:
    repository = FakeServiceRepository()

    result = CreateServiceUseCase(
        repository
    ).execute(
        tenant_id=uuid.uuid4(),
        data=ServiceCreate(
            code="SERV-001",
            name="Instalação",
            category="Instalação",
            unit="UN",
            execution_mode=(
                ServiceExecutionMode.BOTH
            ),
        ),
    )

    assert (
        result.estimated_duration_minutes
        is None
    )


def test_create_rejects_duplicate_code() -> None:
    tenant_id = uuid.uuid4()

    repository = FakeServiceRepository()

    repository.add(
        make_service(
            tenant_id=tenant_id,
            code="SERV-001",
        )
    )

    with pytest.raises(
        ConflictError
    ) as exc_info:
        CreateServiceUseCase(
            repository
        ).execute(
            tenant_id=tenant_id,
            data=ServiceCreate(
                code="serv-001",
                name="Outro",
                category="Categoria",
                unit="UN",
                execution_mode=(
                    ServiceExecutionMode.INTERNAL
                ),
            ),
        )

    assert exc_info.value.details == {
        "field": "code",
        "value": "SERV-001",
    }


def test_same_code_is_allowed_for_other_tenant() -> None:
    repository = FakeServiceRepository()

    first_tenant = uuid.uuid4()
    second_tenant = uuid.uuid4()

    repository.add(
        make_service(
            tenant_id=first_tenant,
            code="SERV-001",
        )
    )

    result = CreateServiceUseCase(
        repository
    ).execute(
        tenant_id=second_tenant,
        data=ServiceCreate(
            code="SERV-001",
            name="Serviço B",
            category="Categoria",
            unit="UN",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
        ),
    )

    assert result.tenant_id == second_tenant


def test_get_service() -> None:
    repository = FakeServiceRepository()

    service = make_service()

    repository.add(
        service
    )

    assert service.id is not None

    result = GetServiceUseCase(
        repository
    ).execute(
        tenant_id=service.tenant_id,
        service_id=service.id,
    )

    assert result is service


def test_get_service_is_tenant_scoped() -> None:
    repository = FakeServiceRepository()

    service = make_service()

    repository.add(
        service
    )

    assert service.id is not None

    with pytest.raises(
        NotFoundError
    ):
        GetServiceUseCase(
            repository
        ).execute(
            tenant_id=uuid.uuid4(),
            service_id=service.id,
        )


def test_get_unknown_service() -> None:
    repository = FakeServiceRepository()

    with pytest.raises(
        NotFoundError
    ):
        GetServiceUseCase(
            repository
        ).execute(
            tenant_id=uuid.uuid4(),
            service_id=uuid.uuid4(),
        )


def test_list_services_is_tenant_scoped() -> None:
    repository = FakeServiceRepository()

    tenant_a = uuid.uuid4()
    tenant_b = uuid.uuid4()

    repository.add(
        make_service(
            tenant_id=tenant_a,
            code="SERV-A",
            name="Serviço A",
        )
    )

    repository.add(
        make_service(
            tenant_id=tenant_b,
            code="SERV-B",
            name="Serviço B",
        )
    )

    result = ListServicesUseCase(
        repository
    ).execute(
        tenant_id=tenant_a
    )

    assert len(result) == 1
    assert result[0].name == "Serviço A"


@pytest.mark.parametrize(
    "search",
    [
        "SERV-001",
        "corte",
        "Corte",
        "H",
    ],
)
def test_list_services_searches_supported_fields(
    search: str,
) -> None:
    tenant_id = uuid.uuid4()

    repository = FakeServiceRepository()

    repository.add(
        make_service(
            tenant_id=tenant_id,
            code="SERV-001",
            name="Corte de MDF",
            category="Corte",
            unit="H",
        )
    )

    repository.add(
        make_service(
            tenant_id=tenant_id,
            code="SERV-002",
            name="Instalação",
            category="Instalação",
            unit="UN",
        )
    )

    result = ListServicesUseCase(
        repository
    ).execute(
        tenant_id=tenant_id,
        search=search,
    )

    assert len(result) == 1
    assert result[0].code == "SERV-001"


def test_list_filters_category() -> None:
    tenant_id = uuid.uuid4()

    repository = FakeServiceRepository()

    repository.add(
        make_service(
            tenant_id=tenant_id,
            code="SERV-001",
            category="Corte",
        )
    )

    repository.add(
        make_service(
            tenant_id=tenant_id,
            code="SERV-002",
            name="Montagem",
            category="Montagem",
        )
    )

    result = ListServicesUseCase(
        repository
    ).execute(
        tenant_id=tenant_id,
        category=" Corte ",
    )

    assert len(result) == 1
    assert result[0].code == "SERV-001"


def test_list_filters_execution_mode() -> None:
    tenant_id = uuid.uuid4()

    repository = FakeServiceRepository()

    repository.add(
        make_service(
            tenant_id=tenant_id,
            code="SERV-001",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
        )
    )

    repository.add(
        make_service(
            tenant_id=tenant_id,
            code="SERV-002",
            name="Pintura",
            execution_mode=(
                ServiceExecutionMode.EXTERNAL
            ),
        )
    )

    result = ListServicesUseCase(
        repository
    ).execute(
        tenant_id=tenant_id,
        execution_mode=(
            ServiceExecutionMode.EXTERNAL
        ),
    )

    assert len(result) == 1
    assert result[0].code == "SERV-002"


def test_list_excludes_inactive_by_default() -> None:
    tenant_id = uuid.uuid4()

    repository = FakeServiceRepository()

    active = make_service(
        tenant_id=tenant_id,
        code="SERV-001",
    )

    inactive = make_service(
        tenant_id=tenant_id,
        code="SERV-002",
        name="Inativo",
    )

    inactive.deactivate()

    repository.add(active)
    repository.add(inactive)

    result = ListServicesUseCase(
        repository
    ).execute(
        tenant_id=tenant_id
    )

    assert result == [
        active
    ]


def test_list_can_include_inactive() -> None:
    tenant_id = uuid.uuid4()

    repository = FakeServiceRepository()

    service = make_service(
        tenant_id=tenant_id
    )

    service.deactivate()

    repository.add(
        service
    )

    result = ListServicesUseCase(
        repository
    ).execute(
        tenant_id=tenant_id,
        include_inactive=True,
    )

    assert result == [
        service
    ]


def test_list_paginates() -> None:
    tenant_id = uuid.uuid4()

    repository = FakeServiceRepository()

    repository.add(
        make_service(
            tenant_id=tenant_id,
            code="SERV-001",
            name="Alfa",
        )
    )

    repository.add(
        make_service(
            tenant_id=tenant_id,
            code="SERV-002",
            name="Beta",
        )
    )

    repository.add(
        make_service(
            tenant_id=tenant_id,
            code="SERV-003",
            name="Gama",
        )
    )

    result = ListServicesUseCase(
        repository
    ).execute(
        tenant_id=tenant_id,
        limit=1,
        offset=1,
    )

    assert len(result) == 1
    assert result[0].name == "Beta"


@pytest.mark.parametrize(
    ("limit", "offset"),
    [
        (
            0,
            0,
        ),
        (
            201,
            0,
        ),
        (
            10,
            -1,
        ),
    ],
)
def test_list_rejects_invalid_pagination(
    limit: int,
    offset: int,
) -> None:
    with pytest.raises(
        ValidationError
    ):
        ListServicesUseCase(
            FakeServiceRepository()
        ).execute(
            tenant_id=uuid.uuid4(),
            limit=limit,
            offset=offset,
        )


def test_list_rejects_blank_search() -> None:
    with pytest.raises(
        ValidationError
    ):
        ListServicesUseCase(
            FakeServiceRepository()
        ).execute(
            tenant_id=uuid.uuid4(),
            search="   ",
        )


def test_update_service() -> None:
    repository = FakeServiceRepository()

    service = make_service()

    repository.add(
        service
    )

    assert service.id is not None

    result = UpdateServiceUseCase(
        repository
    ).execute(
        tenant_id=service.tenant_id,
        service_id=service.id,
        data=ServiceUpdate(
            code=" serv-002 ",
            name=" Montagem ",
            category=" Produção ",
            unit=" un ",
            execution_mode=(
                ServiceExecutionMode.BOTH
            ),
            estimated_duration_minutes=60,
        ),
    )

    assert result.code == "SERV-002"
    assert result.name == "Montagem"
    assert result.category == "Produção"
    assert result.unit == "UN"

    assert (
        result.execution_mode
        is ServiceExecutionMode.BOTH
    )

    assert (
        result.estimated_duration_minutes
        == 60
    )


def test_update_preserves_unspecified_fields() -> None:
    repository = FakeServiceRepository()

    service = make_service(
        estimated_duration_minutes=30
    )

    repository.add(
        service
    )

    assert service.id is not None

    result = UpdateServiceUseCase(
        repository
    ).execute(
        tenant_id=service.tenant_id,
        service_id=service.id,
        data=ServiceUpdate(
            name="Nome Novo"
        ),
    )

    assert result.name == "Nome Novo"
    assert result.code == "SERV-001"
    assert result.category == "Corte"
    assert result.unit == "H"

    assert (
        result.execution_mode
        is ServiceExecutionMode.INTERNAL
    )

    assert (
        result.estimated_duration_minutes
        == 30
    )


def test_update_can_clear_duration() -> None:
    repository = FakeServiceRepository()

    service = make_service(
        estimated_duration_minutes=45
    )

    repository.add(
        service
    )

    assert service.id is not None

    data = ServiceUpdate(
        estimated_duration_minutes=None
    )

    result = UpdateServiceUseCase(
        repository
    ).execute(
        tenant_id=service.tenant_id,
        service_id=service.id,
        data=data,
    )

    assert (
        result.estimated_duration_minutes
        is None
    )


def test_update_rejects_empty_payload() -> None:
    repository = FakeServiceRepository()

    service = make_service()

    repository.add(
        service
    )

    assert service.id is not None

    with pytest.raises(
        ValidationError
    ):
        UpdateServiceUseCase(
            repository
        ).execute(
            tenant_id=service.tenant_id,
            service_id=service.id,
            data=ServiceUpdate(),
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "code",
        "name",
        "category",
        "unit",
        "execution_mode",
    ],
)
def test_update_rejects_null_required_field(
    field_name: str,
) -> None:
    repository = FakeServiceRepository()

    service = make_service()

    repository.add(
        service
    )

    assert service.id is not None

    data = ServiceUpdate.model_validate(
        {
            field_name: None,
        }
    )

    with pytest.raises(
        ValidationError
    ):
        UpdateServiceUseCase(
            repository
        ).execute(
            tenant_id=service.tenant_id,
            service_id=service.id,
            data=data,
        )


def test_update_rejects_duplicate_code() -> None:
    tenant_id = uuid.uuid4()

    repository = FakeServiceRepository()

    first = make_service(
        tenant_id=tenant_id,
        code="SERV-001",
        name="Primeiro",
    )

    second = make_service(
        tenant_id=tenant_id,
        code="SERV-002",
        name="Segundo",
    )

    repository.add(first)
    repository.add(second)

    assert second.id is not None

    with pytest.raises(
        ConflictError
    ):
        UpdateServiceUseCase(
            repository
        ).execute(
            tenant_id=tenant_id,
            service_id=second.id,
            data=ServiceUpdate(
                code="serv-001"
            ),
        )


def test_update_unknown_service() -> None:
    with pytest.raises(
        NotFoundError
    ):
        UpdateServiceUseCase(
            FakeServiceRepository()
        ).execute(
            tenant_id=uuid.uuid4(),
            service_id=uuid.uuid4(),
            data=ServiceUpdate(
                name="Novo"
            ),
        )


def test_deactivate_service() -> None:
    repository = FakeServiceRepository()

    service = make_service()

    repository.add(
        service
    )

    assert service.id is not None

    result = DeactivateServiceUseCase(
        repository
    ).execute(
        tenant_id=service.tenant_id,
        service_id=service.id,
    )

    assert result.is_active is False


def test_deactivate_is_idempotent() -> None:
    repository = FakeServiceRepository()

    service = make_service()

    service.deactivate()

    repository.add(
        service
    )

    assert service.id is not None

    original_updated_at = (
        service.updated_at
    )

    result = DeactivateServiceUseCase(
        repository
    ).execute(
        tenant_id=service.tenant_id,
        service_id=service.id,
    )

    assert result.is_active is False

    assert (
        result.updated_at
        == original_updated_at
    )


def test_deactivate_unknown_service() -> None:
    with pytest.raises(
        NotFoundError
    ):
        DeactivateServiceUseCase(
            FakeServiceRepository()
        ).execute(
            tenant_id=uuid.uuid4(),
            service_id=uuid.uuid4(),
        )


def test_reactivate_service() -> None:
    repository = FakeServiceRepository()

    service = make_service()

    service.deactivate()

    repository.add(
        service
    )

    assert service.id is not None

    result = ReactivateServiceUseCase(
        repository
    ).execute(
        tenant_id=service.tenant_id,
        service_id=service.id,
    )

    assert result.is_active is True


def test_reactivate_is_idempotent() -> None:
    repository = FakeServiceRepository()

    service = make_service()

    repository.add(
        service
    )

    assert service.id is not None

    original_updated_at = (
        service.updated_at
    )

    result = ReactivateServiceUseCase(
        repository
    ).execute(
        tenant_id=service.tenant_id,
        service_id=service.id,
    )

    assert result.is_active is True

    assert (
        result.updated_at
        == original_updated_at
    )


def test_reactivate_unknown_service() -> None:
    with pytest.raises(
        NotFoundError
    ):
        ReactivateServiceUseCase(
            FakeServiceRepository()
        ).execute(
            tenant_id=uuid.uuid4(),
            service_id=uuid.uuid4(),
        )


@pytest.mark.parametrize(
    "duration",
    [
        0,
        -1,
    ],
)
def test_schema_rejects_invalid_duration(
    duration: int,
) -> None:
    with pytest.raises(
        PydanticValidationError
    ):
        ServiceCreate(
            code="SERV-001",
            name="Serviço",
            category="Categoria",
            unit="UN",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
            estimated_duration_minutes=duration,
        )


def test_schema_rejects_extra_fields() -> None:
    with pytest.raises(
        PydanticValidationError
    ):
        ServiceCreate.model_validate(
            {
                "code": "SERV-001",
                "name": "Serviço",
                "category": "Categoria",
                "unit": "UN",
                "execution_mode": "INTERNAL",
                "campo_inexistente": True,
            }
        )
