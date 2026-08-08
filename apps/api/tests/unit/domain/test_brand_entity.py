"""Unit tests for brand domain behavior."""

from __future__ import annotations

import uuid

import pytest

from organizeg3_api.domain.brand.entity import (
    Brand,
)


def test_creates_and_normalizes_brand() -> None:
    tenant_id = uuid.uuid4()

    brand = Brand.create(
        tenant_id=tenant_id,
        code=" marca-001 ",
        name="  Duratex  ",
    )

    assert brand.id is not None
    assert brand.tenant_id == tenant_id
    assert brand.code == "MARCA-001"
    assert brand.name == "Duratex"
    assert brand.is_active is True
    assert brand.created_at is not None
    assert brand.updated_at is not None


@pytest.mark.parametrize(
    "code",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_brand_code(
    code: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="código",
    ):
        Brand.create(
            tenant_id=uuid.uuid4(),
            code=code,
            name="Duratex",
        )


@pytest.mark.parametrize(
    "name",
    [
        "",
        "   ",
    ],
)
def test_rejects_blank_brand_name(
    name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="nome",
    ):
        Brand.create(
            tenant_id=uuid.uuid4(),
            code="MARCA-001",
            name=name,
        )


def test_rejects_null_brand_tenant_uuid() -> None:
    with pytest.raises(
        ValueError,
        match="UUID nulo",
    ):
        Brand.create(
            tenant_id=uuid.UUID(int=0),
            code="MARCA-001",
            name="Duratex",
        )


def test_rejects_invalid_brand_tenant_type() -> None:
    with pytest.raises(
        TypeError,
        match="tenant",
    ):
        Brand.create(  # type: ignore[arg-type]
            tenant_id="tenant",
            code="MARCA-001",
            name="Duratex",
        )


def test_deactivates_brand() -> None:
    brand = Brand.create(
        tenant_id=uuid.uuid4(),
        code="MARCA-001",
        name="Duratex",
    )

    brand.deactivate()

    assert brand.is_active is False


def test_reactivates_brand() -> None:
    brand = Brand.create(
        tenant_id=uuid.uuid4(),
        code="MARCA-001",
        name="Duratex",
    )

    brand.deactivate()
    brand.activate()

    assert brand.is_active is True
