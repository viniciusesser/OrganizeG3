"""SQLAlchemy repository for tenant machines."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.machine.entity import (
    Machine,
)
from organizeg3_api.domain.machine.repository import (
    MachineRepository,
)
from organizeg3_api.domain.machine.value_objects import (
    MachineCode,
    MachineStatus,
)
from organizeg3_api.infrastructure.persistence.models.branch import (
    BranchModel,
)
from organizeg3_api.infrastructure.persistence.models.machine import (
    MachineModel,
)


class SQLAlchemyMachineRepository(
    MachineRepository
):
    """Persist tenant industrial machines using SQLAlchemy."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        machine_id: uuid.UUID,
    ) -> Machine | None:
        """Return one tenant-scoped machine."""

        statement = (
            select(
                MachineModel
            )
            .where(
                MachineModel.id == machine_id,
                MachineModel.tenant_id == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(
                statement
            )
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(
            model
        )

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> Machine | None:
        """Return one machine by normalized code."""

        normalized_code = MachineCode(
            code
        ).value

        statement = (
            select(
                MachineModel
            )
            .where(
                MachineModel.tenant_id == tenant_id,
                MachineModel.code == normalized_code,
            )
            .limit(1)
        )

        model = (
            self._session.execute(
                statement
            )
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(
            model
        )

    def add(
        self,
        machine: Machine,
    ) -> Machine:
        """Persist a new machine."""

        self._validate_branch_scope(
            tenant_id=machine.tenant_id,
            branch_id=machine.branch_id,
        )

        model = MachineModel(
            id=machine.id,
            tenant_id=machine.tenant_id,
            branch_id=machine.branch_id,
            code=machine.code,
            name=machine.name,
            machine_type=machine.machine_type,
            manufacturer=machine.manufacturer,
            model=machine.model,
            serial_number=machine.serial_number,
            status=machine.status.value,
            is_active=machine.is_active,
            created_at=machine.created_at,
            updated_at=machine.updated_at,
        )

        self._session.add(
            model
        )
        self._session.flush()

        return self._to_domain(
            model
        )

    def _validate_branch_scope(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID | None,
    ) -> None:
        """Ensure optional branch belongs to the same tenant."""

        if branch_id is None:
            return

        statement = (
            select(
                BranchModel.id
            )
            .where(
                BranchModel.id == branch_id,
                BranchModel.tenant_id == tenant_id,
            )
            .limit(1)
        )

        existing_branch = (
            self._session.execute(
                statement
            )
            .scalar_one_or_none()
        )

        if existing_branch is None:
            raise ValueError(
                "A filial da máquina não pertence "
                "ao tenant informado."
            )

    @staticmethod
    def _to_domain(
        model: MachineModel,
    ) -> Machine:
        """Convert persistence model to domain entity."""

        return Machine(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            branch_id=model.branch_id,
            code=model.code,
            name=model.name,
            machine_type=model.machine_type,
            manufacturer=model.manufacturer,
            model=model.model,
            serial_number=model.serial_number,
            status=MachineStatus(
                model.status
            ),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
