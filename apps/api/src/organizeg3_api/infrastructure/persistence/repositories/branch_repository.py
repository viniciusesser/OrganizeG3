"""SQLAlchemy repository for tenant branches."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

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
