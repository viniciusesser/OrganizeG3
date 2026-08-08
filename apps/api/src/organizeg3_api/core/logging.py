"""Structured logging configuration for the OrganizeG3 Platform API."""

from __future__ import annotations

from contextvars import ContextVar
import logging
import sys
from typing import Any, cast

import structlog

from organizeg3_api.config import Settings

correlation_id_context: ContextVar[str | None] = ContextVar(
    "correlation_id",
    default=None,
)

tenant_id_context: ContextVar[str | None] = ContextVar(
    "tenant_id",
    default=None,
)

branch_id_context: ContextVar[str | None] = ContextVar(
    "branch_id",
    default=None,
)

user_id_context: ContextVar[str | None] = ContextVar(
    "user_id",
    default=None,
)

device_id_context: ContextVar[str | None] = ContextVar(
    "device_id",
    default=None,
)


def add_request_context(
    logger: Any,  # noqa: ANN401
    method_name: str,
    event_dict: dict[str, Any],
) -> dict[str, Any]:
    """Add contextual request identifiers to every structured log."""

    del logger, method_name

    correlation_id = correlation_id_context.get()
    tenant_id = tenant_id_context.get()
    branch_id = branch_id_context.get()
    user_id = user_id_context.get()
    device_id = device_id_context.get()

    if correlation_id is not None:
        event_dict["correlation_id"] = correlation_id

    if tenant_id is not None:
        event_dict["tenant_id"] = tenant_id

    if branch_id is not None:
        event_dict["branch_id"] = branch_id

    if user_id is not None:
        event_dict["user_id"] = user_id

    if device_id is not None:
        event_dict["device_id"] = device_id

    return event_dict


def configure_logging(settings: Settings) -> None:
    """Configure standard logging and structlog for the API."""

    log_level = getattr(
        logging,
        settings.log_level.value,
        logging.INFO,
    )

    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        add_request_context,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(
            fmt="iso",
            utc=True,
        ),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.log_include_source:
        shared_processors.append(
            structlog.processors.CallsiteParameterAdder(
                parameters={
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                },
            )
        )

    renderer: Any

    if settings.log_json:
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(
            colors=sys.stderr.isatty(),
        )

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)

    for logger_name in (
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "fastapi",
        "sqlalchemy.engine",
    ):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.propagate = True

    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.database_echo else logging.WARNING
    )


def get_logger(
    name: str | None = None,
) -> structlog.stdlib.BoundLogger:
    """Return a structured logger."""

    return cast(
        structlog.stdlib.BoundLogger,
        structlog.get_logger(name),
    )


def set_request_context(
    *,
    correlation_id: str | None = None,
    tenant_id: str | None = None,
    branch_id: str | None = None,
    user_id: str | None = None,
    device_id: str | None = None,
) -> None:
    """Set contextual identifiers for the current request."""

    if correlation_id is not None:
        correlation_id_context.set(
            correlation_id
        )

    if tenant_id is not None:
        tenant_id_context.set(
            tenant_id
        )

    if branch_id is not None:
        branch_id_context.set(
            branch_id
        )

    if user_id is not None:
        user_id_context.set(
            user_id
        )

    if device_id is not None:
        device_id_context.set(
            device_id
        )


def clear_request_context() -> None:
    """Clear request-scoped logging context."""

    correlation_id_context.set(None)
    tenant_id_context.set(None)
    branch_id_context.set(None)
    user_id_context.set(None)
    device_id_context.set(None)

    structlog.contextvars.clear_contextvars()
