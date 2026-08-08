"""Inventory domain value objects."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from enum import StrEnum


class InventoryLocationType(StrEnum):
    """Describe the operational purpose of an inventory location."""

    WAREHOUSE = "WAREHOUSE"
    PRODUCTION = "PRODUCTION"
    CUTTING = "CUTTING"
    RECEIVING = "RECEIVING"
    SHIPPING = "SHIPPING"
    OTHER = "OTHER"


class InventoryMovementType(StrEnum):
    """Describe physical inventory movements."""

    RECEIPT = "RECEIPT"
    ISSUE = "ISSUE"
    TRANSFER = "TRANSFER"
    ADJUSTMENT_IN = "ADJUSTMENT_IN"
    ADJUSTMENT_OUT = "ADJUSTMENT_OUT"
    RETURN_IN = "RETURN_IN"
    RETURN_OUT = "RETURN_OUT"


class InventoryReservationStatus(StrEnum):
    """Describe an inventory reservation lifecycle."""

    ACTIVE = "ACTIVE"
    PARTIALLY_CONSUMED = "PARTIALLY_CONSUMED"
    CONSUMED = "CONSUMED"
    RELEASED = "RELEASED"
    CANCELLED = "CANCELLED"


def normalize_inventory_code(
    value: str,
) -> str:
    """Normalize an inventory code."""

    normalized = value.strip().upper()

    if not normalized:
        raise ValueError(
            "O código é obrigatório."
        )

    return normalized


def normalize_required_text(
    value: str,
    *,
    field_name: str,
) -> str:
    """Normalize a mandatory inventory text."""

    normalized = value.strip()

    if not normalized:
        raise ValueError(
            f"O {field_name} é obrigatório."
        )

    return normalized


def normalize_optional_text(
    value: str | None,
) -> str | None:
    """Normalize an optional inventory text."""

    if value is None:
        return None

    normalized = value.strip()

    return normalized or None


def normalize_quantity(
    value: Decimal | int | str,
    *,
    allow_zero: bool = False,
) -> Decimal:
    """Normalize a non-negative or positive inventory quantity."""

    try:
        quantity = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(
            "A quantidade informada é inválida."
        ) from exc

    if not quantity.is_finite():
        raise ValueError(
            "A quantidade deve ser finita."
        )

    if allow_zero:
        if quantity < 0:
            raise ValueError(
                "A quantidade não pode ser negativa."
            )
    elif quantity <= 0:
        raise ValueError(
            "A quantidade deve ser maior que zero."
        )

    return quantity
