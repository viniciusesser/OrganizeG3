"""HTTP tests for machine application routes."""

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
    MachinePermissions,
)
from organizeg3_api.infrastructure.persistence.models.branch import (
    BranchModel,
)

pytestmark = pytest.mark.api



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


MACHINE_PERMISSION_CODES = (
    MachinePermissions.READ,
    MachinePermissions.CREATE,
    MachinePermissions.UPDATE,
    MachinePermissions.CHANGE_STATUS,
    MachinePermissions.DEACTIVATE,
    MachinePermissions.REACTIVATE,
)


@pytest.fixture
def machine_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide a client authorized for every machine operation."""

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
        permission_codes=MACHINE_PERMISSION_CODES,
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
def unauthorized_machine_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Provide authentication without machine permissions."""

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


def create_branch(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str,
    name: str,
) -> uuid.UUID:
    """Create one tenant branch directly for machine API tests."""

    branch_id = uuid.uuid4()
    now = datetime.now(UTC)

    branch = BranchModel(
        id=branch_id,
        tenant_id=tenant_id,
        code=code,
        name=name,
        is_headquarters=False,
        is_active=True,
        created_at=now,
        updated_at=now,
    )

    session.add(
        branch
    )
    session.flush()

    return branch_id


def create_machine(
    client: TestClient,
    tenant_id: uuid.UUID,
    *,
    code: str,
    name: str,
    machine_type: str = "Seccionadora",
    branch_id: uuid.UUID | None = None,
    manufacturer: str | None = None,
    model: str | None = None,
    serial_number: str | None = None,
) -> dict[str, Any]:
    """Create one machine through the public API."""

    payload: dict[str, Any] = {
        "code": code,
        "name": name,
        "machine_type": machine_type,
    }

    if branch_id is not None:
        payload["branch_id"] = str(
            branch_id
        )

    if manufacturer is not None:
        payload["manufacturer"] = manufacturer

    if model is not None:
        payload["model"] = model

    if serial_number is not None:
        payload["serial_number"] = serial_number

    response = client.post(
        "/api/v1/machines",
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
    """Configure one user with machine access to two tenants."""

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
        permission_codes=MACHINE_PERMISSION_CODES,
    )

    grant_permissions(
        session,
        tenant_id=other_tenant_id,
        membership=other_membership,
        permission_codes=MACHINE_PERMISSION_CODES,
    )

    return StubTokenVerifier(
        VerifiedToken(
            auth_user_id=auth_user_id,
            role="authenticated",
            email=user.email,
        )
    )


