"""SQLAlchemy ORM mappings for Finance core."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
import uuid

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from organizeg3_api.infrastructure.database.base import (
    Base,
    TenantScopedMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class FinancialAccountModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist an account where money is held or cleared."""

    __tablename__ = "financial_accounts"

    __table_args__ = (
        CheckConstraint(
            "TRIM(code) <> ''",
            name="code_not_blank",
        ),
        CheckConstraint(
            "TRIM(name) <> ''",
            name="name_not_blank",
        ),
        CheckConstraint(
            (
                "account_type IN ("
                "'CASH', "
                "'BANK', "
                "'CARD_CLEARING', "
                "'OTHER'"
                ")"
            ),
            name="account_type_valid",
        ),
        CheckConstraint(
            (
                "LENGTH(currency) = 3 "
                "AND currency = UPPER(currency)"
            ),
            name="currency_valid",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_financial_accounts_id_tenant",
        ),
        UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_financial_accounts_tenant_code",
        ),
        ForeignKeyConstraint(
            [
                "branch_id",
                "tenant_id",
            ],
            [
                "branches.id",
                "branches.tenant_id",
            ],
            name="fk_financial_accounts_branch_tenant",
        ),
        Index(
            "ix_financial_accounts_tenant_branch",
            "tenant_id",
            "branch_id",
        ),
        Index(
            "ix_financial_accounts_tenant_type",
            "tenant_id",
            "account_type",
        ),
        Index(
            "ix_financial_accounts_tenant_active",
            "tenant_id",
            "is_active",
        ),
    )

    branch_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    account_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="BRL",
        server_default=text("'BRL'"),
    )

    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
        server_default=text("true"),
    )


class FinancialEntryModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one receivable or payable financial title."""

    __tablename__ = "financial_entries"

    __table_args__ = (
        CheckConstraint(
            "TRIM(code) <> ''",
            name="code_not_blank",
        ),
        CheckConstraint(
            "TRIM(description) <> ''",
            name="description_not_blank",
        ),
        CheckConstraint(
            (
                "entry_type IN ("
                "'RECEIVABLE', "
                "'PAYABLE'"
                ")"
            ),
            name="entry_type_valid",
        ),
        CheckConstraint(
            (
                "status IN ("
                "'OPEN', "
                "'PARTIALLY_SETTLED', "
                "'SETTLED', "
                "'CANCELLED'"
                ")"
            ),
            name="status_valid",
        ),
        CheckConstraint(
            "amount > 0",
            name="amount_positive",
        ),
        CheckConstraint(
            "due_date >= issue_date",
            name="dates_valid",
        ),
        CheckConstraint(
            (
                "(status <> 'SETTLED') "
                "OR settled_at IS NOT NULL"
            ),
            name="settled_state_valid",
        ),
        CheckConstraint(
            (
                "(status <> 'CANCELLED') "
                "OR cancelled_at IS NOT NULL"
            ),
            name="cancelled_state_valid",
        ),
        CheckConstraint(
            (
                "(entry_type <> 'RECEIVABLE') "
                "OR ("
                "supplier_id IS NULL "
                "AND employee_id IS NULL "
                "AND purchase_order_id IS NULL"
                ")"
            ),
            name="receivable_direction_valid",
        ),
        CheckConstraint(
            (
                "(entry_type <> 'PAYABLE') "
                "OR ("
                "customer_id IS NULL "
                "AND sales_order_id IS NULL"
                ")"
            ),
            name="payable_direction_valid",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_financial_entries_id_tenant",
        ),
        UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_financial_entries_tenant_code",
        ),
        ForeignKeyConstraint(
            [
                "branch_id",
                "tenant_id",
            ],
            [
                "branches.id",
                "branches.tenant_id",
            ],
            name="fk_financial_entries_branch_tenant",
        ),
        ForeignKeyConstraint(
            [
                "customer_id",
                "tenant_id",
            ],
            [
                "clientes.id",
                "clientes.tenant_id",
            ],
            name="fk_financial_entries_customer_tenant",
        ),
        ForeignKeyConstraint(
            [
                "supplier_id",
                "tenant_id",
            ],
            [
                "suppliers.id",
                "suppliers.tenant_id",
            ],
            name="fk_financial_entries_supplier_tenant",
        ),
        ForeignKeyConstraint(
            [
                "employee_id",
                "tenant_id",
            ],
            [
                "employees.id",
                "employees.tenant_id",
            ],
            name="fk_financial_entries_employee_tenant",
        ),
        ForeignKeyConstraint(
            [
                "sales_order_id",
                "tenant_id",
            ],
            [
                "sales_orders.id",
                "sales_orders.tenant_id",
            ],
            name="fk_financial_entries_sales_order_tenant",
        ),
        ForeignKeyConstraint(
            [
                "purchase_order_id",
                "tenant_id",
            ],
            [
                "purchase_orders.id",
                "purchase_orders.tenant_id",
            ],
            name="fk_financial_entries_purchase_order_tenant",
        ),
        Index(
            "ix_financial_entries_tenant_branch",
            "tenant_id",
            "branch_id",
        ),
        Index(
            "ix_financial_entries_tenant_customer",
            "tenant_id",
            "customer_id",
        ),
        Index(
            "ix_financial_entries_tenant_supplier",
            "tenant_id",
            "supplier_id",
        ),
        Index(
            "ix_financial_entries_tenant_employee",
            "tenant_id",
            "employee_id",
        ),
        Index(
            "ix_financial_entries_tenant_sales_order",
            "tenant_id",
            "sales_order_id",
        ),
        Index(
            "ix_financial_entries_tenant_purchase_order",
            "tenant_id",
            "purchase_order_id",
        ),
        Index(
            "ix_financial_entries_tenant_type_status",
            "tenant_id",
            "entry_type",
            "status",
        ),
        Index(
            "ix_financial_entries_tenant_due_date",
            "tenant_id",
            "due_date",
        ),
    )

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    entry_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=18,
            scale=6,
        ),
        nullable=False,
    )

    issue_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="OPEN",
        server_default=text("'OPEN'"),
    )

    branch_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    customer_id: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True,
    )

    supplier_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    employee_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    sales_order_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    purchase_order_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    category: Mapped[
        str | None
    ] = mapped_column(
        String(255),
        nullable=True,
    )

    notes: Mapped[
        str | None
    ] = mapped_column(
        String(4000),
        nullable=True,
    )

    settled_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    cancelled_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class FinancialTransactionModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist an actual movement of money."""

    __tablename__ = "financial_transactions"

    __table_args__ = (
        CheckConstraint(
            (
                "transaction_type IN ("
                "'INFLOW', "
                "'OUTFLOW'"
                ")"
            ),
            name="transaction_type_valid",
        ),
        CheckConstraint(
            (
                "status IN ("
                "'POSTED', "
                "'CANCELLED'"
                ")"
            ),
            name="status_valid",
        ),
        CheckConstraint(
            "amount > 0",
            name="amount_positive",
        ),
        CheckConstraint(
            "TRIM(description) <> ''",
            name="description_not_blank",
        ),
        CheckConstraint(
            (
                "(status <> 'CANCELLED') "
                "OR cancelled_at IS NOT NULL"
            ),
            name="cancelled_state_valid",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_financial_transactions_id_tenant",
        ),
        ForeignKeyConstraint(
            [
                "account_id",
                "tenant_id",
            ],
            [
                "financial_accounts.id",
                "financial_accounts.tenant_id",
            ],
            name=(
                "fk_financial_transactions_"
                "account_tenant"
            ),
        ),
        Index(
            "ix_financial_transactions_tenant_account",
            "tenant_id",
            "account_id",
        ),
        Index(
            "ix_financial_transactions_tenant_type_status",
            "tenant_id",
            "transaction_type",
            "status",
        ),
        Index(
            "ix_financial_transactions_tenant_occurred",
            "tenant_id",
            "occurred_at",
        ),
    )

    account_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    transaction_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=18,
            scale=6,
        ),
        nullable=False,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="POSTED",
        server_default=text("'POSTED'"),
    )

    payment_method: Mapped[
        str | None
    ] = mapped_column(
        String(255),
        nullable=True,
    )

    notes: Mapped[
        str | None
    ] = mapped_column(
        String(4000),
        nullable=True,
    )

    cancelled_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class FinancialAllocationModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist allocation of a transaction against a title."""

    __tablename__ = "financial_allocations"

    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="amount_positive",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_financial_allocations_id_tenant",
        ),
        UniqueConstraint(
            "tenant_id",
            "transaction_id",
            "entry_id",
            name=(
                "uq_financial_allocations_"
                "transaction_entry"
            ),
        ),
        ForeignKeyConstraint(
            [
                "transaction_id",
                "tenant_id",
            ],
            [
                "financial_transactions.id",
                "financial_transactions.tenant_id",
            ],
            name=(
                "fk_financial_allocations_"
                "transaction_tenant"
            ),
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            [
                "entry_id",
                "tenant_id",
            ],
            [
                "financial_entries.id",
                "financial_entries.tenant_id",
            ],
            name=(
                "fk_financial_allocations_"
                "entry_tenant"
            ),
            ondelete="CASCADE",
        ),
        Index(
            "ix_financial_allocations_tenant_transaction",
            "tenant_id",
            "transaction_id",
        ),
        Index(
            "ix_financial_allocations_tenant_entry",
            "tenant_id",
            "entry_id",
        ),
    )

    transaction_id: Mapped[
        uuid.UUID
    ] = mapped_column(
        Uuid,
        nullable=False,
    )

    entry_id: Mapped[
        uuid.UUID
    ] = mapped_column(
        Uuid,
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=18,
            scale=6,
        ),
        nullable=False,
    )
