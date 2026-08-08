"""Request context definitions for tenant branches."""

from __future__ import annotations

from dataclasses import dataclass
import uuid


@dataclass(frozen=True, slots=True)
class BranchContext:
    """Represent the optional operational branch of a request."""

    tenant_id: uuid.UUID
    branch_id: uuid.UUID | None

    @property
    def has_branch(self) -> bool:
        """Return whether the request is scoped to a branch."""

        return self.branch_id is not None
