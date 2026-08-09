"""HTTP audit tests for employee mutations."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
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

from organizeg3_api.domain.audit import (
    AuditAction,
    AuditEvent,
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
from organizeg3_api.infrastructure.persistence.repositories.audit_event_repository import (
    SQLAlchemyAuditEventRepository,
)

pytestmark = pytest.mark.api


EMPLOYEE_PERMISSION_CODES = (
    EmployeePermissions.READ,
    EmployeePermissions.CREATE,
    EmployeePermissions.UPDATE,
    EmployeePermissions.DEACTIVATE,
    EmployeePermissions.REACTIVATE,
)


@dataclass(
    frozen=True,
    slots=True,
)
class EmployeeAuditClient:
    """Authenticated client plus expected audit actor identifiers."""

    client: TestClient
    user_id: uuid.UUID
    membership_id: uuid.UUID
    auth_user_id: uuid.UUID


@pytest.fixture
def employee_audit_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[EmployeeAuditClient]:
    """Provide one authorized employee audit actor."""

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
        yield EmployeeAuditClient(
            client=client,
            user_id=user.id,
            membership_id=membership.id,
            auth_user_id=auth_user_id,
        )


def audit_headers(
    tenant_id: uuid.UUID,
    *,
    correlation_id: str,
    device_id: str,
) -> dict[str, str]:
    """Build authenticated headers carrying audit metadata."""

    return {
        **authentication_headers(
            tenant_id
        ),
        "X-Correlation-ID": correlation_id,
        "X-Device-ID": device_id,
    }


def create_branch(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "MATRIZ",
) -> BranchModel:
    """Create one active tenant branch."""

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
    audit_client: EmployeeAuditClient,
    tenant_id: uuid.UUID,
    *,
    branch_id: uuid.UUID | None = None,
    correlation_id: str = "corr-employee-create",
    device_id: str = "device-employee-create",
) -> dict[str, object]:
    """Create one employee through the audited API."""

    payload: dict[str, object] = {
        "code": "FUNC-001",
        "full_name": "Funcionário Teste",
        "document_number": "529.982.247-25",
        "email": "FUNCIONARIO@EXAMPLE.COM",
        "phone": "(18) 99999-1234",
        "job_title": "Marceneiro",
        "contract_type": "CLT",
        "birth_date": "1990-01-01",
        "admission_date": "2025-01-10",
    }

    if branch_id is not None:
        payload["branch_id"] = str(
            branch_id
        )

    response = audit_client.client.post(
        "/api/v1/employees",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id=device_id,
        ),
        json=payload,
    )

    assert response.status_code == 201

    body = response.json()

    assert isinstance(
        body,
        dict,
    )

    return body


def list_employee_events(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    employee_id: uuid.UUID,
) -> list[AuditEvent]:
    """Return audit events for one employee."""

    return SQLAlchemyAuditEventRepository(
        session
    ).list_for_tenant(
        tenant_id=tenant_id,
        resource="employees",
        resource_id=str(
            employee_id
        ),
        limit=100,
        offset=0,
    )


def require_snapshot(
    snapshot: Mapping[str, object] | None,
) -> dict[str, object]:
    """Return a required audit snapshot."""

    if snapshot is None:
        raise AssertionError(
            "O snapshot de auditoria era obrigatório."
        )

    return dict(
        snapshot
    )


def require_event(
    events: list[AuditEvent],
    action: AuditAction,
) -> AuditEvent:
    """Return exactly one event of an audit action."""

    matches = [
        event
        for event in events
        if event.action is action
    ]

    if len(matches) != 1:
        raise AssertionError(
            "Era esperado exatamente um evento "
            f"{action.value}."
        )

    return matches[0]


def test_create_employee_records_audit_event(
    employee_audit_client: EmployeeAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    branch = create_branch(
        session,
        tenant_id=tenant_id,
    )

    correlation_id = "corr-employee-create-001"
    device_id = "device-employee-create-001"

    created = create_employee(
        employee_audit_client,
        tenant_id,
        branch_id=branch.id,
        correlation_id=correlation_id,
        device_id=device_id,
    )

    employee_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events = list_employee_events(
        session,
        tenant_id=tenant_id,
        employee_id=employee_id,
    )

    assert len(events) == 1

    event = require_event(
        events,
        AuditAction.CREATE,
    )

    assert event.tenant_id == tenant_id
    assert event.resource == "employees"

    assert event.resource_id == str(
        employee_id
    )

    assert event.actor_user_id == (
        employee_audit_client.user_id
    )

    assert event.membership_id == (
        employee_audit_client.membership_id
    )

    assert event.auth_user_id == (
        employee_audit_client.auth_user_id
    )

    assert event.correlation_id == correlation_id
    assert event.device_id == device_id
    assert event.before is None

    after = require_snapshot(
        event.after
    )

    assert after["id"] == str(
        employee_id
    )

    assert after["tenant_id"] == str(
        tenant_id
    )

    assert after["branch_id"] == str(
        branch.id
    )

    assert after["code"] == "FUNC-001"
    assert after["full_name"] == "Funcionário Teste"
    assert after["job_title"] == "Marceneiro"
    assert after["contract_type"] == "CLT"
    assert after["status"] == "ACTIVE"
    assert after["birth_date"] == "1990-01-01"
    assert after["admission_date"] == "2025-01-10"
    assert after["termination_date"] is None
    assert after["is_active"] is True


def test_create_employee_redacts_sensitive_fields(
    employee_audit_client: EmployeeAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_employee(
        employee_audit_client,
        tenant_id,
    )

    employee_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    event = require_event(
        list_employee_events(
            session,
            tenant_id=tenant_id,
            employee_id=employee_id,
        ),
        AuditAction.CREATE,
    )

    after = require_snapshot(
        event.after
    )

    assert after["document_number"] != "52998224725"
    assert after["email"] != "funcionario@example.com"
    assert after["phone"] != "18999991234"


def test_update_employee_records_before_and_after(
    employee_audit_client: EmployeeAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_employee(
        employee_audit_client,
        tenant_id,
    )

    employee_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = employee_audit_client.client.patch(
        f"/api/v1/employees/{employee_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-employee-update",
            device_id="device-employee-update",
        ),
        json={
            "code": "FUNC-002",
            "full_name": "Nome Atualizado",
            "job_title": "Projetista",
            "contract_type": "PJ",
        },
    )

    assert response.status_code == 200

    event = require_event(
        list_employee_events(
            session,
            tenant_id=tenant_id,
            employee_id=employee_id,
        ),
        AuditAction.UPDATE,
    )

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["code"] == "FUNC-001"
    assert before["full_name"] == "Funcionário Teste"
    assert before["job_title"] == "Marceneiro"
    assert before["contract_type"] == "CLT"

    assert after["code"] == "FUNC-002"
    assert after["full_name"] == "Nome Atualizado"
    assert after["job_title"] == "Projetista"
    assert after["contract_type"] == "PJ"

    assert before["id"] == after["id"]
    assert before["tenant_id"] == after["tenant_id"]


def test_update_employee_records_branch_change(
    employee_audit_client: EmployeeAuditClient,
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

    created = create_employee(
        employee_audit_client,
        tenant_id,
        branch_id=branch_a.id,
    )

    employee_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = employee_audit_client.client.patch(
        f"/api/v1/employees/{employee_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-employee-branch",
            device_id="device-employee-update",
        ),
        json={
            "branch_id": str(
                branch_b.id
            ),
        },
    )

    assert response.status_code == 200

    event = require_event(
        list_employee_events(
            session,
            tenant_id=tenant_id,
            employee_id=employee_id,
        ),
        AuditAction.UPDATE,
    )

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["branch_id"] == str(
        branch_a.id
    )

    assert after["branch_id"] == str(
        branch_b.id
    )


def test_update_employee_can_clear_optional_fields(
    employee_audit_client: EmployeeAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    branch = create_branch(
        session,
        tenant_id=tenant_id,
    )

    created = create_employee(
        employee_audit_client,
        tenant_id,
        branch_id=branch.id,
    )

    employee_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = employee_audit_client.client.patch(
        f"/api/v1/employees/{employee_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-employee-clear",
            device_id="device-employee-update",
        ),
        json={
            "branch_id": None,
            "email": None,
            "phone": None,
            "job_title": None,
        },
    )

    assert response.status_code == 200

    event = require_event(
        list_employee_events(
            session,
            tenant_id=tenant_id,
            employee_id=employee_id,
        ),
        AuditAction.UPDATE,
    )

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["branch_id"] == str(
        branch.id
    )

    assert after["branch_id"] is None
    assert after["email"] is None
    assert after["phone"] is None
    assert after["job_title"] is None


def test_update_without_business_change_does_not_create_false_event(
    employee_audit_client: EmployeeAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_employee(
        employee_audit_client,
        tenant_id,
    )

    employee_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_employee_events(
        session,
        tenant_id=tenant_id,
        employee_id=employee_id,
    )

    assert len(events_before) == 1

    response = employee_audit_client.client.patch(
        f"/api/v1/employees/{employee_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-employee-noop",
            device_id="device-employee-update",
        ),
        json={
            "full_name": "Funcionário Teste",
        },
    )

    assert response.status_code == 200

    events_after = list_employee_events(
        session,
        tenant_id=tenant_id,
        employee_id=employee_id,
    )

    assert len(events_after) == 1


def test_deactivate_employee_records_status_and_active_change(
    employee_audit_client: EmployeeAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_employee(
        employee_audit_client,
        tenant_id,
    )

    employee_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = employee_audit_client.client.post(
        f"/api/v1/employees/{employee_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-employee-deactivate",
            device_id="device-employee-deactivate",
        ),
    )

    assert response.status_code == 200

    event = require_event(
        list_employee_events(
            session,
            tenant_id=tenant_id,
            employee_id=employee_id,
        ),
        AuditAction.DEACTIVATE,
    )

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["status"] == "ACTIVE"
    assert before["is_active"] is True

    assert after["status"] == "INACTIVE"
    assert after["is_active"] is False


def test_repeated_deactivate_does_not_create_false_event(
    employee_audit_client: EmployeeAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_employee(
        employee_audit_client,
        tenant_id,
    )

    employee_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    url = (
        f"/api/v1/employees/{employee_id}/deactivate"
    )

    first = employee_audit_client.client.post(
        url,
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-employee-deactivate-first",
            device_id="device-employee-deactivate",
        ),
    )

    assert first.status_code == 200

    events_before_second = list_employee_events(
        session,
        tenant_id=tenant_id,
        employee_id=employee_id,
    )

    assert len(events_before_second) == 2

    second = employee_audit_client.client.post(
        url,
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-employee-deactivate-second",
            device_id="device-employee-deactivate",
        ),
    )

    assert second.status_code == 200

    events_after_second = list_employee_events(
        session,
        tenant_id=tenant_id,
        employee_id=employee_id,
    )

    assert len(events_after_second) == 2


def test_reactivate_employee_records_status_and_active_change(
    employee_audit_client: EmployeeAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_employee(
        employee_audit_client,
        tenant_id,
    )

    employee_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    deactivate = employee_audit_client.client.post(
        f"/api/v1/employees/{employee_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-before-reactivate",
            device_id="device-employee-deactivate",
        ),
    )

    assert deactivate.status_code == 200

    response = employee_audit_client.client.post(
        f"/api/v1/employees/{employee_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-employee-reactivate",
            device_id="device-employee-reactivate",
        ),
    )

    assert response.status_code == 200

    event = require_event(
        list_employee_events(
            session,
            tenant_id=tenant_id,
            employee_id=employee_id,
        ),
        AuditAction.REACTIVATE,
    )

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["status"] == "INACTIVE"
    assert before["is_active"] is False

    assert after["status"] == "ACTIVE"
    assert after["is_active"] is True


def test_reactivate_active_employee_does_not_create_false_event(
    employee_audit_client: EmployeeAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_employee(
        employee_audit_client,
        tenant_id,
    )

    employee_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_employee_events(
        session,
        tenant_id=tenant_id,
        employee_id=employee_id,
    )

    assert len(events_before) == 1

    response = employee_audit_client.client.post(
        f"/api/v1/employees/{employee_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-employee-reactivate-noop",
            device_id="device-employee-reactivate",
        ),
    )

    assert response.status_code == 200

    events_after = list_employee_events(
        session,
        tenant_id=tenant_id,
        employee_id=employee_id,
    )

    assert len(events_after) == 1


def test_employee_audit_events_are_tenant_scoped(
    employee_audit_client: EmployeeAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    created = create_employee(
        employee_audit_client,
        tenant_id,
    )

    employee_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    own_events = list_employee_events(
        session,
        tenant_id=tenant_id,
        employee_id=employee_id,
    )

    foreign_events = list_employee_events(
        session,
        tenant_id=other_tenant_id,
        employee_id=employee_id,
    )

    assert len(own_events) == 1
    assert foreign_events == []
