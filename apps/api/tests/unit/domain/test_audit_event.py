"""Unit tests for immutable business audit events."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
import uuid

import pytest

from organizeg3_api.domain.audit import (
    AuditAction,
    AuditEvent,
    AuditEventRepository,
)


def build_event(
    **overrides: object,
) -> AuditEvent:
    """Build one valid audit event for tests."""

    values: dict[str, object] = {
        "tenant_id": uuid.uuid4(),
        "action": AuditAction.UPDATE,
        "resource": "brands",
        "resource_id": str(
            uuid.uuid4()
        ),
        "actor_user_id": uuid.uuid4(),
        "membership_id": uuid.uuid4(),
        "auth_user_id": uuid.uuid4(),
        "correlation_id": "corr-123",
        "branch_id": uuid.uuid4(),
        "device_id": "device-123",
        "before": {
            "name": "Antiga",
            "nested": {
                "value": 1,
            },
        },
        "after": {
            "name": "Nova",
            "items": [
                "A",
                "B",
            ],
        },
        "metadata": {
            "source": "api",
        },
    }

    values.update(
        overrides
    )

    return AuditEvent(
        tenant_id=values["tenant_id"],  # type: ignore[arg-type]
        action=values["action"],  # type: ignore[arg-type]
        resource=values["resource"],  # type: ignore[arg-type]
        resource_id=values["resource_id"],  # type: ignore[arg-type]
        actor_user_id=values["actor_user_id"],  # type: ignore[arg-type]
        membership_id=values["membership_id"],  # type: ignore[arg-type]
        auth_user_id=values["auth_user_id"],  # type: ignore[arg-type]
        correlation_id=values["correlation_id"],  # type: ignore[arg-type]
        branch_id=values.get("branch_id"),  # type: ignore[arg-type]
        device_id=values.get("device_id"),  # type: ignore[arg-type]
        before=values.get("before"),  # type: ignore[arg-type]
        after=values.get("after"),  # type: ignore[arg-type]
        metadata=values.get("metadata"),  # type: ignore[arg-type]
        occurred_at=values.get(  # type: ignore[arg-type]
            "occurred_at",
            datetime.now(
                UTC
            ),
        ),
    )


def test_event_generates_identity_and_timestamp() -> None:
    event = build_event()

    assert isinstance(
        event.id,
        uuid.UUID,
    )
    assert event.id.int != 0

    assert event.occurred_at.tzinfo is not None
    assert event.occurred_at.utcoffset() == timedelta(
        0
    )


def test_event_normalizes_text_fields() -> None:
    event = build_event(
        resource="  Brands  ",
        resource_id="  abc-123  ",
        correlation_id="  corr-123  ",
        device_id="  device-123  ",
    )

    assert event.resource == "brands"
    assert event.resource_id == "abc-123"
    assert event.correlation_id == "corr-123"
    assert event.device_id == "device-123"


def test_event_allows_no_branch() -> None:
    event = build_event(
        branch_id=None
    )

    assert event.branch_id is None


def test_blank_optional_device_becomes_none() -> None:
    event = build_event(
        device_id="   "
    )

    assert event.device_id is None


@pytest.mark.parametrize(
    "field_name",
    [
        "tenant_id",
        "actor_user_id",
        "membership_id",
        "auth_user_id",
    ],
)
def test_required_uuid_rejects_zero_uuid(
    field_name: str,
) -> None:
    with pytest.raises(
        ValueError
    ):
        build_event(
            **{
                field_name: uuid.UUID(
                    int=0
                )
            }
        )


def test_branch_rejects_zero_uuid() -> None:
    with pytest.raises(
        ValueError
    ):
        build_event(
            branch_id=uuid.UUID(
                int=0
            )
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "resource",
        "resource_id",
        "correlation_id",
    ],
)
def test_required_text_rejects_blank(
    field_name: str,
) -> None:
    with pytest.raises(
        ValueError
    ):
        build_event(
            **{
                field_name: "   "
            }
        )


def test_invalid_action_is_rejected() -> None:
    with pytest.raises(
        ValueError
    ):
        build_event(
            action="INVALID"
        )


@pytest.mark.parametrize(
    "action",
    list(
        AuditAction
    ),
)
def test_accepts_every_canonical_action(
    action: AuditAction,
) -> None:
    event = build_event(
        action=action
    )

    assert event.action is action


def test_timestamp_is_normalized_to_utc() -> None:
    event = build_event(
        occurred_at=datetime(
            2026,
            8,
            8,
            18,
            0,
            tzinfo=UTC,
        )
    )

    assert event.occurred_at.tzinfo is UTC


def test_naive_timestamp_is_rejected() -> None:
    aware_timestamp = datetime(
        2026,
        8,
        8,
        18,
        0,
        tzinfo=UTC,
    )

    naive_timestamp = aware_timestamp.replace(
        tzinfo=None
    )

    with pytest.raises(
        ValueError
    ):
        build_event(
            occurred_at=naive_timestamp
        )


def test_event_is_frozen() -> None:
    event = build_event()

    with pytest.raises(
        FrozenInstanceError
    ):
        event.resource = "machines"  # type: ignore[misc]


def test_before_snapshot_is_immutable() -> None:
    event = build_event()

    assert event.before is not None

    with pytest.raises(
        TypeError
    ):
        event.before["name"] = "Alterada"  # type: ignore[index]


def test_nested_snapshot_is_immutable() -> None:
    event = build_event()

    assert event.before is not None

    nested = event.before[
        "nested"
    ]

    assert isinstance(
        nested,
        Mapping,
    )

    with pytest.raises(
        TypeError
    ):
        nested["value"] = 2  # type: ignore[index]


def test_list_values_are_converted_to_tuples() -> None:
    event = build_event()

    assert event.after is not None

    items = event.after[
        "items"
    ]

    assert items == (
        "A",
        "B",
    )


def test_original_snapshot_mutation_does_not_change_event() -> None:
    before = {
        "name": "Original",
        "nested": {
            "value": 1,
        },
    }

    event = build_event(
        before=before
    )

    before["name"] = "Alterado"

    nested = before[
        "nested"
    ]

    assert isinstance(
        nested,
        dict,
    )

    nested["value"] = 999

    assert event.before is not None
    assert event.before["name"] == "Original"

    frozen_nested = event.before[
        "nested"
    ]

    assert isinstance(
        frozen_nested,
        Mapping,
    )

    assert frozen_nested[
        "value"
    ] == 1


def test_non_json_snapshot_value_is_rejected() -> None:
    with pytest.raises(
        TypeError
    ):
        build_event(
            metadata={
                "invalid": uuid.uuid4(),
            }
        )


def test_repository_contract_exposes_no_mutation_methods() -> None:
    assert hasattr(
        AuditEventRepository,
        "append",
    )
    assert hasattr(
        AuditEventRepository,
        "get_by_id_for_tenant",
    )
    assert hasattr(
        AuditEventRepository,
        "list_for_tenant",
    )

    assert not hasattr(
        AuditEventRepository,
        "save",
    )
    assert not hasattr(
        AuditEventRepository,
        "update",
    )
    assert not hasattr(
        AuditEventRepository,
        "delete",
    )
