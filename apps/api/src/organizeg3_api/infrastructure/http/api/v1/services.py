"""FastAPI endpoints for tenant services."""

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
from organizeg3_api.application.service.schemas import (
    ServiceCreate,
    ServiceResponse,
    ServiceUpdate,
)
from organizeg3_api.application.service.use_cases import (
    CreateServiceUseCase,
    DeactivateServiceUseCase,
    GetServiceUseCase,
    ListServicesUseCase,
    ReactivateServiceUseCase,
    UpdateServiceUseCase,
)
from organizeg3_api.domain.audit import (
    AuditAction,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.domain.identity.permissions import (
    ServicePermissions,
)
from organizeg3_api.domain.service.value_objects import (
    ServiceExecutionMode,
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
from organizeg3_api.infrastructure.persistence.repositories.service_repository import (
    SQLAlchemyServiceRepository,
)

router = APIRouter(
    prefix="/services",
    tags=["Services"],
    dependencies=[
        Depends(get_audit_context),
    ],
)


ReadServiceContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            ServicePermissions.READ
        )
    ),
]

CreateServiceContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            ServicePermissions.CREATE
        )
    ),
]

UpdateServiceContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            ServicePermissions.UPDATE
        )
    ),
]

DeactivateServiceContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            ServicePermissions.DEACTIVATE
        )
    ),
]

ReactivateServiceContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            ServicePermissions.REACTIVATE
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


def _service_snapshot(
    service: ServiceResponse,
) -> dict[str, object]:
    """Build the complete auditable state of one service."""

    return {
        "id": service.id,
        "tenant_id": service.tenant_id,
        "code": service.code,
        "name": service.name,
        "category": service.category,
        "unit": service.unit,
        "execution_mode": service.execution_mode,
        "estimated_duration_minutes": (
            service.estimated_duration_minutes
        ),
        "is_active": service.is_active,
        "created_at": _audit_datetime(
            service.created_at
        ),
        "updated_at": _audit_datetime(
            service.updated_at
        ),
    }


def _load_service_snapshot(
    *,
    repository: SQLAlchemyServiceRepository,
    tenant_id: uuid.UUID,
    service_id: uuid.UUID,
) -> dict[str, object] | None:
    """Load one service state before a mutation."""

    service = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        service_id=service_id,
    )

    if service is None:
        return None

    response = ServiceResponse.model_validate(
        service
    )

    return _service_snapshot(
        response
    )


def _record_service_event(
    *,
    session: Session,
    audit_context: AuditRequestContext,
    action: AuditAction,
    service: ServiceResponse,
    before: dict[str, object] | None = None,
) -> None:
    """Append one service event using the current transaction."""

    after = _service_snapshot(
        service
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
        resource="services",
        resource_id=service.id,
        before=before,
        after=after,
    )


@router.post(
    "",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new service",
)
def create_service(
    payload: ServiceCreate,
    context: CreateServiceContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> ServiceResponse:
    """Create a service inside the authenticated tenant."""

    repository = SQLAlchemyServiceRepository(
        session
    )

    service = CreateServiceUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        data=payload,
    )

    response = ServiceResponse.model_validate(
        service
    )

    _record_service_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.CREATE,
        service=response,
    )

    return response


@router.get(
    "",
    response_model=list[ServiceResponse],
    status_code=status.HTTP_200_OK,
    summary="List and search services",
)
def list_services(
    context: ReadServiceContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
    *,
    include_inactive: Annotated[
        bool,
        Query(
            description="Include inactive services"
        ),
    ] = False,
    search: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=255,
            description="Search service data",
        ),
    ] = None,
    category: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=100,
            description="Filter by service category",
        ),
    ] = None,
    execution_mode: Annotated[
        ServiceExecutionMode | None,
        Query(
            description=(
                "Filter by service execution mode"
            )
        ),
    ] = None,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=200,
            description="Maximum services to return",
        ),
    ] = 100,
    offset: Annotated[
        int,
        Query(
            ge=0,
            description="Number of services to skip",
        ),
    ] = 0,
) -> list[ServiceResponse]:
    """List services belonging to the authenticated tenant."""

    repository = SQLAlchemyServiceRepository(
        session
    )

    services = ListServicesUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        include_inactive=include_inactive,
        search=search,
        category=category,
        execution_mode=execution_mode,
        limit=limit,
        offset=offset,
    )

    return [
        ServiceResponse.model_validate(
            service
        )
        for service in services
    ]


@router.get(
    "/{service_id}",
    response_model=ServiceResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a service",
)
def get_service(
    service_id: uuid.UUID,
    context: ReadServiceContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> ServiceResponse:
    """Return one service from the authenticated tenant."""

    repository = SQLAlchemyServiceRepository(
        session
    )

    service = GetServiceUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        service_id=service_id,
    )

    return ServiceResponse.model_validate(
        service
    )


@router.patch(
    "/{service_id}",
    response_model=ServiceResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a service",
)
def update_service(
    service_id: uuid.UUID,
    payload: ServiceUpdate,
    context: UpdateServiceContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> ServiceResponse:
    """Update a service inside the authenticated tenant."""

    repository = SQLAlchemyServiceRepository(
        session
    )

    before = _load_service_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        service_id=service_id,
    )

    service = UpdateServiceUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        service_id=service_id,
        data=payload,
    )

    response = ServiceResponse.model_validate(
        service
    )

    _record_service_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.UPDATE,
        service=response,
        before=before,
    )

    return response


@router.post(
    "/{service_id}/deactivate",
    response_model=ServiceResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate a service",
)
def deactivate_service(
    service_id: uuid.UUID,
    context: DeactivateServiceContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> ServiceResponse:
    """Deactivate one service without deleting its history."""

    repository = SQLAlchemyServiceRepository(
        session
    )

    before = _load_service_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        service_id=service_id,
    )

    service = DeactivateServiceUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        service_id=service_id,
    )

    response = ServiceResponse.model_validate(
        service
    )

    _record_service_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.DEACTIVATE,
        service=response,
        before=before,
    )

    return response


@router.post(
    "/{service_id}/reactivate",
    response_model=ServiceResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate a service",
)
def reactivate_service(
    service_id: uuid.UUID,
    context: ReactivateServiceContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> ServiceResponse:
    """Reactivate one service inside the authenticated tenant."""

    repository = SQLAlchemyServiceRepository(
        session
    )

    before = _load_service_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        service_id=service_id,
    )

    service = ReactivateServiceUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        service_id=service_id,
    )

    response = ServiceResponse.model_validate(
        service
    )

    _record_service_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.REACTIVATE,
        service=response,
        before=before,
    )

    return response


__all__ = [
    "router",
]
