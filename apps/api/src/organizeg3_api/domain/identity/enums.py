"""Identity and authorization enumerations."""

from __future__ import annotations

from enum import StrEnum


class MembershipStatus(StrEnum):
    """Represent the lifecycle of a tenant membership."""

    INVITED = "INVITED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"


class PermissionEffect(StrEnum):
    """Represent an explicit permission override."""

    ALLOW = "ALLOW"
    DENY = "DENY"
