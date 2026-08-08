"""SQLAlchemy repository for tenant materials."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.material.entity import (
    Material,
)
from organizeg3_api.domain.material.repository import (
    MaterialRepository,
)
from organizeg3_api.domain.material.value_objects import (
    MaterialCode,
)
from organizeg3_api.infrastructure.persistence.models.brand import (
    BrandModel,
)
from organizeg3_api.infrastructure.persistence.models.material import (
    MaterialModel,
)


class SQLAlchemyMaterialRepository(
    MaterialRepository
):
    """Persist tenant materials using SQLAlchemy."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        material_id: uuid.UUID,
    ) -> Material | None:
        """Return one tenant-scoped material."""

        statement = (
            select(
                MaterialModel
            )
            .where(
                MaterialModel.id == material_id,
                MaterialModel.tenant_id == tenant_id,
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
    ) -> Material | None:
        """Return one material by normalized code."""

        normalized_code = MaterialCode(
            code
        ).value

        statement = (
            select(
                MaterialModel
            )
            .where(
                MaterialModel.tenant_id == tenant_id,
                MaterialModel.code == normalized_code,
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
        material: Material,
    ) -> Material:
        """Persist a new material."""

        self._validate_brand_scope(
            tenant_id=material.tenant_id,
            brand_id=material.brand_id,
        )

        model = MaterialModel(
            id=material.id,
            tenant_id=material.tenant_id,
            code=material.code,
            name=material.name,
            category=material.category,
            unit=material.unit,
            brand_id=material.brand_id,
            is_active=material.is_active,
            created_at=material.created_at,
            updated_at=material.updated_at,
        )

        self._session.add(
            model
        )
        self._session.flush()

        return self._to_domain(
            model
        )

    def _validate_brand_scope(
        self,
        *,
        tenant_id: uuid.UUID,
        brand_id: uuid.UUID | None,
    ) -> None:
        """Ensure optional brand belongs to the same tenant."""

        if brand_id is None:
            return

        statement = (
            select(
                BrandModel.id
            )
            .where(
                BrandModel.id == brand_id,
                BrandModel.tenant_id == tenant_id,
            )
            .limit(1)
        )

        existing_brand = (
            self._session.execute(
                statement
            )
            .scalar_one_or_none()
        )

        if existing_brand is None:
            raise ValueError(
                "A marca do material não pertence "
                "ao tenant informado."
            )

    @staticmethod
    def _to_domain(
        model: MaterialModel,
    ) -> Material:
        """Convert persistence model to domain entity."""

        return Material(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            code=model.code,
            name=model.name,
            category=model.category,
            unit=model.unit,
            brand_id=model.brand_id,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
