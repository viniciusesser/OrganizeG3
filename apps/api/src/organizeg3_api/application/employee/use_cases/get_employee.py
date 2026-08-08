"""Get-employee use case."""

from __future__ import annotations

import uuid

from organizeg3_api.core.exceptions import (
    NotFoundError,
)
from organizeg3_api.domain.employee.entity import (
    Employee,
)
from organizeg3_api.domain.employee.repository import (
    EmployeeRepository,
)


class GetEmployeeUseCase:
    """Retrieve one tenant-owned employee."""

    def __init__(
        self,
        repository: EmployeeRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        employee_id: uuid.UUID,
    ) -> Employee:
        """Return one employee."""

        employee = (
            self._repository.get_by_id_for_tenant(
                tenant_id=tenant_id,
                employee_id=employee_id,
            )
        )

        if employee is None:
            raise NotFoundError(
                "Funcionário não encontrado."
            )

        return employee
