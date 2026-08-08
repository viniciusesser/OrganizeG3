"""Integration tests for modern sales repositories."""

from __future__ import annotations

from decimal import Decimal
import uuid

import pytest
from sqlalchemy.orm import Session

from organizeg3_api.domain.sales.order import (
    SalesOrder,
    SalesOrderItem,
)
from organizeg3_api.domain.sales.quote import (
    SalesQuote,
    SalesQuoteItem,
)
from organizeg3_api.infrastructure.persistence.models.branch import (
    BranchModel,
)
from organizeg3_api.infrastructure.persistence.models.customer import (
    CustomerModel,
)
from organizeg3_api.infrastructure.persistence.models.material import (
    MaterialModel,
)
from organizeg3_api.infrastructure.persistence.models.service import (
    ServiceModel,
)
from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories.sales_repository import (
    SQLAlchemySalesOrderItemRepository,
    SQLAlchemySalesOrderRepository,
    SQLAlchemySalesQuoteItemRepository,
    SQLAlchemySalesQuoteRepository,
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


def create_customer(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "CLI-001",
) -> CustomerModel:
    customer = CustomerModel(
        tenant_id=tenant_id,
        code=code,
        name=f"Cliente {code}",
        customer_type="INDIVIDUAL",
        is_active=True,
    )

    session.add(customer)
    session.flush()

    return customer


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


def create_service(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "SER-001",
) -> ServiceModel:
    service = ServiceModel(
        tenant_id=tenant_id,
        code=code,
        name=f"Serviço {code}",
        category="MARCENARIA",
        unit="UN",
        execution_mode="INTERNAL",
        is_active=True,
    )

    session.add(service)
    session.flush()

    return service


def create_quote(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    customer_id: int,
    code: str = "ORC-001",
) -> SalesQuote:
    repository = SQLAlchemySalesQuoteRepository(
        session
    )

    return repository.add(
        SalesQuote.create(
            tenant_id=tenant_id,
            customer_id=customer_id,
            code=code,
            project_name="Cozinha planejada",
            proposed_amount="6000",
        )
    )


def create_approved_quote(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    customer_id: int,
    code: str = "ORC-001",
) -> SalesQuote:
    quote = SalesQuote.create(
        tenant_id=tenant_id,
        customer_id=customer_id,
        code=code,
        project_name="Cozinha planejada",
        proposed_amount="6000",
    )

    quote.issue()
    quote.approve(
        approved_amount="5000"
    )

    repository = SQLAlchemySalesQuoteRepository(
        session
    )

    return repository.add(quote)


def test_persists_sales_quote(
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

    repository = SQLAlchemySalesQuoteRepository(
        session
    )

    saved = create_quote(
        session,
        tenant_id=tenant_id,
        customer_id=customer.id,
    )

    assert saved.id is not None

    loaded = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        sales_quote_id=saved.id,
    )

    assert loaded is not None
    assert loaded.code == "ORC-001"
    assert loaded.customer_id == customer.id


def test_sales_quote_code_is_tenant_scoped(
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
        tenant_id=tenant_id,
    )

    create_quote(
        session,
        tenant_id=tenant_id,
        customer_id=customer.id,
    )

    repository = SQLAlchemySalesQuoteRepository(
        session
    )

    assert (
        repository.get_by_code_for_tenant(
            tenant_id=tenant_id,
            code=" orc-001 ",
        )
        is not None
    )

    assert (
        repository.get_by_code_for_tenant(
            tenant_id=other_tenant_id,
            code="ORC-001",
        )
        is None
    )


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

    quote = SalesQuote.create(
        tenant_id=tenant_id,
        customer_id=customer.id,
        code="ORC-001",
        project_name="Projeto",
        proposed_amount="1000",
    )

    repository = SQLAlchemySalesQuoteRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="cliente",
    ):
        repository.add(quote)


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

    customer = create_customer(
        session,
        tenant_id=tenant_id,
    )

    branch = create_branch(
        session,
        tenant_id=other_tenant_id,
    )

    quote = SalesQuote.create(
        tenant_id=tenant_id,
        customer_id=customer.id,
        branch_id=branch.id,
        code="ORC-001",
        project_name="Projeto",
        proposed_amount="1000",
    )

    repository = SQLAlchemySalesQuoteRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="filial",
    ):
        repository.add(quote)


