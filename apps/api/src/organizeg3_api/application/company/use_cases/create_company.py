"""Create-company use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.company.schemas import CompanyCreate
from organizeg3_api.core.exceptions import ConflictError, ValidationError
from organizeg3_api.domain.company.entity import Company
from organizeg3_api.domain.company.repository import ICompanyRepository


class CreateCompanyUseCase:
    """Create the single company owned by one tenant."""

    def __init__(
        self,
        repository: ICompanyRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        payload: CompanyCreate,
    ) -> Company:
        """Create the company when the tenant does not own one yet."""

        existing = self._repository.get_by_tenant(
            tenant_id
        )

        if existing is not None:
            raise ConflictError(
                "O tenant já possui uma empresa cadastrada.",
                details={
                    "tenant_id": str(tenant_id),
                    "company_id": (
                        str(existing.id)
                        if existing.id is not None
                        else None
                    ),
                },
            )

        try:
            company = Company.create(
                tenant_id=tenant_id,
                trade_name=payload.trade_name,
                legal_name=payload.legal_name,
                document_number=payload.document_number,
                state_registration=payload.state_registration,
                email=payload.email,
                phone=payload.phone,
                website=payload.website,
                logo_path=payload.logo_path,
                street=payload.street,
                number=payload.number,
                district=payload.district,
                city=payload.city,
                state=payload.state,
                postal_code=payload.postal_code,
            )
        except (TypeError, ValueError) as exception:
            raise ValidationError(
                str(exception)
            ) from exception

        return self._repository.add(
            company
        )
