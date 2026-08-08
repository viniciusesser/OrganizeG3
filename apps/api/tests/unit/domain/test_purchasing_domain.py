"""Unit tests for purchasing core domain."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
import uuid

import pytest

from organizeg3_api.domain.purchasing.order import (
    PurchaseOrder,
    PurchaseOrderItem,
)
from organizeg3_api.domain.purchasing.receipt import (
    PurchaseReceipt,
    PurchaseReceiptItem,
)
from organizeg3_api.domain.purchasing.value_objects import (
    PurchaseOrderStatus,
    PurchaseReceiptStatus,
)


def test_creates_purchase_order() -> None:
    order = PurchaseOrder.create(
        tenant_id=uuid.uuid4(),
        supplier_id=uuid.uuid4(),
        code=" oc-001 ",
        notes=" Compra de MDF ",
    )

    assert order.id is not None
    assert order.code == "OC-001"
    assert order.notes == "Compra de MDF"
    assert order.status is PurchaseOrderStatus.DRAFT
    assert order.branch_id is None
    assert order.issued_at is None


def test_purchase_order_can_have_optional_branch() -> None:
    branch_id = uuid.uuid4()

    order = PurchaseOrder.create(
        tenant_id=uuid.uuid4(),
        supplier_id=uuid.uuid4(),
        branch_id=branch_id,
        code="OC-001",
    )

    assert order.branch_id == branch_id

    order.remove_branch()

    assert order.branch_id is None


def test_purchase_order_can_be_issued() -> None:
    now = datetime.now(UTC)

    order = PurchaseOrder.create(
        tenant_id=uuid.uuid4(),
        supplier_id=uuid.uuid4(),
        code="OC-001",
        expected_at=(
            now
            + timedelta(days=7)
        ),
    )

    order.issue(
        issued_at=now
    )

    assert order.status is PurchaseOrderStatus.ISSUED
    assert order.issued_at == now


def test_rejects_expected_date_before_issue() -> None:
    now = datetime.now(UTC)

    order = PurchaseOrder.create(
        tenant_id=uuid.uuid4(),
        supplier_id=uuid.uuid4(),
        code="OC-001",
        expected_at=(
            now
            - timedelta(days=1)
        ),
    )

    with pytest.raises(
        ValueError,
        match="não pode anteceder",
    ):
        order.issue(
            issued_at=now
        )


def test_purchase_order_partial_and_full_receipt_lifecycle() -> None:
    order = PurchaseOrder.create(
        tenant_id=uuid.uuid4(),
        supplier_id=uuid.uuid4(),
        code="OC-001",
    )

    order.issue()
    order.mark_partially_received()

    assert (
        order.status
        is PurchaseOrderStatus.PARTIALLY_RECEIVED
    )

    order.mark_received()

    assert order.status is PurchaseOrderStatus.RECEIVED


def test_purchase_order_can_close_partial_balance() -> None:
    order = PurchaseOrder.create(
        tenant_id=uuid.uuid4(),
        supplier_id=uuid.uuid4(),
        code="OC-001",
    )

    order.issue()
    order.mark_partially_received()
    order.close()

    assert order.status is PurchaseOrderStatus.CLOSED


def test_draft_purchase_order_can_be_cancelled() -> None:
    order = PurchaseOrder.create(
        tenant_id=uuid.uuid4(),
        supplier_id=uuid.uuid4(),
        code="OC-001",
    )

    order.cancel()

    assert order.status is PurchaseOrderStatus.CANCELLED


def test_creates_purchase_order_item() -> None:
    item = PurchaseOrderItem.create(
        tenant_id=uuid.uuid4(),
        purchase_order_id=uuid.uuid4(),
        sequence=1,
        material_id=uuid.uuid4(),
        quantity="10.5",
        unit_price="42.30",
    )

    assert item.id is not None
    assert item.quantity == Decimal("10.5")
    assert item.received_quantity == Decimal("0")
    assert item.remaining_quantity == Decimal("10.5")
    assert item.total_amount == Decimal("444.150")


def test_purchase_order_item_supports_partial_receipt() -> None:
    item = PurchaseOrderItem.create(
        tenant_id=uuid.uuid4(),
        purchase_order_id=uuid.uuid4(),
        sequence=1,
        material_id=uuid.uuid4(),
        quantity="10",
        unit_price="20",
    )

    item.register_receipt("4")

    assert item.received_quantity == Decimal("4")
    assert item.remaining_quantity == Decimal("6")


def test_purchase_order_item_supports_multiple_receipts() -> None:
    item = PurchaseOrderItem.create(
        tenant_id=uuid.uuid4(),
        purchase_order_id=uuid.uuid4(),
        sequence=1,
        material_id=uuid.uuid4(),
        quantity="10",
        unit_price="20",
    )

    item.register_receipt("4")
    item.register_receipt("6")

    assert item.received_quantity == Decimal("10")
    assert item.remaining_quantity == Decimal("0")


def test_rejects_receipt_above_order_item_balance() -> None:
    item = PurchaseOrderItem.create(
        tenant_id=uuid.uuid4(),
        purchase_order_id=uuid.uuid4(),
        sequence=1,
        material_id=uuid.uuid4(),
        quantity="5",
        unit_price="10",
    )

    with pytest.raises(
        ValueError,
        match="excede o saldo",
    ):
        item.register_receipt("6")


def test_rejects_non_positive_purchase_item_sequence() -> None:
    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        PurchaseOrderItem.create(
            tenant_id=uuid.uuid4(),
            purchase_order_id=uuid.uuid4(),
            sequence=0,
            material_id=uuid.uuid4(),
            quantity="1",
            unit_price="10",
        )


def test_rejects_negative_unit_price() -> None:
    with pytest.raises(
        ValueError,
        match="não pode ser negativo",
    ):
        PurchaseOrderItem.create(
            tenant_id=uuid.uuid4(),
            purchase_order_id=uuid.uuid4(),
            sequence=1,
            material_id=uuid.uuid4(),
            quantity="1",
            unit_price="-1",
        )


def test_creates_draft_purchase_receipt() -> None:
    receipt = PurchaseReceipt.create(
        tenant_id=uuid.uuid4(),
        purchase_order_id=uuid.uuid4(),
        supplier_id=uuid.uuid4(),
        supplier_document_number=" NF-123 ",
    )

    assert receipt.id is not None
    assert (
        receipt.status
        is PurchaseReceiptStatus.DRAFT
    )
    assert receipt.supplier_document_number == "NF-123"
    assert receipt.posted_at is None
    assert receipt.cancelled_at is None


def test_purchase_receipt_can_be_posted() -> None:
    received_at = datetime.now(UTC)

    receipt = PurchaseReceipt.create(
        tenant_id=uuid.uuid4(),
        purchase_order_id=uuid.uuid4(),
        supplier_id=uuid.uuid4(),
        received_at=received_at,
    )

    posted_at = (
        received_at
        + timedelta(minutes=5)
    )

    receipt.post(
        posted_at=posted_at
    )

    assert (
        receipt.status
        is PurchaseReceiptStatus.POSTED
    )
    assert receipt.posted_at == posted_at


def test_rejects_post_before_physical_receipt() -> None:
    received_at = datetime.now(UTC)

    receipt = PurchaseReceipt.create(
        tenant_id=uuid.uuid4(),
        purchase_order_id=uuid.uuid4(),
        supplier_id=uuid.uuid4(),
        received_at=received_at,
    )

    with pytest.raises(
        ValueError,
        match="não pode anteceder",
    ):
        receipt.post(
            posted_at=(
                received_at
                - timedelta(minutes=1)
            )
        )


def test_draft_purchase_receipt_can_be_cancelled() -> None:
    receipt = PurchaseReceipt.create(
        tenant_id=uuid.uuid4(),
        purchase_order_id=uuid.uuid4(),
        supplier_id=uuid.uuid4(),
    )

    receipt.cancel()

    assert (
        receipt.status
        is PurchaseReceiptStatus.CANCELLED
    )
    assert receipt.cancelled_at is not None


def test_posted_receipt_cannot_be_cancelled_directly() -> None:
    receipt = PurchaseReceipt.create(
        tenant_id=uuid.uuid4(),
        purchase_order_id=uuid.uuid4(),
        supplier_id=uuid.uuid4(),
    )

    receipt.post()

    with pytest.raises(
        ValueError,
        match="rascunho",
    ):
        receipt.cancel()


def test_creates_purchase_receipt_item() -> None:
    item = PurchaseReceiptItem.create(
        tenant_id=uuid.uuid4(),
        purchase_receipt_id=uuid.uuid4(),
        purchase_order_id=uuid.uuid4(),
        purchase_order_item_id=uuid.uuid4(),
        material_id=uuid.uuid4(),
        quantity="3.75",
        notes=" Conferido ",
    )

    assert item.id is not None
    assert item.quantity == Decimal("3.75")
    assert item.notes == "Conferido"


def test_rejects_zero_purchase_receipt_quantity() -> None:
    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        PurchaseReceiptItem.create(
            tenant_id=uuid.uuid4(),
            purchase_receipt_id=uuid.uuid4(),
            purchase_order_id=uuid.uuid4(),
            purchase_order_item_id=uuid.uuid4(),
            material_id=uuid.uuid4(),
            quantity="0",
        )
