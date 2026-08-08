"""Material domain value objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MaterialCode:
    """Represent a normalized material code."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()

        if not normalized:
            raise ValueError(
                "O código do material é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class MaterialName:
    """Represent a normalized material name."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError(
                "O nome do material é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class MaterialCategory:
    """Represent a normalized material category."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError(
                "A categoria do material é obrigatória."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class MaterialUnit:
    """Represent a normalized material measurement unit."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()

        if not normalized:
            raise ValueError(
                "A unidade do material é obrigatória."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )
