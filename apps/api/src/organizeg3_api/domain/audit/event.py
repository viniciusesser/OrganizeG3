"""Immutable business audit event."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
import uuid

from organizeg3_api.domain.audit.action import (
    AuditAction,
)

type JsonScalar = (
    str
    | int
    | float
    | bool
    | None
)

type JsonValue = (
    JsonScalar
    | tuple[JsonValue, ...]
    | Mapping[str, JsonValue]
)


def _require_uuid(
    value: uuid.UUID,
    *,
    field_name: str,
) -> uuid.UUID:
    """Require one non-zero UUID."""

    if not isinstance(value, uuid.UUID):
        raise TypeError(
            f"{field_name} deve ser um UUID válido."
        )

    if value.int == 0:
        raise ValueError(
            f"{field_name} não pode ser o UUID nulo."
        )

    return value


def _normalize_required_text(
    value: str,
    *,
    field_name: str,
) -> str:
    """Normalize and validate required audit text."""

    if not isinstance(value, str):
        raise TypeError(
            f"{field_name} deve ser informado como texto."
        )

    normalized = value.strip()

    if not normalized:
        raise ValueError(
            f"{field_name} é obrigatório."
        )

    return normalized


def _normalize_optional_text(
    value: str | None,
) -> str | None:
    """Normalize optional text values."""

    if value is None:
        return None

    if not isinstance(value, str):
        raise TypeError(
            "O valor opcional deve ser informado como texto."
        )

    normalized = value.strip()

    return normalized or None


def _freeze_json_value(
    value: object,
) -> JsonValue:
    """Convert JSON-compatible mutable structures to immutable values."""

    if value is None:
        return None

    if isinstance(
        value,
        (
            str,
            int,
            float,
            bool,
        ),
    ):
        return value

    if isinstance(
        value,
        Mapping,
    ):
        frozen_mapping = {
            str(key): _freeze_json_value(
                item
            )
            for key, item in value.items()
        }

        return MappingProxyType(
            frozen_mapping
        )

    if isinstance(
        value,
        (
            list,
            tuple,
        ),
    ):
        return tuple(
            _freeze_json_value(
                item
            )
            for item in value
        )

    raise TypeError(
        "Audit snapshots aceitam apenas valores compatíveis com JSON."
    )


def _freeze_mapping(
    value: Mapping[str, object] | None,
) -> Mapping[str, JsonValue] | None:
    """Deep-copy and freeze one audit snapshot mapping."""

    if value is None:
        return None

    copied = deepcopy(
        dict(value)
    )

    frozen = {
        str(key): _freeze_json_value(
            item
        )
        for key, item in copied.items()
    }

    return MappingProxyType(
        frozen
    )


def _normalize_timestamp(
    value: datetime,
) -> datetime:
    """Require and normalize an aware UTC timestamp."""

    if not isinstance(value, datetime):
        raise TypeError(
            "occurred_at deve ser uma data/hora válida."
        )

    if value.tzinfo is None:
        raise ValueError(
            "occurred_at deve possuir timezone."
        )

    return value.astimezone(
        UTC
    )


def _normalize_action(
    value: object,
) -> AuditAction:
    """Return one valid canonical audit action."""

    if isinstance(
        value,
        AuditAction,
    ):
        return value

    if not isinstance(
        value,
        str,
    ):
        raise TypeError(
            "A ação de auditoria deve ser informada como texto."
        )

    try:
        return AuditAction(
            value
        )
    except ValueError as exception:
        raise ValueError(
            "A ação de auditoria é inválida."
        ) from exception


@dataclass(
    frozen=True,
    slots=True,
)
class AuditEvent:
    """Represent one immutable tenant-scoped business audit event."""

    tenant_id: uuid.UUID
    action: AuditAction
    resource: str
    resource_id: str

    actor_user_id: uuid.UUID
    membership_id: uuid.UUID
    auth_user_id: uuid.UUID

    correlation_id: str

    branch_id: uuid.UUID | None = None
    device_id: str | None = None

    before: Mapping[str, object] | None = None
    after: Mapping[str, object] | None = None
    metadata: Mapping[str, object] | None = None

    id: uuid.UUID = field(
        default_factory=uuid.uuid4
    )

    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC
        )
    )

    def __post_init__(
        self,
    ) -> None:
        """Normalize values and enforce audit invariants."""

        object.__setattr__(
            self,
            "id",
            _require_uuid(
                self.id,
                field_name="id",
            ),
        )

        object.__setattr__(
            self,
            "tenant_id",
            _require_uuid(
                self.tenant_id,
                field_name="tenant_id",
            ),
        )

        object.__setattr__(
            self,
            "actor_user_id",
            _require_uuid(
                self.actor_user_id,
                field_name="actor_user_id",
            ),
        )

        object.__setattr__(
            self,
            "membership_id",
            _require_uuid(
                self.membership_id,
                field_name="membership_id",
            ),
        )

        object.__setattr__(
            self,
            "auth_user_id",
            _require_uuid(
                self.auth_user_id,
                field_name="auth_user_id",
            ),
        )

        if self.branch_id is not None:
            object.__setattr__(
                self,
                "branch_id",
                _require_uuid(
                    self.branch_id,
                    field_name="branch_id",
                ),
            )

        raw_action: object = self.action

        object.__setattr__(
            self,
            "action",
            _normalize_action(
                raw_action
            ),
        )

        object.__setattr__(
            self,
            "resource",
            _normalize_required_text(
                self.resource,
                field_name="resource",
            ).lower(),
        )

        object.__setattr__(
            self,
            "resource_id",
            _normalize_required_text(
                self.resource_id,
                field_name="resource_id",
            ),
        )

        object.__setattr__(
            self,
            "correlation_id",
            _normalize_required_text(
                self.correlation_id,
                field_name="correlation_id",
            ),
        )

        object.__setattr__(
            self,
            "device_id",
            _normalize_optional_text(
                self.device_id
            ),
        )

        object.__setattr__(
            self,
            "before",
            _freeze_mapping(
                self.before
            ),
        )

        object.__setattr__(
            self,
            "after",
            _freeze_mapping(
                self.after
            ),
        )

        object.__setattr__(
            self,
            "metadata",
            _freeze_mapping(
                self.metadata
            ),
        )

        object.__setattr__(
            self,
            "occurred_at",
            _normalize_timestamp(
                self.occurred_at
            ),
        )


__all__ = [
    "AuditEvent",
    "JsonScalar",
    "JsonValue",
]
