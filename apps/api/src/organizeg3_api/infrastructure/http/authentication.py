"""FastAPI dependencies for authenticated request contexts."""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, cast
import uuid

from fastapi import Depends, Request, Security
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from organizeg3_api.application.identity.exceptions import (
    InvalidAccessTokenError,
    PermissionRequiredError,
    SupabaseAuthenticationConfigurationError,
)
from organizeg3_api.application.identity.resolve_authenticated_context import (
    ResolveAuthenticatedContext,
)
from organizeg3_api.config import Settings
from organizeg3_api.core.logging import (
    set_request_context,
)
from organizeg3_api.domain.identity.authentication import (
    AuthenticatedContext,
    TokenVerifier,
    VerifiedToken,
)
from organizeg3_api.infrastructure.auth.supabase_jwt import (
    build_supabase_jwt_verifier,
)
from organizeg3_api.infrastructure.http.dependencies import (
    get_db_session,
    get_tenant_id,
)
from organizeg3_api.infrastructure.persistence.repositories.identity_repository import (
    SqlAlchemyIdentityRepository,
)

_bearer_scheme = HTTPBearer(
    auto_error=False,
)


def get_token_verifier(
    request: Request,
) -> TokenVerifier:
    """Return one cached Supabase verifier per application."""

    cached_verifier = getattr(
        request.app.state,
        "supabase_token_verifier",
        None,
    )

    if cached_verifier is not None:
        return cast(
            TokenVerifier,
            cached_verifier,
        )

    settings = cast(
        Settings,
        request.app.state.settings,
    )

    supabase_url = settings.supabase_url

    if supabase_url is None:
        raise (
            SupabaseAuthenticationConfigurationError
        )

    verifier = build_supabase_jwt_verifier(
        str(supabase_url)
    )

    request.app.state.supabase_token_verifier = (
        verifier
    )

    return verifier


def get_verified_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Security(_bearer_scheme),
    ],
    verifier: Annotated[
        TokenVerifier,
        Depends(get_token_verifier),
    ],
) -> VerifiedToken:
    """Verify the request Bearer token."""

    if (
        credentials is None
        or credentials.scheme.lower()
        != "bearer"
        or not credentials.credentials.strip()
    ):
        raise InvalidAccessTokenError

    return verifier.verify(
        credentials.credentials
    )


def get_identity_repository(
    session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> SqlAlchemyIdentityRepository:
    """Build the identity repository for the request."""

    return SqlAlchemyIdentityRepository(
        session
    )


def get_authenticated_context(
    tenant_id: Annotated[
        object,
        Depends(get_tenant_id),
    ],
    token: Annotated[
        VerifiedToken,
        Depends(get_verified_token),
    ],
    repository: Annotated[
        SqlAlchemyIdentityRepository,
        Depends(get_identity_repository),
    ],
) -> AuthenticatedContext:
    """Resolve verified identity and active tenant access."""

    if not isinstance(
        tenant_id,
        uuid.UUID,
    ):
        raise TypeError(
            "O contexto de tenant deve ser um UUID."
        )

    resolver = ResolveAuthenticatedContext(
        repository
    )

    context = resolver.execute(
        token=token,
        tenant_id=tenant_id,
    )

    set_request_context(
        user_id=str(
            context.user_id
        )
    )

    return context


def require_permission(
    permission_code: str,
) -> Callable[..., AuthenticatedContext]:
    """Create a dependency that requires one permission."""

    def permission_dependency(
        context: Annotated[
            AuthenticatedContext,
            Depends(
                get_authenticated_context
            ),
        ],
    ) -> AuthenticatedContext:
        if not context.has_permission(
            permission_code
        ):
            raise PermissionRequiredError(
                permission_code
            )

        return context

    return permission_dependency
