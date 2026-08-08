"""FastAPI endpoints for tenant brands."""

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

from organizeg3_api.application.brand.schemas import (
    BrandCreate,
    BrandResponse,
    BrandUpdate,
)
from organizeg3_api.application.brand.use_cases import (
    CreateBrand,
    DeactivateBrand,
    GetBrand,
    ListBrands,
    ReactivateBrand,
    UpdateBrand,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.domain.identity.permissions import (
    BrandPermissions,
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
from organizeg3_api.infrastructure.persistence.repositories.brand_repository import (
    SQLAlchemyBrandRepository,
)

router = APIRouter(
    prefix="/brands",
    tags=["Brands"],
    dependencies=[
        Depends(get_audit_context),
    ],
)


ReadBrandContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            BrandPermissions.READ
        )
    ),
]

CreateBrandContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            BrandPermissions.CREATE
        )
    ),
]

UpdateBrandContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            BrandPermissions.UPDATE
        )
    ),
]

DeactivateBrandContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            BrandPermissions.DEACTIVATE
        )
    ),
]

ReactivateBrandContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            BrandPermissions.REACTIVATE
        )
    ),
]


@router.post(
    "",
    response_model=BrandResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new brand",
)
def create_brand(
    payload: BrandCreate,
    context: CreateBrandContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BrandResponse:
    """Create a brand inside the authenticated tenant."""

    repository = SQLAlchemyBrandRepository(
        session
    )

    return CreateBrand(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        data=payload,
    )


@router.get(
    "",
    response_model=list[BrandResponse],
    status_code=status.HTTP_200_OK,
    summary="List and search brands",
)
def list_brands(
    context: ReadBrandContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
    *,
    include_inactive: Annotated[
        bool,
        Query(
            description="Include inactive brands"
        ),
    ] = False,
    search: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=255,
            description="Search brand code or name",
        ),
    ] = None,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=200,
            description="Maximum brands to return",
        ),
    ] = 100,
    offset: Annotated[
        int,
        Query(
            ge=0,
            description="Number of brands to skip",
        ),
    ] = 0,
) -> list[BrandResponse]:
    """List brands belonging to the authenticated tenant."""

    repository = SQLAlchemyBrandRepository(
        session
    )

    return ListBrands(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        include_inactive=include_inactive,
        search=search,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{brand_id}",
    response_model=BrandResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a brand",
)
def get_brand(
    brand_id: uuid.UUID,
    context: ReadBrandContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BrandResponse:
    """Return one brand from the authenticated tenant."""

    repository = SQLAlchemyBrandRepository(
        session
    )

    return GetBrand(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        brand_id=brand_id,
    )


@router.patch(
    "/{brand_id}",
    response_model=BrandResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a brand",
)
def update_brand(
    brand_id: uuid.UUID,
    payload: BrandUpdate,
    context: UpdateBrandContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BrandResponse:
    """Update a brand inside the authenticated tenant."""

    repository = SQLAlchemyBrandRepository(
        session
    )

    return UpdateBrand(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        brand_id=brand_id,
        data=payload,
    )


@router.post(
    "/{brand_id}/deactivate",
    response_model=BrandResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate a brand",
)
def deactivate_brand(
    brand_id: uuid.UUID,
    context: DeactivateBrandContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BrandResponse:
    """Deactivate one brand without deleting its history."""

    repository = SQLAlchemyBrandRepository(
        session
    )

    return DeactivateBrand(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        brand_id=brand_id,
    )


@router.post(
    "/{brand_id}/reactivate",
    response_model=BrandResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate a brand",
)
def reactivate_brand(
    brand_id: uuid.UUID,
    context: ReactivateBrandContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BrandResponse:
    """Reactivate one brand inside the authenticated tenant."""

    repository = SQLAlchemyBrandRepository(
        session
    )

    return ReactivateBrand(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        brand_id=brand_id,
    )


__all__ = [
    "router",
]
