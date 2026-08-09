"""FastAPI endpoints for tenant materials."""

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
from organizeg3_api.domain.audit import (
    AuditAction,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.domain.identity.permissions import (
    MaterialPermissions,
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


def _material_snapshot(
    material: MaterialResponse,
) -> dict[str, object]:
    """Build the complete auditable state of one material."""

    return {
        "id": material.id,
        "tenant_id": material.tenant_id,
        "code": material.code,
        "name": material.name,
        "category": material.category,
        "unit": material.unit,
        "brand_id": material.brand_id,
        "is_active": material.is_active,
        "created_at": _audit_datetime(
            material.created_at
        ),
        "updated_at": _audit_datetime(
            material.updated_at
        ),
    }


def _material_business_state(
    snapshot: dict[str, object],
) -> dict[str, object]:
    """Return fields that represent the material's business state."""

    return {
        key: value
        for key, value in snapshot.items()
        if key not in {
            "created_at",
            "updated_at",
        }
    }


def _load_material_snapshot(
    *,
    repository: SQLAlchemyMaterialRepository,
    tenant_id: uuid.UUID,
    material_id: uuid.UUID,
) -> dict[str, object] | None:
    """Load one material state before a mutation."""

    material = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        material_id=material_id,
    )

    if material is None:
        return None

    response = MaterialResponse.model_validate(
        material
    )

    return _material_snapshot(
        response
    )


def _record_material_event(
    *,
    session: Session,
    audit_context: AuditRequestContext,
    action: AuditAction,
    material: MaterialResponse,
    before: dict[str, object] | None = None,
) -> None:
    """Append one material event using the current transaction."""

    after = _material_snapshot(
        material
    )

    if (
        before is not None
        and _material_business_state(
            before
        )
        == _material_business_state(
            after
        )
    ):
        return

    RecordAuditEvent(
        SQLAlchemyAuditEventRepository(
            session
        )
    ).execute(
        context=audit_context,
        action=action,
        resource="materials",
        resource_id=material.id,
        before=before,
        after=after,
    )


@router.post(
    "",
    response_model=MaterialResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new material",
)
def create_material(
    payload: MaterialCreate,
    context: CreateMaterialContext,
    audit_context: AuditRequestContext,
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

    response = MaterialResponse.model_validate(
        material
    )

    _record_material_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.CREATE,
        material=response,
    )

    return response


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
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MaterialResponse:
    """Update a material inside the authenticated tenant."""

    repository = SQLAlchemyMaterialRepository(
        session
    )

    before = _load_material_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        material_id=material_id,
    )

    material = UpdateMaterialUseCase(
        repository
    ).execute(
        context.tenant_id,
        material_id,
        payload,
    )

    response = MaterialResponse.model_validate(
        material
    )

    _record_material_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.UPDATE,
        material=response,
        before=before,
    )

    return response


@router.post(
    "/{material_id}/deactivate",
    response_model=MaterialResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate a material",
)
def deactivate_material(
    material_id: uuid.UUID,
    context: DeactivateMaterialContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MaterialResponse:
    """Deactivate one material without deleting its history."""

    repository = SQLAlchemyMaterialRepository(
        session
    )

    before = _load_material_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        material_id=material_id,
    )

    material = DeactivateMaterialUseCase(
        repository
    ).execute(
        context.tenant_id,
        material_id,
    )

    response = MaterialResponse.model_validate(
        material
    )

    _record_material_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.DEACTIVATE,
        material=response,
        before=before,
    )

    return response


@router.post(
    "/{material_id}/reactivate",
    response_model=MaterialResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate a material",
)
def reactivate_material(
    material_id: uuid.UUID,
    context: ReactivateMaterialContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> MaterialResponse:
    """Reactivate one material inside the authenticated tenant."""

    repository = SQLAlchemyMaterialRepository(
        session
    )

    before = _load_material_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        material_id=material_id,
    )

    material = ReactivateMaterialUseCase(
        repository
    ).execute(
        context.tenant_id,
        material_id,
    )

    response = MaterialResponse.model_validate(
        material
    )

    _record_material_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.REACTIVATE,
        material=response,
        before=before,
    )

    return response


__all__ = [
    "router",
]
