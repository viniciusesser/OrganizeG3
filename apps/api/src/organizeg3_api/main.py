"""Application entry point for the OrganizeG3 Platform API."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from organizeg3_api.config import (
    Environment,
    Settings,
    get_settings,
)
from organizeg3_api.core.logging import (
    configure_logging,
    get_logger,
)
from organizeg3_api.infrastructure.database.session import (
    dispose_database_manager,
    get_database_manager,
)
from organizeg3_api.infrastructure.http.api.v1 import (
    router as api_v1_router,
)
from organizeg3_api.infrastructure.persistence.authorization import (
    sync_permission_catalog,
)
from organizeg3_api.middleware.correlation_id import (
    CorrelationIdMiddleware,
)
from organizeg3_api.middleware.error_handler import (
    register_exception_handlers,
)


def _should_sync_permission_catalog(
    settings: Settings,
) -> bool:
    """Return whether persistent startup bootstrap should run."""

    return (
        settings.app_environment
        is not Environment.TEST
        and settings.database_url is not None
    )


def _synchronize_startup_data(
    settings: Settings,
) -> None:
    """Synchronize canonical persistent data required by the API."""

    logger = get_logger(__name__)

    if not _should_sync_permission_catalog(
        settings
    ):
        reason = (
            "test_environment"
            if settings.app_environment
            is Environment.TEST
            else "database_not_configured"
        )

        logger.info(
            "permission_catalog_sync_skipped",
            reason=reason,
        )
        return

    database_manager = get_database_manager(
        settings
    )

    with database_manager.session() as session:
        sync_result = sync_permission_catalog(
            session
        )

    logger.info(
        "permission_catalog_synchronized",
        created=sync_result.created,
        updated=sync_result.updated,
        reactivated=sync_result.reactivated,
        unchanged=sync_result.unchanged,
        total=sync_result.total,
    )


@asynccontextmanager
async def lifespan(
    application: FastAPI,
) -> AsyncIterator[None]:
    """Manage API startup and shutdown lifecycle."""

    settings: Settings = application.state.settings
    logger = get_logger(__name__)

    logger.info(
        "application_started",
        application=settings.app_name,
        version=settings.app_version,
        environment=settings.app_environment.value,
    )

    try:
        _synchronize_startup_data(
            settings
        )

        yield
    finally:
        dispose_database_manager()

        logger.info(
            "application_stopped",
            application=settings.app_name,
        )


def create_application(
    settings: Settings | None = None,
) -> FastAPI:
    """Create and configure the FastAPI application."""

    effective_settings = (
        settings
        or get_settings()
    )

    configure_logging(
        effective_settings
    )

    application = FastAPI(
        title=effective_settings.app_name,
        description=(
            "API oficial da plataforma OrganizeG3."
        ),
        version=effective_settings.app_version,
        debug=effective_settings.app_debug,
        docs_url=(
            effective_settings.effective_docs_url
        ),
        redoc_url=(
            effective_settings.effective_redoc_url
        ),
        lifespan=lifespan,
    )

    application.state.settings = (
        effective_settings
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=(
            effective_settings.cors_allowed_origins
        ),
        allow_credentials=(
            effective_settings.cors_allow_credentials
        ),
        allow_methods=(
            effective_settings.cors_allowed_methods
        ),
        allow_headers=(
            effective_settings.cors_allowed_headers
        ),
    )

    application.add_middleware(
        CorrelationIdMiddleware
    )

    register_exception_handlers(
        application
    )

    application.include_router(
        api_v1_router,
        prefix=effective_settings.api_prefix,
    )

    @application.get(
        "/health",
        tags=["System"],
        summary="Verificar a saúde da API",
    )
    def health_check() -> dict[str, str]:
        """Return the current API health status."""

        return {
            "status": "healthy",
            "service": "organizeg3-api",
            "version": effective_settings.app_version,
            "environment": (
                effective_settings
                .app_environment
                .value
            ),
        }

    return application


app = create_application()
