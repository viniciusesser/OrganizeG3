"""Unit tests for inventory core domain."""

from __future__ import annotations

from decimal import Decimal
import uuid

import pytest

from organizeg3_api.domain.inventory.balance import (
    InventoryBalance,
)
from organizeg3_api.domain.inventory.location import (
    InventoryLocation,
)
from organizeg3_api.domain.inventory.movement import (
    InventoryMovement,
)
from organizeg3_api.domain.inventory.reservation import (
    InventoryReservation,
)
from organizeg3_api.domain.inventory.value_objects import (
    InventoryLocationType,
    InventoryMovementType,
    InventoryReservationStatus,
)


def test_creates_inventory_location() -> None:
    location = InventoryLocation.create(
        tenant_id=uuid.uuid4(),
        code=" alm-01 ",
        name=" Almoxarifado ",
        location_type=InventoryLocationType.WAREHOUSE,
    )

    assert location.id is not None
    assert location.code == "ALM-01"
    assert location.name == "Almoxarifado"
    assert location.branch_id is None
    assert location.is_active is True


def test_location_can_have_optional_branch() -> None:
    branch_id = uuid.uuid4()

    location = InventoryLocation.create(
        tenant_id=uuid.uuid4(),
        branch_id=branch_id,
        code="CORTE",
        name="Corte",
        location_type=InventoryLocationType.CUTTING,
    )

    assert location.branch_id == branch_id

    location.remove_branch()

    assert location.branch_id is None


def test_creates_empty_inventory_balance() -> None:
    balance = InventoryBalance.create(
        tenant_id=uuid.uuid4(),
        location_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
    )

    assert balance.on_hand_quantity == Decimal("0")
    assert balance.reserved_quantity == Decimal("0")
    assert balance.available_quantity == Decimal("0")


def test_balance_receives_and_issues_stock() -> None:
    balance = InventoryBalance.create(
        tenant_id=uuid.uuid4(),
        location_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
    )

    balance.receive("10.5")
    balance.issue("2.25")

    assert balance.on_hand_quantity == Decimal("8.25")
    assert balance.available_quantity == Decimal("8.25")


def test_balance_reservation_changes_available_quantity() -> None:
    balance = InventoryBalance.create(
        tenant_id=uuid.uuid4(),
        location_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
    )

    balance.receive("10")
    balance.reserve("3")

    assert balance.on_hand_quantity == Decimal("10")
    assert balance.reserved_quantity == Decimal("3")
    assert balance.available_quantity == Decimal("7")


def test_balance_consumes_reserved_stock() -> None:
    balance = InventoryBalance.create(
        tenant_id=uuid.uuid4(),
        location_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
    )

    balance.receive("10")
    balance.reserve("4")
    balance.consume_reserved("2")

    assert balance.on_hand_quantity == Decimal("8")
    assert balance.reserved_quantity == Decimal("2")
    assert balance.available_quantity == Decimal("6")


def test_rejects_issue_above_available_stock() -> None:
    balance = InventoryBalance.create(
        tenant_id=uuid.uuid4(),
        location_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
    )

    balance.receive("10")
    balance.reserve("8")

    with pytest.raises(
        ValueError,
        match="Saldo disponível insuficiente",
    ):
        balance.issue("3")


def test_rejects_balance_below_reserved_on_adjustment() -> None:
    balance = InventoryBalance.create(
        tenant_id=uuid.uuid4(),
        location_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
    )

    balance.receive("10")
    balance.reserve("6")

    with pytest.raises(
        ValueError,
        match="abaixo do reservado",
    ):
        balance.adjust("5")


def test_creates_inventory_receipt() -> None:
    destination_id = uuid.uuid4()

    movement = InventoryMovement.create(
        tenant_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
        movement_type=InventoryMovementType.RECEIPT,
        quantity="12.50",
        destination_location_id=destination_id,
        reference_type=" purchase_order ",
    )

    assert movement.id is not None
    assert movement.quantity == Decimal("12.50")
    assert movement.source_location_id is None
    assert movement.destination_location_id == destination_id
    assert movement.reference_type == "PURCHASE_ORDER"


def test_rejects_receipt_without_destination() -> None:
    with pytest.raises(
        ValueError,
        match="local de destino",
    ):
        InventoryMovement.create(
            tenant_id=uuid.uuid4(),
            material_id=uuid.uuid4(),
            movement_type=InventoryMovementType.RECEIPT,
            quantity="1",
        )


def test_creates_inventory_issue() -> None:
    source_id = uuid.uuid4()

    movement = InventoryMovement.create(
        tenant_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
        movement_type=InventoryMovementType.ISSUE,
        quantity="3",
        source_location_id=source_id,
    )

    assert movement.source_location_id == source_id
    assert movement.destination_location_id is None


def test_creates_inventory_transfer() -> None:
    source_id = uuid.uuid4()
    destination_id = uuid.uuid4()

    movement = InventoryMovement.create(
        tenant_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
        movement_type=InventoryMovementType.TRANSFER,
        quantity="5",
        source_location_id=source_id,
        destination_location_id=destination_id,
    )

    assert movement.source_location_id == source_id
    assert movement.destination_location_id == destination_id


def test_rejects_transfer_to_same_location() -> None:
    location_id = uuid.uuid4()

    with pytest.raises(
        ValueError,
        match="devem ser diferentes",
    ):
        InventoryMovement.create(
            tenant_id=uuid.uuid4(),
            material_id=uuid.uuid4(),
            movement_type=InventoryMovementType.TRANSFER,
            quantity="5",
            source_location_id=location_id,
            destination_location_id=location_id,
        )


def test_creates_inventory_reservation() -> None:
    reservation = InventoryReservation.create(
        tenant_id=uuid.uuid4(),
        location_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
        quantity="7.5",
        reference_type="production_order",
    )

    assert reservation.id is not None
    assert reservation.quantity == Decimal("7.5")
    assert reservation.consumed_quantity == Decimal("0")
    assert reservation.remaining_quantity == Decimal("7.5")
    assert (
        reservation.status
        is InventoryReservationStatus.ACTIVE
    )
    assert reservation.reference_type == "PRODUCTION_ORDER"


def test_partially_consumes_reservation() -> None:
    reservation = InventoryReservation.create(
        tenant_id=uuid.uuid4(),
        location_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
        quantity="10",
    )

    reservation.consume("4")

    assert reservation.consumed_quantity == Decimal("4")
    assert reservation.remaining_quantity == Decimal("6")
    assert (
        reservation.status
        is InventoryReservationStatus.PARTIALLY_CONSUMED
    )


def test_fully_consumes_reservation() -> None:
    reservation = InventoryReservation.create(
        tenant_id=uuid.uuid4(),
        location_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
        quantity="10",
    )

    reservation.consume("10")

    assert reservation.remaining_quantity == Decimal("0")
    assert (
        reservation.status
        is InventoryReservationStatus.CONSUMED
    )


def test_releases_reservation() -> None:
    reservation = InventoryReservation.create(
        tenant_id=uuid.uuid4(),
        location_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
        quantity="10",
    )

    reservation.release()

    assert (
        reservation.status
        is InventoryReservationStatus.RELEASED
    )


def test_rejects_consumption_above_reserved_quantity() -> None:
    reservation = InventoryReservation.create(
        tenant_id=uuid.uuid4(),
        location_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
        quantity="5",
    )

    with pytest.raises(
        ValueError,
        match="excede o saldo",
    ):
        reservation.consume("6")
