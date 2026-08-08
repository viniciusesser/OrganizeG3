"""List-employees use case."""

from __future__ import annotations

import uuid

from organizeg3_api.domain.employee.entity import (
    Employee,
)
from organizeg3_api.domain.employee.repository import (
    EmployeeRepository,
)
from organizeg3_api.domain.employee.value_objects import (
    EmploymentStatus,
)


class ListEmployeesUseCase:
    """List employees belonging to one tenant."""

    def __init__(
        self,
        repository: EmployeeRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        *,
        include_inactive: bool = False,
        search: str | None = None,
        branch_id: uuid.UUID | None = None,
        status: EmploymentStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Employee]:
        """Return tenant employees using optional filters."""

        return self._repository.list_all(
            tenant_id=tenant_id,
            include_inactive=include_inactive,
            search=search,
            branch_id=branch_id,
            status=status,
            limit=limit,
            offset=offset,
        )
