"""Inventory reservation domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
import uuid

from organizeg3_api.domain.inventory.value_objects import (
    InventoryReservationStatus,
    normalize_optional_text,
    normalize_quantity,
)


@dataclass(slots=True)
class InventoryReservation:
    """Represent stock reserved for a future business demand."""

    tenant_id: uuid.UUID
    location_id: uuid.UUID
    material_id: uuid.UUID
    quantity: Decimal
    consumed_quantity: Decimal
    status: InventoryReservationStatus

    reference_type: str | None = None
    reference_id: uuid.UUID | None = None
    notes: str | None = None

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

        if self.reference_id is not None:
            self._validate_uuid(
                self.reference_id,
                "referência",
            )

        self.quantity = normalize_quantity(
            self.quantity
        )

        self.consumed_quantity = normalize_quantity(
            self.consumed_quantity,
            allow_zero=True,
        )

        if self.consumed_quantity > self.quantity:
            raise ValueError(
                "A quantidade consumida não pode exceder "
                "a quantidade reservada."
            )

        if not isinstance(
            self.status,
            InventoryReservationStatus,
        ):
            raise TypeError(
                "O status deve ser InventoryReservationStatus."
            )

        self.reference_type = normalize_optional_text(
            self.reference_type
        )

        if self.reference_type is not None:
            self.reference_type = (
                self.reference_type.upper()
            )

        self.notes = normalize_optional_text(
            self.notes
        )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        location_id: uuid.UUID,
        material_id: uuid.UUID,
        quantity: Decimal | int | str,
        reference_type: str | None = None,
        reference_id: uuid.UUID | None = None,
        notes: str | None = None,
    ) -> InventoryReservation:
        """Create an active inventory reservation."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            location_id=location_id,
            material_id=material_id,
            quantity=normalize_quantity(
                quantity
            ),
            consumed_quantity=Decimal("0"),
            status=InventoryReservationStatus.ACTIVE,
            reference_type=reference_type,
            reference_id=reference_id,
            notes=notes,
            created_at=now,
            updated_at=now,
        )

    @property
    def remaining_quantity(self) -> Decimal:
        """Return unconsumed reserved quantity."""

        return (
            self.quantity
            - self.consumed_quantity
        )

    def consume(
        self,
        quantity: Decimal | int | str,
    ) -> None:
        """Consume part or all of the reservation."""

        if self.status not in {
            InventoryReservationStatus.ACTIVE,
            InventoryReservationStatus.PARTIALLY_CONSUMED,
        }:
            raise ValueError(
                "A reserva não está disponível para consumo."
            )

        normalized = normalize_quantity(
            quantity
        )

        if normalized > self.remaining_quantity:
            raise ValueError(
                "O consumo excede o saldo da reserva."
            )

        self.consumed_quantity += normalized

        if self.remaining_quantity == 0:
            self.status = (
                InventoryReservationStatus.CONSUMED
            )
        else:
            self.status = (
                InventoryReservationStatus.PARTIALLY_CONSUMED
            )

        self._touch()

    def release(self) -> None:
        """Release the unconsumed reservation."""

        if self.status not in {
            InventoryReservationStatus.ACTIVE,
            InventoryReservationStatus.PARTIALLY_CONSUMED,
        }:
            raise ValueError(
                "A reserva não pode ser liberada."
            )

        self.status = InventoryReservationStatus.RELEASED
        self._touch()

    def cancel(self) -> None:
        """Cancel an unused reservation."""

        if self.consumed_quantity > 0:
            raise ValueError(
                "Uma reserva parcialmente consumida "
                "não pode ser cancelada."
            )

        if self.status is not InventoryReservationStatus.ACTIVE:
            raise ValueError(
                "A reserva não pode ser cancelada."
            )

        self.status = InventoryReservationStatus.CANCELLED
        self._touch()

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
