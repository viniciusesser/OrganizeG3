"""Production execution pause domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import uuid


@dataclass(slots=True)
class ProductionPause:
    """Represent one measurable pause during an execution."""

    tenant_id: uuid.UUID
    execution_id: uuid.UUID
    reason_code: str
    started_at: datetime

    ended_at: datetime | None = None
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
            self.execution_id,
            "execução",
        )

        if self.id is not None:
            self._validate_uuid(
                self.id,
                "identificador",
            )

        self.reason_code = self._normalize_required_text(
            self.reason_code,
            field_name="motivo da pausa",
            uppercase=True,
        )

        self.notes = self._normalize_optional_text(
            self.notes
        )

        if (
            self.ended_at is not None
            and self.ended_at < self.started_at
        ):
            raise ValueError(
                "O término da pausa não pode anteceder o início."
            )

    @classmethod
    def start(
        cls,
        *,
        tenant_id: uuid.UUID,
        execution_id: uuid.UUID,
        reason_code: str,
        notes: str | None = None,
        started_at: datetime | None = None,
    ) -> ProductionPause:
        """Start a measurable production pause."""

        now = datetime.now(UTC)
        effective_start = started_at or now

        return cls(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            execution_id=execution_id,
            reason_code=reason_code,
            started_at=effective_start,
            ended_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )

    @property
    def is_open(self) -> bool:
        """Return whether this pause is still running."""

        return self.ended_at is None

    def finish(
        self,
        *,
        ended_at: datetime | None = None,
    ) -> None:
        """Finish the pause."""

        if not self.is_open:
            raise ValueError(
                "A pausa já foi encerrada."
            )

        effective_end = ended_at or datetime.now(UTC)

        if effective_end < self.started_at:
            raise ValueError(
                "O término da pausa não pode anteceder o início."
            )

        self.ended_at = effective_end
        self._touch()

    @staticmethod
    def _normalize_required_text(
        value: str,
        *,
        field_name: str,
        uppercase: bool = False,
    ) -> str:
        normalized = value.strip()

        if uppercase:
            normalized = normalized.upper()

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

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)
