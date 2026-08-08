"""HTTP tests for authenticated identity context."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import cast
import uuid

from fastapi import FastAPI
from fastapi.testclient import TestClient
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
    TenantMembershipModel,
    UserModel,
)


class StubTokenVerifier(TokenVerifier):
    """Token verifier used by API tests."""

    def __init__(
        self,
        verified_token: VerifiedToken,
    ) -> None:
        self._verified_token = (
            verified_token
        )

    def verify(
        self,
        access_token: str,
    ) -> VerifiedToken:
        if access_token != "valid-token":  # noqa: S105
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
    token: str = "valid-token",  # noqa: S107
) -> dict[str, str]:
    """Build authenticated request headers."""

    return {
        "Authorization": (
            f"Bearer {token}"
        ),
        "X-Tenant-ID": str(
            tenant_id
        ),
    }


def create_active_membership(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    auth_user_id: uuid.UUID,
) -> tuple[
    UserModel,
    TenantMembershipModel,
]:
    """Create one active local user and membership."""

    user = UserModel(
        id=uuid.uuid4(),
        auth_user_id=auth_user_id,
        email="admin@example.com",
        display_name="Administrador",
        is_active=True,
    )

    session.add(user)
    session.flush()

    membership = TenantMembershipModel(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        user_id=user.id,
        status=MembershipStatus.ACTIVE.value,
    )

    session.add(membership)
    session.flush()

    return user, membership


def test_returns_authenticated_context(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    auth_user_id = uuid.uuid4()

    user, membership = create_active_membership(
        session,
        tenant_id=tenant_id,
        auth_user_id=auth_user_id,
    )

    verifier = StubTokenVerifier(
        VerifiedToken(
            auth_user_id=auth_user_id,
            role="authenticated",
            email=user.email,
        )
    )

    with override_token_verifier(
        client,
        verifier,
    ):
        response = client.get(
            "/api/v1/auth/me",
            headers=authentication_headers(
                tenant_id
            ),
        )

    assert response.status_code == 200

    body = response.json()

    assert body["tenant_id"] == str(
        tenant_id
    )

    assert body["user_id"] == str(
        user.id
    )

    assert body["membership_id"] == str(
        membership.id
    )

    assert body["auth_user_id"] == str(
        auth_user_id
    )

    assert body["display_name"] == (
        "Administrador"
    )


def test_rejects_invalid_bearer_token(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    verifier = StubTokenVerifier(
        VerifiedToken(
            auth_user_id=uuid.uuid4(),
            role="authenticated",
        )
    )

    with override_token_verifier(
        client,
        verifier,
    ):
        response = client.get(
            "/api/v1/auth/me",
            headers=authentication_headers(
                tenant_id,
                token="invalid-token",  # noqa: S106
            ),
        )

    assert response.status_code == 401
    assert (
        response.json()["error"]["code"]
        == "authentication.invalid_token"
    )


def test_rejects_cross_tenant_access(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    auth_user_id = uuid.uuid4()

    create_active_membership(
        session,
        tenant_id=tenant_id,
        auth_user_id=auth_user_id,
    )

    verifier = StubTokenVerifier(
        VerifiedToken(
            auth_user_id=auth_user_id,
            role="authenticated",
        )
    )

    with override_token_verifier(
        client,
        verifier,
    ):
        response = client.get(
            "/api/v1/auth/me",
            headers=authentication_headers(
                other_tenant_id
            ),
        )

    assert response.status_code == 403

    assert (
        response.json()["error"]["code"]
        == (
            "authorization."
            "tenant_membership_unavailable"
        )
    )
