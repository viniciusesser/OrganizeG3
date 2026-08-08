"""Inventory repository contracts."""

from __future__ import annotations

from typing import Protocol
import uuid

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


class InventoryLocationRepository(Protocol):
    """Persistence contract for inventory locations."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        location_id: uuid.UUID,
    ) -> InventoryLocation | None:
        ...

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> InventoryLocation | None:
        ...

    def add(
        self,
        location: InventoryLocation,
    ) -> InventoryLocation:
        ...


class InventoryBalanceRepository(Protocol):
    """Persistence contract for inventory balances."""

    def get_for_material_at_location(
        self,
        *,
        tenant_id: uuid.UUID,
        location_id: uuid.UUID,
        material_id: uuid.UUID,
    ) -> InventoryBalance | None:
        ...

    def add(
        self,
        balance: InventoryBalance,
    ) -> InventoryBalance:
        ...


class InventoryMovementRepository(Protocol):
    """Persistence contract for immutable inventory movements."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        movement_id: uuid.UUID,
    ) -> InventoryMovement | None:
        ...

    def add(
        self,
        movement: InventoryMovement,
    ) -> InventoryMovement:
        ...


class InventoryReservationRepository(Protocol):
    """Persistence contract for inventory reservations."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        reservation_id: uuid.UUID,
    ) -> InventoryReservation | None:
        ...

    def add(
        self,
        reservation: InventoryReservation,
    ) -> InventoryReservation:
        ...
