"""SQLAlchemy repository for tenant companies."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.company.entity import (
    Company,
)
from organizeg3_api.domain.company.repository import (
    ICompanyRepository,
)
from organizeg3_api.infrastructure.persistence.models.company import (
    CompanyModel,
)


class SQLAlchemyCompanyRepository(
    ICompanyRepository
):
    """Persist company data using SQLAlchemy."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_tenant(
        self,
        tenant_id: uuid.UUID,
    ) -> Company | None:
        """Return the company owned by one tenant."""

        statement = (
            select(CompanyModel)
            .where(
                CompanyModel.tenant_id
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
        company: Company,
    ) -> Company:
        """Persist a new company."""

        model = CompanyModel(
            id=company.id,
            tenant_id=company.tenant_id,
            trade_name=company.trade_name,
            legal_name=company.legal_name,
            document_number=company.document_number,
            state_registration=(
                company.state_registration
            ),
            email=company.email,
            phone=company.phone,
            website=company.website,
            logo_path=company.logo_path,
            street=company.street,
            number=company.number,
            district=company.district,
            city=company.city,
            state=company.state,
            postal_code=company.postal_code,
            is_active=company.is_active,
            created_at=company.created_at,
            updated_at=company.updated_at,
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
        model: CompanyModel,
    ) -> Company:
        """Convert persistence model to domain entity."""

        return Company(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            trade_name=model.trade_name,
            legal_name=model.legal_name,
            document_number=model.document_number,
            state_registration=(
                model.state_registration
            ),
            email=model.email,
            phone=model.phone,
            website=model.website,
            logo_path=model.logo_path,
            street=model.street,
            number=model.number,
            district=model.district,
            city=model.city,
            state=model.state,
            postal_code=model.postal_code,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
