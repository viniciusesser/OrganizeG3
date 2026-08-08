"""SQLAlchemy repositories for the modern sales domain."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import cast
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.sales.order import (
    SalesOrder,
    SalesOrderItem,
)
from organizeg3_api.domain.sales.quote import (
    SalesQuote,
    SalesQuoteItem,
)
from organizeg3_api.domain.sales.value_objects import (
    SalesOrderStatus,
    SalesQuoteStatus,
    normalize_sales_code,
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
from organizeg3_api.infrastructure.persistence.models.material import (
    MaterialModel,
)
from organizeg3_api.infrastructure.persistence.models.sales import (
    SalesOrderItemModel,
    SalesOrderModel,
    SalesQuoteItemModel,
    SalesQuoteModel,
)
from organizeg3_api.infrastructure.persistence.models.service import (
    ServiceModel,
)


def _ensure_utc(
    value: datetime | None,
) -> datetime | None:
    """Normalize persisted datetimes to timezone-aware UTC."""

    if value is None:
        return None

    if value.tzinfo is None:
        return value.replace(
            tzinfo=UTC
        )

    return value.astimezone(UTC)


def _require_customer(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    customer_id: int,
) -> CustomerModel:
    customer = session.scalar(
        select(CustomerModel).where(
            CustomerModel.id == customer_id,
            CustomerModel.tenant_id == tenant_id,
        )
    )

    if customer is None:
        raise ValueError(
            "O cliente informado não pertence ao tenant."
        )

    return customer


def _require_branch(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    branch_id: uuid.UUID,
) -> BranchModel:
    branch = session.scalar(
        select(BranchModel).where(
            BranchModel.id == branch_id,
            BranchModel.tenant_id == tenant_id,
        )
    )

    if branch is None:
        raise ValueError(
            "A filial informada não pertence ao tenant."
        )

    return branch


def _require_employee(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    employee_id: uuid.UUID,
) -> EmployeeModel:
    employee = session.scalar(
        select(EmployeeModel).where(
            EmployeeModel.id == employee_id,
            EmployeeModel.tenant_id == tenant_id,
        )
    )

    if employee is None:
        raise ValueError(
            "O vendedor informado não pertence ao tenant."
        )

    return employee


def _require_material(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    material_id: uuid.UUID,
) -> MaterialModel:
    material = session.scalar(
        select(MaterialModel).where(
            MaterialModel.id == material_id,
            MaterialModel.tenant_id == tenant_id,
        )
    )

    if material is None:
        raise ValueError(
            "O material informado não pertence ao tenant."
        )

    return material


def _require_service(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    service_id: uuid.UUID,
) -> ServiceModel:
    service = session.scalar(
        select(ServiceModel).where(
            ServiceModel.id == service_id,
            ServiceModel.tenant_id == tenant_id,
        )
    )

    if service is None:
        raise ValueError(
            "O serviço informado não pertence ao tenant."
        )

    return service


def _require_quote(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    sales_quote_id: uuid.UUID,
) -> SalesQuoteModel:
    quote = session.scalar(
        select(SalesQuoteModel).where(
            SalesQuoteModel.id == sales_quote_id,
            SalesQuoteModel.tenant_id == tenant_id,
        )
    )

    if quote is None:
        raise ValueError(
            "O orçamento informado não pertence ao tenant."
        )

    return quote


def _require_quote_item(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    sales_quote_item_id: uuid.UUID,
) -> SalesQuoteItemModel:
    item = session.scalar(
        select(SalesQuoteItemModel).where(
            SalesQuoteItemModel.id
            == sales_quote_item_id,
            SalesQuoteItemModel.tenant_id
            == tenant_id,
        )
    )

    if item is None:
        raise ValueError(
            "O item de orçamento informado "
            "não pertence ao tenant."
        )

    return item


def _require_order(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    sales_order_id: uuid.UUID,
) -> SalesOrderModel:
    order = session.scalar(
        select(SalesOrderModel).where(
            SalesOrderModel.id == sales_order_id,
            SalesOrderModel.tenant_id == tenant_id,
        )
    )

    if order is None:
        raise ValueError(
            "O pedido de venda informado "
            "não pertence ao tenant."
        )

    return order


def _quote_to_domain(
    model: SalesQuoteModel,
) -> SalesQuote:
    return SalesQuote(
        id=model.id,
        tenant_id=cast(
            uuid.UUID,
            model.tenant_id,
        ),
        customer_id=model.customer_id,
        branch_id=model.branch_id,
        salesperson_employee_id=(
            model.salesperson_employee_id
        ),
        code=model.code,
        status=SalesQuoteStatus(
            model.status
        ),
        project_name=model.project_name,
        description=model.description,
        issued_at=_ensure_utc(
            model.issued_at
        ),
        valid_until=model.valid_until,
        expected_delivery_at=(
            model.expected_delivery_at
        ),
        payment_terms=model.payment_terms,
        notes=model.notes,
        material_cost=model.material_cost,
        labor_cost=model.labor_cost,
        transport_cost=model.transport_cost,
        other_cost=model.other_cost,
        tax_amount=model.tax_amount,
        discount_amount=model.discount_amount,
        proposed_amount=model.proposed_amount,
        approved_amount=model.approved_amount,
        approved_at=_ensure_utc(
            model.approved_at
        ),
        rejected_at=_ensure_utc(
            model.rejected_at
        ),
        cancelled_at=_ensure_utc(
            model.cancelled_at
        ),
        expired_at=_ensure_utc(
            model.expired_at
        ),
        created_at=_ensure_utc(
            model.created_at
        ),
        updated_at=_ensure_utc(
            model.updated_at
        ),
    )


def _quote_item_to_domain(
    model: SalesQuoteItemModel,
) -> SalesQuoteItem:
    return SalesQuoteItem(
        id=model.id,
        tenant_id=cast(
            uuid.UUID,
            model.tenant_id,
        ),
        sales_quote_id=model.sales_quote_id,
        sequence=model.sequence,
        material_id=model.material_id,
        service_id=model.service_id,
        description_snapshot=(
            model.description_snapshot
        ),
        quantity=model.quantity,
        unit_price=model.unit_price,
        discount_amount=model.discount_amount,
        created_at=_ensure_utc(
            model.created_at
        ),
        updated_at=_ensure_utc(
            model.updated_at
        ),
    )


def _order_to_domain(
    model: SalesOrderModel,
) -> SalesOrder:
    ordered_at = _ensure_utc(
        model.ordered_at
    )

    if ordered_at is None:
        raise RuntimeError(
            "Pedido persistido sem data de criação."
        )

    return SalesOrder(
        id=model.id,
        tenant_id=cast(
            uuid.UUID,
            model.tenant_id,
        ),
        source_quote_id=model.source_quote_id,
        customer_id=model.customer_id,
        branch_id=model.branch_id,
        salesperson_employee_id=(
            model.salesperson_employee_id
        ),
        code=model.code,
        status=SalesOrderStatus(
            model.status
        ),
        ordered_at=ordered_at,
        project_name_snapshot=(
            model.project_name_snapshot
        ),
        expected_delivery_at=(
            model.expected_delivery_at
        ),
        total_amount=model.total_amount,
        payment_terms_snapshot=(
            model.payment_terms_snapshot
        ),
        delivery_address_snapshot=(
            model.delivery_address_snapshot
        ),
        notes=model.notes,
        cancelled_at=_ensure_utc(
            model.cancelled_at
        ),
        delivered_at=_ensure_utc(
            model.delivered_at
        ),
        closed_at=_ensure_utc(
            model.closed_at
        ),
        created_at=_ensure_utc(
            model.created_at
        ),
        updated_at=_ensure_utc(
            model.updated_at
        ),
    )


def _order_item_to_domain(
    model: SalesOrderItemModel,
) -> SalesOrderItem:
    return SalesOrderItem(
        id=model.id,
        tenant_id=cast(
            uuid.UUID,
            model.tenant_id,
        ),
        sales_order_id=model.sales_order_id,
        source_quote_item_id=(
            model.source_quote_item_id
        ),
        sequence=model.sequence,
        material_id=model.material_id,
        service_id=model.service_id,
        description_snapshot=(
            model.description_snapshot
        ),
        quantity=model.quantity,
        unit_price=model.unit_price,
        discount_amount=model.discount_amount,
        created_at=_ensure_utc(
            model.created_at
        ),
        updated_at=_ensure_utc(
            model.updated_at
        ),
    )


class SQLAlchemySalesQuoteRepository:
    """Persist commercial quotes with tenant validation."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        sales_quote_id: uuid.UUID,
    ) -> SalesQuote | None:
        model = self._session.scalar(
            select(SalesQuoteModel).where(
                SalesQuoteModel.id
                == sales_quote_id,
                SalesQuoteModel.tenant_id
                == tenant_id,
            )
        )

        if model is None:
            return None

        return _quote_to_domain(
            model
        )

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> SalesQuote | None:
        normalized_code = normalize_sales_code(
            code
        )

        model = self._session.scalar(
            select(SalesQuoteModel).where(
                SalesQuoteModel.tenant_id
                == tenant_id,
                SalesQuoteModel.code
                == normalized_code,
            )
        )

        if model is None:
            return None

        return _quote_to_domain(
            model
        )

    def add(
        self,
        quote: SalesQuote,
    ) -> SalesQuote:
        _require_customer(
            self._session,
            tenant_id=quote.tenant_id,
            customer_id=quote.customer_id,
        )

        if quote.branch_id is not None:
            _require_branch(
                self._session,
                tenant_id=quote.tenant_id,
                branch_id=quote.branch_id,
            )

        if (
            quote.salesperson_employee_id
            is not None
        ):
            _require_employee(
                self._session,
                tenant_id=quote.tenant_id,
                employee_id=(
                    quote.salesperson_employee_id
                ),
            )

        model = SalesQuoteModel(
            id=quote.id,
            tenant_id=quote.tenant_id,
            customer_id=quote.customer_id,
            branch_id=quote.branch_id,
            salesperson_employee_id=(
                quote.salesperson_employee_id
            ),
            code=quote.code,
            status=quote.status.value,
            project_name=quote.project_name,
            description=quote.description,
            issued_at=quote.issued_at,
            valid_until=quote.valid_until,
            expected_delivery_at=(
                quote.expected_delivery_at
            ),
            payment_terms=quote.payment_terms,
            notes=quote.notes,
            material_cost=quote.material_cost,
            labor_cost=quote.labor_cost,
            transport_cost=quote.transport_cost,
            other_cost=quote.other_cost,
            tax_amount=quote.tax_amount,
            discount_amount=quote.discount_amount,
            proposed_amount=quote.proposed_amount,
            approved_amount=quote.approved_amount,
            approved_at=quote.approved_at,
            rejected_at=quote.rejected_at,
            cancelled_at=quote.cancelled_at,
            expired_at=quote.expired_at,
            created_at=quote.created_at,
            updated_at=quote.updated_at,
        )

        self._session.add(
            model
        )
        self._session.flush()
        self._session.refresh(
            model
        )

        return _quote_to_domain(
            model
        )


