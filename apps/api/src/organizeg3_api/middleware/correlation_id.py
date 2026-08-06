"""Correlation ID middleware for request traceability."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

from organizeg3_api.core.logging import (
    clear_request_context,
    set_request_context,
)

CORRELATION_ID_HEADER = "X-Correlation-ID"
DEVICE_ID_HEADER = "X-Device-ID"


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Assign and propagate a correlation ID for every HTTP request."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        correlation_id = self._resolve_correlation_id(request)
        device_id = request.headers.get(DEVICE_ID_HEADER)

        structlog.contextvars.clear_contextvars()

        structlog.contextvars.bind_contextvars(
            correlation_id=correlation_id,
            device_id=device_id,
        )

        set_request_context(
            correlation_id=correlation_id,
            device_id=device_id,
        )

        request.state.correlation_id = correlation_id
        request.state.device_id = device_id

        try:
            response = await call_next(request)
            response.headers[CORRELATION_ID_HEADER] = correlation_id

            return response
        finally:
            clear_request_context()

    @staticmethod
    def _resolve_correlation_id(request: Request) -> str:
        """Return a validated incoming ID or generate a new UUID."""

        incoming_value = request.headers.get(CORRELATION_ID_HEADER)

        if incoming_value:
            normalized_value = incoming_value.strip()

            if normalized_value and len(normalized_value) <= 128:  # noqa: PLR2004
                return normalized_value

        return str(uuid.uuid4())
