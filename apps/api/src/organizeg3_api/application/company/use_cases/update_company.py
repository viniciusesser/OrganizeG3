"""Update-company use case."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
import uuid

from organizeg3_api.application.company.schemas import CompanyUpdate
from organizeg3_api.core.exceptions import NotFoundError, ValidationError
from organizeg3_api.domain.company.entity import Company
from organizeg3_api.domain.company.repository import ICompanyRepository


class UpdateCompanyUseCase:
    """Update the company owned by the authenticated tenant."""

    def __init__(
        self,
        repository: ICompanyRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        payload: CompanyUpdate,
    ) -> Company:
        """Apply a partial company update."""

        company = self._repository.get_by_tenant(
            tenant_id
        )

        if company is None:
            raise NotFoundError(
                "Empresa não encontrada."
            )

        changed_fields = payload.model_fields_set

        if not changed_fields:
            raise ValidationError(
                "Informe ao menos um campo para atualizar."
            )

        candidate = replace(
            company
        )

        values = {
            field_name: getattr(
                payload,
                field_name,
            )
            for field_name in changed_fields
        }

        if (
            "trade_name" in values
            and values["trade_name"] is None
        ):
            raise ValidationError(
                "O nome fantasia da empresa não pode ser nulo."
            )

        try:
            for field_name, value in values.items():
                setattr(
                    candidate,
                    field_name,
                    value,
                )

            candidate.updated_at = datetime.now(UTC)

            candidate.__post_init__()
        except (TypeError, ValueError) as exception:
            raise ValidationError(
                str(exception)
            ) from exception

        return self._repository.save(
            candidate
        )
