"""HTTP contract tests for tenant context validation."""

from __future__ import annotations

import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantModel,
)


def tenant_headers(
    tenant_id: uuid.UUID,
) -> dict[str, str]:
    return {
        "X-Tenant-ID": str(tenant_id),
    }


def test_accepts_existing_active_tenant(
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

    assert (
        response.json()["error"]["code"]
        == "tenant.unavailable"
    )


def test_rejects_disabled_tenant(
    client: TestClient,
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    session.add(
        TenantModel(
            id=tenant_id,
            name="Empresa Desativada",
            status="ACTIVE",
            is_active=False,
        )
    )

    session.flush()

    response = client.get(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
    )

    assert response.status_code == 403

    assert (
        response.json()["error"]["code"]
        == "tenant.unavailable"
    )


def test_rejects_suspended_tenant(
    client: TestClient,
    session: Session,
) -> None:
    tenant_id = uuid.uuid4()

    session.add(
        TenantModel(
            id=tenant_id,
            name="Empresa Suspensa",
            status="SUSPENDED",
            is_active=True,
        )
    )

    session.flush()

    response = client.get(
        "/api/v1/customers",
        headers=tenant_headers(
            tenant_id
        ),
    )

    assert response.status_code == 403

    assert (
        response.json()["error"]["code"]
        == "tenant.unavailable"
    )


def test_rejects_null_tenant_uuid(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/v1/customers",
        headers={
            "X-Tenant-ID": (
                "00000000-0000-0000-0000-000000000000"
            ),
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "validation.error"
    )
