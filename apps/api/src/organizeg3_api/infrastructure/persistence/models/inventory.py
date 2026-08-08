"""SQLAlchemy ORM mappings for inventory core."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
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


class InventoryLocationModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one physical inventory location."""

    __tablename__ = "inventory_locations"

    __table_args__ = (
        CheckConstraint(
            "TRIM(code) <> ''",
            name="code_not_blank",
        ),
        CheckConstraint(
            "TRIM(name) <> ''",
            name="name_not_blank",
        ),
        CheckConstraint(
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
            name="location_type_valid",
        ),
        UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_inventory_locations_tenant_code",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_inventory_locations_id_tenant",
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
            name="fk_inventory_locations_branch_tenant",
        ),
        Index(
            "ix_inventory_locations_tenant_branch",
            "tenant_id",
            "branch_id",
        ),
        Index(
            "ix_inventory_locations_tenant_type",
            "tenant_id",
            "location_type",
        ),
        Index(
            "ix_inventory_locations_tenant_active",
            "tenant_id",
            "is_active",
        ),
        Index(
            "ix_inventory_locations_tenant_name",
            "tenant_id",
            "name",
        ),
    )

    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    location_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )


class InventoryBalanceModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist current material quantity at one location."""

    __tablename__ = "inventory_balances"

    __table_args__ = (
        CheckConstraint(
            "on_hand_quantity >= 0",
            name="on_hand_quantity_non_negative",
        ),
        CheckConstraint(
            "reserved_quantity >= 0",
            name="reserved_quantity_non_negative",
        ),
        CheckConstraint(
            "reserved_quantity <= on_hand_quantity",
            name="reserved_not_above_on_hand",
        ),
        UniqueConstraint(
            "tenant_id",
            "location_id",
            "material_id",
            name=(
                "uq_inventory_balances_"
                "tenant_location_material"
            ),
        ),
        ForeignKeyConstraint(
            [
                "location_id",
                "tenant_id",
            ],
            [
                "inventory_locations.id",
                "inventory_locations.tenant_id",
            ],
            name="fk_inventory_balances_location_tenant",
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
            name="fk_inventory_balances_material_tenant",
        ),
        Index(
            "ix_inventory_balances_tenant_location",
            "tenant_id",
            "location_id",
        ),
        Index(
            "ix_inventory_balances_tenant_material",
            "tenant_id",
            "material_id",
        ),
    )

    location_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    material_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    on_hand_quantity: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=18,
            scale=6,
        ),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
    )

    reserved_quantity: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=18,
            scale=6,
        ),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
    )


class InventoryMovementModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one immutable physical inventory movement."""

    __tablename__ = "inventory_movements"

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="quantity_positive",
        ),
        CheckConstraint(
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
            name="movement_type_valid",
        ),
        CheckConstraint(
            (
                "("
                "movement_type IN "
                "('RECEIPT', 'ADJUSTMENT_IN', 'RETURN_IN') "
                "AND source_location_id IS NULL "
                "AND destination_location_id IS NOT NULL"
                ") "
                "OR "
                "("
                "movement_type IN "
                "('ISSUE', 'ADJUSTMENT_OUT', 'RETURN_OUT') "
                "AND source_location_id IS NOT NULL "
                "AND destination_location_id IS NULL"
                ") "
                "OR "
                "("
                "movement_type = 'TRANSFER' "
                "AND source_location_id IS NOT NULL "
                "AND destination_location_id IS NOT NULL "
                "AND source_location_id <> destination_location_id"
                ")"
            ),
            name="locations_consistent",
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
            name="fk_inventory_movements_material_tenant",
        ),
        ForeignKeyConstraint(
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
        ForeignKeyConstraint(
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
        Index(
            "ix_inventory_movements_tenant_material",
            "tenant_id",
            "material_id",
        ),
        Index(
            "ix_inventory_movements_tenant_source",
            "tenant_id",
            "source_location_id",
        ),
        Index(
            "ix_inventory_movements_tenant_destination",
            "tenant_id",
            "destination_location_id",
        ),
        Index(
            "ix_inventory_movements_tenant_type",
            "tenant_id",
            "movement_type",
        ),
        Index(
            "ix_inventory_movements_tenant_occurred",
            "tenant_id",
            "occurred_at",
        ),
        Index(
            "ix_inventory_movements_reference",
            "tenant_id",
            "reference_type",
            "reference_id",
        ),
    )

    material_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    movement_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=18,
            scale=6,
        ),
        nullable=False,
    )

    source_location_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )

    destination_location_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        Uuid,
        nullable=True,
    )

    reference_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    reference_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )


class InventoryReservationModel(
    UUIDPrimaryKeyMixin,
    TenantScopedMixin,
    TimestampMixin,
    Base,
):
    """Persist one logical inventory reservation."""

    __tablename__ = "inventory_reservations"

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="quantity_positive",
        ),
        CheckConstraint(
            "consumed_quantity >= 0",
            name="consumed_quantity_non_negative",
        ),
        CheckConstraint(
            "consumed_quantity <= quantity",
            name="consumed_not_above_quantity",
        ),
        CheckConstraint(
            (
                "status IN ("
                "'ACTIVE', "
                "'PARTIALLY_CONSUMED', "
                "'CONSUMED', "
                "'RELEASED', "
                "'CANCELLED'"
                ")"
            ),
            name="status_valid",
        ),
        CheckConstraint(
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
            name="status_quantity_consistent",
        ),
        ForeignKeyConstraint(
            [
                "location_id",
                "tenant_id",
            ],
            [
                "inventory_locations.id",
                "inventory_locations.tenant_id",
            ],
            name=(
                "fk_inventory_reservations_"
                "location_tenant"
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
            name=(
                "fk_inventory_reservations_"
                "material_tenant"
            ),
        ),
        Index(
            "ix_inventory_reservations_tenant_location",
            "tenant_id",
            "location_id",
        ),
        Index(
            "ix_inventory_reservations_tenant_material",
            "tenant_id",
            "material_id",
        ),
        Index(
            "ix_inventory_reservations_tenant_status",
            "tenant_id",
            "status",
        ),
        Index(
            "ix_inventory_reservations_reference",
            "tenant_id",
            "reference_type",
            "reference_id",
        ),
    )

    location_id: Mapped[uuid.UUID] = mapped_column(
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

    consumed_quantity: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=18,
            scale=6,
        ),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="ACTIVE",
        server_default=text("'ACTIVE'"),
    )

    reference_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    reference_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )
