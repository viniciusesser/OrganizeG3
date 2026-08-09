"""Canonical business audit actions."""

from __future__ import annotations

from enum import StrEnum


class AuditAction(StrEnum):
    """Stable actions recorded in the business audit trail."""

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DEACTIVATE = "DEACTIVATE"
    REACTIVATE = "REACTIVATE"
    ARCHIVE = "ARCHIVE"
    STATUS_CHANGE = "STATUS_CHANGE"


__all__ = [
    "AuditAction",
]
