"""Machine application use cases."""

from organizeg3_api.application.machine.use_cases.change_machine_status import (
    ChangeMachineStatusUseCase,
)
from organizeg3_api.application.machine.use_cases.create_machine import (
    CreateMachineUseCase,
)
from organizeg3_api.application.machine.use_cases.deactivate_machine import (
    DeactivateMachineUseCase,
)
from organizeg3_api.application.machine.use_cases.get_machine import (
    GetMachineUseCase,
)
from organizeg3_api.application.machine.use_cases.list_machines import (
    ListMachinesUseCase,
)
from organizeg3_api.application.machine.use_cases.reactivate_machine import (
    ReactivateMachineUseCase,
)
from organizeg3_api.application.machine.use_cases.update_machine import (
    UpdateMachineUseCase,
)

__all__ = [
    "ChangeMachineStatusUseCase",
    "CreateMachineUseCase",
    "DeactivateMachineUseCase",
    "GetMachineUseCase",
    "ListMachinesUseCase",
    "ReactivateMachineUseCase",
    "UpdateMachineUseCase",
]
