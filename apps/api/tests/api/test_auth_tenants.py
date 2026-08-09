"""HTTP tests for authenticated tenant discovery."""

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
from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.models.user import (
    TenantMembershipModel,
    UserModel,
)

VALID_TOKEN = "valid-token"  # noqa: S105
INVALID_TOKEN = "invalid-token"  # noqa: S105


class StubTokenVerifier(TokenVerifier):
    """Token verifier used by tenant discovery tests."""

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
        if access_token != VALID_TOKEN:
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


def authorization_headers(
    *,
    token: str = VALID_TOKEN,
) -> dict[str, str]:
    """Build bearer-only headers for tenant discovery."""

    return {
        "Authorization": (
            f"Bearer {token}"
        ),
    }


def test_lists_only_active_tenants_for_authenticated_user(
    client: TestClient,
    session: Session,
) -> None:
    auth_user_id = uuid.uuid4()

    user = UserModel(
        id=uuid.uuid4(),
        auth_user_id=auth_user_id,
        email="admin@example.com",
        display_name="Administrador",
        is_active=True,
    )

    active_tenant = TenantRecordModel(
        id=uuid.uuid4(),
        name="Empresa Ativa",
        is_active=True,
    )

    inactive_tenant = TenantRecordModel(
        id=uuid.uuid4(),
        name="Empresa Inativa",
        is_active=False,
    )

    session.add_all(
        [
            user,
            active_tenant,
            inactive_tenant,
        ]
    )
    session.flush()

    active_membership = TenantMembershipModel(
        id=uuid.uuid4(),
        tenant_id=active_tenant.id,
        user_id=user.id,
        status=MembershipStatus.ACTIVE.value,
    )

    inactive_tenant_membership = (
        TenantMembershipModel(
            id=uuid.uuid4(),
            tenant_id=inactive_tenant.id,
            user_id=user.id,
            status=MembershipStatus.ACTIVE.value,
        )
    )

    session.add_all(
        [
            active_membership,
            inactive_tenant_membership,
        ]
    )
    session.flush()

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
            "/api/v1/auth/tenants",
            headers=authorization_headers(),
        )

    assert response.status_code == 200

    assert response.json() == [
        {
            "tenant_id": str(
                active_tenant.id
            ),
            "membership_id": str(
                active_membership.id
            ),
            "name": "Empresa Ativa",
        }
    ]


def test_does_not_require_tenant_header(
    client: TestClient,
    session: Session,
) -> None:
    auth_user_id = uuid.uuid4()

    user = UserModel(
        id=uuid.uuid4(),
        auth_user_id=auth_user_id,
        email="user@example.com",
        display_name="Usuário",
        is_active=True,
    )

    session.add(user)
    session.flush()

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
            "/api/v1/auth/tenants",
            headers=authorization_headers(),
        )

    assert response.status_code == 200
    assert response.json() == []


def test_rejects_invalid_token(
    client: TestClient,
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
            "/api/v1/auth/tenants",
            headers=authorization_headers(
                token=INVALID_TOKEN,
            ),
        )

    assert response.status_code == 401
    assert (
        response.json()["error"]["code"]
        == "authentication.invalid_token"
    )
