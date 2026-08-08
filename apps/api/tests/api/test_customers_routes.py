"""HTTP contract tests for customer routes."""

from __future__ import annotations

import uuid

from fastapi.testclient import TestClient
import pytest
from tests.helpers.authentication import (
    TEST_ACCESS_TOKEN,
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


def test_health_endpoint(
    client: TestClient,
) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_customer_route_is_registered(
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


def test_creates_customer(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "name": "Cliente API",
            "customer_type": "CORPORATE",
            "email": "api@example.com",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["tenant_id"] == str(
        tenant_id
    )

    assert body["name"] == "Cliente API"
    assert body["code"].startswith("CUST-")
    assert body["row_version"] == 1


def test_lists_only_header_tenant(
    client: TestClient,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    first_response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "name": "Cliente A",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            other_tenant_id
        ),
        json={
            "name": "Cliente B",
        },
    )

    assert second_response.status_code == 201

    response = client.get(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    assert [
        item["name"]
        for item in response.json()
    ] == ["Cliente A"]


def test_rejects_missing_tenant_header(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/v1/customers",
        headers={
            "Authorization": (
                f"Bearer {TEST_ACCESS_TOKEN}"
            ),
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "validation.error"
    )


def test_rejects_invalid_tenant_header(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/v1/customers",
        headers={
            "Authorization": (
                f"Bearer {TEST_ACCESS_TOKEN}"
            ),
            "X-Tenant-ID": "invalid",
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "validation.error"
    )


def test_rejects_tenant_in_request_body(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "tenant_id": str(
                uuid.uuid4()
            ),
            "name": "Cliente Inválido",
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "request.validation_error"
    )


def test_returns_standard_validation_error(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "name": "",
        },
    )

    assert response.status_code == 422

    body = response.json()

    assert body["success"] is False

    assert (
        body["error"]["code"]
        == "request.validation_error"
    )

    assert "correlation_id" in body["meta"]


def create_customer_for_query_tests(
    client: TestClient,
    tenant_id: uuid.UUID,
    *,
    name: str,
    customer_type: str = "INDIVIDUAL",
    **extra: object,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "name": name,
        "customer_type": customer_type,
    }

    payload.update(extra)

    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json=payload,
    )

    assert response.status_code == 201

    return response.json()


def test_gets_customer_by_id(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer_for_query_tests(
        client,
        tenant_id,
        name="Cliente Consultado",
    )

    response = client.get(
        f"/api/v1/customers/{created['id']}",
        headers=tenant_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    assert (
        response.json()["name"]
        == "Cliente Consultado"
    )


def test_does_not_get_customer_from_other_tenant(
    client: TestClient,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    created = create_customer_for_query_tests(
        client,
        tenant_id,
        name="Cliente A",
    )

    response = client.get(
        f"/api/v1/customers/{created['id']}",
        headers=tenant_headers(
            other_tenant_id
        ),
    )

    assert response.status_code == 404

    assert (
        response.json()["error"]["code"]
        == "resource.not_found"
    )


def test_searches_filters_and_paginates_customers(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_customer_for_query_tests(
        client,
        tenant_id,
        name="Empresa Alfa",
        customer_type="CORPORATE",
    )

    create_customer_for_query_tests(
        client,
        tenant_id,
        name="Empresa Beta",
        customer_type="CORPORATE",
    )

    create_customer_for_query_tests(
        client,
        tenant_id,
        name="Pessoa Gama",
    )

    response = client.get(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        params={
            "search": "Empresa",
            "customer_type": "CORPORATE",
            "limit": 1,
            "offset": 1,
        },
    )

    assert response.status_code == 200

    assert [
        item["name"]
        for item in response.json()
    ] == ["Empresa Beta"]
