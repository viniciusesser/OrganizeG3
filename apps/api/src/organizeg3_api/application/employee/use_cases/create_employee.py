"""Create-employee use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.employee.schemas import (
    EmployeeCreate,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    ValidationError,
)
from organizeg3_api.domain.employee.entity import (
    Employee,
)
from organizeg3_api.domain.employee.repository import (
    EmployeeRepository,
)


class CreateEmployeeUseCase:
    """Create an employee inside one tenant."""

    def __init__(
        self,
        repository: EmployeeRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        payload: EmployeeCreate,
    ) -> Employee:
        """Create a tenant-owned employee."""

        try:
            employee = Employee.create(
                tenant_id=tenant_id,
                code=payload.code,
                full_name=payload.full_name,
                branch_id=payload.branch_id,
                document_number=(
                    payload.document_number
                ),
                email=payload.email,
                phone=payload.phone,
                job_title=payload.job_title,
                contract_type=payload.contract_type,
                birth_date=payload.birth_date,
                admission_date=payload.admission_date,
            )
        except (
            TypeError,
            ValueError,
        ) as exception:
            raise ValidationError(
                str(exception)
            ) from exception

        if self._repository.exists_by_code(
            tenant_id=tenant_id,
            code=employee.code,
        ):
            raise ConflictError(
                "Já existe um funcionário com esse código."
            )

        if (
            employee.document_number is not None
            and self._repository.exists_by_document(
                tenant_id=tenant_id,
                document_number=employee.document_number,
            )
        ):
            raise ConflictError(
                "Já existe um funcionário com esse CPF."
            )

        if (
            employee.branch_id is not None
            and not self._repository.branch_exists_for_tenant(
                tenant_id=tenant_id,
                branch_id=employee.branch_id,
            )
        ):
            raise ValidationError(
                "A filial do funcionário não pertence "
                "ao tenant informado."
            )

        return self._repository.add(
            employee
        )
