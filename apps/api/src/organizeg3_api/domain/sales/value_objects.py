"""Value objects and normalization helpers for sales."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from enum import StrEnum


class SalesQuoteStatus(StrEnum):
    """Lifecycle states for a commercial quote."""

    DRAFT = "DRAFT"
    SENT = "SENT"
    NEGOTIATION = "NEGOTIATION"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class SalesOrderStatus(StrEnum):
    """Lifecycle states for a confirmed sales order."""

    OPEN = "OPEN"
    IN_PRODUCTION = "IN_PRODUCTION"
    READY_FOR_DELIVERY = "READY_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"


def normalize_sales_code(value: str) -> str:
    """Normalize a quote or sales order code."""

    normalized = value.strip().upper()

    if not normalized:
        raise ValueError(
            "O código comercial não pode ficar vazio."
        )

    return normalized


def normalize_required_text(
    value: str,
    *,
    field_name: str,
) -> str:
    """Normalize required human-readable text."""

    normalized = value.strip()

    if not normalized:
        raise ValueError(
            f"{field_name} não pode ficar vazio."
        )

    return normalized


def normalize_optional_text(
    value: str | None,
) -> str | None:
    """Normalize optional text, collapsing blanks to None."""

    if value is None:
        return None

    normalized = value.strip()

    if not normalized:
        return None

    return normalized


def normalize_quantity(
    value: Decimal | int | str,
) -> Decimal:
    """Normalize a strictly positive quantity."""

    normalized = _to_decimal(
        value,
        field_name="A quantidade",
    )

    if normalized <= 0:
        raise ValueError(
            "A quantidade deve ser maior que zero."
        )

    return normalized


def normalize_money(
    value: Decimal | int | str,
    *,
    field_name: str,
    allow_zero: bool = True,
) -> Decimal:
    """Normalize a non-negative monetary value."""

    normalized = _to_decimal(
        value,
        field_name=field_name,
    )

    if normalized < 0:
        raise ValueError(
            f"{field_name} não pode ser negativo."
        )

    if not allow_zero and normalized == 0:
        raise ValueError(
            f"{field_name} deve ser maior que zero."
        )

    return normalized


def _to_decimal(
    value: Decimal | int | str,
    *,
    field_name: str,
) -> Decimal:
    try:
        normalized = Decimal(str(value))
    except (
        InvalidOperation,
        ValueError,
        TypeError,
    ) as exc:
        raise ValueError(
            f"{field_name} deve ser numérico."
        ) from exc

    if not normalized.is_finite():
        raise ValueError(
            f"{field_name} deve ser um valor finito."
        )

    return normalized
