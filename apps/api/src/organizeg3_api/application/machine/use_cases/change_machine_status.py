"""Change-machine-status application use case."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import (
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.machine.entity import (
    Machine,
)
from organizeg3_api.domain.machine.repository import (
    MachineRepository,
)
from organizeg3_api.domain.machine.value_objects import (
    MachineStatus,
)


class ChangeMachineStatusUseCase:
    """Change the operational state of a tenant machine."""

    def __init__(
        self,
        repository: MachineRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        machine_id: uuid.UUID,
        status: MachineStatus,
    ) -> Machine:
        """Change machine operational status."""

        machine = (
            self._repository.get_by_id_for_tenant(
                tenant_id=tenant_id,
                machine_id=machine_id,
            )
        )

        if machine is None:
            raise NotFoundError(
                "Máquina não encontrada."
            )

        try:
            self._apply_status(
                machine,
                status,
            )

            return self._repository.save(
                machine
            )

        except (TypeError, ValueError) as exc:
            raise ValidationError(
                str(exc)
            ) from exc

    @staticmethod
    def _apply_status(
        machine: Machine,
        status: MachineStatus,
    ) -> None:
        if not isinstance(
            status,
            MachineStatus,
        ):
            raise TypeError(
                "O status da máquina deve ser "
                "um MachineStatus."
            )

        handlers = {
            MachineStatus.AVAILABLE: (
                machine.mark_available
            ),
            MachineStatus.IN_USE: (
                machine.mark_in_use
            ),
            MachineStatus.MAINTENANCE: (
                machine.send_to_maintenance
            ),
            MachineStatus.OUT_OF_SERVICE: (
                machine.mark_out_of_service
            ),
        }

        handlers[status]()
