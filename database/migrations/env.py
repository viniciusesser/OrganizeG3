"""Alembic environment configured for synchronous SQLAlchemy migrations."""

from __future__ import annotations

from logging.config import fileConfig
from pathlib import Path
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection

PROJECT_ROOT = Path(__file__).resolve().parents[2]
API_SOURCE = PROJECT_ROOT / "apps" / "api" / "src"

if str(API_SOURCE) not in sys.path:
    sys.path.insert(
        0,
        str(API_SOURCE),
    )

from organizeg3_api.config import get_settings  # noqa: E402
from organizeg3_api.infrastructure.database.base import Base  # noqa: E402
from organizeg3_api.infrastructure.persistence.models.customer import (  # noqa: E402,F401
    CustomerModel,
)
from organizeg3_api.infrastructure.persistence.models.tenant import (  # noqa: E402,F401
    TenantModel,
)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def include_object(
    object_: object,
    name: str | None,
    type_: str,
    reflected: bool,
    compare_to: object | None,
) -> bool:
    """Protect legacy tables and columns that are not mapped yet."""

    del compare_to

    if (
        type_ == "table"
        and reflected
        and name not in target_metadata.tables
    ):
        return False

    if type_ == "column" and reflected:
        table = getattr(
            object_,
            "table",
            None,
        )

        table_name = getattr(
            table,
            "name",
            None,
        )

        if table_name in target_metadata.tables:
            mapped_columns = target_metadata.tables[
                table_name
            ].columns

            if name not in mapped_columns:
                return False

    return True


def normalize_database_url(
    database_url: str,
) -> str:
    """Normalize PostgreSQL URLs to the synchronous psycopg driver."""

    normalized = database_url.strip()

    if normalized.startswith("postgres://"):
        return normalized.replace(
            "postgres://",
            "postgresql+psycopg://",
            1,
        )

    if normalized.startswith("postgresql://"):
        return normalized.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

    return normalized


def run_migrations_offline() -> None:
    """Run migrations without creating a database connection."""

    context.configure(
        url=normalize_database_url(
            get_settings().require_database_url()
        ),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
        include_object=include_object,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(
    connection: Connection,
) -> None:
    """Configure and run migrations on an existing connection."""

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations using the configured synchronous engine."""

    configuration = config.get_section(
        config.config_ini_section,
        {},
    )

    configuration["sqlalchemy.url"] = (
        normalize_database_url(
            get_settings().require_database_url()
        )
    )

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()