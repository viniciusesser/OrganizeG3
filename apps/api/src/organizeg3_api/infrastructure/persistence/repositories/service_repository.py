"""SQLAlchemy repository for tenant services."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from organizeg3_api.domain.service.entity import (
    Service,
)
from organizeg3_api.domain.service.repository import (
    ServiceRepository,
)
from organizeg3_api.domain.service.value_objects import (
    ServiceCategory,
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

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        category: str | None = None,
        execution_mode: ServiceExecutionMode | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Service]:
        """List services belonging to one tenant."""

        statement = select(
            ServiceModel
        ).where(
            ServiceModel.tenant_id == tenant_id
        )

        if not include_inactive:
            statement = statement.where(
                ServiceModel.is_active.is_(
                    True
                )
            )

        if search is not None:
            normalized_search = search.strip()

            if normalized_search:
                pattern = (
                    f"%{normalized_search}%"
                )

                statement = statement.where(
                    or_(
                        ServiceModel.code.ilike(
                            pattern
                        ),
                        ServiceModel.name.ilike(
                            pattern
                        ),
                        ServiceModel.category.ilike(
                            pattern
                        ),
                        ServiceModel.unit.ilike(
                            pattern
                        ),
                    )
                )

        if category is not None:
            normalized_category = ServiceCategory(
                category
            ).value

            statement = statement.where(
                ServiceModel.category
                == normalized_category
            )

        if execution_mode is not None:
            if not isinstance(
                execution_mode,
                ServiceExecutionMode,
            ):
                raise TypeError(
                    "O filtro de modo de execução "
                    "deve ser um ServiceExecutionMode."
                )

            statement = statement.where(
                ServiceModel.execution_mode
                == execution_mode.value
            )

        statement = (
            statement
            .order_by(
                ServiceModel.name,
                ServiceModel.code,
                ServiceModel.id,
            )
            .limit(
                limit
            )
            .offset(
                offset
            )
        )

        models = self._session.execute(
            statement
        ).scalars().all()

        return [
            self._to_domain(
                model
            )
            for model in models
        ]

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_service_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a normalized service code exists."""

        normalized_code = ServiceCode(
            code
        ).value

        statement = select(
            ServiceModel.id
        ).where(
            ServiceModel.tenant_id == tenant_id,
            ServiceModel.code == normalized_code,
        )

        if exclude_service_id is not None:
            statement = statement.where(
                ServiceModel.id
                != exclude_service_id
            )

        statement = statement.limit(1)

        return (
            self._session.execute(
                statement
            ).scalar_one_or_none()
            is not None
        )

    def add(
        self,
        service: Service,
    ) -> Service:
        """Persist a new service."""

        if service.created_at is None:
            raise ValueError(
                "O serviço deve possuir created_at "
                "antes de ser persistido."
            )

        if service.updated_at is None:
            raise ValueError(
                "O serviço deve possuir updated_at "
                "antes de ser persistido."
            )

        model = ServiceModel(
            id=service.id,
            tenant_id=service.tenant_id,
            code=service.code,
            name=service.name,
            category=service.category,
            unit=service.unit,
            execution_mode=(
                service.execution_mode.value
            ),
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

    def save(
        self,
        service: Service,
    ) -> Service:
        """Persist changes to an existing service."""

        if service.id is None:
            raise ValueError(
                "O serviço deve possuir identificador "
                "antes de ser salvo."
            )

        if service.updated_at is None:
            raise ValueError(
                "O serviço deve possuir updated_at "
                "antes de ser salvo."
            )

        statement = (
            select(
                ServiceModel
            )
            .where(
                ServiceModel.id == service.id,
                ServiceModel.tenant_id
                == service.tenant_id,
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
            raise ValueError(
                "O serviço informado não foi encontrado "
                "no tenant."
            )

        model.code = service.code
        model.name = service.name
        model.category = service.category
        model.unit = service.unit
        model.execution_mode = (
            service.execution_mode.value
        )
        model.estimated_duration_minutes = (
            service.estimated_duration_minutes
        )
        model.is_active = service.is_active
        model.updated_at = service.updated_at

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
