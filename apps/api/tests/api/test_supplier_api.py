"""HTTP tests for supplier application routes."""

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

from organizeg3_api.domain.identity.authentication import (
    VerifiedToken,
)
from organizeg3_api.domain.identity.permissions import (
    SupplierPermissions,
)

pytestmark = pytest.mark.api

SUPPLIER_PERMISSION_CODES = (
    SupplierPermissions.READ,
    SupplierPermissions.CREATE,
    SupplierPermissions.UPDATE,
    SupplierPermissions.DEACTIVATE,
    SupplierPermissions.REACTIVATE,
)


@pytest.fixture
def supplier_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide a client authorized for every supplier operation."""

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
        permission_codes=SUPPLIER_PERMISSION_CODES,
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
def unauthorized_supplier_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide an authenticated membership without supplier permissions."""

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


def create_supplier(
    client: TestClient,
    tenant_id: uuid.UUID,
    *,
    code: str,
    name: str,
    document_number: str | None = None,
    email: str | None = None,
) -> dict[str, Any]:
    """Create one supplier through the public API."""

    payload: dict[str, Any] = {
        "code": code,
        "name": name,
    }

    if document_number is not None:
        payload["document_number"] = document_number

    if email is not None:
        payload["email"] = email

    response = client.post(
        "/api/v1/suppliers",
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


def test_create_supplier_normalizes_complete_payload(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = supplier_client.post(
        "/api/v1/suppliers",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " forn-001 ",
            "name": " Fornecedor Teste ",
            "trade_name": " Loja Teste ",
            "legal_name": " Fornecedor Teste Ltda ",
            "document_number": "04.252.011/0001-10",
            "state_registration": " 123456 ",
            "email": " COMERCIAL@EXAMPLE.COM ",
            "invoice_email": " NFE@EXAMPLE.COM ",
            "phone": "(18) 99999-1234",
            "secondary_phone": "(18) 3222-1234",
            "website": " https://example.com ",
            "contact_name": " Contato ",
            "postal_code": "19200-000",
            "street": " Rua Teste ",
            "number": " 100 ",
            "district": " Centro ",
            "city": " Rosana ",
            "state": "sp",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["tenant_id"] == str(
        tenant_id
    )

    assert body["code"] == "FORN-001"
    assert body["name"] == "Fornecedor Teste"
    assert body["trade_name"] == "Loja Teste"

    assert (
        body["legal_name"]
        == "Fornecedor Teste Ltda"
    )

    assert (
        body["document_number"]
        == "04252011000110"
    )

    assert body["state_registration"] == "123456"

    assert (
        body["email"]
        == "comercial@example.com"
    )

    assert (
        body["invoice_email"]
        == "nfe@example.com"
    )

    assert body["phone"] == "18999991234"

    assert (
        body["secondary_phone"]
        == "1832221234"
    )

    assert body["website"] == "https://example.com"
    assert body["contact_name"] == "Contato"
    assert body["postal_code"] == "19200000"
    assert body["street"] == "Rua Teste"
    assert body["number"] == "100"
    assert body["district"] == "Centro"
    assert body["city"] == "Rosana"
    assert body["state"] == "SP"
    assert body["is_active"] is True

    assert body["id"] is not None
    assert body["created_at"] is not None
    assert body["updated_at"] is not None


def test_get_supplier(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    supplier = create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor Consultado",
    )

    response = supplier_client.get(
        f"/api/v1/suppliers/{supplier['id']}",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == supplier["id"]
    assert body["code"] == "FORN-001"

    assert (
        body["name"]
        == "Fornecedor Consultado"
    )


def test_get_unknown_supplier_returns_not_found(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = supplier_client.get(
        f"/api/v1/suppliers/{uuid.uuid4()}",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 404

    assert (
        response.json()["error"]["code"]
        == "resource.not_found"
    )


def test_supplier_get_is_tenant_scoped(
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
        permission_codes=SUPPLIER_PERMISSION_CODES,
    )

    grant_permissions(
        session,
        tenant_id=other_tenant_id,
        membership=other_membership,
        permission_codes=SUPPLIER_PERMISSION_CODES,
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
        supplier = create_supplier(
            client,
            tenant_id,
            code="FORN-A",
            name="Fornecedor Tenant A",
        )

        response = client.get(
            f"/api/v1/suppliers/{supplier['id']}",
            headers=authentication_headers(
                other_tenant_id
            ),
        )

    assert response.status_code == 404

    assert (
        response.json()["error"]["code"]
        == "resource.not_found"
    )


def test_list_suppliers_returns_only_authenticated_tenant(
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
        permission_codes=SUPPLIER_PERMISSION_CODES,
    )

    grant_permissions(
        session,
        tenant_id=other_tenant_id,
        membership=other_membership,
        permission_codes=SUPPLIER_PERMISSION_CODES,
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
        create_supplier(
            client,
            tenant_id,
            code="FORN-A",
            name="Fornecedor A",
        )

        create_supplier(
            client,
            other_tenant_id,
            code="FORN-B",
            name="Fornecedor B",
        )

        response = client.get(
            "/api/v1/suppliers",
            headers=authentication_headers(
                tenant_id
            ),
        )

    assert response.status_code == 200

    assert [
        item["name"]
        for item in response.json()
    ] == [
        "Fornecedor A"
    ]


def test_list_suppliers_searches_by_name(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Madeireira Alfa",
    )

    create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-002",
        name="Ferragens Beta",
    )

    response = supplier_client.get(
        "/api/v1/suppliers",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "search": "Beta",
        },
    )

    assert response.status_code == 200

    assert [
        item["name"]
        for item in response.json()
    ] == [
        "Ferragens Beta"
    ]


def test_list_suppliers_searches_normalized_document(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor Documento",
        document_number="04.252.011/0001-10",
    )

    response = supplier_client.get(
        "/api/v1/suppliers",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "search": "04.252.011",
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 1

    assert (
        response.json()[0]["document_number"]
        == "04252011000110"
    )


def test_list_suppliers_paginates(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor Alfa",
    )

    create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-002",
        name="Fornecedor Beta",
    )

    create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-003",
        name="Fornecedor Gama",
    )

    response = supplier_client.get(
        "/api/v1/suppliers",
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
        "Fornecedor Beta"
    ]


def test_list_suppliers_excludes_inactive_by_default(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    active_supplier = create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor Ativo",
    )

    inactive_supplier = create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-002",
        name="Fornecedor Inativo",
    )

    deactivate_response = supplier_client.post(
        (
            "/api/v1/suppliers/"
            f"{inactive_supplier['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert deactivate_response.status_code == 200

    response = supplier_client.get(
        "/api/v1/suppliers",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    ids = {
        item["id"]
        for item in response.json()
    }

    assert active_supplier["id"] in ids
    assert inactive_supplier["id"] not in ids


def test_list_suppliers_can_include_inactive(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    supplier = create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor Inativo",
    )

    response = supplier_client.post(
        (
            "/api/v1/suppliers/"
            f"{supplier['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    response = supplier_client.get(
        "/api/v1/suppliers",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "include_inactive": True,
        },
    )

    assert response.status_code == 200

    assert supplier["id"] in {
        item["id"]
        for item in response.json()
    }


def test_update_supplier(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    supplier = create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor Antigo",
        email="antigo@example.com",
    )

    response = supplier_client.patch(
        f"/api/v1/suppliers/{supplier['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " forn-002 ",
            "name": " Fornecedor Novo ",
            "email": " NOVO@EXAMPLE.COM ",
            "state": "sp",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["code"] == "FORN-002"
    assert body["name"] == "Fornecedor Novo"
    assert body["email"] == "novo@example.com"
    assert body["state"] == "SP"


def test_update_supplier_preserves_unspecified_fields(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    supplier = create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor",
        email="original@example.com",
    )

    response = supplier_client.patch(
        f"/api/v1/suppliers/{supplier['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "name": "Fornecedor Atualizado",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "Fornecedor Atualizado"

    assert (
        body["email"]
        == "original@example.com"
    )


def test_update_supplier_can_clear_optional_field(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    supplier = create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor",
        email="original@example.com",
    )

    response = supplier_client.patch(
        f"/api/v1/suppliers/{supplier['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "email": None,
        },
    )

    assert response.status_code == 200
    assert response.json()["email"] is None


def test_update_supplier_rejects_empty_payload(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    supplier = create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor",
    )

    response = supplier_client.patch(
        f"/api/v1/suppliers/{supplier['id']}",
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


def test_create_rejects_duplicate_code(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor A",
    )

    response = supplier_client.post(
        "/api/v1/suppliers",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "forn-001",
            "name": "Fornecedor B",
        },
    )

    assert response.status_code == 409

    body = response.json()

    assert body["error"]["code"] == "resource.conflict"

    assert body["error"]["details"] == {
        "field": "code",
        "value": "FORN-001",
    }


def test_create_rejects_duplicate_document(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor A",
        document_number="04.252.011/0001-10",
    )

    response = supplier_client.post(
        "/api/v1/suppliers",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "FORN-002",
            "name": "Fornecedor B",
            "document_number": "04252011000110",
        },
    )

    assert response.status_code == 409

    assert (
        response.json()["error"]["details"]["field"]
        == "document_number"
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        (
            "document_number",
            "04.252.011/0001-11",
        ),
        (
            "email",
            "email-invalido",
        ),
        (
            "phone",
            "9999",
        ),
        (
            "postal_code",
            "123",
        ),
        (
            "state",
            "S",
        ),
    ],
)
def test_create_rejects_invalid_supplier_data(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
    field: str,
    value: str,
) -> None:
    response = supplier_client.post(
        "/api/v1/suppliers",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "FORN-001",
            "name": "Fornecedor Inválido",
            field: value,
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "validation.error"
    )


@pytest.mark.parametrize(
    ("params", "expected_status"),
    [
        (
            {
                "limit": 0,
            },
            422,
        ),
        (
            {
                "limit": 201,
            },
            422,
        ),
        (
            {
                "offset": -1,
            },
            422,
        ),
        (
            {
                "search": "",
            },
            422,
        ),
    ],
)
def test_list_rejects_invalid_query_parameters(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
    params: dict[str, Any],
    expected_status: int,
) -> None:
    response = supplier_client.get(
        "/api/v1/suppliers",
        headers=authentication_headers(
            tenant_id
        ),
        params=params,
    )

    assert response.status_code == expected_status

    assert (
        response.json()["error"]["code"]
        == "request.validation_error"
    )


def test_deactivate_supplier(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    supplier = create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor",
    )

    response = supplier_client.post(
        (
            "/api/v1/suppliers/"
            f"{supplier['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_deactivate_supplier_is_idempotent(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    supplier = create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor",
    )

    url = (
        "/api/v1/suppliers/"
        f"{supplier['id']}/deactivate"
    )

    first = supplier_client.post(
        url,
        headers=authentication_headers(
            tenant_id
        ),
    )

    second = supplier_client.post(
        url,
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json()["is_active"] is False


def test_reactivate_supplier(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    supplier = create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor",
    )

    supplier_client.post(
        (
            "/api/v1/suppliers/"
            f"{supplier['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    response = supplier_client.post(
        (
            "/api/v1/suppliers/"
            f"{supplier['id']}/reactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is True


def test_reactivate_supplier_is_idempotent(
    supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    supplier = create_supplier(
        supplier_client,
        tenant_id,
        code="FORN-001",
        name="Fornecedor",
    )

    response = supplier_client.post(
        (
            "/api/v1/suppliers/"
            f"{supplier['id']}/reactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is True


def test_rejects_supplier_read_without_permission(
    unauthorized_supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_supplier_client.get(
        "/api/v1/suppliers",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert_permission_denied(
        response,
        SupplierPermissions.READ,
    )


def test_rejects_supplier_create_without_permission(
    unauthorized_supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_supplier_client.post(
        "/api/v1/suppliers",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "FORN-001",
            "name": "Sem Permissão",
        },
    )

    assert_permission_denied(
        response,
        SupplierPermissions.CREATE,
    )


def test_rejects_supplier_update_without_permission(
    unauthorized_supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_supplier_client.patch(
        f"/api/v1/suppliers/{uuid.uuid4()}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "name": "Sem Permissão",
        },
    )

    assert_permission_denied(
        response,
        SupplierPermissions.UPDATE,
    )


def test_rejects_supplier_deactivate_without_permission(
    unauthorized_supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_supplier_client.post(
        (
            "/api/v1/suppliers/"
            f"{uuid.uuid4()}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert_permission_denied(
        response,
        SupplierPermissions.DEACTIVATE,
    )


def test_rejects_supplier_reactivate_without_permission(
    unauthorized_supplier_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_supplier_client.post(
        (
            "/api/v1/suppliers/"
            f"{uuid.uuid4()}/reactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert_permission_denied(
        response,
        SupplierPermissions.REACTIVATE,
    )


def test_supplier_openapi_contract(
    client: TestClient,
) -> None:
    application = cast(
        FastAPI,
        client.app,
    )

    openapi = application.openapi()

    expected = {
        "/api/v1/suppliers": {
            "get",
            "post",
        },
        "/api/v1/suppliers/{supplier_id}": {
            "get",
            "patch",
        },
        "/api/v1/suppliers/{supplier_id}/deactivate": {
            "post",
        },
        "/api/v1/suppliers/{supplier_id}/reactivate": {
            "post",
        },
    }

    paths = openapi["paths"]

    for path, methods in expected.items():
        assert path in paths

        assert methods.issubset(
            set(paths[path])
        )
