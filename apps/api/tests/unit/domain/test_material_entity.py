"""Unit tests for material domain behavior."""

from __future__ import annotations

import uuid

import pytest

from organizeg3_api.domain.material.entity import (
    Material,
)


def test_creates_and_normalizes_material() -> None:
    tenant_id = uuid.uuid4()
    brand_id = uuid.uuid4()

    material = Material.create(
        tenant_id=tenant_id,
        code=" mat-001 ",
        name="  MDF Branco TX 15mm  ",
        category="  Chapas  ",
        unit=" un ",
        brand_id=brand_id,
    )

    assert material.id is not None
    assert material.tenant_id == tenant_id
    assert material.code == "MAT-001"
    assert material.name == "MDF Branco TX 15mm"
    assert material.category == "Chapas"
    assert material.unit == "UN"
    assert material.brand_id == brand_id
    assert material.is_active is True
    assert material.created_at is not None
    assert material.updated_at is not None


def test_allows_material_without_brand() -> None:
    material = Material.create(
        tenant_id=uuid.uuid4(),
        code="MAT-001",
        name="Fita de Borda",
        category="Fitas",
        unit="M",
    )

    assert material.brand_id is None


@pytest.mark.parametrize(
    "code",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_material_code(
    code: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="código",
    ):
        Material.create(
            tenant_id=uuid.uuid4(),
            code=code,
            name="Material",
            category="Categoria",
            unit="UN",
        )


@pytest.mark.parametrize(
    "name",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_material_name(
    name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="nome",
    ):
        Material.create(
            tenant_id=uuid.uuid4(),
            code="MAT-001",
            name=name,
            category="Categoria",
            unit="UN",
        )


@pytest.mark.parametrize(
    "category",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_material_category(
    category: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="categoria",
    ):
        Material.create(
            tenant_id=uuid.uuid4(),
            code="MAT-001",
            name="Material",
            category=category,
            unit="UN",
        )


@pytest.mark.parametrize(
    "unit",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_material_unit(
    unit: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="unidade",
    ):
        Material.create(
            tenant_id=uuid.uuid4(),
            code="MAT-001",
            name="Material",
            category="Categoria",
            unit=unit,
        )


def test_rejects_null_material_tenant_uuid() -> None:
    with pytest.raises(
        ValueError,
        match="UUID nulo",
    ):
        Material.create(
            tenant_id=uuid.UUID(int=0),
            code="MAT-001",
            name="Material",
            category="Categoria",
            unit="UN",
        )


def test_rejects_invalid_material_tenant_type() -> None:
    with pytest.raises(
        TypeError,
        match="tenant",
    ):
        Material.create(  # type: ignore[arg-type]
            tenant_id="tenant",
            code="MAT-001",
            name="Material",
            category="Categoria",
            unit="UN",
        )


def test_rejects_null_brand_uuid() -> None:
    with pytest.raises(
        ValueError,
        match="UUID nulo",
    ):
        Material.create(
            tenant_id=uuid.uuid4(),
            code="MAT-001",
            name="Material",
            category="Categoria",
            unit="UN",
            brand_id=uuid.UUID(int=0),
        )


def test_assigns_brand() -> None:
    material = Material.create(
        tenant_id=uuid.uuid4(),
        code="MAT-001",
        name="Material",
        category="Categoria",
        unit="UN",
    )

    brand_id = uuid.uuid4()

    material.assign_brand(
        brand_id
    )

    assert material.brand_id == brand_id


def test_removes_brand() -> None:
    material = Material.create(
        tenant_id=uuid.uuid4(),
        code="MAT-001",
        name="Material",
        category="Categoria",
        unit="UN",
        brand_id=uuid.uuid4(),
    )

    material.remove_brand()

    assert material.brand_id is None


def test_deactivates_material() -> None:
    material = Material.create(
        tenant_id=uuid.uuid4(),
        code="MAT-001",
        name="Material",
        category="Categoria",
        unit="UN",
    )

    material.deactivate()

    assert material.is_active is False


def test_reactivates_material() -> None:
    material = Material.create(
        tenant_id=uuid.uuid4(),
        code="MAT-001",
        name="Material",
        category="Categoria",
        unit="UN",
    )

    material.deactivate()
    material.activate()

    assert material.is_active is True
