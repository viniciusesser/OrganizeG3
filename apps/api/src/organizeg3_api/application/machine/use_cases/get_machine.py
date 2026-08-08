"""Get-machine application use case."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import (
    NotFoundError,
)
from organizeg3_api.domain.machine.entity import (
    Machine,
)
from organizeg3_api.domain.machine.repository import (
    MachineRepository,
)


class GetMachineUseCase:
    """Get one tenant-scoped machine."""

    def __init__(
        self,
        repository: MachineRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        machine_id: uuid.UUID,
    ) -> Machine:
        """Return one machine or raise not-found."""

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

        return machine
