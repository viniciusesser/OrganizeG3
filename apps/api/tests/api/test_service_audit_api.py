"""HTTP audit tests for service mutations."""

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
    ServicePermissions,
)
from organizeg3_api.infrastructure.persistence.repositories.audit_event_repository import (
    SQLAlchemyAuditEventRepository,
)

pytestmark = pytest.mark.api


SERVICE_PERMISSION_CODES = (
    ServicePermissions.READ,
    ServicePermissions.CREATE,
    ServicePermissions.UPDATE,
    ServicePermissions.DEACTIVATE,
    ServicePermissions.REACTIVATE,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ServiceAuditClient:
    """Authenticated API client plus expected audit actor identifiers."""

    client: TestClient
    user_id: uuid.UUID
    membership_id: uuid.UUID
    auth_user_id: uuid.UUID


@pytest.fixture
def service_audit_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[ServiceAuditClient]:
    """Provide one authorized actor with known audit identifiers."""

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
        yield ServiceAuditClient(
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


def list_service_events(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    service_id: uuid.UUID,
) -> list[AuditEvent]:
    """Return audit history for one tenant service."""

    return SQLAlchemyAuditEventRepository(
        session
    ).list_for_tenant(
        tenant_id=tenant_id,
        resource="services",
        resource_id=str(
            service_id
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


def require_event(
    events: list[AuditEvent],
    action: AuditAction,
) -> AuditEvent:
    """Return the single audit event matching the requested action."""

    matches = [
        event
        for event in events
        if event.action is action
    ]

    if len(matches) != 1:
        raise AssertionError(
            "Era esperado exatamente um evento "
            f"de auditoria {action.value}."
        )

    return matches[0]


def create_service(
    audit_client: ServiceAuditClient,
    tenant_id: uuid.UUID,
    *,
    correlation_id: str = "corr-service-create",
    device_id: str = "device-service-create",
) -> dict[str, object]:
    """Create one service through the audited public API."""

    response = audit_client.client.post(
        "/api/v1/services",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id=device_id,
        ),
        json={
            "code": "SERV-001",
            "name": "Corte de MDF",
            "category": "Corte",
            "unit": "H",
            "execution_mode": "INTERNAL",
            "estimated_duration_minutes": 45,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert isinstance(
        body,
        dict,
    )

    return body


def test_create_service_records_audit_event(
    service_audit_client: ServiceAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    correlation_id = "corr-service-create-001"
    device_id = "device-service-create-001"

    created = create_service(
        service_audit_client,
        tenant_id,
        correlation_id=correlation_id,
        device_id=device_id,
    )

    service_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events = list_service_events(
        session,
        tenant_id=tenant_id,
        service_id=service_id,
    )

    assert len(events) == 1

    event = require_event(
        events,
        AuditAction.CREATE,
    )

    assert event.tenant_id == tenant_id
    assert event.resource == "services"
    assert event.resource_id == str(
        service_id
    )

    assert event.actor_user_id == (
        service_audit_client.user_id
    )

    assert event.membership_id == (
        service_audit_client.membership_id
    )

    assert event.auth_user_id == (
        service_audit_client.auth_user_id
    )

    assert event.correlation_id == correlation_id
    assert event.device_id == device_id
    assert event.before is None

    after = require_snapshot(
        event.after
    )

    assert after["id"] == str(
        service_id
    )

    assert after["tenant_id"] == str(
        tenant_id
    )

    assert after["code"] == "SERV-001"
    assert after["name"] == "Corte de MDF"
    assert after["category"] == "Corte"
    assert after["unit"] == "H"
    assert after["execution_mode"] == "INTERNAL"
    assert after["estimated_duration_minutes"] == 45
    assert after["is_active"] is True


def test_update_service_records_before_and_after(
    service_audit_client: ServiceAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_service(
        service_audit_client,
        tenant_id,
    )

    service_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    correlation_id = "corr-service-update-001"
    device_id = "device-service-update-001"

    response = service_audit_client.client.patch(
        f"/api/v1/services/{service_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id=device_id,
        ),
        json={
            "name": "Montagem",
            "category": "Produção",
            "unit": "UN",
            "execution_mode": "BOTH",
            "estimated_duration_minutes": 90,
        },
    )

    assert response.status_code == 200

    events = list_service_events(
        session,
        tenant_id=tenant_id,
        service_id=service_id,
    )

    assert len(events) == 2

    event = require_event(
        events,
        AuditAction.UPDATE,
    )

    assert event.correlation_id == correlation_id
    assert event.device_id == device_id

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["name"] == "Corte de MDF"
    assert before["category"] == "Corte"
    assert before["unit"] == "H"
    assert before["execution_mode"] == "INTERNAL"
    assert before["estimated_duration_minutes"] == 45

    assert after["name"] == "Montagem"
    assert after["category"] == "Produção"
    assert after["unit"] == "UN"
    assert after["execution_mode"] == "BOTH"
    assert after["estimated_duration_minutes"] == 90

    assert before["id"] == after["id"]
    assert before["tenant_id"] == after["tenant_id"]
    assert before["is_active"] is True
    assert after["is_active"] is True


def test_update_service_can_audit_cleared_duration(
    service_audit_client: ServiceAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_service(
        service_audit_client,
        tenant_id,
    )

    service_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = service_audit_client.client.patch(
        f"/api/v1/services/{service_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-service-clear-duration",
            device_id="device-service-update",
        ),
        json={
            "estimated_duration_minutes": None,
        },
    )

    assert response.status_code == 200

    events = list_service_events(
        session,
        tenant_id=tenant_id,
        service_id=service_id,
    )

    event = require_event(
        events,
        AuditAction.UPDATE,
    )

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["estimated_duration_minutes"] == 45
    assert after["estimated_duration_minutes"] is None


def test_update_without_business_change_does_not_create_false_event(
    service_audit_client: ServiceAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_service(
        service_audit_client,
        tenant_id,
    )

    service_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_service_events(
        session,
        tenant_id=tenant_id,
        service_id=service_id,
    )

    assert len(events_before) == 1

    response = service_audit_client.client.patch(
        f"/api/v1/services/{service_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-service-update-noop",
            device_id="device-service-update",
        ),
        json={
            "name": "Corte de MDF",
        },
    )

    assert response.status_code == 200

    events_after = list_service_events(
        session,
        tenant_id=tenant_id,
        service_id=service_id,
    )

    assert len(events_after) == 1


def test_deactivate_service_records_state_change(
    service_audit_client: ServiceAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_service(
        service_audit_client,
        tenant_id,
    )

    service_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    correlation_id = "corr-service-deactivate-001"

    response = service_audit_client.client.post(
        f"/api/v1/services/{service_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id="device-service-deactivate",
        ),
    )

    assert response.status_code == 200

    events = list_service_events(
        session,
        tenant_id=tenant_id,
        service_id=service_id,
    )

    assert len(events) == 2

    event = require_event(
        events,
        AuditAction.DEACTIVATE,
    )

    assert event.correlation_id == correlation_id

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["is_active"] is True
    assert after["is_active"] is False


def test_repeated_deactivate_does_not_create_false_event(
    service_audit_client: ServiceAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_service(
        service_audit_client,
        tenant_id,
    )

    service_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    first_response = service_audit_client.client.post(
        f"/api/v1/services/{service_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-service-deactivate-first",
            device_id="device-service-deactivate",
        ),
    )

    assert first_response.status_code == 200

    events_before_second = list_service_events(
        session,
        tenant_id=tenant_id,
        service_id=service_id,
    )

    assert len(events_before_second) == 2

    second_response = service_audit_client.client.post(
        f"/api/v1/services/{service_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-service-deactivate-second",
            device_id="device-service-deactivate",
        ),
    )

    assert second_response.status_code == 200

    events_after_second = list_service_events(
        session,
        tenant_id=tenant_id,
        service_id=service_id,
    )

    assert len(events_after_second) == 2


def test_reactivate_service_records_state_change(
    service_audit_client: ServiceAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_service(
        service_audit_client,
        tenant_id,
    )

    service_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    deactivate_response = service_audit_client.client.post(
        f"/api/v1/services/{service_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-service-before-reactivate",
            device_id="device-service-deactivate",
        ),
    )

    assert deactivate_response.status_code == 200

    correlation_id = "corr-service-reactivate-001"

    response = service_audit_client.client.post(
        f"/api/v1/services/{service_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id="device-service-reactivate",
        ),
    )

    assert response.status_code == 200

    events = list_service_events(
        session,
        tenant_id=tenant_id,
        service_id=service_id,
    )

    assert len(events) == 3

    event = require_event(
        events,
        AuditAction.REACTIVATE,
    )

    assert event.correlation_id == correlation_id

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["is_active"] is False
    assert after["is_active"] is True


def test_reactivate_active_service_does_not_create_false_event(
    service_audit_client: ServiceAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_service(
        service_audit_client,
        tenant_id,
    )

    service_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_service_events(
        session,
        tenant_id=tenant_id,
        service_id=service_id,
    )

    assert len(events_before) == 1

    response = service_audit_client.client.post(
        f"/api/v1/services/{service_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-service-reactivate-noop",
            device_id="device-service-reactivate",
        ),
    )

    assert response.status_code == 200

    events_after = list_service_events(
        session,
        tenant_id=tenant_id,
        service_id=service_id,
    )

    assert len(events_after) == 1


def test_service_audit_events_are_tenant_scoped(
    service_audit_client: ServiceAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    created = create_service(
        service_audit_client,
        tenant_id,
    )

    service_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    own_events = list_service_events(
        session,
        tenant_id=tenant_id,
        service_id=service_id,
    )

    foreign_events = list_service_events(
        session,
        tenant_id=other_tenant_id,
        service_id=service_id,
    )

    assert len(own_events) == 1
    assert foreign_events == []
