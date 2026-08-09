"""FastAPI endpoints for tenant suppliers."""

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
from organizeg3_api.domain.audit import (
    AuditAction,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.domain.identity.permissions import (
    SupplierPermissions,
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


def _supplier_snapshot(
    supplier: SupplierResponse,
) -> dict[str, object]:
    """Build the complete auditable state of one supplier."""

    return {
        "id": supplier.id,
        "tenant_id": supplier.tenant_id,
        "code": supplier.code,
        "name": supplier.name,
        "trade_name": supplier.trade_name,
        "legal_name": supplier.legal_name,
        "document_number": supplier.document_number,
        "state_registration": supplier.state_registration,
        "email": supplier.email,
        "invoice_email": supplier.invoice_email,
        "phone": supplier.phone,
        "secondary_phone": supplier.secondary_phone,
        "website": supplier.website,
        "contact_name": supplier.contact_name,
        "postal_code": supplier.postal_code,
        "street": supplier.street,
        "number": supplier.number,
        "district": supplier.district,
        "city": supplier.city,
        "state": supplier.state,
        "is_active": supplier.is_active,
        "created_at": _audit_datetime(
            supplier.created_at
        ),
        "updated_at": _audit_datetime(
            supplier.updated_at
        ),
    }


def _supplier_business_state(
    snapshot: dict[str, object],
) -> dict[str, object]:
    """Return fields that represent supplier business state."""

    return {
        key: value
        for key, value in snapshot.items()
        if key not in {
            "created_at",
            "updated_at",
        }
    }


def _load_supplier_snapshot(
    *,
    repository: SQLAlchemySupplierRepository,
    tenant_id: uuid.UUID,
    supplier_id: uuid.UUID,
) -> dict[str, object] | None:
    """Load one supplier state before a mutation."""

    supplier = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        supplier_id=supplier_id,
    )

    if supplier is None:
        return None

    response = SupplierResponse.model_validate(
        supplier
    )

    return _supplier_snapshot(
        response
    )


def _record_supplier_event(
    *,
    session: Session,
    audit_context: AuditRequestContext,
    action: AuditAction,
    supplier: SupplierResponse,
    before: dict[str, object] | None = None,
) -> None:
    """Append one supplier audit event in the current transaction."""

    after = _supplier_snapshot(
        supplier
    )

    if (
        before is not None
        and _supplier_business_state(
            before
        )
        == _supplier_business_state(
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
        resource="suppliers",
        resource_id=supplier.id,
        before=before,
        after=after,
    )


@router.post(
    "",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new supplier",
)
def create_supplier(
    payload: SupplierCreate,
    context: CreateSupplierContext,
    audit_context: AuditRequestContext,
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

    response = SupplierResponse.model_validate(
        supplier
    )

    _record_supplier_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.CREATE,
        supplier=response,
    )

    return response


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
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> SupplierResponse:
    """Update a supplier inside the authenticated tenant."""

    repository = SQLAlchemySupplierRepository(
        session
    )

    before = _load_supplier_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        supplier_id=supplier_id,
    )

    supplier = UpdateSupplierUseCase(
        repository
    ).execute(
        context.tenant_id,
        supplier_id,
        payload,
    )

    response = SupplierResponse.model_validate(
        supplier
    )

    _record_supplier_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.UPDATE,
        supplier=response,
        before=before,
    )

    return response


@router.post(
    "/{supplier_id}/deactivate",
    response_model=SupplierResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate a supplier",
)
def deactivate_supplier(
    supplier_id: uuid.UUID,
    context: DeactivateSupplierContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> SupplierResponse:
    """Deactivate one supplier without deleting its history."""

    repository = SQLAlchemySupplierRepository(
        session
    )

    before = _load_supplier_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        supplier_id=supplier_id,
    )

    supplier = DeactivateSupplierUseCase(
        repository
    ).execute(
        context.tenant_id,
        supplier_id,
    )

    response = SupplierResponse.model_validate(
        supplier
    )

    _record_supplier_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.DEACTIVATE,
        supplier=response,
        before=before,
    )

    return response


@router.post(
    "/{supplier_id}/reactivate",
    response_model=SupplierResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate a supplier",
)
def reactivate_supplier(
    supplier_id: uuid.UUID,
    context: ReactivateSupplierContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> SupplierResponse:
    """Reactivate one supplier inside the authenticated tenant."""

    repository = SQLAlchemySupplierRepository(
        session
    )

    before = _load_supplier_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        supplier_id=supplier_id,
    )

    supplier = ReactivateSupplierUseCase(
        repository
    ).execute(
        context.tenant_id,
        supplier_id,
    )

    response = SupplierResponse.model_validate(
        supplier
    )

    _record_supplier_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.REACTIVATE,
        supplier=response,
        before=before,
    )

    return response


__all__ = [
    "router",
]
