"""FastAPI endpoints for tenant services."""

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
    get_audit_context,
)
from organizeg3_api.infrastructure.http.authentication import (
    require_permission,
)
from organizeg3_api.infrastructure.http.dependencies import (
    get_db_session,
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


@router.post(
    "",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new service",
)
def create_service(
    payload: ServiceCreate,
    context: CreateServiceContext,
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

    return ServiceResponse.model_validate(
        service
    )


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
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> ServiceResponse:
    """Update a service inside the authenticated tenant."""

    repository = SQLAlchemyServiceRepository(
        session
    )

    service = UpdateServiceUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        service_id=service_id,
        data=payload,
    )

    return ServiceResponse.model_validate(
        service
    )


@router.post(
    "/{service_id}/deactivate",
    response_model=ServiceResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate a service",
)
def deactivate_service(
    service_id: uuid.UUID,
    context: DeactivateServiceContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> ServiceResponse:
    """Deactivate one service without deleting its history."""

    repository = SQLAlchemyServiceRepository(
        session
    )

    service = DeactivateServiceUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        service_id=service_id,
    )

    return ServiceResponse.model_validate(
        service
    )


@router.post(
    "/{service_id}/reactivate",
    response_model=ServiceResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate a service",
)
def reactivate_service(
    service_id: uuid.UUID,
    context: ReactivateServiceContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> ServiceResponse:
    """Reactivate one service inside the authenticated tenant."""

    repository = SQLAlchemyServiceRepository(
        session
    )

    service = ReactivateServiceUseCase(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        service_id=service_id,
    )

    return ServiceResponse.model_validate(
        service
    )


__all__ = [
    "router",
]
