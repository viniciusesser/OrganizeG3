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
from organizeg3_api.domain.customer.entity import (
    CustomerType,
)
from organizeg3_api.infrastructure.http.dependencies import (
    get_db_session,
    get_tenant_id,
)
from organizeg3_api.infrastructure.persistence.repositories.customer_repository import (
    SQLAlchemyCustomerRepository,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)

CustomerId = Annotated[
    int,
    Path(
        ge=1,
        description="Identificador interno do cliente",
    ),
]


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new customer",
)
def create_customer(
    payload: CustomerCreate,
    tenant_id: Annotated[
        uuid.UUID,
        Depends(get_tenant_id),
    ],
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> CustomerResponse:
    """Create a customer in the current tenant."""

    repository = SQLAlchemyCustomerRepository(
        session
    )

    customer = CreateCustomerUseCase(
        repository
    ).execute(
        tenant_id,
        payload,
    )

    return CustomerResponse.model_validate(
        customer
    )


@router.get(
    "",
    response_model=list[CustomerResponse],
    status_code=status.HTTP_200_OK,
    summary="List and search customers",
)
def list_customers(
    tenant_id: Annotated[
        uuid.UUID,
        Depends(get_tenant_id),
    ],
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
        Query(ge=1, le=200),
    ] = 100,
    offset: Annotated[
        int,
        Query(ge=0),
    ] = 0,
) -> list[CustomerResponse]:
    """List customers from the current tenant."""

    repository = SQLAlchemyCustomerRepository(
        session
    )

    customers = ListCustomersUseCase(
        repository
    ).execute(
        tenant_id,
        include_inactive=include_inactive,
        search=search,
        customer_type=customer_type,
        limit=limit,
        offset=offset,
    )

    return [
        CustomerResponse.model_validate(customer)
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
    tenant_id: Annotated[
        uuid.UUID,
        Depends(get_tenant_id),
    ],
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
        tenant_id,
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
    tenant_id: Annotated[
        uuid.UUID,
        Depends(get_tenant_id),
    ],
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> CustomerResponse:
    """Partially update a customer."""

    repository = SQLAlchemyCustomerRepository(
        session
    )

    customer = UpdateCustomerUseCase(
        repository
    ).execute(
        tenant_id,
        customer_id,
        payload,
    )

    return CustomerResponse.model_validate(
        customer
    )


@router.post(
    "/{customer_id}/archive",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
    summary="Archive one customer",
)
def archive_customer(
    customer_id: CustomerId,
    payload: CustomerVersionCommand,
    tenant_id: Annotated[
        uuid.UUID,
        Depends(get_tenant_id),
    ],
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> CustomerResponse:
    """Archive a customer while preserving history."""

    repository = SQLAlchemyCustomerRepository(
        session
    )

    customer = ArchiveCustomerUseCase(
        repository
    ).execute(
        tenant_id,
        customer_id,
        payload.row_version,
    )

    return CustomerResponse.model_validate(
        customer
    )


@router.post(
    "/{customer_id}/reactivate",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate one archived customer",
)
def reactivate_customer(
    customer_id: CustomerId,
    payload: CustomerVersionCommand,
    tenant_id: Annotated[
        uuid.UUID,
        Depends(get_tenant_id),
    ],
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> CustomerResponse:
    """Restore an archived customer."""

    repository = SQLAlchemyCustomerRepository(
        session
    )

    customer = ReactivateCustomerUseCase(
        repository
    ).execute(
        tenant_id,
        customer_id,
        payload.row_version,
    )

    return CustomerResponse.model_validate(
        customer
    )
