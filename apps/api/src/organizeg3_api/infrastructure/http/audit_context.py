"""HTTP dependency for trusted audit request context."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request

from organizeg3_api.domain.audit.context import (
    AuditContext,
)
from organizeg3_api.domain.branch.context import (
    BranchContext,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.infrastructure.http.authentication import (
    get_authenticated_context,
)
from organizeg3_api.infrastructure.http.branch_context import (
    get_branch_context,
)

AuthenticatedRequestContext = Annotated[
    AuthenticatedContext,
    Depends(get_authenticated_context),
]

BranchRequestContext = Annotated[
    BranchContext,
    Depends(get_branch_context),
]


def get_audit_context(
    request: Request,
    authenticated_context: AuthenticatedRequestContext,
    branch_context: BranchRequestContext,
) -> AuditContext:
    """Build trusted audit metadata for the current request."""

    if (
        branch_context.tenant_id
        != authenticated_context.tenant_id
    ):
        raise RuntimeError(
            "O contexto de filial pertence a outro tenant."
        )

    correlation_id = getattr(
        request.state,
        "correlation_id",
        None,
    )

    if (
        not isinstance(correlation_id, str)
        or not correlation_id.strip()
    ):
        raise RuntimeError(
            "A requisição não possui correlation ID."
        )

    device_id = getattr(
        request.state,
        "device_id",
        None,
    )

    if device_id is not None:
        device_id = str(device_id)

    audit_context = AuditContext(
        correlation_id=correlation_id,
        tenant_id=authenticated_context.tenant_id,
        branch_id=branch_context.branch_id,
        user_id=authenticated_context.user_id,
        membership_id=authenticated_context.membership_id,
        auth_user_id=authenticated_context.auth_user_id,
        device_id=device_id,
    )

    request.state.audit_context = audit_context

    return audit_context


AuditRequestContext = Annotated[
    AuditContext,
    Depends(get_audit_context),
]
