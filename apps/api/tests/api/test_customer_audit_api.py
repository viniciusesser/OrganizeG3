"""HTTP audit tests for customer mutations."""

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
    CustomerPermissions,
)
from organizeg3_api.infrastructure.persistence.repositories.audit_event_repository import (
    SQLAlchemyAuditEventRepository,
)

pytestmark = pytest.mark.api


CUSTOMER_PERMISSION_CODES = (
    CustomerPermissions.READ,
    CustomerPermissions.CREATE,
    CustomerPermissions.UPDATE,
    CustomerPermissions.ARCHIVE,
    CustomerPermissions.REACTIVATE,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CustomerAuditClient:
    """Authenticated client plus expected audit actor identifiers."""

    client: TestClient
    user_id: uuid.UUID
    membership_id: uuid.UUID
    auth_user_id: uuid.UUID


@pytest.fixture
def customer_audit_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[CustomerAuditClient]:
    """Provide an authorized customer audit actor."""

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
        permission_codes=CUSTOMER_PERMISSION_CODES,
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
        yield CustomerAuditClient(
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
    """Build authenticated request headers with audit metadata."""

    return {
        **authentication_headers(
            tenant_id
        ),
        "X-Correlation-ID": correlation_id,
        "X-Device-ID": device_id,
    }


def create_customer(
    audit_client: CustomerAuditClient,
    tenant_id: uuid.UUID,
    *,
    correlation_id: str = "corr-customer-create",
    device_id: str = "device-customer-create",
) -> dict[str, object]:
    """Create one customer through the audited API."""

    response = audit_client.client.post(
        "/api/v1/customers",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id=device_id,
        ),
        json={
            "name": "Cliente Teste",
            "customer_type": "INDIVIDUAL",
            "document_number": "529.982.247-25",
            "email": "CLIENTE@EXAMPLE.COM",
            "phone": "+55 (18) 99999-0000",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert isinstance(
        body,
        dict,
    )

    return body


def list_customer_events(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    customer_id: int,
) -> list[AuditEvent]:
    """Return audit history for one customer."""

    return SQLAlchemyAuditEventRepository(
        session
    ).list_for_tenant(
        tenant_id=tenant_id,
        resource="customers",
        resource_id=str(
            customer_id
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
    """Return exactly one event matching an action."""

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


def test_create_customer_records_audit_event(
    customer_audit_client: CustomerAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    correlation_id = "corr-customer-create-001"
    device_id = "device-customer-create-001"

    created = create_customer(
        customer_audit_client,
        tenant_id,
        correlation_id=correlation_id,
        device_id=device_id,
    )

    customer_id = int(
        str(
            created["id"]
        )
    )

    events = list_customer_events(
        session,
        tenant_id=tenant_id,
        customer_id=customer_id,
    )

    assert len(events) == 1

    event = require_event(
        events,
        AuditAction.CREATE,
    )

    assert event.tenant_id == tenant_id
    assert event.resource == "customers"
    assert event.resource_id == str(customer_id)

    assert event.actor_user_id == (
        customer_audit_client.user_id
    )

    assert event.membership_id == (
        customer_audit_client.membership_id
    )

    assert event.auth_user_id == (
        customer_audit_client.auth_user_id
    )

    assert event.correlation_id == correlation_id
    assert event.device_id == device_id
    assert event.before is None

    after = require_snapshot(
        event.after
    )

    assert after["id"] == customer_id

    assert after["tenant_id"] == str(
        tenant_id
    )

    assert after["code"] == created["code"]
    assert after["name"] == "Cliente Teste"
    assert after["customer_type"] == "INDIVIDUAL"
    assert after["is_active"] is True
    assert after["row_version"] == 1


def test_create_customer_redacts_sensitive_fields(
    customer_audit_client: CustomerAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        customer_audit_client,
        tenant_id,
    )

    customer_id = int(
        str(
            created["id"]
        )
    )

    event = require_event(
        list_customer_events(
            session,
            tenant_id=tenant_id,
            customer_id=customer_id,
        ),
        AuditAction.CREATE,
    )

    after = require_snapshot(
        event.after
    )

    assert after["document_number"] != "52998224725"
    assert after["email"] != "cliente@example.com"
    assert after["phone"] != "18999990000"


def test_update_customer_records_before_and_after(
    customer_audit_client: CustomerAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        customer_audit_client,
        tenant_id,
    )

    customer_id = int(
        str(
            created["id"]
        )
    )

    response = customer_audit_client.client.patch(
        f"/api/v1/customers/{customer_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-customer-update",
            device_id="device-customer-update",
        ),
        json={
            "row_version": created["row_version"],
            "name": "Cliente Atualizado",
            "email": None,
        },
    )

    assert response.status_code == 200

    events = list_customer_events(
        session,
        tenant_id=tenant_id,
        customer_id=customer_id,
    )

    assert len(events) == 2

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

    assert before["name"] == "Cliente Teste"
    assert after["name"] == "Cliente Atualizado"

    assert before["email"] is not None
    assert after["email"] is None

    assert before["row_version"] == 1
    assert after["row_version"] == 2

    assert before["id"] == after["id"]
    assert before["tenant_id"] == after["tenant_id"]


def test_update_without_business_change_does_not_create_false_event(
    customer_audit_client: CustomerAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        customer_audit_client,
        tenant_id,
    )

    customer_id = int(
        str(
            created["id"]
        )
    )

    response = customer_audit_client.client.patch(
        f"/api/v1/customers/{customer_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-customer-update-noop",
            device_id="device-customer-update",
        ),
        json={
            "row_version": created["row_version"],
            "name": "Cliente Teste",
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["row_version"]
        == created["row_version"]
    )

    events = list_customer_events(
        session,
        tenant_id=tenant_id,
        customer_id=customer_id,
    )

    assert len(events) == 1


def test_archive_customer_records_audit_event(
    customer_audit_client: CustomerAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        customer_audit_client,
        tenant_id,
    )

    customer_id = int(
        str(
            created["id"]
        )
    )

    correlation_id = "corr-customer-archive"

    response = customer_audit_client.client.post(
        f"/api/v1/customers/{customer_id}/archive",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id="device-customer-archive",
        ),
        json={
            "row_version": created["row_version"],
        },
    )

    assert response.status_code == 200

    event = require_event(
        list_customer_events(
            session,
            tenant_id=tenant_id,
            customer_id=customer_id,
        ),
        AuditAction.ARCHIVE,
    )

    assert event.correlation_id == correlation_id

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["is_active"] is True
    assert before["row_version"] == 1

    assert after["is_active"] is False
    assert after["row_version"] == 2


def test_reactivate_customer_records_audit_event(
    customer_audit_client: CustomerAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        customer_audit_client,
        tenant_id,
    )

    customer_id = int(
        str(
            created["id"]
        )
    )

    archived_response = customer_audit_client.client.post(
        f"/api/v1/customers/{customer_id}/archive",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-before-customer-reactivate",
            device_id="device-customer-archive",
        ),
        json={
            "row_version": created["row_version"],
        },
    )

    assert archived_response.status_code == 200

    archived = archived_response.json()

    response = customer_audit_client.client.post(
        f"/api/v1/customers/{customer_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-customer-reactivate",
            device_id="device-customer-reactivate",
        ),
        json={
            "row_version": archived["row_version"],
        },
    )

    assert response.status_code == 200

    event = require_event(
        list_customer_events(
            session,
            tenant_id=tenant_id,
            customer_id=customer_id,
        ),
        AuditAction.REACTIVATE,
    )

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["is_active"] is False
    assert before["row_version"] == 2

    assert after["is_active"] is True
    assert after["row_version"] == 3


def test_failed_stale_update_does_not_record_audit_event(
    customer_audit_client: CustomerAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        customer_audit_client,
        tenant_id,
    )

    customer_id = int(
        str(
            created["id"]
        )
    )

    first_update = customer_audit_client.client.patch(
        f"/api/v1/customers/{customer_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-customer-first-update",
            device_id="device-customer-update",
        ),
        json={
            "row_version": created["row_version"],
            "name": "Primeira alteração",
        },
    )

    assert first_update.status_code == 200

    events_before = list_customer_events(
        session,
        tenant_id=tenant_id,
        customer_id=customer_id,
    )

    assert len(events_before) == 2

    stale_update = customer_audit_client.client.patch(
        f"/api/v1/customers/{customer_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-customer-stale-update",
            device_id="device-customer-update",
        ),
        json={
            "row_version": created["row_version"],
            "name": "Alteração antiga",
        },
    )

    assert stale_update.status_code == 409

    events_after = list_customer_events(
        session,
        tenant_id=tenant_id,
        customer_id=customer_id,
    )

    assert len(events_after) == 2


