"""Value objects for company identity and contact data."""

from __future__ import annotations

from dataclasses import dataclass
import re

_NON_DIGIT_PATTERN = re.compile(r"\D+")

_VALID_DOCUMENT_LENGTHS = {
    11,
    14,
}

_VALID_PHONE_LENGTHS = {
    10,
    11,
}

_POSTAL_CODE_LENGTH = 8


def normalize_optional_text(
    value: str | None,
) -> str | None:
    """Normalize optional textual input."""

    if value is None:
        return None

    normalized = value.strip()

    if not normalized:
        return None

    return normalized


@dataclass(frozen=True, slots=True)
class CompanyDocument:
    """Represent a normalized Brazilian company document."""

    value: str

    def __post_init__(self) -> None:
        normalized = _NON_DIGIT_PATTERN.sub(
            "",
            self.value,
        )

        if len(normalized) not in _VALID_DOCUMENT_LENGTHS:
            raise ValueError(
                "O documento da empresa deve conter CPF ou CNPJ válido."
            )

        if len(set(normalized)) == 1:
            raise ValueError(
                "O documento da empresa não pode conter dígitos repetidos."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class CompanyEmail:
    """Represent a normalized company e-mail address."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()

        if (
            not normalized
            or normalized.count("@") != 1
        ):
            raise ValueError(
                "O e-mail da empresa é inválido."
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
                "O e-mail da empresa é inválido."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class CompanyPhone:
    """Represent a normalized Brazilian company phone."""

    value: str

    def __post_init__(self) -> None:
        normalized = _NON_DIGIT_PATTERN.sub(
            "",
            self.value,
        )

        if normalized.startswith("55"):
            normalized = normalized[2:]

        if len(normalized) not in _VALID_PHONE_LENGTHS:
            raise ValueError(
                "O telefone da empresa é inválido."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class PostalCode:
    """Represent a normalized Brazilian postal code."""

    value: str

    def __post_init__(self) -> None:
        normalized = _NON_DIGIT_PATTERN.sub(
            "",
            self.value,
        )

        if len(normalized) != _POSTAL_CODE_LENGTH:
            raise ValueError(
                "O CEP da empresa deve conter 8 dígitos."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )
