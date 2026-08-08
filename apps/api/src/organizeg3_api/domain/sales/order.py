"""Confirmed sales order domain entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from decimal import Decimal
import uuid

from organizeg3_api.domain.sales.quote import SalesQuote
from organizeg3_api.domain.sales.value_objects import (
    SalesOrderStatus,
    SalesQuoteStatus,
    normalize_money,
    normalize_optional_text,
    normalize_quantity,
    normalize_required_text,
    normalize_sales_code,
)


@dataclass(slots=True)
class SalesOrder:
    """Represent a confirmed commercial commitment."""

    tenant_id: uuid.UUID
    source_quote_id: uuid.UUID
    customer_id: int
    code: str
    status: SalesOrderStatus
    ordered_at: datetime
    total_amount: Decimal

    branch_id: uuid.UUID | None = None
    salesperson_employee_id: uuid.UUID | None = None

    project_name_snapshot: str | None = None
    expected_delivery_at: date | None = None
    payment_terms_snapshot: str | None = None
    delivery_address_snapshot: str | None = None
    notes: str | None = None

    cancelled_at: datetime | None = None
    delivered_at: datetime | None = None
    closed_at: datetime | None = None

    id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_uuid(
            self.tenant_id,
            "tenant",
        )
        self._validate_uuid(
            self.source_quote_id,
            "orçamento de origem",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                "identificador",
            )

        if self.branch_id is not None:
            self._validate_uuid(
                self.branch_id,
                "filial",
            )

        if self.salesperson_employee_id is not None:
            self._validate_uuid(
                self.salesperson_employee_id,
                "vendedor",
            )

        self._validate_customer_id(
            self.customer_id
        )

        if not isinstance(
            self.status,
            SalesOrderStatus,
        ):
            raise TypeError(
                "O status deve ser SalesOrderStatus."
            )

        self.code = normalize_sales_code(
            self.code
        )

        self.total_amount = normalize_money(
            self.total_amount,
            field_name="O valor total do pedido",
            allow_zero=False,
        )

        self.project_name_snapshot = normalize_optional_text(
            self.project_name_snapshot
        )

        self.payment_terms_snapshot = normalize_optional_text(
            self.payment_terms_snapshot
        )

        self.delivery_address_snapshot = normalize_optional_text(
            self.delivery_address_snapshot
        )

        self.notes = normalize_optional_text(
            self.notes
        )

        self._validate_status_dates()

    @classmethod
    def create_from_approved_quote(
        cls,
        *,
        quote: SalesQuote,
        code: str,
        ordered_at: datetime | None = None,
        delivery_address_snapshot: str | None = None,
        notes: str | None = None,
    ) -> SalesOrder:
        """Create one confirmed order from an approved quote."""

        if quote.status is not SalesQuoteStatus.APPROVED:
            raise ValueError(
                "Somente orçamento aprovado "
                "pode gerar pedido de venda."
            )

        if quote.id is None:
            raise ValueError(
                "O orçamento precisa possuir identificador "
                "antes de gerar pedido."
            )

        if quote.approved_amount is None:
            raise ValueError(
                "O orçamento aprovado precisa possuir "
                "valor aprovado."
            )

        now = datetime.now(UTC)

        effective_ordered_at = (
            ordered_at
            or now
        )

        if (
            quote.approved_at is not None
            and effective_ordered_at < quote.approved_at
        ):
            raise ValueError(
                "O pedido não pode anteceder "
                "a aprovação do orçamento."
            )

        return cls(
            id=uuid.uuid4(),
            tenant_id=quote.tenant_id,
            source_quote_id=quote.id,
            customer_id=quote.customer_id,
            branch_id=quote.branch_id,
            salesperson_employee_id=(
                quote.salesperson_employee_id
            ),
            code=code,
            status=SalesOrderStatus.OPEN,
            ordered_at=effective_ordered_at,
            project_name_snapshot=quote.project_name,
            expected_delivery_at=(
                quote.expected_delivery_at
            ),
            total_amount=quote.approved_amount,
            payment_terms_snapshot=(
                quote.payment_terms
            ),
            delivery_address_snapshot=(
                delivery_address_snapshot
            ),
            notes=notes,
            cancelled_at=None,
            delivered_at=None,
            closed_at=None,
            created_at=now,
            updated_at=now,
        )

    def start_production(self) -> None:
        """Mark the order as released to production."""

        if self.status is not SalesOrderStatus.OPEN:
            raise ValueError(
                "Somente pedido aberto pode iniciar produção."
            )

        self.status = SalesOrderStatus.IN_PRODUCTION
        self._touch()

    def mark_ready_for_delivery(self) -> None:
        """Mark the order as ready for delivery."""

        if (
            self.status
            is not SalesOrderStatus.IN_PRODUCTION
        ):
            raise ValueError(
                "Somente pedido em produção pode ficar "
                "pronto para entrega."
            )

        self.status = (
            SalesOrderStatus.READY_FOR_DELIVERY
        )
        self._touch()

    def mark_delivered(
        self,
        *,
        delivered_at: datetime | None = None,
    ) -> None:
        """Record physical delivery."""

        if (
            self.status
            is not SalesOrderStatus.READY_FOR_DELIVERY
        ):
            raise ValueError(
                "Somente pedido pronto para entrega "
                "pode ser entregue."
            )

        effective_delivered_at = (
            delivered_at
            or datetime.now(UTC)
        )

        if effective_delivered_at < self.ordered_at:
            raise ValueError(
                "A entrega não pode anteceder o pedido."
            )

        self.status = SalesOrderStatus.DELIVERED
        self.delivered_at = effective_delivered_at
        self._touch()

    def close(
        self,
        *,
        closed_at: datetime | None = None,
    ) -> None:
        """Close a delivered sales order."""

        if self.status is not SalesOrderStatus.DELIVERED:
            raise ValueError(
                "Somente pedido entregue pode ser encerrado."
            )

        effective_closed_at = (
            closed_at
            or datetime.now(UTC)
        )

        if (
            self.delivered_at is not None
            and effective_closed_at < self.delivered_at
        ):
            raise ValueError(
                "O encerramento não pode anteceder a entrega."
            )

        self.status = SalesOrderStatus.CLOSED
        self.closed_at = effective_closed_at
        self._touch()

    def cancel(
        self,
        *,
        cancelled_at: datetime | None = None,
    ) -> None:
        """Cancel an order before physical delivery."""

        if self.status in {
            SalesOrderStatus.DELIVERED,
            SalesOrderStatus.CLOSED,
            SalesOrderStatus.CANCELLED,
        }:
            raise ValueError(
                "O pedido não pode ser cancelado "
                "no status atual."
            )

        effective_cancelled_at = (
            cancelled_at
            or datetime.now(UTC)
        )

        if effective_cancelled_at < self.ordered_at:
            raise ValueError(
                "O cancelamento não pode anteceder o pedido."
            )

        self.status = SalesOrderStatus.CANCELLED
        self.cancelled_at = effective_cancelled_at
        self._touch()

    def _validate_status_dates(self) -> None:
        if (
            self.status is SalesOrderStatus.DELIVERED
            and self.delivered_at is None
        ):
            raise ValueError(
                "Pedido entregue exige data de entrega."
            )

        if (
            self.status is SalesOrderStatus.CLOSED
            and self.closed_at is None
        ):
            raise ValueError(
                "Pedido encerrado exige data de encerramento."
            )

        if (
            self.status is SalesOrderStatus.CANCELLED
            and self.cancelled_at is None
        ):
            raise ValueError(
                "Pedido cancelado exige data de cancelamento."
            )

        if (
            self.delivered_at is not None
            and self.delivered_at < self.ordered_at
        ):
            raise ValueError(
                "A entrega não pode anteceder o pedido."
            )

        if (
            self.closed_at is not None
            and self.delivered_at is not None
            and self.closed_at < self.delivered_at
        ):
            raise ValueError(
                "O encerramento não pode anteceder a entrega."
            )

        if (
            self.cancelled_at is not None
            and self.cancelled_at < self.ordered_at
        ):
            raise ValueError(
                "O cancelamento não pode anteceder o pedido."
            )

    @staticmethod
    def _validate_customer_id(
        value: object,
    ) -> None:
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
        ):
            raise TypeError(
                "O cliente deve possuir identificador inteiro."
            )

        if value <= 0:
            raise ValueError(
                "O identificador do cliente "
                "deve ser maior que zero."
            )

    @staticmethod
    def _validate_uuid(
        value: object,
        field_name: str,
    ) -> None:
        if not isinstance(value, uuid.UUID):
            raise TypeError(
                f"O {field_name} deve ser um UUID."
            )

        if value.int == 0:
            raise ValueError(
                f"O {field_name} não pode possuir UUID nulo."
            )

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)


@dataclass(slots=True)
class SalesOrderItem:
    """Represent one confirmed sales line snapshot."""

    tenant_id: uuid.UUID
    sales_order_id: uuid.UUID
    sequence: int
    description_snapshot: str
    quantity: Decimal
    unit_price: Decimal
    discount_amount: Decimal

    source_quote_item_id: uuid.UUID | None = None
    material_id: uuid.UUID | None = None
    service_id: uuid.UUID | None = None

    id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_uuid(
            self.tenant_id,
            "tenant",
        )
        self._validate_uuid(
            self.sales_order_id,
            "pedido de venda",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                "identificador",
            )

        if self.source_quote_item_id is not None:
            self._validate_uuid(
                self.source_quote_item_id,
                "item do orçamento de origem",
            )

        if self.material_id is not None:
            self._validate_uuid(
                self.material_id,
                "material",
            )

        if self.service_id is not None:
            self._validate_uuid(
                self.service_id,
                "serviço",
            )

        if (
            self.material_id is not None
            and self.service_id is not None
        ):
            raise ValueError(
                "Um item de venda não pode referenciar "
                "material e serviço simultaneamente."
            )

        if (
            not isinstance(self.sequence, int)
            or isinstance(self.sequence, bool)
        ):
            raise TypeError(
                "A sequência do item deve ser inteira."
            )

        if self.sequence <= 0:
            raise ValueError(
                "A sequência do item deve ser maior que zero."
            )

        self.description_snapshot = normalize_required_text(
            self.description_snapshot,
            field_name="A descrição do item",
        )

        self.quantity = normalize_quantity(
            self.quantity
        )

        self.unit_price = normalize_money(
            self.unit_price,
            field_name="O valor unitário",
        )

        self.discount_amount = normalize_money(
            self.discount_amount,
            field_name="O desconto do item",
        )

        if self.discount_amount > self.gross_amount:
            raise ValueError(
                "O desconto do item não pode ser maior "
                "que o valor bruto."
            )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        sales_order_id: uuid.UUID,
        sequence: int,
        description_snapshot: str,
        quantity: Decimal | int | str,
        unit_price: Decimal | int | str,
        discount_amount: Decimal | int | str = Decimal("0"),
        source_quote_item_id: uuid.UUID | None = None,
        material_id: uuid.UUID | None = None,
        service_id: uuid.UUID | None = None,
    ) -> SalesOrderItem:
        """Create one confirmed sales order item."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            sales_order_id=sales_order_id,
            source_quote_item_id=(
                source_quote_item_id
            ),
            sequence=sequence,
            description_snapshot=description_snapshot,
            quantity=normalize_quantity(
                quantity
            ),
            unit_price=normalize_money(
                unit_price,
                field_name="O valor unitário",
            ),
            discount_amount=normalize_money(
                discount_amount,
                field_name="O desconto do item",
            ),
            material_id=material_id,
            service_id=service_id,
            created_at=now,
            updated_at=now,
        )

    @property
    def gross_amount(self) -> Decimal:
        """Return gross sales line amount."""

        return (
            self.quantity
            * self.unit_price
        )

    @property
    def total_amount(self) -> Decimal:
        """Return final sales line amount."""

        return (
            self.gross_amount
            - self.discount_amount
        )

    @staticmethod
    def _validate_uuid(
        value: object,
        field_name: str,
    ) -> None:
        if not isinstance(value, uuid.UUID):
            raise TypeError(
                f"O {field_name} deve ser um UUID."
            )

        if value.int == 0:
            raise ValueError(
                f"O {field_name} não pode possuir UUID nulo."
            )
