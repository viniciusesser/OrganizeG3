"""Controlled application errors for branch context."""

from __future__ import annotations

from organizeg3_api.core.exceptions import (
    PermissionDeniedError,
    ValidationError,
)


class InvalidBranchIdentifierError(ValidationError):
    """Raised when a branch identifier is structurally invalid."""

    error_code = "branch.invalid_identifier"


class BranchUnavailableError(PermissionDeniedError):
    """Raised when a branch cannot be used in the current tenant."""

    error_code = "authorization.branch_unavailable"


class BranchRequiredError(ValidationError):
    """Raised when an operation requires an explicit branch."""

    error_code = "branch.required"