def test_persists_free_form_quote_item(
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

    quote = create_quote(
        session,
        tenant_id=tenant_id,
        customer_id=customer.id,
    )

    assert quote.id is not None

    item = SalesQuoteItem.create(
        tenant_id=tenant_id,
        sales_quote_id=quote.id,
        sequence=1,
        description_snapshot="Móvel planejado",
        quantity="1",
        unit_price="5000",
    )

    repository = SQLAlchemySalesQuoteItemRepository(
        session
    )

    saved = repository.add(item)

    assert saved.id is not None
    assert saved.quantity == Decimal("1.000000")
    assert saved.total_amount == Decimal("5000.000000")


def test_persists_material_quote_item(
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

    material = create_material(
        session,
        tenant_id=tenant_id,
    )

    quote = create_quote(
        session,
        tenant_id=tenant_id,
        customer_id=customer.id,
    )

    assert quote.id is not None

    repository = SQLAlchemySalesQuoteItemRepository(
        session
    )

    saved = repository.add(
        SalesQuoteItem.create(
            tenant_id=tenant_id,
            sales_quote_id=quote.id,
            sequence=1,
            material_id=material.id,
            description_snapshot="MDF Branco",
            quantity="5",
            unit_price="250",
        )
    )

    assert saved.material_id == material.id


def test_rejects_cross_tenant_quote_item_material(
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
        tenant_id=tenant_id,
    )

    material = create_material(
        session,
        tenant_id=other_tenant_id,
    )

    quote = create_quote(
        session,
        tenant_id=tenant_id,
        customer_id=customer.id,
    )

    assert quote.id is not None

    item = SalesQuoteItem.create(
        tenant_id=tenant_id,
        sales_quote_id=quote.id,
        sequence=1,
        material_id=material.id,
        description_snapshot="MDF",
        quantity="1",
        unit_price="100",
    )

    repository = SQLAlchemySalesQuoteItemRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="material",
    ):
        repository.add(item)


def test_persists_service_quote_item(
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

    service = create_service(
        session,
        tenant_id=tenant_id,
    )

    quote = create_quote(
        session,
        tenant_id=tenant_id,
        customer_id=customer.id,
    )

    assert quote.id is not None

    repository = SQLAlchemySalesQuoteItemRepository(
        session
    )

    saved = repository.add(
        SalesQuoteItem.create(
            tenant_id=tenant_id,
            sales_quote_id=quote.id,
            sequence=1,
            service_id=service.id,
            description_snapshot="Instalação",
            quantity="1",
            unit_price="800",
        )
    )

    assert saved.service_id == service.id


def test_persists_sales_order_from_approved_quote(
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

    quote = create_approved_quote(
        session,
        tenant_id=tenant_id,
        customer_id=customer.id,
    )

    order = SalesOrder.create_from_approved_quote(
        quote=quote,
        code="PED-001",
    )

    repository = SQLAlchemySalesOrderRepository(
        session
    )

    saved = repository.add(order)

    assert saved.id is not None
    assert saved.source_quote_id == quote.id
    assert saved.total_amount == Decimal("5000.000000")

    loaded = repository.get_by_source_quote_for_tenant(
        tenant_id=tenant_id,
        sales_quote_id=quote.id,
    )

    assert loaded is not None
    assert loaded.code == "PED-001"


def test_rejects_order_from_unapproved_quote(
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

    quote = create_quote(
        session,
        tenant_id=tenant_id,
        customer_id=customer.id,
    )

    assert quote.id is not None

    quote.issue()
    quote.approve(
        approved_amount="5000"
    )

    order = SalesOrder.create_from_approved_quote(
        quote=quote,
        code="PED-001",
    )

    repository = SQLAlchemySalesOrderRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="aprovado",
    ):
        repository.add(order)


def test_rejects_second_order_for_same_quote(
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

    quote = create_approved_quote(
        session,
        tenant_id=tenant_id,
        customer_id=customer.id,
    )

    first = SalesOrder.create_from_approved_quote(
        quote=quote,
        code="PED-001",
    )

    second = SalesOrder.create_from_approved_quote(
        quote=quote,
        code="PED-002",
    )

    repository = SQLAlchemySalesOrderRepository(
        session
    )

    repository.add(first)

    with pytest.raises(
        ValueError,
        match="já possui pedido",
    ):
        repository.add(second)


def test_persists_sales_order_item_from_quote_item(
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

    material = create_material(
        session,
        tenant_id=tenant_id,
    )

    quote = create_approved_quote(
        session,
        tenant_id=tenant_id,
        customer_id=customer.id,
    )

    assert quote.id is not None

    quote_item_repository = (
        SQLAlchemySalesQuoteItemRepository(
            session
        )
    )

    quote_item = quote_item_repository.add(
        SalesQuoteItem.create(
            tenant_id=tenant_id,
            sales_quote_id=quote.id,
            sequence=1,
            material_id=material.id,
            description_snapshot="MDF Branco",
            quantity="5",
            unit_price="250",
        )
    )

    assert quote_item.id is not None

    order_repository = SQLAlchemySalesOrderRepository(
        session
    )

    order = order_repository.add(
        SalesOrder.create_from_approved_quote(
            quote=quote,
            code="PED-001",
        )
    )

    assert order.id is not None

    repository = SQLAlchemySalesOrderItemRepository(
        session
    )

    saved = repository.add(
        SalesOrderItem.create(
            tenant_id=tenant_id,
            sales_order_id=order.id,
            source_quote_item_id=quote_item.id,
            sequence=1,
            material_id=material.id,
            description_snapshot="MDF Branco",
            quantity="5",
            unit_price="250",
        )
    )

    assert saved.id is not None
    assert saved.source_quote_item_id == quote_item.id


def test_rejects_order_item_from_different_quote(
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

    quote_a = create_approved_quote(
        session,
        tenant_id=tenant_id,
        customer_id=customer.id,
        code="ORC-A",
    )

    quote_b = create_approved_quote(
        session,
        tenant_id=tenant_id,
        customer_id=customer.id,
        code="ORC-B",
    )

    assert quote_a.id is not None
    assert quote_b.id is not None

    quote_item_repository = (
        SQLAlchemySalesQuoteItemRepository(
            session
        )
    )

    quote_item_b = quote_item_repository.add(
        SalesQuoteItem.create(
            tenant_id=tenant_id,
            sales_quote_id=quote_b.id,
            sequence=1,
            description_snapshot="Outro item",
            quantity="1",
            unit_price="100",
        )
    )

    assert quote_item_b.id is not None

    order_repository = SQLAlchemySalesOrderRepository(
        session
    )

    order_a = order_repository.add(
        SalesOrder.create_from_approved_quote(
            quote=quote_a,
            code="PED-A",
        )
    )

    assert order_a.id is not None

    item = SalesOrderItem.create(
        tenant_id=tenant_id,
        sales_order_id=order_a.id,
        source_quote_item_id=quote_item_b.id,
        sequence=1,
        description_snapshot="Outro item",
        quantity="1",
        unit_price="100",
    )

    repository = SQLAlchemySalesOrderItemRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="não pertence ao orçamento",
    ):
        repository.add(item)
