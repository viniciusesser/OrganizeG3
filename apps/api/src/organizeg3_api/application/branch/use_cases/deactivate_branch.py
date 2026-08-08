"""Deactivate-branch use case."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import (
    NotFoundError,
)
from organizeg3_api.domain.branch.entity import (
    Branch,
)
from organizeg3_api.domain.branch.repository import (
    BranchRepository,
)


class DeactivateBranchUseCase:
    """Deactivate one tenant-owned branch."""

    def __init__(
        self,
        repository: BranchRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID,
    ) -> Branch:
        """Deactivate one branch idempotently."""

        branch = (
            self._repository.get_by_id_for_tenant(
                tenant_id=tenant_id,
                branch_id=branch_id,
            )
        )

        if branch is None:
            raise NotFoundError(
                "Filial não encontrada."
            )

        if not branch.is_active:
            return branch

        branch.deactivate()

        return self._repository.save(
            branch
        )