def test_create_machine_normalizes_payload(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = machine_client.post(
        "/api/v1/machines",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " maq-001 ",
            "name": " Seccionadora ",
            "machine_type": " Corte ",
            "manufacturer": " Homag ",
            "model": " Sawteq ",
            "serial_number": " ABC-123 ",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["tenant_id"] == str(
        tenant_id
    )
    assert body["code"] == "MAQ-001"
    assert body["name"] == "Seccionadora"
    assert body["machine_type"] == "Corte"
    assert body["manufacturer"] == "Homag"
    assert body["model"] == "Sawteq"
    assert body["serial_number"] == "ABC-123"
    assert body["branch_id"] is None
    assert body["status"] == "AVAILABLE"
    assert body["is_active"] is True
    assert body["id"] is not None
    assert body["created_at"] is not None
    assert body["updated_at"] is not None


def test_create_machine_with_branch(
    machine_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    branch_id = create_branch(
        session,
        tenant_id=tenant_id,
        code="FIL-001",
        name="Filial 1",
    )

    response = machine_client.post(
        "/api/v1/machines",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "MAQ-001",
            "name": "Máquina",
            "machine_type": "Tipo",
            "branch_id": str(
                branch_id
            ),
        },
    )

    assert response.status_code == 201

    assert (
        response.json()["branch_id"]
        == str(branch_id)
    )


def test_create_rejects_branch_from_other_tenant(
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

    branch_id = create_branch(
        session,
        tenant_id=other_tenant_id,
        code="FIL-OTHER",
        name="Outra filial",
    )

    with override_token_verifier(
        client,
        verifier,
    ):
        response = client.post(
            "/api/v1/machines",
            headers=authentication_headers(
                tenant_id
            ),
            json={
                "code": "MAQ-001",
                "name": "Máquina",
                "machine_type": "Tipo",
                "branch_id": str(
                    branch_id
                ),
            },
        )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation.error"


def test_create_rejects_duplicate_code(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Máquina A",
    )

    response = machine_client.post(
        "/api/v1/machines",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " maq-001 ",
            "name": "Máquina B",
            "machine_type": "Tipo",
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
            "code",
            "",
        ),
        (
            "name",
            "",
        ),
        (
            "machine_type",
            "",
        ),
    ],
)
def test_create_rejects_invalid_required_fields(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
    field: str,
    value: object,
) -> None:
    payload: dict[str, object] = {
        "code": "MAQ-001",
        "name": "Máquina",
        "machine_type": "Tipo",
    }

    payload[field] = value

    response = machine_client.post(
        "/api/v1/machines",
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
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = machine_client.post(
        "/api/v1/machines",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "MAQ-001",
            "name": "Máquina",
            "machine_type": "Tipo",
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


def test_get_machine(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Seccionadora",
    )

    response = machine_client.get(
        f"/api/v1/machines/{machine['id']}",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == machine["id"]
    assert body["code"] == "MAQ-001"
    assert body["name"] == "Seccionadora"


def test_get_unknown_machine_returns_not_found(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = machine_client.get(
        f"/api/v1/machines/{uuid.uuid4()}",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "resource.not_found"


def test_machine_get_is_tenant_scoped(
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
        machine = create_machine(
            client,
            tenant_id,
            code="MAQ-A",
            name="Tenant A",
        )

        response = client.get(
            f"/api/v1/machines/{machine['id']}",
            headers=authentication_headers(
                other_tenant_id
            ),
        )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "resource.not_found"


def test_list_machines_returns_only_authenticated_tenant(
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
        create_machine(
            client,
            tenant_id,
            code="MAQ-A",
            name="Máquina A",
        )

        create_machine(
            client,
            other_tenant_id,
            code="MAQ-B",
            name="Máquina B",
        )

        response = client.get(
            "/api/v1/machines",
            headers=authentication_headers(
                tenant_id
            ),
        )

    assert response.status_code == 200

    assert [
        item["name"]
        for item in response.json()
    ] == [
        "Máquina A"
    ]


@pytest.mark.parametrize(
    "search",
    [
        "MAQ-001",
        "Seccionadora",
        "Corte",
        "Homag",
        "Sawteq",
        "ABC-123",
    ],
)
def test_list_searches_supported_fields(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
    search: str,
) -> None:
    create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Seccionadora",
        machine_type="Corte",
        manufacturer="Homag",
        model="Sawteq",
        serial_number="ABC-123",
    )

    create_machine(
        machine_client,
        tenant_id,
        code="MAQ-002",
        name="Coladeira",
        machine_type="Borda",
    )

    response = machine_client.get(
        "/api/v1/machines",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "search": search,
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["code"] == "MAQ-001"


def test_list_filters_machine_type(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Seccionadora",
        machine_type="Corte",
    )

    create_machine(
        machine_client,
        tenant_id,
        code="MAQ-002",
        name="Coladeira",
        machine_type="Borda",
    )

    response = machine_client.get(
        "/api/v1/machines",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "machine_type": "Corte",
        },
    )

    assert response.status_code == 200

    assert [
        item["code"]
        for item in response.json()
    ] == [
        "MAQ-001"
    ]


def test_list_filters_status(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    first = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="DisponÃ­vel",
    )

    second = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-002",
        name="ManutenÃ§Ã£o",
    )

    response = machine_client.post(
        f"/api/v1/machines/{second['id']}/status",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "status": "MAINTENANCE",
        },
    )

    assert response.status_code == 200

    response = machine_client.get(
        "/api/v1/machines",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "status": "MAINTENANCE",
        },
    )

    assert response.status_code == 200

    ids = {
        item["id"]
        for item in response.json()
    }

    assert second["id"] in ids
    assert first["id"] not in ids


def test_list_rejects_invalid_status(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    response = machine_client.get(
        "/api/v1/machines",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "status": "INVALID",
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "request.validation_error"
    )


def test_list_filters_branch(
    machine_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    branch_a = create_branch(
        session,
        tenant_id=tenant_id,
        code="FIL-A",
        name="Filial A",
    )

    branch_b = create_branch(
        session,
        tenant_id=tenant_id,
        code="FIL-B",
        name="Filial B",
    )

    first = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Máquina A",
        branch_id=branch_a,
    )

    create_machine(
        machine_client,
        tenant_id,
        code="MAQ-002",
        name="Máquina B",
        branch_id=branch_b,
    )

    response = machine_client.get(
        "/api/v1/machines",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "branch_id": str(
                branch_a
            ),
        },
    )

    assert response.status_code == 200

    assert [
        item["id"]
        for item in response.json()
    ] == [
        first["id"]
    ]


def test_list_paginates(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Alfa",
    )

    create_machine(
        machine_client,
        tenant_id,
        code="MAQ-002",
        name="Beta",
    )

    create_machine(
        machine_client,
        tenant_id,
        code="MAQ-003",
        name="Gama",
    )

    response = machine_client.get(
        "/api/v1/machines",
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
    machine_client: TestClient,
    tenant_id: uuid.UUID,
    parameter: str,
    value: int,
) -> None:
    response = machine_client.get(
        "/api/v1/machines",
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
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    active_machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Ativa",
    )

    inactive_machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-002",
        name="Inativa",
    )

    response = machine_client.post(
        (
            "/api/v1/machines/"
            f"{inactive_machine['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    response = machine_client.get(
        "/api/v1/machines",
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    ids = {
        item["id"]
        for item in response.json()
    }

    assert active_machine["id"] in ids
    assert inactive_machine["id"] not in ids


def test_list_can_include_inactive(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Inativa",
    )

    response = machine_client.post(
        (
            "/api/v1/machines/"
            f"{machine['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200

    response = machine_client.get(
        "/api/v1/machines",
        headers=authentication_headers(
            tenant_id
        ),
        params={
            "include_inactive": True,
        },
    )

    assert response.status_code == 200

    assert machine["id"] in {
        item["id"]
        for item in response.json()
    }


def test_update_machine(
    machine_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    branch_id = create_branch(
        session,
        tenant_id=tenant_id,
        code="FIL-001",
        name="Filial",
    )

    machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Antiga",
        machine_type="Antigo",
    )

    response = machine_client.patch(
        f"/api/v1/machines/{machine['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": " maq-002 ",
            "name": " Nova ",
            "machine_type": " Corte ",
            "branch_id": str(
                branch_id
            ),
            "manufacturer": " Homag ",
            "model": " Sawteq ",
            "serial_number": " ABC ",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["code"] == "MAQ-002"
    assert body["name"] == "Nova"
    assert body["machine_type"] == "Corte"
    assert body["branch_id"] == str(
        branch_id
    )
    assert body["manufacturer"] == "Homag"
    assert body["model"] == "Sawteq"
    assert body["serial_number"] == "ABC"


def test_update_preserves_unspecified_fields(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Máquina",
        machine_type="Corte",
        manufacturer="Homag",
    )

    response = machine_client.patch(
        f"/api/v1/machines/{machine['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "name": "Atualizada",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "Atualizada"
    assert body["code"] == "MAQ-001"
    assert body["machine_type"] == "Corte"
    assert body["manufacturer"] == "Homag"


def test_update_can_clear_optional_fields(
    machine_client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    branch_id = create_branch(
        session,
        tenant_id=tenant_id,
        code="FIL-001",
        name="Filial",
    )

    machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Máquina",
        branch_id=branch_id,
        manufacturer="Homag",
        model="Sawteq",
        serial_number="123",
    )

    response = machine_client.patch(
        f"/api/v1/machines/{machine['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "branch_id": None,
            "manufacturer": None,
            "model": None,
            "serial_number": None,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["branch_id"] is None
    assert body["manufacturer"] is None
    assert body["model"] is None
    assert body["serial_number"] is None


def test_update_rejects_empty_payload(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Máquina",
    )

    response = machine_client.patch(
        f"/api/v1/machines/{machine['id']}",
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
        "machine_type",
    ],
)
def test_update_rejects_null_required_fields(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
    field: str,
) -> None:
    machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Máquina",
    )

    response = machine_client.patch(
        f"/api/v1/machines/{machine['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            field: None,
        },
    )

    assert response.status_code == 422


def test_update_rejects_duplicate_code(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Primeira",
    )

    second = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-002",
        name="Segunda",
    )

    response = machine_client.patch(
        f"/api/v1/machines/{second['id']}",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "code": "maq-001",
        },
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "resource.conflict"


def test_update_rejects_branch_from_other_tenant(
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

    foreign_branch = create_branch(
        session,
        tenant_id=other_tenant_id,
        code="FIL-OTHER",
        name="Outra filial",
    )

    with override_token_verifier(
        client,
        verifier,
    ):
        machine = create_machine(
            client,
            tenant_id,
            code="MAQ-001",
            name="Máquina",
        )

        response = client.patch(
            f"/api/v1/machines/{machine['id']}",
            headers=authentication_headers(
                tenant_id
            ),
            json={
                "branch_id": str(
                    foreign_branch
                ),
            },
        )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation.error"


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
        machine = create_machine(
            client,
            tenant_id,
            code="MAQ-A",
            name="Tenant A",
        )

        response = client.patch(
            f"/api/v1/machines/{machine['id']}",
            headers=authentication_headers(
                other_tenant_id
            ),
            json={
                "name": "Tentativa indevida",
            },
        )

    assert response.status_code == 404


@pytest.mark.parametrize(
    "machine_status",
    [
        "AVAILABLE",
        "IN_USE",
        "MAINTENANCE",
        "OUT_OF_SERVICE",
    ],
)
def test_change_machine_status(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
    machine_status: str,
) -> None:
    machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Máquina",
    )

    response = machine_client.post(
        f"/api/v1/machines/{machine['id']}/status",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "status": machine_status,
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == machine_status


def test_change_status_rejects_invalid_status(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Máquina",
    )

    response = machine_client.post(
        f"/api/v1/machines/{machine['id']}/status",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "status": "INVALID",
        },
    )

    assert response.status_code == 422

    assert (
        response.json()["error"]["code"]
        == "request.validation_error"
    )


def test_change_status_is_idempotent(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Máquina",
    )

    original_updated_at = machine[
        "updated_at"
    ]

    response = machine_client.post(
        f"/api/v1/machines/{machine['id']}/status",
        headers=authentication_headers(
            tenant_id
        ),
        json={
            "status": "AVAILABLE",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "AVAILABLE"
    assert parse_api_datetime(
        response.json()["updated_at"]
    ) == parse_api_datetime(
        original_updated_at
    )


def test_change_status_is_tenant_scoped(
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
        machine = create_machine(
            client,
            tenant_id,
            code="MAQ-A",
            name="Tenant A",
        )

        response = client.post(
            f"/api/v1/machines/{machine['id']}/status",
            headers=authentication_headers(
                other_tenant_id
            ),
            json={
                "status": "MAINTENANCE",
            },
        )

    assert response.status_code == 404


def test_deactivate_machine(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Máquina",
    )

    response = machine_client.post(
        (
            "/api/v1/machines/"
            f"{machine['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_deactivate_is_idempotent(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Máquina",
    )

    first_response = machine_client.post(
        (
            "/api/v1/machines/"
            f"{machine['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert first_response.status_code == 200

    first_updated_at = first_response.json()[
        "updated_at"
    ]

    second_response = machine_client.post(
        (
            "/api/v1/machines/"
            f"{machine['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert second_response.status_code == 200
    assert second_response.json()["is_active"] is False
    assert parse_api_datetime(
        second_response.json()["updated_at"]
    ) == parse_api_datetime(
        first_updated_at
    )


def test_reactivate_machine(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Máquina",
    )

    deactivate_response = machine_client.post(
        (
            "/api/v1/machines/"
            f"{machine['id']}/deactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert deactivate_response.status_code == 200

    response = machine_client.post(
        (
            "/api/v1/machines/"
            f"{machine['id']}/reactivate"
        ),
        headers=authentication_headers(
            tenant_id
        ),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is True


def test_reactivate_is_idempotent(
    machine_client: TestClient,
    tenant_id: uuid.UUID,
) -> None:
    machine = create_machine(
        machine_client,
        tenant_id,
        code="MAQ-001",
        name="Máquina",
    )

    original_updated_at = machine[
        "updated_at"
    ]

    response = machine_client.post(
        (
            "/api/v1/machines/"
            f"{machine['id']}/reactivate"
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
            "/api/v1/machines",
            MachinePermissions.READ,
        ),
        (
            "get",
            "/api/v1/machines/{machine_id}",
            MachinePermissions.READ,
        ),
        (
            "post",
            "/api/v1/machines",
            MachinePermissions.CREATE,
        ),
        (
            "patch",
            "/api/v1/machines/{machine_id}",
            MachinePermissions.UPDATE,
        ),
        (
            "status",
            "/api/v1/machines/{machine_id}/status",
            MachinePermissions.CHANGE_STATUS,
        ),
        (
            "post",
            "/api/v1/machines/{machine_id}/deactivate",
            MachinePermissions.DEACTIVATE,
        ),
        (
            "post",
            "/api/v1/machines/{machine_id}/reactivate",
            MachinePermissions.REACTIVATE,
        ),
    ],
)
def test_machine_routes_require_permission(
    unauthorized_machine_client: TestClient,
    tenant_id: uuid.UUID,
    method: str,
    path: str,
    permission: str,
) -> None:
    machine_id = uuid.uuid4()

    resolved_path = path.format(
        machine_id=machine_id
    )

    headers = authentication_headers(
        tenant_id
    )

    if method == "get":
        response = unauthorized_machine_client.get(
            resolved_path,
            headers=headers,
        )

    elif method == "patch":
        response = unauthorized_machine_client.patch(
            resolved_path,
            headers=headers,
            json={
                "name": "Atualizada",
            },
        )

    elif method == "status":
        response = unauthorized_machine_client.post(
            resolved_path,
            headers=headers,
            json={
                "status": "MAINTENANCE",
            },
        )

    else:
        payload = None

        if resolved_path == "/api/v1/machines":
            payload = {
                "code": "MAQ-001",
                "name": "Máquina",
                "machine_type": "Tipo",
            }

        response = unauthorized_machine_client.post(
            resolved_path,
            headers=headers,
            json=payload,
        )

    assert_permission_denied(
        response,
        permission,
    )


def test_machine_routes_are_registered(
    client: TestClient,
) -> None:
    """Ensure every public machine operation is in OpenAPI."""

    schema = client.app.openapi()
    paths = schema["paths"]

    expected = {
        "/api/v1/machines": {
            "get",
            "post",
        },
        "/api/v1/machines/{machine_id}": {
            "get",
            "patch",
        },
        "/api/v1/machines/{machine_id}/status": {
            "post",
        },
        "/api/v1/machines/{machine_id}/deactivate": {
            "post",
        },
        "/api/v1/machines/{machine_id}/reactivate": {
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

