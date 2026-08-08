"""SQLAlchemy repository for tenant machines."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import or_, select
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
    MachineType,
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

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        machine_type: str | None = None,
        status: MachineStatus | None = None,
        branch_id: uuid.UUID | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Machine]:
        """List tenant machines with filters and pagination."""

        statement = select(
            MachineModel
        ).where(
            MachineModel.tenant_id == tenant_id
        )

        if not include_inactive:
            statement = statement.where(
                MachineModel.is_active.is_(
                    True
                )
            )

        if search is not None:
            normalized_search = search.strip()

            if normalized_search:
                pattern = (
                    f"%{normalized_search}%"
                )

                statement = statement.where(
                    or_(
                        MachineModel.code.ilike(
                            pattern
                        ),
                        MachineModel.name.ilike(
                            pattern
                        ),
                        MachineModel.machine_type.ilike(
                            pattern
                        ),
                        MachineModel.manufacturer.ilike(
                            pattern
                        ),
                        MachineModel.model.ilike(
                            pattern
                        ),
                        MachineModel.serial_number.ilike(
                            pattern
                        ),
                    )
                )

        if machine_type is not None:
            normalized_machine_type = MachineType(
                machine_type
            ).value

            statement = statement.where(
                MachineModel.machine_type
                == normalized_machine_type
            )

        if status is not None:
            if not isinstance(
                status,
                MachineStatus,
            ):
                raise TypeError(
                    "O filtro de status deve ser "
                    "um MachineStatus."
                )

            statement = statement.where(
                MachineModel.status
                == status.value
            )

        if branch_id is not None:
            statement = statement.where(
                MachineModel.branch_id
                == branch_id
            )

        statement = (
            statement
            .order_by(
                MachineModel.name,
                MachineModel.code,
                MachineModel.id,
            )
            .limit(
                limit
            )
            .offset(
                offset
            )
        )

        models = self._session.execute(
            statement
        ).scalars().all()

        return [
            self._to_domain(
                model
            )
            for model in models
        ]

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_machine_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a normalized code exists in the tenant."""

        normalized_code = MachineCode(
            code
        ).value

        statement = select(
            MachineModel.id
        ).where(
            MachineModel.tenant_id == tenant_id,
            MachineModel.code == normalized_code,
        )

        if exclude_machine_id is not None:
            statement = statement.where(
                MachineModel.id
                != exclude_machine_id
            )

        statement = statement.limit(
            1
        )

        return (
            self._session.execute(
                statement
            ).scalar_one_or_none()
            is not None
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

        if machine.created_at is None:
            raise ValueError(
                "A máquina deve possuir created_at "
                "antes de ser persistida."
            )

        if machine.updated_at is None:
            raise ValueError(
                "A máquina deve possuir updated_at "
                "antes de ser persistida."
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

    def save(
        self,
        machine: Machine,
    ) -> Machine:
        """Persist changes to an existing tenant machine."""

        if machine.id is None:
            raise ValueError(
                "A máquina deve possuir identificador "
                "antes de ser salva."
            )

        if machine.updated_at is None:
            raise ValueError(
                "A máquina deve possuir updated_at "
                "antes de ser salva."
            )

        self._validate_branch_scope(
            tenant_id=machine.tenant_id,
            branch_id=machine.branch_id,
        )

        statement = (
            select(
                MachineModel
            )
            .where(
                MachineModel.id == machine.id,
                MachineModel.tenant_id
                == machine.tenant_id,
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
            raise ValueError(
                "A máquina informada não foi encontrada "
                "no tenant."
            )

        model.branch_id = machine.branch_id
        model.code = machine.code
        model.name = machine.name
        model.machine_type = machine.machine_type
        model.manufacturer = machine.manufacturer
        model.model = machine.model
        model.serial_number = machine.serial_number
        model.status = machine.status.value
        model.is_active = machine.is_active
        model.updated_at = machine.updated_at

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
