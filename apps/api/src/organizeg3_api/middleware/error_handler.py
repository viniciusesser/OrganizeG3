"""Global exception handlers for the OrganizeG3 API."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import (
    RequestValidationError,
)
from fastapi.responses import JSONResponse
from starlette.exceptions import (
    HTTPException as StarletteHTTPException,
)

from organizeg3_api.core.exceptions import (
    OrganizeG3Error,
)
from organizeg3_api.core.logging import (
    get_logger,
)

logger = get_logger(__name__)


def get_correlation_id(
    request: Request,
) -> str | None:
    """Return the current correlation identifier."""

    return getattr(
        request.state,
        "correlation_id",
        None,
    )


def build_error_response(
    *,
    request: Request,
    status_code: int,
    error_code: str,
    message: str,
    details: Any = None,  # noqa: ANN401
) -> JSONResponse:
    """Build the standard API error response."""

    correlation_id = get_correlation_id(
        request
    )

    content: dict[str, Any] = {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
            "details": details,
        },
        "meta": {
            "correlation_id": correlation_id,
        },
    }

    return JSONResponse(
        status_code=status_code,
        content=content,
    )


def sanitize_validation_errors(
    errors: Sequence[
        dict[str, Any]
    ],
) -> list[dict[str, Any]]:
    """Convert validation contexts into JSON-safe values."""

    sanitized: list[
        dict[str, Any]
    ] = []

    for error in errors:
        item = dict(error)
        context = item.get("ctx")

        if isinstance(context, dict):
            item["ctx"] = {
                key: (
                    str(value)
                    if isinstance(
                        value,
                        BaseException,
                    )
                    else value
                )
                for key, value
                in context.items()
            }

        sanitized.append(item)

    return sanitized


def register_exception_handlers(
    application: FastAPI,
) -> None:
    """Register global exception handlers."""

    @application.exception_handler(
        OrganizeG3Error
    )
    async def handle_organizeg3_error(
        request: Request,
        exception: OrganizeG3Error,
    ) -> JSONResponse:
        logger.warning(
            "controlled_application_error",
            error_code=exception.error_code,
            error_message=exception.message,
            path=request.url.path,
            method=request.method,
        )

        return build_error_response(
            request=request,
            status_code=exception.status_code,
            error_code=exception.error_code,
            message=exception.message,
            details=(
                exception.details
                or None
            ),
        )

    @application.exception_handler(
        RequestValidationError
    )
    async def handle_request_validation_error(
        request: Request,
        exception: RequestValidationError,
    ) -> JSONResponse:
        validation_errors = (
            sanitize_validation_errors(
                exception.errors()
            )
        )

        logger.warning(
            "request_validation_failed",
            path=request.url.path,
            method=request.method,
            validation_errors=(
                validation_errors
            ),
        )

        return build_error_response(
            request=request,
            status_code=422,
            error_code=(
                "request.validation_error"
            ),
            message=(
                "Os dados enviados são inválidos."
            ),
            details=validation_errors,
        )

    @application.exception_handler(
        StarletteHTTPException
    )
    async def handle_http_exception(
        request: Request,
        exception: StarletteHTTPException,
    ) -> JSONResponse:
        message = (
            exception.detail
            if isinstance(
                exception.detail,
                str,
            )
            else (
                "A requisição não pôde ser processada."
            )
        )

        return build_error_response(
            request=request,
            status_code=exception.status_code,
            error_code=(
                f"http.{exception.status_code}"
            ),
            message=message,
        )

    @application.exception_handler(
        Exception
    )
    async def handle_unexpected_exception(
        request: Request,
        exception: Exception,
    ) -> JSONResponse:
        logger.error(
            "unexpected_application_error",
            path=request.url.path,
            method=request.method,
            exception_type=(
                type(exception).__name__
            ),
            exc_info=exception,
        )

        return build_error_response(
            request=request,
            status_code=500,
            error_code=(
                "internal_server_error"
            ),
            message=(
                "Ocorreu um erro interno inesperado."
            ),
        )
