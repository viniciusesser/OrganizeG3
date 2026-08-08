"""Resolve the optional active branch for a tenant request."""

from __future__ import annotations

import uuid

from organizeg3_api.application.branch.exceptions import (
    BranchUnavailableError,
    InvalidBranchIdentifierError,
)
from organizeg3_api.domain.branch.repository import (
    BranchRepository,
)


class ResolveActiveBranch:
    """Resolve an optional branch inside the current tenant boundary."""

    def __init__(
        self,
        repository: BranchRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID | None,
    ) -> uuid.UUID | None:
        """Return a validated branch identifier when provided."""

        if branch_id is None:
            return None

        if tenant_id.int == 0:
            raise InvalidBranchIdentifierError(
                "O tenant atual não pode possuir UUID nulo.",
            )

        if branch_id.int == 0:
            raise InvalidBranchIdentifierError(
                "O cabeçalho X-Branch-ID não pode conter o UUID nulo.",
            )

        if not self._repository.exists_active_for_tenant(
            tenant_id=tenant_id,
            branch_id=branch_id,
        ):
            raise BranchUnavailableError(
                "A filial informada não está disponível.",
                details={
                    "reason": "branch_unavailable",
                },
            )

        return branch_id
