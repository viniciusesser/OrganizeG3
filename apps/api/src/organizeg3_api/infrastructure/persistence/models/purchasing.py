"""SQLAlchemy ORM mappings for purchasing core."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import (
    CheckConstraint,
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


class PurchaseOrderModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one purchase order."""

    __tablename__ = "purchase_orders"

    __table_args__ = (
        CheckConstraint(
            "TRIM(code) <> ''",
            name="code_not_blank",
        ),
        CheckConstraint(
            (
                "status IN ("
                "'DRAFT', "
                "'ISSUED', "
                "'PARTIALLY_RECEIVED', "
                "'RECEIVED', "
                "'CLOSED', "
                "'CANCELLED'"
                ")"
            ),
            name="status_valid",
        ),
        CheckConstraint(
            (
                "expected_at IS NULL "
                "OR issued_at IS NULL "
                "OR expected_at >= issued_at"
            ),
            name="dates_valid",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_purchase_orders_id_tenant",
        ),
        UniqueConstraint(
            "id",
            "supplier_id",
            "tenant_id",
            name="uq_purchase_orders_id_supplier_tenant",
        ),
        UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_purchase_orders_tenant_code",
        ),
        ForeignKeyConstraint(
            [
                "supplier_id",
                "tenant_id",
            ],
            [
                "suppliers.id",
                "suppliers.tenant_id",
            ],
            name="fk_purchase_orders_supplier_tenant",
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
            name="fk_purchase_orders_branch_tenant",
        ),
        Index(
            "ix_purchase_orders_tenant_supplier",
            "tenant_id",
            "supplier_id",
        ),
        Index(
            "ix_purchase_orders_tenant_branch",
            "tenant_id",
            "branch_id",
        ),
        Index(
            "ix_purchase_orders_tenant_status",
            "tenant_id",
            "status",
        ),
        Index(
            "ix_purchase_orders_tenant_issued",
            "tenant_id",
            "issued_at",
        ),
    )

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    branch_id: Mapped[uuid.UUID | None] = mapped_column(
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

    issued_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    expected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )


class PurchaseOrderItemModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one purchase order material item."""

    __tablename__ = "purchase_order_items"

    __table_args__ = (
        CheckConstraint(
            "sequence > 0",
            name="sequence_positive",
        ),
        CheckConstraint(
            "quantity > 0",
            name="quantity_positive",
        ),
        CheckConstraint(
            "received_quantity >= 0",
            name="received_quantity_non_negative",
        ),
        CheckConstraint(
            "received_quantity <= quantity",
            name="received_not_above_quantity",
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="unit_price_non_negative",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_purchase_order_items_id_tenant",
        ),
        UniqueConstraint(
            "id",
            "purchase_order_id",
            "material_id",
            "tenant_id",
            name=(
                "uq_purchase_order_items_"
                "id_order_material_tenant"
            ),
        ),
        UniqueConstraint(
            "purchase_order_id",
            "sequence",
            name=(
                "uq_purchase_order_items_"
                "order_sequence"
            ),
        ),
        ForeignKeyConstraint(
            [
                "purchase_order_id",
                "tenant_id",
            ],
            [
                "purchase_orders.id",
                "purchase_orders.tenant_id",
            ],
            name=(
                "fk_purchase_order_items_"
                "order_tenant"
            ),
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
            name=(
                "fk_purchase_order_items_"
                "material_tenant"
            ),
        ),
        Index(
            "ix_purchase_order_items_tenant_order",
            "tenant_id",
            "purchase_order_id",
        ),
        Index(
            "ix_purchase_order_items_tenant_material",
            "tenant_id",
            "material_id",
        ),
    )

    purchase_order_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    material_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=18,
            scale=6,
        ),
        nullable=False,
    )

    received_quantity: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=18,
            scale=6,
        ),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=18,
            scale=6,
        ),
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )


class PurchaseReceiptModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one physical supplier receipt."""

    __tablename__ = "purchase_receipts"

    __table_args__ = (
        CheckConstraint(
            (
                "status IN ("
                "'DRAFT', "
                "'POSTED', "
                "'CANCELLED'"
                ")"
            ),
            name="status_valid",
        ),
        CheckConstraint(
            (
                "("
                "status = 'DRAFT' "
                "AND posted_at IS NULL "
                "AND cancelled_at IS NULL"
                ") "
                "OR "
                "("
                "status = 'POSTED' "
                "AND posted_at IS NOT NULL "
                "AND cancelled_at IS NULL "
                "AND posted_at >= received_at"
                ") "
                "OR "
                "("
                "status = 'CANCELLED' "
                "AND cancelled_at IS NOT NULL "
                "AND posted_at IS NULL "
                "AND cancelled_at >= received_at"
                ")"
            ),
            name="status_dates_consistent",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_purchase_receipts_id_tenant",
        ),
        UniqueConstraint(
            "id",
            "purchase_order_id",
            "tenant_id",
            name=(
                "uq_purchase_receipts_"
                "id_order_tenant"
            ),
        ),
        ForeignKeyConstraint(
            [
                "purchase_order_id",
                "supplier_id",
                "tenant_id",
            ],
            [
                "purchase_orders.id",
                "purchase_orders.supplier_id",
                "purchase_orders.tenant_id",
            ],
            name=(
                "fk_purchase_receipts_"
                "order_supplier_tenant"
            ),
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
            name=(
                "fk_purchase_receipts_branch_tenant"
            ),
        ),
        Index(
            "ix_purchase_receipts_tenant_order",
            "tenant_id",
            "purchase_order_id",
        ),
        Index(
            "ix_purchase_receipts_tenant_supplier",
            "tenant_id",
            "supplier_id",
        ),
        Index(
            "ix_purchase_receipts_tenant_branch",
            "tenant_id",
            "branch_id",
        ),
        Index(
            "ix_purchase_receipts_tenant_status",
            "tenant_id",
            "status",
        ),
        Index(
            "ix_purchase_receipts_tenant_received",
            "tenant_id",
            "received_at",
        ),
    )

    purchase_order_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DRAFT",
        server_default=text("'DRAFT'"),
    )

    supplier_document_number: Mapped[
        str | None
    ] = mapped_column(
        String(100),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )

    posted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    cancelled_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class PurchaseReceiptItemModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one material quantity received."""

    __tablename__ = "purchase_receipt_items"

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="quantity_positive",
        ),
        ForeignKeyConstraint(
            [
                "purchase_receipt_id",
                "purchase_order_id",
                "tenant_id",
            ],
            [
                "purchase_receipts.id",
                "purchase_receipts.purchase_order_id",
                "purchase_receipts.tenant_id",
            ],
            name=(
                "fk_purchase_receipt_items_"
                "receipt_order_tenant"
            ),
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            [
                "purchase_order_item_id",
                "purchase_order_id",
                "material_id",
                "tenant_id",
            ],
            [
                "purchase_order_items.id",
                "purchase_order_items.purchase_order_id",
                "purchase_order_items.material_id",
                "purchase_order_items.tenant_id",
            ],
            name=(
                "fk_purchase_receipt_items_"
                "order_item_order_material_tenant"
            ),
        ),
        Index(
            "ix_purchase_receipt_items_tenant_receipt",
            "tenant_id",
            "purchase_receipt_id",
        ),
        Index(
            "ix_purchase_receipt_items_tenant_order",
            "tenant_id",
            "purchase_order_id",
        ),
        Index(
            "ix_purchase_receipt_items_tenant_order_item",
            "tenant_id",
            "purchase_order_item_id",
        ),
        Index(
            "ix_purchase_receipt_items_tenant_material",
            "tenant_id",
            "material_id",
        ),
    )

    purchase_receipt_id: Mapped[
        uuid.UUID
    ] = mapped_column(
        Uuid,
        nullable=False,
    )

    purchase_order_id: Mapped[
        uuid.UUID
    ] = mapped_column(
        Uuid,
        nullable=False,
    )

    purchase_order_item_id: Mapped[
        uuid.UUID
    ] = mapped_column(
        Uuid,
        nullable=False,
    )

    material_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=18,
            scale=6,
        ),
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )
