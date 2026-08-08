"""Employee repository contracts."""

from __future__ import annotations

from typing import Protocol
import uuid

from organizeg3_api.domain.employee.entity import (
    Employee,
)
from organizeg3_api.domain.employee.value_objects import (
    EmploymentStatus,
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

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        branch_id: uuid.UUID | None = None,
        status: EmploymentStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Employee]:
        """List employees belonging to one tenant."""
        ...

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_employee_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether an employee code is already used."""
        ...

    def exists_by_document(
        self,
        *,
        tenant_id: uuid.UUID,
        document_number: str,
        exclude_employee_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether an employee CPF is already used."""
        ...

    def branch_exists_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID,
    ) -> bool:
        """Return whether the branch belongs to the tenant."""
        ...

    def add(
        self,
        employee: Employee,
    ) -> Employee:
        """Persist a new employee."""
        ...

    def save(
        self,
        employee: Employee,
    ) -> Employee:
        """Persist changes to an existing employee."""
        ...
