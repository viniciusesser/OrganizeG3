"""Integration tests for audit event persistence."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.audit import (
    AuditAction,
    AuditEvent,
)
from organizeg3_api.infrastructure.persistence.models.audit_event import (
    AuditEventModel,
)
from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.repositories.audit_event_repository import (
    SQLAlchemyAuditEventRepository,
)


def add_tenant(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    name: str,
) -> None:
    """Persist one tenant used by audit tests."""

    session.add(
        TenantRecordModel(
            id=tenant_id,
            name=name,
            status="ACTIVE",
            is_active=True,
        )
    )

    session.flush()


def build_event(
    *,
    tenant_id: uuid.UUID,
    resource: str = "brands",
    resource_id: str | None = None,
    correlation_id: str = "corr-001",
    actor_user_id: uuid.UUID | None = None,
    occurred_at: datetime | None = None,
) -> AuditEvent:
    """Build one valid audit event."""

    return AuditEvent(
        tenant_id=tenant_id,
        branch_id=uuid.uuid4(),
        actor_user_id=(
            actor_user_id
            or uuid.uuid4()
        ),
        membership_id=uuid.uuid4(),
        auth_user_id=uuid.uuid4(),
        action=AuditAction.UPDATE,
        resource=resource,
        resource_id=(
            resource_id
            or str(
                uuid.uuid4()
            )
        ),
        correlation_id=correlation_id,
        device_id="device-test",
        before={
            "name": "Antes",
            "nested": {
                "enabled": False,
            },
        },
        after={
            "name": "Depois",
            "items": [
                "A",
                "B",
            ],
        },
        metadata={
            "source": "integration-test",
        },
        occurred_at=(
            occurred_at
            or datetime.now(
                UTC
            )
        ),
    )


def test_append_and_get_event(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    add_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Audit",
    )

    repository = SQLAlchemyAuditEventRepository(
        session
    )

    event = build_event(
        tenant_id=tenant_id
    )

    persisted = repository.append(
        event
    )

    loaded = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        event_id=persisted.id,
    )

    assert loaded is not None
    assert loaded.id == event.id
    assert loaded.tenant_id == tenant_id
    assert loaded.action is AuditAction.UPDATE
    assert loaded.resource == "brands"
    assert loaded.correlation_id == "corr-001"


def test_json_snapshots_round_trip(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    add_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant JSON",
    )

    repository = SQLAlchemyAuditEventRepository(
        session
    )

    persisted = repository.append(
        build_event(
            tenant_id=tenant_id
        )
    )

    assert persisted.before is not None
    assert persisted.after is not None
    assert persisted.metadata is not None

    assert persisted.before["name"] == "Antes"

    nested = persisted.before[
        "nested"
    ]

    assert nested[
        "enabled"
    ] is False  # type: ignore[index]

    assert persisted.after[
        "items"
    ] == (
        "A",
        "B",
    )

    assert (
        persisted.metadata[
            "source"
        ]
        == "integration-test"
    )


def test_get_is_tenant_scoped(
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    add_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant A",
    )

    add_tenant(
        session,
        tenant_id=other_tenant_id,
        name="Tenant B",
    )

    repository = SQLAlchemyAuditEventRepository(
        session
    )

    persisted = repository.append(
        build_event(
            tenant_id=tenant_id
        )
    )

    result = repository.get_by_id_for_tenant(
        tenant_id=other_tenant_id,
        event_id=persisted.id,
    )

    assert result is None


def test_list_returns_only_requested_tenant(
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> None:
    add_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Principal",
    )

    add_tenant(
        session,
        tenant_id=other_tenant_id,
        name="Outro Tenant",
    )

    repository = SQLAlchemyAuditEventRepository(
        session
    )

    first = repository.append(
        build_event(
            tenant_id=tenant_id,
            correlation_id="corr-main",
        )
    )

    repository.append(
        build_event(
            tenant_id=other_tenant_id,
            correlation_id="corr-other",
        )
    )

    result = repository.list_for_tenant(
        tenant_id=tenant_id
    )

    assert [
        item.id
        for item in result
    ] == [
        first.id
    ]


def test_list_filters_resource_and_resource_id(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    add_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Filter",
    )

    repository = SQLAlchemyAuditEventRepository(
        session
    )

    target_id = str(
        uuid.uuid4()
    )

    target = repository.append(
        build_event(
            tenant_id=tenant_id,
            resource="brands",
            resource_id=target_id,
        )
    )

    repository.append(
        build_event(
            tenant_id=tenant_id,
            resource="machines",
        )
    )

    repository.append(
        build_event(
            tenant_id=tenant_id,
            resource="brands",
        )
    )

    result = repository.list_for_tenant(
        tenant_id=tenant_id,
        resource=" BRANDS ",
        resource_id=f" {target_id} ",
    )

    assert [
        item.id
        for item in result
    ] == [
        target.id
    ]


def test_list_filters_correlation_id(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    add_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Correlation",
    )

    repository = SQLAlchemyAuditEventRepository(
        session
    )

    target = repository.append(
        build_event(
            tenant_id=tenant_id,
            correlation_id="corr-target",
        )
    )

    repository.append(
        build_event(
            tenant_id=tenant_id,
            correlation_id="corr-other",
        )
    )

    result = repository.list_for_tenant(
        tenant_id=tenant_id,
        correlation_id=" corr-target ",
    )

    assert [
        item.id
        for item in result
    ] == [
        target.id
    ]


def test_list_orders_newest_first(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    add_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Ordering",
    )

    repository = SQLAlchemyAuditEventRepository(
        session
    )

    base_time = datetime(
        2026,
        8,
        8,
        12,
        0,
        tzinfo=UTC,
    )

    oldest = repository.append(
        build_event(
            tenant_id=tenant_id,
            occurred_at=base_time,
        )
    )

    newest = repository.append(
        build_event(
            tenant_id=tenant_id,
            occurred_at=(
                base_time
                + timedelta(
                    minutes=2
                )
            ),
        )
    )

    middle = repository.append(
        build_event(
            tenant_id=tenant_id,
            occurred_at=(
                base_time
                + timedelta(
                    minutes=1
                )
            ),
        )
    )

    result = repository.list_for_tenant(
        tenant_id=tenant_id
    )

    assert [
        item.id
        for item in result
    ] == [
        newest.id,
        middle.id,
        oldest.id,
    ]


def test_list_supports_pagination(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    add_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Pagination",
    )

    repository = SQLAlchemyAuditEventRepository(
        session
    )

    base_time = datetime(
        2026,
        8,
        8,
        12,
        0,
        tzinfo=UTC,
    )

    events = [
        repository.append(
            build_event(
                tenant_id=tenant_id,
                occurred_at=(
                    base_time
                    + timedelta(
                        minutes=index
                    )
                ),
            )
        )
        for index in range(
            3
        )
    ]

    result = repository.list_for_tenant(
        tenant_id=tenant_id,
        limit=1,
        offset=1,
    )

    assert len(
        result
    ) == 1

    assert result[0].id == events[1].id


def test_database_rows_use_plain_json(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    add_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Raw JSON",
    )

    repository = SQLAlchemyAuditEventRepository(
        session
    )

    persisted = repository.append(
        build_event(
            tenant_id=tenant_id
        )
    )

    statement = select(
        AuditEventModel
    ).where(
        AuditEventModel.id == persisted.id
    )

    model = session.execute(
        statement
    ).scalar_one()

    assert isinstance(
        model.before_snapshot,
        dict,
    )

    assert isinstance(
        model.after_snapshot,
        dict,
    )

    assert isinstance(
        model.after_snapshot[
            "items"
        ],
        list,
    )


def test_repository_exposes_append_only_mutation_api() -> None:
    repository_type = SQLAlchemyAuditEventRepository

    assert hasattr(
        repository_type,
        "append",
    )

    assert not hasattr(
        repository_type,
        "save",
    )

    assert not hasattr(
        repository_type,
        "update",
    )

    assert not hasattr(
        repository_type,
        "delete",
    )


def test_persisted_event_cannot_be_mutated_through_domain(
    session: Session,
    tenant_id: uuid.UUID,
) -> None:
    add_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Immutable",
    )

    repository = SQLAlchemyAuditEventRepository(
        session
    )

    persisted = repository.append(
        build_event(
            tenant_id=tenant_id
        )
    )

    loaded = repository.get_by_id_for_tenant(
        tenant_id=tenant_id,
        event_id=persisted.id,
    )

    assert loaded is not None
    assert loaded == persisted
