"""Authenticated identity and request context definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
import uuid


@dataclass(frozen=True, slots=True)
class VerifiedToken:
    """Represent identity claims from a verified access token."""

    auth_user_id: uuid.UUID
    role: str
    email: str | None = None
    session_id: uuid.UUID | None = None


@dataclass(frozen=True, slots=True)
class AuthenticatedContext:
    """Represent the authenticated OrganizeG3 request context."""

    tenant_id: uuid.UUID
    user_id: uuid.UUID
    membership_id: uuid.UUID
    auth_user_id: uuid.UUID
    email: str
    display_name: str
    permission_codes: frozenset[str]

    def has_permission(
        self,
        permission_code: str,
    ) -> bool:
        """Return whether the context contains one permission."""

        return permission_code in self.permission_codes


class TokenVerifier(Protocol):
    """Verify an external access token."""

    def verify(
        self,
        access_token: str,
    ) -> VerifiedToken:
        """Verify the token and return trusted claims."""
