"""SQLAlchemy repository for append-only business audit events."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.audit import (
    AuditAction,
    AuditEvent,
    AuditEventRepository,
    JsonScalar,
)
from organizeg3_api.infrastructure.persistence.models.audit_event import (
    AuditEventModel,
)

type PersistedJsonValue = (
    JsonScalar
    | list[PersistedJsonValue]
    | dict[str, PersistedJsonValue]
)


def _thaw_json_value(
    value: object,
) -> PersistedJsonValue:
    """Convert immutable domain JSON values to persistence values."""

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
        return {
            str(key): _thaw_json_value(
                item
            )
            for key, item in value.items()
        }

    if isinstance(
        value,
        (
            tuple,
            list,
        ),
    ):
        return [
            _thaw_json_value(
                item
            )
            for item in value
        ]

    raise TypeError(
        "Audit snapshots aceitam apenas valores compatíveis com JSON."
    )


def _thaw_mapping(
    value: Mapping[str, object] | None,
) -> dict[str, PersistedJsonValue] | None:
    """Convert one domain audit mapping to ordinary JSON data."""

    if value is None:
        return None

    return {
        str(key): _thaw_json_value(
            item
        )
        for key, item in value.items()
    }


def _normalize_database_timestamp(
    value: datetime,
) -> datetime:
    """Normalize a database timestamp to aware UTC."""

    if value.tzinfo is None:
        return value.replace(
            tzinfo=UTC
        )

    return value.astimezone(
        UTC
    )


class SQLAlchemyAuditEventRepository(
    AuditEventRepository,
):
    """Persist and query immutable audit events."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def append(
        self,
        event: AuditEvent,
    ) -> AuditEvent:
        """Append one audit event without mutation semantics."""

        model = AuditEventModel(
            id=event.id,
            tenant_id=event.tenant_id,
            branch_id=event.branch_id,
            actor_user_id=event.actor_user_id,
            membership_id=event.membership_id,
            auth_user_id=event.auth_user_id,
            action=event.action.value,
            resource=event.resource,
            resource_id=event.resource_id,
            correlation_id=event.correlation_id,
            device_id=event.device_id,
            before_snapshot=_thaw_mapping(
                event.before
            ),
            after_snapshot=_thaw_mapping(
                event.after
            ),
            event_metadata=_thaw_mapping(
                event.metadata
            ),
            occurred_at=event.occurred_at,
        )

        self._session.add(
            model
        )
        self._session.flush()

        return self._to_domain(
            model
        )

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        event_id: uuid.UUID,
    ) -> AuditEvent | None:
        """Return one event inside its tenant boundary."""

        statement = (
            select(
                AuditEventModel
            )
            .where(
                AuditEventModel.tenant_id == tenant_id,
                AuditEventModel.id == event_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(
                statement
            )
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(
            model
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
        """List tenant audit history with optional filters."""

        statement = select(
            AuditEventModel
        ).where(
            AuditEventModel.tenant_id == tenant_id
        )

        normalized_resource = (
            resource.strip().lower()
            if resource is not None
            else ""
        )

        normalized_resource_id = (
            resource_id.strip()
            if resource_id is not None
            else ""
        )

        normalized_correlation_id = (
            correlation_id.strip()
            if correlation_id is not None
            else ""
        )

        if normalized_resource:
            statement = statement.where(
                AuditEventModel.resource
                == normalized_resource
            )

        if normalized_resource_id:
            statement = statement.where(
                AuditEventModel.resource_id
                == normalized_resource_id
            )

        if normalized_correlation_id:
            statement = statement.where(
                AuditEventModel.correlation_id
                == normalized_correlation_id
            )

        statement = (
            statement
            .order_by(
                AuditEventModel.occurred_at.desc(),
                AuditEventModel.id.desc(),
            )
            .limit(
                limit
            )
            .offset(
                offset
            )
        )

        models = (
            self._session.execute(
                statement
            )
            .scalars()
            .all()
        )

        return [
            self._to_domain(
                model
            )
            for model in models
        ]

    @staticmethod
    def _to_domain(
        model: AuditEventModel,
    ) -> AuditEvent:
        """Convert one persistence model to an immutable domain event."""

        return AuditEvent(
            id=model.id,
            tenant_id=model.tenant_id,
            branch_id=model.branch_id,
            actor_user_id=model.actor_user_id,
            membership_id=model.membership_id,
            auth_user_id=model.auth_user_id,
            action=AuditAction(
                model.action
            ),
            resource=model.resource,
            resource_id=model.resource_id,
            correlation_id=model.correlation_id,
            device_id=model.device_id,
            before=model.before_snapshot,
            after=model.after_snapshot,
            metadata=model.event_metadata,
            occurred_at=_normalize_database_timestamp(
                model.occurred_at
            ),
        )


__all__ = [
    "SQLAlchemyAuditEventRepository",
]
