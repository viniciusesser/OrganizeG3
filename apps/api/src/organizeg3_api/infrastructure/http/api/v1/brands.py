"""FastAPI endpoints for tenant brands."""

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
from organizeg3_api.domain.audit import (
    AuditAction,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.domain.identity.permissions import (
    BrandPermissions,
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


def _audit_datetime(
    value: datetime | None,
) -> datetime | None:
    """Normalize persistence timestamps to aware UTC for auditing."""

    if value is None:
        return None

    if value.tzinfo is None:
        return value.replace(
            tzinfo=UTC
        )

    return value.astimezone(
        UTC
    )


def _brand_snapshot(
    brand: BrandResponse,
) -> dict[str, object]:
    """Build the complete business snapshot of one brand."""

    return {
        "id": brand.id,
        "tenant_id": brand.tenant_id,
        "code": brand.code,
        "name": brand.name,
        "is_active": brand.is_active,
        "created_at": _audit_datetime(
            brand.created_at
        ),
        "updated_at": _audit_datetime(
            brand.updated_at
        ),
    }


def _record_brand_event(
    *,
    session: Session,
    audit_context: AuditRequestContext,
    action: AuditAction,
    brand: BrandResponse,
    before: dict[str, object] | None = None,
) -> None:
    """Append one brand event using the current transaction."""

    after = _brand_snapshot(
        brand
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
        resource="brands",
        resource_id=brand.id,
        before=before,
        after=after,
    )


def _load_brand_snapshot(
    *,
    repository: SQLAlchemyBrandRepository,
    tenant_id: uuid.UUID,
    brand_id: uuid.UUID,
) -> dict[str, object] | None:
    """Load the current state before one mutation."""

    brand = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        brand_id=brand_id,
    )

    if brand is None:
        return None

    return _brand_snapshot(
        BrandResponse.from_entity(
            brand
        )
    )


@router.post(
    "",
    response_model=BrandResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new brand",
)
def create_brand(
    payload: BrandCreate,
    context: CreateBrandContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BrandResponse:
    """Create a brand inside the authenticated tenant."""

    repository = SQLAlchemyBrandRepository(
        session
    )

    result = CreateBrand(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        data=payload,
    )

    _record_brand_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.CREATE,
        brand=result,
    )

    return result


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
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BrandResponse:
    """Update a brand inside the authenticated tenant."""

    repository = SQLAlchemyBrandRepository(
        session
    )

    before = _load_brand_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        brand_id=brand_id,
    )

    result = UpdateBrand(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        brand_id=brand_id,
        data=payload,
    )

    _record_brand_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.UPDATE,
        brand=result,
        before=before,
    )

    return result


@router.post(
    "/{brand_id}/deactivate",
    response_model=BrandResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate a brand",
)
def deactivate_brand(
    brand_id: uuid.UUID,
    context: DeactivateBrandContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BrandResponse:
    """Deactivate one brand without deleting its history."""

    repository = SQLAlchemyBrandRepository(
        session
    )

    before = _load_brand_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        brand_id=brand_id,
    )

    result = DeactivateBrand(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        brand_id=brand_id,
    )

    _record_brand_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.DEACTIVATE,
        brand=result,
        before=before,
    )

    return result


@router.post(
    "/{brand_id}/reactivate",
    response_model=BrandResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate a brand",
)
def reactivate_brand(
    brand_id: uuid.UUID,
    context: ReactivateBrandContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BrandResponse:
    """Reactivate one brand inside the authenticated tenant."""

    repository = SQLAlchemyBrandRepository(
        session
    )

    before = _load_brand_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        brand_id=brand_id,
    )

    result = ReactivateBrand(
        repository
    ).execute(
        tenant_id=context.tenant_id,
        brand_id=brand_id,
    )

    _record_brand_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.REACTIVATE,
        brand=result,
        before=before,
    )

    return result


__all__ = [
    "router",
]
