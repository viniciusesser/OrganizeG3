"""Supplier domain value objects."""

from __future__ import annotations

from dataclasses import dataclass
import re

_NON_DIGIT_PATTERN = re.compile(r"\D+")

_CPF_LENGTH = 11
_CNPJ_LENGTH = 14

_CPF_BASE_LENGTH = 9
_CNPJ_BASE_LENGTH = 12

_CHECK_DIGIT_ZERO_THRESHOLD = 2
_CHECK_DIGIT_MODULUS = 11

_PHONE_LENGTHS = {
    10,
    11,
}
_PHONE_MAX_LOCAL_LENGTH = 11

_BRAZIL_COUNTRY_CODE = "55"

_POSTAL_CODE_LENGTH = 8
_STATE_CODE_LENGTH = 2


def normalize_optional_text(
    value: str | None,
) -> str | None:
    """Normalize optional textual values."""

    if value is None:
        return None

    normalized = value.strip()

    if not normalized:
        return None

    return normalized


@dataclass(frozen=True, slots=True)
class SupplierCode:
    """Represent a normalized supplier code."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()

        if not normalized:
            raise ValueError(
                "O código do fornecedor é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class SupplierDocument:
    """Represent a valid CPF or CNPJ."""

    value: str

    def __post_init__(self) -> None:
        normalized = _NON_DIGIT_PATTERN.sub(
            "",
            self.value,
        )

        if len(normalized) == _CPF_LENGTH:
            if not self._is_valid_cpf(
                normalized
            ):
                raise ValueError(
                    "O CPF do fornecedor é inválido."
                )

        elif len(normalized) == _CNPJ_LENGTH:
            if not self._is_valid_cnpj(
                normalized
            ):
                raise ValueError(
                    "O CNPJ do fornecedor é inválido."
                )

        else:
            raise ValueError(
                "O documento do fornecedor deve ser "
                "um CPF ou CNPJ válido."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )

    @staticmethod
    def _is_repeated(
        value: str,
    ) -> bool:
        return len(set(value)) == 1

    @classmethod
    def _is_valid_cpf(
        cls,
        value: str,
    ) -> bool:
        if cls._is_repeated(value):
            return False

        first_digit = cls._calculate_cpf_digit(
            value[:_CPF_BASE_LENGTH]
        )

        second_digit = cls._calculate_cpf_digit(
            value[:_CPF_BASE_LENGTH]
            + str(first_digit)
        )

        return value[-2:] == (
            f"{first_digit}{second_digit}"
        )

    @staticmethod
    def _calculate_cpf_digit(
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

        remainder = (
            total
            % _CHECK_DIGIT_MODULUS
        )

        if (
            remainder
            < _CHECK_DIGIT_ZERO_THRESHOLD
        ):
            return 0

        return (
            _CHECK_DIGIT_MODULUS
            - remainder
        )

    @classmethod
    def _is_valid_cnpj(
        cls,
        value: str,
    ) -> bool:
        if cls._is_repeated(value):
            return False

        first_digit = cls._calculate_cnpj_digit(
            value[:_CNPJ_BASE_LENGTH]
        )

        second_digit = cls._calculate_cnpj_digit(
            value[:_CNPJ_BASE_LENGTH]
            + str(first_digit)
        )

        return value[-2:] == (
            f"{first_digit}{second_digit}"
        )

    @staticmethod
    def _calculate_cnpj_digit(
        digits: str,
    ) -> int:
        weights = (
            (
                5,
                4,
                3,
                2,
                9,
                8,
                7,
                6,
                5,
                4,
                3,
                2,
            )
            if len(digits)
            == _CNPJ_BASE_LENGTH
            else (
                6,
                5,
                4,
                3,
                2,
                9,
                8,
                7,
                6,
                5,
                4,
                3,
                2,
            )
        )

        total = sum(
            int(digit) * weight
            for digit, weight in zip(
                digits,
                weights,
                strict=True,
            )
        )

        remainder = (
            total
            % _CHECK_DIGIT_MODULUS
        )

        if (
            remainder
            < _CHECK_DIGIT_ZERO_THRESHOLD
        ):
            return 0

        return (
            _CHECK_DIGIT_MODULUS
            - remainder
        )


@dataclass(frozen=True, slots=True)
class SupplierEmail:
    """Represent a normalized supplier email."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()

        if (
            not normalized
            or normalized.count("@") != 1
        ):
            raise ValueError(
                "O e-mail do fornecedor é inválido."
            )

        local_part, domain = normalized.split(
            "@",
            maxsplit=1,
        )

        if (
            not local_part
            or not domain
            or "." not in domain
            or local_part.startswith(".")
            or local_part.endswith(".")
            or domain.startswith("-")
            or domain.endswith("-")
        ):
            raise ValueError(
                "O e-mail do fornecedor é inválido."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class SupplierPhone:
    """Represent a normalized Brazilian phone."""

    value: str

    def __post_init__(self) -> None:
        normalized = _NON_DIGIT_PATTERN.sub(
            "",
            self.value,
        )

        if (
            len(normalized)
            > _PHONE_MAX_LOCAL_LENGTH
            and normalized.startswith(
                _BRAZIL_COUNTRY_CODE
            )
        ):
            normalized = normalized[2:]

        if len(normalized) not in _PHONE_LENGTHS:
            raise ValueError(
                "O telefone do fornecedor é inválido."
            )

        area_code = normalized[:2]

        if area_code == "00":
            raise ValueError(
                "O telefone do fornecedor é inválido."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class SupplierPostalCode:
    """Represent a normalized Brazilian postal code."""

    value: str

    def __post_init__(self) -> None:
        normalized = _NON_DIGIT_PATTERN.sub(
            "",
            self.value,
        )

        if (
            len(normalized)
            != _POSTAL_CODE_LENGTH
        ):
            raise ValueError(
                "O CEP do fornecedor deve conter "
                "8 dígitos."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class SupplierState:
    """Represent a normalized Brazilian state code."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()

        if (
            len(normalized)
            != _STATE_CODE_LENGTH
            or not normalized.isalpha()
        ):
            raise ValueError(
                "O estado do fornecedor deve possuir "
                "uma UF válida."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )
