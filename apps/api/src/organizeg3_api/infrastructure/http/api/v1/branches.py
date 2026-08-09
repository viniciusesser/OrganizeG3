"""FastAPI endpoints for tenant branches."""

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
from organizeg3_api.application.branch.schemas import (
    BranchCreate,
    BranchResponse,
    BranchUpdate,
)
from organizeg3_api.application.branch.use_cases import (
    CreateBranchUseCase,
    DeactivateBranchUseCase,
    GetBranchUseCase,
    ListBranchesUseCase,
    ReactivateBranchUseCase,
    UpdateBranchUseCase,
)
from organizeg3_api.domain.audit import (
    AuditAction,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.domain.identity.permissions import (
    BranchPermissions,
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
from organizeg3_api.infrastructure.persistence.repositories.branch_repository import (
    SQLAlchemyBranchRepository,
)

router = APIRouter(
    prefix="/branches",
    tags=["Branches"],
    dependencies=[
        Depends(get_audit_context),
    ],
)


ReadBranchContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            BranchPermissions.READ
        )
    ),
]

CreateBranchContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            BranchPermissions.CREATE
        )
    ),
]

UpdateBranchContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            BranchPermissions.UPDATE
        )
    ),
]

DeactivateBranchContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            BranchPermissions.DEACTIVATE
        )
    ),
]

ReactivateBranchContext = Annotated[
    AuthenticatedContext,
    Depends(
        require_permission(
            BranchPermissions.REACTIVATE
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


def _branch_snapshot(
    branch: BranchResponse,
) -> dict[str, object]:
    """Build the complete auditable public state of one branch."""

    return {
        "id": branch.id,
        "tenant_id": branch.tenant_id,
        "code": branch.code,
        "name": branch.name,
        "legal_name": branch.legal_name,
        "document_number": branch.document_number,
        "state_registration": branch.state_registration,
        "email": branch.email,
        "phone": branch.phone,
        "website": branch.website,
        "street": branch.street,
        "number": branch.number,
        "district": branch.district,
        "city": branch.city,
        "state": branch.state,
        "postal_code": branch.postal_code,
        "is_headquarters": branch.is_headquarters,
        "is_active": branch.is_active,
        "created_at": _audit_datetime(
            branch.created_at
        ),
        "updated_at": _audit_datetime(
            branch.updated_at
        ),
    }


def _branch_business_state(
    snapshot: dict[str, object],
) -> dict[str, object]:
    """Return branch state excluding persistence timestamps."""

    return {
        key: value
        for key, value in snapshot.items()
        if key not in {
            "created_at",
            "updated_at",
        }
    }


def _load_branch_snapshot(
    *,
    repository: SQLAlchemyBranchRepository,
    tenant_id: uuid.UUID,
    branch_id: uuid.UUID,
) -> dict[str, object] | None:
    """Load one branch state before a mutation."""

    branch = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    if branch is None:
        return None

    response = BranchResponse.model_validate(
        branch
    )

    return _branch_snapshot(
        response
    )


def _record_branch_event(
    *,
    session: Session,
    audit_context: AuditRequestContext,
    action: AuditAction,
    branch: BranchResponse,
    before: dict[str, object] | None = None,
) -> None:
    """Append one branch audit event in the current transaction."""

    after = _branch_snapshot(
        branch
    )

    if (
        before is not None
        and _branch_business_state(
            before
        )
        == _branch_business_state(
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
        resource="branches",
        resource_id=branch.id,
        before=before,
        after=after,
    )


@router.post(
    "",
    response_model=BranchResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create branch",
)
def create_branch(
    payload: BranchCreate,
    context: CreateBranchContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BranchResponse:
    """Create one branch owned by the authenticated tenant."""

    repository = SQLAlchemyBranchRepository(
        session
    )

    branch = CreateBranchUseCase(
        repository
    ).execute(
        context.tenant_id,
        payload,
    )

    response = BranchResponse.model_validate(
        branch
    )

    _record_branch_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.CREATE,
        branch=response,
    )

    return response


@router.get(
    "",
    response_model=list[BranchResponse],
    status_code=status.HTTP_200_OK,
    summary="List branches",
)
def list_branches(
    context: ReadBranchContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
    *,
    include_inactive: Annotated[
        bool,
        Query(),
    ] = False,
    search: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=255,
        ),
    ] = None,
    is_headquarters: Annotated[
        bool | None,
        Query(),
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
) -> list[BranchResponse]:
    """List filtered and paginated tenant branches."""

    repository = SQLAlchemyBranchRepository(
        session
    )

    branches = ListBranchesUseCase(
        repository
    ).execute(
        context.tenant_id,
        include_inactive=include_inactive,
        search=search,
        is_headquarters=is_headquarters,
        limit=limit,
        offset=offset,
    )

    return [
        BranchResponse.model_validate(
            branch
        )
        for branch in branches
    ]


@router.get(
    "/{branch_id}",
    response_model=BranchResponse,
    status_code=status.HTTP_200_OK,
    summary="Get branch",
)
def get_branch(
    branch_id: uuid.UUID,
    context: ReadBranchContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BranchResponse:
    """Return one branch owned by the authenticated tenant."""

    repository = SQLAlchemyBranchRepository(
        session
    )

    branch = GetBranchUseCase(
        repository
    ).execute(
        context.tenant_id,
        branch_id,
    )

    return BranchResponse.model_validate(
        branch
    )


@router.patch(
    "/{branch_id}",
    response_model=BranchResponse,
    status_code=status.HTTP_200_OK,
    summary="Update branch",
)
def update_branch(
    branch_id: uuid.UUID,
    payload: BranchUpdate,
    context: UpdateBranchContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BranchResponse:
    """Partially update one tenant branch."""

    repository = SQLAlchemyBranchRepository(
        session
    )

    before = _load_branch_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        branch_id=branch_id,
    )

    branch = UpdateBranchUseCase(
        repository
    ).execute(
        context.tenant_id,
        branch_id,
        payload,
    )

    response = BranchResponse.model_validate(
        branch
    )

    _record_branch_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.UPDATE,
        branch=response,
        before=before,
    )

    return response


@router.post(
    "/{branch_id}/deactivate",
    response_model=BranchResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate branch",
)
def deactivate_branch(
    branch_id: uuid.UUID,
    context: DeactivateBranchContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BranchResponse:
    """Deactivate one tenant branch."""

    repository = SQLAlchemyBranchRepository(
        session
    )

    before = _load_branch_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        branch_id=branch_id,
    )

    branch = DeactivateBranchUseCase(
        repository
    ).execute(
        context.tenant_id,
        branch_id,
    )

    response = BranchResponse.model_validate(
        branch
    )

    _record_branch_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.DEACTIVATE,
        branch=response,
        before=before,
    )

    return response


@router.post(
    "/{branch_id}/reactivate",
    response_model=BranchResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate branch",
)
def reactivate_branch(
    branch_id: uuid.UUID,
    context: ReactivateBranchContext,
    audit_context: AuditRequestContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BranchResponse:
    """Reactivate one tenant branch."""

    repository = SQLAlchemyBranchRepository(
        session
    )

    before = _load_branch_snapshot(
        repository=repository,
        tenant_id=context.tenant_id,
        branch_id=branch_id,
    )

    branch = ReactivateBranchUseCase(
        repository
    ).execute(
        context.tenant_id,
        branch_id,
    )

    response = BranchResponse.model_validate(
        branch
    )

    _record_branch_event(
        session=session,
        audit_context=audit_context,
        action=AuditAction.REACTIVATE,
        branch=response,
        before=before,
    )

    return response
