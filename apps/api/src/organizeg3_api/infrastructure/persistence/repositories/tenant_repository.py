"""SQLAlchemy implementation of the tenant repository."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.tenant.repository import ITenantRepository
from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantRecordModel,
)


class SQLAlchemyTenantRepository(
    ITenantRepository
):
    """Read tenant availability from the relational database."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def exists_active(
        self,
        tenant_id: uuid.UUID,
    ) -> bool:
        """Return whether the tenant exists and is operational."""

        statement = (
            select(TenantRecordModel.id)
            .where(
                TenantRecordModel.id == tenant_id,
                TenantRecordModel.is_active.is_(True),
                TenantRecordModel.status == "ACTIVE",
            )
            .limit(1)
        )

        return (
            self._session.execute(
                statement
            ).scalar_one_or_none()
            is not None
        )
