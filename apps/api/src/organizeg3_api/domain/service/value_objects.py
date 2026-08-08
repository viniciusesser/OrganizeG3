"""Service domain value objects."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ServiceExecutionMode(StrEnum):
    """Define where a service may normally be executed."""

    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"
    BOTH = "BOTH"


@dataclass(frozen=True, slots=True)
class ServiceCode:
    """Represent a normalized service code."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()

        if not normalized:
            raise ValueError(
                "O código do serviço é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class ServiceName:
    """Represent a normalized service name."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError(
                "O nome do serviço é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class ServiceCategory:
    """Represent a normalized service category."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError(
                "A categoria do serviço é obrigatória."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class ServiceUnit:
    """Represent a normalized service measurement unit."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()

        if not normalized:
            raise ValueError(
                "A unidade do serviço é obrigatória."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class EstimatedDurationMinutes:
    """Represent an optional positive service duration estimate."""

    value: int

    def __post_init__(self) -> None:
        if isinstance(
            self.value,
            bool,
        ):
            raise TypeError(
                "A duração estimada deve ser um número inteiro."
            )

        if not isinstance(
            self.value,
            int,
        ):
            raise TypeError(
                "A duração estimada deve ser um número inteiro."
            )

        if self.value <= 0:
            raise ValueError(
                "A duração estimada deve ser maior que zero."
            )
