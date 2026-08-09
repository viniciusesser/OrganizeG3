"""HTTP audit tests for brand mutations."""

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
    BrandPermissions,
)
from organizeg3_api.infrastructure.persistence.repositories.audit_event_repository import (
    SQLAlchemyAuditEventRepository,
)

pytestmark = pytest.mark.api


BRAND_PERMISSION_CODES = (
    BrandPermissions.READ,
    BrandPermissions.CREATE,
    BrandPermissions.UPDATE,
    BrandPermissions.DEACTIVATE,
    BrandPermissions.REACTIVATE,
)


@dataclass(
    frozen=True,
    slots=True,
)
class BrandAuditClient:
    """Authenticated API client plus expected audit actor identifiers."""

    client: TestClient
    user_id: uuid.UUID
    membership_id: uuid.UUID
    auth_user_id: uuid.UUID


@pytest.fixture
def brand_audit_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[BrandAuditClient]:
    """Provide a fully authorized actor whose identifiers are known."""

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
        yield BrandAuditClient(
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


def list_brand_events(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    brand_id: uuid.UUID,
) -> list[AuditEvent]:
    """Return all persisted audit events for one brand."""

    return SQLAlchemyAuditEventRepository(
        session
    ).list_for_tenant(
        tenant_id=tenant_id,
        resource="brands",
        resource_id=str(
            brand_id
        ),
        limit=100,
        offset=0,
    )


def require_snapshot(
    snapshot: Mapping[str, object] | None,
) -> dict[str, object]:
    """Return one audit snapshot as a plain mutable mapping."""

    if snapshot is None:
        raise AssertionError(
            "O snapshot de auditoria era obrigatório."
        )

    return dict(
        snapshot
    )


def create_brand(
    audit_client: BrandAuditClient,
    tenant_id: uuid.UUID,
    *,
    code: str = "MARCA-001",
    name: str = "Duratex",
    correlation_id: str = "corr-brand-create",
    device_id: str = "device-brand-create",
) -> dict[str, object]:
    """Create one brand through the audited public API."""

    response = audit_client.client.post(
        "/api/v1/brands",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id=device_id,
        ),
        json={
            "code": code,
            "name": name,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert isinstance(
        body,
        dict,
    )

    return body


def test_create_brand_records_audit_event(
    brand_audit_client: BrandAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    correlation_id = "corr-brand-create-001"
    device_id = "device-brand-create-001"

    created = create_brand(
        brand_audit_client,
        tenant_id,
        correlation_id=correlation_id,
        device_id=device_id,
    )

    brand_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events = list_brand_events(
        session,
        tenant_id=tenant_id,
        brand_id=brand_id,
    )

    assert len(events) == 1

    event = events[0]

    assert event.action is AuditAction.CREATE
    assert event.tenant_id == tenant_id
    assert event.resource == "brands"
    assert event.resource_id == str(
        brand_id
    )

    assert event.actor_user_id == (
        brand_audit_client.user_id
    )

    assert event.membership_id == (
        brand_audit_client.membership_id
    )

    assert event.auth_user_id == (
        brand_audit_client.auth_user_id
    )

    assert event.correlation_id == correlation_id
    assert event.device_id == device_id

    assert event.before is None

    after = require_snapshot(
        event.after
    )

    assert after["id"] == str(
        brand_id
    )

    assert after["tenant_id"] == str(
        tenant_id
    )

    assert after["code"] == "MARCA-001"
    assert after["name"] == "Duratex"
    assert after["is_active"] is True


def test_update_brand_records_before_and_after(
    brand_audit_client: BrandAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_brand(
        brand_audit_client,
        tenant_id,
    )

    brand_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    correlation_id = "corr-brand-update-001"
    device_id = "device-brand-update-001"

    response = brand_audit_client.client.patch(
        f"/api/v1/brands/{brand_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id=device_id,
        ),
        json={
            "code": "MARCA-002",
            "name": "Arauco",
        },
    )

    assert response.status_code == 200

    events = list_brand_events(
        session,
        tenant_id=tenant_id,
        brand_id=brand_id,
    )

    assert len(events) == 2

    event = events[0]

    assert event.action is AuditAction.UPDATE
    assert event.correlation_id == correlation_id
    assert event.device_id == device_id

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["code"] == "MARCA-001"
    assert before["name"] == "Duratex"
    assert before["is_active"] is True

    assert after["code"] == "MARCA-002"
    assert after["name"] == "Arauco"
    assert after["is_active"] is True

    assert before["id"] == after["id"]
    assert before["tenant_id"] == after["tenant_id"]


def test_deactivate_brand_records_state_change(
    brand_audit_client: BrandAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_brand(
        brand_audit_client,
        tenant_id,
    )

    brand_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    correlation_id = "corr-brand-deactivate-001"

    response = brand_audit_client.client.post(
        f"/api/v1/brands/{brand_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id="device-brand-deactivate",
        ),
    )

    assert response.status_code == 200

    events = list_brand_events(
        session,
        tenant_id=tenant_id,
        brand_id=brand_id,
    )

    assert len(events) == 2

    event = events[0]

    assert event.action is AuditAction.DEACTIVATE
    assert event.correlation_id == correlation_id

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["is_active"] is True
    assert after["is_active"] is False


def test_reactivate_brand_records_state_change(
    brand_audit_client: BrandAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_brand(
        brand_audit_client,
        tenant_id,
    )

    brand_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    deactivate_response = (
        brand_audit_client.client.post(
            f"/api/v1/brands/{brand_id}/deactivate",
            headers=audit_headers(
                tenant_id,
                correlation_id=(
                    "corr-brand-deactivate-before-reactivate"
                ),
                device_id="device-brand-deactivate",
            ),
        )
    )

    assert deactivate_response.status_code == 200

    correlation_id = "corr-brand-reactivate-001"

    response = brand_audit_client.client.post(
        f"/api/v1/brands/{brand_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id="device-brand-reactivate",
        ),
    )

    assert response.status_code == 200

    events = list_brand_events(
        session,
        tenant_id=tenant_id,
        brand_id=brand_id,
    )

    assert len(events) == 3

    event = events[0]

    assert event.action is AuditAction.REACTIVATE
    assert event.correlation_id == correlation_id

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["is_active"] is False
    assert after["is_active"] is True


def test_repeated_deactivate_does_not_create_false_event(
    brand_audit_client: BrandAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_brand(
        brand_audit_client,
        tenant_id,
    )

    brand_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    first_response = brand_audit_client.client.post(
        f"/api/v1/brands/{brand_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-brand-deactivate-first",
            device_id="device-brand-deactivate",
        ),
    )

    assert first_response.status_code == 200

    before_second_call = list_brand_events(
        session,
        tenant_id=tenant_id,
        brand_id=brand_id,
    )

    assert len(before_second_call) == 2

    second_response = brand_audit_client.client.post(
        f"/api/v1/brands/{brand_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-brand-deactivate-second",
            device_id="device-brand-deactivate",
        ),
    )

    assert second_response.status_code == 200

    after_second_call = list_brand_events(
        session,
        tenant_id=tenant_id,
        brand_id=brand_id,
    )

    assert len(after_second_call) == 2


def test_reactivate_already_active_brand_does_not_create_false_event(
    brand_audit_client: BrandAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_brand(
        brand_audit_client,
        tenant_id,
    )

    brand_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_brand_events(
        session,
        tenant_id=tenant_id,
        brand_id=brand_id,
    )

    assert len(events_before) == 1

    response = brand_audit_client.client.post(
        f"/api/v1/brands/{brand_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-brand-reactivate-noop",
            device_id="device-brand-reactivate",
        ),
    )

    assert response.status_code == 200

    events_after = list_brand_events(
        session,
        tenant_id=tenant_id,
        brand_id=brand_id,
    )

    assert len(events_after) == 1


def test_brand_audit_events_are_tenant_scoped(
    brand_audit_client: BrandAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    created = create_brand(
        brand_audit_client,
        tenant_id,
    )

    brand_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    own_events = list_brand_events(
        session,
        tenant_id=tenant_id,
        brand_id=brand_id,
    )

    foreign_events = list_brand_events(
        session,
        tenant_id=other_tenant_id,
        brand_id=brand_id,
    )

    assert len(own_events) == 1
    assert foreign_events == []
