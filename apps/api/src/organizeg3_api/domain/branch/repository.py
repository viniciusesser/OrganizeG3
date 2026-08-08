"""Branch persistence contracts."""

from __future__ import annotations

from typing import Protocol
import uuid

from organizeg3_api.domain.branch.entity import (
    Branch,
)


class BranchRepository(Protocol):
    """Define persistence operations required by branch workflows."""

    def exists_active_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID,
    ) -> bool:
        """Return whether an active branch belongs to the tenant."""
        ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID,
    ) -> Branch | None:
        """Return one branch belonging to the tenant."""
        ...

    def add(
        self,
        branch: Branch,
    ) -> Branch:
        """Persist a new branch."""
        ...
