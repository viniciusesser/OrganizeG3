"""Shared authentication helpers for API tests."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import cast
import uuid

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.application.identity.exceptions import (
    InvalidAccessTokenError,
)
from organizeg3_api.domain.identity.authentication import (
    TokenVerifier,
    VerifiedToken,
)
from organizeg3_api.domain.identity.enums import (
    MembershipStatus,
)
from organizeg3_api.infrastructure.http.authentication import (
    get_token_verifier,
)
from organizeg3_api.infrastructure.persistence.models import (
    AccessProfileModel,
    AccessProfilePermissionModel,
    PermissionModel,
    TenantMembershipModel,
    TenantMembershipProfileModel,
    UserModel,
)

TEST_ACCESS_TOKEN = "test-access-token"  # noqa: S105


class StubTokenVerifier(TokenVerifier):
    """Token verifier used by API tests."""

    def __init__(
        self,
        verified_token: VerifiedToken,
    ) -> None:
        self._verified_token = verified_token

    def verify(
        self,
        access_token: str,
    ) -> VerifiedToken:
        if access_token != TEST_ACCESS_TOKEN:
            raise InvalidAccessTokenError

        return self._verified_token


@contextmanager
def override_token_verifier(
    client: TestClient,
    verifier: TokenVerifier,
) -> Iterator[None]:
    """Temporarily replace the external token verifier."""

    application = cast(
        FastAPI,
        client.app,
    )

    def override() -> TokenVerifier:
        return verifier

    application.dependency_overrides[
        get_token_verifier
    ] = override

    try:
        yield
    finally:
        application.dependency_overrides.pop(
            get_token_verifier,
            None,
        )


def authentication_headers(
    tenant_id: uuid.UUID,
    *,
    token: str = TEST_ACCESS_TOKEN,
) -> dict[str, str]:
    """Build authenticated request headers."""

    return {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": str(tenant_id),
    }


def create_active_membership(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    user: UserModel,
) -> TenantMembershipModel:
    """Create one active membership for an existing user."""

    membership = TenantMembershipModel(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        user_id=user.id,
        status=MembershipStatus.ACTIVE.value,
    )

    session.add(membership)
    session.flush()

    return membership


def create_test_user(
    session: Session,
    *,
    auth_user_id: uuid.UUID,
) -> UserModel:
    """Create the local user represented by a test token."""

    user = UserModel(
        id=uuid.uuid4(),
        auth_user_id=auth_user_id,
        email=f"{auth_user_id}@example.com",
        display_name="Usuário de Teste",
        is_active=True,
    )

    session.add(user)
    session.flush()

    return user


def _get_or_create_permission(
    session: Session,
    *,
    permission_code: str,
) -> PermissionModel:
    """Return one canonical permission row for a test code."""

    permission = session.scalar(
        select(PermissionModel).where(
            PermissionModel.code
            == permission_code
        )
    )

    if permission is not None:
        return permission

    resource = permission_code.split(
        ".",
        maxsplit=1,
    )[0]

    action = permission_code.rsplit(
        ".",
        maxsplit=1,
    )[-1]

    permission = PermissionModel(
        id=uuid.uuid4(),
        code=permission_code,
        name=permission_code,
        module=resource,
        resource=resource,
        action=action,
        is_active=True,
    )

    session.add(permission)
    session.flush()

    return permission


def grant_permissions(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    membership: TenantMembershipModel,
    permission_codes: tuple[str, ...],
) -> None:
    """Grant permissions through one tenant access profile."""

    profile = AccessProfileModel(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        code="API_TEST_ACCESS",
        name="API Test Access",
        is_system=False,
        is_active=True,
    )

    session.add(profile)
    session.flush()

    for permission_code in permission_codes:
        permission = _get_or_create_permission(
            session,
            permission_code=permission_code,
        )

        session.add(
            AccessProfilePermissionModel(
                access_profile_id=profile.id,
                permission_id=permission.id,
            )
        )

    session.add(
        TenantMembershipProfileModel(
            tenant_id=tenant_id,
            membership_id=membership.id,
            access_profile_id=profile.id,
        )
    )

    session.flush()
