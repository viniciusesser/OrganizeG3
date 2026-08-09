"""Safe serialization and sensitive-field protection for audit events."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING
import uuid

from pydantic import BaseModel

if TYPE_CHECKING:
    from _typeshed import DataclassInstance


_REDACTION_MARKER = "[REDACTED]"
_PERSONAL_DATA_MARKER = "[REDACTED_PERSONAL_DATA]"

REDACTED_SECRET = _REDACTION_MARKER
REDACTED_PERSONAL_DATA = _PERSONAL_DATA_MARKER


_SECRET_FIELDS = frozenset(
    {
        "access_token",
        "api_key",
        "apikey",
        "authorization",
        "client_secret",
        "credential",
        "credentials",
        "password",
        "password_hash",
        "refresh_token",
        "secret",
        "token",
    }
)


_PERSONAL_DATA_FIELDS = frozenset(
    {
        "cpf",
        "cnpj",
        "document",
        "document_number",
        "email",
        "email_address",
        "phone",
        "phone_number",
        "telephone",
    }
)


def _normalize_field_name(
    value: object,
) -> str:
    """Normalize a mapping key for policy comparison."""

    return str(
        value
    ).strip().lower()


def _is_secret_field(
    field_name: str,
) -> bool:
    """Return whether a field must never expose its value."""

    normalized = _normalize_field_name(
        field_name
    )

    if normalized in _SECRET_FIELDS:
        return True

    return any(
        normalized.endswith(
            f"_{suffix}"
        )
        for suffix in _SECRET_FIELDS
    )


def _is_personal_data_field(
    field_name: str,
) -> bool:
    """Return whether a field contains protected personal data."""

    normalized = _normalize_field_name(
        field_name
    )

    if normalized in _PERSONAL_DATA_FIELDS:
        return True

    return any(
        normalized.endswith(
            f"_{suffix}"
        )
        for suffix in _PERSONAL_DATA_FIELDS
    )


def _serialize_sequence(
    value: Sequence[object],
) -> list[object]:
    """Serialize a sequence to detached JSON-compatible values."""

    return [
        serialize_audit_value(
            item
        )
        for item in value
    ]


def _serialize_mapping(
    value: Mapping[str, object],
) -> dict[str, object]:
    """Serialize and sanitize one string-keyed mapping recursively."""

    result: dict[str, object] = {}

    for key, raw_value in value.items():
        if _is_secret_field(
            key
        ):
            result[key] = REDACTED_SECRET

        elif _is_personal_data_field(
            key
        ):
            result[key] = (
                None
                if raw_value is None
                else REDACTED_PERSONAL_DATA
            )

        else:
            result[key] = serialize_audit_value(
                raw_value
            )

    return result


def _normalize_mapping_keys(
    value: Mapping[object, object],
) -> dict[str, object]:
    """Convert arbitrary mapping keys to strings."""

    return {
        str(key): item
        for key, item in value.items()
    }


def _serialize_datetime(
    value: datetime,
) -> str:
    """Serialize one timezone-aware datetime."""

    if value.tzinfo is None:
        raise ValueError(
            "Datas de auditoria devem possuir timezone."
        )

    return value.isoformat()


def _serialize_pydantic_model(
    value: BaseModel,
) -> dict[str, object]:
    """Serialize one Pydantic model without retaining model objects."""

    raw_data = value.model_dump(
        mode="python"
    )

    normalized: dict[str, object] = {
        str(key): item
        for key, item in raw_data.items()
    }

    return _serialize_mapping(
        normalized
    )


def _serialize_dataclass(
    value: DataclassInstance,
) -> dict[str, object]:
    """Serialize one dataclass instance."""

    raw_data = asdict(
        value
    )

    normalized: dict[str, object] = {
        str(key): item
        for key, item in raw_data.items()
    }

    return _serialize_mapping(
        normalized
    )


def serialize_audit_value(
    value: object,
) -> object:
    """Convert supported application values to JSON-compatible data."""

    result: object

    if value is None:
        result = None

    elif isinstance(
        value,
        Enum,
    ):
        result = serialize_audit_value(
            value.value
        )

    elif isinstance(
        value,
        (
            str,
            int,
            float,
            bool,
        ),
    ):
        result = value

    elif isinstance(
        value,
        uuid.UUID,
    ):
        result = str(
            value
        )

    elif isinstance(
        value,
        datetime,
    ):
        result = _serialize_datetime(
            value
        )

    elif isinstance(
        value,
        date,
    ):
        result = value.isoformat()

    elif isinstance(
        value,
        Decimal,
    ):
        result = str(
            value
        )

    elif isinstance(
        value,
        BaseModel,
    ):
        result = _serialize_pydantic_model(
            value
        )

    elif (
        is_dataclass(
            value
        )
        and not isinstance(
            value,
            type,
        )
    ):
        result = _serialize_dataclass(
            value
        )

    elif isinstance(
        value,
        Mapping,
    ):
        normalized_mapping = _normalize_mapping_keys(
            value
        )

        result = _serialize_mapping(
            normalized_mapping
        )

    elif (
        isinstance(
            value,
            Sequence,
        )
        and not isinstance(
            value,
            (
                str,
                bytes,
                bytearray,
            ),
        )
    ):
        result = _serialize_sequence(
            value
        )

    else:
        raise TypeError(
            "O valor informado não pode ser serializado "
            "com segurança para auditoria."
        )

    return result


def sanitize_audit_mapping(
    value: Mapping[str, object] | BaseModel | None,
) -> dict[str, object] | None:
    """Return a safe detached audit mapping."""

    if value is None:
        return None

    if isinstance(
        value,
        BaseModel,
    ):
        return _serialize_pydantic_model(
            value
        )

    return _serialize_mapping(
        value
    )


__all__ = [
    "REDACTED_PERSONAL_DATA",
    "REDACTED_SECRET",
    "sanitize_audit_mapping",
    "serialize_audit_value",
]
