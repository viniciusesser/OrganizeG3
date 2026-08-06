"""Synchronous SQLAlchemy engine and transactional session management."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from organizeg3_api.config import Settings, get_settings
from organizeg3_api.core.logging import get_logger

logger = get_logger(__name__)


class DatabaseNotConfiguredError(RuntimeError):
    """Raised when a database operation is requested without configuration."""


class DatabaseManager:
    """Own the process-level synchronous engine and session factory."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._engine: Engine | None = None
        self._session_factory: sessionmaker[Session] | None = None

    @property
    def is_configured(self) -> bool:
        return self._settings.database_url is not None

    @property
    def is_initialized(self) -> bool:
        return self._engine is not None

    @property
    def engine(self) -> Engine:
        self._ensure_initialized()
        if self._engine is None:
            raise DatabaseNotConfiguredError("O engine do banco não foi inicializado.")
        return self._engine

    @property
    def session_factory(self) -> sessionmaker[Session]:
        self._ensure_initialized()
        if self._session_factory is None:
            raise DatabaseNotConfiguredError("A fábrica de sessões não foi inicializada.")
        return self._session_factory

    def initialize(self) -> None:
        if self.is_initialized:
            return

        database_url = self._normalize_database_url(self._get_database_url())
        if database_url.startswith("sqlite"):
            self._engine = create_engine(
                database_url,
                echo=self._settings.database_echo,
                pool_pre_ping=True,
            )
        else:
            self._engine = create_engine(
                database_url,
                echo=self._settings.database_echo,
                pool_pre_ping=True,
                pool_size=self._settings.database_pool_size,
                max_overflow=self._settings.database_max_overflow,
                pool_timeout=self._settings.database_pool_timeout_seconds,
                pool_recycle=self._settings.database_pool_recycle_seconds,
            )
        self._session_factory = sessionmaker(
            bind=self._engine,
            class_=Session,
            autoflush=False,
            expire_on_commit=False,
        )
        logger.info("database_engine_initialized")

    def dispose(self) -> None:
        if self._engine is None:
            return
        self._engine.dispose()
        self._engine = None
        self._session_factory = None
        logger.info("database_engine_disposed")

    @contextmanager
    def session(self) -> Iterator[Session]:
        database_session = self.session_factory()
        try:
            yield database_session
            database_session.commit()
        except Exception:
            database_session.rollback()
            logger.exception("database_transaction_rolled_back")
            raise
        finally:
            database_session.close()

    def health_check(self) -> bool:
        if not self.is_configured:
            return False
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except Exception:
            logger.exception("database_health_check_failed")
            return False
        return True

    def _ensure_initialized(self) -> None:
        if not self.is_initialized:
            self.initialize()

    def _get_database_url(self) -> str:
        try:
            return self._settings.require_database_url()
        except RuntimeError as exception:
            raise DatabaseNotConfiguredError(str(exception)) from exception

    @staticmethod
    def _normalize_database_url(database_url: str) -> str:
        normalized_url = database_url.strip()
        if normalized_url.startswith("postgres://"):
            return normalized_url.replace("postgres://", "postgresql+psycopg://", 1)
        if normalized_url.startswith("postgresql://"):
            return normalized_url.replace("postgresql://", "postgresql+psycopg://", 1)
        return normalized_url


class DatabaseManagerRegistry:
    """Store the process-level manager while allowing test replacement."""

    def __init__(self) -> None:
        self._manager: DatabaseManager | None = None

    def get(self, settings: Settings | None = None) -> DatabaseManager:
        if self._manager is None:
            self._manager = DatabaseManager(settings or get_settings())
        return self._manager

    def dispose(self) -> None:
        if self._manager is None:
            return
        self._manager.dispose()
        self._manager = None


_database_registry = DatabaseManagerRegistry()


def get_database_manager(settings: Settings | None = None) -> DatabaseManager:
    """Return the process-level database manager."""

    return _database_registry.get(settings)


def get_database_session() -> Iterator[Session]:
    """FastAPI dependency providing one transaction per request."""

    manager = get_database_manager()
    with manager.session() as database_session:
        yield database_session


def dispose_database_manager() -> None:
    """Dispose and reset the process-level database manager."""

    _database_registry.dispose()
