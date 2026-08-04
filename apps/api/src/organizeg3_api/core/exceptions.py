"""Application exceptions exposed through the Platform API."""

from __future__ import annotations

from typing import Any


class OrganizeG3Error(Exception):
    """Base exception for controlled OrganizeG3 errors."""

    error_code = "organizeg3.error"
    status_code = 500

    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)

        self.message = message
        self.details = details or {}


class ValidationError(OrganizeG3Error):
    """Raised when submitted data violates an application rule."""

    error_code = "validation.error"
    status_code = 422


class NotFoundError(OrganizeG3Error):
    """Raised when an authorized resource cannot be found."""

    error_code = "resource.not_found"
    status_code = 404


class ConflictError(OrganizeG3Error):
    """Raised when an operation conflicts with current state."""

    error_code = "resource.conflict"
    status_code = 409


class PermissionDeniedError(OrganizeG3Error):
    """Raised when the authenticated actor lacks permission."""

    error_code = "authorization.permission_denied"
    status_code = 403


class AuthenticationError(OrganizeG3Error):
    """Raised when authentication is missing or invalid."""

    error_code = "authentication.invalid"
    status_code = 401


class InvalidTransitionError(ConflictError):
    """Raised when a workflow transition is not allowed."""

    error_code = "workflow.invalid_transition"


class ConcurrencyError(ConflictError):
    """Raised when optimistic concurrency validation fails."""

    error_code = "concurrency.conflict"


class IdempotencyConflictError(ConflictError):
    """Raised when an idempotency key is reused incompatibly."""

    error_code = "idempotency.conflict"


class ConfigurationError(OrganizeG3Error):
    """Raised when the application configuration is invalid."""

    error_code = "configuration.error"
    status_code = 500
