"""Production operation checklist item domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import uuid


@dataclass(slots=True)
class ProductionChecklistItem:
    """Represent one checklist requirement of a production operation."""

    tenant_id: uuid.UUID
    production_operation_id: uuid.UUID
    sequence: int
    title: str

    is_required: bool = True
    is_applicable: bool = True

    completed_at: datetime | None = None
    completed_by_employee_id: uuid.UUID | None = None

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
            self.production_operation_id,
            "operação de produção",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                "identificador",
            )

        if self.completed_by_employee_id is not None:
            self._validate_uuid(
                self.completed_by_employee_id,
                "funcionário responsável pela conclusão",
            )

        self._validate_sequence()

        self.title = self._normalize_required_text(
            self.title,
            "título do item",
        )
        self.notes = self._normalize_optional_text(
            self.notes
        )

        if self.completed_at is not None:
            self.completed_at = self._ensure_utc(
                self.completed_at,
                "data de conclusão",
            )

        if (
            self.completed_by_employee_id is not None
            and self.completed_at is None
        ):
            raise ValueError(
                "Um funcionário de conclusão exige "
                "uma data de conclusão."
            )

        if not self.is_applicable and self.completed_at is not None:
            raise ValueError(
                "Um item não aplicável não pode estar concluído."
            )

        if (
            not self.is_applicable
            and self.completed_by_employee_id is not None
        ):
            raise ValueError(
                "Um item não aplicável não pode possuir "
                "funcionário de conclusão."
            )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: uuid.UUID,
        production_operation_id: uuid.UUID,
        sequence: int,
        title: str,
        is_required: bool = True,
        notes: str | None = None,
    ) -> ProductionChecklistItem:
        """Create one applicable and pending checklist item."""

        now = datetime.now(UTC)

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            production_operation_id=production_operation_id,
            sequence=sequence,
            title=title,
            is_required=is_required,
            is_applicable=True,
            completed_at=None,
            completed_by_employee_id=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )

    @property
    def is_completed(self) -> bool:
        """Return whether the applicable item is completed."""

        return (
            self.is_applicable
            and self.completed_at is not None
        )

    @property
    def is_pending(self) -> bool:
        """Return whether the item still requires action."""

        return (
            self.is_applicable
            and self.completed_at is None
        )

    def complete(
        self,
        *,
        employee_id: uuid.UUID | None = None,
        completed_at: datetime | None = None,
        notes: str | None = None,
    ) -> None:
        """Complete the checklist item."""

        if not self.is_applicable:
            raise ValueError(
                "Um item não aplicável não pode ser concluído."
            )

        if self.completed_at is not None:
            raise ValueError(
                "O item de checklist já está concluído."
            )

        if employee_id is not None:
            self._validate_uuid(
                employee_id,
                "funcionário responsável pela conclusão",
            )

        effective_at = self._ensure_utc(
            completed_at or datetime.now(UTC),
            "data de conclusão",
        )

        self.completed_at = effective_at
        self.completed_by_employee_id = employee_id

        if notes is not None:
            self.notes = self._normalize_optional_text(
                notes
            )

        self._touch()

    def reopen(self) -> None:
        """Reopen a completed checklist item."""

        if not self.is_applicable:
            raise ValueError(
                "Um item não aplicável não pode ser reaberto."
            )

        if self.completed_at is None:
            raise ValueError(
                "Somente itens concluídos podem ser reabertos."
            )

        self.completed_at = None
        self.completed_by_employee_id = None
        self._touch()

    def mark_not_applicable(
        self,
        *,
        notes: str | None = None,
    ) -> None:
        """Record that the checklist item does not apply."""

        if self.completed_at is not None:
            raise ValueError(
                "Um item concluído deve ser reaberto antes "
                "de ser marcado como não aplicável."
            )

        self.is_applicable = False
        self.completed_by_employee_id = None

        if notes is not None:
            self.notes = self._normalize_optional_text(
                notes
            )

        self._touch()

    def restore_applicability(self) -> None:
        """Return a non-applicable item to pending state."""

        if self.is_applicable:
            raise ValueError(
                "O item já está marcado como aplicável."
            )

        self.is_applicable = True
        self.completed_at = None
        self.completed_by_employee_id = None
        self._touch()

    def _validate_sequence(self) -> None:
        if isinstance(
            self.sequence,
            bool,
        ):
            raise TypeError(
                "A sequência do checklist deve ser inteira."
            )

        if not isinstance(
            self.sequence,
            int,
        ):
            raise TypeError(
                "A sequência do checklist deve ser inteira."
            )

        if self.sequence <= 0:
            raise ValueError(
                "A sequência do checklist deve ser maior que zero."
            )

    @staticmethod
    def _normalize_required_text(
        value: str,
        field_name: str,
    ) -> str:
        if not isinstance(
            value,
            str,
        ):
            raise TypeError(
                f"O {field_name} deve ser texto."
            )

        normalized = value.strip()

        if not normalized:
            raise ValueError(
                f"O {field_name} é obrigatório."
            )

        return normalized

    @staticmethod
    def _normalize_optional_text(
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        if not isinstance(
            value,
            str,
        ):
            raise TypeError(
                "As observações devem ser texto."
            )

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
