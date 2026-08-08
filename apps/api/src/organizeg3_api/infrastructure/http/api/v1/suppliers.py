"""FastAPI endpoints for tenant suppliers."""

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

from organizeg3_api.application.supplier.schemas import (
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate,
)
from organizeg3_api.application.supplier.use_cases import (
    CreateSupplierUseCase,
    DeactivateSupplierUseCase,
    GetSupplierUseCase,
    ListSuppliersUseCase,
    ReactivateSupplierUseCase,
    UpdateSupplierUseCase,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.domain.identity.permissions import (
    SupplierPermissions,
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
from organizeg3_api.infrastructure.persistence.repositories.supplier_repository import (
    SQLAlchemySupplierRepository,
)

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
    dependencies=[
        Depends(get_audit_context),
    ],
)


ReadSupplierContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            SupplierPermissions.READ
        )
    ),
]

CreateSupplierContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            SupplierPermissions.CREATE
        )
    ),
]

UpdateSupplierContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            SupplierPermissions.UPDATE
        )
    ),
]

DeactivateSupplierContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            SupplierPermissions.DEACTIVATE
        )
    ),
]

ReactivateSupplierContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            SupplierPermissions.REACTIVATE
        )
    ),
]


@router.post(
    "",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new supplier",
)
def create_supplier(
    payload: SupplierCreate,
    context: CreateSupplierContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> SupplierResponse:
    """Create a supplier inside the authenticated tenant."""

    repository = SQLAlchemySupplierRepository(
        session
    )

    supplier = CreateSupplierUseCase(
        repository
    ).execute(
        context.tenant_id,
        payload,
    )

    return SupplierResponse.model_validate(
        supplier
    )


@router.get(
    "",
    response_model=list[SupplierResponse],
    status_code=status.HTTP_200_OK,
    summary="List and search suppliers",
)
def list_suppliers(
    context: ReadSupplierContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
    *,
    include_inactive: Annotated[
        bool,
        Query(
            description="Include inactive suppliers"
        ),
    ] = False,
    search: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=255,
            description="Search supplier data",
        ),
    ] = None,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=200,
            description="Maximum suppliers to return",
        ),
    ] = 100,
    offset: Annotated[
        int,
        Query(
            ge=0,
            description="Number of suppliers to skip",
        ),
    ] = 0,
) -> list[SupplierResponse]:
    """List suppliers belonging to the authenticated tenant."""

    repository = SQLAlchemySupplierRepository(
        session
    )

    suppliers = ListSuppliersUseCase(
        repository
    ).execute(
        context.tenant_id,
        include_inactive=include_inactive,
        search=search,
        limit=limit,
        offset=offset,
    )

    return [
        SupplierResponse.model_validate(
            supplier
        )
        for supplier in suppliers
    ]


@router.get(
    "/{supplier_id}",
    response_model=SupplierResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a supplier",
)
def get_supplier(
    supplier_id: uuid.UUID,
    context: ReadSupplierContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> SupplierResponse:
    """Return one supplier from the authenticated tenant."""

    repository = SQLAlchemySupplierRepository(
        session
    )

    supplier = GetSupplierUseCase(
        repository
    ).execute(
        context.tenant_id,
        supplier_id,
    )

    return SupplierResponse.model_validate(
        supplier
    )


@router.patch(
    "/{supplier_id}",
    response_model=SupplierResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a supplier",
)
def update_supplier(
    supplier_id: uuid.UUID,
    payload: SupplierUpdate,
    context: UpdateSupplierContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> SupplierResponse:
    """Update a supplier inside the authenticated tenant."""

    repository = SQLAlchemySupplierRepository(
        session
    )

    supplier = UpdateSupplierUseCase(
        repository
    ).execute(
        context.tenant_id,
        supplier_id,
        payload,
    )

    return SupplierResponse.model_validate(
        supplier
    )


@router.post(
    "/{supplier_id}/deactivate",
    response_model=SupplierResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate a supplier",
)
def deactivate_supplier(
    supplier_id: uuid.UUID,
    context: DeactivateSupplierContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> SupplierResponse:
    """Deactivate one supplier without deleting its history."""

    repository = SQLAlchemySupplierRepository(
        session
    )

    supplier = DeactivateSupplierUseCase(
        repository
    ).execute(
        context.tenant_id,
        supplier_id,
    )

    return SupplierResponse.model_validate(
        supplier
    )


@router.post(
    "/{supplier_id}/reactivate",
    response_model=SupplierResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate a supplier",
)
def reactivate_supplier(
    supplier_id: uuid.UUID,
    context: ReactivateSupplierContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> SupplierResponse:
    """Reactivate one supplier inside the authenticated tenant."""

    repository = SQLAlchemySupplierRepository(
        session
    )

    supplier = ReactivateSupplierUseCase(
        repository
    ).execute(
        context.tenant_id,
        supplier_id,
    )

    return SupplierResponse.model_validate(
        supplier
    )


__all__ = [
    "router",
]
