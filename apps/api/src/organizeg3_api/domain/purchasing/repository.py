"""Purchasing repository contracts."""

from __future__ import annotations

from typing import Protocol
import uuid

from organizeg3_api.domain.purchasing.order import (
    PurchaseOrder,
    PurchaseOrderItem,
)
from organizeg3_api.domain.purchasing.receipt import (
    PurchaseReceipt,
    PurchaseReceiptItem,
)


class PurchaseOrderRepository(Protocol):
    """Persistence contract for purchase orders."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        purchase_order_id: uuid.UUID,
    ) -> PurchaseOrder | None:
        ...

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> PurchaseOrder | None:
        ...

    def add(
        self,
        order: PurchaseOrder,
    ) -> PurchaseOrder:
        ...


class PurchaseOrderItemRepository(Protocol):
    """Persistence contract for purchase order items."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        purchase_order_item_id: uuid.UUID,
    ) -> PurchaseOrderItem | None:
        ...

    def add(
        self,
        item: PurchaseOrderItem,
    ) -> PurchaseOrderItem:
        ...


class PurchaseReceiptRepository(Protocol):
    """Persistence contract for purchase receipts."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        purchase_receipt_id: uuid.UUID,
    ) -> PurchaseReceipt | None:
        ...

    def add(
        self,
        receipt: PurchaseReceipt,
    ) -> PurchaseReceipt:
        ...


class PurchaseReceiptItemRepository(Protocol):
    """Persistence contract for purchase receipt items."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        purchase_receipt_item_id: uuid.UUID,
    ) -> PurchaseReceiptItem | None:
        ...

    def add(
        self,
        item: PurchaseReceiptItem,
    ) -> PurchaseReceiptItem:
        ...