class SQLAlchemySalesQuoteItemRepository:
    """Persist tenant-scoped commercial quote items."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        sales_quote_item_id: uuid.UUID,
    ) -> SalesQuoteItem | None:
        model = self._session.scalar(
            select(SalesQuoteItemModel).where(
                SalesQuoteItemModel.id
                == sales_quote_item_id,
                SalesQuoteItemModel.tenant_id
                == tenant_id,
            )
        )

        if model is None:
            return None

        return _quote_item_to_domain(
            model
        )

    def add(
        self,
        item: SalesQuoteItem,
    ) -> SalesQuoteItem:
        _require_quote(
            self._session,
            tenant_id=item.tenant_id,
            sales_quote_id=(
                item.sales_quote_id
            ),
        )

        if item.material_id is not None:
            _require_material(
                self._session,
                tenant_id=item.tenant_id,
                material_id=item.material_id,
            )

        if item.service_id is not None:
            _require_service(
                self._session,
                tenant_id=item.tenant_id,
                service_id=item.service_id,
            )

        model = SalesQuoteItemModel(
            id=item.id,
            tenant_id=item.tenant_id,
            sales_quote_id=(
                item.sales_quote_id
            ),
            sequence=item.sequence,
            material_id=item.material_id,
            service_id=item.service_id,
            description_snapshot=(
                item.description_snapshot
            ),
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount_amount=(
                item.discount_amount
            ),
            created_at=item.created_at,
            updated_at=item.updated_at,
        )

        self._session.add(
            model
        )
        self._session.flush()
        self._session.refresh(
            model
        )

        return _quote_item_to_domain(
            model
        )


class SQLAlchemySalesOrderRepository:
    """Persist confirmed sales orders."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        sales_order_id: uuid.UUID,
    ) -> SalesOrder | None:
        model = self._session.scalar(
            select(SalesOrderModel).where(
                SalesOrderModel.id
                == sales_order_id,
                SalesOrderModel.tenant_id
                == tenant_id,
            )
        )

        if model is None:
            return None

        return _order_to_domain(
            model
        )

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> SalesOrder | None:
        normalized_code = normalize_sales_code(
            code
        )

        model = self._session.scalar(
            select(SalesOrderModel).where(
                SalesOrderModel.tenant_id
                == tenant_id,
                SalesOrderModel.code
                == normalized_code,
            )
        )

        if model is None:
            return None

        return _order_to_domain(
            model
        )

    def get_by_source_quote_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        sales_quote_id: uuid.UUID,
    ) -> SalesOrder | None:
        model = self._session.scalar(
            select(SalesOrderModel).where(
                SalesOrderModel.tenant_id
                == tenant_id,
                SalesOrderModel.source_quote_id
                == sales_quote_id,
            )
        )

        if model is None:
            return None

        return _order_to_domain(
            model
        )

    def add(
        self,
        order: SalesOrder,
    ) -> SalesOrder:
        quote = _require_quote(
            self._session,
            tenant_id=order.tenant_id,
            sales_quote_id=(
                order.source_quote_id
            ),
        )

        if (
            quote.status
            != SalesQuoteStatus.APPROVED.value
        ):
            raise ValueError(
                "Somente orçamento aprovado "
                "pode originar pedido de venda."
            )

        if (
            quote.customer_id
            != order.customer_id
        ):
            raise ValueError(
                "O cliente do pedido não corresponde "
                "ao cliente do orçamento."
            )

        existing_order = self._session.scalar(
            select(
                SalesOrderModel.id
            ).where(
                SalesOrderModel.tenant_id
                == order.tenant_id,
                SalesOrderModel.source_quote_id
                == order.source_quote_id,
            )
        )

        if existing_order is not None:
            raise ValueError(
                "O orçamento já possui pedido "
                "de venda associado."
            )

        _require_customer(
            self._session,
            tenant_id=order.tenant_id,
            customer_id=order.customer_id,
        )

        if order.branch_id is not None:
            _require_branch(
                self._session,
                tenant_id=order.tenant_id,
                branch_id=order.branch_id,
            )

        if (
            order.salesperson_employee_id
            is not None
        ):
            _require_employee(
                self._session,
                tenant_id=order.tenant_id,
                employee_id=(
                    order.salesperson_employee_id
                ),
            )

        model = SalesOrderModel(
            id=order.id,
            tenant_id=order.tenant_id,
            source_quote_id=(
                order.source_quote_id
            ),
            customer_id=order.customer_id,
            branch_id=order.branch_id,
            salesperson_employee_id=(
                order.salesperson_employee_id
            ),
            code=order.code,
            status=order.status.value,
            ordered_at=order.ordered_at,
            project_name_snapshot=(
                order.project_name_snapshot
            ),
            expected_delivery_at=(
                order.expected_delivery_at
            ),
            total_amount=order.total_amount,
            payment_terms_snapshot=(
                order.payment_terms_snapshot
            ),
            delivery_address_snapshot=(
                order.delivery_address_snapshot
            ),
            notes=order.notes,
            cancelled_at=order.cancelled_at,
            delivered_at=order.delivered_at,
            closed_at=order.closed_at,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )

        self._session.add(
            model
        )
        self._session.flush()
        self._session.refresh(
            model
        )

        return _order_to_domain(
            model
        )


