"""Repository contracts for Finance."""

from __future__ import annotations

from abc import ABC, abstractmethod
import uuid

from organizeg3_api.domain.finance.account import (
    FinancialAccount,
)
from organizeg3_api.domain.finance.entry import (
    FinancialEntry,
)
from organizeg3_api.domain.finance.transaction import (
    FinancialAllocation,
    FinancialTransaction,
)


class IFinancialAccountRepository(
    ABC,
):
    """Persistence contract for financial accounts."""

    @abstractmethod
    def add(
        self,
        account: FinancialAccount,
    ) -> FinancialAccount:
        """Persist a financial account."""

    @abstractmethod
    def get_by_id(
        self,
        *,
        tenant_id: uuid.UUID,
        account_id: uuid.UUID,
    ) -> FinancialAccount | None:
        """Return one tenant-scoped account."""

    @abstractmethod
    def get_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> FinancialAccount | None:
        """Return one account by business code."""


class IFinancialEntryRepository(
    ABC,
):
    """Persistence contract for financial entries."""

    @abstractmethod
    def add(
        self,
        entry: FinancialEntry,
    ) -> FinancialEntry:
        """Persist a financial entry."""

    @abstractmethod
    def get_by_id(
        self,
        *,
        tenant_id: uuid.UUID,
        entry_id: uuid.UUID,
    ) -> FinancialEntry | None:
        """Return one tenant-scoped entry."""

    @abstractmethod
    def get_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> FinancialEntry | None:
        """Return one entry by business code."""


class IFinancialTransactionRepository(
    ABC,
):
    """Persistence contract for money movements."""

    @abstractmethod
    def add(
        self,
        transaction: FinancialTransaction,
    ) -> FinancialTransaction:
        """Persist an actual money movement."""

    @abstractmethod
    def get_by_id(
        self,
        *,
        tenant_id: uuid.UUID,
        transaction_id: uuid.UUID,
    ) -> FinancialTransaction | None:
        """Return one tenant-scoped transaction."""


class IFinancialAllocationRepository(
    ABC,
):
    """Persistence contract for title settlements."""

    @abstractmethod
    def add(
        self,
        allocation: FinancialAllocation,
    ) -> FinancialAllocation:
        """Persist a financial allocation."""

    @abstractmethod
    def list_by_entry(
        self,
        *,
        tenant_id: uuid.UUID,
        entry_id: uuid.UUID,
    ) -> list[FinancialAllocation]:
        """Return allocations belonging to a title."""

    @abstractmethod
    def list_by_transaction(
        self,
        *,
        tenant_id: uuid.UUID,
        transaction_id: uuid.UUID,
    ) -> list[FinancialAllocation]:
        """Return allocations belonging to a movement."""
