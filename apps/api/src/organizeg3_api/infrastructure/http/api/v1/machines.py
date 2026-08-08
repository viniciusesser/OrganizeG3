"""FastAPI endpoints for tenant machines."""

from __future__ import annotations

from typing import Annotated
import uuid

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)
from sqlalchemy.orm import Session

from organizeg3_api.application.machine.schemas import (
    MachineCreate,
    MachineResponse,
    MachineStatusUpdate,
    MachineUpdate,
)
from organizeg3_api.application.machine.use_cases import (
    ChangeMachineStatusUseCase,
    CreateMachineUseCase,
    DeactivateMachineUseCase,
    GetMachineUseCase,
    ListMachinesUseCase,
    ReactivateMachineUseCase,
    UpdateMachineUseCase,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.domain.identity.permissions import (
    MachinePermissions,
)
from organizeg3_api.domain.machine.value_objects import (
    MachineStatus,
)
from organizeg3_api.infrastructure.http.audit_context import (
    get_audit_context,
)
from organizeg3_api.infrastructure.http.authentication import (
    require_permission,
)
from organizeg3_api.infrastructure.http.dependencies import (
    get_db_session,
)
from organizeg3_api.infrastructure.persistence.repositories.machine_repository import (
    SQLAlchemyMachineRepository,
)

router = APIRouter(
    prefix="/machines",
    tags=["Machines"],
    dependencies=[
        Depends(get_audit_context),
    ],
)


ReadMachineContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            MachinePermissions.READ
        )
    ),
]

CreateMachineContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            MachinePermissions.CREATE
        )
    ),
]

UpdateMachineContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            MachinePermissions.UPDATE
        )
    ),
]

ChangeMachineStatusContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            MachinePermissions.CHANGE_STATUS
        )
    ),
]

DeactivateMachineContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            MachinePermissions.DEACTIVATE
        )
    ),
]

ReactivateMachineContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            MachinePermissions.REACTIVATE
        )
    ),
]


@router.post(
    "",
    response_model=MachineResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new machine",
)
def create_machine(
    payload: MachineCreate,
    context: CreateMachineContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MachineResponse:
    """Create a machine inside the authenticated tenant."""

    repository = SQLAlchemyMachineRepository(
        session
    )

    machine = CreateMachineUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        data=payload,
    )

    return MachineResponse.model_validate(
        machine
    )


@router.get(
    "",
    response_model=list[MachineResponse],
    status_code=status.HTTP_200_OK,
    summary="List and search machines",
)
def list_machines(
    context: ReadMachineContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
    *,
    include_inactive: Annotated[
        bool,
        Query(
            description="Include inactive machines"
        ),
    ] = False,
    search: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=255,
            description="Search machine data",
        ),
    ] = None,
    machine_type: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=100,
            description="Filter by machine type",
        ),
    ] = None,
    machine_status: Annotated[
        MachineStatus | None,
        Query(
            alias="status",
            description="Filter by operational machine status",
        ),
    ] = None,
    branch_id: Annotated[
        uuid.UUID | None,
        Query(
            description="Filter by branch identifier"
        ),
    ] = None,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=200,
            description="Maximum machines to return",
        ),
    ] = 100,
    offset: Annotated[
        int,
        Query(
            ge=0,
            description="Number of machines to skip",
        ),
    ] = 0,
) -> list[MachineResponse]:
    """List machines belonging to the authenticated tenant."""

    repository = SQLAlchemyMachineRepository(
        session
    )

    machines = ListMachinesUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        include_inactive=include_inactive,
        search=search,
        machine_type=machine_type,
        status=machine_status,
        branch_id=branch_id,
        limit=limit,
        offset=offset,
    )

    return [
        MachineResponse.model_validate(
            machine
        )
        for machine in machines
    ]


@router.get(
    "/{machine_id}",
    response_model=MachineResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a machine",
)
def get_machine(
    machine_id: uuid.UUID,
    context: ReadMachineContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MachineResponse:
    """Return one machine from the authenticated tenant."""

    repository = SQLAlchemyMachineRepository(
        session
    )

    machine = GetMachineUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        machine_id=machine_id,
    )

    return MachineResponse.model_validate(
        machine
    )


@router.patch(
    "/{machine_id}",
    response_model=MachineResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a machine",
)
def update_machine(
    machine_id: uuid.UUID,
    payload: MachineUpdate,
    context: UpdateMachineContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MachineResponse:
    """Update machine registration data in the authenticated tenant."""

    repository = SQLAlchemyMachineRepository(
        session
    )

    machine = UpdateMachineUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        machine_id=machine_id,
        data=payload,
    )

    return MachineResponse.model_validate(
        machine
    )


@router.post(
    "/{machine_id}/status",
    response_model=MachineResponse,
    status_code=status.HTTP_200_OK,
    summary="Change machine operational status",
)
def change_machine_status(
    machine_id: uuid.UUID,
    payload: MachineStatusUpdate,
    context: ChangeMachineStatusContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MachineResponse:
    """Change the operational status of one tenant machine."""

    repository = SQLAlchemyMachineRepository(
        session
    )

    machine = ChangeMachineStatusUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        machine_id=machine_id,
        status=payload.status,
    )

    return MachineResponse.model_validate(
        machine
    )


@router.post(
    "/{machine_id}/deactivate",
    response_model=MachineResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate a machine",
)
def deactivate_machine(
    machine_id: uuid.UUID,
    context: DeactivateMachineContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MachineResponse:
    """Deactivate one machine without deleting its history."""

    repository = SQLAlchemyMachineRepository(
        session
    )

    machine = DeactivateMachineUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        machine_id=machine_id,
    )

    return MachineResponse.model_validate(
        machine
    )


@router.post(
    "/{machine_id}/reactivate",
    response_model=MachineResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate a machine",
)
def reactivate_machine(
    machine_id: uuid.UUID,
    context: ReactivateMachineContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MachineResponse:
    """Reactivate one machine inside the authenticated tenant."""

    repository = SQLAlchemyMachineRepository(
        session
    )

    machine = ReactivateMachineUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        machine_id=machine_id,
    )

    return MachineResponse.model_validate(
        machine
    )


__all__ = [
    "router",
]
