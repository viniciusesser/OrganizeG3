"""FastAPI endpoints for tenant machines."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated
import uuid

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)
from sqlalchemy.orm import Session

from organizeg3_api.application.audit import (
    RecordAuditEvent,
)
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
from organizeg3_api.domain.audit import (
    AuditAction,
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
    AuditRequestContext,
    get_audit_context,
)
from organizeg3_api.infrastructure.http.authentication import (
    require_permission,
)
from organizeg3_api.infrastructure.http.dependencies import (
    get_db_session,
)
from organizeg3_api.infrastructure.persistence.repositories.audit_event_repository import (
    SQLAlchemyAuditEventRepository,
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


def _audit_datetime(
    value: datetime,
) -> datetime:
    """Normalize persistence timestamps to aware UTC for auditing."""

    if value.tzinfo is None:
        return value.replace(
            tzinfo=UTC
        )

    return value.astimezone(
        UTC
    )


def _machine_snapshot(
    machine: MachineResponse,
) -> dict[str, object]:
    """Build the complete auditable state of one machine."""

    return {
        "id": machine.id,
        "tenant_id": machine.tenant_id,
        "code": machine.code,
        "name": machine.name,
        "machine_type": machine.machine_type,
        "status": machine.status,
        "branch_id": machine.branch_id,
        "manufacturer": machine.manufacturer,
        "model": machine.model,
        "serial_number": machine.serial_number,
        "is_active": machine.is_active,
        "created_at": _audit_datetime(
            machine.created_at
        ),
        "updated_at": _audit_datetime(
            machine.updated_at
        ),
    }


def _load_machine_snapshot(
    *,
    repository: SQLAlchemyMachineRepository,
    tenant_id: uuid.UUID,
    machine_id: uuid.UUID,
) -> dict[str, object] | None:
    """Load one machine state before a mutation."""

    machine = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        machine_id=machine_id,
    )

    if machine is None:
        return None

    response = MachineResponse.model_validate(
        machine
    )

    return _machine_snapshot(
        response
    )


def _record_machine_event(
    *,
    session: Session,
    audit_context: AuditRequestContext,
    action: AuditAction,
    machine: MachineResponse,
    before: dict[str, object] | None = None,
) -> None:
    """Append one machine event using the current transaction."""

    after = _machine_snapshot(
        machine
    )

    if (
        before is not None
        and before == after
    ):
        return

    RecordAuditEvent(
        SQLAlchemyAuditEventRepository(
            session
        )
    ).execute(
        context=audit_context,
        action=action,
        resource="machines",
        resource_id=machine.id,
        before=before,
        after=after,
    )


@router.post(
    "",
    response_model=MachineResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new machine",
)
def create_machine(
    payload: MachineCreate,
    context: CreateMachineContext,
    audit_context: AuditRequestContext,
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

    response = MachineResponse.model_validate(
        machine
    )

    _record_machine_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.CREATE,
        machine=response,
    )

    return response


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
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MachineResponse:
    """Update machine registration data in the authenticated tenant."""

    repository = SQLAlchemyMachineRepository(
        session
    )

    before = _load_machine_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        machine_id=machine_id,
    )

    machine = UpdateMachineUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        machine_id=machine_id,
        data=payload,
    )

    response = MachineResponse.model_validate(
        machine
    )

    _record_machine_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.UPDATE,
        machine=response,
        before=before,
    )

    return response


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
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MachineResponse:
    """Change the operational status of one tenant machine."""

    repository = SQLAlchemyMachineRepository(
        session
    )

    before = _load_machine_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        machine_id=machine_id,
    )

    machine = ChangeMachineStatusUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        machine_id=machine_id,
        status=payload.status,
    )

    response = MachineResponse.model_validate(
        machine
    )

    _record_machine_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.STATUS_CHANGE,
        machine=response,
        before=before,
    )

    return response


@router.post(
    "/{machine_id}/deactivate",
    response_model=MachineResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate a machine",
)
def deactivate_machine(
    machine_id: uuid.UUID,
    context: DeactivateMachineContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MachineResponse:
    """Deactivate one machine without deleting its history."""

    repository = SQLAlchemyMachineRepository(
        session
    )

    before = _load_machine_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        machine_id=machine_id,
    )

    machine = DeactivateMachineUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        machine_id=machine_id,
    )

    response = MachineResponse.model_validate(
        machine
    )

    _record_machine_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.DEACTIVATE,
        machine=response,
        before=before,
    )

    return response


@router.post(
    "/{machine_id}/reactivate",
    response_model=MachineResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate a machine",
)
def reactivate_machine(
    machine_id: uuid.UUID,
    context: ReactivateMachineContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MachineResponse:
    """Reactivate one machine inside the authenticated tenant."""

    repository = SQLAlchemyMachineRepository(
        session
    )

    before = _load_machine_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        machine_id=machine_id,
    )

    machine = ReactivateMachineUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        machine_id=machine_id,
    )

    response = MachineResponse.model_validate(
        machine
    )

    _record_machine_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.REACTIVATE,
        machine=response,
        before=before,
    )

    return response


__all__ = [
    "router",
]
