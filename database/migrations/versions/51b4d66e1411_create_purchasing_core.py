"""Create the tenant-scoped purchasing core.

Revision ID: 51b4d66e1411
Revises: 7b2db4ad5a69
Create Date: 2026-08-07 16:29:36.052161
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "51b4d66e1411"
down_revision: str | Sequence[str] | None = "7b2db4ad5a69"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the modern tenant-scoped purchasing schema."""

    op.create_unique_constraint(
        "uq_suppliers_id_tenant",
        "suppliers",
        [
            "id",
            "tenant_id",
        ],
    )

    op.create_table(
        "purchase_orders",
        sa.Column(
            "supplier_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "branch_id",
            sa.Uuid(),
            nullable=True,
        ),
        sa.Column(
            "code",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=30),
            server_default=sa.text("'DRAFT'"),
            nullable=False,
        ),
        sa.Column(
            "issued_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "expected_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "notes",
            sa.String(length=2000),
            nullable=True,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.CheckConstraint(
            "TRIM(code) <> ''",
            name=op.f(
                "ck_purchase_orders_code_not_blank"
            ),
        ),
        sa.CheckConstraint(
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
            name=op.f(
                "ck_purchase_orders_status_valid"
            ),
        ),
        sa.CheckConstraint(
            (
                "expected_at IS NULL "
                "OR issued_at IS NULL "
                "OR expected_at >= issued_at"
            ),
            name=op.f(
                "ck_purchase_orders_dates_valid"
            ),
        ),
        sa.ForeignKeyConstraint(
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
        sa.ForeignKeyConstraint(
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
        sa.ForeignKeyConstraint(
            [
                "tenant_id",
            ],
            [
                "tenants.id",
            ],
            name=op.f(
                "fk_purchase_orders_tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_purchase_orders"
            ),
        ),
        sa.UniqueConstraint(
            "id",
            "supplier_id",
            "tenant_id",
            name="uq_purchase_orders_id_supplier_tenant",
        ),
        sa.UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_purchase_orders_id_tenant",
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_purchase_orders_tenant_code",
        ),
    )

    op.create_index(
        "ix_purchase_orders_tenant_branch",
        "purchase_orders",
        [
            "tenant_id",
            "branch_id",
        ],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_purchase_orders_tenant_id"
        ),
        "purchase_orders",
        [
            "tenant_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_purchase_orders_tenant_issued",
        "purchase_orders",
        [
            "tenant_id",
            "issued_at",
        ],
        unique=False,
    )

    op.create_index(
        "ix_purchase_orders_tenant_status",
        "purchase_orders",
        [
            "tenant_id",
            "status",
        ],
        unique=False,
    )

    op.create_index(
        "ix_purchase_orders_tenant_supplier",
        "purchase_orders",
        [
            "tenant_id",
            "supplier_id",
        ],
        unique=False,
    )

    op.create_table(
        "purchase_order_items",
        sa.Column(
            "purchase_order_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "sequence",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "material_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "quantity",
            sa.Numeric(
                precision=18,
                scale=6,
            ),
            nullable=False,
        ),
        sa.Column(
            "received_quantity",
            sa.Numeric(
                precision=18,
                scale=6,
            ),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "unit_price",
            sa.Numeric(
                precision=18,
                scale=6,
            ),
            nullable=False,
        ),
        sa.Column(
            "notes",
            sa.String(length=2000),
            nullable=True,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.CheckConstraint(
            "quantity > 0",
            name=op.f(
                "ck_purchase_order_items_quantity_positive"
            ),
        ),
        sa.CheckConstraint(
            "received_quantity <= quantity",
            name=op.f(
                "ck_purchase_order_items_"
                "received_not_above_quantity"
            ),
        ),
        sa.CheckConstraint(
            "received_quantity >= 0",
            name=op.f(
                "ck_purchase_order_items_"
                "received_quantity_non_negative"
            ),
        ),
        sa.CheckConstraint(
            "sequence > 0",
            name=op.f(
                "ck_purchase_order_items_sequence_positive"
            ),
        ),
        sa.CheckConstraint(
            "unit_price >= 0",
            name=op.f(
                "ck_purchase_order_items_"
                "unit_price_non_negative"
            ),
        ),
        sa.ForeignKeyConstraint(
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
        sa.ForeignKeyConstraint(
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
        sa.ForeignKeyConstraint(
            [
                "tenant_id",
            ],
            [
                "tenants.id",
            ],
            name=op.f(
                "fk_purchase_order_items_"
                "tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_purchase_order_items"
            ),
        ),
        sa.UniqueConstraint(
            "id",
            "purchase_order_id",
            "material_id",
            "tenant_id",
            name=(
                "uq_purchase_order_items_"
                "id_order_material_tenant"
            ),
        ),
        sa.UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_purchase_order_items_id_tenant",
        ),
        sa.UniqueConstraint(
            "purchase_order_id",
            "sequence",
            name=(
                "uq_purchase_order_items_"
                "order_sequence"
            ),
        ),
    )

    op.create_index(
        op.f(
            "ix_purchase_order_items_tenant_id"
        ),
        "purchase_order_items",
        [
            "tenant_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_purchase_order_items_tenant_material",
        "purchase_order_items",
        [
            "tenant_id",
            "material_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_purchase_order_items_tenant_order",
        "purchase_order_items",
        [
            "tenant_id",
            "purchase_order_id",
        ],
        unique=False,
    )

    op.create_table(
        "purchase_receipts",
        sa.Column(
            "purchase_order_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "supplier_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "branch_id",
            sa.Uuid(),
            nullable=True,
        ),
        sa.Column(
            "received_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=30),
            server_default=sa.text("'DRAFT'"),
            nullable=False,
        ),
        sa.Column(
            "supplier_document_number",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "notes",
            sa.String(length=2000),
            nullable=True,
        ),
        sa.Column(
            "posted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "cancelled_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.CheckConstraint(
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
            name=op.f(
                "ck_purchase_receipts_"
                "status_dates_consistent"
            ),
        ),
        sa.CheckConstraint(
            (
                "status IN ("
                "'DRAFT', "
                "'POSTED', "
                "'CANCELLED'"
                ")"
            ),
            name=op.f(
                "ck_purchase_receipts_status_valid"
            ),
        ),
        sa.ForeignKeyConstraint(
            [
                "branch_id",
                "tenant_id",
            ],
            [
                "branches.id",
                "branches.tenant_id",
            ],
            name=(
                "fk_purchase_receipts_"
                "branch_tenant"
            ),
        ),
        sa.ForeignKeyConstraint(
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
        sa.ForeignKeyConstraint(
            [
                "tenant_id",
            ],
            [
                "tenants.id",
            ],
            name=op.f(
                "fk_purchase_receipts_"
                "tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_purchase_receipts"
            ),
        ),
        sa.UniqueConstraint(
            "id",
            "purchase_order_id",
            "tenant_id",
            name=(
                "uq_purchase_receipts_"
                "id_order_tenant"
            ),
        ),
        sa.UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_purchase_receipts_id_tenant",
        ),
    )

    op.create_index(
        "ix_purchase_receipts_tenant_branch",
        "purchase_receipts",
        [
            "tenant_id",
            "branch_id",
        ],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_purchase_receipts_tenant_id"
        ),
        "purchase_receipts",
        [
            "tenant_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_purchase_receipts_tenant_order",
        "purchase_receipts",
        [
            "tenant_id",
            "purchase_order_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_purchase_receipts_tenant_received",
        "purchase_receipts",
        [
            "tenant_id",
            "received_at",
        ],
        unique=False,
    )

    op.create_index(
        "ix_purchase_receipts_tenant_status",
        "purchase_receipts",
        [
            "tenant_id",
            "status",
        ],
        unique=False,
    )

    op.create_index(
        "ix_purchase_receipts_tenant_supplier",
        "purchase_receipts",
        [
            "tenant_id",
            "supplier_id",
        ],
        unique=False,
    )

    op.create_table(
        "purchase_receipt_items",
        sa.Column(
            "purchase_receipt_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "purchase_order_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "purchase_order_item_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "material_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "quantity",
            sa.Numeric(
                precision=18,
                scale=6,
            ),
            nullable=False,
        ),
        sa.Column(
            "notes",
            sa.String(length=2000),
            nullable=True,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.CheckConstraint(
            "quantity > 0",
            name=op.f(
                "ck_purchase_receipt_items_"
                "quantity_positive"
            ),
        ),
        sa.ForeignKeyConstraint(
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
        sa.ForeignKeyConstraint(
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
        sa.ForeignKeyConstraint(
            [
                "tenant_id",
            ],
            [
                "tenants.id",
            ],
            name=op.f(
                "fk_purchase_receipt_items_"
                "tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_purchase_receipt_items"
            ),
        ),
    )

    op.create_index(
        op.f(
            "ix_purchase_receipt_items_tenant_id"
        ),
        "purchase_receipt_items",
        [
            "tenant_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_purchase_receipt_items_tenant_material",
        "purchase_receipt_items",
        [
            "tenant_id",
            "material_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_purchase_receipt_items_tenant_order",
        "purchase_receipt_items",
        [
            "tenant_id",
            "purchase_order_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_purchase_receipt_items_tenant_order_item",
        "purchase_receipt_items",
        [
            "tenant_id",
            "purchase_order_item_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_purchase_receipt_items_tenant_receipt",
        "purchase_receipt_items",
        [
            "tenant_id",
            "purchase_receipt_id",
        ],
        unique=False,
    )


def downgrade() -> None:
    """Remove the modern tenant-scoped purchasing schema."""

    op.drop_index(
        "ix_purchase_receipt_items_tenant_receipt",
        table_name="purchase_receipt_items",
    )

    op.drop_index(
        "ix_purchase_receipt_items_tenant_order_item",
        table_name="purchase_receipt_items",
    )

    op.drop_index(
        "ix_purchase_receipt_items_tenant_order",
        table_name="purchase_receipt_items",
    )

    op.drop_index(
        "ix_purchase_receipt_items_tenant_material",
        table_name="purchase_receipt_items",
    )

    op.drop_index(
        op.f(
            "ix_purchase_receipt_items_tenant_id"
        ),
        table_name="purchase_receipt_items",
    )

    op.drop_table(
        "purchase_receipt_items"
    )

    op.drop_index(
        "ix_purchase_receipts_tenant_supplier",
        table_name="purchase_receipts",
    )

    op.drop_index(
        "ix_purchase_receipts_tenant_status",
        table_name="purchase_receipts",
    )

    op.drop_index(
        "ix_purchase_receipts_tenant_received",
        table_name="purchase_receipts",
    )

    op.drop_index(
        "ix_purchase_receipts_tenant_order",
        table_name="purchase_receipts",
    )

    op.drop_index(
        op.f(
            "ix_purchase_receipts_tenant_id"
        ),
        table_name="purchase_receipts",
    )

    op.drop_index(
        "ix_purchase_receipts_tenant_branch",
        table_name="purchase_receipts",
    )

    op.drop_table(
        "purchase_receipts"
    )

    op.drop_index(
        "ix_purchase_order_items_tenant_order",
        table_name="purchase_order_items",
    )

    op.drop_index(
        "ix_purchase_order_items_tenant_material",
        table_name="purchase_order_items",
    )

    op.drop_index(
        op.f(
            "ix_purchase_order_items_tenant_id"
        ),
        table_name="purchase_order_items",
    )

    op.drop_table(
        "purchase_order_items"
    )

    op.drop_index(
        "ix_purchase_orders_tenant_supplier",
        table_name="purchase_orders",
    )

    op.drop_index(
        "ix_purchase_orders_tenant_status",
        table_name="purchase_orders",
    )

    op.drop_index(
        "ix_purchase_orders_tenant_issued",
        table_name="purchase_orders",
    )

    op.drop_index(
        op.f(
            "ix_purchase_orders_tenant_id"
        ),
        table_name="purchase_orders",
    )

    op.drop_index(
        "ix_purchase_orders_tenant_branch",
        table_name="purchase_orders",
    )

    op.drop_table(
        "purchase_orders"
    )

    op.drop_constraint(
        "uq_suppliers_id_tenant",
        "suppliers",
        type_="unique",
    )
