"""Unit tests for the Finance domain."""

from datetime import UTC, date, datetime
from decimal import Decimal
import uuid

import pytest

from organizeg3_api.domain.finance import (
    FinancialAccount,
    FinancialAccountType,
    FinancialAllocation,
    FinancialEntry,
    FinancialEntryStatus,
    FinancialEntryType,
    FinancialTransaction,
    FinancialTransactionStatus,
    FinancialTransactionType,
    validate_financial_allocation,
)

TENANT_ID = uuid.uuid4()
ACCOUNT_ID = uuid.uuid4()


def utc_now() -> datetime:
    """Return a deterministic aware datetime for tests."""

    return datetime(
        2026,
        8,
        8,
        12,
        0,
        tzinfo=UTC,
    )


def make_receivable(
    **overrides: object,
) -> FinancialEntry:
    """Create a valid receivable for tests."""

    values: dict[str, object] = {
        "id": uuid.uuid4(),
        "tenant_id": TENANT_ID,
        "code": "REC-0001",
        "entry_type": (
            FinancialEntryType.RECEIVABLE
        ),
        "description": "Venda planejada",
        "amount": Decimal("5000"),
        "issue_date": date(
            2026,
            8,
            8,
        ),
        "due_date": date(
            2026,
            8,
            20,
        ),
        "customer_id": 1,
        "sales_order_id": uuid.uuid4(),
    }

    values.update(
        overrides
    )

    return FinancialEntry(
        **values,  # type: ignore[arg-type]
    )


def make_payable(
    **overrides: object,
) -> FinancialEntry:
    """Create a valid payable for tests."""

    values: dict[str, object] = {
        "id": uuid.uuid4(),
        "tenant_id": TENANT_ID,
        "code": "PAY-0001",
        "entry_type": (
            FinancialEntryType.PAYABLE
        ),
        "description": "Compra de MDF",
        "amount": Decimal("1250"),
        "issue_date": date(
            2026,
            8,
            8,
        ),
        "due_date": date(
            2026,
            8,
            15,
        ),
        "supplier_id": uuid.uuid4(),
        "purchase_order_id": uuid.uuid4(),
    }

    values.update(
        overrides
    )

    return FinancialEntry(
        **values,  # type: ignore[arg-type]
    )


def make_transaction(
    *,
    transaction_type: FinancialTransactionType,
    amount: Decimal = Decimal("1000"),
    tenant_id: uuid.UUID = TENANT_ID,
) -> FinancialTransaction:
    """Create a valid transaction for tests."""

    return FinancialTransaction(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        account_id=ACCOUNT_ID,
        transaction_type=transaction_type,
        amount=amount,
        occurred_at=utc_now(),
        description="Movimentação financeira",
    )


def test_creates_financial_account() -> None:
    account = FinancialAccount(
        id=ACCOUNT_ID,
        tenant_id=TENANT_ID,
        code=" banco-01 ",
        name=" Conta principal ",
        account_type=FinancialAccountType.BANK,
    )

    assert account.code == "BANCO-01"
    assert account.name == "Conta principal"
    assert account.currency == "BRL"
    assert account.is_active is True


def test_financial_account_can_be_deactivated() -> None:
    account = FinancialAccount(
        id=ACCOUNT_ID,
        tenant_id=TENANT_ID,
        code="CX-01",
        name="Caixa",
        account_type=FinancialAccountType.CASH,
    )

    account.deactivate()

    assert account.is_active is False

    account.activate()

    assert account.is_active is True


def test_account_rejects_blank_name() -> None:
    with pytest.raises(
        ValueError,
        match="Account name cannot be blank",
    ):
        FinancialAccount(
            id=ACCOUNT_ID,
            tenant_id=TENANT_ID,
            code="CX-01",
            name="   ",
            account_type=FinancialAccountType.CASH,
        )


def test_account_rejects_invalid_currency() -> None:
    with pytest.raises(
        ValueError,
        match="Currency",
    ):
        FinancialAccount(
            id=ACCOUNT_ID,
            tenant_id=TENANT_ID,
            code="CX-01",
            name="Caixa",
            account_type=FinancialAccountType.CASH,
            currency="REAL",
        )


def test_creates_receivable() -> None:
    entry = make_receivable()

    assert (
        entry.entry_type
        == FinancialEntryType.RECEIVABLE
    )
    assert (
        entry.status
        == FinancialEntryStatus.OPEN
    )
    assert entry.amount == Decimal(
        "5000.000000"
    )


def test_creates_payable() -> None:
    entry = make_payable()

    assert (
        entry.entry_type
        == FinancialEntryType.PAYABLE
    )
    assert (
        entry.status
        == FinancialEntryStatus.OPEN
    )


