"""Inventory movement domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
import uuid

from organizeg3_api.domain.inventory.value_objects import (
    InventoryMovementType,
    normalize_optional_text,
    normalize_quantity,
)


@dataclass(slots=True)
class InventoryMovement:
    """Represent an immutable physical inventory movement."""

    tenant_id: uuid.UUID
    material_id: uuid.UUID
    movement_type: InventoryMovementType
    quantity: Decimal
    occurred_at: datetime

    source_location_id: uuid.UUID | None = None
    destination_location_id: uuid.UUID | None = None

    reference_type: str | None = None
    reference_id: uuid.UUID | None = None
    notes: str | None = None

    id: uuid.UUID | None = None
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_uuid(
            self.tenant_id,
            "tenant",
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

        if self.source_location_id is not None:
            self._validate_uuid(
                self.source_location_id,
                "local de origem",
            )

        if self.destination_location_id is not None:
            self._validate_uuid(
                self.destination_location_id,
                "local de destino",
            )

        if self.reference_id is not None:
            self._validate_uuid(
                self.reference_id,
                "referência",
            )

        if not isinstance(
            self.movement_type,
            InventoryMovementType,
        ):
            raise TypeError(
                "O tipo deve ser InventoryMovementType."
            )

        self.quantity = normalize_quantity(
            self.quantity
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

        self._validate_locations()

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        material_id: uuid.UUID,
        movement_type: InventoryMovementType,
        quantity: Decimal | int | str,
        source_location_id: uuid.UUID | None = None,
        destination_location_id: uuid.UUID | None = None,
        reference_type: str | None = None,
        reference_id: uuid.UUID | None = None,
        notes: str | None = None,
        occurred_at: datetime | None = None,
    ) -> InventoryMovement:
        """Create an immutable inventory movement."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            material_id=material_id,
            movement_type=movement_type,
            quantity=normalize_quantity(
                quantity
            ),
            source_location_id=source_location_id,
            destination_location_id=destination_location_id,
            reference_type=reference_type,
            reference_id=reference_id,
            notes=notes,
            occurred_at=occurred_at or now,
            created_at=now,
        )

    def _validate_locations(self) -> None:
        incoming = {
            InventoryMovementType.RECEIPT,
            InventoryMovementType.ADJUSTMENT_IN,
            InventoryMovementType.RETURN_IN,
        }

        outgoing = {
            InventoryMovementType.ISSUE,
            InventoryMovementType.ADJUSTMENT_OUT,
            InventoryMovementType.RETURN_OUT,
        }

        if self.movement_type in incoming:
            if self.destination_location_id is None:
                raise ValueError(
                    "Movimento de entrada exige local de destino."
                )

            if self.source_location_id is not None:
                raise ValueError(
                    "Movimento de entrada não deve informar "
                    "local de origem."
                )

            return

        if self.movement_type in outgoing:
            if self.source_location_id is None:
                raise ValueError(
                    "Movimento de saída exige local de origem."
                )

            if self.destination_location_id is not None:
                raise ValueError(
                    "Movimento de saída não deve informar "
                    "local de destino."
                )

            return

        if self.movement_type is InventoryMovementType.TRANSFER:
            if (
                self.source_location_id is None
                or self.destination_location_id is None
            ):
                raise ValueError(
                    "Transferência exige origem e destino."
                )

            if (
                self.source_location_id
                == self.destination_location_id
            ):
                raise ValueError(
                    "Origem e destino da transferência "
                    "devem ser diferentes."
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
