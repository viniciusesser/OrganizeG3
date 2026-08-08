"""Branch persistence contracts."""

from __future__ import annotations

from collections.abc import Sequence
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
        ...

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_branch_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a normalized code already exists."""
        ...

    def exists_headquarters_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        exclude_branch_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether the tenant already has a headquarters branch."""
        ...

    def add(
        self,
        branch: Branch,
    ) -> Branch:
        """Persist a new branch."""
        ...

    def save(
        self,
        branch: Branch,
    ) -> Branch:
        """Persist changes to an existing branch."""
        ...
