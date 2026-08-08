"""Material application use cases."""

from organizeg3_api.application.material.use_cases.create_material import (
    CreateMaterialUseCase,
)
from organizeg3_api.application.material.use_cases.deactivate_material import (
    DeactivateMaterialUseCase,
)
from organizeg3_api.application.material.use_cases.get_material import (
    GetMaterialUseCase,
)
from organizeg3_api.application.material.use_cases.list_materials import (
    ListMaterialsUseCase,
)
from organizeg3_api.application.material.use_cases.reactivate_material import (
    ReactivateMaterialUseCase,
)
from organizeg3_api.application.material.use_cases.update_material import (
    UpdateMaterialUseCase,
)

__all__ = [
    "CreateMaterialUseCase",
    "DeactivateMaterialUseCase",
    "GetMaterialUseCase",
    "ListMaterialsUseCase",
    "ReactivateMaterialUseCase",
    "UpdateMaterialUseCase",
]
