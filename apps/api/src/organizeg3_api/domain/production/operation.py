"""Production operation domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import uuid

from organizeg3_api.domain.production.value_objects import (
    OperationName,
    OperationSequence,
    ProductionOperationStatus,
)


@dataclass(slots=True)
class ProductionOperation:
    """Represent one ordered operation of a production order."""

    tenant_id: uuid.UUID
    production_order_id: uuid.UUID
    sequence: int
    name: str

    service_id: uuid.UUID | None = None
    machine_id: uuid.UUID | None = None

    status: ProductionOperationStatus = ProductionOperationStatus.PENDING
    is_applicable: bool = True

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

        if self.service_id is not None:
            self._validate_uuid(
                self.service_id,
                "serviço",
            )

        if self.machine_id is not None:
            self._validate_uuid(
                self.machine_id,
                "máquina",
            )

        self.sequence = OperationSequence(
            self.sequence
        ).value

        self.name = OperationName(
            self.name
        ).value

        if not isinstance(
            self.status,
            ProductionOperationStatus,
        ):
            raise TypeError(
                "O status da operação deve ser "
                "ProductionOperationStatus."
            )

        if not self.is_applicable:
            self.status = (
                ProductionOperationStatus.NOT_APPLICABLE
            )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        production_order_id: uuid.UUID,
        sequence: int,
        name: str,
        service_id: uuid.UUID | None = None,
        machine_id: uuid.UUID | None = None,
    ) -> ProductionOperation:
        """Create one pending production operation."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            production_order_id=production_order_id,
            sequence=sequence,
            name=name,
            service_id=service_id,
            machine_id=machine_id,
            status=ProductionOperationStatus.PENDING,
            is_applicable=True,
            created_at=now,
            updated_at=now,
        )

    def mark_ready(self) -> None:
        """Mark the operation as ready for execution."""

        if self.status is not ProductionOperationStatus.PENDING:
            raise ValueError(
                "Somente operações pendentes podem ficar prontas."
            )

        self.status = ProductionOperationStatus.READY
        self._touch()

    def start(self) -> None:
        """Start or resume the operation."""

        if self.status not in {
            ProductionOperationStatus.READY,
            ProductionOperationStatus.PAUSED,
        }:
            raise ValueError(
                "A operação não pode ser iniciada no status atual."
            )

        self.status = ProductionOperationStatus.IN_PROGRESS
        self._touch()

    def pause(self) -> None:
        """Pause the operation."""

        if self.status is not ProductionOperationStatus.IN_PROGRESS:
            raise ValueError(
                "Somente operações em andamento podem ser pausadas."
            )

        self.status = ProductionOperationStatus.PAUSED
        self._touch()

    def complete(self) -> None:
        """Complete the operation."""

        if self.status not in {
            ProductionOperationStatus.IN_PROGRESS,
            ProductionOperationStatus.PAUSED,
        }:
            raise ValueError(
                "A operação não pode ser concluída no status atual."
            )

        self.status = ProductionOperationStatus.COMPLETED
        self._touch()

    def mark_not_applicable(self) -> None:
        """Record that the operation is not applicable."""

        if self.status in {
            ProductionOperationStatus.IN_PROGRESS,
            ProductionOperationStatus.COMPLETED,
        }:
            raise ValueError(
                "A operação em execução ou concluída "
                "não pode virar não aplicável."
            )

        self.is_applicable = False
        self.status = ProductionOperationStatus.NOT_APPLICABLE
        self._touch()

    def reopen(self) -> None:
        """Return an operation for correction or rework."""

        if self.status not in {
            ProductionOperationStatus.COMPLETED,
            ProductionOperationStatus.NOT_APPLICABLE,
        }:
            raise ValueError(
                "Somente operações encerradas podem ser reabertas."
            )

        self.is_applicable = True
        self.status = ProductionOperationStatus.READY
        self._touch()

    def assign_machine(
        self,
        machine_id: uuid.UUID,
    ) -> None:
        """Assign or replace an operation machine."""

        self._validate_uuid(
            machine_id,
            "máquina",
        )

        if self.machine_id == machine_id:
            return

        self.machine_id = machine_id
        self._touch()

    def remove_machine(self) -> None:
        """Remove optional machine assignment."""

        if self.machine_id is None:
            return

        self.machine_id = None
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
