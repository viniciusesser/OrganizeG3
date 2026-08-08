"""Unit tests for service domain behavior."""

from __future__ import annotations

import uuid

import pytest

from organizeg3_api.domain.service.entity import (
    Service,
)
from organizeg3_api.domain.service.value_objects import (
    ServiceExecutionMode,
)


def test_creates_and_normalizes_service() -> None:
    tenant_id = uuid.uuid4()

    service = Service.create(
        tenant_id=tenant_id,
        code=" serv-001 ",
        name="  Corte de MDF  ",
        category="  Corte  ",
        unit=" h ",
        execution_mode=ServiceExecutionMode.INTERNAL,
        estimated_duration_minutes=45,
    )

    assert service.id is not None
    assert service.tenant_id == tenant_id
    assert service.code == "SERV-001"
    assert service.name == "Corte de MDF"
    assert service.category == "Corte"
    assert service.unit == "H"

    assert (
        service.execution_mode
        is ServiceExecutionMode.INTERNAL
    )

    assert (
        service.estimated_duration_minutes
        == 45
    )

    assert service.is_active is True
    assert service.created_at is not None
    assert service.updated_at is not None


def test_allows_service_without_duration() -> None:
    service = Service.create(
        tenant_id=uuid.uuid4(),
        code="SERV-001",
        name="Instalação",
        category="Instalação",
        unit="UN",
        execution_mode=ServiceExecutionMode.BOTH,
    )

    assert (
        service.estimated_duration_minutes
        is None
    )


@pytest.mark.parametrize(
    "code",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_service_code(
    code: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="código",
    ):
        Service.create(
            tenant_id=uuid.uuid4(),
            code=code,
            name="Serviço",
            category="Categoria",
            unit="UN",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
        )


@pytest.mark.parametrize(
    "name",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_service_name(
    name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="nome",
    ):
        Service.create(
            tenant_id=uuid.uuid4(),
            code="SERV-001",
            name=name,
            category="Categoria",
            unit="UN",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
        )


@pytest.mark.parametrize(
    "category",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_service_category(
    category: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="categoria",
    ):
        Service.create(
            tenant_id=uuid.uuid4(),
            code="SERV-001",
            name="Serviço",
            category=category,
            unit="UN",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
        )


@pytest.mark.parametrize(
    "unit",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_service_unit(
    unit: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="unidade",
    ):
        Service.create(
            tenant_id=uuid.uuid4(),
            code="SERV-001",
            name="Serviço",
            category="Categoria",
            unit=unit,
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
        )


def test_rejects_null_tenant_uuid() -> None:
    with pytest.raises(
        ValueError,
        match="UUID nulo",
    ):
        Service.create(
            tenant_id=uuid.UUID(int=0),
            code="SERV-001",
            name="Serviço",
            category="Categoria",
            unit="UN",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
        )


def test_rejects_invalid_tenant_type() -> None:
    with pytest.raises(
        TypeError,
        match="tenant",
    ):
        Service.create(  # type: ignore[arg-type]
            tenant_id="tenant",
            code="SERV-001",
            name="Serviço",
            category="Categoria",
            unit="UN",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
        )


def test_rejects_invalid_execution_mode() -> None:
    with pytest.raises(
        TypeError,
        match="modo de execução",
    ):
        Service.create(  # type: ignore[arg-type]
            tenant_id=uuid.uuid4(),
            code="SERV-001",
            name="Serviço",
            category="Categoria",
            unit="UN",
            execution_mode="INTERNAL",
        )


@pytest.mark.parametrize(
    "duration",
    [
        0,
        -1,
        -60,
    ],
)
def test_rejects_non_positive_duration(
    duration: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        Service.create(
            tenant_id=uuid.uuid4(),
            code="SERV-001",
            name="Serviço",
            category="Categoria",
            unit="UN",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
            estimated_duration_minutes=duration,
        )


def test_rejects_boolean_duration() -> None:
    with pytest.raises(
        TypeError,
        match="número inteiro",
    ):
        Service.create(  # type: ignore[arg-type]
            tenant_id=uuid.uuid4(),
            code="SERV-001",
            name="Serviço",
            category="Categoria",
            unit="UN",
            execution_mode=(
                ServiceExecutionMode.INTERNAL
            ),
            estimated_duration_minutes=True,
        )


def test_changes_execution_mode() -> None:
    service = Service.create(
        tenant_id=uuid.uuid4(),
        code="SERV-001",
        name="Montagem",
        category="Montagem",
        unit="H",
        execution_mode=ServiceExecutionMode.INTERNAL,
    )

    service.change_execution_mode(
        ServiceExecutionMode.BOTH
    )

    assert (
        service.execution_mode
        is ServiceExecutionMode.BOTH
    )


def test_changes_estimated_duration() -> None:
    service = Service.create(
        tenant_id=uuid.uuid4(),
        code="SERV-001",
        name="Fitagem",
        category="Fitagem",
        unit="H",
        execution_mode=ServiceExecutionMode.INTERNAL,
        estimated_duration_minutes=30,
    )

    service.change_estimated_duration(
        45
    )

    assert (
        service.estimated_duration_minutes
        == 45
    )


def test_clears_estimated_duration() -> None:
    service = Service.create(
        tenant_id=uuid.uuid4(),
        code="SERV-001",
        name="Fitagem",
        category="Fitagem",
        unit="H",
        execution_mode=ServiceExecutionMode.INTERNAL,
        estimated_duration_minutes=30,
    )

    service.change_estimated_duration(
        None
    )

    assert (
        service.estimated_duration_minutes
        is None
    )


def test_deactivates_service() -> None:
    service = Service.create(
        tenant_id=uuid.uuid4(),
        code="SERV-001",
        name="Serviço",
        category="Categoria",
        unit="UN",
        execution_mode=ServiceExecutionMode.INTERNAL,
    )

    service.deactivate()

    assert service.is_active is False


def test_reactivates_service() -> None:
    service = Service.create(
        tenant_id=uuid.uuid4(),
        code="SERV-001",
        name="Serviço",
        category="Categoria",
        unit="UN",
        execution_mode=ServiceExecutionMode.INTERNAL,
    )

    service.deactivate()
    service.activate()

    assert service.is_active is True
