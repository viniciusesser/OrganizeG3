"""FastAPI endpoints for customers."""

from __future__ import annotations

from typing import Annotated
import uuid

from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    status,
)
from sqlalchemy.orm import Session

from organizeg3_api.application.audit import (
    RecordAuditEvent,
)
from organizeg3_api.application.customer.schemas import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
    CustomerVersionCommand,
)
from organizeg3_api.application.customer.use_cases import (
    ArchiveCustomerUseCase,
    CreateCustomerUseCase,
    GetCustomerUseCase,
    ListCustomersUseCase,
    ReactivateCustomerUseCase,
    UpdateCustomerUseCase,
)
from organizeg3_api.domain.audit import (
    AuditAction,
)
from organizeg3_api.domain.customer.entity import (
    CustomerType,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.domain.identity.permissions import (
    CustomerPermissions,
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
from organizeg3_api.infrastructure.persistence.repositories.customer_repository import (
    SQLAlchemyCustomerRepository,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    dependencies=[
        Depends(get_audit_context),
    ],
)

CustomerId = Annotated[
    int,
    Path(
        ge=1,
        description="Identificador interno do cliente",
    ),
]

ReadCustomerContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            CustomerPermissions.READ
        )
    ),
]

CreateCustomerContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            CustomerPermissions.CREATE
        )
    ),
]

UpdateCustomerContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            CustomerPermissions.UPDATE
        )
    ),
]

ArchiveCustomerContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            CustomerPermissions.ARCHIVE
        )
    ),
]

ReactivateCustomerContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            CustomerPermissions.REACTIVATE
        )
    ),
]


def _customer_snapshot(
    customer: CustomerResponse,
) -> dict[str, object]:
    """Build the complete public auditable customer state."""

    return {
        "id": customer.id,
        "tenant_id": customer.tenant_id,
        "code": customer.code,
        "name": customer.name,
        "customer_type": customer.customer_type,
        "document_number": customer.document_number,
        "email": customer.email,
        "phone": customer.phone,
        "is_active": customer.is_active,
        "row_version": customer.row_version,
    }


def _customer_business_state(
    snapshot: dict[str, object],
) -> dict[str, object]:
    """Return customer state excluding concurrency metadata."""

    return {
        key: value
        for key, value in snapshot.items()
        if key != "row_version"
    }


def _load_customer_snapshot(
    *,
    repository: SQLAlchemyCustomerRepository,
    tenant_id: uuid.UUID,
    customer_id: int,
    include_archived: bool = False,
) -> dict[str, object] | None:
    """Load one customer state before a mutation."""

    customer = repository.get_by_id(
        tenant_id,
        customer_id,
        include_archived=include_archived,
    )

    if customer is None:
        return None

    response = CustomerResponse.model_validate(
        customer
    )

    return _customer_snapshot(
        response
    )


def _record_customer_event(
    *,
    session: Session,
    audit_context: AuditRequestContext,
    action: AuditAction,
    customer: CustomerResponse,
    before: dict[str, object] | None = None,
) -> None:
    """Append one customer audit event in the current transaction."""

    after = _customer_snapshot(
        customer
    )

    if (
        before is not None
        and _customer_business_state(
            before
        )
        == _customer_business_state(
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
        resource="customers",
        resource_id=customer.id,
        before=before,
        after=after,
    )


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new customer",
)
def create_customer(
    payload: CustomerCreate,
    context: CreateCustomerContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> CustomerResponse:
    """Create a customer in the authenticated tenant."""

    repository = SQLAlchemyCustomerRepository(
        session
    )

    customer = CreateCustomerUseCase(
        repository
    ).execute(
        context.tenant_id,
        payload,
    )

    response = CustomerResponse.model_validate(
        customer
    )

    _record_customer_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.CREATE,
        customer=response,
    )

    return response


@router.get(
    "",
    response_model=list[CustomerResponse],
    status_code=status.HTTP_200_OK,
    summary="List and search customers",
)
def list_customers(
    context: ReadCustomerContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
    *,
    include_inactive: Annotated[
        bool,
        Query(
            description="Include inactive customers"
        ),
    ] = False,
    search: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=255,
            description="Search customer data",
        ),
    ] = None,
    customer_type: Annotated[
        CustomerType | None,
        Query(
            description=(
                "Filter by customer classification"
            )
        ),
    ] = None,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=200,
        ),
    ] = 100,
    offset: Annotated[
        int,
        Query(
            ge=0,
        ),
    ] = 0,
) -> list[CustomerResponse]:
    """List customers from the authenticated tenant."""

    repository = SQLAlchemyCustomerRepository(
        session
    )

    customers = ListCustomersUseCase(
        repository
    ).execute(
        context.tenant_id,
        include_inactive=include_inactive,
        search=search,
        customer_type=customer_type,
        limit=limit,
        offset=offset,
    )

    return [
        CustomerResponse.model_validate(
            customer
        )
        for customer in customers
    ]


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
    summary="Get one customer",
)
def get_customer(
    customer_id: CustomerId,
    context: ReadCustomerContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> CustomerResponse:
    """Return one non-archived customer."""

    repository = SQLAlchemyCustomerRepository(
        session
    )

    customer = GetCustomerUseCase(
        repository
    ).execute(
        context.tenant_id,
        customer_id,
    )

    return CustomerResponse.model_validate(
        customer
    )


@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
    summary="Update one customer",
)
def update_customer(
    customer_id: CustomerId,
    payload: CustomerUpdate,
    context: UpdateCustomerContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> CustomerResponse:
    """Partially update a customer."""

    repository = SQLAlchemyCustomerRepository(
        session
    )

    before = _load_customer_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        customer_id=customer_id,
    )

    customer = UpdateCustomerUseCase(
        repository
    ).execute(
        context.tenant_id,
        customer_id,
        payload,
    )

    response = CustomerResponse.model_validate(
        customer
    )

    _record_customer_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.UPDATE,
        customer=response,
        before=before,
    )

    return response


@router.post(
    "/{customer_id}/archive",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
    summary="Archive one customer",
)
def archive_customer(
    customer_id: CustomerId,
    payload: CustomerVersionCommand,
    context: ArchiveCustomerContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> CustomerResponse:
    """Archive a customer while preserving history."""

    repository = SQLAlchemyCustomerRepository(
        session
    )

    before = _load_customer_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        customer_id=customer_id,
        include_archived=True,
    )

    customer = ArchiveCustomerUseCase(
        repository
    ).execute(
        context.tenant_id,
        customer_id,
        payload.row_version,
    )

    response = CustomerResponse.model_validate(
        customer
    )

    _record_customer_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.ARCHIVE,
        customer=response,
        before=before,
    )

    return response


@router.post(
    "/{customer_id}/reactivate",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate one archived customer",
)
def reactivate_customer(
    customer_id: CustomerId,
    payload: CustomerVersionCommand,
    context: ReactivateCustomerContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> CustomerResponse:
    """Restore an archived customer."""

    repository = SQLAlchemyCustomerRepository(
        session
    )

    before = _load_customer_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        customer_id=customer_id,
        include_archived=True,
    )

    customer = ReactivateCustomerUseCase(
        repository
    ).execute(
        context.tenant_id,
        customer_id,
        payload.row_version,
    )

    response = CustomerResponse.model_validate(
        customer
    )

    _record_customer_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.REACTIVATE,
        customer=response,
        before=before,
    )

    return response
