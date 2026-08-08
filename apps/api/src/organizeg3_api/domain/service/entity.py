"""Service domain entity."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
import uuid

from organizeg3_api.domain.service.value_objects import (
    EstimatedDurationMinutes,
    ServiceCategory,
    ServiceCode,
    ServiceExecutionMode,
    ServiceName,
    ServiceUnit,
)


@dataclass(slots=True)
class Service:
    """Represent a tenant-scoped service catalog item."""

    tenant_id: uuid.UUID
    code: str
    name: str
    category: str
    unit: str
    execution_mode: ServiceExecutionMode

    id: uuid.UUID | None = None
    estimated_duration_minutes: int | None = None

    is_active: bool = True

    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        """Validate and normalize service state."""

        self._validate_uuid(
            self.tenant_id,
            field_name="tenant",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                field_name="identificador",
            )

        self.code = ServiceCode(
            self.code
        ).value

        self.name = ServiceName(
            self.name
        ).value

        self.category = ServiceCategory(
            self.category
        ).value

        self.unit = ServiceUnit(
            self.unit
        ).value

        self.execution_mode = (
            self._normalize_execution_mode(
                self.execution_mode
            )
        )

        if self.estimated_duration_minutes is not None:
            self.estimated_duration_minutes = (
                EstimatedDurationMinutes(
                    self.estimated_duration_minutes
                ).value
            )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        code: str,
        name: str,
        category: str,
        unit: str,
        execution_mode: ServiceExecutionMode,
        estimated_duration_minutes: int | None = None,
    ) -> Service:
        """Create a new active service."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            code=code,
            name=name,
            category=category,
            unit=unit,
            execution_mode=execution_mode,
            estimated_duration_minutes=(
                estimated_duration_minutes
            ),
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def update_details(
        self,
        *,
        code: str,
        name: str,
        category: str,
        unit: str,
        execution_mode: ServiceExecutionMode,
        estimated_duration_minutes: int | None,
    ) -> None:
        """Atomically validate and update service details."""

        candidate = replace(
            self,
            code=code,
            name=name,
            category=category,
            unit=unit,
            execution_mode=execution_mode,
            estimated_duration_minutes=(
                estimated_duration_minutes
            ),
        )

        changed = (
            self.code != candidate.code
            or self.name != candidate.name
            or self.category != candidate.category
            or self.unit != candidate.unit
            or self.execution_mode != candidate.execution_mode
            or (
                self.estimated_duration_minutes
                != candidate.estimated_duration_minutes
            )
        )

        if not changed:
            return

        self.code = candidate.code
        self.name = candidate.name
        self.category = candidate.category
        self.unit = candidate.unit
        self.execution_mode = candidate.execution_mode
        self.estimated_duration_minutes = (
            candidate.estimated_duration_minutes
        )

        self._touch()

    def change_execution_mode(
        self,
        execution_mode: ServiceExecutionMode,
    ) -> None:
        """Change where the service may be executed."""

        normalized = self._normalize_execution_mode(
            execution_mode
        )

        if self.execution_mode == normalized:
            return

        self.execution_mode = normalized
        self._touch()

    def change_estimated_duration(
        self,
        estimated_duration_minutes: int | None,
    ) -> None:
        """Change or clear the planning duration estimate."""

        normalized: int | None

        if estimated_duration_minutes is None:
            normalized = None
        else:
            normalized = EstimatedDurationMinutes(
                estimated_duration_minutes
            ).value

        if (
            self.estimated_duration_minutes
            == normalized
        ):
            return

        self.estimated_duration_minutes = normalized
        self._touch()

    def deactivate(self) -> None:
        """Deactivate the service."""

        if not self.is_active:
            return

        self.is_active = False
        self._touch()

    def activate(self) -> None:
        """Reactivate the service."""

        if self.is_active:
            return

        self.is_active = True
        self._touch()

    @staticmethod
    def _normalize_execution_mode(
        value: ServiceExecutionMode,
    ) -> ServiceExecutionMode:
        if not isinstance(
            value,
            ServiceExecutionMode,
        ):
            raise TypeError(
                "O modo de execução do serviço "
                "deve ser um ServiceExecutionMode."
            )

        return value

    @staticmethod
    def _validate_uuid(
        value: object,
        *,
        field_name: str,
    ) -> None:
        if not isinstance(
            value,
            uuid.UUID,
        ):
            raise TypeError(
                f"O {field_name} do serviço "
                "deve ser um UUID."
            )

        if value.int == 0:
            raise ValueError(
                f"O {field_name} do serviço "
                "não pode possuir UUID nulo."
            )

    @staticmethod
    def _next_timestamp(
        previous: datetime | None,
    ) -> datetime:
        """Return a UTC timestamp newer than the previous value."""

        now = datetime.now(UTC)

        if previous is None:
            return now

        if previous.tzinfo is None:
            normalized_previous = previous.replace(
                tzinfo=UTC
            )
        else:
            normalized_previous = previous.astimezone(
                UTC
            )

        if now > normalized_previous:
            return now

        return (
            normalized_previous
            + timedelta(
                microseconds=1
            )
        )

    def _touch(self) -> None:
        self.updated_at = self._next_timestamp(
            self.updated_at
        )
