"""HTTP audit tests for machine mutations."""

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
    MachinePermissions,
)
from organizeg3_api.infrastructure.persistence.repositories.audit_event_repository import (
    SQLAlchemyAuditEventRepository,
)

pytestmark = pytest.mark.api


MACHINE_PERMISSION_CODES = (
    MachinePermissions.READ,
    MachinePermissions.CREATE,
    MachinePermissions.UPDATE,
    MachinePermissions.CHANGE_STATUS,
    MachinePermissions.DEACTIVATE,
    MachinePermissions.REACTIVATE,
)


@dataclass(
    frozen=True,
    slots=True,
)
class MachineAuditClient:
    """Authenticated API client plus expected audit actor identifiers."""

    client: TestClient
    user_id: uuid.UUID
    membership_id: uuid.UUID
    auth_user_id: uuid.UUID


@pytest.fixture
def machine_audit_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[MachineAuditClient]:
    """Provide one machine actor whose audit identifiers are known."""

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
        yield MachineAuditClient(
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
    """Build authenticated headers with deterministic audit metadata."""

    return {
        **authentication_headers(
            tenant_id
        ),
        "X-Correlation-ID": correlation_id,
        "X-Device-ID": device_id,
    }


def list_machine_events(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    machine_id: uuid.UUID,
) -> list[AuditEvent]:
    """Return audit history for one tenant machine."""

    return SQLAlchemyAuditEventRepository(
        session
    ).list_for_tenant(
        tenant_id=tenant_id,
        resource="machines",
        resource_id=str(
            machine_id
        ),
        limit=100,
        offset=0,
    )


def require_snapshot(
    snapshot: Mapping[str, object] | None,
) -> dict[str, object]:
    """Return one required audit snapshot as a plain mapping."""

    if snapshot is None:
        raise AssertionError(
            "O snapshot de auditoria era obrigatório."
        )

    return dict(
        snapshot
    )


def create_machine(
    audit_client: MachineAuditClient,
    tenant_id: uuid.UUID,
    *,
    correlation_id: str = "corr-machine-create",
    device_id: str = "device-machine-create",
) -> dict[str, object]:
    """Create one machine through the audited public API."""

    response = audit_client.client.post(
        "/api/v1/machines",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id=device_id,
        ),
        json={
            "code": "MAQ-001",
            "name": "Seccionadora",
            "machine_type": "Corte",
            "manufacturer": "Homag",
            "model": "Sawteq",
            "serial_number": "ABC-123",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert isinstance(
        body,
        dict,
    )

    return body


def test_create_machine_records_audit_event(
    machine_audit_client: MachineAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    correlation_id = "corr-machine-create-001"
    device_id = "device-machine-create-001"

    created = create_machine(
        machine_audit_client,
        tenant_id,
        correlation_id=correlation_id,
        device_id=device_id,
    )

    machine_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events = list_machine_events(
        session,
        tenant_id=tenant_id,
        machine_id=machine_id,
    )

    assert len(events) == 1

    event = events[0]

    assert event.action is AuditAction.CREATE
    assert event.tenant_id == tenant_id
    assert event.resource == "machines"
    assert event.resource_id == str(
        machine_id
    )

    assert event.actor_user_id == (
        machine_audit_client.user_id
    )

    assert event.membership_id == (
        machine_audit_client.membership_id
    )

    assert event.auth_user_id == (
        machine_audit_client.auth_user_id
    )

    assert event.correlation_id == correlation_id
    assert event.device_id == device_id
    assert event.before is None

    after = require_snapshot(
        event.after
    )

    assert after["id"] == str(
        machine_id
    )

    assert after["tenant_id"] == str(
        tenant_id
    )

    assert after["code"] == "MAQ-001"
    assert after["name"] == "Seccionadora"
    assert after["machine_type"] == "Corte"
    assert after["status"] == "AVAILABLE"
    assert after["branch_id"] is None
    assert after["manufacturer"] == "Homag"
    assert after["model"] == "Sawteq"
    assert after["serial_number"] == "ABC-123"
    assert after["is_active"] is True


def test_update_machine_records_before_and_after(
    machine_audit_client: MachineAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_machine(
        machine_audit_client,
        tenant_id,
    )

    machine_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    correlation_id = "corr-machine-update-001"

    response = machine_audit_client.client.patch(
        f"/api/v1/machines/{machine_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id="device-machine-update",
        ),
        json={
            "name": "Seccionadora Nova",
            "manufacturer": "Biesse",
            "model": "Selco",
        },
    )

    assert response.status_code == 200

    events = list_machine_events(
        session,
        tenant_id=tenant_id,
        machine_id=machine_id,
    )

    assert len(events) == 2

    event = events[0]

    assert event.action is AuditAction.UPDATE
    assert event.correlation_id == correlation_id

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["name"] == "Seccionadora"
    assert before["manufacturer"] == "Homag"
    assert before["model"] == "Sawteq"

    assert after["name"] == "Seccionadora Nova"
    assert after["manufacturer"] == "Biesse"
    assert after["model"] == "Selco"

    assert before["status"] == "AVAILABLE"
    assert after["status"] == "AVAILABLE"

    assert before["id"] == after["id"]
    assert before["tenant_id"] == after["tenant_id"]


def test_change_machine_status_records_status_change(
    machine_audit_client: MachineAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_machine(
        machine_audit_client,
        tenant_id,
    )

    machine_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    correlation_id = "corr-machine-status-001"

    response = machine_audit_client.client.post(
        f"/api/v1/machines/{machine_id}/status",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id="device-machine-status",
        ),
        json={
            "status": "MAINTENANCE",
        },
    )

    assert response.status_code == 200

    events = list_machine_events(
        session,
        tenant_id=tenant_id,
        machine_id=machine_id,
    )

    assert len(events) == 2

    event = events[0]

    assert event.action is AuditAction.STATUS_CHANGE
    assert event.correlation_id == correlation_id

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["status"] == "AVAILABLE"
    assert after["status"] == "MAINTENANCE"

    assert before["is_active"] is True
    assert after["is_active"] is True


def test_same_machine_status_does_not_create_false_event(
    machine_audit_client: MachineAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_machine(
        machine_audit_client,
        tenant_id,
    )

    machine_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    before_call = list_machine_events(
        session,
        tenant_id=tenant_id,
        machine_id=machine_id,
    )

    assert len(before_call) == 1

    response = machine_audit_client.client.post(
        f"/api/v1/machines/{machine_id}/status",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-machine-status-noop",
            device_id="device-machine-status",
        ),
        json={
            "status": "AVAILABLE",
        },
    )

    assert response.status_code == 200

    after_call = list_machine_events(
        session,
        tenant_id=tenant_id,
        machine_id=machine_id,
    )

    assert len(after_call) == 1


def test_deactivate_machine_records_state_change(
    machine_audit_client: MachineAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_machine(
        machine_audit_client,
        tenant_id,
    )

    machine_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = machine_audit_client.client.post(
        f"/api/v1/machines/{machine_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-machine-deactivate-001",
            device_id="device-machine-deactivate",
        ),
    )

    assert response.status_code == 200

    events = list_machine_events(
        session,
        tenant_id=tenant_id,
        machine_id=machine_id,
    )

    assert len(events) == 2

    event = events[0]

    assert event.action is AuditAction.DEACTIVATE

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["is_active"] is True
    assert after["is_active"] is False


def test_repeated_deactivate_does_not_create_false_event(
    machine_audit_client: MachineAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_machine(
        machine_audit_client,
        tenant_id,
    )

    machine_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    first_response = machine_audit_client.client.post(
        f"/api/v1/machines/{machine_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-machine-deactivate-first",
            device_id="device-machine-deactivate",
        ),
    )

    assert first_response.status_code == 200

    events_before_second = list_machine_events(
        session,
        tenant_id=tenant_id,
        machine_id=machine_id,
    )

    assert len(events_before_second) == 2

    second_response = machine_audit_client.client.post(
        f"/api/v1/machines/{machine_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-machine-deactivate-second",
            device_id="device-machine-deactivate",
        ),
    )

    assert second_response.status_code == 200

    events_after_second = list_machine_events(
        session,
        tenant_id=tenant_id,
        machine_id=machine_id,
    )

    assert len(events_after_second) == 2


def test_reactivate_machine_records_state_change(
    machine_audit_client: MachineAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_machine(
        machine_audit_client,
        tenant_id,
    )

    machine_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    deactivate_response = machine_audit_client.client.post(
        f"/api/v1/machines/{machine_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-machine-before-reactivate",
            device_id="device-machine-deactivate",
        ),
    )

    assert deactivate_response.status_code == 200

    response = machine_audit_client.client.post(
        f"/api/v1/machines/{machine_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-machine-reactivate-001",
            device_id="device-machine-reactivate",
        ),
    )

    assert response.status_code == 200

    events = list_machine_events(
        session,
        tenant_id=tenant_id,
        machine_id=machine_id,
    )

    assert len(events) == 3

    event = events[0]

    assert event.action is AuditAction.REACTIVATE

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["is_active"] is False
    assert after["is_active"] is True


def test_reactivate_active_machine_does_not_create_false_event(
    machine_audit_client: MachineAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_machine(
        machine_audit_client,
        tenant_id,
    )

    machine_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    before_call = list_machine_events(
        session,
        tenant_id=tenant_id,
        machine_id=machine_id,
    )

    assert len(before_call) == 1

    response = machine_audit_client.client.post(
        f"/api/v1/machines/{machine_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-machine-reactivate-noop",
            device_id="device-machine-reactivate",
        ),
    )

    assert response.status_code == 200

    after_call = list_machine_events(
        session,
        tenant_id=tenant_id,
        machine_id=machine_id,
    )

    assert len(after_call) == 1


def test_machine_audit_events_are_tenant_scoped(
    machine_audit_client: MachineAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    created = create_machine(
        machine_audit_client,
        tenant_id,
    )

    machine_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    own_events = list_machine_events(
        session,
        tenant_id=tenant_id,
        machine_id=machine_id,
    )

    foreign_events = list_machine_events(
        session,
        tenant_id=other_tenant_id,
        machine_id=machine_id,
    )

    assert len(own_events) == 1
    assert foreign_events == []
