"""SQLAlchemy repositories for inventory core."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import select
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
from organizeg3_api.domain.inventory.repository import (
    InventoryBalanceRepository,
    InventoryLocationRepository,
    InventoryMovementRepository,
    InventoryReservationRepository,
)
from organizeg3_api.domain.inventory.reservation import (
    InventoryReservation,
)
from organizeg3_api.domain.inventory.value_objects import (
    InventoryLocationType,
    InventoryMovementType,
    InventoryReservationStatus,
    normalize_inventory_code,
)
from organizeg3_api.infrastructure.persistence.models.branch import (
    BranchModel,
)
from organizeg3_api.infrastructure.persistence.models.inventory import (
    InventoryBalanceModel,
    InventoryLocationModel,
    InventoryMovementModel,
    InventoryReservationModel,
)
from organizeg3_api.infrastructure.persistence.models.material import (
    MaterialModel,
)


class SQLAlchemyInventoryLocationRepository(
    InventoryLocationRepository
):
    """Persist inventory locations."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        location_id: uuid.UUID,
    ) -> InventoryLocation | None:
        statement = (
            select(InventoryLocationModel)
            .where(
                InventoryLocationModel.id
                == location_id,
                InventoryLocationModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> InventoryLocation | None:
        normalized_code = normalize_inventory_code(
            code
        )

        statement = (
            select(InventoryLocationModel)
            .where(
                InventoryLocationModel.tenant_id
                == tenant_id,
                InventoryLocationModel.code
                == normalized_code,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def add(
        self,
        location: InventoryLocation,
    ) -> InventoryLocation:
        self._validate_branch_scope(
            tenant_id=location.tenant_id,
            branch_id=location.branch_id,
        )

        model = InventoryLocationModel(
            id=location.id,
            tenant_id=location.tenant_id,
            branch_id=location.branch_id,
            code=location.code,
            name=location.name,
            location_type=location.location_type.value,
            description=location.description,
            is_active=location.is_active,
            created_at=location.created_at,
            updated_at=location.updated_at,
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    def _validate_branch_scope(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID | None,
    ) -> None:
        if branch_id is None:
            return

        statement = (
            select(BranchModel.id)
            .where(
                BranchModel.id == branch_id,
                BranchModel.tenant_id == tenant_id,
            )
            .limit(1)
        )

        if (
            self._session.execute(statement)
            .scalar_one_or_none()
            is None
        ):
            raise ValueError(
                "A filial do local de estoque "
                "não pertence ao tenant informado."
            )

    @staticmethod
    def _to_domain(
        model: InventoryLocationModel,
    ) -> InventoryLocation:
        return InventoryLocation(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            branch_id=model.branch_id,
            code=model.code,
            name=model.name,
            location_type=InventoryLocationType(
                model.location_type
            ),
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyInventoryBalanceRepository(
    InventoryBalanceRepository
):
    """Persist current inventory balances."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_for_material_at_location(
        self,
        *,
        tenant_id: uuid.UUID,
        location_id: uuid.UUID,
        material_id: uuid.UUID,
    ) -> InventoryBalance | None:
        statement = (
            select(InventoryBalanceModel)
            .where(
                InventoryBalanceModel.tenant_id
                == tenant_id,
                InventoryBalanceModel.location_id
                == location_id,
                InventoryBalanceModel.material_id
                == material_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def add(
        self,
        balance: InventoryBalance,
    ) -> InventoryBalance:
        self._validate_location_scope(
            tenant_id=balance.tenant_id,
            location_id=balance.location_id,
        )

        self._validate_material_scope(
            tenant_id=balance.tenant_id,
            material_id=balance.material_id,
        )

        model = InventoryBalanceModel(
            id=balance.id,
            tenant_id=balance.tenant_id,
            location_id=balance.location_id,
            material_id=balance.material_id,
            on_hand_quantity=balance.on_hand_quantity,
            reserved_quantity=balance.reserved_quantity,
            created_at=balance.created_at,
            updated_at=balance.updated_at,
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    def _validate_location_scope(
        self,
        *,
        tenant_id: uuid.UUID,
        location_id: uuid.UUID,
    ) -> None:
        _require_location_for_tenant(
            self._session,
            tenant_id=tenant_id,
            location_id=location_id,
        )

    def _validate_material_scope(
        self,
        *,
        tenant_id: uuid.UUID,
        material_id: uuid.UUID,
    ) -> None:
        _require_material_for_tenant(
            self._session,
            tenant_id=tenant_id,
            material_id=material_id,
        )

    @staticmethod
    def _to_domain(
        model: InventoryBalanceModel,
    ) -> InventoryBalance:
        return InventoryBalance(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            location_id=model.location_id,
            material_id=model.material_id,
            on_hand_quantity=model.on_hand_quantity,
            reserved_quantity=model.reserved_quantity,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyInventoryMovementRepository(
    InventoryMovementRepository
):
    """Persist immutable inventory movements."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        movement_id: uuid.UUID,
    ) -> InventoryMovement | None:
        statement = (
            select(InventoryMovementModel)
            .where(
                InventoryMovementModel.id
                == movement_id,
                InventoryMovementModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def add(
        self,
        movement: InventoryMovement,
    ) -> InventoryMovement:
        _require_material_for_tenant(
            self._session,
            tenant_id=movement.tenant_id,
            material_id=movement.material_id,
        )

        if movement.source_location_id is not None:
            _require_location_for_tenant(
                self._session,
                tenant_id=movement.tenant_id,
                location_id=movement.source_location_id,
            )

        if movement.destination_location_id is not None:
            _require_location_for_tenant(
                self._session,
                tenant_id=movement.tenant_id,
                location_id=(
                    movement.destination_location_id
                ),
            )

        model = InventoryMovementModel(
            id=movement.id,
            tenant_id=movement.tenant_id,
            material_id=movement.material_id,
            movement_type=movement.movement_type.value,
            quantity=movement.quantity,
            source_location_id=(
                movement.source_location_id
            ),
            destination_location_id=(
                movement.destination_location_id
            ),
            reference_type=movement.reference_type,
            reference_id=movement.reference_id,
            notes=movement.notes,
            occurred_at=movement.occurred_at,
            created_at=movement.created_at,
            updated_at=movement.created_at,
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: InventoryMovementModel,
    ) -> InventoryMovement:
        return InventoryMovement(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            material_id=model.material_id,
            movement_type=InventoryMovementType(
                model.movement_type
            ),
            quantity=model.quantity,
            source_location_id=(
                model.source_location_id
            ),
            destination_location_id=(
                model.destination_location_id
            ),
            reference_type=model.reference_type,
            reference_id=model.reference_id,
            notes=model.notes,
            occurred_at=model.occurred_at,
            created_at=model.created_at,
        )


class SQLAlchemyInventoryReservationRepository(
    InventoryReservationRepository
):
    """Persist inventory reservations."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        reservation_id: uuid.UUID,
    ) -> InventoryReservation | None:
        statement = (
            select(InventoryReservationModel)
            .where(
                InventoryReservationModel.id
                == reservation_id,
                InventoryReservationModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def add(
        self,
        reservation: InventoryReservation,
    ) -> InventoryReservation:
        _require_location_for_tenant(
            self._session,
            tenant_id=reservation.tenant_id,
            location_id=reservation.location_id,
        )

        _require_material_for_tenant(
            self._session,
            tenant_id=reservation.tenant_id,
            material_id=reservation.material_id,
        )

        model = InventoryReservationModel(
            id=reservation.id,
            tenant_id=reservation.tenant_id,
            location_id=reservation.location_id,
            material_id=reservation.material_id,
            quantity=reservation.quantity,
            consumed_quantity=(
                reservation.consumed_quantity
            ),
            status=reservation.status.value,
            reference_type=reservation.reference_type,
            reference_id=reservation.reference_id,
            notes=reservation.notes,
            created_at=reservation.created_at,
            updated_at=reservation.updated_at,
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: InventoryReservationModel,
    ) -> InventoryReservation:
        return InventoryReservation(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            location_id=model.location_id,
            material_id=model.material_id,
            quantity=model.quantity,
            consumed_quantity=model.consumed_quantity,
            status=InventoryReservationStatus(
                model.status
            ),
            reference_type=model.reference_type,
            reference_id=model.reference_id,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


def _require_location_for_tenant(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    location_id: uuid.UUID,
) -> None:
    statement = (
        select(InventoryLocationModel.id)
        .where(
            InventoryLocationModel.id
            == location_id,
            InventoryLocationModel.tenant_id
            == tenant_id,
        )
        .limit(1)
    )

    if (
        session.execute(statement)
        .scalar_one_or_none()
        is None
    ):
        raise ValueError(
            "O local de estoque não pertence "
            "ao tenant informado."
        )


def _require_material_for_tenant(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    material_id: uuid.UUID,
) -> None:
    statement = (
        select(MaterialModel.id)
        .where(
            MaterialModel.id == material_id,
            MaterialModel.tenant_id == tenant_id,
        )
        .limit(1)
    )

    if (
        session.execute(statement)
        .scalar_one_or_none()
        is None
    ):
        raise ValueError(
            "O material não pertence "
            "ao tenant informado."
        )
