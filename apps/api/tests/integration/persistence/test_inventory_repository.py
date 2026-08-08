"""Integration tests for inventory persistence repositories."""

from __future__ import annotations

from decimal import Decimal
import uuid

import pytest
from sqlalchemy.orm import Session

from organizeg3_api.domain.inventory.balance import (
    InventoryBalance,
)
from organizeg3_api.domain.inventory.location import (
    InventoryLocation,
)
from organizeg3_api.domain.inventory.movement import (
    InventoryMovement,
)
from organizeg3_api.domain.inventory.reservation import (
    InventoryReservation,
)
from organizeg3_api.domain.inventory.value_objects import (
    InventoryLocationType,
    InventoryMovementType,
)
from organizeg3_api.infrastructure.persistence.models.branch import (
    BranchModel,
)
from organizeg3_api.infrastructure.persistence.models.material import (
    MaterialModel,
)
from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories.inventory_repository import (
    SQLAlchemyInventoryBalanceRepository,
    SQLAlchemyInventoryLocationRepository,
    SQLAlchemyInventoryMovementRepository,
    SQLAlchemyInventoryReservationRepository,
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
) -> TenantRecordModel:
    tenant = TenantRecordModel(
        id=tenant_id,
        name=name,
        status="ACTIVE",
        is_active=True,
    )

    session.add(tenant)
    session.flush()

    return tenant


def create_branch(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "BR-001",
) -> BranchModel:
    branch = BranchModel(
        tenant_id=tenant_id,
        code=code,
        name=f"Filial {code}",
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


def create_location(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "ALM-001",
    branch_id: uuid.UUID | None = None,
) -> InventoryLocation:
    repository = SQLAlchemyInventoryLocationRepository(
        session
    )

    location = InventoryLocation.create(
        tenant_id=tenant_id,
        branch_id=branch_id,
        code=code,
        name=f"Local {code}",
        location_type=InventoryLocationType.WAREHOUSE,
    )

    return repository.add(
        location
    )


def test_persists_inventory_location(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Estoque",
    )

    repository = SQLAlchemyInventoryLocationRepository(
        session
    )

    saved = create_location(
        session,
        tenant_id=tenant_id,
    )

    assert saved.id is not None

    loaded = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        location_id=saved.id,
    )

    assert loaded is not None
    assert loaded.code == "ALM-001"


def test_location_code_is_tenant_scoped(
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

    create_location(
        session,
        tenant_id=tenant_id,
        code="ALM-001",
    )

    repository = SQLAlchemyInventoryLocationRepository(
        session
    )

    assert (
        repository.get_by_code_for_tenant(
            tenant_id=tenant_id,
            code=" alm-001 ",
        )
        is not None
    )

    assert (
        repository.get_by_code_for_tenant(
            tenant_id=other_tenant_id,
            code="ALM-001",
        )
        is None
    )


def test_rejects_location_with_cross_tenant_branch(
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

    branch = create_branch(
        session,
        tenant_id=other_tenant_id,
    )

    location = InventoryLocation.create(
        tenant_id=tenant_id,
        branch_id=branch.id,
        code="ALM-001",
        name="Almoxarifado",
        location_type=InventoryLocationType.WAREHOUSE,
    )

    repository = SQLAlchemyInventoryLocationRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="filial",
    ):
        repository.add(
            location
        )


def test_persists_inventory_balance(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Estoque",
    )

    material = create_material(
        session,
        tenant_id=tenant_id,
    )

    location = create_location(
        session,
        tenant_id=tenant_id,
    )

    assert location.id is not None

    balance = InventoryBalance.create(
        tenant_id=tenant_id,
        location_id=location.id,
        material_id=material.id,
    )

    balance.receive("12.5")
    balance.reserve("2.5")

    repository = SQLAlchemyInventoryBalanceRepository(
        session
    )

    saved = repository.add(
        balance
    )

    assert saved.on_hand_quantity == Decimal("12.500000")
    assert saved.reserved_quantity == Decimal("2.500000")

    loaded = repository.get_for_material_at_location(
        tenant_id=tenant_id,
        location_id=location.id,
        material_id=material.id,
    )

    assert loaded is not None
    assert loaded.available_quantity == Decimal("10.000000")


def test_rejects_balance_with_cross_tenant_material(
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

    material = create_material(
        session,
        tenant_id=other_tenant_id,
    )

    location = create_location(
        session,
        tenant_id=tenant_id,
    )

    assert location.id is not None

    balance = InventoryBalance.create(
        tenant_id=tenant_id,
        location_id=location.id,
        material_id=material.id,
    )

    repository = SQLAlchemyInventoryBalanceRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="material",
    ):
        repository.add(
            balance
        )


def test_persists_inventory_receipt(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Estoque",
    )

    material = create_material(
        session,
        tenant_id=tenant_id,
    )

    location = create_location(
        session,
        tenant_id=tenant_id,
    )

    assert location.id is not None

    movement = InventoryMovement.create(
        tenant_id=tenant_id,
        material_id=material.id,
        movement_type=InventoryMovementType.RECEIPT,
        quantity="25.5",
        destination_location_id=location.id,
        reference_type="PURCHASE_ORDER",
        reference_id=uuid.uuid4(),
    )

    repository = SQLAlchemyInventoryMovementRepository(
        session
    )

    saved = repository.add(
        movement
    )

    assert saved.id is not None
    assert saved.quantity == Decimal("25.500000")

    loaded = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        movement_id=saved.id,
    )

    assert loaded is not None
    assert (
        loaded.movement_type
        is InventoryMovementType.RECEIPT
    )


