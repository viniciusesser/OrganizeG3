"""Tests for business audit application services."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum
import uuid

from pydantic import BaseModel
import pytest

from organizeg3_api.application.audit import (
    REDACTED_PERSONAL_DATA,
    REDACTED_SECRET,
    AuditEventFactory,
    RecordAuditEvent,
    sanitize_audit_mapping,
    serialize_audit_value,
)
from organizeg3_api.domain.audit import (
    AuditAction,
    AuditContext,
    AuditEvent,
)


class InMemoryAuditRepository:
    """Minimal append-only audit repository for application tests."""

    def __init__(
        self,
    ) -> None:
        self.events: list[AuditEvent] = []

    def append(
        self,
        event: AuditEvent,
    ) -> AuditEvent:
        self.events.append(
            event
        )

        return event

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        event_id: uuid.UUID,
    ) -> AuditEvent | None:
        return next(
            (
                event
                for event in self.events
                if event.tenant_id == tenant_id
                and event.id == event_id
            ),
            None,
        )

    def list_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        resource: str | None = None,
        resource_id: str | None = None,
        correlation_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[AuditEvent]:
        events = [
            event
            for event in self.events
            if event.tenant_id == tenant_id
        ]

        if resource is not None:
            events = [
                event
                for event in events
                if event.resource
                == resource.strip().lower()
            ]

        if resource_id is not None:
            events = [
                event
                for event in events
                if event.resource_id
                == resource_id.strip()
            ]

        if correlation_id is not None:
            events = [
                event
                for event in events
                if event.correlation_id
                == correlation_id.strip()
            ]

        return events[
            offset : offset + limit
        ]


class ExampleModel(
    BaseModel
):
    """Pydantic payload used by serializer tests."""

    name: str
    email: str
    password: str


class ExampleEnum(
    StrEnum
):
    """Enum used by serializer tests."""

    ACTIVE = "ACTIVE"


@dataclass(
    frozen=True,
    slots=True,
)
class ExampleDataclass:
    """Dataclass used by serializer tests."""

    name: str
    phone: str


def build_context() -> AuditContext:
    """Build trusted audit context."""

    return AuditContext(
        correlation_id="corr-test-123",
        tenant_id=uuid.uuid4(),
        branch_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        membership_id=uuid.uuid4(),
        auth_user_id=uuid.uuid4(),
        device_id="device-test-123",
    )


def test_secret_fields_are_redacted() -> None:
    sanitized = sanitize_audit_mapping(
        {
            "password": "123456",
            "access_token": "token-value",
            "client_secret": "secret-value",
            "api_key": "api-key-value",
        }
    )

    assert sanitized is not None

    assert sanitized == {
        "password": REDACTED_SECRET,
        "access_token": REDACTED_SECRET,
        "client_secret": REDACTED_SECRET,
        "api_key": REDACTED_SECRET,
    }


def test_nested_secret_fields_are_redacted() -> None:
    sanitized = sanitize_audit_mapping(
        {
            "authentication": {
                "token": "token-value",
                "credentials": {
                    "password_hash": "hash-value",
                },
            },
        }
    )

    assert sanitized is not None

    authentication = sanitized[
        "authentication"
    ]

    assert isinstance(
        authentication,
        dict,
    )

    assert (
        authentication["token"]
        == REDACTED_SECRET
    )

    assert (
        authentication["credentials"]
        == REDACTED_SECRET
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "cpf",
        "cnpj",
        "document",
        "document_number",
        "email",
        "email_address",
        "phone",
        "phone_number",
        "telephone",
    ],
)
def test_personal_data_is_redacted(
    field_name: str,
) -> None:
    sanitized = sanitize_audit_mapping(
        {
            field_name: "sensitive-value",
        }
    )

    assert sanitized is not None

    assert (
        sanitized[field_name]
        == REDACTED_PERSONAL_DATA
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "billing_email",
        "contact_email",
        "invoice_email",
        "personal_email",
        "secondary_phone",
        "mobile_phone",
        "emergency_phone",
        "customer_document_number",
        "supplier_document_number",
    ],
)
def test_prefixed_personal_data_fields_are_redacted(
    field_name: str,
) -> None:
    sanitized = sanitize_audit_mapping(
        {
            field_name: "sensitive-value",
        }
    )

    assert sanitized is not None

    assert (
        sanitized[field_name]
        == REDACTED_PERSONAL_DATA
    )


def test_similar_non_personal_field_names_are_not_redacted() -> None:
    sanitized = sanitize_audit_mapping(
        {
            "email_enabled": True,
            "phone_extension": "123",
            "document_type": "CNPJ",
        }
    )

    assert sanitized == {
        "email_enabled": True,
        "phone_extension": "123",
        "document_type": "CNPJ",
    }


def test_null_personal_data_remains_null() -> None:
    sanitized = sanitize_audit_mapping(
        {
            "email": None,
            "invoice_email": None,
            "phone": None,
            "secondary_phone": None,
        }
    )

    assert sanitized == {
        "email": None,
        "invoice_email": None,
        "phone": None,
        "secondary_phone": None,
    }


def test_pydantic_models_are_sanitized() -> None:
    credential_value = uuid.uuid4().hex

    payload = ExampleModel(
        name="Cliente Teste",
        email="cliente@example.com",
        password=credential_value,
    )

    sanitized = sanitize_audit_mapping(
        payload
    )

    assert sanitized == {
        "name": "Cliente Teste",
        "email": REDACTED_PERSONAL_DATA,
        "password": REDACTED_SECRET,
    }


def test_dataclasses_are_serialized_and_sanitized() -> None:
    value = ExampleDataclass(
        name="Cliente",
        phone="11999999999",
    )

    serialized = serialize_audit_value(
        value
    )

    assert serialized == {
        "name": "Cliente",
        "phone": REDACTED_PERSONAL_DATA,
    }


def test_uuid_is_serialized_as_string() -> None:
    value = uuid.uuid4()

    assert serialize_audit_value(
        value
    ) == str(
        value
    )


def test_aware_datetime_is_serialized() -> None:
    value = datetime(
        2026,
        8,
        8,
        18,
        0,
        tzinfo=UTC,
    )

    assert serialize_audit_value(
        value
    ) == value.isoformat()


def test_naive_datetime_is_rejected() -> None:
    value = datetime(
        2026,
        8,
        8,
        18,
        0,
        tzinfo=UTC,
    ).replace(
        tzinfo=None
    )

    with pytest.raises(
        ValueError
    ):
        serialize_audit_value(
            value
        )


def test_decimal_is_serialized_as_string() -> None:
    assert serialize_audit_value(
        Decimal(
            "123.45"
        )
    ) == "123.45"


def test_enum_is_serialized_using_value() -> None:
    serialized = serialize_audit_value(
        ExampleEnum.ACTIVE
    )

    assert serialized == "ACTIVE"
    assert type(serialized) is str


def test_unsupported_object_is_rejected() -> None:
    with pytest.raises(
        TypeError
    ):
        serialize_audit_value(
            object()
        )


def test_factory_uses_only_trusted_context_identity() -> None:
    context = build_context()

    event = AuditEventFactory().create(
        context=context,
        action=AuditAction.CREATE,
        resource="brands",
        resource_id=uuid.uuid4(),
        after={
            "code": "MARCA-01",
            "name": "Marca Teste",
        },
    )

    assert event.tenant_id == context.tenant_id
    assert event.branch_id == context.branch_id
    assert event.actor_user_id == context.user_id
    assert event.membership_id == context.membership_id
    assert event.auth_user_id == context.auth_user_id
    assert event.correlation_id == context.correlation_id
    assert event.device_id == context.device_id


def test_factory_sanitizes_before_after_and_metadata() -> None:
    context = build_context()

    event = AuditEventFactory().create(
        context=context,
        action=AuditAction.UPDATE,
        resource="customers",
        resource_id=123,
        before={
            "email": "old@example.com",
            "name": "Antes",
        },
        after={
            "email": "new@example.com",
            "name": "Depois",
        },
        metadata={
            "access_token": "never-store-this",
            "reason": "profile_update",
        },
    )

    assert event.resource_id == "123"

    assert event.before is not None
    assert event.after is not None
    assert event.metadata is not None

    assert (
        event.before["email"]
        == REDACTED_PERSONAL_DATA
    )

    assert (
        event.after["email"]
        == REDACTED_PERSONAL_DATA
    )

    assert (
        event.metadata["access_token"]
        == REDACTED_SECRET
    )

    assert (
        event.metadata["reason"]
        == "profile_update"
    )


def test_factory_sanitizes_prefixed_personal_fields() -> None:
    event = AuditEventFactory().create(
        context=build_context(),
        action=AuditAction.CREATE,
        resource="suppliers",
        resource_id=uuid.uuid4(),
        after={
            "email": "supplier@example.com",
            "invoice_email": "nfe@example.com",
            "phone": "18999991234",
            "secondary_phone": "1832221234",
            "document_number": "04252011000110",
        },
    )

    assert event.after is not None

    assert event.after == {
        "email": REDACTED_PERSONAL_DATA,
        "invoice_email": REDACTED_PERSONAL_DATA,
        "phone": REDACTED_PERSONAL_DATA,
        "secondary_phone": REDACTED_PERSONAL_DATA,
        "document_number": REDACTED_PERSONAL_DATA,
    }


def test_record_audit_event_appends_factory_result() -> None:
    context = build_context()
    repository = InMemoryAuditRepository()

    use_case = RecordAuditEvent(
        repository
    )

    event = use_case.execute(
        context=context,
        action=AuditAction.DEACTIVATE,
        resource="brands",
        resource_id=uuid.uuid4(),
        before={
            "is_active": True,
        },
        after={
            "is_active": False,
        },
    )

    assert repository.events == [
        event
    ]

    assert event.action is AuditAction.DEACTIVATE


def test_recorded_event_contains_sanitized_snapshot() -> None:
    repository = InMemoryAuditRepository()

    event = RecordAuditEvent(
        repository
    ).execute(
        context=build_context(),
        action=AuditAction.UPDATE,
        resource="customers",
        resource_id=1,
        after={
            "document_number": "12345678909",
            "email": "cliente@example.com",
            "phone": "11999999999",
            "name": "Cliente",
        },
    )

    assert event.after is not None

    assert (
        event.after["document_number"]
        == REDACTED_PERSONAL_DATA
    )

    assert (
        event.after["email"]
        == REDACTED_PERSONAL_DATA
    )

    assert (
        event.after["phone"]
        == REDACTED_PERSONAL_DATA
    )

    assert event.after["name"] == "Cliente"
