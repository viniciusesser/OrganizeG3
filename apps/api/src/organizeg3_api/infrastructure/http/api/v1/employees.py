"""FastAPI endpoints for tenant employees."""

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

from organizeg3_api.application.employee import (
    CreateEmployeeUseCase,
    DeactivateEmployeeUseCase,
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
    GetEmployeeUseCase,
    ListEmployeesUseCase,
    ReactivateEmployeeUseCase,
    UpdateEmployeeUseCase,
)
from organizeg3_api.domain.employee import (
    EmploymentStatus,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.domain.identity.permissions import (
    EmployeePermissions,
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
from organizeg3_api.infrastructure.persistence.repositories.employee_repository import (
    SQLAlchemyEmployeeRepository,
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    dependencies=[
        Depends(
            get_audit_context
        ),
    ],
)


ReadEmployeeContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            EmployeePermissions.READ
        )
    ),
]

CreateEmployeeContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            EmployeePermissions.CREATE
        )
    ),
]

UpdateEmployeeContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            EmployeePermissions.UPDATE
        )
    ),
]

DeactivateEmployeeContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            EmployeePermissions.DEACTIVATE
        )
    ),
]

ReactivateEmployeeContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            EmployeePermissions.REACTIVATE
        )
    ),
]


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an employee",
)
def create_employee(
    payload: EmployeeCreate,
    context: CreateEmployeeContext,
    session: Annotated[
        Session,
        Depends(
            get_db_session
        ),
    ],
) -> EmployeeResponse:
    """Create an employee inside the authenticated tenant."""

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    employee = CreateEmployeeUseCase(
        repository
    ).execute(
        context.tenant_id,
        payload,
    )

    return EmployeeResponse.model_validate(
        employee
    )


@router.get(
    "",
    response_model=list[
        EmployeeResponse
    ],
    status_code=status.HTTP_200_OK,
    summary="List employees",
)
def list_employees(
    context: ReadEmployeeContext,
    session: Annotated[
        Session,
        Depends(
            get_db_session
        ),
    ],
    *,
    include_inactive: bool = False,
    search: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=255,
        ),
    ] = None,
    branch_id: uuid.UUID | None = None,
    employee_status: Annotated[
        EmploymentStatus | None,
        Query(
            alias="status"
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
            ge=0
        ),
    ] = 0,
) -> list[EmployeeResponse]:
    """List employees belonging to the authenticated tenant."""

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    employees = ListEmployeesUseCase(
        repository
    ).execute(
        context.tenant_id,
        include_inactive=include_inactive,
        search=search,
        branch_id=branch_id,
        status=employee_status,
        limit=limit,
        offset=offset,
    )

    return [
        EmployeeResponse.model_validate(
            employee
        )
        for employee in employees
    ]


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get an employee",
)
def get_employee(
    employee_id: uuid.UUID,
    context: ReadEmployeeContext,
    session: Annotated[
        Session,
        Depends(
            get_db_session
        ),
    ],
) -> EmployeeResponse:
    """Return one employee belonging to the authenticated tenant."""

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    employee = GetEmployeeUseCase(
        repository
    ).execute(
        context.tenant_id,
        employee_id,
    )

    return EmployeeResponse.model_validate(
        employee
    )


@router.patch(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an employee",
)
def update_employee(
    employee_id: uuid.UUID,
    payload: EmployeeUpdate,
    context: UpdateEmployeeContext,
    session: Annotated[
        Session,
        Depends(
            get_db_session
        ),
    ],
) -> EmployeeResponse:
    """Update an employee belonging to the authenticated tenant."""

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    employee = UpdateEmployeeUseCase(
        repository
    ).execute(
        context.tenant_id,
        employee_id,
        payload,
    )

    return EmployeeResponse.model_validate(
        employee
    )


@router.post(
    "/{employee_id}/deactivate",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate an employee",
)
def deactivate_employee(
    employee_id: uuid.UUID,
    context: DeactivateEmployeeContext,
    session: Annotated[
        Session,
        Depends(
            get_db_session
        ),
    ],
) -> EmployeeResponse:
    """Deactivate an employee without deleting its history."""

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    employee = DeactivateEmployeeUseCase(
        repository
    ).execute(
        context.tenant_id,
        employee_id,
    )

    return EmployeeResponse.model_validate(
        employee
    )


@router.post(
    "/{employee_id}/reactivate",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate an employee",
)
def reactivate_employee(
    employee_id: uuid.UUID,
    context: ReactivateEmployeeContext,
    session: Annotated[
        Session,
        Depends(
            get_db_session
        ),
    ],
) -> EmployeeResponse:
    """Reactivate an inactive employee."""

    repository = SQLAlchemyEmployeeRepository(
        session
    )

    employee = ReactivateEmployeeUseCase(
        repository
    ).execute(
        context.tenant_id,
        employee_id,
    )

    return EmployeeResponse.model_validate(
        employee
    )
