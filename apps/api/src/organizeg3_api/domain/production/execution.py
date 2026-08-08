"""Production execution domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import uuid

from organizeg3_api.domain.production.value_objects import (
    ProductionExecutionStatus,
)


@dataclass(slots=True)
class ProductionExecution:
    """Represent one employee execution of a production operation."""

    tenant_id: uuid.UUID
    operation_id: uuid.UUID
    employee_id: uuid.UUID

    started_at: datetime

    status: ProductionExecutionStatus = ProductionExecutionStatus.RUNNING

    finished_at: datetime | None = None

    id: uuid.UUID | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_uuid(
            self.tenant_id,
            "tenant",
        )

        self._validate_uuid(
            self.operation_id,
            "operação",
        )

        self._validate_uuid(
            self.employee_id,
            "funcionário",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                "identificador",
            )

        if not isinstance(
            self.status,
            ProductionExecutionStatus,
        ):
            raise TypeError(
                "O status da execução deve ser "
                "ProductionExecutionStatus."
            )

        if (
            self.finished_at is not None
            and self.finished_at < self.started_at
        ):
            raise ValueError(
                "O término da execução não pode anteceder o início."
            )

    @classmethod
    def start(
        cls,
        *,
        tenant_id: uuid.UUID,
        operation_id: uuid.UUID,
        employee_id: uuid.UUID,
        started_at: datetime | None = None,
    ) -> ProductionExecution:
        """Start one employee execution."""

        now = datetime.now(UTC)
        effective_start = started_at or now

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            operation_id=operation_id,
            employee_id=employee_id,
            started_at=effective_start,
            status=ProductionExecutionStatus.RUNNING,
            finished_at=None,
            created_at=now,
            updated_at=now,
        )

    def pause(self) -> None:
        """Pause the current execution."""

        if self.status is not ProductionExecutionStatus.RUNNING:
            raise ValueError(
                "Somente execuções em andamento podem ser pausadas."
            )

        self.status = ProductionExecutionStatus.PAUSED
        self._touch()

    def resume(self) -> None:
        """Resume a paused execution."""

        if self.status is not ProductionExecutionStatus.PAUSED:
            raise ValueError(
                "Somente execuções pausadas podem ser retomadas."
            )

        self.status = ProductionExecutionStatus.RUNNING
        self._touch()

    def complete(
        self,
        *,
        finished_at: datetime | None = None,
    ) -> None:
        """Finish the execution."""

        if self.status not in {
            ProductionExecutionStatus.RUNNING,
            ProductionExecutionStatus.PAUSED,
        }:
            raise ValueError(
                "A execução não pode ser concluída no status atual."
            )

        effective_finish = finished_at or datetime.now(UTC)

        if effective_finish < self.started_at:
            raise ValueError(
                "O término da execução não pode anteceder o início."
            )

        self.finished_at = effective_finish
        self.status = ProductionExecutionStatus.COMPLETED
        self._touch()

    def cancel(self) -> None:
        """Cancel an unfinished execution."""

        if self.status is ProductionExecutionStatus.COMPLETED:
            raise ValueError(
                "Uma execução concluída não pode ser cancelada."
            )

        if self.status is ProductionExecutionStatus.CANCELLED:
            return

        self.status = ProductionExecutionStatus.CANCELLED
        self._touch()

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

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)
