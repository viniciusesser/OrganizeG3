"""SQLAlchemy repositories for purchasing core."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.purchasing.order import (
    PurchaseOrder,
    PurchaseOrderItem,
)
from organizeg3_api.domain.purchasing.receipt import (
    PurchaseReceipt,
    PurchaseReceiptItem,
)
from organizeg3_api.domain.purchasing.repository import (
    PurchaseOrderItemRepository,
    PurchaseOrderRepository,
    PurchaseReceiptItemRepository,
    PurchaseReceiptRepository,
)
from organizeg3_api.domain.purchasing.value_objects import (
    PurchaseOrderStatus,
    PurchaseReceiptStatus,
    normalize_purchase_code,
)
from organizeg3_api.infrastructure.persistence.models.branch import (
    BranchModel,
)
from organizeg3_api.infrastructure.persistence.models.material import (
    MaterialModel,
)
from organizeg3_api.infrastructure.persistence.models.purchasing import (
    PurchaseOrderItemModel,
    PurchaseOrderModel,
    PurchaseReceiptItemModel,
    PurchaseReceiptModel,
)
from organizeg3_api.infrastructure.persistence.models.supplier import (
    SupplierModel,
)


class SQLAlchemyPurchaseOrderRepository(
    PurchaseOrderRepository
):
    """Persist purchase orders."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        purchase_order_id: uuid.UUID,
    ) -> PurchaseOrder | None:
        statement = (
            select(PurchaseOrderModel)
            .where(
                PurchaseOrderModel.id
                == purchase_order_id,
                PurchaseOrderModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> PurchaseOrder | None:
        normalized = normalize_purchase_code(
            code
        )

        statement = (
            select(PurchaseOrderModel)
            .where(
                PurchaseOrderModel.tenant_id
                == tenant_id,
                PurchaseOrderModel.code
                == normalized,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def add(
        self,
        order: PurchaseOrder,
    ) -> PurchaseOrder:
        _require_supplier(
            self._session,
            tenant_id=order.tenant_id,
            supplier_id=order.supplier_id,
        )

        if order.branch_id is not None:
            _require_branch(
                self._session,
                tenant_id=order.tenant_id,
                branch_id=order.branch_id,
            )

        model = PurchaseOrderModel(
            id=order.id,
            tenant_id=order.tenant_id,
            supplier_id=order.supplier_id,
            branch_id=order.branch_id,
            code=order.code,
            status=order.status.value,
            issued_at=order.issued_at,
            expected_at=order.expected_at,
            notes=order.notes,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: PurchaseOrderModel,
    ) -> PurchaseOrder:
        return PurchaseOrder(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            supplier_id=model.supplier_id,
            branch_id=model.branch_id,
            code=model.code,
            status=PurchaseOrderStatus(
                model.status
            ),
            issued_at=model.issued_at,
            expected_at=model.expected_at,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyPurchaseOrderItemRepository(
    PurchaseOrderItemRepository
):
    """Persist purchase order items."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        purchase_order_item_id: uuid.UUID,
    ) -> PurchaseOrderItem | None:
        statement = (
            select(PurchaseOrderItemModel)
            .where(
                PurchaseOrderItemModel.id
                == purchase_order_item_id,
                PurchaseOrderItemModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def add(
        self,
        item: PurchaseOrderItem,
    ) -> PurchaseOrderItem:
        _require_purchase_order(
            self._session,
            tenant_id=item.tenant_id,
            purchase_order_id=(
                item.purchase_order_id
            ),
        )

        _require_material(
            self._session,
            tenant_id=item.tenant_id,
            material_id=item.material_id,
        )

        model = PurchaseOrderItemModel(
            id=item.id,
            tenant_id=item.tenant_id,
            purchase_order_id=(
                item.purchase_order_id
            ),
            sequence=item.sequence,
            material_id=item.material_id,
            quantity=item.quantity,
            received_quantity=(
                item.received_quantity
            ),
            unit_price=item.unit_price,
            notes=item.notes,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: PurchaseOrderItemModel,
    ) -> PurchaseOrderItem:
        return PurchaseOrderItem(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            purchase_order_id=(
                model.purchase_order_id
            ),
            sequence=model.sequence,
            material_id=model.material_id,
            quantity=model.quantity,
            received_quantity=(
                model.received_quantity
            ),
            unit_price=model.unit_price,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyPurchaseReceiptRepository(
    PurchaseReceiptRepository
):
    """Persist supplier receipts."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        purchase_receipt_id: uuid.UUID,
    ) -> PurchaseReceipt | None:
        statement = (
            select(PurchaseReceiptModel)
            .where(
                PurchaseReceiptModel.id
                == purchase_receipt_id,
                PurchaseReceiptModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def add(
        self,
        receipt: PurchaseReceipt,
    ) -> PurchaseReceipt:
        order = _require_purchase_order(
            self._session,
            tenant_id=receipt.tenant_id,
            purchase_order_id=(
                receipt.purchase_order_id
            ),
        )

        _require_supplier(
            self._session,
            tenant_id=receipt.tenant_id,
            supplier_id=receipt.supplier_id,
        )

        if order.supplier_id != receipt.supplier_id:
            raise ValueError(
                "O fornecedor do recebimento "
                "não corresponde ao fornecedor "
                "da ordem de compra."
            )

        if receipt.branch_id is not None:
            _require_branch(
                self._session,
                tenant_id=receipt.tenant_id,
                branch_id=receipt.branch_id,
            )

        model = PurchaseReceiptModel(
            id=receipt.id,
            tenant_id=receipt.tenant_id,
            purchase_order_id=(
                receipt.purchase_order_id
            ),
            supplier_id=receipt.supplier_id,
            branch_id=receipt.branch_id,
            received_at=receipt.received_at,
            status=receipt.status.value,
            supplier_document_number=(
                receipt.supplier_document_number
            ),
            notes=receipt.notes,
            posted_at=receipt.posted_at,
            cancelled_at=receipt.cancelled_at,
            created_at=receipt.created_at,
            updated_at=receipt.updated_at,
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: PurchaseReceiptModel,
    ) -> PurchaseReceipt:
        return PurchaseReceipt(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            purchase_order_id=(
                model.purchase_order_id
            ),
            supplier_id=model.supplier_id,
            branch_id=model.branch_id,
            received_at=model.received_at,
            status=PurchaseReceiptStatus(
                model.status
            ),
            supplier_document_number=(
                model.supplier_document_number
            ),
            notes=model.notes,
            posted_at=model.posted_at,
            cancelled_at=model.cancelled_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyPurchaseReceiptItemRepository(
    PurchaseReceiptItemRepository
):
    """Persist purchase receipt items."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        purchase_receipt_item_id: uuid.UUID,
    ) -> PurchaseReceiptItem | None:
        statement = (
            select(PurchaseReceiptItemModel)
            .where(
                PurchaseReceiptItemModel.id
                == purchase_receipt_item_id,
                PurchaseReceiptItemModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def add(
        self,
        item: PurchaseReceiptItem,
    ) -> PurchaseReceiptItem:
        receipt = _require_purchase_receipt(
            self._session,
            tenant_id=item.tenant_id,
            purchase_receipt_id=(
                item.purchase_receipt_id
            ),
        )

        order_item = _require_purchase_order_item(
            self._session,
            tenant_id=item.tenant_id,
            purchase_order_item_id=(
                item.purchase_order_item_id
            ),
        )

        _require_material(
            self._session,
            tenant_id=item.tenant_id,
            material_id=item.material_id,
        )

        if (
            receipt.purchase_order_id
            != item.purchase_order_id
        ):
            raise ValueError(
                "A ordem informada no item recebido "
                "não corresponde à ordem do recebimento."
            )

        if (
            order_item.purchase_order_id
            != item.purchase_order_id
        ):
            raise ValueError(
                "O item recebido não pertence "
                "à ordem de compra informada."
            )

        if (
            order_item.material_id
            != item.material_id
        ):
            raise ValueError(
                "O material recebido não corresponde "
                "ao material do item da ordem."
            )

        model = PurchaseReceiptItemModel(
            id=item.id,
            tenant_id=item.tenant_id,
            purchase_receipt_id=(
                item.purchase_receipt_id
            ),
            purchase_order_id=(
                item.purchase_order_id
            ),
            purchase_order_item_id=(
                item.purchase_order_item_id
            ),
            material_id=item.material_id,
            quantity=item.quantity,
            notes=item.notes,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: PurchaseReceiptItemModel,
    ) -> PurchaseReceiptItem:
        return PurchaseReceiptItem(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            purchase_receipt_id=(
                model.purchase_receipt_id
            ),
            purchase_order_id=(
                model.purchase_order_id
            ),
            purchase_order_item_id=(
                model.purchase_order_item_id
            ),
            material_id=model.material_id,
            quantity=model.quantity,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


def _require_supplier(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    supplier_id: uuid.UUID,
) -> SupplierModel:
    statement = (
        select(SupplierModel)
        .where(
            SupplierModel.id == supplier_id,
            SupplierModel.tenant_id == tenant_id,
        )
        .limit(1)
    )

    supplier = (
        session.execute(statement)
        .scalar_one_or_none()
    )

    if supplier is None:
        raise ValueError(
            "O fornecedor não pertence "
            "ao tenant informado."
        )

    return supplier


def _require_branch(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    branch_id: uuid.UUID,
) -> BranchModel:
    statement = (
        select(BranchModel)
        .where(
            BranchModel.id == branch_id,
            BranchModel.tenant_id == tenant_id,
        )
        .limit(1)
    )

    branch = (
        session.execute(statement)
        .scalar_one_or_none()
    )

    if branch is None:
        raise ValueError(
            "A filial não pertence "
            "ao tenant informado."
        )

    return branch


def _require_material(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    material_id: uuid.UUID,
) -> MaterialModel:
    statement = (
        select(MaterialModel)
        .where(
            MaterialModel.id == material_id,
            MaterialModel.tenant_id == tenant_id,
        )
        .limit(1)
    )

    material = (
        session.execute(statement)
        .scalar_one_or_none()
    )

    if material is None:
        raise ValueError(
            "O material não pertence "
            "ao tenant informado."
        )

    return material


def _require_purchase_order(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    purchase_order_id: uuid.UUID,
) -> PurchaseOrderModel:
    statement = (
        select(PurchaseOrderModel)
        .where(
            PurchaseOrderModel.id
            == purchase_order_id,
            PurchaseOrderModel.tenant_id
            == tenant_id,
        )
        .limit(1)
    )

    order = (
        session.execute(statement)
        .scalar_one_or_none()
    )

    if order is None:
        raise ValueError(
            "A ordem de compra não pertence "
            "ao tenant informado."
        )

    return order


def _require_purchase_order_item(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    purchase_order_item_id: uuid.UUID,
) -> PurchaseOrderItemModel:
    statement = (
        select(PurchaseOrderItemModel)
        .where(
            PurchaseOrderItemModel.id
            == purchase_order_item_id,
            PurchaseOrderItemModel.tenant_id
            == tenant_id,
        )
        .limit(1)
    )

    item = (
        session.execute(statement)
        .scalar_one_or_none()
    )

    if item is None:
        raise ValueError(
            "O item da ordem de compra "
            "não pertence ao tenant informado."
        )

    return item


def _require_purchase_receipt(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    purchase_receipt_id: uuid.UUID,
) -> PurchaseReceiptModel:
    statement = (
        select(PurchaseReceiptModel)
        .where(
            PurchaseReceiptModel.id
            == purchase_receipt_id,
            PurchaseReceiptModel.tenant_id
            == tenant_id,
        )
        .limit(1)
    )

    receipt = (
        session.execute(statement)
        .scalar_one_or_none()
    )

    if receipt is None:
        raise ValueError(
            "O recebimento não pertence "
            "ao tenant informado."
        )

    return receipt
