"""Production domain value objects."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ProductionOrderStatus(StrEnum):
    """Represent the lifecycle state of a production order."""

    PLANNED = "PLANNED"
    RELEASED = "RELEASED"
    IN_PROGRESS = "IN_PROGRESS"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ProductionOperationStatus(StrEnum):
    """Represent the lifecycle state of a production operation."""

    PENDING = "PENDING"
    READY = "READY"
    IN_PROGRESS = "IN_PROGRESS"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    CANCELLED = "CANCELLED"


class ProductionExecutionStatus(StrEnum):
    """Represent the state of one employee execution."""

    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ProductionPriority(StrEnum):
    """Represent production planning priority."""

    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"


@dataclass(frozen=True, slots=True)
class ProductionCode:
    """Represent a normalized production order code."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()

        if not normalized:
            raise ValueError(
                "O código da ordem de produção é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class ProductionTitle:
    """Represent a normalized production title."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError(
                "O título da ordem de produção é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class OperationName:
    """Represent a normalized production operation name."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError(
                "O nome da operação é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class OperationSequence:
    """Represent a positive operation sequence."""

    value: int

    def __post_init__(self) -> None:
        if isinstance(
            self.value,
            bool,
        ):
            raise TypeError(
                "A sequência da operação deve ser inteira."
            )

        if not isinstance(
            self.value,
            int,
        ):
            raise TypeError(
                "A sequência da operação deve ser inteira."
            )

        if self.value <= 0:
            raise ValueError(
                "A sequência da operação deve ser maior que zero."
            )
