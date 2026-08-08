"""Production order aggregate root."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import uuid

from organizeg3_api.domain.production.value_objects import (
    ProductionCode,
    ProductionOrderStatus,
    ProductionPriority,
    ProductionTitle,
)


@dataclass(slots=True)
class ProductionOrder:
    """Represent one tenant-scoped production order."""

    tenant_id: uuid.UUID
    code: str
    title: str

    branch_id: uuid.UUID | None = None

    status: ProductionOrderStatus = ProductionOrderStatus.PLANNED
    priority: ProductionPriority = ProductionPriority.NORMAL

    planned_start_at: datetime | None = None
    planned_end_at: datetime | None = None

    id: uuid.UUID | None = None

    is_active: bool = True

    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_uuid(
            self.tenant_id,
            "tenant",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                "identificador",
            )

        if self.branch_id is not None:
            self._validate_uuid(
                self.branch_id,
                "filial",
            )

        self.code = ProductionCode(
            self.code
        ).value

        self.title = ProductionTitle(
            self.title
        ).value

        if not isinstance(
            self.status,
            ProductionOrderStatus,
        ):
            raise TypeError(
                "O status da ordem deve ser ProductionOrderStatus."
            )

        if not isinstance(
            self.priority,
            ProductionPriority,
        ):
            raise TypeError(
                "A prioridade da ordem deve ser ProductionPriority."
            )

        self._validate_planning_dates()

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        code: str,
        title: str,
        branch_id: uuid.UUID | None = None,
        priority: ProductionPriority = ProductionPriority.NORMAL,
        planned_start_at: datetime | None = None,
        planned_end_at: datetime | None = None,
    ) -> ProductionOrder:
        """Create one planned production order."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            branch_id=branch_id,
            code=code,
            title=title,
            status=ProductionOrderStatus.PLANNED,
            priority=priority,
            planned_start_at=planned_start_at,
            planned_end_at=planned_end_at,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def release(self) -> None:
        """Release the order to production."""

        if self.status is not ProductionOrderStatus.PLANNED:
            raise ValueError(
                "Somente ordens planejadas podem ser liberadas."
            )

        self.status = ProductionOrderStatus.RELEASED
        self._touch()

    def start(self) -> None:
        """Start production."""

        if self.status not in {
            ProductionOrderStatus.RELEASED,
            ProductionOrderStatus.PAUSED,
        }:
            raise ValueError(
                "A ordem não pode ser iniciada no status atual."
            )

        self.status = ProductionOrderStatus.IN_PROGRESS
        self._touch()

    def pause(self) -> None:
        """Pause production."""

        if self.status is not ProductionOrderStatus.IN_PROGRESS:
            raise ValueError(
                "Somente ordens em produção podem ser pausadas."
            )

        self.status = ProductionOrderStatus.PAUSED
        self._touch()

    def complete(self) -> None:
        """Complete production."""

        if self.status not in {
            ProductionOrderStatus.IN_PROGRESS,
            ProductionOrderStatus.PAUSED,
        }:
            raise ValueError(
                "A ordem não pode ser concluída no status atual."
            )

        self.status = ProductionOrderStatus.COMPLETED
        self._touch()

    def cancel(self) -> None:
        """Cancel an unfinished production order."""

        if self.status is ProductionOrderStatus.COMPLETED:
            raise ValueError(
                "Uma ordem concluída não pode ser cancelada."
            )

        if self.status is ProductionOrderStatus.CANCELLED:
            return

        self.status = ProductionOrderStatus.CANCELLED
        self._touch()

    def assign_branch(
        self,
        branch_id: uuid.UUID,
    ) -> None:
        """Assign the production order to a branch."""

        self._validate_uuid(
            branch_id,
            "filial",
        )

        if self.branch_id == branch_id:
            return

        self.branch_id = branch_id
        self._touch()

    def remove_branch(self) -> None:
        """Remove optional branch assignment."""

        if self.branch_id is None:
            return

        self.branch_id = None
        self._touch()

    def deactivate(self) -> None:
        """Deactivate the production order."""

        if not self.is_active:
            return

        self.is_active = False
        self._touch()

    def activate(self) -> None:
        """Reactivate the production order."""

        if self.is_active:
            return

        self.is_active = True
        self._touch()

    def _validate_planning_dates(self) -> None:
        if (
            self.planned_start_at is not None
            and self.planned_end_at is not None
            and self.planned_end_at < self.planned_start_at
        ):
            raise ValueError(
                "O término planejado não pode anteceder o início."
            )

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
