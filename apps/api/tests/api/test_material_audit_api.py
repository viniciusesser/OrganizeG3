"""HTTP audit tests for material mutations."""

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
from organizeg3_api.infrastructure.persistence.repositories.audit_event_repository import (
    SQLAlchemyAuditEventRepository,
)

pytestmark = pytest.mark.api


MATERIAL_PERMISSION_CODES = (
    MaterialPermissions.READ,
    MaterialPermissions.CREATE,
    MaterialPermissions.UPDATE,
    MaterialPermissions.DEACTIVATE,
    MaterialPermissions.REACTIVATE,
)


@dataclass(
    frozen=True,
    slots=True,
)
class MaterialAuditClient:
    """Authenticated client plus expected audit actor identifiers."""

    client: TestClient
    user_id: uuid.UUID
    membership_id: uuid.UUID
    auth_user_id: uuid.UUID


@pytest.fixture
def material_audit_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[MaterialAuditClient]:
    """Provide one authorized material actor."""

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
        yield MaterialAuditClient(
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
    """Build authentication and audit request headers."""

    return {
        **authentication_headers(
            tenant_id
        ),
        "X-Correlation-ID": correlation_id,
        "X-Device-ID": device_id,
    }


def create_brand(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    code: str = "MARCA-001",
    name: str = "Duratex",
) -> uuid.UUID:
    """Persist one brand for material audit tests."""

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

    if brand.id is None:
        raise AssertionError(
            "A marca de teste deveria possuir identificador."
        )

    return brand.id


def create_material(
    audit_client: MaterialAuditClient,
    tenant_id: uuid.UUID,
    *,
    brand_id: uuid.UUID | None = None,
    correlation_id: str = "corr-material-create",
    device_id: str = "device-material-create",
) -> dict[str, object]:
    """Create one material through the audited API."""

    payload: dict[str, object] = {
        "code": "MAT-001",
        "name": "MDF Branco TX 15mm",
        "category": "Chapas",
        "unit": "CHAPA",
    }

    if brand_id is not None:
        payload["brand_id"] = str(
            brand_id
        )

    response = audit_client.client.post(
        "/api/v1/materials",
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


def list_material_events(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    material_id: uuid.UUID,
) -> list[AuditEvent]:
    """Return audit history for one material."""

    return SQLAlchemyAuditEventRepository(
        session
    ).list_for_tenant(
        tenant_id=tenant_id,
        resource="materials",
        resource_id=str(
            material_id
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
    """Return the unique event for one action."""

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


def test_create_material_records_audit_event(
    material_audit_client: MaterialAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    correlation_id = "corr-material-create-001"
    device_id = "device-material-create-001"

    created = create_material(
        material_audit_client,
        tenant_id,
        correlation_id=correlation_id,
        device_id=device_id,
    )

    material_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events = list_material_events(
        session,
        tenant_id=tenant_id,
        material_id=material_id,
    )

    assert len(events) == 1

    event = require_event(
        events,
        AuditAction.CREATE,
    )

    assert event.tenant_id == tenant_id
    assert event.resource == "materials"
    assert event.resource_id == str(
        material_id
    )

    assert event.actor_user_id == (
        material_audit_client.user_id
    )

    assert event.membership_id == (
        material_audit_client.membership_id
    )

    assert event.auth_user_id == (
        material_audit_client.auth_user_id
    )

    assert event.correlation_id == correlation_id
    assert event.device_id == device_id
    assert event.before is None

    after = require_snapshot(
        event.after
    )

    assert after["id"] == str(
        material_id
    )

    assert after["tenant_id"] == str(
        tenant_id
    )

    assert after["code"] == "MAT-001"
    assert after["name"] == "MDF Branco TX 15mm"
    assert after["category"] == "Chapas"
    assert after["unit"] == "CHAPA"
    assert after["brand_id"] is None
    assert after["is_active"] is True


def test_create_material_with_brand_records_brand_id(
    material_audit_client: MaterialAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    brand_id = create_brand(
        session,
        tenant_id=tenant_id,
    )

    created = create_material(
        material_audit_client,
        tenant_id,
        brand_id=brand_id,
    )

    material_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events = list_material_events(
        session,
        tenant_id=tenant_id,
        material_id=material_id,
    )

    event = require_event(
        events,
        AuditAction.CREATE,
    )

    after = require_snapshot(
        event.after
    )

    assert after["brand_id"] == str(
        brand_id
    )


def test_update_material_records_before_and_after(
    material_audit_client: MaterialAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_material(
        material_audit_client,
        tenant_id,
    )

    material_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    correlation_id = "corr-material-update-001"

    response = material_audit_client.client.patch(
        f"/api/v1/materials/{material_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id="device-material-update",
        ),
        json={
            "code": "MAT-002",
            "name": "MDF Cristallo 18mm",
            "category": "MDF",
            "unit": "UN",
        },
    )

    assert response.status_code == 200

    events = list_material_events(
        session,
        tenant_id=tenant_id,
        material_id=material_id,
    )

    assert len(events) == 2

    event = require_event(
        events,
        AuditAction.UPDATE,
    )

    assert event.correlation_id == correlation_id

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["code"] == "MAT-001"
    assert before["name"] == "MDF Branco TX 15mm"
    assert before["category"] == "Chapas"
    assert before["unit"] == "CHAPA"

    assert after["code"] == "MAT-002"
    assert after["name"] == "MDF Cristallo 18mm"
    assert after["category"] == "MDF"
    assert after["unit"] == "UN"

    assert before["id"] == after["id"]
    assert before["tenant_id"] == after["tenant_id"]


def test_update_material_assigns_brand_in_audit(
    material_audit_client: MaterialAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    brand_id = create_brand(
        session,
        tenant_id=tenant_id,
    )

    created = create_material(
        material_audit_client,
        tenant_id,
    )

    material_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = material_audit_client.client.patch(
        f"/api/v1/materials/{material_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-material-assign-brand",
            device_id="device-material-update",
        ),
        json={
            "brand_id": str(
                brand_id
            ),
        },
    )

    assert response.status_code == 200

    events = list_material_events(
        session,
        tenant_id=tenant_id,
        material_id=material_id,
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

    assert before["brand_id"] is None
    assert after["brand_id"] == str(
        brand_id
    )


def test_update_material_removes_brand_in_audit(
    material_audit_client: MaterialAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    brand_id = create_brand(
        session,
        tenant_id=tenant_id,
    )

    created = create_material(
        material_audit_client,
        tenant_id,
        brand_id=brand_id,
    )

    material_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = material_audit_client.client.patch(
        f"/api/v1/materials/{material_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-material-remove-brand",
            device_id="device-material-update",
        ),
        json={
            "brand_id": None,
        },
    )

    assert response.status_code == 200

    events = list_material_events(
        session,
        tenant_id=tenant_id,
        material_id=material_id,
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

    assert before["brand_id"] == str(
        brand_id
    )

    assert after["brand_id"] is None


def test_update_without_business_change_does_not_create_false_event(
    material_audit_client: MaterialAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_material(
        material_audit_client,
        tenant_id,
    )

    material_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_material_events(
        session,
        tenant_id=tenant_id,
        material_id=material_id,
    )

    assert len(events_before) == 1

    response = material_audit_client.client.patch(
        f"/api/v1/materials/{material_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-material-update-noop",
            device_id="device-material-update",
        ),
        json={
            "name": "MDF Branco TX 15mm",
        },
    )

    assert response.status_code == 200

    events_after = list_material_events(
        session,
        tenant_id=tenant_id,
        material_id=material_id,
    )

    assert len(events_after) == 1


def test_deactivate_material_records_state_change(
    material_audit_client: MaterialAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_material(
        material_audit_client,
        tenant_id,
    )

    material_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = material_audit_client.client.post(
        f"/api/v1/materials/{material_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-material-deactivate",
            device_id="device-material-deactivate",
        ),
    )

    assert response.status_code == 200

    events = list_material_events(
        session,
        tenant_id=tenant_id,
        material_id=material_id,
    )

    assert len(events) == 2

    event = require_event(
        events,
        AuditAction.DEACTIVATE,
    )

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["is_active"] is True
    assert after["is_active"] is False


def test_repeated_deactivate_does_not_create_false_event(
    material_audit_client: MaterialAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_material(
        material_audit_client,
        tenant_id,
    )

    material_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    url = (
        f"/api/v1/materials/{material_id}/deactivate"
    )

    first = material_audit_client.client.post(
        url,
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-material-deactivate-first",
            device_id="device-material-deactivate",
        ),
    )

    assert first.status_code == 200

    events_before_second = list_material_events(
        session,
        tenant_id=tenant_id,
        material_id=material_id,
    )

    assert len(events_before_second) == 2

    second = material_audit_client.client.post(
        url,
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-material-deactivate-second",
            device_id="device-material-deactivate",
        ),
    )

    assert second.status_code == 200

    events_after_second = list_material_events(
        session,
        tenant_id=tenant_id,
        material_id=material_id,
    )

    assert len(events_after_second) == 2


def test_reactivate_material_records_state_change(
    material_audit_client: MaterialAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_material(
        material_audit_client,
        tenant_id,
    )

    material_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    deactivate_response = material_audit_client.client.post(
        f"/api/v1/materials/{material_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-material-before-reactivate",
            device_id="device-material-deactivate",
        ),
    )

    assert deactivate_response.status_code == 200

    response = material_audit_client.client.post(
        f"/api/v1/materials/{material_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-material-reactivate",
            device_id="device-material-reactivate",
        ),
    )

    assert response.status_code == 200

    events = list_material_events(
        session,
        tenant_id=tenant_id,
        material_id=material_id,
    )

    assert len(events) == 3

    event = require_event(
        events,
        AuditAction.REACTIVATE,
    )

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["is_active"] is False
    assert after["is_active"] is True


def test_reactivate_active_material_does_not_create_false_event(
    material_audit_client: MaterialAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_material(
        material_audit_client,
        tenant_id,
    )

    material_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_material_events(
        session,
        tenant_id=tenant_id,
        material_id=material_id,
    )

    assert len(events_before) == 1

    response = material_audit_client.client.post(
        f"/api/v1/materials/{material_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-material-reactivate-noop",
            device_id="device-material-reactivate",
        ),
    )

    assert response.status_code == 200

    events_after = list_material_events(
        session,
        tenant_id=tenant_id,
        material_id=material_id,
    )

    assert len(events_after) == 1


def test_material_audit_events_are_tenant_scoped(
    material_audit_client: MaterialAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    created = create_material(
        material_audit_client,
        tenant_id,
    )

    material_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    own_events = list_material_events(
        session,
        tenant_id=tenant_id,
        material_id=material_id,
    )

    foreign_events = list_material_events(
        session,
        tenant_id=other_tenant_id,
        material_id=material_id,
    )

    assert len(own_events) == 1
    assert foreign_events == []
