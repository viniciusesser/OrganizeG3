"""Employee domain value objects."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import re

_NON_DIGIT_PATTERN = re.compile(r"\D+")

_CPF_LENGTH = 11
_CPF_REMAINDER_ZERO_THRESHOLD = 2
_PHONE_MAX_LOCAL_LENGTH = 11

_VALID_PHONE_LENGTHS = {
    10,
    11,
}


def normalize_optional_text(
    value: str | None,
) -> str | None:
    """Normalize optional text values."""

    if value is None:
        return None

    normalized = value.strip()

    if not normalized:
        return None

    return normalized


class EmploymentStatus(StrEnum):
    """Supported employee employment states."""

    ACTIVE = "ACTIVE"
    ON_LEAVE = "ON_LEAVE"
    INACTIVE = "INACTIVE"
    TERMINATED = "TERMINATED"


@dataclass(frozen=True, slots=True)
class EmployeeCode:
    """Represent a normalized employee code."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()

        if not normalized:
            raise ValueError(
                "O código do funcionário é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class EmployeeDocument:
    """Represent a valid normalized Brazilian CPF."""

    value: str

    def __post_init__(self) -> None:
        normalized = _NON_DIGIT_PATTERN.sub(
            "",
            self.value,
        )

        if len(normalized) != _CPF_LENGTH:
            raise ValueError(
                "O CPF do funcionário deve conter 11 dígitos."
            )

        if len(set(normalized)) == 1:
            raise ValueError(
                "O CPF do funcionário é inválido."
            )

        if not self._has_valid_check_digits(
            normalized
        ):
            raise ValueError(
                "O CPF do funcionário é inválido."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )

    @staticmethod
    def _calculate_digit(
        digits: str,
    ) -> int:
        weight = len(digits) + 1

        total = sum(
            int(digit) * (
                weight - index
            )
            for index, digit in enumerate(
                digits
            )
        )

        remainder = total % 11

        if (
            remainder
            < _CPF_REMAINDER_ZERO_THRESHOLD
        ):
            return 0

        return 11 - remainder

    @classmethod
    def _has_valid_check_digits(
        cls,
        value: str,
    ) -> bool:
        first_digit = cls._calculate_digit(
            value[:9]
        )

        second_digit = cls._calculate_digit(
            value[:9]
            + str(first_digit)
        )

        return value[-2:] == (
            f"{first_digit}{second_digit}"
        )


@dataclass(frozen=True, slots=True)
class EmployeeEmail:
    """Represent a normalized employee email."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()

        if (
            not normalized
            or normalized.count("@") != 1
        ):
            raise ValueError(
                "O e-mail do funcionário é inválido."
            )

        local_part, domain = normalized.split(
            "@",
            maxsplit=1,
        )

        if (
            not local_part
            or not domain
            or "." not in domain
        ):
            raise ValueError(
                "O e-mail do funcionário é inválido."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class EmployeePhone:
    """Represent a normalized Brazilian employee phone."""

    value: str

    def __post_init__(self) -> None:
        normalized = _NON_DIGIT_PATTERN.sub(
            "",
            self.value,
        )

        if (
            len(normalized)
            > _PHONE_MAX_LOCAL_LENGTH
            and normalized.startswith("55")
        ):
            normalized = normalized[2:]

        if len(normalized) not in _VALID_PHONE_LENGTHS:
            raise ValueError(
                "O telefone do funcionário é inválido."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )
