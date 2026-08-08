"""Create the tenant-scoped inventory core.

Revision ID: 7b2db4ad5a69
Revises: 49b92745c01a
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "7b2db4ad5a69"
down_revision: str | Sequence[str] | None = "49b92745c01a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the modern inventory core."""

    # Required before composite tenant-safe material foreign keys.
    op.create_unique_constraint(
        "uq_materials_id_tenant",
        "materials",
        [
            "id",
            "tenant_id",
        ],
    )

    op.create_table(
        "inventory_locations",
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
            "name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "location_type",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.String(length=1000),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
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
                "ck_inventory_locations_code_not_blank"
            ),
        ),
        sa.CheckConstraint(
            (
                "location_type IN ("
                "'WAREHOUSE', "
                "'PRODUCTION', "
                "'CUTTING', "
                "'RECEIVING', "
                "'SHIPPING', "
                "'OTHER'"
                ")"
            ),
            name=op.f(
                "ck_inventory_locations_location_type_valid"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(name) <> ''",
            name=op.f(
                "ck_inventory_locations_name_not_blank"
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
            name="fk_inventory_locations_branch_tenant",
        ),
        sa.ForeignKeyConstraint(
            [
                "tenant_id",
            ],
            [
                "tenants.id",
            ],
            name=op.f(
                "fk_inventory_locations_tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_inventory_locations"
            ),
        ),
        sa.UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_inventory_locations_id_tenant",
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_inventory_locations_tenant_code",
        ),
    )

    op.create_index(
        "ix_inventory_locations_tenant_active",
        "inventory_locations",
        [
            "tenant_id",
            "is_active",
        ],
        unique=False,
    )

    op.create_index(
        "ix_inventory_locations_tenant_branch",
        "inventory_locations",
        [
            "tenant_id",
            "branch_id",
        ],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_inventory_locations_tenant_id"
        ),
        "inventory_locations",
        [
            "tenant_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_inventory_locations_tenant_name",
        "inventory_locations",
        [
            "tenant_id",
            "name",
        ],
        unique=False,
    )

    op.create_index(
        "ix_inventory_locations_tenant_type",
        "inventory_locations",
        [
            "tenant_id",
            "location_type",
        ],
        unique=False,
    )

    op.create_table(
        "inventory_balances",
        sa.Column(
            "location_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "material_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "on_hand_quantity",
            sa.Numeric(
                precision=18,
                scale=6,
            ),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "reserved_quantity",
            sa.Numeric(
                precision=18,
                scale=6,
            ),
            server_default=sa.text("0"),
            nullable=False,
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
            "on_hand_quantity >= 0",
            name=op.f(
                "ck_inventory_balances_"
                "on_hand_quantity_non_negative"
            ),
        ),
        sa.CheckConstraint(
            (
                "reserved_quantity "
                "<= on_hand_quantity"
            ),
            name=op.f(
                "ck_inventory_balances_"
                "reserved_not_above_on_hand"
            ),
        ),
        sa.CheckConstraint(
            "reserved_quantity >= 0",
            name=op.f(
                "ck_inventory_balances_"
                "reserved_quantity_non_negative"
            ),
        ),
        sa.ForeignKeyConstraint(
            [
                "location_id",
                "tenant_id",
            ],
            [
                "inventory_locations.id",
                "inventory_locations.tenant_id",
            ],
            name=(
                "fk_inventory_balances_location_tenant"
            ),
            ondelete="CASCADE",
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
                "fk_inventory_balances_material_tenant"
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
                "fk_inventory_balances_tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_inventory_balances"
            ),
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "location_id",
            "material_id",
            name=(
                "uq_inventory_balances_"
                "tenant_location_material"
            ),
        ),
    )

    op.create_index(
        op.f(
            "ix_inventory_balances_tenant_id"
        ),
        "inventory_balances",
        [
            "tenant_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_inventory_balances_tenant_location",
        "inventory_balances",
        [
            "tenant_id",
            "location_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_inventory_balances_tenant_material",
        "inventory_balances",
        [
            "tenant_id",
            "material_id",
        ],
        unique=False,
    )

    op.create_table(
        "inventory_movements",
        sa.Column(
            "material_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "movement_type",
            sa.String(length=30),
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
            "source_location_id",
            sa.Uuid(),
            nullable=True,
        ),
        sa.Column(
            "destination_location_id",
            sa.Uuid(),
            nullable=True,
        ),
        sa.Column(
            "reference_type",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "reference_id",
            sa.Uuid(),
            nullable=True,
        ),
        sa.Column(
            "notes",
            sa.String(length=2000),
            nullable=True,
        ),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            nullable=False,
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
                "movement_type IN "
                "('RECEIPT', "
                "'ADJUSTMENT_IN', "
                "'RETURN_IN') "
                "AND source_location_id IS NULL "
                "AND destination_location_id IS NOT NULL"
                ") "
                "OR "
                "("
                "movement_type IN "
                "('ISSUE', "
                "'ADJUSTMENT_OUT', "
                "'RETURN_OUT') "
                "AND source_location_id IS NOT NULL "
                "AND destination_location_id IS NULL"
                ") "
                "OR "
                "("
                "movement_type = 'TRANSFER' "
                "AND source_location_id IS NOT NULL "
                "AND destination_location_id IS NOT NULL "
                "AND source_location_id "
                "<> destination_location_id"
                ")"
            ),
            name=op.f(
                "ck_inventory_movements_locations_consistent"
            ),
        ),
        sa.CheckConstraint(
            (
                "movement_type IN ("
                "'RECEIPT', "
                "'ISSUE', "
                "'TRANSFER', "
                "'ADJUSTMENT_IN', "
                "'ADJUSTMENT_OUT', "
                "'RETURN_IN', "
                "'RETURN_OUT'"
                ")"
            ),
            name=op.f(
                "ck_inventory_movements_movement_type_valid"
            ),
        ),
        sa.CheckConstraint(
            "quantity > 0",
            name=op.f(
                "ck_inventory_movements_quantity_positive"
            ),
        ),
        sa.ForeignKeyConstraint(
            [
                "destination_location_id",
                "tenant_id",
            ],
            [
                "inventory_locations.id",
                "inventory_locations.tenant_id",
            ],
            name=(
                "fk_inventory_movements_"
                "destination_location_tenant"
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
                "fk_inventory_movements_material_tenant"
            ),
        ),
        sa.ForeignKeyConstraint(
            [
                "source_location_id",
                "tenant_id",
            ],
            [
                "inventory_locations.id",
                "inventory_locations.tenant_id",
            ],
            name=(
                "fk_inventory_movements_"
                "source_location_tenant"
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
                "fk_inventory_movements_tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_inventory_movements"
            ),
        ),
    )

    op.create_index(
        "ix_inventory_movements_reference",
        "inventory_movements",
        [
            "tenant_id",
            "reference_type",
            "reference_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_inventory_movements_tenant_destination",
        "inventory_movements",
        [
            "tenant_id",
            "destination_location_id",
        ],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_inventory_movements_tenant_id"
        ),
        "inventory_movements",
        [
            "tenant_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_inventory_movements_tenant_material",
        "inventory_movements",
        [
            "tenant_id",
            "material_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_inventory_movements_tenant_occurred",
        "inventory_movements",
        [
            "tenant_id",
            "occurred_at",
        ],
        unique=False,
    )

    op.create_index(
        "ix_inventory_movements_tenant_source",
        "inventory_movements",
        [
            "tenant_id",
            "source_location_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_inventory_movements_tenant_type",
        "inventory_movements",
        [
            "tenant_id",
            "movement_type",
        ],
        unique=False,
    )

    op.create_table(
        "inventory_reservations",
        sa.Column(
            "location_id",
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
            "consumed_quantity",
            sa.Numeric(
                precision=18,
                scale=6,
            ),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=30),
            server_default=sa.text("'ACTIVE'"),
            nullable=False,
        ),
        sa.Column(
            "reference_type",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "reference_id",
            sa.Uuid(),
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
            (
                "consumed_quantity "
                "<= quantity"
            ),
            name=op.f(
                "ck_inventory_reservations_"
                "consumed_not_above_quantity"
            ),
        ),
        sa.CheckConstraint(
            "consumed_quantity >= 0",
            name=op.f(
                "ck_inventory_reservations_"
                "consumed_quantity_non_negative"
            ),
        ),
        sa.CheckConstraint(
            "quantity > 0",
            name=op.f(
                "ck_inventory_reservations_quantity_positive"
            ),
        ),
        sa.CheckConstraint(
            (
                "("
                "status = 'ACTIVE' "
                "AND consumed_quantity = 0"
                ") "
                "OR "
                "("
                "status = 'PARTIALLY_CONSUMED' "
                "AND consumed_quantity > 0 "
                "AND consumed_quantity < quantity"
                ") "
                "OR "
                "("
                "status = 'CONSUMED' "
                "AND consumed_quantity = quantity"
                ") "
                "OR "
                "("
                "status = 'RELEASED' "
                "AND consumed_quantity < quantity"
                ") "
                "OR "
                "("
                "status = 'CANCELLED' "
                "AND consumed_quantity = 0"
                ")"
            ),
            name=op.f(
                "ck_inventory_reservations_"
                "status_quantity_consistent"
            ),
        ),
        sa.CheckConstraint(
            (
                "status IN ("
                "'ACTIVE', "
                "'PARTIALLY_CONSUMED', "
                "'CONSUMED', "
                "'RELEASED', "
                "'CANCELLED'"
                ")"
            ),
            name=op.f(
                "ck_inventory_reservations_status_valid"
            ),
        ),
        sa.ForeignKeyConstraint(
            [
                "location_id",
                "tenant_id",
            ],
            [
                "inventory_locations.id",
                "inventory_locations.tenant_id",
            ],
            name=(
                "fk_inventory_reservations_location_tenant"
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
                "fk_inventory_reservations_material_tenant"
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
                "fk_inventory_reservations_tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_inventory_reservations"
            ),
        ),
    )

    op.create_index(
        "ix_inventory_reservations_reference",
        "inventory_reservations",
        [
            "tenant_id",
            "reference_type",
            "reference_id",
        ],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_inventory_reservations_tenant_id"
        ),
        "inventory_reservations",
        [
            "tenant_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_inventory_reservations_tenant_location",
        "inventory_reservations",
        [
            "tenant_id",
            "location_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_inventory_reservations_tenant_material",
        "inventory_reservations",
        [
            "tenant_id",
            "material_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_inventory_reservations_tenant_status",
        "inventory_reservations",
        [
            "tenant_id",
            "status",
        ],
        unique=False,
    )


def downgrade() -> None:
    """Remove the modern inventory core."""

    op.drop_index(
        "ix_inventory_reservations_tenant_status",
        table_name="inventory_reservations",
    )
    op.drop_index(
        "ix_inventory_reservations_tenant_material",
        table_name="inventory_reservations",
    )
    op.drop_index(
        "ix_inventory_reservations_tenant_location",
        table_name="inventory_reservations",
    )
    op.drop_index(
        op.f(
            "ix_inventory_reservations_tenant_id"
        ),
        table_name="inventory_reservations",
    )
    op.drop_index(
        "ix_inventory_reservations_reference",
        table_name="inventory_reservations",
    )
    op.drop_table(
        "inventory_reservations"
    )

    op.drop_index(
        "ix_inventory_movements_tenant_type",
        table_name="inventory_movements",
    )
    op.drop_index(
        "ix_inventory_movements_tenant_source",
        table_name="inventory_movements",
    )
    op.drop_index(
        "ix_inventory_movements_tenant_occurred",
        table_name="inventory_movements",
    )
    op.drop_index(
        "ix_inventory_movements_tenant_material",
        table_name="inventory_movements",
    )
    op.drop_index(
        op.f(
            "ix_inventory_movements_tenant_id"
        ),
        table_name="inventory_movements",
    )
    op.drop_index(
        "ix_inventory_movements_tenant_destination",
        table_name="inventory_movements",
    )
    op.drop_index(
        "ix_inventory_movements_reference",
        table_name="inventory_movements",
    )
    op.drop_table(
        "inventory_movements"
    )

    op.drop_index(
        "ix_inventory_balances_tenant_material",
        table_name="inventory_balances",
    )
    op.drop_index(
        "ix_inventory_balances_tenant_location",
        table_name="inventory_balances",
    )
    op.drop_index(
        op.f(
            "ix_inventory_balances_tenant_id"
        ),
        table_name="inventory_balances",
    )
    op.drop_table(
        "inventory_balances"
    )

    op.drop_index(
        "ix_inventory_locations_tenant_type",
        table_name="inventory_locations",
    )
    op.drop_index(
        "ix_inventory_locations_tenant_name",
        table_name="inventory_locations",
    )
    op.drop_index(
        op.f(
            "ix_inventory_locations_tenant_id"
        ),
        table_name="inventory_locations",
    )
    op.drop_index(
        "ix_inventory_locations_tenant_branch",
        table_name="inventory_locations",
    )
    op.drop_index(
        "ix_inventory_locations_tenant_active",
        table_name="inventory_locations",
    )
    op.drop_table(
        "inventory_locations"
    )

    op.drop_constraint(
        "uq_materials_id_tenant",
        "materials",
        type_="unique",
    )
