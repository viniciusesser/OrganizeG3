"""Integration tests for Finance repositories."""

from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
import uuid

import pytest
from sqlalchemy.orm import Session

from organizeg3_api.domain.finance import (
    FinancialAccount,
    FinancialAccountType,
    FinancialAllocation,
    FinancialEntry,
    FinancialEntryType,
    FinancialTransaction,
    FinancialTransactionType,
)
from organizeg3_api.infrastructure.persistence.models.branch import (
    BranchModel,
)
from organizeg3_api.infrastructure.persistence.models.customer import (
    CustomerModel,
)
from organizeg3_api.infrastructure.persistence.models.supplier import (
    SupplierModel,
)
from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories.finance_repository import (
    SQLAlchemyFinancialAccountRepository,
    SQLAlchemyFinancialAllocationRepository,
    SQLAlchemyFinancialEntryRepository,
    SQLAlchemyFinancialTransactionRepository,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.database,
]


def utc_now() -> datetime:
    """Return deterministic UTC datetime."""

    return datetime(
        2026,
        8,
        8,
        12,
        0,
        tzinfo=UTC,
    )


def create_tenant(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    name: str,
) -> None:
    """Create one tenant fixture."""

    session.add(
        TenantRecordModel(
            id=tenant_id,
            name=name,
            status="ACTIVE",
            is_active=True,
        )
    )
    session.flush()


def create_branch(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "BR-001",
) -> BranchModel:
    """Create one tenant branch."""

    model = BranchModel(
        tenant_id=tenant_id,
        code=code,
        name=f"Filial {code}",
        is_headquarters=False,
        is_active=True,
    )

    session.add(model)
    session.flush()

    return model


def create_customer(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "CLI-FIN-001",
) -> CustomerModel:
    """Create one tenant customer."""

    model = CustomerModel(
        tenant_id=tenant_id,
        code=code,
        name=f"Cliente {code}",
        is_active=True,
    )

    session.add(model)
    session.flush()

    return model


def create_supplier(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "FOR-FIN-001",
) -> SupplierModel:
    """Create one tenant supplier."""

    model = SupplierModel(
        tenant_id=tenant_id,
        code=code,
        name=f"Fornecedor {code}",
        is_active=True,
    )

    session.add(model)
    session.flush()

    return model


def create_account(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "CX-001",
    branch_id: uuid.UUID | None = None,
) -> FinancialAccount:
    """Create and persist a financial account."""

    repository = SQLAlchemyFinancialAccountRepository(session)

    return repository.add(
        FinancialAccount(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            branch_id=branch_id,
            code=code,
            name="Conta Financeira",
            account_type=FinancialAccountType.BANK,
        )
    )


def create_receivable(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "REC-001",
    amount: Decimal = Decimal("1000"),
    customer_id: int | None = None,
) -> FinancialEntry:
    """Create and persist a receivable."""

    repository = SQLAlchemyFinancialEntryRepository(session)

    return repository.add(
        FinancialEntry(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            code=code,
            entry_type=FinancialEntryType.RECEIVABLE,
            description="Conta a receber",
            amount=amount,
            issue_date=date(
                2026,
                8,
                8,
            ),
            due_date=date(
                2026,
                8,
                20,
            ),
            customer_id=customer_id,
        )
    )


def create_payable(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "PAY-001",
    supplier_id: uuid.UUID | None = None,
) -> FinancialEntry:
    """Create and persist a payable."""

    repository = SQLAlchemyFinancialEntryRepository(session)

    return repository.add(
        FinancialEntry(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            code=code,
            entry_type=FinancialEntryType.PAYABLE,
            description="Conta a pagar",
            amount=Decimal("800"),
            issue_date=date(
                2026,
                8,
                8,
            ),
            due_date=date(
                2026,
                8,
                15,
            ),
            supplier_id=supplier_id,
        )
    )


