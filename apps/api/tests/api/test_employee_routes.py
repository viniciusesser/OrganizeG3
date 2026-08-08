"""API tests for tenant employee operations."""

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
    EmployeePermissions,
)
from organizeg3_api.infrastructure.persistence.models import (
    BranchModel,
)

EMPLOYEE_PERMISSION_CODES = (
    EmployeePermissions.READ,
    EmployeePermissions.CREATE,
    EmployeePermissions.UPDATE,
    EmployeePermissions.DEACTIVATE,
    EmployeePermissions.REACTIVATE,
)


@pytest.fixture
def authenticated_employee_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide a client authorized for employee operations."""

    auth_user_id = uuid.uuid4()

    user = create_test_user(
        session,
        auth_user_id=auth_user_id,
    )

    primary_membership = create_active_membership(
        session,
        tenant_id=tenant_id,
        user=user,
    )

    secondary_membership = create_active_membership(
        session,
        tenant_id=other_tenant_id,
        user=user,
    )

    grant_permissions(
        session,
        tenant_id=tenant_id,
        membership=primary_membership,
        permission_codes=EMPLOYEE_PERMISSION_CODES,
    )

    grant_permissions(
        session,
        tenant_id=other_tenant_id,
        membership=secondary_membership,
        permission_codes=EMPLOYEE_PERMISSION_CODES,
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
def employee_client_without_permissions(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide an authenticated employee client without permissions."""

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


def create_branch(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str,
) -> BranchModel:
    """Create one active branch for API tests."""

    branch = BranchModel(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        code=code,
        name=f"Filial {code}",
        is_active=True,
    )

    session.add(
        branch
    )
    session.flush()

    return branch


def create_employee(
    client: TestClient,
    *,
    tenant_id: uuid.UUID,
    code: str,
    full_name: str,
    branch_id: uuid.UUID | None = None,
    document_number: str | None = None,
    email: str | None = None,
) -> dict[str, object]:
    """Create an employee through the public API."""

    payload: dict[str, object] = {
        "code": code,
        "full_name": full_name,
    }

    if branch_id is not None:
        payload["branch_id"] = str(
            branch_id
        )

    if document_number is not None:
        payload["document_number"] = (
            document_number
        )

    if email is not None:
        payload["email"] = email

    response = client.post(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
        json=payload,
    )

    assert response.status_code == 201

    return cast(
        dict[str, object],
        response.json(),
    )


