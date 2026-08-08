"""Employee repository contracts."""

from __future__ import annotations

from typing import Protocol
import uuid

from organizeg3_api.domain.employee.entity import (
    Employee,
)


class EmployeeRepository(Protocol):
    """Define persistence operations for employees."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        employee_id: uuid.UUID,
    ) -> Employee | None:
        """Return one employee scoped to a tenant."""
        ...

    def get_by_document_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        document_number: str,
    ) -> Employee | None:
        """Return one employee by CPF within a tenant."""
        ...

    def add(
        self,
        employee: Employee,
    ) -> Employee:
        """Persist a new employee."""
        ...
