"""SQLAlchemy repositories for Finance core."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import cast
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from organizeg3_api.domain.finance.account import (
    FinancialAccount,
)
from organizeg3_api.domain.finance.entry import (
    FinancialEntry,
)
from organizeg3_api.domain.finance.repository import (
    IFinancialAccountRepository,
    IFinancialAllocationRepository,
    IFinancialEntryRepository,
    IFinancialTransactionRepository,
)
from organizeg3_api.domain.finance.transaction import (
    FinancialAllocation,
    FinancialTransaction,
    validate_financial_allocation,
)
from organizeg3_api.domain.finance.value_objects import (
    FinancialAccountType,
    FinancialEntryStatus,
    FinancialEntryType,
    FinancialTransactionStatus,
    FinancialTransactionType,
    normalize_code,
)
from organizeg3_api.infrastructure.persistence.models.branch import (
    BranchModel,
)
from organizeg3_api.infrastructure.persistence.models.customer import (
    CustomerModel,
)
from organizeg3_api.infrastructure.persistence.models.employee import (
    EmployeeModel,
)
from organizeg3_api.infrastructure.persistence.models.finance import (
    FinancialAccountModel,
    FinancialAllocationModel,
    FinancialEntryModel,
    FinancialTransactionModel,
)
from organizeg3_api.infrastructure.persistence.models.purchasing import (
    PurchaseOrderModel,
)
from organizeg3_api.infrastructure.persistence.models.sales import (
    SalesOrderModel,
)
from organizeg3_api.infrastructure.persistence.models.supplier import (
    SupplierModel,
)

ZERO_MONEY = Decimal("0.000000")


def _ensure_utc(
    value: datetime | None,
) -> datetime | None:
    """Normalize persisted datetime to aware UTC."""

    if value is None:
        return None

    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)

    return value.astimezone(UTC)


def _require_branch(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    branch_id: uuid.UUID,
) -> BranchModel:
    model = session.scalar(
        select(BranchModel).where(
            BranchModel.id == branch_id,
            BranchModel.tenant_id == tenant_id,
        )
    )

    if model is None:
        raise ValueError("A filial informada nÃ£o pertence ao tenant.")

    return model


def _require_customer(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    customer_id: int,
) -> CustomerModel:
    model = session.scalar(
        select(CustomerModel).where(
            CustomerModel.id == customer_id,
            CustomerModel.tenant_id == tenant_id,
        )
    )

    if model is None:
        raise ValueError("O cliente informado nÃ£o pertence ao tenant.")

    return model


def _require_supplier(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    supplier_id: uuid.UUID,
) -> SupplierModel:
    model = session.scalar(
        select(SupplierModel).where(
            SupplierModel.id == supplier_id,
            SupplierModel.tenant_id == tenant_id,
        )
    )

    if model is None:
        raise ValueError("O fornecedor informado nÃ£o pertence ao tenant.")

    return model


def _require_employee(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    employee_id: uuid.UUID,
) -> EmployeeModel:
    model = session.scalar(
        select(EmployeeModel).where(
            EmployeeModel.id == employee_id,
            EmployeeModel.tenant_id == tenant_id,
        )
    )

    if model is None:
        raise ValueError("O funcionÃ¡rio informado nÃ£o pertence ao tenant.")

    return model


def _require_sales_order(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    sales_order_id: uuid.UUID,
) -> SalesOrderModel:
    model = session.scalar(
        select(SalesOrderModel).where(
            SalesOrderModel.id == sales_order_id,
            SalesOrderModel.tenant_id == tenant_id,
        )
    )

    if model is None:
        raise ValueError("O pedido de venda informado nÃ£o pertence ao tenant.")

    return model


def _require_purchase_order(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    purchase_order_id: uuid.UUID,
) -> PurchaseOrderModel:
    model = session.scalar(
        select(PurchaseOrderModel).where(
            PurchaseOrderModel.id == purchase_order_id,
            PurchaseOrderModel.tenant_id == tenant_id,
        )
    )

    if model is None:
        raise ValueError("A ordem de compra informada nÃ£o pertence ao tenant.")

    return model


def _require_account(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    account_id: uuid.UUID,
) -> FinancialAccountModel:
    model = session.scalar(
        select(FinancialAccountModel).where(
            FinancialAccountModel.id == account_id,
            FinancialAccountModel.tenant_id == tenant_id,
        )
    )

    if model is None:
        raise ValueError("A conta financeira informada nÃ£o pertence ao tenant.")

    return model


def _require_entry(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    entry_id: uuid.UUID,
    for_update: bool = False,
) -> FinancialEntryModel:
    statement = select(FinancialEntryModel).where(
        FinancialEntryModel.id == entry_id,
        FinancialEntryModel.tenant_id == tenant_id,
    )

    if for_update:
        statement = statement.with_for_update()

    model = session.scalar(statement)

    if model is None:
        raise ValueError("O tÃ­tulo financeiro informado nÃ£o pertence ao tenant.")

    return model


def _require_transaction(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    transaction_id: uuid.UUID,
    for_update: bool = False,
) -> FinancialTransactionModel:
    statement = select(FinancialTransactionModel).where(
        FinancialTransactionModel.id == transaction_id,
        FinancialTransactionModel.tenant_id == tenant_id,
    )

    if for_update:
        statement = statement.with_for_update()

    model = session.scalar(statement)

    if model is None:
        raise ValueError("A movimentaÃ§Ã£o financeira informada nÃ£o pertence ao tenant.")

    return model


def _account_to_domain(
    model: FinancialAccountModel,
) -> FinancialAccount:
    return FinancialAccount(
        id=model.id,
        tenant_id=cast(
            uuid.UUID,
            model.tenant_id,
        ),
        branch_id=model.branch_id,
        code=model.code,
        name=model.name,
        account_type=FinancialAccountType(model.account_type),
        currency=model.currency,
        is_active=model.is_active,
    )


def _entry_to_domain(
    model: FinancialEntryModel,
) -> FinancialEntry:
    return FinancialEntry(
        id=model.id,
        tenant_id=cast(
            uuid.UUID,
            model.tenant_id,
        ),
        code=model.code,
        entry_type=FinancialEntryType(model.entry_type),
        description=model.description,
        amount=model.amount,
        issue_date=model.issue_date,
        due_date=model.due_date,
        status=FinancialEntryStatus(model.status),
        branch_id=model.branch_id,
        customer_id=model.customer_id,
        supplier_id=model.supplier_id,
        employee_id=model.employee_id,
        sales_order_id=model.sales_order_id,
        purchase_order_id=model.purchase_order_id,
        category=model.category,
        notes=model.notes,
        settled_at=_ensure_utc(model.settled_at),
        cancelled_at=_ensure_utc(model.cancelled_at),
    )


def _transaction_to_domain(
    model: FinancialTransactionModel,
) -> FinancialTransaction:
    occurred_at = _ensure_utc(model.occurred_at)

    if occurred_at is None:
        raise RuntimeError("MovimentaÃ§Ã£o persistida sem occurred_at.")

    return FinancialTransaction(
        id=model.id,
        tenant_id=cast(
            uuid.UUID,
            model.tenant_id,
        ),
        account_id=model.account_id,
        transaction_type=(FinancialTransactionType(model.transaction_type)),
        amount=model.amount,
        occurred_at=occurred_at,
        description=model.description,
        status=FinancialTransactionStatus(model.status),
        payment_method=model.payment_method,
        notes=model.notes,
        cancelled_at=_ensure_utc(model.cancelled_at),
    )


def _allocation_to_domain(
    model: FinancialAllocationModel,
) -> FinancialAllocation:
    return FinancialAllocation(
        id=model.id,
        tenant_id=cast(
            uuid.UUID,
            model.tenant_id,
        ),
        transaction_id=model.transaction_id,
        entry_id=model.entry_id,
        amount=model.amount,
    )


class SQLAlchemyFinancialAccountRepository(
    IFinancialAccountRepository,
):
    """Persist tenant-scoped financial accounts."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id(
        self,
        *,
        tenant_id: uuid.UUID,
        account_id: uuid.UUID,
    ) -> FinancialAccount | None:
        model = self._session.scalar(
            select(FinancialAccountModel).where(
                FinancialAccountModel.id == account_id,
                FinancialAccountModel.tenant_id == tenant_id,
            )
        )

        if model is None:
            return None

        return _account_to_domain(model)

    def get_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> FinancialAccount | None:
        normalized_code = normalize_code(code)

        model = self._session.scalar(
            select(FinancialAccountModel).where(
                FinancialAccountModel.tenant_id == tenant_id,
                FinancialAccountModel.code == normalized_code,
            )
        )

        if model is None:
            return None

        return _account_to_domain(model)

    def add(
        self,
        account: FinancialAccount,
    ) -> FinancialAccount:
        if account.branch_id is not None:
            _require_branch(
                self._session,
                tenant_id=account.tenant_id,
                branch_id=account.branch_id,
            )

        model = FinancialAccountModel(
            id=account.id,
            tenant_id=account.tenant_id,
            branch_id=account.branch_id,
            code=account.code,
            name=account.name,
            account_type=account.account_type.value,
            currency=account.currency,
            is_active=account.is_active,
        )

        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)

        return _account_to_domain(model)


