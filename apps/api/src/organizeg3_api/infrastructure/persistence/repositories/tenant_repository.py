"""Synchronous SQLAlchemy tenant repository."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.tenant.repository import ITenantRepository
from organizeg3_api.infrastructure.persistence.models.tenant import TenantModel


class SQLAlchemyTenantRepository(ITenantRepository):
    """Query tenant availability using the platform database."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def is_active(
        self,
        tenant_id: uuid.UUID,
    ) -> bool:
        """Return whether the tenant exists and is fully active."""

        statement = (
            select(TenantModel.id)
            .where(
                TenantModel.id == tenant_id,
                TenantModel.is_active.is_(True),
                TenantModel.status == "ACTIVE",
            )
            .limit(1)
        )

        return (
            self._session.execute(statement).scalar_one_or_none()
            is not None
        )
