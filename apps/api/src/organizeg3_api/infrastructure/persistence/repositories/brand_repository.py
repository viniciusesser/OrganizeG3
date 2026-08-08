"""SQLAlchemy repository for tenant material brands."""

from __future__ import annotations

from datetime import datetime
from typing import cast
import uuid

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from organizeg3_api.domain.brand.entity import (
    Brand,
)
from organizeg3_api.domain.brand.repository import (
    BrandRepository,
)
from organizeg3_api.domain.brand.value_objects import (
    BrandCode,
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

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> Brand | None:
        """Return one tenant-scoped brand by normalized code."""

        normalized_code = BrandCode(
            code
        ).value

        statement = (
            select(
                BrandModel
            )
            .where(
                BrandModel.tenant_id == tenant_id,
                BrandModel.code == normalized_code,
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

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Brand]:
        """List tenant-scoped brands."""

        statement = select(
            BrandModel
        ).where(
            BrandModel.tenant_id == tenant_id
        )

        if not include_inactive:
            statement = statement.where(
                BrandModel.is_active.is_(True)
            )

        normalized_search = (
            search.strip()
            if search is not None
            else ""
        )

        if normalized_search:
            pattern = (
                f"%{normalized_search}%"
            )

            statement = statement.where(
                or_(
                    BrandModel.code.ilike(
                        pattern
                    ),
                    BrandModel.name.ilike(
                        pattern
                    ),
                )
            )

        statement = (
            statement
            .order_by(
                BrandModel.name.asc(),
                BrandModel.id.asc(),
            )
            .limit(
                limit
            )
            .offset(
                offset
            )
        )

        models = (
            self._session.execute(
                statement
            )
            .scalars()
            .all()
        )

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
        exclude_brand_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a normalized code already exists."""

        normalized_code = BrandCode(
            code
        ).value

        statement = (
            select(
                BrandModel.id
            )
            .where(
                BrandModel.tenant_id == tenant_id,
                BrandModel.code == normalized_code,
            )
        )

        if exclude_brand_id is not None:
            statement = statement.where(
                BrandModel.id
                != exclude_brand_id
            )

        statement = statement.limit(
            1
        )

        return (
            self._session.execute(
                statement
            )
            .scalar_one_or_none()
            is not None
        )

    def exists_by_name(
        self,
        *,
        tenant_id: uuid.UUID,
        name: str,
        exclude_brand_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a normalized name already exists."""

        normalized_name = BrandName(
            name
        ).value

        statement = (
            select(
                BrandModel.id
            )
            .where(
                BrandModel.tenant_id == tenant_id,
                BrandModel.name == normalized_name,
            )
        )

        if exclude_brand_id is not None:
            statement = statement.where(
                BrandModel.id
                != exclude_brand_id
            )

        statement = statement.limit(
            1
        )

        return (
            self._session.execute(
                statement
            )
            .scalar_one_or_none()
            is not None
        )

    def add(
        self,
        brand: Brand,
    ) -> Brand:
        """Persist a new brand."""

        created_at = self._require_timestamp(
            brand.created_at,
            field_name="data de criação",
        )

        updated_at = self._require_timestamp(
            brand.updated_at,
            field_name="data de atualização",
        )

        model = BrandModel(
            id=brand.id,
            tenant_id=brand.tenant_id,
            code=brand.code,
            name=brand.name,
            is_active=brand.is_active,
            created_at=created_at,
            updated_at=updated_at,
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
        brand: Brand,
    ) -> Brand:
        """Persist changes to an existing brand."""

        if brand.id is None:
            raise ValueError(
                "A marca deve possuir identificador "
                "para ser atualizada."
            )

        updated_at = self._require_timestamp(
            brand.updated_at,
            field_name="data de atualização",
        )

        statement = (
            select(
                BrandModel
            )
            .where(
                BrandModel.id == brand.id,
                BrandModel.tenant_id == brand.tenant_id,
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
                "A marca não foi encontrada "
                "para atualização."
            )

        model.code = brand.code
        model.name = brand.name
        model.is_active = brand.is_active
        model.updated_at = updated_at

        self._session.flush()

        return self._to_domain(
            model
        )

    @staticmethod
    def _require_timestamp(
        value: datetime | None,
        *,
        field_name: str,
    ) -> datetime:
        """Require a persistence timestamp."""

        if value is None:
            raise ValueError(
                f"A marca deve possuir {field_name}."
            )

        return value

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