class SQLAlchemySalesOrderItemRepository:
    """Persist confirmed sales order item snapshots."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        sales_order_item_id: uuid.UUID,
    ) -> SalesOrderItem | None:
        model = self._session.scalar(
            select(SalesOrderItemModel).where(
                SalesOrderItemModel.id
                == sales_order_item_id,
                SalesOrderItemModel.tenant_id
                == tenant_id,
            )
        )

        if model is None:
            return None

        return _order_item_to_domain(
            model
        )

    def add(
        self,
        item: SalesOrderItem,
    ) -> SalesOrderItem:
        order = _require_order(
            self._session,
            tenant_id=item.tenant_id,
            sales_order_id=(
                item.sales_order_id
            ),
        )

        quote_item: SalesQuoteItemModel | None = None

        if (
            item.source_quote_item_id
            is not None
        ):
            quote_item = _require_quote_item(
                self._session,
                tenant_id=item.tenant_id,
                sales_quote_item_id=(
                    item.source_quote_item_id
                ),
            )

            if (
                quote_item.sales_quote_id
                != order.source_quote_id
            ):
                raise ValueError(
                    "O item de orçamento informado "
                    "não pertence ao orçamento que "
                    "originou o pedido."
                )

        if item.material_id is not None:
            _require_material(
                self._session,
                tenant_id=item.tenant_id,
                material_id=item.material_id,
            )

        if item.service_id is not None:
            _require_service(
                self._session,
                tenant_id=item.tenant_id,
                service_id=item.service_id,
            )

        if quote_item is not None:
            if (
                quote_item.material_id
                != item.material_id
            ):
                raise ValueError(
                    "O material do item de pedido "
                    "não corresponde ao item "
                    "do orçamento de origem."
                )

            if (
                quote_item.service_id
                != item.service_id
            ):
                raise ValueError(
                    "O serviço do item de pedido "
                    "não corresponde ao item "
                    "do orçamento de origem."
                )

        model = SalesOrderItemModel(
            id=item.id,
            tenant_id=item.tenant_id,
            sales_order_id=(
                item.sales_order_id
            ),
            source_quote_id=(
                order.source_quote_id
            ),
            source_quote_item_id=(
                item.source_quote_item_id
            ),
            sequence=item.sequence,
            material_id=item.material_id,
            service_id=item.service_id,
            description_snapshot=(
                item.description_snapshot
            ),
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount_amount=(
                item.discount_amount
            ),
            created_at=item.created_at,
            updated_at=item.updated_at,
        )

        self._session.add(
            model
        )
        self._session.flush()
        self._session.refresh(
            model
        )

        return _order_item_to_domain(
            model
        )
