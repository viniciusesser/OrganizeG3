"""Repository contracts for sales."""

from __future__ import annotations

from typing import Protocol
import uuid

from organizeg3_api.domain.sales.order import (
    SalesOrder,
    SalesOrderItem,
)
from organizeg3_api.domain.sales.quote import (
    SalesQuote,
    SalesQuoteItem,
)


class SalesQuoteRepository(Protocol):
    """Persistence contract for sales quotes."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        sales_quote_id: uuid.UUID,
    ) -> SalesQuote | None:
        """Return one quote inside a tenant."""

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> SalesQuote | None:
        """Return one quote by tenant-scoped code."""

    def add(
        self,
        quote: SalesQuote,
    ) -> SalesQuote:
        """Persist one quote."""


class SalesQuoteItemRepository(Protocol):
    """Persistence contract for quote items."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        sales_quote_item_id: uuid.UUID,
    ) -> SalesQuoteItem | None:
        """Return one quote item inside a tenant."""

    def add(
        self,
        item: SalesQuoteItem,
    ) -> SalesQuoteItem:
        """Persist one quote item."""


class SalesOrderRepository(Protocol):
    """Persistence contract for confirmed sales orders."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        sales_order_id: uuid.UUID,
    ) -> SalesOrder | None:
        """Return one sales order inside a tenant."""

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> SalesOrder | None:
        """Return one sales order by tenant-scoped code."""

    def get_by_source_quote_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        sales_quote_id: uuid.UUID,
    ) -> SalesOrder | None:
        """Return the order generated from a quote."""

    def add(
        self,
        order: SalesOrder,
    ) -> SalesOrder:
        """Persist one sales order."""


class SalesOrderItemRepository(Protocol):
    """Persistence contract for sales order items."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        sales_order_item_id: uuid.UUID,
    ) -> SalesOrderItem | None:
        """Return one order item inside a tenant."""

    def add(
        self,
        item: SalesOrderItem,
    ) -> SalesOrderItem:
        """Persist one sales order item."""
