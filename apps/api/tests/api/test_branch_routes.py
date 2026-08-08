"""HTTP tests for branch routes."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, cast
import uuid

from fastapi import FastAPI
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

from organizeg3_api.domain.branch.entity import (
    Branch,
)
from organizeg3_api.domain.identity.authentication import (
    VerifiedToken,
)
from organizeg3_api.domain.identity.permissions import (
    BranchPermissions,
)
from organizeg3_api.infrastructure.persistence.repositories.branch_repository import (
    SQLAlchemyBranchRepository,
)

pytestmark = pytest.mark.api


BRANCH_PERMISSION_CODES = (
    BranchPermissions.READ,
    BranchPermissions.CREATE,
    BranchPermissions.UPDATE,
    BranchPermissions.DEACTIVATE,
    BranchPermissions.REACTIVATE,
)


@pytest.fixture
def authenticated_branch_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide an authenticated client with all branch permissions."""

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
        permission_codes=BRANCH_PERMISSION_CODES,
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


@pytest.fixture
def unauthorized_branch_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide an active membership without branch permissions."""

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
    response: Any,
    permission_code: str,
) -> None:
    """Assert the standardized permission error contract."""

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


def create_branch_through_api(
    client: TestClient,
    tenant_id: uuid.UUID,
    *,
    code: str = "FILIAL-01",
    name: str = "Filial 01",
    is_headquarters: bool = False,
) -> dict[str, Any]:
    """Create a branch and return its response payload."""

    response = client.post(
        "/api/v1/branches",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": code,
            "name": name,
            "is_headquarters": is_headquarters,
        },
    )

    assert response.status_code == 201

    return cast(
        dict[str, Any],
        response.json(),
    )


def test_creates_branch(
    authenticated_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = authenticated_branch_client.post(
        "/api/v1/branches",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " matriz ",
            "name": " Matriz ",
            "legal_name": " Empresa Matriz LTDA ",
            "document_number": "12.345.678/0001-90",
            "email": " MATRIZ@EXAMPLE.COM ",
            "phone": "(18) 3222-1234",
            "city": " Rosana ",
            "state": "sp",
            "postal_code": "19273-000",
            "is_headquarters": True,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["tenant_id"] == str(
        tenant_id
    )
    assert body["code"] == "MATRIZ"
    assert body["name"] == "Matriz"
    assert (
        body["legal_name"]
        == "Empresa Matriz LTDA"
    )
    assert (
        body["document_number"]
        == "12345678000190"
    )
    assert (
        body["email"]
        == "matriz@example.com"
    )
    assert body["phone"] == "1832221234"
    assert body["city"] == "Rosana"
    assert body["state"] == "SP"
    assert body["postal_code"] == "19273000"
    assert body["is_headquarters"] is True
    assert body["is_active"] is True


def test_lists_branches(
    authenticated_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_branch_through_api(
        authenticated_branch_client,
        tenant_id,
        code="FILIAL-01",
        name="Filial 01",
    )

    create_branch_through_api(
        authenticated_branch_client,
        tenant_id,
        code="FILIAL-02",
        name="Filial 02",
    )

    response = authenticated_branch_client.get(
        "/api/v1/branches",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 2
    assert {
        branch["code"]
        for branch in body
    } == {
        "FILIAL-01",
        "FILIAL-02",
    }


def test_lists_branches_with_search_and_pagination(
    authenticated_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    for index in range(3):
        create_branch_through_api(
            authenticated_branch_client,
            tenant_id,
            code=f"FILIAL-{index}",
            name=f"Unidade {index}",
        )

    response = authenticated_branch_client.get(
        "/api/v1/branches",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "search": "unidade",
            "limit": 1,
            "offset": 1,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert body[0]["code"] == "FILIAL-1"


def test_filters_headquarters(
    authenticated_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_branch_through_api(
        authenticated_branch_client,
        tenant_id,
        code="MATRIZ",
        name="Matriz",
        is_headquarters=True,
    )

    create_branch_through_api(
        authenticated_branch_client,
        tenant_id,
        code="FILIAL",
        name="Filial",
    )

    response = authenticated_branch_client.get(
        "/api/v1/branches",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "is_headquarters": "true",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert body[0]["code"] == "MATRIZ"


def test_gets_branch(
    authenticated_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    created = create_branch_through_api(
        authenticated_branch_client,
        tenant_id,
    )

    response = authenticated_branch_client.get(
        f"/api/v1/branches/{created['id']}",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert (
        response.json()["id"]
        == created["id"]
    )


def test_updates_branch(
    authenticated_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    created = create_branch_through_api(
        authenticated_branch_client,
        tenant_id,
    )

    response = authenticated_branch_client.patch(
        f"/api/v1/branches/{created['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " filial-nova ",
            "name": " Filial Nova ",
            "email": " NOVA@EXAMPLE.COM ",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["code"] == "FILIAL-NOVA"
    assert body["name"] == "Filial Nova"
    assert body["email"] == "nova@example.com"


def test_deactivates_and_reactivates_branch(
    authenticated_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    created = create_branch_through_api(
        authenticated_branch_client,
        tenant_id,
    )

    deactivate_response = (
        authenticated_branch_client.post(
            (
                f"/api/v1/branches/"
                f"{created['id']}/deactivate"
            ),
            headers=authentication_headers(
                tenant_id
            ),
        )
    )

    assert deactivate_response.status_code == 200
    assert (
        deactivate_response.json()["is_active"]
        is False
    )

    list_response = authenticated_branch_client.get(
        "/api/v1/branches",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert list_response.status_code == 200
    assert list_response.json() == []

    inactive_response = (
        authenticated_branch_client.get(
            "/api/v1/branches",
            headers=authentication_headers(
                tenant_id
            ),
            params={
                "include_inactive": "true",
            },
        )
    )

    assert inactive_response.status_code == 200
    assert len(inactive_response.json()) == 1

    reactivate_response = (
        authenticated_branch_client.post(
            (
                f"/api/v1/branches/"
                f"{created['id']}/reactivate"
            ),
            headers=authentication_headers(
                tenant_id
            ),
        )
    )

    assert reactivate_response.status_code == 200
    assert (
        reactivate_response.json()["is_active"]
        is True
    )


def test_rejects_duplicate_branch_code(
    authenticated_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_branch_through_api(
        authenticated_branch_client,
        tenant_id,
        code="FILIAL",
    )

    response = authenticated_branch_client.post(
        "/api/v1/branches",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " filial ",
            "name": "Outra Filial",
        },
    )

    assert response.status_code == 409
    assert (
        response.json()["error"]["code"]
        == "resource.conflict"
    )


def test_rejects_second_headquarters(
    authenticated_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_branch_through_api(
        authenticated_branch_client,
        tenant_id,
        code="MATRIZ",
        name="Matriz",
        is_headquarters=True,
    )

    response = authenticated_branch_client.post(
        "/api/v1/branches",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "MATRIZ-02",
            "name": "Outra Matriz",
            "is_headquarters": True,
        },
    )

    assert response.status_code == 409
    assert (
        response.json()["error"]["code"]
        == "resource.conflict"
    )


def test_returns_not_found_for_unknown_branch(
    authenticated_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = authenticated_branch_client.get(
        f"/api/v1/branches/{uuid.uuid4()}",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 404
    assert (
        response.json()["error"]["code"]
        == "resource.not_found"
    )


def test_rejects_empty_update(
    authenticated_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    created = create_branch_through_api(
        authenticated_branch_client,
        tenant_id,
    )

    response = authenticated_branch_client.patch(
        f"/api/v1/branches/{created['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={},
    )

    assert response.status_code == 422
    assert (
        response.json()["error"]["code"]
        == "validation.error"
    )


def test_rejects_invalid_branch_payload(
    authenticated_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = authenticated_branch_client.post(
        "/api/v1/branches",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "FILIAL",
            "name": "Filial",
            "email": "email-invalido",
        },
    )

    assert response.status_code == 422
    assert (
        response.json()["error"]["code"]
        == "request.validation_error"
    )


def test_branch_is_tenant_isolated(
    authenticated_branch_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    repository = SQLAlchemyBranchRepository(
        session
    )

    other_branch = repository.add(
        Branch.create(
            tenant_id=other_tenant_id,
            code="OUTRO-TENANT",
            name="Outro Tenant",
        )
    )

    assert other_branch.id is not None

    response = authenticated_branch_client.get(
        f"/api/v1/branches/{other_branch.id}",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 404


def test_rejects_read_without_permission(
    unauthorized_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_branch_client.get(
        "/api/v1/branches",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert_permission_denied(
        response,
        BranchPermissions.READ,
    )


def test_rejects_create_without_permission(
    unauthorized_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_branch_client.post(
        "/api/v1/branches",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "FILIAL",
            "name": "Filial",
        },
    )

    assert_permission_denied(
        response,
        BranchPermissions.CREATE,
    )


def test_rejects_update_without_permission(
    unauthorized_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_branch_client.patch(
        f"/api/v1/branches/{uuid.uuid4()}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "name": "Filial",
        },
    )

    assert_permission_denied(
        response,
        BranchPermissions.UPDATE,
    )


def test_rejects_deactivate_without_permission(
    unauthorized_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_branch_client.post(
        (
            f"/api/v1/branches/"
            f"{uuid.uuid4()}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert_permission_denied(
        response,
        BranchPermissions.DEACTIVATE,
    )


def test_rejects_reactivate_without_permission(
    unauthorized_branch_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_branch_client.post(
        (
            f"/api/v1/branches/"
            f"{uuid.uuid4()}/reactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert_permission_denied(
        response,
        BranchPermissions.REACTIVATE,
    )


@pytest.mark.parametrize(
    "permission_code",
    [
        BranchPermissions.READ,
        BranchPermissions.CREATE,
        BranchPermissions.UPDATE,
        BranchPermissions.DEACTIVATE,
        BranchPermissions.REACTIVATE,
    ],
)
def test_granted_branch_permission_is_resolved(
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


def test_openapi_exposes_branch_contract(
    client: TestClient,
) -> None:
    application = cast(
        FastAPI,
        client.app,
    )

    schema = application.openapi()

    paths = schema["paths"]

    assert "/api/v1/branches" in paths
    assert "/api/v1/branches/{branch_id}" in paths

    assert (
        "/api/v1/branches/"
        "{branch_id}/deactivate"
    ) in paths

    assert (
        "/api/v1/branches/"
        "{branch_id}/reactivate"
    ) in paths

    assert set(
        paths["/api/v1/branches"]
    ) == {
        "get",
        "post",
    }

    assert set(
        paths[
            "/api/v1/branches/{branch_id}"
        ]
    ) == {
        "get",
        "patch",
    }

    assert set(
        paths[
            (
                "/api/v1/branches/"
                "{branch_id}/deactivate"
            )
        ]
    ) == {
        "post",
    }

    assert set(
        paths[
            (
                "/api/v1/branches/"
                "{branch_id}/reactivate"
            )
        ]
    ) == {
        "post",
    }
