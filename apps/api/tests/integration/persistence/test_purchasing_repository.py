"""Integration tests for purchasing repositories."""

from __future__ import annotations

from decimal import Decimal
import uuid

import pytest
from sqlalchemy.orm import Session

from organizeg3_api.domain.purchasing.order import (
    PurchaseOrder,
    PurchaseOrderItem,
)
from organizeg3_api.domain.purchasing.receipt import (
    PurchaseReceipt,
    PurchaseReceiptItem,
)
from organizeg3_api.infrastructure.persistence.models.branch import (
    BranchModel,
)
from organizeg3_api.infrastructure.persistence.models.material import (
    MaterialModel,
)
from organizeg3_api.infrastructure.persistence.models.supplier import (
    SupplierModel,
)
from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories.purchasing_repository import (
    SQLAlchemyPurchaseOrderItemRepository,
    SQLAlchemyPurchaseOrderRepository,
    SQLAlchemyPurchaseReceiptItemRepository,
    SQLAlchemyPurchaseReceiptRepository,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.database,
]


def create_tenant(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    name: str,
) -> None:
    session.add(
        TenantRecordModel(
            id=tenant_id,
            name=name,
            status="ACTIVE",
            is_active=True,
        )
    )
    session.flush()


def create_supplier(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "FOR-001",
) -> SupplierModel:
    supplier = SupplierModel(
        tenant_id=tenant_id,
        code=code,
        name=f"Fornecedor {code}",
        is_active=True,
    )

    session.add(supplier)
    session.flush()

    return supplier


def create_material(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "MAT-001",
) -> MaterialModel:
    material = MaterialModel(
        tenant_id=tenant_id,
        code=code,
        name=f"Material {code}",
        category="MDF",
        unit="UN",
        is_active=True,
    )

    session.add(material)
    session.flush()

    return material


def create_branch(
    session: Session,
    *,
    tenant_id: uuid.UUID,
) -> BranchModel:
    branch = BranchModel(
        tenant_id=tenant_id,
        code="BR-001",
        name="Filial",
        is_headquarters=False,
        is_active=True,
    )

    session.add(branch)
    session.flush()

    return branch


def create_order(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    supplier_id: uuid.UUID,
    code: str = "OC-001",
) -> PurchaseOrder:
    repository = SQLAlchemyPurchaseOrderRepository(
        session
    )

    return repository.add(
        PurchaseOrder.create(
            tenant_id=tenant_id,
            supplier_id=supplier_id,
            code=code,
        )
    )


def test_persists_purchase_order(
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

    repository = SQLAlchemyPurchaseOrderRepository(
        session
    )

    saved = create_order(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier.id,
    )

    assert saved.id is not None

    loaded = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        purchase_order_id=saved.id,
    )

    assert loaded is not None
    assert loaded.code == "OC-001"


def test_purchase_order_code_is_tenant_scoped(
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
        tenant_id=tenant_id,
    )

    create_order(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier.id,
    )

    repository = SQLAlchemyPurchaseOrderRepository(
        session
    )

    assert (
        repository.get_by_code_for_tenant(
            tenant_id=tenant_id,
            code=" oc-001 ",
        )
        is not None
    )

    assert (
        repository.get_by_code_for_tenant(
            tenant_id=other_tenant_id,
            code="OC-001",
        )
        is None
    )


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

    order = PurchaseOrder.create(
        tenant_id=tenant_id,
        supplier_id=supplier.id,
        code="OC-001",
    )

    repository = SQLAlchemyPurchaseOrderRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="fornecedor",
    ):
        repository.add(order)


def test_rejects_cross_tenant_branch(
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
        tenant_id=tenant_id,
    )

    branch = create_branch(
        session,
        tenant_id=other_tenant_id,
    )

    order = PurchaseOrder.create(
        tenant_id=tenant_id,
        supplier_id=supplier.id,
        branch_id=branch.id,
        code="OC-001",
    )

    repository = SQLAlchemyPurchaseOrderRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="filial",
    ):
        repository.add(order)


