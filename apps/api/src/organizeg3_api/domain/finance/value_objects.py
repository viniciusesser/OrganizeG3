"""Value objects and normalization rules for Finance."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from enum import StrEnum

CODE_MAX_LENGTH = 100
CURRENCY_CODE_LENGTH = 3
MONEY_QUANTUM = Decimal("0.000001")


class FinancialAccountType(StrEnum):
    """Physical or logical location where money is held."""

    CASH = "CASH"
    BANK = "BANK"
    CARD_CLEARING = "CARD_CLEARING"
    OTHER = "OTHER"


class FinancialEntryType(StrEnum):
    """Commercial direction of a financial title."""

    RECEIVABLE = "RECEIVABLE"
    PAYABLE = "PAYABLE"


class FinancialEntryStatus(StrEnum):
    """Settlement lifecycle of a financial title."""

    OPEN = "OPEN"
    PARTIALLY_SETTLED = "PARTIALLY_SETTLED"
    SETTLED = "SETTLED"
    CANCELLED = "CANCELLED"


class FinancialTransactionType(StrEnum):
    """Direction of an actual movement of money."""

    INFLOW = "INFLOW"
    OUTFLOW = "OUTFLOW"


class FinancialTransactionStatus(StrEnum):
    """Lifecycle of an actual financial transaction."""

    POSTED = "POSTED"
    CANCELLED = "CANCELLED"


def normalize_code(
    value: str,
) -> str:
    """Normalize a business code."""

    normalized = value.strip().upper()

    if not normalized:
        raise ValueError(
            "Code cannot be blank."
        )

    if len(normalized) > CODE_MAX_LENGTH:
        raise ValueError(
            "Code cannot exceed "
            f"{CODE_MAX_LENGTH} characters."
        )

    return normalized


def normalize_required_text(
    value: str,
    *,
    field_name: str,
    max_length: int,
) -> str:
    """Normalize required text."""

    normalized = value.strip()

    if not normalized:
        raise ValueError(
            f"{field_name} cannot be blank."
        )

    if len(normalized) > max_length:
        raise ValueError(
            f"{field_name} cannot exceed "
            f"{max_length} characters."
        )

    return normalized


def normalize_optional_text(
    value: str | None,
    *,
    field_name: str,
    max_length: int,
) -> str | None:
    """Normalize optional text."""

    if value is None:
        return None

    normalized = value.strip()

    if not normalized:
        return None

    if len(normalized) > max_length:
        raise ValueError(
            f"{field_name} cannot exceed "
            f"{max_length} characters."
        )

    return normalized


def normalize_currency(
    value: str,
) -> str:
    """Normalize an ISO-style currency code."""

    normalized = value.strip().upper()

    if len(normalized) != CURRENCY_CODE_LENGTH:
        raise ValueError(
            "Currency must contain exactly "
            f"{CURRENCY_CODE_LENGTH} characters."
        )

    if not normalized.isalpha():
        raise ValueError(
            "Currency must contain letters only."
        )

    return normalized


def normalize_money(
    value: Decimal | int | str,
    *,
    allow_zero: bool = True,
) -> Decimal:
    """Normalize a monetary amount without binary floating point."""

    if isinstance(
        value,
        bool,
    ):
        raise TypeError(
            "Money cannot be boolean."
        )

    try:
        amount = Decimal(
            str(value)
        ).quantize(
            MONEY_QUANTUM
        )
    except (
        InvalidOperation,
        ValueError,
    ) as exc:
        raise ValueError(
            "Invalid monetary amount."
        ) from exc

    if not amount.is_finite():
        raise ValueError(
            "Money must be finite."
        )

    if amount < 0:
        raise ValueError(
            "Money cannot be negative."
        )

    if (
        not allow_zero
        and amount == 0
    ):
        raise ValueError(
            "Money must be greater than zero."
        )

    return amount


def ensure_utc_datetime(
    value: datetime,
) -> datetime:
    """Return an aware UTC datetime."""

    if value.tzinfo is None:
        raise ValueError(
            "Datetime must be timezone-aware."
        )

    return value.astimezone(
        UTC
    )
