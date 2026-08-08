"""Financial transaction and allocation domain entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import uuid

from organizeg3_api.domain.finance.entry import (
    FinancialEntry,
)
from organizeg3_api.domain.finance.value_objects import (
    FinancialEntryStatus,
    FinancialEntryType,
    FinancialTransactionStatus,
    FinancialTransactionType,
    ensure_utc_datetime,
    normalize_money,
    normalize_optional_text,
    normalize_required_text,
)


@dataclass(
    slots=True,
)
class FinancialTransaction:
    """An actual movement of money."""

    id: uuid.UUID
    tenant_id: uuid.UUID
    account_id: uuid.UUID
    transaction_type: FinancialTransactionType
    amount: Decimal
    occurred_at: datetime
    description: str

    status: FinancialTransactionStatus = (
        FinancialTransactionStatus.POSTED
    )

    payment_method: str | None = None
    notes: str | None = None
    cancelled_at: datetime | None = None

    def __post_init__(
        self,
    ) -> None:
        """Validate and normalize transaction data."""

        self.amount = normalize_money(
            self.amount,
            allow_zero=False,
        )

        self.occurred_at = ensure_utc_datetime(
            self.occurred_at
        )

        self.description = normalize_required_text(
            self.description,
            field_name="Description",
            max_length=2000,
        )

        self.payment_method = (
            normalize_optional_text(
                self.payment_method,
                field_name="Payment method",
                max_length=255,
            )
        )

        self.notes = normalize_optional_text(
            self.notes,
            field_name="Notes",
            max_length=4000,
        )

        if self.cancelled_at is not None:
            self.cancelled_at = (
                ensure_utc_datetime(
                    self.cancelled_at
                )
            )

        if (
            self.status
            == FinancialTransactionStatus.CANCELLED
            and self.cancelled_at is None
        ):
            raise ValueError(
                "Cancelled transaction requires "
                "cancelled_at."
            )

    def cancel(
        self,
        *,
        at: datetime,
    ) -> None:
        """Cancel an existing posted movement."""

        if (
            self.status
            == FinancialTransactionStatus.CANCELLED
        ):
            raise ValueError(
                "Transaction is already cancelled."
            )

        self.status = (
            FinancialTransactionStatus.CANCELLED
        )

        self.cancelled_at = ensure_utc_datetime(
            at
        )


@dataclass(
    slots=True,
)
class FinancialAllocation:
    """Allocation of a real movement against a title."""

    id: uuid.UUID
    tenant_id: uuid.UUID
    transaction_id: uuid.UUID
    entry_id: uuid.UUID
    amount: Decimal

    def __post_init__(
        self,
    ) -> None:
        """Validate allocation amount."""

        self.amount = normalize_money(
            self.amount,
            allow_zero=False,
        )


def validate_financial_allocation(
    *,
    entry: FinancialEntry,
    transaction: FinancialTransaction,
    allocation: FinancialAllocation,
    outstanding_amount: Decimal | int | str,
) -> None:
    """Validate an allocation across financial aggregates."""

    if (
        entry.tenant_id
        != transaction.tenant_id
        or entry.tenant_id
        != allocation.tenant_id
    ):
        raise ValueError(
            "Financial allocation cannot "
            "cross tenants."
        )

    if (
        allocation.entry_id
        != entry.id
    ):
        raise ValueError(
            "Allocation entry does not match."
        )

    if (
        allocation.transaction_id
        != transaction.id
    ):
        raise ValueError(
            "Allocation transaction "
            "does not match."
        )

    if (
        transaction.status
        != FinancialTransactionStatus.POSTED
    ):
        raise ValueError(
            "Allocation requires a posted "
            "transaction."
        )

    if (
        entry.status
        == FinancialEntryStatus.CANCELLED
    ):
        raise ValueError(
            "Cancelled entry cannot receive "
            "allocations."
        )

    if (
        entry.entry_type
        == FinancialEntryType.RECEIVABLE
        and transaction.transaction_type
        != FinancialTransactionType.INFLOW
    ):
        raise ValueError(
            "Receivable must be settled "
            "by an inflow."
        )

    if (
        entry.entry_type
        == FinancialEntryType.PAYABLE
        and transaction.transaction_type
        != FinancialTransactionType.OUTFLOW
    ):
        raise ValueError(
            "Payable must be settled "
            "by an outflow."
        )

    outstanding = normalize_money(
        outstanding_amount
    )

    if allocation.amount > outstanding:
        raise ValueError(
            "Allocation cannot exceed "
            "outstanding amount."
        )

    if allocation.amount > transaction.amount:
        raise ValueError(
            "Allocation cannot exceed "
            "transaction amount."
        )
