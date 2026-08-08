"""Unit tests for trusted HTTP audit context."""

from __future__ import annotations

import uuid

import pytest
from starlette.requests import Request

from organizeg3_api.domain.branch.context import (
    BranchContext,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
)
from organizeg3_api.infrastructure.http.audit_context import (
    get_audit_context,
)


def build_request(
    *,
    correlation_id: str | None = "correlation-test",
    device_id: str | None = "device-test",
) -> Request:
    """Build a minimal request with middleware state."""

    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/",
            "headers": [],
        }
    )

    if correlation_id is not None:
        request.state.correlation_id = correlation_id

    if device_id is not None:
        request.state.device_id = device_id

    return request


def build_authenticated_context(
    tenant_id: uuid.UUID,
) -> AuthenticatedContext:
    """Build an authenticated context for tests."""

    return AuthenticatedContext(
        tenant_id=tenant_id,
        user_id=uuid.uuid4(),
        membership_id=uuid.uuid4(),
        auth_user_id=uuid.uuid4(),
        email="user@example.com",
        display_name="Usuário Teste",
        permission_codes=frozenset(),
    )


def test_builds_audit_context_without_branch() -> None:
    tenant_id = uuid.uuid4()

    authenticated_context = (
        build_authenticated_context(
            tenant_id
        )
    )

    branch_context = BranchContext(
        tenant_id=tenant_id,
        branch_id=None,
    )

    request = build_request()

    audit_context = get_audit_context(
        request,
        authenticated_context,
        branch_context,
    )

    assert (
        audit_context.correlation_id
        == "correlation-test"
    )
    assert audit_context.tenant_id == tenant_id
    assert audit_context.branch_id is None
    assert (
        audit_context.user_id
        == authenticated_context.user_id
    )
    assert (
        audit_context.membership_id
        == authenticated_context.membership_id
    )
    assert (
        audit_context.auth_user_id
        == authenticated_context.auth_user_id
    )
    assert audit_context.device_id == "device-test"

    assert (
        request.state.audit_context
        == audit_context
    )


def test_builds_audit_context_with_branch() -> None:
    tenant_id = uuid.uuid4()
    branch_id = uuid.uuid4()

    authenticated_context = (
        build_authenticated_context(
            tenant_id
        )
    )

    branch_context = BranchContext(
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    request = build_request(
        device_id=None
    )

    audit_context = get_audit_context(
        request,
        authenticated_context,
        branch_context,
    )

    assert audit_context.branch_id == branch_id
    assert audit_context.device_id is None


def test_rejects_cross_tenant_branch_context() -> None:
    authenticated_context = (
        build_authenticated_context(
            uuid.uuid4()
        )
    )

    branch_context = BranchContext(
        tenant_id=uuid.uuid4(),
        branch_id=uuid.uuid4(),
    )

    request = build_request()

    with pytest.raises(
        RuntimeError,
        match="outro tenant",
    ):
        get_audit_context(
            request,
            authenticated_context,
            branch_context,
        )


def test_requires_correlation_id() -> None:
    tenant_id = uuid.uuid4()

    authenticated_context = (
        build_authenticated_context(
            tenant_id
        )
    )

    branch_context = BranchContext(
        tenant_id=tenant_id,
        branch_id=None,
    )

    request = build_request(
        correlation_id=None
    )

    with pytest.raises(
        RuntimeError,
        match="correlation ID",
    ):
        get_audit_context(
            request,
            authenticated_context,
            branch_context,
        )
