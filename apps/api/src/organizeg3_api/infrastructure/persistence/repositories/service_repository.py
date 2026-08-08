"""SQLAlchemy repository for tenant services."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.service.entity import (
    Service,
)
from organizeg3_api.domain.service.repository import (
    ServiceRepository,
)
from organizeg3_api.domain.service.value_objects import (
    ServiceCode,
    ServiceExecutionMode,
)
from organizeg3_api.infrastructure.persistence.models.service import (
    ServiceModel,
)


class SQLAlchemyServiceRepository(
    ServiceRepository
):
    """Persist tenant services using SQLAlchemy."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        service_id: uuid.UUID,
    ) -> Service | None:
        """Return one tenant-scoped service."""

        statement = (
            select(
                ServiceModel
            )
            .where(
                ServiceModel.id == service_id,
                ServiceModel.tenant_id == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(
                statement
            )
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(
            model
        )

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> Service | None:
        """Return one service by normalized code."""

        normalized_code = ServiceCode(
            code
        ).value

        statement = (
            select(
                ServiceModel
            )
            .where(
                ServiceModel.tenant_id == tenant_id,
                ServiceModel.code == normalized_code,
            )
            .limit(1)
        )

        model = (
            self._session.execute(
                statement
            )
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(
            model
        )

    def add(
        self,
        service: Service,
    ) -> Service:
        """Persist a new service."""

        model = ServiceModel(
            id=service.id,
            tenant_id=service.tenant_id,
            code=service.code,
            name=service.name,
            category=service.category,
            unit=service.unit,
            execution_mode=service.execution_mode.value,
            estimated_duration_minutes=(
                service.estimated_duration_minutes
            ),
            is_active=service.is_active,
            created_at=service.created_at,
            updated_at=service.updated_at,
        )

        self._session.add(
            model
        )
        self._session.flush()

        return self._to_domain(
            model
        )

    @staticmethod
    def _to_domain(
        model: ServiceModel,
    ) -> Service:
        """Convert persistence model to domain entity."""

        return Service(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            code=model.code,
            name=model.name,
            category=model.category,
            unit=model.unit,
            execution_mode=ServiceExecutionMode(
                model.execution_mode
            ),
            estimated_duration_minutes=(
                model.estimated_duration_minutes
            ),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
