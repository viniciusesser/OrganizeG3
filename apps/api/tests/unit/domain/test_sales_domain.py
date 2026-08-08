"""Unit tests for sales core domain."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
import uuid

import pytest

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
)


def create_quote(
    *,
    proposed_amount: str = "6000",
) -> SalesQuote:
    return SalesQuote.create(
        tenant_id=uuid.uuid4(),
        customer_id=1,
        code="ORC-001",
        project_name="Cozinha planejada",
        proposed_amount=proposed_amount,
        payment_terms="50% entrada e 50% entrega",
    )


def create_approved_quote() -> SalesQuote:
    quote = create_quote()
    quote.issue()
    quote.approve(
        approved_amount="5000"
    )
    return quote


def test_creates_draft_sales_quote() -> None:
    quote = SalesQuote.create(
        tenant_id=uuid.uuid4(),
        customer_id=1,
        code=" orc-001 ",
        project_name=" Cozinha ",
        proposed_amount="6150",
        description=" Projeto completo ",
    )

    assert quote.id is not None
    assert quote.code == "ORC-001"
    assert quote.project_name == "Cozinha"
    assert quote.description == "Projeto completo"
    assert quote.status is SalesQuoteStatus.DRAFT
    assert quote.proposed_amount == Decimal("6150")
    assert quote.approved_amount is None


def test_quote_customer_id_must_be_positive() -> None:
    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        SalesQuote.create(
            tenant_id=uuid.uuid4(),
            customer_id=0,
            code="ORC-001",
            project_name="Projeto",
        )


def test_quote_can_have_optional_branch_and_salesperson() -> None:
    branch_id = uuid.uuid4()
    salesperson_id = uuid.uuid4()

    quote = SalesQuote.create(
        tenant_id=uuid.uuid4(),
        customer_id=1,
        branch_id=branch_id,
        salesperson_employee_id=salesperson_id,
        code="ORC-001",
        project_name="Projeto",
    )

    assert quote.branch_id == branch_id
    assert quote.salesperson_employee_id == salesperson_id


def test_quote_total_cost_and_estimated_profit() -> None:
    quote = SalesQuote.create(
        tenant_id=uuid.uuid4(),
        customer_id=1,
        code="ORC-001",
        project_name="Projeto",
        proposed_amount="6000",
        material_cost="2000",
        labor_cost="1000",
        transport_cost="300",
        other_cost="200",
        tax_amount="500",
    )

    assert quote.total_cost == Decimal("4000")
    assert quote.estimated_profit == Decimal("2000")


def test_draft_quote_can_be_issued() -> None:
    issued_at = datetime.now(UTC)

    quote = create_quote()

    quote.issue(
        issued_at=issued_at
    )

    assert quote.status is SalesQuoteStatus.SENT
    assert quote.issued_at == issued_at


def test_quote_without_value_cannot_be_issued() -> None:
    quote = create_quote(
        proposed_amount="0"
    )

    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        quote.issue()


def test_sent_quote_can_enter_negotiation() -> None:
    quote = create_quote()

    quote.issue()
    quote.start_negotiation()

    assert quote.status is SalesQuoteStatus.NEGOTIATION


def test_sent_quote_can_be_approved_with_closed_value() -> None:
    quote = create_quote(
        proposed_amount="6150"
    )

    quote.issue()
    quote.approve(
        approved_amount="5000"
    )

    assert quote.status is SalesQuoteStatus.APPROVED
    assert quote.proposed_amount == Decimal("6150")
    assert quote.approved_amount == Decimal("5000")
    assert quote.approved_at is not None


def test_approved_value_must_be_positive() -> None:
    quote = create_quote()
    quote.issue()

    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        quote.approve(
            approved_amount="0"
        )


def test_approved_quote_cannot_be_cancelled_directly() -> None:
    quote = create_approved_quote()

    with pytest.raises(
        ValueError,
        match="não pode ser cancelado",
    ):
        quote.cancel()


def test_sent_quote_can_be_rejected() -> None:
    quote = create_quote()

    quote.issue()
    quote.reject()

    assert quote.status is SalesQuoteStatus.REJECTED
    assert quote.rejected_at is not None


def test_draft_quote_can_be_cancelled() -> None:
    quote = create_quote()

    quote.cancel()

    assert quote.status is SalesQuoteStatus.CANCELLED
    assert quote.cancelled_at is not None


def test_quote_can_expire_after_validity() -> None:
    now = datetime.now(UTC)

    quote = SalesQuote.create(
        tenant_id=uuid.uuid4(),
        customer_id=1,
        code="ORC-001",
        project_name="Projeto",
        proposed_amount="5000",
        valid_until=datetime.now(UTC).date(),
    )

    quote.issue(
        issued_at=now
    )

    quote.expire(
        expired_at=(
            now
            + timedelta(days=1)
        )
    )

    assert quote.status is SalesQuoteStatus.EXPIRED


def test_quote_cannot_expire_inside_validity() -> None:
    now = datetime.now(UTC)

    quote = SalesQuote.create(
        tenant_id=uuid.uuid4(),
        customer_id=1,
        code="ORC-001",
        project_name="Projeto",
        proposed_amount="5000",
        valid_until=(
            datetime.now(UTC).date()
            + timedelta(days=10)
        ),
    )

    quote.issue(
        issued_at=now
    )

    with pytest.raises(
        ValueError,
        match="dentro do prazo",
    ):
        quote.expire(
            expired_at=(
                now
                + timedelta(days=1)
            )
        )


def test_creates_free_form_quote_item() -> None:
    item = SalesQuoteItem.create(
        tenant_id=uuid.uuid4(),
        sales_quote_id=uuid.uuid4(),
        sequence=1,
        description_snapshot=" Armário planejado ",
        quantity="1",
        unit_price="5000",
    )

    assert item.id is not None
    assert item.description_snapshot == "Armário planejado"
    assert item.gross_amount == Decimal("5000")
    assert item.total_amount == Decimal("5000")


def test_quote_item_can_reference_material() -> None:
    material_id = uuid.uuid4()

    item = SalesQuoteItem.create(
        tenant_id=uuid.uuid4(),
        sales_quote_id=uuid.uuid4(),
        sequence=1,
        material_id=material_id,
        description_snapshot="MDF Branco",
        quantity="5",
        unit_price="250",
    )

    assert item.material_id == material_id
    assert item.service_id is None


def test_quote_item_can_reference_service() -> None:
    service_id = uuid.uuid4()

    item = SalesQuoteItem.create(
        tenant_id=uuid.uuid4(),
        sales_quote_id=uuid.uuid4(),
        sequence=1,
        service_id=service_id,
        description_snapshot="Instalação",
        quantity="1",
        unit_price="800",
    )

    assert item.service_id == service_id
    assert item.material_id is None


def test_quote_item_cannot_reference_material_and_service() -> None:
    with pytest.raises(
        ValueError,
        match="simultaneamente",
    ):
        SalesQuoteItem.create(
            tenant_id=uuid.uuid4(),
            sales_quote_id=uuid.uuid4(),
            sequence=1,
            material_id=uuid.uuid4(),
            service_id=uuid.uuid4(),
            description_snapshot="Item inválido",
            quantity="1",
            unit_price="100",
        )


def test_quote_item_applies_discount() -> None:
    item = SalesQuoteItem.create(
        tenant_id=uuid.uuid4(),
        sales_quote_id=uuid.uuid4(),
        sequence=1,
        description_snapshot="Móvel",
        quantity="2",
        unit_price="1000",
        discount_amount="250",
    )

    assert item.gross_amount == Decimal("2000")
    assert item.total_amount == Decimal("1750")


def test_quote_item_rejects_discount_above_gross_amount() -> None:
    with pytest.raises(
        ValueError,
        match="maior que o valor bruto",
    ):
        SalesQuoteItem.create(
            tenant_id=uuid.uuid4(),
            sales_quote_id=uuid.uuid4(),
            sequence=1,
            description_snapshot="Móvel",
            quantity="1",
            unit_price="100",
            discount_amount="101",
        )


def test_approved_quote_creates_sales_order() -> None:
    quote = create_approved_quote()

    order = SalesOrder.create_from_approved_quote(
        quote=quote,
        code=" ped-001 ",
        delivery_address_snapshot=(
            "Rua Principal, 100 - Rosana/SP"
        ),
    )

    assert order.id is not None
    assert order.code == "PED-001"
    assert order.status is SalesOrderStatus.OPEN
    assert order.source_quote_id == quote.id
    assert order.customer_id == quote.customer_id
    assert order.total_amount == Decimal("5000")
    assert (
        order.payment_terms_snapshot
        == "50% entrada e 50% entrega"
    )


def test_unapproved_quote_cannot_create_sales_order() -> None:
    quote = create_quote()

    with pytest.raises(
        ValueError,
        match="Somente orçamento aprovado",
    ):
        SalesOrder.create_from_approved_quote(
            quote=quote,
            code="PED-001",
        )


def test_sales_order_production_lifecycle() -> None:
    order = SalesOrder.create_from_approved_quote(
        quote=create_approved_quote(),
        code="PED-001",
    )

    order.start_production()

    assert order.status is SalesOrderStatus.IN_PRODUCTION

    order.mark_ready_for_delivery()

    assert (
        order.status
        is SalesOrderStatus.READY_FOR_DELIVERY
    )

    order.mark_delivered()

    assert order.status is SalesOrderStatus.DELIVERED
    assert order.delivered_at is not None

    order.close()

    assert order.status is SalesOrderStatus.CLOSED
    assert order.closed_at is not None


def test_open_sales_order_can_be_cancelled() -> None:
    order = SalesOrder.create_from_approved_quote(
        quote=create_approved_quote(),
        code="PED-001",
    )

    order.cancel()

    assert order.status is SalesOrderStatus.CANCELLED
    assert order.cancelled_at is not None


def test_delivered_sales_order_cannot_be_cancelled() -> None:
    order = SalesOrder.create_from_approved_quote(
        quote=create_approved_quote(),
        code="PED-001",
    )

    order.start_production()
    order.mark_ready_for_delivery()
    order.mark_delivered()

    with pytest.raises(
        ValueError,
        match="não pode ser cancelado",
    ):
        order.cancel()


def test_creates_sales_order_item_snapshot() -> None:
    item = SalesOrderItem.create(
        tenant_id=uuid.uuid4(),
        sales_order_id=uuid.uuid4(),
        source_quote_item_id=uuid.uuid4(),
        sequence=1,
        description_snapshot="Cozinha planejada",
        quantity="1",
        unit_price="5000",
        discount_amount="250",
    )

    assert item.id is not None
    assert item.gross_amount == Decimal("5000")
    assert item.total_amount == Decimal("4750")


def test_sales_order_item_rejects_zero_quantity() -> None:
    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        SalesOrderItem.create(
            tenant_id=uuid.uuid4(),
            sales_order_id=uuid.uuid4(),
            sequence=1,
            description_snapshot="Item",
            quantity="0",
            unit_price="100",
        )
