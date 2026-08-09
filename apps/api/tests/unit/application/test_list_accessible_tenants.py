"""Tests for accessible tenant listing."""

from __future__ import annotations

import uuid

from organizeg3_api.application.identity.list_accessible_tenants import (
    ListAccessibleTenants,
)
from organizeg3_api.domain.identity.authentication import (
    VerifiedToken,
)
from organizeg3_api.domain.identity.repository import (
    AccessibleTenant,
)


class StubIdentityRepository:
    """Identity repository stub for tenant listing tests."""

    def __init__(
        self,
        tenants: tuple[
            AccessibleTenant,
            ...,
        ],
    ) -> None:
        self.tenants = tenants
        self.received_auth_user_id: (
            uuid.UUID | None
        ) = None

    def list_accessible_tenants(
        self,
        *,
        auth_user_id: uuid.UUID,
    ) -> tuple[
        AccessibleTenant,
        ...,
    ]:
        self.received_auth_user_id = (
            auth_user_id
        )
        return self.tenants

    def resolve_active_access(
        self,
        *,
        auth_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> None:
        del auth_user_id
        del tenant_id


def test_lists_tenants_for_verified_identity() -> None:
    auth_user_id = uuid.uuid4()

    expected = (
        AccessibleTenant(
            tenant_id=uuid.uuid4(),
            membership_id=uuid.uuid4(),
            name="Empresa A",
        ),
        AccessibleTenant(
            tenant_id=uuid.uuid4(),
            membership_id=uuid.uuid4(),
            name="Empresa B",
        ),
    )

    repository = StubIdentityRepository(
        expected
    )

    use_case = ListAccessibleTenants(
        repository
    )

    result = use_case.execute(
        token=VerifiedToken(
            auth_user_id=auth_user_id,
            role="authenticated",
        )
    )

    assert result == expected
    assert (
        repository.received_auth_user_id
        == auth_user_id
    )


def test_returns_empty_tuple_when_user_has_no_tenants() -> None:
    repository = StubIdentityRepository(
        ()
    )

    use_case = ListAccessibleTenants(
        repository
    )

    result = use_case.execute(
        token=VerifiedToken(
            auth_user_id=uuid.uuid4(),
            role="authenticated",
        )
    )

    assert result == ()

