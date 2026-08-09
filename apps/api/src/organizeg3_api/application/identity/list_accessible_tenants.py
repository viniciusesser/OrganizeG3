"""List tenants available to one authenticated identity."""

from __future__ import annotations

from organizeg3_api.domain.identity.authentication import (
    VerifiedToken,
)
from organizeg3_api.domain.identity.repository import (
    AccessibleTenant,
    IdentityRepository,
)


class ListAccessibleTenants:
    """Return active tenant memberships for a verified identity."""

    def __init__(
        self,
        repository: IdentityRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        *,
        token: VerifiedToken,
    ) -> tuple[AccessibleTenant, ...]:
        """List tenants the verified user can currently access."""

        return self._repository.list_accessible_tenants(
            auth_user_id=token.auth_user_id,
        )

