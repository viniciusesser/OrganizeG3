"""Machine domain value objects."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class MachineStatus(StrEnum):
    """Represent the operational state of a machine."""

    AVAILABLE = "AVAILABLE"
    IN_USE = "IN_USE"
    MAINTENANCE = "MAINTENANCE"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"


@dataclass(frozen=True, slots=True)
class MachineCode:
    """Represent a normalized machine code."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()

        if not normalized:
            raise ValueError(
                "O código da máquina é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class MachineName:
    """Represent a normalized machine name."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError(
                "O nome da máquina é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class MachineType:
    """Represent a normalized machine type."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError(
                "O tipo da máquina é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class OptionalMachineText:
    """Represent an optional normalized machine text."""

    value: str | None

    def __post_init__(self) -> None:
        if self.value is None:
            return

        normalized = self.value.strip()

        object.__setattr__(
            self,
            "value",
            normalized or None,
        )