class SQLAlchemyFinancialEntryRepository(
    IFinancialEntryRepository,
):
    """Persist receivables and payables."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id(
        self,
        *,
        tenant_id: uuid.UUID,
        entry_id: uuid.UUID,
    ) -> FinancialEntry | None:
        model = self._session.scalar(
            select(FinancialEntryModel).where(
                FinancialEntryModel.id == entry_id,
                FinancialEntryModel.tenant_id == tenant_id,
            )
        )

        if model is None:
            return None

        return _entry_to_domain(model)

    def get_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> FinancialEntry | None:
        normalized_code = normalize_code(code)

        model = self._session.scalar(
            select(FinancialEntryModel).where(
                FinancialEntryModel.tenant_id == tenant_id,
                FinancialEntryModel.code == normalized_code,
            )
        )

        if model is None:
            return None

        return _entry_to_domain(model)

    def add(
        self,
        entry: FinancialEntry,
    ) -> FinancialEntry:
        if entry.branch_id is not None:
            _require_branch(
                self._session,
                tenant_id=entry.tenant_id,
                branch_id=entry.branch_id,
            )

        if entry.customer_id is not None:
            _require_customer(
                self._session,
                tenant_id=entry.tenant_id,
                customer_id=entry.customer_id,
            )

        if entry.supplier_id is not None:
            _require_supplier(
                self._session,
                tenant_id=entry.tenant_id,
                supplier_id=entry.supplier_id,
            )

        if entry.employee_id is not None:
            _require_employee(
                self._session,
                tenant_id=entry.tenant_id,
                employee_id=entry.employee_id,
            )

        if entry.sales_order_id is not None:
            sales_order = _require_sales_order(
                self._session,
                tenant_id=entry.tenant_id,
                sales_order_id=entry.sales_order_id,
            )

            if entry.customer_id is not None and sales_order.customer_id != entry.customer_id:
                raise ValueError(
                    "O cliente do tÃ­tulo financeiro nÃ£o corresponde ao cliente do pedido de venda."
                )

        if entry.purchase_order_id is not None:
            purchase_order = _require_purchase_order(
                self._session,
                tenant_id=entry.tenant_id,
                purchase_order_id=(entry.purchase_order_id),
            )

            if entry.supplier_id is not None and purchase_order.supplier_id != entry.supplier_id:
                raise ValueError(
                    "O fornecedor do tÃ­tulo financeiro "
                    "nÃ£o corresponde ao fornecedor "
                    "da ordem de compra."
                )

        model = FinancialEntryModel(
            id=entry.id,
            tenant_id=entry.tenant_id,
            code=entry.code,
            entry_type=entry.entry_type.value,
            description=entry.description,
            amount=entry.amount,
            issue_date=entry.issue_date,
            due_date=entry.due_date,
            status=entry.status.value,
            branch_id=entry.branch_id,
            customer_id=entry.customer_id,
            supplier_id=entry.supplier_id,
            employee_id=entry.employee_id,
            sales_order_id=entry.sales_order_id,
            purchase_order_id=entry.purchase_order_id,
            category=entry.category,
            notes=entry.notes,
            settled_at=entry.settled_at,
            cancelled_at=entry.cancelled_at,
        )

        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)

        return _entry_to_domain(model)


class SQLAlchemyFinancialTransactionRepository(
    IFinancialTransactionRepository,
):
    """Persist actual money movements."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id(
        self,
        *,
        tenant_id: uuid.UUID,
        transaction_id: uuid.UUID,
    ) -> FinancialTransaction | None:
        model = self._session.scalar(
            select(FinancialTransactionModel).where(
                FinancialTransactionModel.id == transaction_id,
                FinancialTransactionModel.tenant_id == tenant_id,
            )
        )

        if model is None:
            return None

        return _transaction_to_domain(model)

    def add(
        self,
        transaction: FinancialTransaction,
    ) -> FinancialTransaction:
        account = _require_account(
            self._session,
            tenant_id=transaction.tenant_id,
            account_id=transaction.account_id,
        )

        if not account.is_active:
            raise ValueError("A conta financeira informada estÃ¡ inativa.")

        model = FinancialTransactionModel(
            id=transaction.id,
            tenant_id=transaction.tenant_id,
            account_id=transaction.account_id,
            transaction_type=(transaction.transaction_type.value),
            amount=transaction.amount,
            occurred_at=transaction.occurred_at,
            description=transaction.description,
            status=transaction.status.value,
            payment_method=transaction.payment_method,
            notes=transaction.notes,
            cancelled_at=transaction.cancelled_at,
        )

        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)

        return _transaction_to_domain(model)


