"""Purchasing domain value objects."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from enum import StrEnum


class PurchaseOrderStatus(StrEnum):
    """Represent the lifecycle of a purchase order."""

    DRAFT = "DRAFT"
    ISSUED = "ISSUED"
    PARTIALLY_RECEIVED = "PARTIALLY_RECEIVED"
    RECEIVED = "RECEIVED"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"


class PurchaseReceiptStatus(StrEnum):
    """Represent the lifecycle of a purchase receipt."""

    DRAFT = "DRAFT"
    POSTED = "POSTED"
    CANCELLED = "CANCELLED"


def normalize_purchase_code(
    value: str,
) -> str:
    """Normalize a purchase document code."""

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
    """Normalize required purchasing text."""

    normalized = value.strip()

    if not normalized:
        raise ValueError(
            f"O {field_name} é obrigatório."
        )

    return normalized


def normalize_optional_text(
    value: str | None,
) -> str | None:
    """Normalize optional purchasing text."""

    if value is None:
        return None

    normalized = value.strip()

    return normalized or None


def normalize_quantity(
    value: Decimal | int | str,
    *,
    allow_zero: bool = False,
) -> Decimal:
    """Normalize a purchasing quantity."""

    try:
        quantity = Decimal(
            str(value)
        )
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


def normalize_money(
    value: Decimal | int | str,
) -> Decimal:
    """Normalize a non-negative monetary value."""

    try:
        amount = Decimal(
            str(value)
        )
    except InvalidOperation as exc:
        raise ValueError(
            "O valor monetário informado é inválido."
        ) from exc

    if not amount.is_finite():
        raise ValueError(
            "O valor monetário deve ser finito."
        )

    if amount < 0:
        raise ValueError(
            "O valor monetário não pode ser negativo."
        )

    return amount