def test_entry_rejects_zero_amount() -> None:
    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        make_receivable(
            amount=Decimal("0"),
        )


def test_entry_rejects_due_date_before_issue_date() -> None:
    with pytest.raises(
        ValueError,
        match="Due date",
    ):
        make_receivable(
            due_date=date(
                2026,
                8,
                7,
            ),
        )


def test_receivable_rejects_supplier() -> None:
    with pytest.raises(
        ValueError,
        match="supplier",
    ):
        make_receivable(
            supplier_id=uuid.uuid4(),
        )


def test_receivable_rejects_purchase_order() -> None:
    with pytest.raises(
        ValueError,
        match="purchase order",
    ):
        make_receivable(
            purchase_order_id=uuid.uuid4(),
        )


def test_payable_rejects_customer() -> None:
    with pytest.raises(
        ValueError,
        match="customer",
    ):
        make_payable(
            customer_id=1,
        )


def test_payable_rejects_sales_order() -> None:
    with pytest.raises(
        ValueError,
        match="sales order",
    ):
        make_payable(
            sales_order_id=uuid.uuid4(),
        )


def test_entry_becomes_partially_settled() -> None:
    entry = make_receivable()

    entry.reconcile_settlement(
        Decimal("2500"),
        at=utc_now(),
    )

    assert (
        entry.status
        == FinancialEntryStatus.PARTIALLY_SETTLED
    )

    assert entry.settled_at is None


def test_entry_becomes_settled() -> None:
    entry = make_receivable()

    entry.reconcile_settlement(
        Decimal("5000"),
        at=utc_now(),
    )

    assert (
        entry.status
        == FinancialEntryStatus.SETTLED
    )

    assert entry.settled_at == utc_now()


def test_entry_returns_to_open_when_no_allocations() -> None:
    entry = make_receivable()

    entry.reconcile_settlement(
        Decimal("2500"),
        at=utc_now(),
    )

    entry.reconcile_settlement(
        Decimal("0"),
        at=utc_now(),
    )

    assert (
        entry.status
        == FinancialEntryStatus.OPEN
    )

    assert entry.settled_at is None


def test_entry_rejects_over_settlement() -> None:
    entry = make_receivable()

    with pytest.raises(
        ValueError,
        match="cannot exceed",
    ):
        entry.reconcile_settlement(
            Decimal("5000.01"),
            at=utc_now(),
        )


def test_open_entry_can_be_cancelled() -> None:
    entry = make_receivable()

    entry.cancel(
        at=utc_now(),
    )

    assert (
        entry.status
        == FinancialEntryStatus.CANCELLED
    )

    assert entry.cancelled_at == utc_now()


def test_settled_entry_cannot_be_cancelled() -> None:
    entry = make_receivable()

    entry.reconcile_settlement(
        entry.amount,
        at=utc_now(),
    )

    with pytest.raises(
        ValueError,
        match="Settled entry",
    ):
        entry.cancel(
            at=utc_now(),
        )


def test_creates_inflow_transaction() -> None:
    transaction = make_transaction(
        transaction_type=(
            FinancialTransactionType.INFLOW
        ),
    )

    assert transaction.amount == Decimal(
        "1000.000000"
    )

    assert (
        transaction.status
        == FinancialTransactionStatus.POSTED
    )


def test_transaction_rejects_zero_amount() -> None:
    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        make_transaction(
            transaction_type=(
                FinancialTransactionType.INFLOW
            ),
            amount=Decimal("0"),
        )


def test_transaction_can_be_cancelled() -> None:
    transaction = make_transaction(
        transaction_type=(
            FinancialTransactionType.OUTFLOW
        ),
    )

    transaction.cancel(
        at=utc_now(),
    )

    assert (
        transaction.status
        == FinancialTransactionStatus.CANCELLED
    )

    assert transaction.cancelled_at == utc_now()


def test_creates_financial_allocation() -> None:
    allocation = FinancialAllocation(
        id=uuid.uuid4(),
        tenant_id=TENANT_ID,
        transaction_id=uuid.uuid4(),
        entry_id=uuid.uuid4(),
        amount=Decimal("250"),
    )

    assert allocation.amount == Decimal(
        "250.000000"
    )


def test_receivable_accepts_inflow_allocation() -> None:
    entry = make_receivable()

    transaction = make_transaction(
        transaction_type=(
            FinancialTransactionType.INFLOW
        ),
        amount=Decimal("2500"),
    )

    allocation = FinancialAllocation(
        id=uuid.uuid4(),
        tenant_id=TENANT_ID,
        transaction_id=transaction.id,
        entry_id=entry.id,
        amount=Decimal("2500"),
    )

    validate_financial_allocation(
        entry=entry,
        transaction=transaction,
        allocation=allocation,
        outstanding_amount=entry.amount,
    )