def test_invalid_archive_transition_does_not_record_event(
    customer_audit_client: CustomerAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        customer_audit_client,
        tenant_id,
    )

    customer_id = int(
        str(
            created["id"]
        )
    )

    first = customer_audit_client.client.post(
        f"/api/v1/customers/{customer_id}/archive",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-customer-first-archive",
            device_id="device-customer-archive",
        ),
        json={
            "row_version": created["row_version"],
        },
    )

    assert first.status_code == 200

    archived = first.json()

    events_before = list_customer_events(
        session,
        tenant_id=tenant_id,
        customer_id=customer_id,
    )

    assert len(events_before) == 2

    second = customer_audit_client.client.post(
        f"/api/v1/customers/{customer_id}/archive",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-customer-second-archive",
            device_id="device-customer-archive",
        ),
        json={
            "row_version": archived["row_version"],
        },
    )

    assert second.status_code == 409

    events_after = list_customer_events(
        session,
        tenant_id=tenant_id,
        customer_id=customer_id,
    )

    assert len(events_after) == 2


def test_invalid_reactivate_transition_does_not_record_event(
    customer_audit_client: CustomerAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        customer_audit_client,
        tenant_id,
    )

    customer_id = int(
        str(
            created["id"]
        )
    )

    response = customer_audit_client.client.post(
        f"/api/v1/customers/{customer_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-invalid-customer-reactivate",
            device_id="device-customer-reactivate",
        ),
        json={
            "row_version": created["row_version"],
        },
    )

    assert response.status_code == 409

    events = list_customer_events(
        session,
        tenant_id=tenant_id,
        customer_id=customer_id,
    )

    assert len(events) == 1


def test_customer_audit_events_are_tenant_scoped(
    customer_audit_client: CustomerAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    created = create_customer(
        customer_audit_client,
        tenant_id,
    )

    customer_id = int(
        str(
            created["id"]
        )
    )

    own_events = list_customer_events(
        session,
        tenant_id=tenant_id,
        customer_id=customer_id,
    )

    foreign_events = list_customer_events(
        session,
        tenant_id=other_tenant_id,
        customer_id=customer_id,
    )

    assert len(own_events) == 1
    assert foreign_events == []
