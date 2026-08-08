"""Resolve the authenticated OrganizeG3 request context."""

from __future__ import annotations

import uuid

from organizeg3_api.application.identity.exceptions import (
    TenantMembershipUnavailableError,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
    VerifiedToken,
)
from organizeg3_api.domain.identity.repository import (
    IdentityRepository,
)


class ResolveAuthenticatedContext:
    """Resolve local tenant access from a verified identity."""

    def __init__(
        self,
        repository: IdentityRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        *,
        token: VerifiedToken,
        tenant_id: uuid.UUID,
    ) -> AuthenticatedContext:
        """Return the authenticated context for one tenant."""

        access = self._repository.resolve_active_access(
            auth_user_id=token.auth_user_id,
            tenant_id=tenant_id,
        )

        if access is None:
            raise TenantMembershipUnavailableError

        return AuthenticatedContext(
            tenant_id=tenant_id,
            user_id=access.user_id,
            membership_id=access.membership_id,
            auth_user_id=access.auth_user_id,
            email=access.email,
            display_name=access.display_name,
            permission_codes=access.permission_codes,
        )
