"""Production operational event domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
import uuid


class ProductionEventType(StrEnum):
    """Represent relevant production audit events."""

    ORDER_RELEASED = "ORDER_RELEASED"
    ORDER_STARTED = "ORDER_STARTED"
    ORDER_PAUSED = "ORDER_PAUSED"
    ORDER_COMPLETED = "ORDER_COMPLETED"
    ORDER_CANCELLED = "ORDER_CANCELLED"

    OPERATION_READY = "OPERATION_READY"
    OPERATION_STARTED = "OPERATION_STARTED"
    OPERATION_PAUSED = "OPERATION_PAUSED"
    OPERATION_COMPLETED = "OPERATION_COMPLETED"
    OPERATION_NOT_APPLICABLE = "OPERATION_NOT_APPLICABLE"
    OPERATION_REOPENED = "OPERATION_REOPENED"

    EXECUTION_STARTED = "EXECUTION_STARTED"
    EXECUTION_PAUSED = "EXECUTION_PAUSED"
    EXECUTION_RESUMED = "EXECUTION_RESUMED"
    EXECUTION_COMPLETED = "EXECUTION_COMPLETED"
    EXECUTION_CANCELLED = "EXECUTION_CANCELLED"

    REASSIGNED = "REASSIGNED"
    REWORK = "REWORK"
    RETURNED = "RETURNED"
    MATERIAL_SHORTAGE = "MATERIAL_SHORTAGE"
    PROBLEM_REPORTED = "PROBLEM_REPORTED"
    NOTE = "NOTE"


@dataclass(slots=True)
class ProductionEvent:
    """Represent an immutable operational production event."""

    tenant_id: uuid.UUID
    production_order_id: uuid.UUID
    event_type: ProductionEventType
    occurred_at: datetime

    operation_id: uuid.UUID | None = None
    execution_id: uuid.UUID | None = None
    employee_id: uuid.UUID | None = None

    reason_code: str | None = None
    notes: str | None = None

    id: uuid.UUID | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_uuid(
            self.tenant_id,
            "tenant",
        )

        self._validate_uuid(
            self.production_order_id,
            "ordem de produção",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                "identificador",
            )

        if self.operation_id is not None:
            self._validate_uuid(
                self.operation_id,
                "operação",
            )

        if self.execution_id is not None:
            self._validate_uuid(
                self.execution_id,
                "execução",
            )

        if self.employee_id is not None:
            self._validate_uuid(
                self.employee_id,
                "funcionário",
            )

        if not isinstance(
            self.event_type,
            ProductionEventType,
        ):
            raise TypeError(
                "O tipo do evento deve ser ProductionEventType."
            )

        if (
            self.execution_id is not None
            and self.operation_id is None
        ):
            raise ValueError(
                "Um evento de execução deve informar a operação."
            )

        self.reason_code = self._normalize_optional_code(
            self.reason_code
        )

        self.notes = self._normalize_optional_text(
            self.notes
        )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        production_order_id: uuid.UUID,
        event_type: ProductionEventType,
        operation_id: uuid.UUID | None = None,
        execution_id: uuid.UUID | None = None,
        employee_id: uuid.UUID | None = None,
        reason_code: str | None = None,
        notes: str | None = None,
        occurred_at: datetime | None = None,
    ) -> ProductionEvent:
        """Create an operational event."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            production_order_id=production_order_id,
            operation_id=operation_id,
            execution_id=execution_id,
            employee_id=employee_id,
            event_type=event_type,
            reason_code=reason_code,
            notes=notes,
            occurred_at=occurred_at or now,
            created_at=now,
            updated_at=now,
        )

    @staticmethod
    def _normalize_optional_code(
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        normalized = value.strip().upper()

        return normalized or None

    @staticmethod
    def _normalize_optional_text(
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        normalized = value.strip()

        return normalized or None

    @staticmethod
    def _validate_uuid(
        value: object,
        field_name: str,
    ) -> None:
        if not isinstance(
            value,
            uuid.UUID,
        ):
            raise TypeError(
                f"O {field_name} deve ser um UUID."
            )

        if value.int == 0:
            raise ValueError(
                f"O {field_name} não pode possuir UUID nulo."
            )
