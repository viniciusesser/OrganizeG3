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

from organizeg3_api.config import (
    Environment,
    Settings,
)
from organizeg3_api.domain.identity.authentication import (
    VerifiedToken,
)
from organizeg3_api.domain.identity.permissions import (
    CustomerPermissions,
)
from organizeg3_api.infrastructure.database.base import Base
from organizeg3_api.infrastructure.http.dependencies import (
    get_db_session,
)
from organizeg3_api.infrastructure.persistence.models import (  # noqa: F401
    CustomerModel,
    TenantRecordModel,
)
from organizeg3_api.main import create_application
from tests.helpers.authentication import (
    StubTokenVerifier,
    authentication_headers,
    create_active_membership,
    create_test_user,
    grant_permissions,
    override_token_verifier,
)


@pytest.fixture
def tenant_id() -> uuid.UUID:
    """Return a stable active tenant identifier."""

    return uuid.uuid4()


@pytest.fixture
def other_tenant_id() -> uuid.UUID:
    """Return another active tenant identifier."""

    return uuid.uuid4()


@pytest.fixture
def inactive_tenant_id() -> uuid.UUID:
    """Return one inactive tenant identifier."""

    return uuid.uuid4()


@pytest.fixture(scope="session")
def test_database_url() -> str:
    """Return the disposable test database URL."""

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

    if (
        development_url
        and test_url == development_url
    ):
        pytest.fail(
            "TEST_DATABASE_URL não pode ser igual "
            "a DATABASE_URL."
        )

    return test_url


@pytest.fixture
def engine(
    test_database_url: str,
) -> Iterator[Engine]:
    """Create an isolated test engine."""

    options: dict[str, object] = {}

    if test_database_url.startswith(
        "sqlite"
    ):
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
    """Provide one isolated SQLAlchemy session."""

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


def add_test_tenant(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    name: str,
    is_active: bool = True,
    status: str = "ACTIVE",
) -> TenantRecordModel:
    """Persist one tenant used by API tests."""

    tenant = TenantRecordModel(
        id=tenant_id,
        name=name,
        status=status,
        is_active=is_active,
    )

    session.add(tenant)

    return tenant


@pytest.fixture
def client(
    session: Session,
    test_database_url: str,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
    inactive_tenant_id: uuid.UUID,
) -> Iterator[TestClient]:
    """Create an API client with registered test tenants."""

    add_test_tenant(
        session,
        tenant_id=tenant_id,
        name="Tenant Principal",
    )

    add_test_tenant(
        session,
        tenant_id=other_tenant_id,
        name="Tenant Secundário",
    )

    add_test_tenant(
        session,
        tenant_id=inactive_tenant_id,
        name="Tenant Inativo",
        is_active=False,
        status="INACTIVE",
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

    with TestClient(
        application
    ) as test_client:
        yield test_client

    application.dependency_overrides.clear()


@pytest.fixture
def customer_permission_codes() -> tuple[str, ...]:
    """Return every customer permission used by API tests."""

    return (
        CustomerPermissions.READ,
        CustomerPermissions.CREATE,
        CustomerPermissions.UPDATE,
        CustomerPermissions.ARCHIVE,
        CustomerPermissions.REACTIVATE,
    )


@pytest.fixture
def authenticated_customer_client(
    client: TestClient,
    session: Session,
    tenant_id: uuid.UUID,
    other_tenant_id: uuid.UUID,
    customer_permission_codes: tuple[str, ...],
) -> Iterator[TestClient]:
    """Provide a client authorized for customer operations."""

    auth_user_id = uuid.uuid4()

    user = create_test_user(
        session,
        auth_user_id=auth_user_id,
    )

    primary_membership = create_active_membership(
        session,
        tenant_id=tenant_id,
        user=user,
    )

    secondary_membership = create_active_membership(
        session,
        tenant_id=other_tenant_id,
        user=user,
    )

    grant_permissions(
        session,
        tenant_id=tenant_id,
        membership=primary_membership,
        permission_codes=customer_permission_codes,
    )

    grant_permissions(
        session,
        tenant_id=other_tenant_id,
        membership=secondary_membership,
        permission_codes=customer_permission_codes,
    )

    verifier = StubTokenVerifier(
        VerifiedToken(
            auth_user_id=auth_user_id,
            role="authenticated",
            email=user.email,
        )
    )

    with override_token_verifier(
        client,
        verifier,
    ):
        yield client


@pytest.fixture
def customer_headers():
    """Build authenticated headers for customer tests."""

    return authentication_headers
