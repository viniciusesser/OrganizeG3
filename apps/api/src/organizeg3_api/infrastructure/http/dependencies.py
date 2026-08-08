"""FastAPI dependencies shared by HTTP endpoints."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Annotated
import uuid

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from organizeg3_api.application.tenant.resolve_active_tenant import (
    ResolveActiveTenant,
)
from organizeg3_api.core.exceptions import ValidationError
from organizeg3_api.core.logging import set_request_context
from organizeg3_api.infrastructure.database.session import (
    get_database_session,
)
from organizeg3_api.infrastructure.persistence.repositories.tenant_repository import (
    SQLAlchemyTenantRepository,
)


def get_db_session() -> Iterator[Session]:
    """Delegate transaction ownership to database infrastructure."""

    yield from get_database_session()


DatabaseSession = Annotated[
    Session,
    Depends(get_db_session),
]


def parse_tenant_header(
    raw_tenant_id: str | None,
) -> uuid.UUID:
    """Parse and validate the tenant header syntax."""

    if (
        raw_tenant_id is None
        or not raw_tenant_id.strip()
    ):
        raise ValidationError(
            "O cabeçalho X-Tenant-ID é obrigatório."
        )

    try:
        tenant_id = uuid.UUID(
            raw_tenant_id.strip()
        )
    except ValueError as exception:
        raise ValidationError(
            "O cabeçalho X-Tenant-ID deve conter um UUID válido."
        ) from exception

    if tenant_id.int == 0:
        raise ValidationError(
            "O cabeçalho X-Tenant-ID não pode conter o UUID nulo."
        )

    return tenant_id


def parse_branch_header(
    raw_branch_id: str | None,
) -> uuid.UUID | None:
    """Parse the optional branch header syntax."""

    if raw_branch_id is None:
        return None

    normalized = raw_branch_id.strip()

    if not normalized:
        return None

    try:
        branch_id = uuid.UUID(
            normalized
        )
    except ValueError as exception:
        raise ValidationError(
            "O cabeçalho X-Branch-ID deve conter um UUID válido."
        ) from exception

    if branch_id.int == 0:
        raise ValidationError(
            "O cabeçalho X-Branch-ID não pode conter o UUID nulo."
        )

    return branch_id


def get_tenant_id(
    database_session: DatabaseSession,
    raw_tenant_id: Annotated[
        str | None,
        Header(alias="X-Tenant-ID"),
    ] = None,
) -> uuid.UUID:
    """Resolve an existing active tenant for the current request."""

    tenant_id = parse_tenant_header(
        raw_tenant_id
    )

    tenant_repository = SQLAlchemyTenantRepository(
        database_session
    )

    resolver = ResolveActiveTenant(
        tenant_repository
    )

    resolved_tenant_id = resolver.execute(
        tenant_id
    )

    set_request_context(
        tenant_id=str(
            resolved_tenant_id
        )
    )

    return resolved_tenant_id


TenantId = Annotated[
    uuid.UUID,
    Depends(get_tenant_id),
]
