"""Value objects for customer identity and contact data."""

from __future__ import annotations

import re
from typing import Final

_NON_DIGITS: Final = re.compile(r"\D+")
_DOMAIN_LABEL: Final = re.compile(
    r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$"
)

_CPF_LENGTH: Final = 11
_CNPJ_LENGTH: Final = 14

_LANDLINE_LENGTH: Final = 10
_MOBILE_LENGTH: Final = 11
_VALID_LANDLINE_PREFIXES: Final = "2345"

_MAX_EMAIL_LENGTH: Final = 255
_MAX_LOCAL_PART_LENGTH: Final = 64
_MIN_DOMAIN_LABEL_COUNT: Final = 2

_BRAZIL_COUNTRY_CODE: Final = "55"
_CHECK_DIGIT_REMAINDER_LIMIT: Final = 2
_CHECK_DIGIT_MODULUS: Final = 11


class DocumentNumber(str):
    """Validated and normalized Brazilian CPF or CNPJ."""

    def __new__(
        cls,
        value: str,
    ) -> DocumentNumber:
        if not isinstance(value, str):
            raise TypeError(
                "CPF/CNPJ deve ser informado como texto."
            )

        digits = _NON_DIGITS.sub("", value)

        if len(digits) == _CPF_LENGTH:
            if not cls._is_valid_cpf(digits):
                raise ValueError("CPF inválido.")

        elif len(digits) == _CNPJ_LENGTH:
            if not cls._is_valid_cnpj(digits):
                raise ValueError("CNPJ inválido.")

        else:
            raise ValueError(
                "CPF/CNPJ deve possuir 11 ou 14 dígitos."
            )

        return str.__new__(
            cls,
            digits,
        )

    @property
    def is_cpf(self) -> bool:
        """Return whether this document is a CPF."""

        return len(self) == _CPF_LENGTH

    @property
    def is_cnpj(self) -> bool:
        """Return whether this document is a CNPJ."""

        return len(self) == _CNPJ_LENGTH

    @staticmethod
    def _calculate_check_digit(
        digits: str,
        weights: tuple[int, ...] | range,
    ) -> int:
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
            < _CHECK_DIGIT_REMAINDER_LIMIT
        ):
            return 0

        return (
            _CHECK_DIGIT_MODULUS
            - remainder
        )

    @classmethod
    def _is_valid_cpf(
        cls,
        digits: str,
    ) -> bool:
        if digits == digits[0] * len(digits):
            return False

        first_digit = (
            cls._calculate_check_digit(
                digits[:9],
                range(10, 1, -1),
            )
        )

        if first_digit != int(digits[9]):
            return False

        second_digit = (
            cls._calculate_check_digit(
                digits[:10],
                range(11, 1, -1),
            )
        )

        return (
            second_digit
            == int(digits[10])
        )

    @classmethod
    def _is_valid_cnpj(
        cls,
        digits: str,
    ) -> bool:
        if digits == digits[0] * len(digits):
            return False

        first_weights = (
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

        first_digit = (
            cls._calculate_check_digit(
                digits[:12],
                first_weights,
            )
        )

        if first_digit != int(digits[12]):
            return False

        second_weights = (
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

        second_digit = (
            cls._calculate_check_digit(
                digits[:13],
                second_weights,
            )
        )

        return (
            second_digit
            == int(digits[13])
        )


class EmailAddress(str):
    """Normalized email address with conservative syntax validation."""

    def __new__(
        cls,
        value: str,
    ) -> EmailAddress:
        if not isinstance(value, str):
            raise TypeError(
                "E-mail deve ser informado como texto."
            )

        normalized = value.strip().lower()

        if (
            len(normalized)
            > _MAX_EMAIL_LENGTH
            or normalized.count("@") != 1
        ):
            raise ValueError(
                "E-mail inválido."
            )

        local_part, domain = (
            normalized.rsplit(
                "@",
                1,
            )
        )

        if (
            not local_part
            or len(local_part)
            > _MAX_LOCAL_PART_LENGTH
        ):
            raise ValueError(
                "E-mail inválido."
            )

        if (
            local_part.startswith(".")
            or local_part.endswith(".")
            or ".." in local_part
        ):
            raise ValueError(
                "E-mail inválido."
            )

        if any(
            character.isspace()
            for character in local_part
        ):
            raise ValueError(
                "E-mail inválido."
            )

        labels = domain.split(".")

        if (
            len(labels)
            < _MIN_DOMAIN_LABEL_COUNT
            or any(
                not _DOMAIN_LABEL.fullmatch(
                    label
                )
                for label in labels
            )
        ):
            raise ValueError(
                "E-mail inválido."
            )

        return str.__new__(
            cls,
            normalized,
        )


class PhoneNumber(str):
    """Normalized Brazilian landline or mobile phone number."""

    def __new__(
        cls,
        value: str,
    ) -> PhoneNumber:
        if not isinstance(value, str):
            raise TypeError(
                "Telefone deve ser informado como texto."
            )

        digits = _NON_DIGITS.sub(
            "",
            value,
        )

        if (
            len(digits)
            in {
                _LANDLINE_LENGTH + 2,
                _MOBILE_LENGTH + 2,
            }
            and digits.startswith(
                _BRAZIL_COUNTRY_CODE
            )
        ):
            digits = digits[
                len(_BRAZIL_COUNTRY_CODE) :
            ]

        if len(digits) not in {
            _LANDLINE_LENGTH,
            _MOBILE_LENGTH,
        }:
            raise ValueError(
                "Telefone deve possuir DDD e 10 ou 11 dígitos."
            )

        if (
            digits[0] == "0"
            or digits[1] == "0"
        ):
            raise ValueError(
                "DDD do telefone é inválido."
            )

        if (
            len(digits) == _MOBILE_LENGTH
            and digits[2] != "9"
        ):
            raise ValueError(
                "Celular deve iniciar com 9 após o DDD."
            )

        if (
            len(digits) == _LANDLINE_LENGTH
            and digits[2]
            not in _VALID_LANDLINE_PREFIXES
        ):
            raise ValueError(
                "Telefone fixo possui prefixo inválido."
            )

        return str.__new__(
            cls,
            digits,
        )


def optional_document(
    value: str | DocumentNumber | None,
) -> DocumentNumber | None:
    """Build an optional document value object."""

    if (
        value is None
        or not str(value).strip()
    ):
        return None

    if isinstance(
        value,
        DocumentNumber,
    ):
        return value

    return DocumentNumber(value)


def optional_email(
    value: str | EmailAddress | None,
) -> EmailAddress | None:
    """Build an optional email value object."""

    if (
        value is None
        or not str(value).strip()
    ):
        return None

    if isinstance(
        value,
        EmailAddress,
    ):
        return value

    return EmailAddress(value)


def optional_phone(
    value: str | PhoneNumber | None,
) -> PhoneNumber | None:
    """Build an optional phone value object."""

    if (
        value is None
        or not str(value).strip()
    ):
        return None

    if isinstance(
        value,
        PhoneNumber,
    ):
        return value

    return PhoneNumber(value)
