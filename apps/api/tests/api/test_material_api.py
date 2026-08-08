"""HTTP tests for material application routes."""

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

from organizeg3_api.domain.brand.entity import (
    Brand,
)
from organizeg3_api.domain.identity.authentication import (
    VerifiedToken,
)
from organizeg3_api.domain.identity.permissions import (
    MaterialPermissions,
)
from organizeg3_api.infrastructure.persistence.repositories import (
    SQLAlchemyBrandRepository,
)

pytestmark = pytest.mark.api

MATERIAL_PERMISSION_CODES = (
    MaterialPermissions.READ,
    MaterialPermissions.CREATE,
    MaterialPermissions.UPDATE,
    MaterialPermissions.DEACTIVATE,
    MaterialPermissions.REACTIVATE,
)


@pytest.fixture
def material_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide a client authorized for every material operation."""

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
        permission_codes=MATERIAL_PERMISSION_CODES,
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
def unauthorized_material_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide authentication without material permissions."""

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
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "MARCA-001",
    name: str = "Duratex",
) -> uuid.UUID:
    """Persist one brand for material API tests."""

    repository = SQLAlchemyBrandRepository(
        session
    )

    brand = repository.add(
        Brand.create(
            tenant_id=tenant_id,
            code=code,
            name=name,
        )
    )

    assert brand.id is not None

    return brand.id


