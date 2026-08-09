"""HTTP audit tests for company mutations."""

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
    CompanyPermissions,
)
from organizeg3_api.infrastructure.persistence.repositories.audit_event_repository import (
    SQLAlchemyAuditEventRepository,
)

pytestmark = pytest.mark.api


COMPANY_PERMISSION_CODES = (
    CompanyPermissions.READ,
    CompanyPermissions.CREATE,
    CompanyPermissions.UPDATE,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CompanyAuditClient:
    """Authenticated company client with expected audit actor identifiers."""

    client: TestClient
    user_id: uuid.UUID
    membership_id: uuid.UUID
    auth_user_id: uuid.UUID


@pytest.fixture
def company_audit_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> Iterator[CompanyAuditClient]:
    """Provide an authorized actor for company audit tests."""

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
        permission_codes=COMPANY_PERMISSION_CODES,
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
        yield CompanyAuditClient(
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


def create_company(
    audit_client: CompanyAuditClient,
    tenant_id: uuid.UUID,
    *,
    correlation_id: str = "corr-company-create",
    device_id: str = "device-company-create",
) -> dict[str, object]:
    """Create one complete company through the audited API."""

    response = audit_client.client.post(
        "/api/v1/company",
        headers=audit_headers(
            tenant_id,
            correlation_id=correlation_id,
            device_id=device_id,
        ),
        json={
            "trade_name": "Empresa Teste",
            "legal_name": "Empresa Teste LTDA",
            "document_number": "12.345.678/0001-90",
            "state_registration": "123456789",
            "email": "CONTATO@EXAMPLE.COM",
            "phone": "(18) 3222-1234",
            "website": "https://example.com",
            "logo_path": "/logos/company.png",
            "street": "Rua Teste",
            "number": "123",
            "district": "Centro",
            "city": "Rosana",
            "state": "SP",
            "postal_code": "19273-000",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert isinstance(
        body,
        dict,
    )

    return body


def list_company_events(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    company_id: uuid.UUID,
) -> list[AuditEvent]:
    """Return audit history for one company."""

    return SQLAlchemyAuditEventRepository(
        session
    ).list_for_tenant(
        tenant_id=tenant_id,
        resource="companies",
        resource_id=str(
            company_id
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
    """Return exactly one company event for the requested action."""

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


def test_create_company_records_audit_event(
    company_audit_client: CompanyAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    correlation_id = "corr-company-create-001"
    device_id = "device-company-create-001"

    created = create_company(
        company_audit_client,
        tenant_id,
        correlation_id=correlation_id,
        device_id=device_id,
    )

    company_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events = list_company_events(
        session,
        tenant_id=tenant_id,
        company_id=company_id,
    )

    assert len(events) == 1

    event = require_event(
        events,
        AuditAction.CREATE,
    )

    assert event.tenant_id == tenant_id
    assert event.resource == "companies"
    assert event.resource_id == str(company_id)

    assert event.actor_user_id == (
        company_audit_client.user_id
    )

    assert event.membership_id == (
        company_audit_client.membership_id
    )

    assert event.auth_user_id == (
        company_audit_client.auth_user_id
    )

    assert event.correlation_id == correlation_id
    assert event.device_id == device_id
    assert event.before is None

    after = require_snapshot(
        event.after
    )

    assert after["id"] == str(
        company_id
    )

    assert after["tenant_id"] == str(
        tenant_id
    )

    assert after["trade_name"] == "Empresa Teste"
    assert after["legal_name"] == "Empresa Teste LTDA"
    assert after["state_registration"] == "123456789"
    assert after["website"] == "https://example.com"
    assert after["logo_path"] == "/logos/company.png"
    assert after["street"] == "Rua Teste"
    assert after["number"] == "123"
    assert after["district"] == "Centro"
    assert after["city"] == "Rosana"
    assert after["state"] == "SP"
    assert after["postal_code"] == "19273000"
    assert after["is_active"] is True


def test_create_company_redacts_sensitive_fields(
    company_audit_client: CompanyAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_company(
        company_audit_client,
        tenant_id,
    )

    company_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    event = require_event(
        list_company_events(
            session,
            tenant_id=tenant_id,
            company_id=company_id,
        ),
        AuditAction.CREATE,
    )

    after = require_snapshot(
        event.after
    )

    assert (
        after["document_number"]
        != "12345678000190"
    )

    assert (
        after["email"]
        != "contato@example.com"
    )

    assert (
        after["phone"]
        != "1832221234"
    )


def test_update_company_records_before_and_after(
    company_audit_client: CompanyAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_company(
        company_audit_client,
        tenant_id,
    )

    company_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = company_audit_client.client.patch(
        "/api/v1/company",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-company-update",
            device_id="device-company-update",
        ),
        json={
            "trade_name": "Empresa Atualizada",
            "website": "https://updated.example.com",
            "city": "Presidente Prudente",
        },
    )

    assert response.status_code == 200

    events = list_company_events(
        session,
        tenant_id=tenant_id,
        company_id=company_id,
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

    assert before["trade_name"] == "Empresa Teste"
    assert before["website"] == "https://example.com"
    assert before["city"] == "Rosana"

    assert after["trade_name"] == "Empresa Atualizada"

    assert (
        after["website"]
        == "https://updated.example.com"
    )

    assert (
        after["city"]
        == "Presidente Prudente"
    )


def test_update_company_can_clear_optional_fields(
    company_audit_client: CompanyAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_company(
        company_audit_client,
        tenant_id,
    )

    company_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    response = company_audit_client.client.patch(
        "/api/v1/company",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-company-clear-fields",
            device_id="device-company-update",
        ),
        json={
            "legal_name": None,
            "email": None,
            "phone": None,
            "website": None,
            "logo_path": None,
        },
    )

    assert response.status_code == 200

    event = require_event(
        list_company_events(
            session,
            tenant_id=tenant_id,
            company_id=company_id,
        ),
        AuditAction.UPDATE,
    )

    before = require_snapshot(
        event.before
    )

    after = require_snapshot(
        event.after
    )

    assert before["legal_name"] == "Empresa Teste LTDA"
    assert before["email"] is not None
    assert before["phone"] is not None
    assert before["website"] == "https://example.com"
    assert before["logo_path"] == "/logos/company.png"

    assert after["legal_name"] is None
    assert after["email"] is None
    assert after["phone"] is None
    assert after["website"] is None
    assert after["logo_path"] is None


def test_update_without_business_change_does_not_create_false_event(
    company_audit_client: CompanyAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_company(
        company_audit_client,
        tenant_id,
    )

    company_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_company_events(
        session,
        tenant_id=tenant_id,
        company_id=company_id,
    )

    assert len(events_before) == 1

    response = company_audit_client.client.patch(
        "/api/v1/company",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-company-update-noop",
            device_id="device-company-update",
        ),
        json={
            "trade_name": "Empresa Teste",
        },
    )

    assert response.status_code == 200

    events_after = list_company_events(
        session,
        tenant_id=tenant_id,
        company_id=company_id,
    )

    assert len(events_after) == 1


def test_duplicate_company_does_not_create_false_event(
    company_audit_client: CompanyAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_company(
        company_audit_client,
        tenant_id,
    )

    company_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_company_events(
        session,
        tenant_id=tenant_id,
        company_id=company_id,
    )

    assert len(events_before) == 1

    response = company_audit_client.client.post(
        "/api/v1/company",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-company-duplicate",
            device_id="device-company-create",
        ),
        json={
            "trade_name": "Empresa Duplicada",
        },
    )

    assert response.status_code == 409

    events_after = list_company_events(
        session,
        tenant_id=tenant_id,
        company_id=company_id,
    )

    assert len(events_after) == 1


def test_empty_update_does_not_create_false_event(
    company_audit_client: CompanyAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    created = create_company(
        company_audit_client,
        tenant_id,
    )

    company_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    events_before = list_company_events(
        session,
        tenant_id=tenant_id,
        company_id=company_id,
    )

    assert len(events_before) == 1

    response = company_audit_client.client.patch(
        "/api/v1/company",
        headers=audit_headers(
            tenant_id,
            correlation_id="corr-company-empty-update",
            device_id="device-company-update",
        ),
        json={},
    )

    assert response.status_code == 422

    events_after = list_company_events(
        session,
        tenant_id=tenant_id,
        company_id=company_id,
    )

    assert len(events_after) == 1


def test_company_audit_events_are_tenant_scoped(
    company_audit_client: CompanyAuditClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    created = create_company(
        company_audit_client,
        tenant_id,
    )

    company_id = uuid.UUID(
        str(
            created["id"]
        )
    )

    own_events = list_company_events(
        session,
        tenant_id=tenant_id,
        company_id=company_id,
    )

    foreign_events = list_company_events(
        session,
        tenant_id=other_tenant_id,
        company_id=company_id,
    )

    assert len(own_events) == 1
    assert foreign_events == []
