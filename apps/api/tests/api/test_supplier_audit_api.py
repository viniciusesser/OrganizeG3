"""HTTP audit tests for supplier mutations."""

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
    SupplierPermissions,
)
from organizeg3_api.infrastructure.persistence.repositories.audit_event_repository import (
    SQLAlchemyAuditEventRepository,
)

pytestmark = pytest.mark.api


SUPPLIER_PERMISSION_CODES = (
    SupplierPermissions.READ,
    SupplierPermissions.CREATE,
    SupplierPermissions.UPDATE,
    SupplierPermissions.DEACTIVATE,
    SupplierPermissions.REACTIVATE,
)


@dataclass(
    frozen=True,
    slots=True,
)
class SupplierAuditClient:
    """Authenticated client plus expected audit actor identifiers."""

    client: TestClient
    user_id: uuid.UUID
    membership_id: uuid.UUID
    auth_user_id: uuid.UUID


@pytest.fixture
def supplier_audit_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[SupplierAuditClient]:
    """Provide one authorized supplier actor."""

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
        permission_codes=SUPPLIER_PERMISSION_CODES,
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
        yield SupplierAuditClient(
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


def create_supplier(
    audit_client: SupplierAuditClient,
    tenant_id: uuid.UUID,
    *,
    correlation_id: str = "corr-supplier-create",
    device_id: str = "device-supplier-create",
) -> dict[str, object]:
    """Create one supplier through the audited public API."""

    response = audit_client.client.post(
        "/api/v1/suppliers",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id=device_id,
        ),
        json={
            "code": "FORN-001",
            "name": "Fornecedor Teste",
            "trade_name": "Loja Teste",
            "legal_name": "Fornecedor Teste Ltda",
            "document_number": "04.252.011/0001-10",
            "state_registration": "123456",
            "email": "compras@example.com",
            "invoice_email": "nfe@example.com",
            "phone": "(18) 99999-1234",
            "secondary_phone": "(18) 3222-1234",
            "website": "https://example.com",
            "contact_name": "Contato",
            "postal_code": "19200-000",
            "street": "Rua Teste",
            "number": "100",
            "district": "Centro",
            "city": "Rosana",
            "state": "SP",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert isinstance(
        body,
        dict,
    )

    return body


def list_supplier_events(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    supplier_id: uuid.UUID,
) -> list[AuditEvent]:
    """Return audit history for one supplier."""

    return SQLAlchemyAuditEventRepository(
        session
    ).list_for_tenant(
        tenant_id=tenant_id,
        resource="suppliers",
        resource_id=str(
            supplier_id
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
    """Return exactly one event matching an audit action."""

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


def test_create_supplier_records_audit_event(
    supplier_audit_client: SupplierAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    correlation_id = "corr-supplier-create-001"
    device_id = "device-supplier-create-001"

    created = create_supplier(
        supplier_audit_client,
        tenant_id,
        correlation_id=correlation_id,
        device_id=device_id,
    )

    supplier_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events = list_supplier_events(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier_id,
    )

    assert len(events) == 1

    event = require_event(
        events,
        AuditAction.CREATE,
    )

    assert event.tenant_id == tenant_id
    assert event.resource == "suppliers"

    assert event.resource_id == str(
        supplier_id
    )

    assert event.actor_user_id == (
        supplier_audit_client.user_id
    )

    assert event.membership_id == (
        supplier_audit_client.membership_id
    )

    assert event.auth_user_id == (
        supplier_audit_client.auth_user_id
    )

    assert event.correlation_id == correlation_id
    assert event.device_id == device_id
    assert event.before is None

    after = require_snapshot(
        event.after
    )

    assert after["id"] == str(
        supplier_id
    )

    assert after["tenant_id"] == str(
        tenant_id
    )

    assert after["code"] == "FORN-001"
    assert after["name"] == "Fornecedor Teste"
    assert after["trade_name"] == "Loja Teste"
    assert after["legal_name"] == "Fornecedor Teste Ltda"
    assert after["state_registration"] == "123456"
    assert after["website"] == "https://example.com"
    assert after["contact_name"] == "Contato"
    assert after["street"] == "Rua Teste"
    assert after["number"] == "100"
    assert after["district"] == "Centro"
    assert after["city"] == "Rosana"
    assert after["state"] == "SP"
    assert after["is_active"] is True


def test_create_supplier_does_not_expose_sensitive_values(
    supplier_audit_client: SupplierAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_supplier(
        supplier_audit_client,
        tenant_id,
    )

    supplier_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events = list_supplier_events(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier_id,
    )

    event = require_event(
        events,
        AuditAction.CREATE,
    )

    after = require_snapshot(
        event.after
    )

    assert after["document_number"] != "04252011000110"
    assert after["email"] != "compras@example.com"
    assert after["invoice_email"] != "nfe@example.com"
    assert after["phone"] != "18999991234"
    assert after["secondary_phone"] != "1832221234"


def test_update_supplier_records_before_and_after(
    supplier_audit_client: SupplierAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_supplier(
        supplier_audit_client,
        tenant_id,
    )

    supplier_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    correlation_id = "corr-supplier-update-001"

    response = supplier_audit_client.client.patch(
        f"/api/v1/suppliers/{supplier_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id="device-supplier-update",
        ),
        json={
            "code": "FORN-002",
            "name": "Fornecedor Atualizado",
            "trade_name": "Nova Loja",
            "website": "https://updated.example.com",
            "contact_name": "Novo Contato",
            "city": "Presidente Prudente",
            "state": "SP",
        },
    )

    assert response.status_code == 200

    events = list_supplier_events(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier_id,
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

    assert before["code"] == "FORN-001"
    assert before["name"] == "Fornecedor Teste"
    assert before["trade_name"] == "Loja Teste"
    assert before["contact_name"] == "Contato"
    assert before["city"] == "Rosana"

    assert after["code"] == "FORN-002"
    assert after["name"] == "Fornecedor Atualizado"
    assert after["trade_name"] == "Nova Loja"
    assert after["contact_name"] == "Novo Contato"
    assert after["city"] == "Presidente Prudente"

    assert before["id"] == after["id"]
    assert before["tenant_id"] == after["tenant_id"]


def test_update_supplier_can_clear_optional_field(
    supplier_audit_client: SupplierAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_supplier(
        supplier_audit_client,
        tenant_id,
    )

    supplier_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = supplier_audit_client.client.patch(
        f"/api/v1/suppliers/{supplier_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-supplier-clear-website",
            device_id="device-supplier-update",
        ),
        json={
            "website": None,
        },
    )

    assert response.status_code == 200

    events = list_supplier_events(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier_id,
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

    assert before["website"] == "https://example.com"
    assert after["website"] is None


def test_update_without_business_change_does_not_create_false_event(
    supplier_audit_client: SupplierAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_supplier(
        supplier_audit_client,
        tenant_id,
    )

    supplier_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_supplier_events(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier_id,
    )

    assert len(events_before) == 1

    response = supplier_audit_client.client.patch(
        f"/api/v1/suppliers/{supplier_id}",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-supplier-update-noop",
            device_id="device-supplier-update",
        ),
        json={
            "name": "Fornecedor Teste",
        },
    )

    assert response.status_code == 200

    events_after = list_supplier_events(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier_id,
    )

    assert len(events_after) == 1


def test_deactivate_supplier_records_state_change(
    supplier_audit_client: SupplierAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_supplier(
        supplier_audit_client,
        tenant_id,
    )

    supplier_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = supplier_audit_client.client.post(
        f"/api/v1/suppliers/{supplier_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-supplier-deactivate",
            device_id="device-supplier-deactivate",
        ),
    )

    assert response.status_code == 200

    events = list_supplier_events(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier_id,
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
    supplier_audit_client: SupplierAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_supplier(
        supplier_audit_client,
        tenant_id,
    )

    supplier_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    url = (
        f"/api/v1/suppliers/{supplier_id}/deactivate"
    )

    first = supplier_audit_client.client.post(
        url,
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-supplier-deactivate-first",
            device_id="device-supplier-deactivate",
        ),
    )

    assert first.status_code == 200

    events_before_second = list_supplier_events(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier_id,
    )

    assert len(events_before_second) == 2

    second = supplier_audit_client.client.post(
        url,
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-supplier-deactivate-second",
            device_id="device-supplier-deactivate",
        ),
    )

    assert second.status_code == 200

    events_after_second = list_supplier_events(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier_id,
    )

    assert len(events_after_second) == 2


def test_reactivate_supplier_records_state_change(
    supplier_audit_client: SupplierAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_supplier(
        supplier_audit_client,
        tenant_id,
    )

    supplier_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    deactivate_response = supplier_audit_client.client.post(
        f"/api/v1/suppliers/{supplier_id}/deactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-supplier-before-reactivate",
            device_id="device-supplier-deactivate",
        ),
    )

    assert deactivate_response.status_code == 200

    response = supplier_audit_client.client.post(
        f"/api/v1/suppliers/{supplier_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-supplier-reactivate",
            device_id="device-supplier-reactivate",
        ),
    )

    assert response.status_code == 200

    events = list_supplier_events(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier_id,
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


def test_reactivate_active_supplier_does_not_create_false_event(
    supplier_audit_client: SupplierAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_supplier(
        supplier_audit_client,
        tenant_id,
    )

    supplier_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_supplier_events(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier_id,
    )

    assert len(events_before) == 1

    response = supplier_audit_client.client.post(
        f"/api/v1/suppliers/{supplier_id}/reactivate",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-supplier-reactivate-noop",
            device_id="device-supplier-reactivate",
        ),
    )

    assert response.status_code == 200

    events_after = list_supplier_events(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier_id,
    )

    assert len(events_after) == 1


def test_supplier_audit_events_are_tenant_scoped(
    supplier_audit_client: SupplierAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    created = create_supplier(
        supplier_audit_client,
        tenant_id,
    )

    supplier_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    own_events = list_supplier_events(
        session,
        tenant_id=tenant_id,
        supplier_id=supplier_id,
    )

    foreign_events = list_supplier_events(
        session,
        tenant_id=other_tenant_id,
        supplier_id=supplier_id,
    )

    assert len(own_events) == 1
    assert foreign_events == []
