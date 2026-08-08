"""Get-company use case."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import NotFoundError
from organizeg3_api.domain.company.entity import Company
from organizeg3_api.domain.company.repository import ICompanyRepository


class GetCompanyUseCase:
    """Return the company owned by the authenticated tenant."""

    def __init__(
        self,
        repository: ICompanyRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
    ) -> Company:
        """Return the tenant company or raise a controlled error."""

        company = self._repository.get_by_tenant(
            tenant_id
        )

        if company is None:
            raise NotFoundError(
                "Empresa não encontrada."
            )

        return company
