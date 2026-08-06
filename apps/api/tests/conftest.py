"""Shared fixtures for the OrganizeG3 API test suite."""

from __future__ import annotations

from collections.abc import Iterator
import os
import uuid

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from organizeg3_api.config import Environment, Settings
from organizeg3_api.infrastructure.database.base import Base
from organizeg3_api.infrastructure.http.dependencies import get_db_session
from organizeg3_api.infrastructure.persistence.models.customer import (
    CustomerModel,
)
from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantModel,
)
from organizeg3_api.main import create_application

__all__ = [
    "CustomerModel",
    "TenantModel",
]


@pytest.fixture
def tenant_id() -> uuid.UUID:
    """Return a stable tenant identifier for one test."""

    return uuid.uuid4()


@pytest.fixture
def other_tenant_id() -> uuid.UUID:
    """Return another tenant identifier."""

    return uuid.uuid4()


@pytest.fixture(scope="session")
def test_database_url() -> str:
    """Return the explicitly configured disposable test database URL."""

    test_url = os.getenv(
        "TEST_DATABASE_URL",
        "",
    ).strip()

    development_url = os.getenv(
        "DATABASE_URL",
        "",
    ).strip()

    if not test_url:
        pytest.fail(
            "TEST_DATABASE_URL deve apontar para "
            "um banco descartável de testes."
        )

    if development_url and test_url == development_url:
        pytest.fail(
            "TEST_DATABASE_URL não pode ser igual a DATABASE_URL."
        )

    return test_url


@pytest.fixture
def engine(
    test_database_url: str,
) -> Iterator[Engine]:
    """Create an isolated engine exclusively from TEST_DATABASE_URL."""

    options: dict[str, object] = {}

    if test_database_url.startswith("sqlite"):
        options = {
            "connect_args": {
                "check_same_thread": False,
            },
            "poolclass": StaticPool,
        }

    database_engine = create_engine(
        test_database_url,
        **options,
    )

    Base.metadata.create_all(
        database_engine
    )

    try:
        yield database_engine
    finally:
        Base.metadata.drop_all(
            database_engine
        )

        database_engine.dispose()


@pytest.fixture
def session(
    engine: Engine,
) -> Iterator[Session]:
    """Provide one isolated SQLAlchemy session per test."""

    factory = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
    )

    database_session = factory()

    try:
        yield database_session
    finally:
        database_session.rollback()
        database_session.close()


@pytest.fixture
def client(
    session: Session,
    test_database_url: str,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Create a FastAPI client with two active test tenants."""

    session.add_all(
        [
            TenantModel(
                id=tenant_id,
                name="Empresa de Teste",
                status="ACTIVE",
                is_active=True,
            ),
            TenantModel(
                id=other_tenant_id,
                name="Outra Empresa de Teste",
                status="ACTIVE",
                is_active=True,
            ),
        ]
    )

    session.flush()

    settings = Settings(
        _env_file=None,
        APP_ENVIRONMENT=Environment.TEST,
        DATABASE_URL=test_database_url,
        DOCS_ENABLED=False,
        LOG_JSON=False,
    )

    application = create_application(
        settings
    )

    def override_database_session() -> Iterator[Session]:
        yield session

    application.dependency_overrides[
        get_db_session
    ] = override_database_session

    with TestClient(application) as test_client:
        yield test_client

    application.dependency_overrides.clear()
