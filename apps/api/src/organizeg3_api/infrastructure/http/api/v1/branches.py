"""FastAPI endpoints for tenant branches."""

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
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.domain.identity.permissions import (
    BranchPermissions,
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


@router.post(
    "",
    response_model=BranchResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create branch",
)
def create_branch(
    payload: BranchCreate,
    context: CreateBranchContext,
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

    return BranchResponse.model_validate(
        branch
    )


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
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BranchResponse:
    """Partially update one tenant branch."""

    repository = SQLAlchemyBranchRepository(
        session
    )

    branch = UpdateBranchUseCase(
        repository
    ).execute(
        context.tenant_id,
        branch_id,
        payload,
    )

    return BranchResponse.model_validate(
        branch
    )


@router.post(
    "/{branch_id}/deactivate",
    response_model=BranchResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate branch",
)
def deactivate_branch(
    branch_id: uuid.UUID,
    context: DeactivateBranchContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BranchResponse:
    """Deactivate one tenant branch."""

    repository = SQLAlchemyBranchRepository(
        session
    )

    branch = DeactivateBranchUseCase(
        repository
    ).execute(
        context.tenant_id,
        branch_id,
    )

    return BranchResponse.model_validate(
        branch
    )


@router.post(
    "/{branch_id}/reactivate",
    response_model=BranchResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate branch",
)
def reactivate_branch(
    branch_id: uuid.UUID,
    context: ReactivateBranchContext,
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> BranchResponse:
    """Reactivate one tenant branch."""

    repository = SQLAlchemyBranchRepository(
        session
    )

    branch = ReactivateBranchUseCase(
        repository
    ).execute(
        context.tenant_id,
        branch_id,
    )

    return BranchResponse.model_validate(
        branch
    )
