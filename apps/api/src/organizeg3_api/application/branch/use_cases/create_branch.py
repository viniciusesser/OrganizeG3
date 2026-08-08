"""Create-branch use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.branch.schemas import (
    BranchCreate,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    ValidationError,
)
from organizeg3_api.domain.branch.entity import (
    Branch,
)
from organizeg3_api.domain.branch.repository import (
    BranchRepository,
)


class CreateBranchUseCase:
    """Create one branch inside the authenticated tenant."""

    def __init__(
        self,
        repository: BranchRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        payload: BranchCreate,
    ) -> Branch:
        """Create and persist a tenant-owned branch."""

        if self._repository.exists_by_code(
            tenant_id=tenant_id,
            code=payload.code,
        ):
            raise ConflictError(
                "Já existe uma filial com este código."
            )

        if (
            payload.is_headquarters
            and self._repository.exists_headquarters_for_tenant(
                tenant_id=tenant_id
            )
        ):
            raise ConflictError(
                "O tenant já possui uma filial matriz."
            )

        try:
            branch = Branch.create(
                tenant_id=tenant_id,
                code=payload.code,
                name=payload.name,
                legal_name=payload.legal_name,
                document_number=payload.document_number,
                state_registration=payload.state_registration,
                email=payload.email,
                phone=payload.phone,
                website=payload.website,
                street=payload.street,
                number=payload.number,
                district=payload.district,
                city=payload.city,
                state=payload.state,
                postal_code=payload.postal_code,
                is_headquarters=payload.is_headquarters,
            )
        except (TypeError, ValueError) as exception:
            raise ValidationError(
                str(exception)
            ) from exception

        return self._repository.add(
            branch
        )
