"""Employee domain definitions."""

from organizeg3_api.domain.employee.entity import (
    Employee,
)
from organizeg3_api.domain.employee.repository import (
    EmployeeRepository,
)
from organizeg3_api.domain.employee.value_objects import (
    EmployeeCode,
    EmployeeDocument,
    EmployeeEmail,
    EmployeePhone,
    EmploymentStatus,
)

__all__ = [
    "Employee",
    "EmployeeCode",
    "EmployeeDocument",
    "EmployeeEmail",
    "EmployeePhone",
    "EmployeeRepository",
    "EmploymentStatus",
]
