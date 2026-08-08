"""Value objects for branch identity and contact data."""

from __future__ import annotations

from dataclasses import dataclass
import re

_NON_DIGIT_PATTERN = re.compile(r"\D+")

_BRANCH_DOCUMENT_LENGTH = 14
_VALID_PHONE_LENGTHS = {
    10,
    11,
}
_POSTAL_CODE_LENGTH = 8
_STATE_CODE_LENGTH = 2


def normalize_optional_text(
    value: str | None,
) -> str | None:
    """Normalize optional branch text."""

    if value is None:
        return None

    normalized = value.strip()

    if not normalized:
        return None

    return normalized


@dataclass(frozen=True, slots=True)
class BranchCode:
    """Represent a normalized branch code."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()

        if not normalized:
            raise ValueError(
                "O código da filial é obrigatório."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class BranchDocument:
    """Represent a normalized Brazilian branch CNPJ."""

    value: str

    def __post_init__(self) -> None:
        normalized = _NON_DIGIT_PATTERN.sub(
            "",
            self.value,
        )

        if (
            len(normalized)
            != _BRANCH_DOCUMENT_LENGTH
        ):
            raise ValueError(
                "O documento da filial deve conter "
                "14 dígitos de CNPJ."
            )

        if len(set(normalized)) == 1:
            raise ValueError(
                "O documento da filial não pode "
                "conter dígitos repetidos."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class BranchEmail:
    """Represent a normalized branch e-mail."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()

        if (
            not normalized
            or normalized.count("@") != 1
        ):
            raise ValueError(
                "O e-mail da filial é inválido."
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
                "O e-mail da filial é inválido."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class BranchPhone:
    """Represent a normalized Brazilian branch phone."""

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
                "O telefone da filial é inválido."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class BranchPostalCode:
    """Represent a normalized Brazilian postal code."""

    value: str

    def __post_init__(self) -> None:
        normalized = _NON_DIGIT_PATTERN.sub(
            "",
            self.value,
        )

        if len(normalized) != _POSTAL_CODE_LENGTH:
            raise ValueError(
                "O CEP da filial deve conter 8 dígitos."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True)
class BranchState:
    """Represent a normalized Brazilian state code."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()

        if len(normalized) != _STATE_CODE_LENGTH:
            raise ValueError(
                "O estado da filial deve utilizar a sigla UF."
            )

        if not normalized.isalpha():
            raise ValueError(
                "O estado da filial deve utilizar a sigla UF."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )
