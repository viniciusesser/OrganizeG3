"""HTTP tests for customer update and lifecycle."""

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


def create_customer(
    client: TestClient,
    tenant_id: uuid.UUID,
    *,
    name: str = "Cliente",
    **extra: object,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "name": name,
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


def test_updates_customer_and_version(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        client,
        tenant_id,
        name="Cliente Original",
        email="original@example.com",
    )

    response = client.patch(
        f"/api/v1/customers/{created['id']}",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "row_version": created["row_version"],
            "name": "Cliente Atualizado",
            "email": None,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "Cliente Atualizado"
    assert body["email"] is None
    assert body["row_version"] == 2


def test_rejects_stale_update(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        client,
        tenant_id,
    )

    first_update = client.patch(
        f"/api/v1/customers/{created['id']}",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "row_version": created["row_version"],
            "name": "Primeira alteração",
        },
    )

    assert first_update.status_code == 200

    stale_update = client.patch(
        f"/api/v1/customers/{created['id']}",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "row_version": created["row_version"],
            "name": "Alteração antiga",
        },
    )

    assert stale_update.status_code == 409

    assert (
        stale_update.json()["error"]["code"]
        == "concurrency.conflict"
    )


def test_rejects_cross_tenant_update(
    client: TestClient,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        client,
        tenant_id,
    )

    response = client.patch(
        f"/api/v1/customers/{created['id']}",
        headers=tenant_headers(
            other_tenant_id
        ),
        json={
            "row_version": created["row_version"],
            "name": "Tentativa cruzada",
        },
    )

    assert response.status_code == 404


def test_archives_and_hides_customer(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        client,
        tenant_id,
        name="Arquivável",
    )

    archived_response = client.post(
        (
            f"/api/v1/customers/"
            f"{created['id']}/archive"
        ),
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "row_version": created["row_version"],
        },
    )

    assert archived_response.status_code == 200

    archived = archived_response.json()

    assert archived["is_active"] is False
    assert archived["row_version"] == 2

    get_response = client.get(
        f"/api/v1/customers/{created['id']}",
        headers=tenant_headers(
            tenant_id
        ),
    )

    assert get_response.status_code == 404

    list_response = client.get(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
        params={
            "include_inactive": True,
        },
    )

    assert list_response.status_code == 200
    assert list_response.json() == []


def test_reactivates_archived_customer(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        client,
        tenant_id,
        name="Reativável",
    )

    archived_response = client.post(
        (
            f"/api/v1/customers/"
            f"{created['id']}/archive"
        ),
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "row_version": created["row_version"],
        },
    )

    assert archived_response.status_code == 200

    archived = archived_response.json()

    response = client.post(
        (
            f"/api/v1/customers/"
            f"{created['id']}/reactivate"
        ),
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "row_version": archived["row_version"],
        },
    )

    assert response.status_code == 200

    restored = response.json()

    assert restored["is_active"] is True
    assert restored["row_version"] == 3

    get_response = client.get(
        f"/api/v1/customers/{created['id']}",
        headers=tenant_headers(
            tenant_id
        ),
    )

    assert get_response.status_code == 200


def test_rejects_archiving_twice(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        client,
        tenant_id,
    )

    first_response = client.post(
        (
            f"/api/v1/customers/"
            f"{created['id']}/archive"
        ),
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "row_version": created["row_version"],
        },
    )

    assert first_response.status_code == 200

    archived = first_response.json()

    second_response = client.post(
        (
            f"/api/v1/customers/"
            f"{created['id']}/archive"
        ),
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "row_version": archived["row_version"],
        },
    )

    assert second_response.status_code == 409

    assert (
        second_response.json()["error"]["code"]
        == "workflow.invalid_transition"
    )


def test_rejects_invalid_reactivation(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        client,
        tenant_id,
    )

    response = client.post(
        (
            f"/api/v1/customers/"
            f"{created['id']}/reactivate"
        ),
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "row_version": created["row_version"],
        },
    )

    assert response.status_code == 409

    assert (
        response.json()["error"]["code"]
        == "workflow.invalid_transition"
    )


def test_archived_customer_cannot_be_updated(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        client,
        tenant_id,
    )

    archived_response = client.post(
        (
            f"/api/v1/customers/"
            f"{created['id']}/archive"
        ),
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "row_version": created["row_version"],
        },
    )

    assert archived_response.status_code == 200

    archived = archived_response.json()

    response = client.patch(
        f"/api/v1/customers/{created['id']}",
        headers=tenant_headers(
            tenant_id
        ),
        json={
            "row_version": archived["row_version"],
            "name": "Não permitido",
        },
    )

    assert response.status_code == 404