def test_persists_purchase_order_item(
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

    material = create_material(
        session,
        tenant_id=tenant_id,
    )

    order = create_order(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier.id,
    )

    assert order.id is not None

    item = PurchaseOrderItem.create(
        tenant_id=tenant_id,
        purchase_order_id=order.id,
        sequence=1,
        material_id=material.id,
        quantity="10",
        unit_price="25.5",
    )

    repository = (
        SQLAlchemyPurchaseOrderItemRepository(
            session
        )
    )

    saved = repository.add(item)

    assert saved.id is not None
    assert saved.quantity == Decimal("10.000000")
    assert saved.unit_price == Decimal("25.500000")


def test_rejects_order_item_cross_tenant_material(
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
        tenant_id=tenant_id,
    )

    material = create_material(
        session,
        tenant_id=other_tenant_id,
    )

    order = create_order(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier.id,
    )

    assert order.id is not None

    item = PurchaseOrderItem.create(
        tenant_id=tenant_id,
        purchase_order_id=order.id,
        sequence=1,
        material_id=material.id,
        quantity="1",
        unit_price="10",
    )

    repository = (
        SQLAlchemyPurchaseOrderItemRepository(
            session
        )
    )

    with pytest.raises(
        ValueError,
        match="material",
    ):
        repository.add(item)


def test_persists_purchase_receipt(
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

    order = create_order(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier.id,
    )

    assert order.id is not None

    receipt = PurchaseReceipt.create(
        tenant_id=tenant_id,
        purchase_order_id=order.id,
        supplier_id=supplier.id,
        supplier_document_number="NF-123",
    )

    repository = SQLAlchemyPurchaseReceiptRepository(
        session
    )

    saved = repository.add(receipt)

    assert saved.id is not None

    loaded = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        purchase_receipt_id=saved.id,
    )

    assert loaded is not None
    assert loaded.supplier_document_number == "NF-123"


def test_rejects_receipt_supplier_different_from_order(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    supplier_a = create_supplier(
        session,
        tenant_id=tenant_id,
        code="FOR-A",
    )

    supplier_b = create_supplier(
        session,
        tenant_id=tenant_id,
        code="FOR-B",
    )

    order = create_order(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier_a.id,
    )

    assert order.id is not None

    receipt = PurchaseReceipt.create(
        tenant_id=tenant_id,
        purchase_order_id=order.id,
        supplier_id=supplier_b.id,
    )

    repository = SQLAlchemyPurchaseReceiptRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="não corresponde",
    ):
        repository.add(receipt)


def test_persists_purchase_receipt_item(
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

    material = create_material(
        session,
        tenant_id=tenant_id,
    )

    order = create_order(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier.id,
    )

    assert order.id is not None

    order_item_repository = (
        SQLAlchemyPurchaseOrderItemRepository(
            session
        )
    )

    order_item = (
        order_item_repository.add(
            PurchaseOrderItem.create(
                tenant_id=tenant_id,
                purchase_order_id=order.id,
                sequence=1,
                material_id=material.id,
                quantity="10",
                unit_price="20",
            )
        )
    )

    assert order_item.id is not None

    receipt_repository = (
        SQLAlchemyPurchaseReceiptRepository(
            session
        )
    )

    receipt = receipt_repository.add(
        PurchaseReceipt.create(
            tenant_id=tenant_id,
            purchase_order_id=order.id,
            supplier_id=supplier.id,
        )
    )

    assert receipt.id is not None

    item = PurchaseReceiptItem.create(
        tenant_id=tenant_id,
        purchase_receipt_id=receipt.id,
        purchase_order_id=order.id,
        purchase_order_item_id=order_item.id,
        material_id=material.id,
        quantity="4",
    )

    repository = (
        SQLAlchemyPurchaseReceiptItemRepository(
            session
        )
    )

    saved = repository.add(item)

    assert saved.id is not None
    assert saved.quantity == Decimal("4.000000")


def test_rejects_receipt_item_from_different_order(
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

    material = create_material(
        session,
        tenant_id=tenant_id,
    )

    order_a = create_order(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier.id,
        code="OC-A",
    )

    order_b = create_order(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier.id,
        code="OC-B",
    )

    assert order_a.id is not None
    assert order_b.id is not None

    item_repository = (
        SQLAlchemyPurchaseOrderItemRepository(
            session
        )
    )

    order_item = item_repository.add(
        PurchaseOrderItem.create(
            tenant_id=tenant_id,
            purchase_order_id=order_b.id,
            sequence=1,
            material_id=material.id,
            quantity="5",
            unit_price="10",
        )
    )

    assert order_item.id is not None

    receipt_repository = (
        SQLAlchemyPurchaseReceiptRepository(
            session
        )
    )

    receipt = receipt_repository.add(
        PurchaseReceipt.create(
            tenant_id=tenant_id,
            purchase_order_id=order_a.id,
            supplier_id=supplier.id,
        )
    )

    assert receipt.id is not None

    item = PurchaseReceiptItem.create(
        tenant_id=tenant_id,
        purchase_receipt_id=receipt.id,
        purchase_order_id=order_b.id,
        purchase_order_item_id=order_item.id,
        material_id=material.id,
        quantity="1",
    )

    repository = (
        SQLAlchemyPurchaseReceiptItemRepository(
            session
        )
    )

    with pytest.raises(
        ValueError,
        match="não corresponde",
    ):
        repository.add(item)