class SQLAlchemyFinancialAllocationRepository(
    IFinancialAllocationRepository,
):
    """Persist settlements between titles and money movements."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def add(
        self,
        allocation: FinancialAllocation,
    ) -> FinancialAllocation:
        entry_model = _require_entry(
            self._session,
            tenant_id=allocation.tenant_id,
            entry_id=allocation.entry_id,
            for_update=True,
        )

        transaction_model = _require_transaction(
            self._session,
            tenant_id=allocation.tenant_id,
            transaction_id=(allocation.transaction_id),
            for_update=True,
        )

        entry = _entry_to_domain(entry_model)

        transaction = _transaction_to_domain(transaction_model)

        entry_allocated = self._sum_for_entry(
            tenant_id=allocation.tenant_id,
            entry_id=allocation.entry_id,
        )

        transaction_allocated = self._sum_for_transaction(
            tenant_id=allocation.tenant_id,
            transaction_id=(allocation.transaction_id),
        )

        entry_outstanding = entry.amount - entry_allocated

        transaction_remaining = transaction.amount - transaction_allocated

        validate_financial_allocation(
            entry=entry,
            transaction=transaction,
            allocation=allocation,
            outstanding_amount=(entry_outstanding),
        )

        if allocation.amount > transaction_remaining:
            raise ValueError("Allocation cannot exceed remaining transaction amount.")

        model = FinancialAllocationModel(
            id=allocation.id,
            tenant_id=allocation.tenant_id,
            transaction_id=(allocation.transaction_id),
            entry_id=allocation.entry_id,
            amount=allocation.amount,
        )

        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)

        return _allocation_to_domain(model)

    def list_by_entry(
        self,
        *,
        tenant_id: uuid.UUID,
        entry_id: uuid.UUID,
    ) -> list[FinancialAllocation]:
        models = self._session.scalars(
            select(FinancialAllocationModel)
            .where(
                FinancialAllocationModel.tenant_id == tenant_id,
                FinancialAllocationModel.entry_id == entry_id,
            )
            .order_by(
                FinancialAllocationModel.created_at,
                FinancialAllocationModel.id,
            )
        ).all()

        return [_allocation_to_domain(model) for model in models]

    def list_by_transaction(
        self,
        *,
        tenant_id: uuid.UUID,
        transaction_id: uuid.UUID,
    ) -> list[FinancialAllocation]:
        models = self._session.scalars(
            select(FinancialAllocationModel)
            .where(
                FinancialAllocationModel.tenant_id == tenant_id,
                FinancialAllocationModel.transaction_id == transaction_id,
            )
            .order_by(
                FinancialAllocationModel.created_at,
                FinancialAllocationModel.id,
            )
        ).all()

        return [_allocation_to_domain(model) for model in models]

    def _sum_for_entry(
        self,
        *,
        tenant_id: uuid.UUID,
        entry_id: uuid.UUID,
    ) -> Decimal:
        value = self._session.scalar(
            select(
                func.coalesce(
                    func.sum(FinancialAllocationModel.amount),
                    ZERO_MONEY,
                )
            ).where(
                FinancialAllocationModel.tenant_id == tenant_id,
                FinancialAllocationModel.entry_id == entry_id,
            )
        )

        return Decimal(value or ZERO_MONEY)

    def _sum_for_transaction(
        self,
        *,
        tenant_id: uuid.UUID,
        transaction_id: uuid.UUID,
    ) -> Decimal:
        value = self._session.scalar(
            select(
                func.coalesce(
                    func.sum(FinancialAllocationModel.amount),
                    ZERO_MONEY,
                )
            ).where(
                FinancialAllocationModel.tenant_id == tenant_id,
                FinancialAllocationModel.transaction_id == transaction_id,
            )
        )

        return Decimal(value or ZERO_MONEY)
