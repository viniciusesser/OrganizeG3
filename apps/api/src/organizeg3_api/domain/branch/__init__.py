"""Branch domain definitions."""

from organizeg3_api.domain.branch.context import (
    BranchContext,
)
from organizeg3_api.domain.branch.entity import (
    Branch,
)
from organizeg3_api.domain.branch.repository import (
    BranchRepository,
)
from organizeg3_api.domain.branch.value_objects import (
    BranchCode,
    BranchDocument,
    BranchEmail,
    BranchPhone,
    BranchPostalCode,
    BranchState,
)

__all__ = [
    "Branch",
    "BranchCode",
    "BranchContext",
    "BranchDocument",
    "BranchEmail",
    "BranchPhone",
    "BranchPostalCode",
    "BranchRepository",
    "BranchState",
]