def create_material(
    client: TestClient,
    tenant_id: uuid.UUID,
    *,
    code: str,
    name: str,
    category: str = "Chapas",
    unit: str = "UN",
    brand_id: uuid.UUID | None = None,
) -> dict[str, Any]:
    """Create one material through the public API."""

    payload: dict[str, Any] = {
        "code": code,
        "name": name,
        "category": category,
        "unit": unit,
    }

    if brand_id is not None:
        payload["brand_id"] = str(
            brand_id
        )

    response = client.post(
        "/api/v1/materials",
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


def test_create_material_normalizes_payload(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = material_client.post(
        "/api/v1/materials",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " mat-001 ",
            "name": " MDF Branco TX 15mm ",
            "category": " Chapas ",
            "unit": " chapa ",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["tenant_id"] == str(
        tenant_id
    )
    assert body["code"] == "MAT-001"
    assert body["name"] == "MDF Branco TX 15mm"
    assert body["category"] == "Chapas"
    assert body["unit"] == "CHAPA"
    assert body["brand_id"] is None
    assert body["is_active"] is True
    assert body["id"] is not None
    assert body["created_at"] is not None
    assert body["updated_at"] is not None


def test_create_material_with_brand(
    material_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    brand_id = create_brand(
        session,
        tenant_id=tenant_id,
    )

    response = material_client.post(
        "/api/v1/materials",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "MAT-001",
            "name": "MDF",
            "category": "Chapas",
            "unit": "UN",
            "brand_id": str(
                brand_id
            ),
        },
    )

    assert response.status_code == 201

    assert (
        response.json()["brand_id"]
        == str(brand_id)
    )


def test_create_rejects_brand_from_other_tenant(
    material_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    foreign_brand_id = create_brand(
        session,
        tenant_id=other_tenant_id,
        code="MARCA-OUTRA",
    )

    response = material_client.post(
        "/api/v1/materials",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "MAT-001",
            "name": "Material",
            "category": "Chapas",
            "unit": "UN",
            "brand_id": str(
                foreign_brand_id
            ),
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "validation.error"
    )


def test_create_rejects_unknown_brand(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = material_client.post(
        "/api/v1/materials",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "MAT-001",
            "name": "Material",
            "category": "Chapas",
            "unit": "UN",
            "brand_id": str(
                uuid.uuid4()
            ),
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "validation.error"
    )


def test_create_rejects_duplicate_code(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material A",
    )

    response = material_client.post(
        "/api/v1/materials",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " mat-001 ",
            "name": "Material B",
            "category": "Chapas",
            "unit": "UN",
        },
    )

    assert response.status_code == 409

    assert (
        response.json()["error"]["code"]
        == "resource.conflict"
    )


def test_same_code_is_allowed_in_different_tenants(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    auth_user_id = uuid.uuid4()

    user = create_test_user(
        session,
        auth_user_id=auth_user_id,
    )

    first_membership = create_active_membership(
        session,
        tenant_id=tenant_id,
        user=user,
    )

    second_membership = create_active_membership(
        session,
        tenant_id=other_tenant_id,
        user=user,
    )

    grant_permissions(
        session,
        tenant_id=tenant_id,
        membership=first_membership,
        permission_codes=MATERIAL_PERMISSION_CODES,
    )

    grant_permissions(
        session,
        tenant_id=other_tenant_id,
        membership=second_membership,
        permission_codes=MATERIAL_PERMISSION_CODES,
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
        first = create_material(
            client,
            tenant_id,
            code="MAT-001",
            name="Material Tenant A",
        )

        second = create_material(
            client,
            other_tenant_id,
            code="MAT-001",
            name="Material Tenant B",
        )

    assert first["code"] == "MAT-001"
    assert second["code"] == "MAT-001"

    assert (
        first["tenant_id"]
        != second["tenant_id"]
    )


def test_get_material(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material Consultado",
    )

    response = material_client.get(
        f"/api/v1/materials/{material['id']}",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == material["id"]
    assert body["code"] == "MAT-001"
    assert body["name"] == "Material Consultado"


def test_get_unknown_material_returns_not_found(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = material_client.get(
        f"/api/v1/materials/{uuid.uuid4()}",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 404

    assert (
        response.json()["error"]["code"]
        == "resource.not_found"
    )


def test_material_get_is_tenant_scoped(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    auth_user_id = uuid.uuid4()

    user = create_test_user(
        session,
        auth_user_id=auth_user_id,
    )

    first_membership = create_active_membership(
        session,
        tenant_id=tenant_id,
        user=user,
    )

    second_membership = create_active_membership(
        session,
        tenant_id=other_tenant_id,
        user=user,
    )

    grant_permissions(
        session,
        tenant_id=tenant_id,
        membership=first_membership,
        permission_codes=MATERIAL_PERMISSION_CODES,
    )

    grant_permissions(
        session,
        tenant_id=other_tenant_id,
        membership=second_membership,
        permission_codes=MATERIAL_PERMISSION_CODES,
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
        material = create_material(
            client,
            tenant_id,
            code="MAT-001",
            name="Material Tenant A",
        )

        response = client.get(
            f"/api/v1/materials/{material['id']}",
            headers=authentication_headers(
                other_tenant_id
            ),
        )

    assert response.status_code == 404

    assert (
        response.json()["error"]["code"]
        == "resource.not_found"
    )


def test_list_materials_returns_only_authenticated_tenant(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    auth_user_id = uuid.uuid4()

    user = create_test_user(
        session,
        auth_user_id=auth_user_id,
    )

    first_membership = create_active_membership(
        session,
        tenant_id=tenant_id,
        user=user,
    )

    second_membership = create_active_membership(
        session,
        tenant_id=other_tenant_id,
        user=user,
    )

    grant_permissions(
        session,
        tenant_id=tenant_id,
        membership=first_membership,
        permission_codes=MATERIAL_PERMISSION_CODES,
    )

    grant_permissions(
        session,
        tenant_id=other_tenant_id,
        membership=second_membership,
        permission_codes=MATERIAL_PERMISSION_CODES,
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
        create_material(
            client,
            tenant_id,
            code="MAT-A",
            name="Material A",
        )

        create_material(
            client,
            other_tenant_id,
            code="MAT-B",
            name="Material B",
        )

        response = client.get(
            "/api/v1/materials",
            headers=authentication_headers(
                tenant_id
            ),
        )

    assert response.status_code == 200

    assert [
        item["name"]
        for item in response.json()
    ] == [
        "Material A"
    ]


@pytest.mark.parametrize(
    ("search", "expected_name"),
    [
        (
            "MAT-ALFA",
            "MDF Branco",
        ),
        (
            "Branco",
            "MDF Branco",
        ),
        (
            "Chapas",
            "MDF Branco",
        ),
        (
            "CHAPA",
            "MDF Branco",
        ),
    ],
)
def test_list_materials_searches_supported_fields(
    material_client: TestClient,
    tenant_id: uuid.UUID,
    search: str,
    expected_name: str,
) -> None:
    create_material(
        material_client,
        tenant_id,
        code="MAT-ALFA",
        name="MDF Branco",
        category="Chapas",
        unit="CHAPA",
    )

    create_material(
        material_client,
        tenant_id,
        code="MAT-BETA",
        name="Fita Preta",
        category="Fitas",
        unit="M",
    )

    response = material_client.get(
        "/api/v1/materials",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "search": search,
        },
    )

    assert response.status_code == 200

    assert [
        item["name"]
        for item in response.json()
    ] == [
        expected_name
    ]


def test_list_materials_filters_category(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="MDF",
        category="Chapas",
    )

    create_material(
        material_client,
        tenant_id,
        code="MAT-002",
        name="Fita",
        category="Fitas",
        unit="M",
    )

    response = material_client.get(
        "/api/v1/materials",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "category": "Chapas",
        },
    )

    assert response.status_code == 200

    assert [
        item["name"]
        for item in response.json()
    ] == [
        "MDF"
    ]


def test_list_materials_filters_brand(
    material_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    first_brand_id = create_brand(
        session,
        tenant_id=tenant_id,
        code="MARCA-001",
        name="Duratex",
    )

    second_brand_id = create_brand(
        session,
        tenant_id=tenant_id,
        code="MARCA-002",
        name="Arauco",
    )

    create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="MDF Duratex",
        brand_id=first_brand_id,
    )

    create_material(
        material_client,
        tenant_id,
        code="MAT-002",
        name="MDF Arauco",
        brand_id=second_brand_id,
    )

    response = material_client.get(
        "/api/v1/materials",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "brand_id": str(
                first_brand_id
            ),
        },
    )

    assert response.status_code == 200

    assert [
        item["name"]
        for item in response.json()
    ] == [
        "MDF Duratex"
    ]


def test_list_materials_paginates(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material Alfa",
    )

    create_material(
        material_client,
        tenant_id,
        code="MAT-002",
        name="Material Beta",
    )

    create_material(
        material_client,
        tenant_id,
        code="MAT-003",
        name="Material Gama",
    )

    response = material_client.get(
        "/api/v1/materials",
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
        "Material Beta"
    ]


def test_list_materials_excludes_inactive_by_default(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    active_material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material Ativo",
    )

    inactive_material = create_material(
        material_client,
        tenant_id,
        code="MAT-002",
        name="Material Inativo",
    )

    deactivate_response = material_client.post(
        (
            "/api/v1/materials/"
            f"{inactive_material['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert deactivate_response.status_code == 200

    response = material_client.get(
        "/api/v1/materials",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    ids = {
        item["id"]
        for item in response.json()
    }

    assert active_material["id"] in ids
    assert inactive_material["id"] not in ids


def test_list_materials_can_include_inactive(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material Inativo",
    )

    deactivate_response = material_client.post(
        (
            "/api/v1/materials/"
            f"{material['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert deactivate_response.status_code == 200

    response = material_client.get(
        "/api/v1/materials",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "include_inactive": True,
        },
    )

    assert response.status_code == 200

    assert material["id"] in {
        item["id"]
        for item in response.json()
    }


def test_update_material(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material Antigo",
        category="Chapas",
        unit="UN",
    )

    response = material_client.patch(
        f"/api/v1/materials/{material['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " mat-002 ",
            "name": " Material Novo ",
            "category": " MDF ",
            "unit": " chapa ",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["code"] == "MAT-002"
    assert body["name"] == "Material Novo"
    assert body["category"] == "MDF"
    assert body["unit"] == "CHAPA"


def test_update_material_preserves_unspecified_fields(
    material_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    brand_id = create_brand(
        session,
        tenant_id=tenant_id,
    )

    material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material",
        category="Chapas",
        unit="UN",
        brand_id=brand_id,
    )

    response = material_client.patch(
        f"/api/v1/materials/{material['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "name": "Material Atualizado",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "Material Atualizado"
    assert body["code"] == "MAT-001"
    assert body["category"] == "Chapas"
    assert body["unit"] == "UN"

    assert (
        body["brand_id"]
        == str(brand_id)
    )


def test_update_material_assigns_brand(
    material_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    brand_id = create_brand(
        session,
        tenant_id=tenant_id,
    )

    material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material",
    )

    response = material_client.patch(
        f"/api/v1/materials/{material['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "brand_id": str(
                brand_id
            ),
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["brand_id"]
        == str(brand_id)
    )


def test_update_material_can_remove_brand(
    material_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    brand_id = create_brand(
        session,
        tenant_id=tenant_id,
    )

    material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material",
        brand_id=brand_id,
    )

    response = material_client.patch(
        f"/api/v1/materials/{material['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "brand_id": None,
        },
    )

    assert response.status_code == 200
    assert response.json()["brand_id"] is None


def test_update_rejects_brand_from_other_tenant(
    material_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material",
    )

    foreign_brand_id = create_brand(
        session,
        tenant_id=other_tenant_id,
        code="MARCA-OUTRA",
    )

    response = material_client.patch(
        f"/api/v1/materials/{material['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "brand_id": str(
                foreign_brand_id
            ),
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "validation.error"
    )


def test_update_rejects_unknown_brand(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material",
    )

    response = material_client.patch(
        f"/api/v1/materials/{material['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "brand_id": str(
                uuid.uuid4()
            ),
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "validation.error"
    )


def test_update_material_rejects_empty_payload(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material",
    )

    response = material_client.patch(
        f"/api/v1/materials/{material['id']}",
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


def test_update_rejects_duplicate_code(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material A",
    )

    second = create_material(
        material_client,
        tenant_id,
        code="MAT-002",
        name="Material B",
    )

    response = material_client.patch(
        f"/api/v1/materials/{second['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "mat-001",
        },
    )

    assert response.status_code == 409

    assert (
        response.json()["error"]["code"]
        == "resource.conflict"
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "code",
        "name",
        "category",
        "unit",
    ],
)
def test_update_rejects_null_required_fields(
    material_client: TestClient,
    tenant_id: uuid.UUID,
    field_name: str,
) -> None:
    material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material",
    )

    response = material_client.patch(
        f"/api/v1/materials/{material['id']}",
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


@pytest.mark.parametrize(
    "payload",
    [
        {
            "name": "",
        },
        {
            "code": "",
        },
        {
            "category": "",
        },
        {
            "unit": "",
        },
    ],
)
def test_create_rejects_invalid_material_payload(
    material_client: TestClient,
    tenant_id: uuid.UUID,
    payload: dict[str, Any],
) -> None:
    request_payload: dict[str, Any] = {
        "code": "MAT-001",
        "name": "Material",
        "category": "Chapas",
        "unit": "UN",
    }

    request_payload.update(
        payload
    )

    response = material_client.post(
        "/api/v1/materials",
        headers=authentication_headers(
            tenant_id
        ),
        json=request_payload,
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "request.validation_error"
    )


@pytest.mark.parametrize(
    "params",
    [
        {
            "limit": 0,
        },
        {
            "limit": 201,
        },
        {
            "offset": -1,
        },
        {
            "search": "",
        },
        {
            "category": "",
        },
    ],
)
def test_list_rejects_invalid_query_parameters(
    material_client: TestClient,
    tenant_id: uuid.UUID,
    params: dict[str, Any],
) -> None:
    response = material_client.get(
        "/api/v1/materials",
        headers=authentication_headers(
            tenant_id
        ),
        params=params,
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "request.validation_error"
    )


def test_deactivate_material(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material",
    )

    response = material_client.post(
        (
            "/api/v1/materials/"
            f"{material['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_deactivate_material_is_idempotent(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material",
    )

    url = (
        "/api/v1/materials/"
        f"{material['id']}/deactivate"
    )

    first = material_client.post(
        url,
        headers=authentication_headers(
            tenant_id
        ),
    )

    second = material_client.post(
        url,
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json()["is_active"] is False


def test_reactivate_material(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material",
    )

    material_client.post(
        (
            "/api/v1/materials/"
            f"{material['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    response = material_client.post(
        (
            "/api/v1/materials/"
            f"{material['id']}/reactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is True


def test_reactivate_material_is_idempotent(
    material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    material = create_material(
        material_client,
        tenant_id,
        code="MAT-001",
        name="Material",
    )

    url = (
        "/api/v1/materials/"
        f"{material['id']}/reactivate"
    )

    first = material_client.post(
        url,
        headers=authentication_headers(
            tenant_id
        ),
    )

    second = material_client.post(
        url,
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json()["is_active"] is True


def test_rejects_material_read_without_permission(
    unauthorized_material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_material_client.get(
        "/api/v1/materials",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert_permission_denied(
        response,
        MaterialPermissions.READ,
    )


def test_rejects_material_create_without_permission(
    unauthorized_material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_material_client.post(
        "/api/v1/materials",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "MAT-001",
            "name": "Material",
            "category": "Chapas",
            "unit": "UN",
        },
    )

    assert_permission_denied(
        response,
        MaterialPermissions.CREATE,
    )


def test_rejects_material_update_without_permission(
    unauthorized_material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_material_client.patch(
        f"/api/v1/materials/{uuid.uuid4()}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "name": "Sem Permissão",
        },
    )

    assert_permission_denied(
        response,
        MaterialPermissions.UPDATE,
    )


def test_rejects_material_deactivate_without_permission(
    unauthorized_material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_material_client.post(
        (
            "/api/v1/materials/"
            f"{uuid.uuid4()}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert_permission_denied(
        response,
        MaterialPermissions.DEACTIVATE,
    )


def test_rejects_material_reactivate_without_permission(
    unauthorized_material_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_material_client.post(
        (
            "/api/v1/materials/"
            f"{uuid.uuid4()}/reactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert_permission_denied(
        response,
        MaterialPermissions.REACTIVATE,
    )


def test_material_openapi_contract(
    client: TestClient,
) -> None:
    application = cast(
        FastAPI,
        client.app,
    )

    openapi = application.openapi()

    expected = {
        "/api/v1/materials": {
            "get",
            "post",
        },
        "/api/v1/materials/{material_id}": {
            "get",
            "patch",
        },
        "/api/v1/materials/{material_id}/deactivate": {
            "post",
        },
        "/api/v1/materials/{material_id}/reactivate": {
            "post",
        },
    }

    paths = openapi["paths"]

    for path, methods in expected.items():
        assert path in paths

        assert methods.issubset(
            set(paths[path])
        )
