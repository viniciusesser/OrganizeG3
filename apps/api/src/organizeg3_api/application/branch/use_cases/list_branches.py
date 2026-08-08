"""List-branches use case."""

from __future__ import annotations

from collections.abc import Sequence
import uuid

from organizeg3_api.domain.branch.entity import (
    Branch,
)
from organizeg3_api.domain.branch.repository import (
    BranchRepository,
)


class ListBranchesUseCase:
    """List branches owned by one tenant."""

    def __init__(
        self,
        repository: BranchRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        *,
        include_inactive: bool = False,
        search: str | None = None,
        is_headquarters: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Branch]:
        """Return filtered and paginated branches."""

        return self._repository.list_all(
            tenant_id=tenant_id,
            include_inactive=include_inactive,
            search=search,
            is_headquarters=is_headquarters,
            limit=limit,
            offset=offset,
        )
