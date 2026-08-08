"""HTTP tests for tenant context authorization."""

from __future__ import annotations

import uuid

from fastapi.testclient import TestClient
import pytest
from tests.helpers.authentication import (
    authentication_headers,
)

pytestmark = pytest.mark.api


@pytest.fixture(autouse=True)
def authorize_customer_requests(
    authenticated_customer_client: TestClient,
) -> None:
    """Authorize customer requests for this test module."""


def tenant_headers(
    tenant_id: uuid.UUID,
) -> dict[str, str]:
    """Build authenticated tenant headers."""

    return authentication_headers(
        tenant_id
    )


def test_accepts_registered_active_tenant(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = client.get(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200


def test_rejects_unknown_tenant(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/v1/customers",
        headers=tenant_headers(
            uuid.uuid4()
        ),
    )

    assert response.status_code == 403

    body = response.json()

    assert (
        body["error"]["code"]
        == "authorization.permission_denied"
    )

    assert (
        body["error"]["details"]["reason"]
        == "tenant_unavailable"
    )


def test_rejects_inactive_tenant(
    client: TestClient,
    inactive_tenant_id: uuid.UUID,
) -> None:
    response = client.get(
        "/api/v1/customers",
        headers=tenant_headers(
            inactive_tenant_id
        ),
    )

    assert response.status_code == 403

    assert (
        response.json()["error"]["code"]
        == "authorization.permission_denied"
    )


def test_rejects_null_tenant_uuid(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/v1/customers",
        headers=tenant_headers(
            uuid.UUID(int=0)
        ),
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "validation.error"
    )
