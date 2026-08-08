"""Inventory balance domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
import uuid

from organizeg3_api.domain.inventory.value_objects import (
    normalize_quantity,
)


@dataclass(slots=True)
class InventoryBalance:
    """Represent the current material balance at one location."""

    tenant_id: uuid.UUID
    location_id: uuid.UUID
    material_id: uuid.UUID

    on_hand_quantity: Decimal = Decimal("0")
    reserved_quantity: Decimal = Decimal("0")

    id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_uuid(
            self.tenant_id,
            "tenant",
        )
        self._validate_uuid(
            self.location_id,
            "local",
        )
        self._validate_uuid(
            self.material_id,
            "material",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                "identificador",
            )

        self.on_hand_quantity = normalize_quantity(
            self.on_hand_quantity,
            allow_zero=True,
        )

        self.reserved_quantity = normalize_quantity(
            self.reserved_quantity,
            allow_zero=True,
        )

        self._validate_reserved_quantity()

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        location_id: uuid.UUID,
        material_id: uuid.UUID,
    ) -> InventoryBalance:
        """Create an empty inventory balance."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            location_id=location_id,
            material_id=material_id,
            on_hand_quantity=Decimal("0"),
            reserved_quantity=Decimal("0"),
            created_at=now,
            updated_at=now,
        )

    @property
    def available_quantity(self) -> Decimal:
        """Return physically available quantity."""

        return (
            self.on_hand_quantity
            - self.reserved_quantity
        )

    def receive(
        self,
        quantity: Decimal | int | str,
    ) -> None:
        """Increase physical stock."""

        normalized = normalize_quantity(
            quantity
        )

        self.on_hand_quantity += normalized
        self._touch()

    def issue(
        self,
        quantity: Decimal | int | str,
    ) -> None:
        """Decrease physical stock."""

        normalized = normalize_quantity(
            quantity
        )

        if normalized > self.available_quantity:
            raise ValueError(
                "Saldo disponível insuficiente."
            )

        self.on_hand_quantity -= normalized
        self._touch()

    def reserve(
        self,
        quantity: Decimal | int | str,
    ) -> None:
        """Reserve available stock."""

        normalized = normalize_quantity(
            quantity
        )

        if normalized > self.available_quantity:
            raise ValueError(
                "Saldo disponível insuficiente para reserva."
            )

        self.reserved_quantity += normalized
        self._touch()

    def release_reservation(
        self,
        quantity: Decimal | int | str,
    ) -> None:
        """Release previously reserved stock."""

        normalized = normalize_quantity(
            quantity
        )

        if normalized > self.reserved_quantity:
            raise ValueError(
                "A liberação excede a quantidade reservada."
            )

        self.reserved_quantity -= normalized
        self._touch()

    def consume_reserved(
        self,
        quantity: Decimal | int | str,
    ) -> None:
        """Consume stock that had already been reserved."""

        normalized = normalize_quantity(
            quantity
        )

        if normalized > self.reserved_quantity:
            raise ValueError(
                "O consumo excede a quantidade reservada."
            )

        if normalized > self.on_hand_quantity:
            raise ValueError(
                "Saldo físico insuficiente."
            )

        self.reserved_quantity -= normalized
        self.on_hand_quantity -= normalized
        self._touch()

    def adjust(
        self,
        new_quantity: Decimal | int | str,
    ) -> None:
        """Set physical quantity after an inventory count."""

        normalized = normalize_quantity(
            new_quantity,
            allow_zero=True,
        )

        if normalized < self.reserved_quantity:
            raise ValueError(
                "O saldo físico não pode ficar abaixo do reservado."
            )

        self.on_hand_quantity = normalized
        self._touch()

    def _validate_reserved_quantity(self) -> None:
        if (
            self.reserved_quantity
            > self.on_hand_quantity
        ):
            raise ValueError(
                "A quantidade reservada não pode exceder "
                "o saldo físico."
            )

    @staticmethod
    def _validate_uuid(
        value: object,
        field_name: str,
    ) -> None:
        if not isinstance(
            value,
            uuid.UUID,
        ):
            raise TypeError(
                f"O {field_name} deve ser um UUID."
            )

        if value.int == 0:
            raise ValueError(
                f"O {field_name} não pode possuir UUID nulo."
            )

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)
