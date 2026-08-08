"""Unit tests for brand domain behavior."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import uuid

import pytest

from organizeg3_api.domain.brand.entity import (
    Brand,
)


def create_brand() -> Brand:
    """Create one valid brand for domain tests."""

    return Brand.create(
        tenant_id=uuid.uuid4(),
        code="MARCA-001",
        name="Duratex",
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
            tenant_id=uuid.UUID(
                int=0
            ),
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


def test_rejects_null_brand_id_uuid() -> None:
    with pytest.raises(
        ValueError,
        match="UUID nulo",
    ):
        Brand(
            id=uuid.UUID(
                int=0
            ),
            tenant_id=uuid.uuid4(),
            code="MARCA-001",
            name="Duratex",
        )


def test_rejects_invalid_brand_id_type() -> None:
    with pytest.raises(
        TypeError,
        match="identificador",
    ):
        Brand(  # type: ignore[arg-type]
            id="brand-id",
            tenant_id=uuid.uuid4(),
            code="MARCA-001",
            name="Duratex",
        )


def test_updates_brand_details_atomically() -> None:
    brand = create_brand()

    previous_updated_at = brand.updated_at

    brand.update_details(
        code=" marca-002 ",
        name="  Arauco  ",
    )

    assert brand.code == "MARCA-002"
    assert brand.name == "Arauco"
    assert brand.updated_at is not None

    if previous_updated_at is not None:
        assert (
            brand.updated_at
            > previous_updated_at
        )


def test_invalid_update_does_not_partially_modify_brand() -> None:
    brand = create_brand()

    original_code = brand.code
    original_name = brand.name
    original_updated_at = brand.updated_at

    with pytest.raises(
        ValueError
    ):
        brand.update_details(
            code="MARCA-002",
            name="   ",
        )

    assert brand.code == original_code
    assert brand.name == original_name
    assert (
        brand.updated_at
        == original_updated_at
    )


def test_update_timestamp_is_strictly_monotonic() -> None:
    brand = create_brand()

    future = datetime.now(
        UTC
    ) + timedelta(
        days=1
    )

    brand.updated_at = future

    brand.update_details(
        code="MARCA-002",
        name="Arauco",
    )

    assert brand.updated_at is not None
    assert brand.updated_at > future


def test_deactivates_brand() -> None:
    brand = create_brand()

    previous_updated_at = brand.updated_at

    brand.deactivate()

    assert brand.is_active is False
    assert brand.updated_at is not None

    if previous_updated_at is not None:
        assert (
            brand.updated_at
            > previous_updated_at
        )


def test_deactivate_is_idempotent() -> None:
    brand = create_brand()

    brand.deactivate()

    first_updated_at = brand.updated_at

    brand.deactivate()

    assert brand.is_active is False
    assert brand.updated_at == first_updated_at


def test_reactivates_brand() -> None:
    brand = create_brand()

    brand.deactivate()

    previous_updated_at = brand.updated_at

    brand.activate()

    assert brand.is_active is True
    assert brand.updated_at is not None

    if previous_updated_at is not None:
        assert (
            brand.updated_at
            > previous_updated_at
        )


def test_activate_is_idempotent() -> None:
    brand = create_brand()

    original_updated_at = brand.updated_at

    brand.activate()

    assert brand.is_active is True
    assert brand.updated_at == original_updated_at


def test_lifecycle_timestamp_is_strictly_monotonic() -> None:
    brand = create_brand()

    future = datetime.now(
        UTC
    ) + timedelta(
        days=1
    )

    brand.updated_at = future

    brand.deactivate()

    assert brand.updated_at is not None
    assert brand.updated_at > future
