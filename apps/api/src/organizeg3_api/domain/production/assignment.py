"""Production employee assignment domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import uuid


@dataclass(slots=True)
class ProductionAssignment:
    """Represent an employee assignment to a production operation."""

    tenant_id: uuid.UUID
    production_operation_id: uuid.UUID
    employee_id: uuid.UUID
    assigned_at: datetime

    assigned_by_user_id: uuid.UUID | None = None
    unassigned_at: datetime | None = None
    is_active: bool = True

    id: uuid.UUID | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_uuid(
            self.tenant_id,
            "tenant",
        )
        self._validate_uuid(
            self.production_operation_id,
            "operação de produção",
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

        if self.assigned_by_user_id is not None:
            self._validate_uuid(
                self.assigned_by_user_id,
                "usuário responsável pela atribuição",
            )

        self.assigned_at = self._ensure_utc(
            self.assigned_at,
            "data de atribuição",
        )

        if self.unassigned_at is not None:
            self.unassigned_at = self._ensure_utc(
                self.unassigned_at,
                "data de desatribuição",
            )

            if self.unassigned_at < self.assigned_at:
                raise ValueError(
                    "A desatribuição não pode anteceder "
                    "a atribuição."
                )

        if self.is_active and self.unassigned_at is not None:
            raise ValueError(
                "Uma atribuição ativa não pode possuir "
                "data de desatribuição."
            )

        if not self.is_active and self.unassigned_at is None:
            raise ValueError(
                "Uma atribuição inativa deve possuir "
                "data de desatribuição."
            )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        production_operation_id: uuid.UUID,
        employee_id: uuid.UUID,
        assigned_by_user_id: uuid.UUID | None = None,
        assigned_at: datetime | None = None,
    ) -> ProductionAssignment:
        """Create one active employee assignment."""

        now = datetime.now(UTC)
        effective_assigned_at = assigned_at or now

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            production_operation_id=production_operation_id,
            employee_id=employee_id,
            assigned_at=effective_assigned_at,
            assigned_by_user_id=assigned_by_user_id,
            unassigned_at=None,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def unassign(
        self,
        *,
        at: datetime | None = None,
    ) -> None:
        """Close the active assignment while preserving history."""

        if not self.is_active:
            raise ValueError(
                "A atribuição já está inativa."
            )

        effective_at = self._ensure_utc(
            at or datetime.now(UTC),
            "data de desatribuição",
        )

        if effective_at < self.assigned_at:
            raise ValueError(
                "A desatribuição não pode anteceder "
                "a atribuição."
            )

        self.unassigned_at = effective_at
        self.is_active = False
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

    @staticmethod
    def _ensure_utc(
        value: datetime,
        field_name: str,
    ) -> datetime:
        if value.tzinfo is None:
            raise ValueError(
                f"A {field_name} deve possuir timezone."
            )

        return value.astimezone(UTC)

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)
