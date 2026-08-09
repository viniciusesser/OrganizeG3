"""HTTP audit tests for branch mutations."""

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
    BranchPermissions,
)
from organizeg3_api.infrastructure.persistence.repositories.audit_event_repository import (
    SQLAlchemyAuditEventRepository,
)

pytestmark = pytest.mark.api


BRANCH_PERMISSION_CODES = (
    BranchPermissions.READ,
    BranchPermissions.CREATE,
    BranchPermissions.UPDATE,
    BranchPermissions.DEACTIVATE,
    BranchPermissions.REACTIVATE,
)


@dataclass(
    frozen=True,
    slots=True,
)
class BranchAuditClient:
    """Authenticated branch client with expected audit actor identifiers."""

    client: TestClient
    user_id: uuid.UUID
    membership_id: uuid.UUID
    auth_user_id: uuid.UUID


@pytest.fixture
def branch_audit_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[BranchAuditClient]:
    """Provide an authorized branch audit actor."""

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
        permission_codes=BRANCH_PERMISSION_CODES,
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
        yield BranchAuditClient(
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
    audit_client: BranchAuditClient,
    tenant_id: uuid.UUID,
    *,
    code: str = "FILIAL-01",
    name: str = "Filial 01",
    is_headquarters: bool = False,
    correlation_id: str = "corr-branch-create",
    device_id: str = "device-branch-create",
) -> dict[str, object]:
    """Create one complete branch through the audited API."""

    response = audit_client.client.post(
        "/api/v1/branches",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id=device_id,
        ),
        json={
            "code": code,
            "name": name,
            "legal_name": "Filial Teste LTDA",
            "document_number": "12.345.678/0001-95",
            "state_registration": "123456789",
            "email": "FILIAL@EXAMPLE.COM",
            "phone": "(18) 3333-4444",
            "website": "https://example.com",
            "street": "Rua das Flores",
            "number": "100",
            "district": "Centro",
            "city": "Rosana",
            "state": "SP",
            "postal_code": "19273-000",
            "is_headquarters": is_headquarters,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert isinstance(
        body,
        dict,
    )

    return body


def list_branch_events(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    branch_id: uuid.UUID,
) -> list[AuditEvent]:
    """Return audit history for one branch."""

    return SQLAlchemyAuditEventRepository(
        session
    ).list_for_tenant(
        tenant_id=tenant_id,
        resource="branches",
        resource_id=str(
            branch_id
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
    """Return exactly one audit event for the requested action."""

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


def test_create_branch_records_audit_event(
    branch_audit_client: BranchAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    correlation_id = "corr-branch-create-001"
    device_id = "device-branch-create-001"

    created = create_branch(
        branch_audit_client,
        tenant_id,
        correlation_id=correlation_id,
        device_id=device_id,
    )

    branch_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events = list_branch_events(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    assert len(events) == 1

    event = require_event(
        events,
        AuditAction.CREATE,
    )

    assert event.tenant_id == tenant_id
    assert event.resource == "branches"
    assert event.resource_id == str(branch_id)

    assert event.actor_user_id == (
        branch_audit_client.user_id
    )

    assert event.membership_id == (
        branch_audit_client.membership_id
    )

    assert event.auth_user_id == (
        branch_audit_client.auth_user_id
    )

    assert event.correlation_id == correlation_id
    assert event.device_id == device_id
    assert event.before is None

    after = require_snapshot(
        event.after
    )

    assert after["id"] == str(
        branch_id
    )

    assert after["tenant_id"] == str(
        tenant_id
    )

    assert after["code"] == "FILIAL-01"
    assert after["name"] == "Filial 01"
    assert after["legal_name"] == "Filial Teste LTDA"
    assert after["state_registration"] == "123456789"
    assert after["website"] == "https://example.com"
    assert after["street"] == "Rua das Flores"
    assert after["number"] == "100"
    assert after["district"] == "Centro"
    assert after["city"] == "Rosana"
    assert after["state"] == "SP"
    assert after["postal_code"] == "19273000"
    assert after["is_headquarters"] is False
    assert after["is_active"] is True


def test_create_branch_redacts_sensitive_fields(
    branch_audit_client: BranchAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_branch(
        branch_audit_client,
        tenant_id,
    )

    branch_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    event = require_event(
        list_branch_events(
            session,
            tenant_id=tenant_id,
            branch_id=branch_id,
        ),
        AuditAction.CREATE,
    )

    after = require_snapshot(
        event.after
    )

    assert (
        after["document_number"]
        != "12345678000195"
    )

    assert (
        after["email"]
        != "filial@example.com"
    )

    assert (
        after["phone"]
        != "1833334444"
    )


def test_update_branch_records_before_and_after(
    branch_audit_client: BranchAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_branch(
        branch_audit_client,
        tenant_id,
    )

    branch_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = branch_audit_client.client.patch(
        f"/api/v1/branches/{branch_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-branch-update",
            device_id="device-branch-update",
        ),
        json={
            "code": "FILIAL-02",
            "name": "Filial Atualizada",
            "website": "https://updated.example.com",
            "city": "Presidente Prudente",
        },
    )

    assert response.status_code == 200

    event = require_event(
        list_branch_events(
            session,
            tenant_id=tenant_id,
            branch_id=branch_id,
        ),
        AuditAction.UPDATE,
    )

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["code"] == "FILIAL-01"
    assert before["name"] == "Filial 01"
    assert before["website"] == "https://example.com"
    assert before["city"] == "Rosana"

    assert after["code"] == "FILIAL-02"
    assert after["name"] == "Filial Atualizada"

    assert (
        after["website"]
        == "https://updated.example.com"
    )

    assert (
        after["city"]
        == "Presidente Prudente"
    )


def test_update_branch_can_clear_optional_fields(
    branch_audit_client: BranchAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_branch(
        branch_audit_client,
        tenant_id,
    )

    branch_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = branch_audit_client.client.patch(
        f"/api/v1/branches/{branch_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-branch-clear",
            device_id="device-branch-update",
        ),
        json={
            "legal_name": None,
            "email": None,
            "phone": None,
            "website": None,
        },
    )

    assert response.status_code == 200

    event = require_event(
        list_branch_events(
            session,
            tenant_id=tenant_id,
            branch_id=branch_id,
        ),
        AuditAction.UPDATE,
    )

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["legal_name"] == "Filial Teste LTDA"
    assert before["email"] is not None
    assert before["phone"] is not None
    assert before["website"] == "https://example.com"

    assert after["legal_name"] is None
    assert after["email"] is None
    assert after["phone"] is None
    assert after["website"] is None


def test_update_headquarters_change_is_audited(
    branch_audit_client: BranchAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_branch(
        branch_audit_client,
        tenant_id,
    )

    branch_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = branch_audit_client.client.patch(
        f"/api/v1/branches/{branch_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-branch-headquarters",
            device_id="device-branch-update",
        ),
        json={
            "is_headquarters": True,
        },
    )

    assert response.status_code == 200

    event = require_event(
        list_branch_events(
            session,
            tenant_id=tenant_id,
            branch_id=branch_id,
        ),
        AuditAction.UPDATE,
    )

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["is_headquarters"] is False
    assert after["is_headquarters"] is True


def test_update_without_business_change_does_not_create_false_event(
    branch_audit_client: BranchAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_branch(
        branch_audit_client,
        tenant_id,
    )

    branch_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_branch_events(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    assert len(events_before) == 1

    response = branch_audit_client.client.patch(
        f"/api/v1/branches/{branch_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-branch-update-noop",
            device_id="device-branch-update",
        ),
        json={
            "name": "Filial 01",
        },
    )

    assert response.status_code == 200

    events_after = list_branch_events(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    assert len(events_after) == 1


def test_deactivate_branch_records_audit_event(
    branch_audit_client: BranchAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_branch(
        branch_audit_client,
        tenant_id,
    )

    branch_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = branch_audit_client.client.post(
        f"/api/v1/branches/{branch_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-branch-deactivate",
            device_id="device-branch-deactivate",
        ),
    )

    assert response.status_code == 200

    event = require_event(
        list_branch_events(
            session,
            tenant_id=tenant_id,
            branch_id=branch_id,
        ),
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
    branch_audit_client: BranchAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_branch(
        branch_audit_client,
        tenant_id,
    )

    branch_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    url = (
        f"/api/v1/branches/{branch_id}/deactivate"
    )

    first = branch_audit_client.client.post(
        url,
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-branch-deactivate-first",
            device_id="device-branch-deactivate",
        ),
    )

    assert first.status_code == 200

    events_before_second = list_branch_events(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    assert len(events_before_second) == 2

    second = branch_audit_client.client.post(
        url,
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-branch-deactivate-second",
            device_id="device-branch-deactivate",
        ),
    )

    assert second.status_code == 200

    events_after_second = list_branch_events(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    assert len(events_after_second) == 2


def test_reactivate_branch_records_audit_event(
    branch_audit_client: BranchAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_branch(
        branch_audit_client,
        tenant_id,
    )

    branch_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    deactivate_response = branch_audit_client.client.post(
        f"/api/v1/branches/{branch_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-before-branch-reactivate",
            device_id="device-branch-deactivate",
        ),
    )

    assert deactivate_response.status_code == 200

    response = branch_audit_client.client.post(
        f"/api/v1/branches/{branch_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-branch-reactivate",
            device_id="device-branch-reactivate",
        ),
    )

    assert response.status_code == 200

    event = require_event(
        list_branch_events(
            session,
            tenant_id=tenant_id,
            branch_id=branch_id,
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
    assert after["is_active"] is True


def test_reactivate_active_branch_does_not_create_false_event(
    branch_audit_client: BranchAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_branch(
        branch_audit_client,
        tenant_id,
    )

    branch_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_branch_events(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    assert len(events_before) == 1

    response = branch_audit_client.client.post(
        f"/api/v1/branches/{branch_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-branch-reactivate-noop",
            device_id="device-branch-reactivate",
        ),
    )

    assert response.status_code == 200

    events_after = list_branch_events(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    assert len(events_after) == 1


def test_failed_duplicate_headquarters_does_not_record_event(
    branch_audit_client: BranchAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    create_branch(
        branch_audit_client,
        tenant_id,
        code="MATRIZ",
        name="Matriz",
        is_headquarters=True,
        correlation_id="corr-create-matriz",
    )

    created = create_branch(
        branch_audit_client,
        tenant_id,
        code="FILIAL-02",
        name="Filial 02",
        correlation_id="corr-create-filial",
    )

    branch_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_branch_events(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    assert len(events_before) == 1

    response = branch_audit_client.client.patch(
        f"/api/v1/branches/{branch_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-duplicate-headquarters",
            device_id="device-branch-update",
        ),
        json={
            "is_headquarters": True,
        },
    )

    assert response.status_code == 409

    events_after = list_branch_events(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    assert len(events_after) == 1


def test_branch_audit_events_are_tenant_scoped(
    branch_audit_client: BranchAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    created = create_branch(
        branch_audit_client,
        tenant_id,
    )

    branch_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    own_events = list_branch_events(
        session,
        tenant_id=tenant_id,
        branch_id=branch_id,
    )

    foreign_events = list_branch_events(
        session,
        tenant_id=other_tenant_id,
        branch_id=branch_id,
    )

    assert len(own_events) == 1
    assert foreign_events == []
