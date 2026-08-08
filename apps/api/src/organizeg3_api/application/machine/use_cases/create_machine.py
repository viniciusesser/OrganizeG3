"""Create-machine application use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.machine.schemas import (
    MachineCreate,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    ValidationError,
)
from organizeg3_api.domain.machine.entity import (
    Machine,
)
from organizeg3_api.domain.machine.repository import (
    MachineRepository,
)
from organizeg3_api.domain.machine.value_objects import (
    MachineCode,
)


class CreateMachineUseCase:
    """Create one machine inside a tenant."""

    def __init__(
        self,
        repository: MachineRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        data: MachineCreate,
    ) -> Machine:
        """Create and persist a tenant machine."""

        try:
            normalized_code = MachineCode(
                data.code
            ).value

            self._ensure_code_available(
                tenant_id=tenant_id,
                code=normalized_code,
            )

            machine = Machine.create(
                tenant_id=tenant_id,
                code=normalized_code,
                name=data.name,
                machine_type=data.machine_type,
                branch_id=data.branch_id,
                manufacturer=data.manufacturer,
                model=data.model,
                serial_number=data.serial_number,
            )

            return self._repository.add(
                machine
            )

        except ConflictError:
            raise
        except (TypeError, ValueError) as exc:
            raise ValidationError(
                str(exc)
            ) from exc

    def _ensure_code_available(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> None:
        if not self._repository.exists_by_code(
            tenant_id=tenant_id,
            code=code,
        ):
            return

        raise ConflictError(
            "Já existe uma máquina com este código.",
            details={
                "field": "code",
                "value": code,
            },
        )
