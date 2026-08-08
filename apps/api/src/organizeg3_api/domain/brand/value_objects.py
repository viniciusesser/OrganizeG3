"""Brand domain value objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BrandCode:
    """Represent a normalized brand code."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()

        if not normalized:
            raise ValueError(
                "O código da marca é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class BrandName:
    """Represent a normalized brand name."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError(
                "O nome da marca é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )
