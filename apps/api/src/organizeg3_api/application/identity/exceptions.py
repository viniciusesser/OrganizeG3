"""Controlled authentication and authorization exceptions."""

from __future__ import annotations

from organizeg3_api.core.exceptions import (
    AuthenticationError,
    ConfigurationError,
    OrganizeG3Error,
    PermissionDeniedError,
)


class InvalidAccessTokenError(AuthenticationError):
    """Raised when an access token cannot be trusted."""

    error_code = "authentication.invalid_token"

    def __init__(self) -> None:
        super().__init__(
            "O token de acesso está ausente, inválido ou expirado."
        )


class AuthenticationProviderUnavailableError(
    OrganizeG3Error
):
    """Raised when the external identity provider is unavailable."""

    error_code = "authentication.provider_unavailable"
    status_code = 503

    def __init__(self) -> None:
        super().__init__(
            "O provedor de autenticação está temporariamente indisponível."
        )


class SupabaseAuthenticationConfigurationError(
    ConfigurationError
):
    """Raised when Supabase authentication is not configured."""

    error_code = "authentication.configuration_error"

    def __init__(self) -> None:
        super().__init__(
            "A autenticação do Supabase não está configurada corretamente."
        )


class TenantMembershipUnavailableError(
    PermissionDeniedError
):
    """Raised when the user has no active tenant membership."""

    error_code = "authorization.tenant_membership_unavailable"

    def __init__(self) -> None:
        super().__init__(
            "O usuário não possui acesso ativo a esta empresa."
        )


class PermissionRequiredError(
    PermissionDeniedError
):
    """Raised when one granular permission is missing."""

    error_code = "authorization.permission_required"

    def __init__(
        self,
        permission_code: str,
    ) -> None:
        super().__init__(
            "O usuário não possui permissão para executar esta operação.",
            details={
                "permission": permission_code,
            },
        )
