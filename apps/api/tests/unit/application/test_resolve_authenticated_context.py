"""Tests for authenticated context resolution."""

from __future__ import annotations

import uuid

import pytest

from organizeg3_api.application.identity.exceptions import (
    TenantMembershipUnavailableError,
)
from organizeg3_api.application.identity.resolve_authenticated_context import (
    ResolveAuthenticatedContext,
)
from organizeg3_api.domain.identity.authentication import (
    VerifiedToken,
)
from organizeg3_api.domain.identity.repository import (
    IdentityAccess,
)


class FakeIdentityRepository:
    """Configurable identity repository test double."""

    def __init__(
        self,
        access: IdentityAccess | None,
    ) -> None:
        self._access = access

    def resolve_active_access(
        self,
        *,
        auth_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> IdentityAccess | None:
        del auth_user_id
        del tenant_id

        return self._access


def test_resolves_authenticated_context() -> None:
    tenant_id = uuid.uuid4()
    auth_user_id = uuid.uuid4()

    access = IdentityAccess(
        user_id=uuid.uuid4(),
        membership_id=uuid.uuid4(),
        auth_user_id=auth_user_id,
        email="admin@example.com",
        display_name="Administrador",
        permission_codes=frozenset(
            {
                "customers.read",
                "customers.create",
            }
        ),
    )

    resolver = ResolveAuthenticatedContext(
        FakeIdentityRepository(
            access
        )
    )

    context = resolver.execute(
        token=VerifiedToken(
            auth_user_id=auth_user_id,
            role="authenticated",
            email="admin@example.com",
        ),
        tenant_id=tenant_id,
    )

    assert context.tenant_id == tenant_id
    assert context.user_id == access.user_id
    assert context.auth_user_id == auth_user_id
    assert context.has_permission(
        "customers.read"
    )


def test_rejects_unavailable_membership() -> None:
    resolver = ResolveAuthenticatedContext(
        FakeIdentityRepository(
            None
        )
    )

    with pytest.raises(
        TenantMembershipUnavailableError
    ):
        resolver.execute(
            token=VerifiedToken(
                auth_user_id=uuid.uuid4(),
                role="authenticated",
            ),
            tenant_id=uuid.uuid4(),
        )
