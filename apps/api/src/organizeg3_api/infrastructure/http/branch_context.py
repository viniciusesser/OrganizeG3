"""HTTP dependencies for optional tenant branch context."""

from __future__ import annotations

from typing import Annotated
import uuid

from fastapi import Depends, Header

from organizeg3_api.application.branch.exceptions import (
    BranchRequiredError,
)
from organizeg3_api.application.branch.resolve_active_branch import (
    ResolveActiveBranch,
)
from organizeg3_api.core.logging import set_request_context
from organizeg3_api.domain.branch.context import (
    BranchContext,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.infrastructure.http.authentication import (
    get_authenticated_context,
)
from organizeg3_api.infrastructure.http.dependencies import (
    DatabaseSession,
    parse_branch_header,
)
from organizeg3_api.infrastructure.persistence.repositories.branch_repository import (
    SQLAlchemyBranchRepository,
)

AuthenticatedRequestContext = Annotated[
    AuthenticatedContext,
    Depends(get_authenticated_context),
]


def get_branch_context(
    database_session: DatabaseSession,
    authenticated_context: AuthenticatedRequestContext,
    raw_branch_id: Annotated[
        str | None,
        Header(alias="X-Branch-ID"),
    ] = None,
) -> BranchContext:
    """Resolve an optional branch inside the authenticated tenant."""

    branch_id = parse_branch_header(
        raw_branch_id
    )

    repository = SQLAlchemyBranchRepository(
        database_session
    )

    resolver = ResolveActiveBranch(
        repository
    )

    resolved_branch_id = resolver.execute(
        tenant_id=authenticated_context.tenant_id,
        branch_id=branch_id,
    )

    if resolved_branch_id is not None:
        set_request_context(
            branch_id=str(
                resolved_branch_id
            )
        )

    return BranchContext(
        tenant_id=authenticated_context.tenant_id,
        branch_id=resolved_branch_id,
    )


BranchRequestContext = Annotated[
    BranchContext,
    Depends(get_branch_context),
]


def require_branch(
    branch_context: BranchRequestContext,
) -> uuid.UUID:
    """Require a validated branch for branch-scoped operations."""

    if branch_context.branch_id is None:
        raise BranchRequiredError(
            "Esta operação exige a seleção de uma filial.",
            details={
                "reason": "branch_required",
            },
        )

    return branch_context.branch_id


RequiredBranchId = Annotated[
    uuid.UUID,
    Depends(require_branch),
]
