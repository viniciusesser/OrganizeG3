"""SQLAlchemy repository for tenant branches."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime
from typing import cast
import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from organizeg3_api.core.exceptions import (
    NotFoundError,
)
from organizeg3_api.domain.branch.entity import (
    Branch,
)
from organizeg3_api.domain.branch.repository import (
    BranchRepository,
)
from organizeg3_api.infrastructure.persistence.models.branch import (
    BranchModel,
)


class SQLAlchemyBranchRepository(
    BranchRepository
):
    """Persist and resolve branches using SQLAlchemy."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def exists_active_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID,
    ) -> bool:
        """Return whether an active branch belongs to the tenant."""

        statement = (
            select(
                BranchModel.id
            )
            .where(
                BranchModel.id
                == branch_id,
                BranchModel.tenant_id
                == tenant_id,
                BranchModel.is_active
                .is_(True),
            )
            .limit(1)
        )

        return (
            self._session.execute(
                statement
            ).scalar_one_or_none()
            is not None
        )

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID,
    ) -> Branch | None:
        """Return one branch belonging to a tenant."""

        statement = (
            select(
                BranchModel
            )
            .where(
                BranchModel.id
                == branch_id,
                BranchModel.tenant_id
                == tenant_id,
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
        is_headquarters: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Branch]:
        """List branches within one tenant boundary."""

        statement = select(
            BranchModel
        ).where(
            BranchModel.tenant_id
            == tenant_id
        )

        if not include_inactive:
            statement = statement.where(
                BranchModel.is_active
                .is_(True)
            )

        if is_headquarters is not None:
            statement = statement.where(
                BranchModel.is_headquarters
                .is_(is_headquarters)
            )

        normalized_search = (
            search.strip().lower()
            if search is not None
            else ""
        )

        if normalized_search:
            statement = statement.where(
                or_(
                    func.lower(
                        BranchModel.code
                    ).contains(
                        normalized_search,
                        autoescape=True,
                    ),
                    func.lower(
                        BranchModel.name
                    ).contains(
                        normalized_search,
                        autoescape=True,
                    ),
                    func.lower(
                        BranchModel.legal_name
                    ).contains(
                        normalized_search,
                        autoescape=True,
                    ),
                    func.lower(
                        BranchModel.document_number
                    ).contains(
                        normalized_search,
                        autoescape=True,
                    ),
                    func.lower(
                        BranchModel.email
                    ).contains(
                        normalized_search,
                        autoescape=True,
                    ),
                )
            )

        statement = (
            statement
            .order_by(
                BranchModel.is_headquarters.desc(),
                BranchModel.code.asc(),
                BranchModel.id.asc(),
            )
            .limit(limit)
            .offset(offset)
        )

        models = self._session.scalars(
            statement
        ).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_branch_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a normalized code already exists."""

        normalized_code = (
            code.strip().lower()
        )

        statement = select(
            BranchModel.id
        ).where(
            BranchModel.tenant_id
            == tenant_id,
            func.lower(
                func.trim(
                    BranchModel.code
                )
            )
            == normalized_code,
        )

        if exclude_branch_id is not None:
            statement = statement.where(
                BranchModel.id
                != exclude_branch_id
            )

        statement = statement.limit(1)

        return (
            self._session.scalar(
                statement
            )
            is not None
        )

    def exists_headquarters_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        exclude_branch_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether the tenant already has a headquarters branch."""

        statement = select(
            BranchModel.id
        ).where(
            BranchModel.tenant_id
            == tenant_id,
            BranchModel.is_headquarters
            .is_(True),
        )

        if exclude_branch_id is not None:
            statement = statement.where(
                BranchModel.id
                != exclude_branch_id
            )

        statement = statement.limit(1)

        return (
            self._session.scalar(
                statement
            )
            is not None
        )

    def add(
        self,
        branch: Branch,
    ) -> Branch:
        """Persist a new branch."""

        model = BranchModel(
            id=branch.id,
            tenant_id=branch.tenant_id,
            code=branch.code,
            name=branch.name,
            legal_name=branch.legal_name,
            document_number=branch.document_number,
            state_registration=(
                branch.state_registration
            ),
            email=branch.email,
            phone=branch.phone,
            website=branch.website,
            street=branch.street,
            number=branch.number,
            district=branch.district,
            city=branch.city,
            state=branch.state,
            postal_code=branch.postal_code,
            is_headquarters=(
                branch.is_headquarters
            ),
            is_active=branch.is_active,
            created_at=branch.created_at,
            updated_at=branch.updated_at,
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
        branch: Branch,
    ) -> Branch:
        """Persist changes to an existing branch."""

        if branch.id is None:
            raise ValueError(
                "A filial deve possuir identificador para ser atualizada."
            )

        statement = select(
            BranchModel
        ).where(
            BranchModel.id
            == branch.id,
            BranchModel.tenant_id
            == branch.tenant_id,
        )

        model = self._session.scalar(
            statement
        )

        if model is None:
            raise NotFoundError(
                "Filial não encontrada."
            )

        model.code = branch.code
        model.name = branch.name
        model.legal_name = branch.legal_name
        model.document_number = branch.document_number
        model.state_registration = (
            branch.state_registration
        )
        model.email = branch.email
        model.phone = branch.phone
        model.website = branch.website
        model.street = branch.street
        model.number = branch.number
        model.district = branch.district
        model.city = branch.city
        model.state = branch.state
        model.postal_code = branch.postal_code
        model.is_headquarters = (
            branch.is_headquarters
        )
        model.is_active = branch.is_active
        model.updated_at = (
            branch.updated_at
            or datetime.now(UTC)
        )

        self._session.flush()

        return self._to_domain(
            model
        )

    @staticmethod
    def _to_domain(
        model: BranchModel,
    ) -> Branch:
        """Convert persistence state into a domain entity."""

        return Branch(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            code=model.code,
            name=model.name,
            legal_name=model.legal_name,
            document_number=model.document_number,
            state_registration=(
                model.state_registration
            ),
            email=model.email,
            phone=model.phone,
            website=model.website,
            street=model.street,
            number=model.number,
            district=model.district,
            city=model.city,
            state=model.state,
            postal_code=model.postal_code,
            is_headquarters=(
                model.is_headquarters
            ),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