def test_creates_complete_employee(
    authenticated_employee_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    branch = create_branch(
        session,
        tenant_id=tenant_id,
        code="MATRIZ",
    )

    response = authenticated_employee_client.post(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " func-001 ",
            "full_name": " Funcionário Teste ",
            "branch_id": str(
                branch.id
            ),
            "document_number": "529.982.247-25",
            "email": "FUNCIONARIO@EXAMPLE.COM",
            "phone": "(18) 99999-1234",
            "job_title": " Marceneiro ",
            "contract_type": " CLT ",
            "birth_date": "1990-01-01",
            "admission_date": "2025-01-10",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["tenant_id"] == str(
        tenant_id
    )
    assert body["branch_id"] == str(
        branch.id
    )
    assert body["code"] == "FUNC-001"

    assert (
        body["full_name"]
        == "Funcionário Teste"
    )

    assert (
        body["document_number"]
        == "52998224725"
    )

    assert (
        body["email"]
        == "funcionario@example.com"
    )

    assert body["phone"] == "18999991234"
    assert body["job_title"] == "Marceneiro"
    assert body["contract_type"] == "CLT"
    assert body["status"] == "ACTIVE"
    assert body["is_active"] is True

    assert (
        body["birth_date"]
        == "1990-01-01"
    )

    assert (
        body["admission_date"]
        == "2025-01-10"
    )

    assert body["termination_date"] is None
    assert body["id"] is not None
    assert body["created_at"] is not None
    assert body["updated_at"] is not None


def test_creates_employee_without_branch(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    employee = create_employee(
        authenticated_employee_client,
        tenant_id=tenant_id,
        code="FUNC-001",
        full_name="Funcionário",
    )

    assert employee["branch_id"] is None


def test_lists_only_authenticated_tenant_employees(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    create_employee(
        authenticated_employee_client,
        tenant_id=tenant_id,
        code="FUNC-A",
        full_name="Funcionário A",
    )

    create_employee(
        authenticated_employee_client,
        tenant_id=other_tenant_id,
        code="FUNC-B",
        full_name="Funcionário B",
    )

    response = authenticated_employee_client.get(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert body[0]["code"] == "FUNC-A"

    assert (
        body[0]["tenant_id"]
        == str(
            tenant_id
        )
    )


def test_lists_with_search(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_employee(
        authenticated_employee_client,
        tenant_id=tenant_id,
        code="MARC-001",
        full_name="João da Silva",
        email="joao@example.com",
    )

    create_employee(
        authenticated_employee_client,
        tenant_id=tenant_id,
        code="ADM-001",
        full_name="Maria Souza",
    )

    response = authenticated_employee_client.get(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "search": "joão",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1

    assert (
        body[0]["full_name"]
        == "João da Silva"
    )


def test_lists_with_pagination(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    for index, name in enumerate(
        (
            "Ana",
            "Bruno",
            "Carlos",
        ),
        start=1,
    ):
        create_employee(
            authenticated_employee_client,
            tenant_id=tenant_id,
            code=f"FUNC-{index}",
            full_name=name,
        )

    response = authenticated_employee_client.get(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "limit": 1,
            "offset": 1,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert body[0]["full_name"] == "Bruno"


def test_filters_by_branch(
    authenticated_employee_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    branch_a = create_branch(
        session,
        tenant_id=tenant_id,
        code="A",
    )

    branch_b = create_branch(
        session,
        tenant_id=tenant_id,
        code="B",
    )

    create_employee(
        authenticated_employee_client,
        tenant_id=tenant_id,
        code="FUNC-A",
        full_name="Funcionário A",
        branch_id=branch_a.id,
    )

    create_employee(
        authenticated_employee_client,
        tenant_id=tenant_id,
        code="FUNC-B",
        full_name="Funcionário B",
        branch_id=branch_b.id,
    )

    response = authenticated_employee_client.get(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "branch_id": str(
                branch_a.id
            ),
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert body[0]["code"] == "FUNC-A"


def test_filters_by_status_and_include_inactive(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    employee = create_employee(
        authenticated_employee_client,
        tenant_id=tenant_id,
        code="FUNC-I",
        full_name="Funcionário Inativo",
    )

    employee_id = employee["id"]

    deactivate_response = (
        authenticated_employee_client.post(
            (
                "/api/v1/employees/"
                f"{employee_id}/deactivate"
            ),
            headers=authentication_headers(
                tenant_id
            ),
        )
    )

    assert (
        deactivate_response.status_code
        == 200
    )

    default_response = (
        authenticated_employee_client.get(
            "/api/v1/employees",
            headers=authentication_headers(
                tenant_id
            ),
        )
    )

    assert default_response.status_code == 200
    assert default_response.json() == []

    filtered_response = (
        authenticated_employee_client.get(
            "/api/v1/employees",
            headers=authentication_headers(
                tenant_id
            ),
            params={
                "include_inactive": "true",
                "status": "INACTIVE",
            },
        )
    )

    assert filtered_response.status_code == 200

    body = filtered_response.json()

    assert len(body) == 1
    assert body[0]["status"] == "INACTIVE"
    assert body[0]["is_active"] is False


def test_gets_employee(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    employee = create_employee(
        authenticated_employee_client,
        tenant_id=tenant_id,
        code="FUNC-001",
        full_name="Funcionário",
    )

    response = authenticated_employee_client.get(
        (
            "/api/v1/employees/"
            f"{employee['id']}"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["id"] == employee["id"]


def test_updates_employee(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    employee = create_employee(
        authenticated_employee_client,
        tenant_id=tenant_id,
        code="FUNC-001",
        full_name="Nome Antigo",
        email="antigo@example.com",
    )

    response = authenticated_employee_client.patch(
        (
            "/api/v1/employees/"
            f"{employee['id']}"
        ),
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " func-002 ",
            "full_name": " Nome Novo ",
            "email": "NOVO@EXAMPLE.COM",
            "job_title": " Marceneiro ",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["code"] == "FUNC-002"
    assert body["full_name"] == "Nome Novo"
    assert body["email"] == "novo@example.com"
    assert body["job_title"] == "Marceneiro"


def test_update_can_clear_optional_fields(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    employee = create_employee(
        authenticated_employee_client,
        tenant_id=tenant_id,
        code="FUNC-001",
        full_name="Funcionário",
        email="funcionario@example.com",
    )

    response = authenticated_employee_client.patch(
        (
            "/api/v1/employees/"
            f"{employee['id']}"
        ),
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "email": None,
            "phone": None,
            "job_title": None,
            "branch_id": None,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["email"] is None
    assert body["phone"] is None
    assert body["job_title"] is None
    assert body["branch_id"] is None


def test_deactivates_and_reactivates_employee(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    employee = create_employee(
        authenticated_employee_client,
        tenant_id=tenant_id,
        code="FUNC-001",
        full_name="Funcionário",
    )

    employee_id = employee["id"]

    deactivate_response = (
        authenticated_employee_client.post(
            (
                "/api/v1/employees/"
                f"{employee_id}/deactivate"
            ),
            headers=authentication_headers(
                tenant_id
            ),
        )
    )

    assert (
        deactivate_response.status_code
        == 200
    )

    deactivated = deactivate_response.json()

    assert deactivated["status"] == "INACTIVE"
    assert deactivated["is_active"] is False

    reactivate_response = (
        authenticated_employee_client.post(
            (
                "/api/v1/employees/"
                f"{employee_id}/reactivate"
            ),
            headers=authentication_headers(
                tenant_id
            ),
        )
    )

    assert (
        reactivate_response.status_code
        == 200
    )

    reactivated = reactivate_response.json()

    assert reactivated["status"] == "ACTIVE"
    assert reactivated["is_active"] is True


def test_rejects_duplicate_code(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_employee(
        authenticated_employee_client,
        tenant_id=tenant_id,
        code="FUNC-001",
        full_name="Funcionário A",
    )

    response = authenticated_employee_client.post(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "func-001",
            "full_name": "Funcionário B",
        },
    )

    assert response.status_code == 409


def test_rejects_duplicate_document(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_employee(
        authenticated_employee_client,
        tenant_id=tenant_id,
        code="FUNC-001",
        full_name="Funcionário A",
        document_number="529.982.247-25",
    )

    response = authenticated_employee_client.post(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "FUNC-002",
            "full_name": "Funcionário B",
            "document_number": "52998224725",
        },
    )

    assert response.status_code == 409


def test_rejects_invalid_employee_payload(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = authenticated_employee_client.post(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "FUNC-001",
            "full_name": "Funcionário",
            "document_number": "123",
        },
    )

    assert response.status_code == 422


def test_rejects_unknown_branch(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = authenticated_employee_client.post(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "FUNC-001",
            "full_name": "Funcionário",
            "branch_id": str(
                uuid.uuid4()
            ),
        },
    )

    assert response.status_code == 422


def test_rejects_branch_from_another_tenant(
    authenticated_employee_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    foreign_branch = create_branch(
        session,
        tenant_id=other_tenant_id,
        code="OUTRA",
    )

    response = authenticated_employee_client.post(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "FUNC-001",
            "full_name": "Funcionário",
            "branch_id": str(
                foreign_branch.id
            ),
        },
    )

    assert response.status_code == 422


def test_returns_not_found_for_unknown_employee(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = authenticated_employee_client.get(
        (
            "/api/v1/employees/"
            f"{uuid.uuid4()}"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 404


def test_rejects_empty_update(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    employee = create_employee(
        authenticated_employee_client,
        tenant_id=tenant_id,
        code="FUNC-001",
        full_name="Funcionário",
    )

    response = authenticated_employee_client.patch(
        (
            "/api/v1/employees/"
            f"{employee['id']}"
        ),
        headers=authentication_headers(
            tenant_id
        ),
        json={},
    )

    assert response.status_code == 422


def test_employee_is_tenant_isolated(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    employee = create_employee(
        authenticated_employee_client,
        tenant_id=other_tenant_id,
        code="FUNC-OUTRO",
        full_name="Outro Tenant",
    )

    response = authenticated_employee_client.get(
        (
            "/api/v1/employees/"
            f"{employee['id']}"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 404


def test_rejects_read_without_permission(
    employee_client_without_permissions: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = employee_client_without_permissions.get(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert_permission_denied(
        response,
        EmployeePermissions.READ,
    )


def test_rejects_create_without_permission(
    employee_client_without_permissions: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = employee_client_without_permissions.post(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "FUNC-001",
            "full_name": "Funcionário",
        },
    )

    assert_permission_denied(
        response,
        EmployeePermissions.CREATE,
    )


def test_rejects_update_without_permission(
    employee_client_without_permissions: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = employee_client_without_permissions.patch(
        (
            "/api/v1/employees/"
            f"{uuid.uuid4()}"
        ),
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "full_name": "Novo Nome",
        },
    )

    assert_permission_denied(
        response,
        EmployeePermissions.UPDATE,
    )


def test_rejects_deactivate_without_permission(
    employee_client_without_permissions: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = employee_client_without_permissions.post(
        (
            "/api/v1/employees/"
            f"{uuid.uuid4()}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert_permission_denied(
        response,
        EmployeePermissions.DEACTIVATE,
    )


def test_rejects_reactivate_without_permission(
    employee_client_without_permissions: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = employee_client_without_permissions.post(
        (
            "/api/v1/employees/"
            f"{uuid.uuid4()}/reactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert_permission_denied(
        response,
        EmployeePermissions.REACTIVATE,
    )


def test_rejects_invalid_pagination(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = authenticated_employee_client.get(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "limit": 0,
        },
    )

    assert response.status_code == 422

    response = authenticated_employee_client.get(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "offset": -1,
        },
    )

    assert response.status_code == 422


def test_rejects_invalid_status_filter(
    authenticated_employee_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = authenticated_employee_client.get(
        "/api/v1/employees",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "status": "INVALID",
        },
    )

    assert response.status_code == 422


def test_openapi_exposes_employee_contract(
    authenticated_employee_client: TestClient,
) -> None:
    response = authenticated_employee_client.get(
        "/openapi.json"
    )

    assert response.status_code == 200

    paths = response.json()["paths"]

    assert "/api/v1/employees" in paths

    assert (
        "/api/v1/employees/{employee_id}"
        in paths
    )

    assert (
        "/api/v1/employees/"
        "{employee_id}/deactivate"
        in paths
    )

    assert (
        "/api/v1/employees/"
        "{employee_id}/reactivate"
        in paths
    )

    collection = paths[
        "/api/v1/employees"
    ]

    assert "get" in collection
    assert "post" in collection

    detail = paths[
        "/api/v1/employees/{employee_id}"
    ]

    assert "get" in detail
    assert "patch" in detail

    parameter_names = {
        parameter["name"]
        for parameter in collection[
            "get"
        ]["parameters"]
    }

    assert {
        "include_inactive",
        "search",
        "branch_id",
        "status",
        "limit",
        "offset",
    }.issubset(
        parameter_names
    )
