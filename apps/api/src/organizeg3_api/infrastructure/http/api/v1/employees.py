"""FastAPI endpoints for tenant employees."""

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
from organizeg3_api.domain.audit import (
    AuditAction,
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


def _audit_datetime(
    value: datetime | None,
) -> datetime | None:
    """Normalize persisted timestamps to aware UTC for audit snapshots."""

    if value is None:
        return None

    if value.tzinfo is None:
        return value.replace(
            tzinfo=UTC
        )

    return value.astimezone(
        UTC
    )


def _employee_snapshot(
    employee: EmployeeResponse,
) -> dict[str, object]:
    """Build the complete auditable state of one employee."""

    return {
        "id": employee.id,
        "tenant_id": employee.tenant_id,
        "branch_id": employee.branch_id,
        "code": employee.code,
        "full_name": employee.full_name,
        "document_number": employee.document_number,
        "email": employee.email,
        "phone": employee.phone,
        "job_title": employee.job_title,
        "contract_type": employee.contract_type,
        "status": employee.status,
        "birth_date": employee.birth_date,
        "admission_date": employee.admission_date,
        "termination_date": employee.termination_date,
        "is_active": employee.is_active,
        "created_at": _audit_datetime(
            employee.created_at
        ),
        "updated_at": _audit_datetime(
            employee.updated_at
        ),
    }


def _employee_business_state(
    snapshot: dict[str, object],
) -> dict[str, object]:
    """Return only fields representing employee business state."""

    return {
        key: value
        for key, value in snapshot.items()
        if key not in {
            "created_at",
            "updated_at",
        }
    }


def _load_employee_snapshot(
    *,
    repository: SQLAlchemyEmployeeRepository,
    tenant_id: uuid.UUID,
    employee_id: uuid.UUID,
) -> dict[str, object] | None:
    """Load one employee state before a mutation."""

    employee = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        employee_id=employee_id,
    )

    if employee is None:
        return None

    response = EmployeeResponse.model_validate(
        employee
    )

    return _employee_snapshot(
        response
    )


def _record_employee_event(
    *,
    session: Session,
    audit_context: AuditRequestContext,
    action: AuditAction,
    employee: EmployeeResponse,
    before: dict[str, object] | None = None,
) -> None:
    """Append one employee audit event in the current transaction."""

    after = _employee_snapshot(
        employee
    )

    if (
        before is not None
        and _employee_business_state(
            before
        )
        == _employee_business_state(
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
        resource="employees",
        resource_id=employee.id,
        before=before,
        after=after,
    )


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an employee",
)
def create_employee(
    payload: EmployeeCreate,
    context: CreateEmployeeContext,
    audit_context: AuditRequestContext,
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

    response = EmployeeResponse.model_validate(
        employee
    )

    _record_employee_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.CREATE,
        employee=response,
    )

    return response


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
    audit_context: AuditRequestContext,
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

    before = _load_employee_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        employee_id=employee_id,
    )

    employee = UpdateEmployeeUseCase(
        repository
    ).execute(
        context.tenant_id,
        employee_id,
        payload,
    )

    response = EmployeeResponse.model_validate(
        employee
    )

    _record_employee_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.UPDATE,
        employee=response,
        before=before,
    )

    return response


@router.post(
    "/{employee_id}/deactivate",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate an employee",
)
def deactivate_employee(
    employee_id: uuid.UUID,
    context: DeactivateEmployeeContext,
    audit_context: AuditRequestContext,
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

    before = _load_employee_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        employee_id=employee_id,
    )

    employee = DeactivateEmployeeUseCase(
        repository
    ).execute(
        context.tenant_id,
        employee_id,
    )

    response = EmployeeResponse.model_validate(
        employee
    )

    _record_employee_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.DEACTIVATE,
        employee=response,
        before=before,
    )

    return response


@router.post(
    "/{employee_id}/reactivate",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate an employee",
)
def reactivate_employee(
    employee_id: uuid.UUID,
    context: ReactivateEmployeeContext,
    audit_context: AuditRequestContext,
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

    before = _load_employee_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        employee_id=employee_id,
    )

    employee = ReactivateEmployeeUseCase(
        repository
    ).execute(
        context.tenant_id,
        employee_id,
    )

    response = EmployeeResponse.model_validate(
        employee
    )

    _record_employee_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.REACTIVATE,
        employee=response,
        before=before,
    )

    return response
