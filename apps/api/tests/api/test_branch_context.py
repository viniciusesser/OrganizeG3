"""HTTP tests for optional branch request context."""

from __future__ import annotations

import uuid

from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session
from tests.helpers.authentication import (
    authentication_headers,
)

from organizeg3_api.infrastructure.persistence.models import (
    BranchModel,
)

pytestmark = pytest.mark.api


@pytest.fixture(autouse=True)
def authorize_customer_requests(
    authenticated_customer_client: TestClient,
) -> None:
    """Authorize customer requests for this module."""


def create_branch(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    branch_id: uuid.UUID,
    code: str,
    is_active: bool = True,
) -> BranchModel:
    """Create one branch for HTTP context tests."""

    branch = BranchModel(
        id=branch_id,
        tenant_id=tenant_id,
        code=code,
        name=f"Filial {code}",
        is_active=is_active,
    )

    session.add(branch)
    session.flush()

    return branch


def branch_headers(
    tenant_id: uuid.UUID,
    branch_id: uuid.UUID | str | None = None,
) -> dict[str, str]:
    """Build authenticated headers with optional branch context."""

    headers = authentication_headers(
        tenant_id
    )

    if branch_id is not None:
        headers["X-Branch-ID"] = str(
            branch_id
        )

    return headers


def test_allows_request_without_branch(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = client.get(
        "/api/v1/customers",
        headers=branch_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200


def test_accepts_active_branch_from_current_tenant(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    branch_id = uuid.uuid4()

    create_branch(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
        code="MATRIZ",
    )

    response = client.get(
        "/api/v1/customers",
        headers=branch_headers(
            tenant_id,
            branch_id,
        ),
    )

    assert response.status_code == 200


def test_rejects_unknown_branch(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = client.get(
        "/api/v1/customers",
        headers=branch_headers(
            tenant_id,
            uuid.uuid4(),
        ),
    )

    assert response.status_code == 403

    assert (
        response.json()["error"]["code"]
        == "authorization.branch_unavailable"
    )

    assert (
        response.json()["error"]["details"]["reason"]
        == "branch_unavailable"
    )


def test_rejects_inactive_branch(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    branch_id = uuid.uuid4()

    create_branch(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
        code="INATIVA",
        is_active=False,
    )

    response = client.get(
        "/api/v1/customers",
        headers=branch_headers(
            tenant_id,
            branch_id,
        ),
    )

    assert response.status_code == 403

    assert (
        response.json()["error"]["code"]
        == "authorization.branch_unavailable"
    )


def test_rejects_branch_from_other_tenant(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    branch_id = uuid.uuid4()

    create_branch(
        session,
        tenant_id=other_tenant_id,
        branch_id=branch_id,
        code="OUTRO",
    )

    response = client.get(
        "/api/v1/customers",
        headers=branch_headers(
            tenant_id,
            branch_id,
        ),
    )

    assert response.status_code == 403

    assert (
        response.json()["error"]["code"]
        == "authorization.branch_unavailable"
    )


def test_rejects_invalid_branch_header(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = client.get(
        "/api/v1/customers",
        headers=branch_headers(
            tenant_id,
            "invalid",
        ),
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "validation.error"
    )


def test_rejects_null_branch_uuid(
    client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = client.get(
        "/api/v1/customers",
        headers=branch_headers(
            tenant_id,
            uuid.UUID(int=0),
        ),
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "validation.error"
    )
