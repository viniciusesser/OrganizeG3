"""HTTP authorization tests for customer routes."""

from __future__ import annotations

from collections.abc import Iterator
import uuid

from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session
from tests.helpers.authentication import (
    StubTokenVerifier,
    authentication_headers,
    create_active_membership,
    create_test_user,
    grant_permissions,
    override_token_verifier,
)

from organizeg3_api.domain.identity.authentication import (
    VerifiedToken,
)
from organizeg3_api.domain.identity.permissions import (
    CustomerPermissions,
)

pytestmark = pytest.mark.api


@pytest.fixture
def unauthorized_customer_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide an authenticated membership with no permissions."""

    auth_user_id = uuid.uuid4()

    user = create_test_user(
        session,
        auth_user_id=auth_user_id,
    )

    create_active_membership(
        session,
        tenant_id=tenant_id,
        user=user,
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
        yield client


def assert_permission_denied(
    response,
    permission_code: str,
) -> None:
    """Assert the standardized permission error."""

    assert response.status_code == 403

    body = response.json()

    assert (
        body["error"]["code"]
        == "authorization.permission_required"
    )

    assert (
        body["error"]["details"]["permission"]
        == permission_code
    )


def test_rejects_customer_read_without_permission(
    unauthorized_customer_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_customer_client.get(
        "/api/v1/customers",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert_permission_denied(
        response,
        CustomerPermissions.READ,
    )


def test_rejects_customer_create_without_permission(
    unauthorized_customer_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_customer_client.post(
        "/api/v1/customers",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "name": "Sem Permissão",
        },
    )

    assert_permission_denied(
        response,
        CustomerPermissions.CREATE,
    )


def test_rejects_customer_update_without_permission(
    unauthorized_customer_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_customer_client.patch(
        "/api/v1/customers/1",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "row_version": 1,
            "name": "Sem Permissão",
        },
    )

    assert_permission_denied(
        response,
        CustomerPermissions.UPDATE,
    )


def test_rejects_customer_archive_without_permission(
    unauthorized_customer_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_customer_client.post(
        "/api/v1/customers/1/archive",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "row_version": 1,
        },
    )

    assert_permission_denied(
        response,
        CustomerPermissions.ARCHIVE,
    )


def test_rejects_customer_reactivate_without_permission(
    unauthorized_customer_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_customer_client.post(
        "/api/v1/customers/1/reactivate",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "row_version": 1,
        },
    )

    assert_permission_denied(
        response,
        CustomerPermissions.REACTIVATE,
    )


@pytest.mark.parametrize(
    "permission_code",
    [
        CustomerPermissions.READ,
        CustomerPermissions.CREATE,
        CustomerPermissions.UPDATE,
        CustomerPermissions.ARCHIVE,
        CustomerPermissions.REACTIVATE,
    ],
)
def test_granted_customer_permission_is_resolved(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    permission_code: str,
) -> None:
    auth_user_id = uuid.uuid4()

    user = create_test_user(
        session,
        auth_user_id=auth_user_id,
    )

    membership = create_active_membership(
        session,
        tenant_id=tenant_id,
        user=user,
    )

    grant_permissions(
        session,
        tenant_id=tenant_id,
        membership=membership,
        permission_codes=(
            permission_code,
        ),
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

    assert permission_code in (
        response.json()["permissions"]
    )
