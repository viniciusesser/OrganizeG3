"""HTTP tests for company routes."""

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

from organizeg3_api.domain.company.entity import (
    Company,
)
from organizeg3_api.domain.identity.authentication import (
    VerifiedToken,
)
from organizeg3_api.domain.identity.permissions import (
    CompanyPermissions,
)
from organizeg3_api.infrastructure.persistence.repositories.company_repository import (
    SQLAlchemyCompanyRepository,
)

pytestmark = pytest.mark.api


COMPANY_PERMISSION_CODES = (
    CompanyPermissions.READ,
    CompanyPermissions.CREATE,
    CompanyPermissions.UPDATE,
)


@pytest.fixture
def authenticated_company_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide an authenticated client with every company permission."""

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
        permission_codes=COMPANY_PERMISSION_CODES,
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
def unauthorized_company_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide an authenticated membership with no company permissions."""

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
    """Assert the standardized permission error."""

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


def test_creates_company(
    authenticated_company_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = authenticated_company_client.post(
        "/api/v1/company",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "trade_name": " Empresa Teste ",
            "legal_name": " Empresa Teste LTDA ",
            "document_number": "12.345.678/0001-90",
            "email": " CONTATO@EXAMPLE.COM ",
            "phone": "(18) 3222-1234",
            "city": " Rosana ",
            "state": "sp",
            "postal_code": "19273-000",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["tenant_id"] == str(
        tenant_id
    )
    assert body["trade_name"] == "Empresa Teste"
    assert (
        body["legal_name"]
        == "Empresa Teste LTDA"
    )
    assert (
        body["document_number"]
        == "12345678000190"
    )
    assert (
        body["email"]
        == "contato@example.com"
    )
    assert body["phone"] == "1832221234"
    assert body["city"] == "Rosana"
    assert body["state"] == "SP"
    assert body["postal_code"] == "19273000"
    assert body["is_active"] is True


def test_gets_company(
    authenticated_company_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_response = (
        authenticated_company_client.post(
            "/api/v1/company",
            headers=authentication_headers(
                tenant_id
            ),
            json={
                "trade_name": "Empresa Teste",
            },
        )
    )

    assert create_response.status_code == 201

    response = authenticated_company_client.get(
        "/api/v1/company",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert (
        response.json()["trade_name"]
        == "Empresa Teste"
    )


def test_updates_company(
    authenticated_company_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_response = (
        authenticated_company_client.post(
            "/api/v1/company",
            headers=authentication_headers(
                tenant_id
            ),
            json={
                "trade_name": "Empresa Antiga",
                "email": "antigo@example.com",
            },
        )
    )

    assert create_response.status_code == 201

    response = authenticated_company_client.patch(
        "/api/v1/company",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "trade_name": " Empresa Nova ",
            "email": " NOVO@EXAMPLE.COM ",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["trade_name"] == "Empresa Nova"
    assert body["email"] == "novo@example.com"


def test_rejects_duplicate_company(
    authenticated_company_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    first_response = (
        authenticated_company_client.post(
            "/api/v1/company",
            headers=authentication_headers(
                tenant_id
            ),
            json={
                "trade_name": "Empresa A",
            },
        )
    )

    assert first_response.status_code == 201

    response = authenticated_company_client.post(
        "/api/v1/company",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "trade_name": "Empresa B",
        },
    )

    assert response.status_code == 409
    assert (
        response.json()["error"]["code"]
        == "resource.conflict"
    )


def test_returns_not_found_when_company_does_not_exist(
    authenticated_company_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = authenticated_company_client.get(
        "/api/v1/company",
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
    authenticated_company_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_response = (
        authenticated_company_client.post(
            "/api/v1/company",
            headers=authentication_headers(
                tenant_id
            ),
            json={
                "trade_name": "Empresa",
            },
        )
    )

    assert create_response.status_code == 201

    response = authenticated_company_client.patch(
        "/api/v1/company",
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


def test_rejects_invalid_company_payload(
    authenticated_company_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = authenticated_company_client.post(
        "/api/v1/company",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "trade_name": "Empresa",
            "email": "email-invalido",
        },
    )

    assert response.status_code == 422
    assert (
        response.json()["error"]["code"]
        == "request.validation_error"
    )


def test_company_is_tenant_isolated(
    authenticated_company_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    repository = SQLAlchemyCompanyRepository(
        session
    )

    repository.add(
        Company.create(
            tenant_id=other_tenant_id,
            trade_name="Empresa do Outro Tenant",
        )
    )

    response = authenticated_company_client.get(
        "/api/v1/company",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 404


def test_rejects_company_read_without_permission(
    unauthorized_company_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_company_client.get(
        "/api/v1/company",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert_permission_denied(
        response,
        CompanyPermissions.READ,
    )


def test_rejects_company_create_without_permission(
    unauthorized_company_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_company_client.post(
        "/api/v1/company",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "trade_name": "Empresa",
        },
    )

    assert_permission_denied(
        response,
        CompanyPermissions.CREATE,
    )


def test_rejects_company_update_without_permission(
    unauthorized_company_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = unauthorized_company_client.patch(
        "/api/v1/company",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "trade_name": "Empresa",
        },
    )

    assert_permission_denied(
        response,
        CompanyPermissions.UPDATE,
    )


@pytest.mark.parametrize(
    "permission_code",
    [
        CompanyPermissions.READ,
        CompanyPermissions.CREATE,
        CompanyPermissions.UPDATE,
    ],
)
def test_granted_company_permission_is_resolved(
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


def test_openapi_exposes_company_contract(
    client: TestClient,
) -> None:
    application = cast(
        FastAPI,
        client.app,
    )

    schema = application.openapi()

    assert "/api/v1/company" in schema[
        "paths"
    ]

    assert set(
        schema["paths"]["/api/v1/company"]
    ) == {
        "get",
        "patch",
        "post",
    }