def test_payable_accepts_outflow_allocation() -> None:
    entry = make_payable()

    transaction = make_transaction(
        transaction_type=(
            FinancialTransactionType.OUTFLOW
        ),
        amount=entry.amount,
    )

    allocation = FinancialAllocation(
        id=uuid.uuid4(),
        tenant_id=TENANT_ID,
        transaction_id=transaction.id,
        entry_id=entry.id,
        amount=entry.amount,
    )

    validate_financial_allocation(
        entry=entry,
        transaction=transaction,
        allocation=allocation,
        outstanding_amount=entry.amount,
    )


def test_receivable_rejects_outflow_allocation() -> None:
    entry = make_receivable()

    transaction = make_transaction(
        transaction_type=(
            FinancialTransactionType.OUTFLOW
        ),
    )

    allocation = FinancialAllocation(
        id=uuid.uuid4(),
        tenant_id=TENANT_ID,
        transaction_id=transaction.id,
        entry_id=entry.id,
        amount=Decimal("100"),
    )

    with pytest.raises(
        ValueError,
        match="inflow",
    ):
        validate_financial_allocation(
            entry=entry,
            transaction=transaction,
            allocation=allocation,
            outstanding_amount=entry.amount,
        )


def test_payable_rejects_inflow_allocation() -> None:
    entry = make_payable()

    transaction = make_transaction(
        transaction_type=(
            FinancialTransactionType.INFLOW
        ),
    )

    allocation = FinancialAllocation(
        id=uuid.uuid4(),
        tenant_id=TENANT_ID,
        transaction_id=transaction.id,
        entry_id=entry.id,
        amount=Decimal("100"),
    )

    with pytest.raises(
        ValueError,
        match="outflow",
    ):
        validate_financial_allocation(
            entry=entry,
            transaction=transaction,
            allocation=allocation,
            outstanding_amount=entry.amount,
        )


def test_allocation_cannot_cross_tenants() -> None:
    entry = make_receivable()

    other_tenant = uuid.uuid4()

    transaction = make_transaction(
        transaction_type=(
            FinancialTransactionType.INFLOW
        ),
        tenant_id=other_tenant,
    )

    allocation = FinancialAllocation(
        id=uuid.uuid4(),
        tenant_id=other_tenant,
        transaction_id=transaction.id,
        entry_id=entry.id,
        amount=Decimal("100"),
    )

    with pytest.raises(
        ValueError,
        match="cross tenants",
    ):
        validate_financial_allocation(
            entry=entry,
            transaction=transaction,
            allocation=allocation,
            outstanding_amount=entry.amount,
        )


def test_allocation_cannot_exceed_outstanding_amount() -> None:
    entry = make_receivable()

    transaction = make_transaction(
        transaction_type=(
            FinancialTransactionType.INFLOW
        ),
        amount=Decimal("1000"),
    )

    allocation = FinancialAllocation(
        id=uuid.uuid4(),
        tenant_id=TENANT_ID,
        transaction_id=transaction.id,
        entry_id=entry.id,
        amount=Decimal("1000"),
    )

    with pytest.raises(
        ValueError,
        match="outstanding",
    ):
        validate_financial_allocation(
            entry=entry,
            transaction=transaction,
            allocation=allocation,
            outstanding_amount=Decimal(
                "500"
            ),
        )


def test_allocation_cannot_exceed_transaction_amount() -> None:
    entry = make_receivable()

    transaction = make_transaction(
        transaction_type=(
            FinancialTransactionType.INFLOW
        ),
        amount=Decimal("500"),
    )

    allocation = FinancialAllocation(
        id=uuid.uuid4(),
        tenant_id=TENANT_ID,
        transaction_id=transaction.id,
        entry_id=entry.id,
        amount=Decimal("600"),
    )

    with pytest.raises(
        ValueError,
        match="transaction amount",
    ):
        validate_financial_allocation(
            entry=entry,
            transaction=transaction,
            allocation=allocation,
            outstanding_amount=entry.amount,
        )


def test_cancelled_transaction_cannot_be_allocated() -> None:
    entry = make_receivable()

    transaction = make_transaction(
        transaction_type=(
            FinancialTransactionType.INFLOW
        ),
    )

    transaction.cancel(
        at=utc_now(),
    )

    allocation = FinancialAllocation(
        id=uuid.uuid4(),
        tenant_id=TENANT_ID,
        transaction_id=transaction.id,
        entry_id=entry.id,
        amount=Decimal("100"),
    )

    with pytest.raises(
        ValueError,
        match="posted transaction",
    ):
        validate_financial_allocation(
            entry=entry,
            transaction=transaction,
            allocation=allocation,
            outstanding_amount=entry.amount,
        )
