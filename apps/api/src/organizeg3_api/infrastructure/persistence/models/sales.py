"""SQLAlchemy ORM mappings for the modern sales domain."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
import uuid

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from organizeg3_api.infrastructure.database.base import (
    Base,
    TenantScopedMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class SalesQuoteModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist a tenant-scoped commercial quote."""

    __tablename__ = "sales_quotes"

    __table_args__ = (
        CheckConstraint(
            "TRIM(code) <> ''",
            name="code_not_blank",
        ),
        CheckConstraint(
            "TRIM(project_name) <> ''",
            name="project_name_not_blank",
        ),
        CheckConstraint(
            (
                "status IN ("
                "'DRAFT', "
                "'SENT', "
                "'NEGOTIATION', "
                "'APPROVED', "
                "'REJECTED', "
                "'CANCELLED', "
                "'EXPIRED'"
                ")"
            ),
            name="status_valid",
        ),
        CheckConstraint(
            "material_cost >= 0",
            name="material_cost_non_negative",
        ),
        CheckConstraint(
            "labor_cost >= 0",
            name="labor_cost_non_negative",
        ),
        CheckConstraint(
            "transport_cost >= 0",
            name="transport_cost_non_negative",
        ),
        CheckConstraint(
            "other_cost >= 0",
            name="other_cost_non_negative",
        ),
        CheckConstraint(
            "tax_amount >= 0",
            name="tax_amount_non_negative",
        ),
        CheckConstraint(
            "discount_amount >= 0",
            name="discount_amount_non_negative",
        ),
        CheckConstraint(
            "proposed_amount >= 0",
            name="proposed_amount_non_negative",
        ),
        CheckConstraint(
            (
                "approved_amount IS NULL "
                "OR approved_amount > 0"
            ),
            name="approved_amount_positive",
        ),
        CheckConstraint(
            (
                "valid_until IS NULL "
                "OR issued_at IS NULL "
                "OR valid_until >= CAST(issued_at AS DATE)"
            ),
            name="validity_dates_valid",
        ),
        CheckConstraint(
            (
                "(status <> 'APPROVED') "
                "OR (approved_amount IS NOT NULL "
                "AND approved_at IS NOT NULL)"
            ),
            name="approved_state_valid",
        ),
        CheckConstraint(
            (
                "(status <> 'REJECTED') "
                "OR rejected_at IS NOT NULL"
            ),
            name="rejected_state_valid",
        ),
        CheckConstraint(
            (
                "(status <> 'CANCELLED') "
                "OR cancelled_at IS NOT NULL"
            ),
            name="cancelled_state_valid",
        ),
        CheckConstraint(
            (
                "(status <> 'EXPIRED') "
                "OR expired_at IS NOT NULL"
            ),
            name="expired_state_valid",
        ),
        ForeignKeyConstraint(
            [
                "customer_id",
                "tenant_id",
            ],
            [
                "clientes.id",
                "clientes.tenant_id",
            ],
            name="fk_sales_quotes_customer_tenant",
        ),
        ForeignKeyConstraint(
            [
                "branch_id",
                "tenant_id",
            ],
            [
                "branches.id",
                "branches.tenant_id",
            ],
            name="fk_sales_quotes_branch_tenant",
        ),
        ForeignKeyConstraint(
            [
                "salesperson_employee_id",
                "tenant_id",
            ],
            [
                "employees.id",
                "employees.tenant_id",
            ],
            name="fk_sales_quotes_salesperson_tenant",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_sales_quotes_id_tenant",
        ),
        UniqueConstraint(
            "id",
            "customer_id",
            "tenant_id",
            name="uq_sales_quotes_id_customer_tenant",
        ),
        UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_sales_quotes_tenant_code",
        ),
        Index(
            "ix_sales_quotes_tenant_customer",
            "tenant_id",
            "customer_id",
        ),
        Index(
            "ix_sales_quotes_tenant_branch",
            "tenant_id",
            "branch_id",
        ),
        Index(
            "ix_sales_quotes_tenant_salesperson",
            "tenant_id",
            "salesperson_employee_id",
        ),
        Index(
            "ix_sales_quotes_tenant_status",
            "tenant_id",
            "status",
        ),
        Index(
            "ix_sales_quotes_tenant_issued",
            "tenant_id",
            "issued_at",
        ),
    )

    customer_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )

    salesperson_employee_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DRAFT",
        server_default=text("'DRAFT'"),
    )

    project_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(4000),
        nullable=True,
    )

    issued_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    valid_until: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    expected_delivery_at: Mapped[
        date | None
    ] = mapped_column(
        Date,
        nullable=True,
    )

    payment_terms: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        String(4000),
        nullable=True,
    )

    material_cost: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
    )

    labor_cost: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
    )

    transport_cost: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
    )

    other_cost: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
    )

    proposed_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
    )

    approved_amount: Mapped[
        Decimal | None
    ] = mapped_column(
        Numeric(18, 6),
        nullable=True,
    )

    approved_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    rejected_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    cancelled_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    expired_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class SalesQuoteItemModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one commercial quote line."""

    __tablename__ = "sales_quote_items"

    __table_args__ = (
        CheckConstraint(
            "sequence > 0",
            name="sequence_positive",
        ),
        CheckConstraint(
            "TRIM(description_snapshot) <> ''",
            name="description_not_blank",
        ),
        CheckConstraint(
            "quantity > 0",
            name="quantity_positive",
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="unit_price_non_negative",
        ),
        CheckConstraint(
            "discount_amount >= 0",
            name="discount_non_negative",
        ),
        CheckConstraint(
            (
                "discount_amount "
                "<= quantity * unit_price"
            ),
            name="discount_not_above_gross",
        ),
        CheckConstraint(
            (
                "NOT ("
                "material_id IS NOT NULL "
                "AND service_id IS NOT NULL"
                ")"
            ),
            name="catalog_reference_exclusive",
        ),
        ForeignKeyConstraint(
            [
                "sales_quote_id",
                "tenant_id",
            ],
            [
                "sales_quotes.id",
                "sales_quotes.tenant_id",
            ],
            name="fk_sales_quote_items_quote_tenant",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            [
                "material_id",
                "tenant_id",
            ],
            [
                "materials.id",
                "materials.tenant_id",
            ],
            name="fk_sales_quote_items_material_tenant",
        ),
        ForeignKeyConstraint(
            [
                "service_id",
                "tenant_id",
            ],
            [
                "services.id",
                "services.tenant_id",
            ],
            name="fk_sales_quote_items_service_tenant",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_sales_quote_items_id_tenant",
        ),
        UniqueConstraint(
            "id",
            "sales_quote_id",
            "tenant_id",
            name="uq_sales_quote_items_id_quote_tenant",
        ),
        UniqueConstraint(
            "sales_quote_id",
            "sequence",
            name="uq_sales_quote_items_quote_sequence",
        ),
        Index(
            "ix_sales_quote_items_tenant_quote",
            "tenant_id",
            "sales_quote_id",
        ),
        Index(
            "ix_sales_quote_items_tenant_material",
            "tenant_id",
            "material_id",
        ),
        Index(
            "ix_sales_quote_items_tenant_service",
            "tenant_id",
            "service_id",
        ),
    )

    sales_quote_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    material_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    service_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    description_snapshot: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
    )


class SalesOrderModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist a confirmed customer sales order."""

    __tablename__ = "sales_orders"

    __table_args__ = (
        CheckConstraint(
            "TRIM(code) <> ''",
            name="code_not_blank",
        ),
        CheckConstraint(
            (
                "status IN ("
                "'OPEN', "
                "'IN_PRODUCTION', "
                "'READY_FOR_DELIVERY', "
                "'DELIVERED', "
                "'CLOSED', "
                "'CANCELLED'"
                ")"
            ),
            name="status_valid",
        ),
        CheckConstraint(
            "total_amount > 0",
            name="total_amount_positive",
        ),
        CheckConstraint(
            (
                "(status <> 'DELIVERED') "
                "OR delivered_at IS NOT NULL"
            ),
            name="delivered_state_valid",
        ),
        CheckConstraint(
            (
                "(status <> 'CLOSED') "
                "OR closed_at IS NOT NULL"
            ),
            name="closed_state_valid",
        ),
        CheckConstraint(
            (
                "(status <> 'CANCELLED') "
                "OR cancelled_at IS NOT NULL"
            ),
            name="cancelled_state_valid",
        ),
        ForeignKeyConstraint(
            [
                "source_quote_id",
                "customer_id",
                "tenant_id",
            ],
            [
                "sales_quotes.id",
                "sales_quotes.customer_id",
                "sales_quotes.tenant_id",
            ],
            name=(
                "fk_sales_orders_quote_customer_tenant"
            ),
        ),
        ForeignKeyConstraint(
            [
                "customer_id",
                "tenant_id",
            ],
            [
                "clientes.id",
                "clientes.tenant_id",
            ],
            name="fk_sales_orders_customer_tenant",
        ),
        ForeignKeyConstraint(
            [
                "branch_id",
                "tenant_id",
            ],
            [
                "branches.id",
                "branches.tenant_id",
            ],
            name="fk_sales_orders_branch_tenant",
        ),
        ForeignKeyConstraint(
            [
                "salesperson_employee_id",
                "tenant_id",
            ],
            [
                "employees.id",
                "employees.tenant_id",
            ],
            name="fk_sales_orders_salesperson_tenant",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_sales_orders_id_tenant",
        ),
        UniqueConstraint(
            "id",
            "source_quote_id",
            "tenant_id",
            name="uq_sales_orders_id_quote_tenant",
        ),
        UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_sales_orders_tenant_code",
        ),
        UniqueConstraint(
            "tenant_id",
            "source_quote_id",
            name="uq_sales_orders_tenant_source_quote",
        ),
        Index(
            "ix_sales_orders_tenant_customer",
            "tenant_id",
            "customer_id",
        ),
        Index(
            "ix_sales_orders_tenant_branch",
            "tenant_id",
            "branch_id",
        ),
        Index(
            "ix_sales_orders_tenant_salesperson",
            "tenant_id",
            "salesperson_employee_id",
        ),
        Index(
            "ix_sales_orders_tenant_status",
            "tenant_id",
            "status",
        ),
        Index(
            "ix_sales_orders_tenant_ordered",
            "tenant_id",
            "ordered_at",
        ),
    )

    source_quote_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    customer_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    branch_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    salesperson_employee_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="OPEN",
        server_default=text("'OPEN'"),
    )

    ordered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    project_name_snapshot: Mapped[
        str | None
    ] = mapped_column(
        String(255),
        nullable=True,
    )

    expected_delivery_at: Mapped[
        date | None
    ] = mapped_column(
        Date,
        nullable=True,
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
    )

    payment_terms_snapshot: Mapped[
        str | None
    ] = mapped_column(
        String(2000),
        nullable=True,
    )

    delivery_address_snapshot: Mapped[
        str | None
    ] = mapped_column(
        String(2000),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        String(4000),
        nullable=True,
    )

    cancelled_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    delivered_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    closed_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class SalesOrderItemModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one confirmed sales order line."""

    __tablename__ = "sales_order_items"

    __table_args__ = (
        CheckConstraint(
            "sequence > 0",
            name="sequence_positive",
        ),
        CheckConstraint(
            "TRIM(description_snapshot) <> ''",
            name="description_not_blank",
        ),
        CheckConstraint(
            "quantity > 0",
            name="quantity_positive",
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="unit_price_non_negative",
        ),
        CheckConstraint(
            "discount_amount >= 0",
            name="discount_non_negative",
        ),
        CheckConstraint(
            (
                "discount_amount "
                "<= quantity * unit_price"
            ),
            name="discount_not_above_gross",
        ),
        CheckConstraint(
            (
                "NOT ("
                "material_id IS NOT NULL "
                "AND service_id IS NOT NULL"
                ")"
            ),
            name="catalog_reference_exclusive",
        ),
        ForeignKeyConstraint(
            [
                "sales_order_id",
                "source_quote_id",
                "tenant_id",
            ],
            [
                "sales_orders.id",
                "sales_orders.source_quote_id",
                "sales_orders.tenant_id",
            ],
            name=(
                "fk_sales_order_items_"
                "order_quote_tenant"
            ),
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            [
                "source_quote_item_id",
                "source_quote_id",
                "tenant_id",
            ],
            [
                "sales_quote_items.id",
                "sales_quote_items.sales_quote_id",
                "sales_quote_items.tenant_id",
            ],
            name=(
                "fk_sales_order_items_"
                "quote_item_quote_tenant"
            ),
        ),
        ForeignKeyConstraint(
            [
                "material_id",
                "tenant_id",
            ],
            [
                "materials.id",
                "materials.tenant_id",
            ],
            name="fk_sales_order_items_material_tenant",
        ),
        ForeignKeyConstraint(
            [
                "service_id",
                "tenant_id",
            ],
            [
                "services.id",
                "services.tenant_id",
            ],
            name="fk_sales_order_items_service_tenant",
        ),
        UniqueConstraint(
            "sales_order_id",
            "sequence",
            name="uq_sales_order_items_order_sequence",
        ),
        Index(
            "ix_sales_order_items_tenant_order",
            "tenant_id",
            "sales_order_id",
        ),
        Index(
            "ix_sales_order_items_tenant_quote_item",
            "tenant_id",
            "source_quote_item_id",
        ),
        Index(
            "ix_sales_order_items_tenant_material",
            "tenant_id",
            "material_id",
        ),
        Index(
            "ix_sales_order_items_tenant_service",
            "tenant_id",
            "service_id",
        ),
    )

    sales_order_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    source_quote_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    source_quote_item_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    material_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    service_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    description_snapshot: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
    )
