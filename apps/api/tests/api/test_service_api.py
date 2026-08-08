"""HTTP tests for service application routes."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, cast
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
    ServicePermissions,
)

pytestmark = pytest.mark.api


SERVICE_PERMISSION_CODES = (
    ServicePermissions.READ,
    ServicePermissions.CREATE,
    ServicePermissions.UPDATE,
    ServicePermissions.DEACTIVATE,
    ServicePermissions.REACTIVATE,
)


@pytest.fixture
def service_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide a client authorized for every service operation."""

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
        permission_codes=SERVICE_PERMISSION_CODES,
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
def unauthorized_service_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide authentication without service permissions."""

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
    """Assert the standardized permission-required response."""

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


def create_service(
    client: TestClient,
    tenant_id: uuid.UUID,
    *,
    code: str,
    name: str,
    category: str = "Corte",
    unit: str = "H",
    execution_mode: str = "INTERNAL",
    estimated_duration_minutes: int | None = 30,
) -> dict[str, Any]:
    """Create one service through the public API."""

    payload: dict[str, Any] = {
        "code": code,
        "name": name,
        "category": category,
        "unit": unit,
        "execution_mode": execution_mode,
        "estimated_duration_minutes": (
            estimated_duration_minutes
        ),
    }

    response = client.post(
        "/api/v1/services",
        headers=authentication_headers(
            tenant_id
        ),
        json=payload,
    )

    assert response.status_code == 201

    return cast(
        dict[str, Any],
        response.json(),
    )


def configure_two_tenant_access(
    *,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> StubTokenVerifier:
    """Configure one user with service access to two tenants."""

    auth_user_id = uuid.uuid4()

    user = create_test_user(
        session,
        auth_user_id=auth_user_id,
    )

    tenant_membership = create_active_membership(
        session,
        tenant_id=tenant_id,
        user=user,
    )

    other_membership = create_active_membership(
        session,
        tenant_id=other_tenant_id,
        user=user,
    )

    grant_permissions(
        session,
        tenant_id=tenant_id,
        membership=tenant_membership,
        permission_codes=SERVICE_PERMISSION_CODES,
    )

    grant_permissions(
        session,
        tenant_id=other_tenant_id,
        membership=other_membership,
        permission_codes=SERVICE_PERMISSION_CODES,
    )

    return StubTokenVerifier(
        VerifiedToken(
            auth_user_id=auth_user_id,
            role="authenticated",
            email=user.email,
        )
    )


def test_create_service_normalizes_payload(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = service_client.post(
        "/api/v1/services",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " serv-001 ",
            "name": " Corte de MDF ",
            "category": " Corte ",
            "unit": " h ",
            "execution_mode": "INTERNAL",
            "estimated_duration_minutes": 45,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["tenant_id"] == str(
        tenant_id
    )
    assert body["code"] == "SERV-001"
    assert body["name"] == "Corte de MDF"
    assert body["category"] == "Corte"
    assert body["unit"] == "H"
    assert body["execution_mode"] == "INTERNAL"
    assert body["estimated_duration_minutes"] == 45
    assert body["is_active"] is True
    assert body["id"] is not None
    assert body["created_at"] is not None
    assert body["updated_at"] is not None


def test_create_service_without_duration(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = service_client.post(
        "/api/v1/services",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "SERV-001",
            "name": "Instalação",
            "category": "Instalação",
            "unit": "UN",
            "execution_mode": "BOTH",
        },
    )

    assert response.status_code == 201
    assert response.json()["estimated_duration_minutes"] is None


def test_create_rejects_duplicate_code(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Serviço A",
    )

    response = service_client.post(
        "/api/v1/services",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "serv-001",
            "name": "Serviço B",
            "category": "Corte",
            "unit": "UN",
            "execution_mode": "INTERNAL",
        },
    )

    assert response.status_code == 409

    body = response.json()

    assert body["error"]["code"] == "resource.conflict"
    assert body["error"]["details"]["field"] == "code"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        (
            "estimated_duration_minutes",
            0,
        ),
        (
            "estimated_duration_minutes",
            -1,
        ),
        (
            "execution_mode",
            "INVALID",
        ),
    ],
)
def test_create_rejects_invalid_payload(
    service_client: TestClient,
    tenant_id: uuid.UUID,
    field: str,
    value: object,
) -> None:
    payload: dict[str, object] = {
        "code": "SERV-001",
        "name": "Serviço",
        "category": "Categoria",
        "unit": "UN",
        "execution_mode": "INTERNAL",
    }

    payload[field] = value

    response = service_client.post(
        "/api/v1/services",
        headers=authentication_headers(
            tenant_id
        ),
        json=payload,
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "request.validation_error"
    )


def test_create_rejects_extra_field(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = service_client.post(
        "/api/v1/services",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "SERV-001",
            "name": "Serviço",
            "category": "Categoria",
            "unit": "UN",
            "execution_mode": "INTERNAL",
            "tenant_id": str(
                tenant_id
            ),
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "request.validation_error"
    )


def test_get_service(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    service = create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Corte de MDF",
    )

    response = service_client.get(
        f"/api/v1/services/{service['id']}",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == service["id"]
    assert body["code"] == "SERV-001"
    assert body["name"] == "Corte de MDF"


def test_get_unknown_service_returns_not_found(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = service_client.get(
        f"/api/v1/services/{uuid.uuid4()}",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "resource.not_found"


def test_service_get_is_tenant_scoped(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    verifier = configure_two_tenant_access(
        session=session,
        tenant_id=tenant_id,
        other_tenant_id=other_tenant_id,
    )

    with override_token_verifier(
        client,
        verifier,
    ):
        service = create_service(
            client,
            tenant_id,
            code="SERV-A",
            name="Tenant A",
        )

        response = client.get(
            f"/api/v1/services/{service['id']}",
            headers=authentication_headers(
                other_tenant_id
            ),
        )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "resource.not_found"


def test_list_services_returns_only_authenticated_tenant(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    verifier = configure_two_tenant_access(
        session=session,
        tenant_id=tenant_id,
        other_tenant_id=other_tenant_id,
    )

    with override_token_verifier(
        client,
        verifier,
    ):
        create_service(
            client,
            tenant_id,
            code="SERV-A",
            name="Serviço A",
        )

        create_service(
            client,
            other_tenant_id,
            code="SERV-B",
            name="Serviço B",
        )

        response = client.get(
            "/api/v1/services",
            headers=authentication_headers(
                tenant_id
            ),
        )

    assert response.status_code == 200

    assert [
        item["name"]
        for item in response.json()
    ] == [
        "Serviço A"
    ]


@pytest.mark.parametrize(
    "search",
    [
        "SERV-001",
        "MDF",
        "Corte",
        "H",
    ],
)
def test_list_services_searches_supported_fields(
    service_client: TestClient,
    tenant_id: uuid.UUID,
    search: str,
) -> None:
    create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Corte de MDF",
        category="Corte",
        unit="H",
    )

    create_service(
        service_client,
        tenant_id,
        code="SERV-002",
        name="Instalação",
        category="Instalação",
        unit="UN",
    )

    response = service_client.get(
        "/api/v1/services",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "search": search,
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["code"] == "SERV-001"


def test_list_filters_category(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Corte",
        category="Corte",
    )

    create_service(
        service_client,
        tenant_id,
        code="SERV-002",
        name="Montagem",
        category="Montagem",
    )

    response = service_client.get(
        "/api/v1/services",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "category": "Corte",
        },
    )

    assert response.status_code == 200

    assert [
        item["code"]
        for item in response.json()
    ] == [
        "SERV-001"
    ]


def test_list_filters_execution_mode(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Corte",
        execution_mode="INTERNAL",
    )

    create_service(
        service_client,
        tenant_id,
        code="SERV-002",
        name="Pintura",
        execution_mode="EXTERNAL",
    )

    create_service(
        service_client,
        tenant_id,
        code="SERV-003",
        name="Instalação",
        execution_mode="BOTH",
    )

    response = service_client.get(
        "/api/v1/services",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "execution_mode": "EXTERNAL",
        },
    )

    assert response.status_code == 200

    assert [
        item["code"]
        for item in response.json()
    ] == [
        "SERV-002"
    ]


def test_list_rejects_invalid_execution_mode(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = service_client.get(
        "/api/v1/services",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "execution_mode": "INVALID",
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "request.validation_error"
    )


def test_list_paginates(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Alfa",
    )

    create_service(
        service_client,
        tenant_id,
        code="SERV-002",
        name="Beta",
    )

    create_service(
        service_client,
        tenant_id,
        code="SERV-003",
        name="Gama",
    )

    response = service_client.get(
        "/api/v1/services",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "limit": 1,
            "offset": 1,
        },
    )

    assert response.status_code == 200

    assert [
        item["name"]
        for item in response.json()
    ] == [
        "Beta"
    ]


@pytest.mark.parametrize(
    ("parameter", "value"),
    [
        (
            "limit",
            0,
        ),
        (
            "limit",
            201,
        ),
        (
            "offset",
            -1,
        ),
    ],
)
def test_list_rejects_invalid_pagination(
    service_client: TestClient,
    tenant_id: uuid.UUID,
    parameter: str,
    value: int,
) -> None:
    response = service_client.get(
        "/api/v1/services",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            parameter: value,
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "request.validation_error"
    )


def test_list_excludes_inactive_by_default(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    active_service = create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Ativo",
    )

    inactive_service = create_service(
        service_client,
        tenant_id,
        code="SERV-002",
        name="Inativo",
    )

    response = service_client.post(
        (
            "/api/v1/services/"
            f"{inactive_service['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    response = service_client.get(
        "/api/v1/services",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    ids = {
        item["id"]
        for item in response.json()
    }

    assert active_service["id"] in ids
    assert inactive_service["id"] not in ids


def test_list_can_include_inactive(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    service = create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Inativo",
    )

    response = service_client.post(
        (
            "/api/v1/services/"
            f"{service['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    response = service_client.get(
        "/api/v1/services",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "include_inactive": True,
        },
    )

    assert response.status_code == 200

    assert service["id"] in {
        item["id"]
        for item in response.json()
    }


def test_update_service(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    service = create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Corte Antigo",
        category="Corte",
        unit="H",
        execution_mode="INTERNAL",
        estimated_duration_minutes=30,
    )

    response = service_client.patch(
        f"/api/v1/services/{service['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " serv-002 ",
            "name": " Montagem ",
            "category": " Produção ",
            "unit": " un ",
            "execution_mode": "BOTH",
            "estimated_duration_minutes": 60,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["code"] == "SERV-002"
    assert body["name"] == "Montagem"
    assert body["category"] == "Produção"
    assert body["unit"] == "UN"
    assert body["execution_mode"] == "BOTH"
    assert body["estimated_duration_minutes"] == 60


def test_update_preserves_unspecified_fields(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    service = create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Serviço",
        category="Corte",
        unit="H",
        execution_mode="INTERNAL",
        estimated_duration_minutes=45,
    )

    response = service_client.patch(
        f"/api/v1/services/{service['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "name": "Serviço Atualizado",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "Serviço Atualizado"
    assert body["code"] == "SERV-001"
    assert body["category"] == "Corte"
    assert body["unit"] == "H"
    assert body["execution_mode"] == "INTERNAL"
    assert body["estimated_duration_minutes"] == 45


def test_update_can_clear_duration(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    service = create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Serviço",
        estimated_duration_minutes=45,
    )

    response = service_client.patch(
        f"/api/v1/services/{service['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "estimated_duration_minutes": None,
        },
    )

    assert response.status_code == 200
    assert response.json()["estimated_duration_minutes"] is None


def test_update_rejects_empty_payload(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    service = create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Serviço",
    )

    response = service_client.patch(
        f"/api/v1/services/{service['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation.error"


@pytest.mark.parametrize(
    "field",
    [
        "code",
        "name",
        "category",
        "unit",
        "execution_mode",
    ],
)
def test_update_rejects_null_required_fields(
    service_client: TestClient,
    tenant_id: uuid.UUID,
    field: str,
) -> None:
    service = create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Serviço",
    )

    response = service_client.patch(
        f"/api/v1/services/{service['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            field: None,
        },
    )

    assert response.status_code == 422


def test_update_rejects_duplicate_code(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Primeiro",
    )

    second = create_service(
        service_client,
        tenant_id,
        code="SERV-002",
        name="Segundo",
    )

    response = service_client.patch(
        f"/api/v1/services/{second['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "serv-001",
        },
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "resource.conflict"


def test_update_is_tenant_scoped(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    verifier = configure_two_tenant_access(
        session=session,
        tenant_id=tenant_id,
        other_tenant_id=other_tenant_id,
    )

    with override_token_verifier(
        client,
        verifier,
    ):
        service = create_service(
            client,
            tenant_id,
            code="SERV-A",
            name="Tenant A",
        )

        response = client.patch(
            f"/api/v1/services/{service['id']}",
            headers=authentication_headers(
                other_tenant_id
            ),
            json={
                "name": "Tentativa indevida",
            },
        )

    assert response.status_code == 404


def test_deactivate_service(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    service = create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Serviço",
    )

    response = service_client.post(
        (
            "/api/v1/services/"
            f"{service['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_deactivate_is_idempotent(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    service = create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Serviço",
    )

    first_response = service_client.post(
        (
            "/api/v1/services/"
            f"{service['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert first_response.status_code == 200

    second_response = service_client.post(
        (
            "/api/v1/services/"
            f"{service['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert second_response.status_code == 200
    assert second_response.json()["is_active"] is False


def test_reactivate_service(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    service = create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Serviço",
    )

    deactivate_response = service_client.post(
        (
            "/api/v1/services/"
            f"{service['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert deactivate_response.status_code == 200

    response = service_client.post(
        (
            "/api/v1/services/"
            f"{service['id']}/reactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is True


def test_reactivate_is_idempotent(
    service_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    service = create_service(
        service_client,
        tenant_id,
        code="SERV-001",
        name="Serviço",
    )

    response = service_client.post(
        (
            "/api/v1/services/"
            f"{service['id']}/reactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is True


@pytest.mark.parametrize(
    ("method", "path", "permission"),
    [
        (
            "get",
            "/api/v1/services",
            ServicePermissions.READ,
        ),
        (
            "get",
            "/api/v1/services/{service_id}",
            ServicePermissions.READ,
        ),
        (
            "post",
            "/api/v1/services",
            ServicePermissions.CREATE,
        ),
        (
            "patch",
            "/api/v1/services/{service_id}",
            ServicePermissions.UPDATE,
        ),
        (
            "post",
            "/api/v1/services/{service_id}/deactivate",
            ServicePermissions.DEACTIVATE,
        ),
        (
            "post",
            "/api/v1/services/{service_id}/reactivate",
            ServicePermissions.REACTIVATE,
        ),
    ],
)
def test_service_routes_require_permission(
    unauthorized_service_client: TestClient,
    tenant_id: uuid.UUID,
    method: str,
    path: str,
    permission: str,
) -> None:
    service_id = uuid.uuid4()

    resolved_path = path.format(
        service_id=service_id
    )

    headers = authentication_headers(
        tenant_id
    )

    if method == "get":
        response = unauthorized_service_client.get(
            resolved_path,
            headers=headers,
        )
    elif method == "patch":
        response = unauthorized_service_client.patch(
            resolved_path,
            headers=headers,
            json={
                "name": "Atualizado",
            },
        )
    else:
        payload = None

        if resolved_path == "/api/v1/services":
            payload = {
                "code": "SERV-001",
                "name": "Serviço",
                "category": "Categoria",
                "unit": "UN",
                "execution_mode": "INTERNAL",
            }

        response = unauthorized_service_client.post(
            resolved_path,
            headers=headers,
            json=payload,
        )

    assert_permission_denied(
        response,
        permission,
    )


def test_service_routes_are_registered(
    client: TestClient,
) -> None:
    """Ensure every public service operation is in OpenAPI."""

    schema = client.app.openapi()
    paths = schema["paths"]

    expected = {
        "/api/v1/services": {
            "get",
            "post",
        },
        "/api/v1/services/{service_id}": {
            "get",
            "patch",
        },
        "/api/v1/services/{service_id}/deactivate": {
            "post",
        },
        "/api/v1/services/{service_id}/reactivate": {
            "post",
        },
    }

    for path, expected_methods in expected.items():
        assert path in paths

        actual_methods = {
            method.lower()
            for method in paths[path]
        }

        assert expected_methods.issubset(
            actual_methods
        )
