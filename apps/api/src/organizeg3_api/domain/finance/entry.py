"""Financial entry domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
import uuid

from organizeg3_api.domain.finance.value_objects import (
    FinancialEntryStatus,
    FinancialEntryType,
    ensure_utc_datetime,
    normalize_code,
    normalize_money,
    normalize_optional_text,
    normalize_required_text,
)


@dataclass(
    slots=True,
)
class FinancialEntry:
    """A receivable or payable financial title."""

    id: uuid.UUID
    tenant_id: uuid.UUID
    code: str
    entry_type: FinancialEntryType
    description: str
    amount: Decimal
    issue_date: date
    due_date: date

    status: FinancialEntryStatus = (
        FinancialEntryStatus.OPEN
    )

    branch_id: uuid.UUID | None = None

    customer_id: int | None = None
    supplier_id: uuid.UUID | None = None
    employee_id: uuid.UUID | None = None

    sales_order_id: uuid.UUID | None = None
    purchase_order_id: uuid.UUID | None = None

    category: str | None = None
    notes: str | None = None

    settled_at: datetime | None = None
    cancelled_at: datetime | None = None

    def __post_init__(
        self,
    ) -> None:
        """Validate and normalize financial title data."""

        self.code = normalize_code(
            self.code
        )

        self.description = normalize_required_text(
            self.description,
            field_name="Description",
            max_length=2000,
        )

        self.amount = normalize_money(
            self.amount,
            allow_zero=False,
        )

        self.category = normalize_optional_text(
            self.category,
            field_name="Category",
            max_length=255,
        )

        self.notes = normalize_optional_text(
            self.notes,
            field_name="Notes",
            max_length=4000,
        )

        if self.due_date < self.issue_date:
            raise ValueError(
                "Due date cannot be before "
                "issue date."
            )

        if (
            self.customer_id is not None
            and self.customer_id <= 0
        ):
            raise ValueError(
                "Customer ID must be positive."
            )

        self._validate_business_direction()

        if self.settled_at is not None:
            self.settled_at = ensure_utc_datetime(
                self.settled_at
            )

        if self.cancelled_at is not None:
            self.cancelled_at = (
                ensure_utc_datetime(
                    self.cancelled_at
                )
            )

        self._validate_status_state()

    def _validate_business_direction(
        self,
    ) -> None:
        """Validate source references against entry direction."""

        if (
            self.entry_type
            == FinancialEntryType.RECEIVABLE
        ):
            if self.supplier_id is not None:
                raise ValueError(
                    "Receivable cannot reference "
                    "a supplier."
                )

            if self.purchase_order_id is not None:
                raise ValueError(
                    "Receivable cannot reference "
                    "a purchase order."
                )

            if self.employee_id is not None:
                raise ValueError(
                    "Receivable cannot reference "
                    "an employee."
                )

        if (
            self.entry_type
            == FinancialEntryType.PAYABLE
        ):
            if self.customer_id is not None:
                raise ValueError(
                    "Payable cannot reference "
                    "a customer."
                )

            if self.sales_order_id is not None:
                raise ValueError(
                    "Payable cannot reference "
                    "a sales order."
                )

    def _validate_status_state(
        self,
    ) -> None:
        """Ensure lifecycle timestamps agree with status."""

        if (
            self.status
            == FinancialEntryStatus.SETTLED
            and self.settled_at is None
        ):
            raise ValueError(
                "Settled entry requires "
                "settled_at."
            )

        if (
            self.status
            == FinancialEntryStatus.CANCELLED
            and self.cancelled_at is None
        ):
            raise ValueError(
                "Cancelled entry requires "
                "cancelled_at."
            )

    def reconcile_settlement(
        self,
        allocated_amount: Decimal | int | str,
        *,
        at: datetime,
    ) -> None:
        """Reconcile status from the total valid allocations."""

        if (
            self.status
            == FinancialEntryStatus.CANCELLED
        ):
            raise ValueError(
                "Cancelled entry cannot "
                "be settled."
            )

        allocated = normalize_money(
            allocated_amount
        )

        if allocated > self.amount:
            raise ValueError(
                "Allocated amount cannot exceed "
                "entry amount."
            )

        if allocated == 0:
            self.status = (
                FinancialEntryStatus.OPEN
            )
            self.settled_at = None
            return

        if allocated < self.amount:
            self.status = (
                FinancialEntryStatus
                .PARTIALLY_SETTLED
            )
            self.settled_at = None
            return

        self.status = (
            FinancialEntryStatus.SETTLED
        )

        self.settled_at = ensure_utc_datetime(
            at
        )

    def cancel(
        self,
        *,
        at: datetime,
    ) -> None:
        """Cancel an unsettled financial title."""

        if (
            self.status
            == FinancialEntryStatus.SETTLED
        ):
            raise ValueError(
                "Settled entry cannot "
                "be cancelled."
            )

        if (
            self.status
            == FinancialEntryStatus.CANCELLED
        ):
            raise ValueError(
                "Entry is already cancelled."
            )

        self.status = (
            FinancialEntryStatus.CANCELLED
        )

        self.cancelled_at = ensure_utc_datetime(
            at
        )

        self.settled_at = None