def test_persists_inventory_transfer(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Estoque",
    )

    material = create_material(
        session,
        tenant_id=tenant_id,
    )

    source = create_location(
        session,
        tenant_id=tenant_id,
        code="ALM-001",
    )

    destination = create_location(
        session,
        tenant_id=tenant_id,
        code="CORTE",
    )

    assert source.id is not None
    assert destination.id is not None

    movement = InventoryMovement.create(
        tenant_id=tenant_id,
        material_id=material.id,
        movement_type=InventoryMovementType.TRANSFER,
        quantity="4",
        source_location_id=source.id,
        destination_location_id=destination.id,
    )

    repository = SQLAlchemyInventoryMovementRepository(
        session
    )

    saved = repository.add(
        movement
    )

    assert saved.source_location_id == source.id
    assert saved.destination_location_id == destination.id


def test_rejects_movement_with_cross_tenant_location(
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

    material = create_material(
        session,
        tenant_id=tenant_id,
    )

    foreign_location = create_location(
        session,
        tenant_id=other_tenant_id,
    )

    assert foreign_location.id is not None

    movement = InventoryMovement.create(
        tenant_id=tenant_id,
        material_id=material.id,
        movement_type=InventoryMovementType.RECEIPT,
        quantity="1",
        destination_location_id=foreign_location.id,
    )

    repository = SQLAlchemyInventoryMovementRepository(
        session
    )

    with pytest.raises(
        ValueError,
        match="local de estoque",
    ):
        repository.add(
            movement
        )


def test_persists_inventory_reservation(
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    create_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Estoque",
    )

    material = create_material(
        session,
        tenant_id=tenant_id,
    )

    location = create_location(
        session,
        tenant_id=tenant_id,
    )

    assert location.id is not None

    reservation = InventoryReservation.create(
        tenant_id=tenant_id,
        location_id=location.id,
        material_id=material.id,
        quantity="7",
        reference_type="PRODUCTION_ORDER",
        reference_id=uuid.uuid4(),
    )

    reservation.consume("2")

    repository = (
        SQLAlchemyInventoryReservationRepository(
            session
        )
    )

    saved = repository.add(
        reservation
    )

    assert saved.id is not None
    assert saved.quantity == Decimal("7.000000")
    assert saved.consumed_quantity == Decimal("2.000000")

    loaded = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        reservation_id=saved.id,
    )

    assert loaded is not None
    assert loaded.remaining_quantity == Decimal("5.000000")


def test_inventory_read_is_tenant_scoped(
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

    location = create_location(
        session,
        tenant_id=tenant_id,
    )

    assert location.id is not None

    repository = SQLAlchemyInventoryLocationRepository(
        session
    )

    assert (
        repository.get_by_id_for_tenant(
            tenant_id=other_tenant_id,
            location_id=location.id,
        )
        is None
    )
