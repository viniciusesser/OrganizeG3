"""HTTP tests for customer identity validation."""

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


def test_create_normalizes_identity_and_contact_data(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "name": "Cliente Normalizado",
            "customer_type": "INDIVIDUAL",
            "document_number": "529.982.247-25",
            "email": "  CLIENTE@EXAMPLE.COM  ",
            "phone": "+55 (18) 99999-0000",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert (
        body["document_number"]
        == "52998224725"
    )

    assert (
        body["email"]
        == "cliente@example.com"
    )

    assert (
        body["phone"]
        == "18999990000"
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        (
            "document_number",
            "529.982.247-24",
        ),
        (
            "email",
            "email-invalido",
        ),
        (
            "phone",
            "9999-0000",
        ),
    ],
)
def test_create_rejects_invalid_identity_data(
    client: TestClient,
    tenant_id: uuid.UUID,
    field: str,
    value: str,
) -> None:
    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "name": "Cliente Inválido",
            field: value,
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "request.validation_error"
    )


def test_create_rejects_document_incompatible_with_customer_type(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "name": "Empresa Inválida",
            "customer_type": "CORPORATE",
            "document_number": "529.982.247-25",
        },
    )

    assert response.status_code == 422


def test_rejects_duplicate_document_in_same_tenant(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    payload = {
        "name": "Primeiro Cliente",
        "document_number": "529.982.247-25",
    }

    first_response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json=payload,
    )

    assert first_response.status_code == 201

    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "name": "Segundo Cliente",
            "document_number": "52998224725",
        },
    )

    assert response.status_code == 409

    assert (
        response.json()["error"]["code"]
        == "customer.duplicate"
    )

    assert (
        response.json()["error"]["details"]
        == {
            "field": "document_number",
        }
    )


def test_rejects_duplicate_email_case_insensitively(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    first_response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "name": "Primeiro Cliente",
            "email": "cliente@example.com",
        },
    )

    assert first_response.status_code == 201

    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "name": "Segundo Cliente",
            "email": "CLIENTE@EXAMPLE.COM",
        },
    )

    assert response.status_code == 409

    assert (
        response.json()["error"]["details"]
        == {
            "field": "email",
        }
    )


def test_allows_same_identity_data_in_other_tenant(
    client: TestClient,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    payload = {
        "name": "Cliente",
        "document_number": "52998224725",
        "email": "cliente@example.com",
    }

    first_response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json=payload,
    )

    assert first_response.status_code == 201

    response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            other_tenant_id
        ),
        json=payload,
    )

    assert response.status_code == 201


def test_update_rejects_identity_used_by_another_customer(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    first_response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "name": "Primeiro",
            "email": "primeiro@example.com",
        },
    )

    assert first_response.status_code == 201
    first = first_response.json()

    second_response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "name": "Segundo",
            "email": "segundo@example.com",
        },
    )

    assert second_response.status_code == 201
    second = second_response.json()

    response = client.patch(
        f"/api/v1/customers/{second['id']}",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "row_version": second["row_version"],
            "email": first["email"],
        },
    )

    assert response.status_code == 409

    assert (
        response.json()["error"]["details"]
        == {
            "field": "email",
        }
    )


def test_update_keeps_own_identity_data(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_response = client.post(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "name": "Cliente",
            "document_number": "52998224725",
            "email": "cliente@example.com",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()

    response = client.patch(
        f"/api/v1/customers/{created['id']}",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "row_version": created["row_version"],
            "name": "Cliente Atualizado",
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["name"]
        == "Cliente Atualizado"
    )