def create_transaction(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    account_id: uuid.UUID,
    transaction_type: FinancialTransactionType,
    amount: Decimal = Decimal("1000"),
) -> FinancialTransaction:
    """Create and persist a financial transaction."""

    repository = SQLAlchemyFinancialTransactionRepository(session)

    return repository.add(
        FinancialTransaction(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            account_id=account_id,
            transaction_type=transaction_type,
            amount=amount,
            occurred_at=utc_now(),
            description="Movimentação financeira",
        )
    )


def test_persists_financial_account(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    saved = create_account(
        session,
        tenant_id=tenant_id,
    )

    repository = SQLAlchemyFinancialAccountRepository(session)

    loaded = repository.get_by_id(
        tenant_id=tenant_id,
        account_id=saved.id,
    )

    assert loaded is not None
    assert loaded.code == "CX-001"
    assert loaded.currency == "BRL"


def test_account_code_is_tenant_scoped(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=other_tenant_id,
        name="Tenant B",
    )

    create_account(
        session,
        tenant_id=tenant_id,
        code="BANCO-01",
    )

    repository = SQLAlchemyFinancialAccountRepository(session)

    assert (
        repository.get_by_code(
            tenant_id=tenant_id,
            code=" banco-01 ",
        )
        is not None
    )

    assert (
        repository.get_by_code(
            tenant_id=other_tenant_id,
            code="BANCO-01",
        )
        is None
    )


def test_rejects_cross_tenant_account_branch(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=other_tenant_id,
        name="Tenant B",
    )

    branch = create_branch(
        session,
        tenant_id=other_tenant_id,
    )

    repository = SQLAlchemyFinancialAccountRepository(session)

    account = FinancialAccount(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        branch_id=branch.id,
        code="CX-001",
        name="Caixa",
        account_type=FinancialAccountType.CASH,
    )

    with pytest.raises(
        ValueError,
        match="filial",
    ):
        repository.add(account)


def test_persists_receivable_with_customer(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    customer = create_customer(
        session,
        tenant_id=tenant_id,
    )

    saved = create_receivable(
        session,
        tenant_id=tenant_id,
        customer_id=customer.id,
    )

    repository = SQLAlchemyFinancialEntryRepository(session)

    loaded = repository.get_by_id(
        tenant_id=tenant_id,
        entry_id=saved.id,
    )

    assert loaded is not None
    assert loaded.customer_id == customer.id
    assert loaded.amount == Decimal("1000.000000")


def test_rejects_cross_tenant_customer(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=other_tenant_id,
        name="Tenant B",
    )

    customer = create_customer(
        session,
        tenant_id=other_tenant_id,
    )

    repository = SQLAlchemyFinancialEntryRepository(session)

    entry = FinancialEntry(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        code="REC-001",
        entry_type=FinancialEntryType.RECEIVABLE,
        description="Venda",
        amount=Decimal("500"),
        issue_date=date(
            2026,
            8,
            8,
        ),
        due_date=date(
            2026,
            8,
            20,
        ),
        customer_id=customer.id,
    )

    with pytest.raises(
        ValueError,
        match="cliente",
    ):
        repository.add(entry)


def test_persists_payable_with_supplier(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    supplier = create_supplier(
        session,
        tenant_id=tenant_id,
    )

    saved = create_payable(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier.id,
    )

    assert saved.supplier_id == supplier.id


def test_rejects_cross_tenant_supplier(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=other_tenant_id,
        name="Tenant B",
    )

    supplier = create_supplier(
        session,
        tenant_id=other_tenant_id,
    )

    repository = SQLAlchemyFinancialEntryRepository(session)

    entry = FinancialEntry(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        code="PAY-001",
        entry_type=FinancialEntryType.PAYABLE,
        description="Compra",
        amount=Decimal("500"),
        issue_date=date(
            2026,
            8,
            8,
        ),
        due_date=date(
            2026,
            8,
            20,
        ),
        supplier_id=supplier.id,
    )

    with pytest.raises(
        ValueError,
        match="fornecedor",
    ):
        repository.add(entry)


def test_persists_financial_transaction(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    account = create_account(
        session,
        tenant_id=tenant_id,
    )

    transaction = create_transaction(
        session,
        tenant_id=tenant_id,
        account_id=account.id,
        transaction_type=FinancialTransactionType.INFLOW,
    )

    assert transaction.account_id == account.id
    assert transaction.amount == Decimal("1000.000000")


def test_rejects_transaction_account_from_other_tenant(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()
    other_tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    create_tenant(
        session,
        tenant_id=other_tenant_id,
        name="Tenant B",
    )

    account = create_account(
        session,
        tenant_id=other_tenant_id,
    )

    repository = SQLAlchemyFinancialTransactionRepository(session)

    transaction = FinancialTransaction(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        account_id=account.id,
        transaction_type=FinancialTransactionType.INFLOW,
        amount=Decimal("100"),
        occurred_at=utc_now(),
        description="Recebimento",
    )

    with pytest.raises(
        ValueError,
        match="conta financeira",
    ):
        repository.add(transaction)


def test_persists_financial_allocation(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    account = create_account(
        session,
        tenant_id=tenant_id,
    )

    entry = create_receivable(
        session,
        tenant_id=tenant_id,
    )

    transaction = create_transaction(
        session,
        tenant_id=tenant_id,
        account_id=account.id,
        transaction_type=FinancialTransactionType.INFLOW,
        amount=Decimal("500"),
    )

    repository = SQLAlchemyFinancialAllocationRepository(session)

    saved = repository.add(
        FinancialAllocation(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            transaction_id=transaction.id,
            entry_id=entry.id,
            amount=Decimal("500"),
        )
    )

    assert saved.amount == Decimal("500.000000")

    allocations = repository.list_by_entry(
        tenant_id=tenant_id,
        entry_id=entry.id,
    )

    assert len(allocations) == 1


def test_allocation_cannot_exceed_entry_remaining(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    account = create_account(
        session,
        tenant_id=tenant_id,
    )

    entry = create_receivable(
        session,
        tenant_id=tenant_id,
        amount=Decimal("1000"),
    )

    transaction_a = create_transaction(
        session,
        tenant_id=tenant_id,
        account_id=account.id,
        transaction_type=FinancialTransactionType.INFLOW,
        amount=Decimal("700"),
    )

    transaction_b = create_transaction(
        session,
        tenant_id=tenant_id,
        account_id=account.id,
        transaction_type=FinancialTransactionType.INFLOW,
        amount=Decimal("400"),
    )

    repository = SQLAlchemyFinancialAllocationRepository(session)

    repository.add(
        FinancialAllocation(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            transaction_id=transaction_a.id,
            entry_id=entry.id,
            amount=Decimal("700"),
        )
    )

    with pytest.raises(
        ValueError,
        match="outstanding",
    ):
        repository.add(
            FinancialAllocation(
                id=uuid.uuid4(),
                tenant_id=tenant_id,
                transaction_id=transaction_b.id,
                entry_id=entry.id,
                amount=Decimal("400"),
            )
        )


def test_transaction_allocations_cannot_exceed_transaction(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    account = create_account(
        session,
        tenant_id=tenant_id,
    )

    entry_a = create_receivable(
        session,
        tenant_id=tenant_id,
        code="REC-A",
        amount=Decimal("1000"),
    )

    entry_b = create_receivable(
        session,
        tenant_id=tenant_id,
        code="REC-B",
        amount=Decimal("1000"),
    )

    transaction = create_transaction(
        session,
        tenant_id=tenant_id,
        account_id=account.id,
        transaction_type=FinancialTransactionType.INFLOW,
        amount=Decimal("1000"),
    )

    repository = SQLAlchemyFinancialAllocationRepository(session)

    repository.add(
        FinancialAllocation(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            transaction_id=transaction.id,
            entry_id=entry_a.id,
            amount=Decimal("700"),
        )
    )

    with pytest.raises(
        ValueError,
        match="remaining transaction amount",
    ):
        repository.add(
            FinancialAllocation(
                id=uuid.uuid4(),
                tenant_id=tenant_id,
                transaction_id=transaction.id,
                entry_id=entry_b.id,
                amount=Decimal("400"),
            )
        )
