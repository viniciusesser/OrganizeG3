"""Asynchronous SQLAlchemy engine and session management.

The database engine is created lazily. Importing this module never opens a
database connection.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from organizeg3_api.config import Settings, get_settings
from organizeg3_api.core.logging import get_logger

if TYPE_CHECKING:
    from sqlalchemy.engine import URL


logger = get_logger(__name__)


class DatabaseNotConfiguredError(RuntimeError):
    """Raised when a database operation is requested without configuration."""


class DatabaseManager:
    """Own the asynchronous SQLAlchemy engine and session factory.

    One manager should exist per API process. The engine and session factory are
    initialized lazily and disposed during application shutdown.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None

    @property
    def is_configured(self) -> bool:
        """Return whether a database URL is available."""

        return self._settings.database_url is not None

    @property
    def is_initialized(self) -> bool:
        """Return whether the SQLAlchemy engine has already been created."""

        return self._engine is not None

    @property
    def engine(self) -> AsyncEngine:
        """Return the initialized engine."""

        self._ensure_initialized()

        if self._engine is None:
            raise DatabaseNotConfiguredError("O engine do banco de dados não foi inicializado.")

        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Return the initialized asynchronous session factory."""

        self._ensure_initialized()

        if self._session_factory is None:
            raise DatabaseNotConfiguredError("A fábrica de sessões do banco não foi inicializada.")

        return self._session_factory

    def initialize(self) -> None:
        """Create the engine and session factory when necessary."""

        if self.is_initialized:
            return

        database_url = self._get_database_url()

        self._engine = create_async_engine(
            database_url,
            echo=self._settings.database_echo,
            pool_pre_ping=True,
            pool_size=self._settings.database_pool_size,
            max_overflow=self._settings.database_max_overflow,
            pool_timeout=self._settings.database_pool_timeout_seconds,
            pool_recycle=self._settings.database_pool_recycle_seconds,
        )

        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

        logger.info(
            "database_engine_initialized",
            pool_size=self._settings.database_pool_size,
            max_overflow=self._settings.database_max_overflow,
        )

    async def dispose(self) -> None:
        """Dispose the engine and release pooled connections."""

        if self._engine is None:
            return

        await self._engine.dispose()

        self._engine = None
        self._session_factory = None

        logger.info("database_engine_disposed")

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Provide a transactional asynchronous database session."""

        factory = self.session_factory

        async with factory() as database_session:
            try:
                yield database_session
                await database_session.commit()
            except Exception:
                await database_session.rollback()

                logger.exception("database_transaction_rolled_back")

                raise
            finally:
                await database_session.close()

    async def health_check(self) -> bool:
        """Check whether the database accepts a simple query."""

        if not self.is_configured:
            return False

        try:
            async with self.engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
        except Exception:
            logger.exception("database_health_check_failed")
            return False
        else:
            return True

    def _ensure_initialized(self) -> None:
        """Initialize the engine if it has not been created yet."""

        if not self.is_initialized:
            self.initialize()

    def _get_database_url(self) -> str | URL:
        """Return a SQLAlchemy-compatible asynchronous database URL."""

        try:
            database_url = self._settings.require_database_url()
        except RuntimeError as exception:
            raise DatabaseNotConfiguredError(str(exception)) from exception

        return self._normalize_database_url(database_url)

    @staticmethod
    def _normalize_database_url(database_url: str) -> str:
        """Normalize common PostgreSQL URLs for SQLAlchemy async usage."""

        normalized_url = database_url.strip()

        if normalized_url.startswith("postgres://"):
            return normalized_url.replace(
                "postgres://",
                "postgresql+psycopg://",
                1,
            )

        if normalized_url.startswith("postgresql://"):
            return normalized_url.replace(
                "postgresql://",
                "postgresql+psycopg://",
                1,
            )

        return normalized_url


class DatabaseManagerRegistry:
    """Store the process-level database manager without module globals."""

    def __init__(self) -> None:
        self._manager: DatabaseManager | None = None

    def get(
        self,
        settings: Settings | None = None,
    ) -> DatabaseManager:
        """Return the current manager, creating it when necessary."""

        if self._manager is None:
            self._manager = DatabaseManager(settings or get_settings())

        return self._manager

    async def dispose(self) -> None:
        """Dispose and remove the current manager."""

        if self._manager is None:
            return

        await self._manager.dispose()
        self._manager = None


_database_registry = DatabaseManagerRegistry()


def get_database_manager(
    settings: Settings | None = None,
) -> DatabaseManager:
    """Return the process-level database manager."""

    return _database_registry.get(settings)


async def get_database_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency that provides one transactional session."""

    manager = get_database_manager()

    async with manager.session() as database_session:
        yield database_session


async def dispose_database_manager() -> None:
    """Dispose and reset the process-level database manager."""

    await _database_registry.dispose()
