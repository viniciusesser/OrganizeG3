"""SQLAlchemy repository for tenant material brands."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.brand.entity import (
    Brand,
)
from organizeg3_api.domain.brand.repository import (
    BrandRepository,
)
from organizeg3_api.domain.brand.value_objects import (
    BrandName,
)
from organizeg3_api.infrastructure.persistence.models.brand import (
    BrandModel,
)


class SQLAlchemyBrandRepository(
    BrandRepository
):
    """Persist material brands using SQLAlchemy."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        brand_id: uuid.UUID,
    ) -> Brand | None:
        """Return one tenant-scoped brand."""

        statement = (
            select(
                BrandModel
            )
            .where(
                BrandModel.id == brand_id,
                BrandModel.tenant_id == tenant_id,
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

    def get_by_name_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        name: str,
    ) -> Brand | None:
        """Return one tenant-scoped brand by normalized name."""

        normalized_name = BrandName(
            name
        ).value

        statement = (
            select(
                BrandModel
            )
            .where(
                BrandModel.tenant_id == tenant_id,
                BrandModel.name == normalized_name,
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
        brand: Brand,
    ) -> Brand:
        """Persist a new brand."""

        model = BrandModel(
            id=brand.id,
            tenant_id=brand.tenant_id,
            code=brand.code,
            name=brand.name,
            is_active=brand.is_active,
            created_at=brand.created_at,
            updated_at=brand.updated_at,
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
        model: BrandModel,
    ) -> Brand:
        """Convert persistence model to domain entity."""

        return Brand(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            code=model.code,
            name=model.name,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
