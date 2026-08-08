"""HTTP tests for brand application routes."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime
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
    BrandPermissions,
)

pytestmark = pytest.mark.api


BRAND_PERMISSION_CODES = (
    BrandPermissions.READ,
    BrandPermissions.CREATE,
    BrandPermissions.UPDATE,
    BrandPermissions.DEACTIVATE,
    BrandPermissions.REACTIVATE,
)


def parse_api_datetime(
    value: str,
) -> datetime:
    """Normalize an API datetime to an aware UTC datetime."""

    parsed = datetime.fromisoformat(
        value.replace(
            "Z",
            "+00:00",
        )
    )

    if parsed.tzinfo is None:
        return parsed.replace(
            tzinfo=UTC
        )

    return parsed.astimezone(
        UTC
    )


@pytest.fixture
def brand_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide a client authorized for every brand operation."""

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
        permission_codes=BRAND_PERMISSION_CODES,
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
def unauthorized_brand_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide authentication without brand permissions."""

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


def create_brand(
    client: TestClient,
    tenant_id: uuid.UUID,
    *,
    code: str,
    name: str,
) -> dict[str, Any]:
    """Create one brand through the public API."""

    response = client.post(
        "/api/v1/brands",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": code,
            "name": name,
        },
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
    """Configure one user with brand access to two tenants."""

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
        permission_codes=BRAND_PERMISSION_CODES,
    )

    grant_permissions(
        session,
        tenant_id=other_tenant_id,
        membership=other_membership,
        permission_codes=BRAND_PERMISSION_CODES,
    )

    return StubTokenVerifier(
        VerifiedToken(
            auth_user_id=auth_user_id,
            role="authenticated",
            email=user.email,
        )
    )


def test_create_brand_normalizes_payload(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = brand_client.post(
        "/api/v1/brands",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " marca-001 ",
            "name": " Duratex ",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["tenant_id"] == str(
        tenant_id
    )
    assert body["code"] == "MARCA-001"
    assert body["name"] == "Duratex"
    assert body["is_active"] is True
    assert body["id"] is not None
    assert body["created_at"] is not None
    assert body["updated_at"] is not None


def test_create_rejects_duplicate_code(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    response = brand_client.post(
        "/api/v1/brands",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "marca-001",
            "name": "Arauco",
        },
    )

    assert response.status_code == 409

    body = response.json()

    assert body["error"]["code"] == "resource.conflict"
    assert body["error"]["details"]["field"] == "code"


def test_create_rejects_duplicate_name(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    response = brand_client.post(
        "/api/v1/brands",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "MARCA-002",
            "name": "Duratex",
        },
    )

    assert response.status_code == 409
    assert (
        response.json()["error"]["details"]["field"]
        == "name"
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        (
            "code",
            "",
        ),
        (
            "name",
            "",
        ),
    ],
)
def test_create_rejects_invalid_payload(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
    field: str,
    value: object,
) -> None:
    payload: dict[str, object] = {
        "code": "MARCA-001",
        "name": "Duratex",
    }

    payload[field] = value

    response = brand_client.post(
        "/api/v1/brands",
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
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = brand_client.post(
        "/api/v1/brands",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "MARCA-001",
            "name": "Duratex",
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


def test_get_brand(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    brand = create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    response = brand_client.get(
        f"/api/v1/brands/{brand['id']}",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["id"] == brand["id"]
    assert response.json()["code"] == "MARCA-001"
    assert response.json()["name"] == "Duratex"


def test_get_unknown_brand_returns_not_found(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = brand_client.get(
        f"/api/v1/brands/{uuid.uuid4()}",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 404
    assert (
        response.json()["error"]["code"]
        == "resource.not_found"
    )


def test_brand_get_is_tenant_scoped(
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
        brand = create_brand(
            client,
            tenant_id,
            code="MARCA-A",
            name="Tenant A",
        )

        response = client.get(
            f"/api/v1/brands/{brand['id']}",
            headers=authentication_headers(
                other_tenant_id
            ),
        )

    assert response.status_code == 404
    assert (
        response.json()["error"]["code"]
        == "resource.not_found"
    )


def test_list_brands_returns_only_authenticated_tenant(
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
        create_brand(
            client,
            tenant_id,
            code="MARCA-A",
            name="Arauco",
        )

        create_brand(
            client,
            other_tenant_id,
            code="MARCA-B",
            name="Duratex",
        )

        response = client.get(
            "/api/v1/brands",
            headers=authentication_headers(
                tenant_id
            ),
        )

    assert response.status_code == 200

    assert [
        item["name"]
        for item in response.json()
    ] == [
        "Arauco"
    ]


@pytest.mark.parametrize(
    "search",
    [
        "MARCA-001",
        "marca-001",
        "Duratex",
        "duratex",
    ],
)
def test_list_brands_searches_code_or_name(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
    search: str,
) -> None:
    create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    create_brand(
        brand_client,
        tenant_id,
        code="MARCA-002",
        name="Arauco",
    )

    response = brand_client.get(
        "/api/v1/brands",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "search": search,
        },
    )

    assert response.status_code == 200
    assert len(
        response.json()
    ) == 1
    assert response.json()[0]["code"] == "MARCA-001"


def test_list_paginates(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Arauco",
    )

    create_brand(
        brand_client,
        tenant_id,
        code="MARCA-002",
        name="Duratex",
    )

    create_brand(
        brand_client,
        tenant_id,
        code="MARCA-003",
        name="Guararapes",
    )

    response = brand_client.get(
        "/api/v1/brands",
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
        "Duratex"
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
    brand_client: TestClient,
    tenant_id: uuid.UUID,
    parameter: str,
    value: int,
) -> None:
    response = brand_client.get(
        "/api/v1/brands",
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
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    active = create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Arauco",
    )

    inactive = create_brand(
        brand_client,
        tenant_id,
        code="MARCA-002",
        name="Duratex",
    )

    response = brand_client.post(
        (
            "/api/v1/brands/"
            f"{inactive['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    response = brand_client.get(
        "/api/v1/brands",
        headers=authentication_headers(
            tenant_id
        ),
    )

    ids = {
        item["id"]
        for item in response.json()
    }

    assert active["id"] in ids
    assert inactive["id"] not in ids


def test_list_can_include_inactive(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    brand = create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    brand_client.post(
        (
            "/api/v1/brands/"
            f"{brand['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    response = brand_client.get(
        "/api/v1/brands",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "include_inactive": True,
        },
    )

    assert response.status_code == 200
    assert brand["id"] in {
        item["id"]
        for item in response.json()
    }


def test_update_brand(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    brand = create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    response = brand_client.patch(
        f"/api/v1/brands/{brand['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " marca-002 ",
            "name": " Arauco ",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["code"] == "MARCA-002"
    assert body["name"] == "Arauco"


def test_update_preserves_unspecified_fields(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    brand = create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    response = brand_client.patch(
        f"/api/v1/brands/{brand['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "name": "Arauco",
        },
    )

    assert response.status_code == 200
    assert response.json()["code"] == "MARCA-001"
    assert response.json()["name"] == "Arauco"


def test_update_rejects_empty_payload(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    brand = create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    response = brand_client.patch(
        f"/api/v1/brands/{brand['id']}",
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


@pytest.mark.parametrize(
    "field_name",
    [
        "code",
        "name",
    ],
)
def test_update_rejects_null_required_field(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
    field_name: str,
) -> None:
    brand = create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    response = brand_client.patch(
        f"/api/v1/brands/{brand['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            field_name: None,
        },
    )

    assert response.status_code == 422
    assert (
        response.json()["error"]["code"]
        == "validation.error"
    )
    assert (
        response.json()["error"]["details"]["field"]
        == field_name
    )


def test_update_rejects_duplicate_code(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    second = create_brand(
        brand_client,
        tenant_id,
        code="MARCA-002",
        name="Arauco",
    )

    response = brand_client.patch(
        f"/api/v1/brands/{second['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "marca-001",
        },
    )

    assert response.status_code == 409
    assert (
        response.json()["error"]["details"]["field"]
        == "code"
    )


def test_update_rejects_duplicate_name(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    second = create_brand(
        brand_client,
        tenant_id,
        code="MARCA-002",
        name="Arauco",
    )

    response = brand_client.patch(
        f"/api/v1/brands/{second['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "name": "Duratex",
        },
    )

    assert response.status_code == 409
    assert (
        response.json()["error"]["details"]["field"]
        == "name"
    )


def test_deactivate_brand(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    brand = create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    response = brand_client.post(
        (
            "/api/v1/brands/"
            f"{brand['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_deactivate_is_idempotent(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    brand = create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    first = brand_client.post(
        (
            "/api/v1/brands/"
            f"{brand['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    second = brand_client.post(
        (
            "/api/v1/brands/"
            f"{brand['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json()["is_active"] is False

    assert parse_api_datetime(
        second.json()["updated_at"]
    ) == parse_api_datetime(
        first.json()["updated_at"]
    )


def test_reactivate_brand(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    brand = create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    brand_client.post(
        (
            "/api/v1/brands/"
            f"{brand['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    response = brand_client.post(
        (
            "/api/v1/brands/"
            f"{brand['id']}/reactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is True


def test_reactivate_is_idempotent(
    brand_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    brand = create_brand(
        brand_client,
        tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    original_updated_at = brand[
        "updated_at"
    ]

    response = brand_client.post(
        (
            "/api/v1/brands/"
            f"{brand['id']}/reactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is True

    assert parse_api_datetime(
        response.json()["updated_at"]
    ) == parse_api_datetime(
        original_updated_at
    )


@pytest.mark.parametrize(
    ("method", "path", "permission"),
    [
        (
            "get",
            "/api/v1/brands",
            BrandPermissions.READ,
        ),
        (
            "get",
            "/api/v1/brands/{brand_id}",
            BrandPermissions.READ,
        ),
        (
            "post",
            "/api/v1/brands",
            BrandPermissions.CREATE,
        ),
        (
            "patch",
            "/api/v1/brands/{brand_id}",
            BrandPermissions.UPDATE,
        ),
        (
            "post",
            "/api/v1/brands/{brand_id}/deactivate",
            BrandPermissions.DEACTIVATE,
        ),
        (
            "post",
            "/api/v1/brands/{brand_id}/reactivate",
            BrandPermissions.REACTIVATE,
        ),
    ],
)
def test_brand_routes_require_permission(
    unauthorized_brand_client: TestClient,
    tenant_id: uuid.UUID,
    method: str,
    path: str,
    permission: str,
) -> None:
    brand_id = uuid.uuid4()

    resolved_path = path.format(
        brand_id=brand_id
    )

    headers = authentication_headers(
        tenant_id
    )

    if method == "get":
        response = unauthorized_brand_client.get(
            resolved_path,
            headers=headers,
        )

    elif method == "patch":
        response = unauthorized_brand_client.patch(
            resolved_path,
            headers=headers,
            json={
                "name": "Atualizada",
            },
        )

    else:
        payload = None

        if resolved_path == "/api/v1/brands":
            payload = {
                "code": "MARCA-001",
                "name": "Duratex",
            }

        response = unauthorized_brand_client.post(
            resolved_path,
            headers=headers,
            json=payload,
        )

    assert_permission_denied(
        response,
        permission,
    )


def test_brand_routes_are_registered(
    client: TestClient,
) -> None:
    """Ensure every public brand operation is in OpenAPI."""

    schema = client.app.openapi()
    paths = schema["paths"]

    expected = {
        "/api/v1/brands": {
            "get",
            "post",
        },
        "/api/v1/brands/{brand_id}": {
            "get",
            "patch",
        },
        "/api/v1/brands/{brand_id}/deactivate": {
            "post",
        },
        "/api/v1/brands/{brand_id}/reactivate": {
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
