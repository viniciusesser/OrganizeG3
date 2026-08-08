"""FastAPI endpoints for tenant materials."""

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

from organizeg3_api.application.material.schemas import (
    MaterialCreate,
    MaterialResponse,
    MaterialUpdate,
)
from organizeg3_api.application.material.use_cases import (
    CreateMaterialUseCase,
    DeactivateMaterialUseCase,
    GetMaterialUseCase,
    ListMaterialsUseCase,
    ReactivateMaterialUseCase,
    UpdateMaterialUseCase,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.domain.identity.permissions import (
    MaterialPermissions,
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
from organizeg3_api.infrastructure.persistence.repositories.material_repository import (
    SQLAlchemyMaterialRepository,
)

router = APIRouter(
    prefix="/materials",
    tags=["Materials"],
    dependencies=[
        Depends(get_audit_context),
    ],
)


ReadMaterialContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            MaterialPermissions.READ
        )
    ),
]

CreateMaterialContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            MaterialPermissions.CREATE
        )
    ),
]

UpdateMaterialContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            MaterialPermissions.UPDATE
        )
    ),
]

DeactivateMaterialContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            MaterialPermissions.DEACTIVATE
        )
    ),
]

ReactivateMaterialContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            MaterialPermissions.REACTIVATE
        )
    ),
]


@router.post(
    "",
    response_model=MaterialResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new material",
)
def create_material(
    payload: MaterialCreate,
    context: CreateMaterialContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MaterialResponse:
    """Create a material inside the authenticated tenant."""

    repository = SQLAlchemyMaterialRepository(
        session
    )

    material = CreateMaterialUseCase(
        repository
    ).execute(
        context.tenant_id,
        payload,
    )

    return MaterialResponse.model_validate(
        material
    )


@router.get(
    "",
    response_model=list[MaterialResponse],
    status_code=status.HTTP_200_OK,
    summary="List and search materials",
)
def list_materials(
    context: ReadMaterialContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
    *,
    include_inactive: Annotated[
        bool,
        Query(
            description="Include inactive materials"
        ),
    ] = False,
    search: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=255,
            description="Search material data",
        ),
    ] = None,
    category: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=100,
            description="Filter by material category",
        ),
    ] = None,
    brand_id: Annotated[
        uuid.UUID | None,
        Query(
            description="Filter by brand identifier"
        ),
    ] = None,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=200,
            description="Maximum materials to return",
        ),
    ] = 100,
    offset: Annotated[
        int,
        Query(
            ge=0,
            description="Number of materials to skip",
        ),
    ] = 0,
) -> list[MaterialResponse]:
    """List materials belonging to the authenticated tenant."""

    repository = SQLAlchemyMaterialRepository(
        session
    )

    materials = ListMaterialsUseCase(
        repository
    ).execute(
        context.tenant_id,
        include_inactive=include_inactive,
        search=search,
        category=category,
        brand_id=brand_id,
        limit=limit,
        offset=offset,
    )

    return [
        MaterialResponse.model_validate(
            material
        )
        for material in materials
    ]


@router.get(
    "/{material_id}",
    response_model=MaterialResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a material",
)
def get_material(
    material_id: uuid.UUID,
    context: ReadMaterialContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MaterialResponse:
    """Return one material from the authenticated tenant."""

    repository = SQLAlchemyMaterialRepository(
        session
    )

    material = GetMaterialUseCase(
        repository
    ).execute(
        context.tenant_id,
        material_id,
    )

    return MaterialResponse.model_validate(
        material
    )


@router.patch(
    "/{material_id}",
    response_model=MaterialResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a material",
)
def update_material(
    material_id: uuid.UUID,
    payload: MaterialUpdate,
    context: UpdateMaterialContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MaterialResponse:
    """Update a material inside the authenticated tenant."""

    repository = SQLAlchemyMaterialRepository(
        session
    )

    material = UpdateMaterialUseCase(
        repository
    ).execute(
        context.tenant_id,
        material_id,
        payload,
    )

    return MaterialResponse.model_validate(
        material
    )


@router.post(
    "/{material_id}/deactivate",
    response_model=MaterialResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate a material",
)
def deactivate_material(
    material_id: uuid.UUID,
    context: DeactivateMaterialContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MaterialResponse:
    """Deactivate one material without deleting its history."""

    repository = SQLAlchemyMaterialRepository(
        session
    )

    material = DeactivateMaterialUseCase(
        repository
    ).execute(
        context.tenant_id,
        material_id,
    )

    return MaterialResponse.model_validate(
        material
    )


@router.post(
    "/{material_id}/reactivate",
    response_model=MaterialResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate a material",
)
def reactivate_material(
    material_id: uuid.UUID,
    context: ReactivateMaterialContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MaterialResponse:
    """Reactivate one material inside the authenticated tenant."""

    repository = SQLAlchemyMaterialRepository(
        session
    )

    material = ReactivateMaterialUseCase(
        repository
    ).execute(
        context.tenant_id,
        material_id,
    )

    return MaterialResponse.model_validate(
        material
    )


__all__ = [
    "router",
]
