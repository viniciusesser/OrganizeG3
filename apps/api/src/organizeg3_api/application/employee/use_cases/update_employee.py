"""Update-employee use case."""

from __future__ import annotations

import uuid

from organizeg3_api.application.employee.schemas import (
    EmployeeUpdate,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.employee.entity import (
    Employee,
)
from organizeg3_api.domain.employee.repository import (
    EmployeeRepository,
)


class UpdateEmployeeUseCase:
    """Update employee details inside one tenant."""

    def __init__(
        self,
        repository: EmployeeRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        tenant_id: uuid.UUID,
        employee_id: uuid.UUID,
        payload: EmployeeUpdate,
    ) -> Employee:
        """Apply a partial employee update."""

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

        changed_fields = payload.model_fields_set

        if not changed_fields:
            raise ValidationError(
                "Informe ao menos um campo para atualizar."
            )

        if (
            "code" in changed_fields
            and payload.code is None
        ):
            raise ValidationError(
                "O código do funcionário não pode ser nulo."
            )

        if (
            "full_name" in changed_fields
            and payload.full_name is None
        ):
            raise ValidationError(
                "O nome do funcionário não pode ser nulo."
            )

        code = (
            payload.code
            if "code" in changed_fields
            else employee.code
        )

        full_name = (
            payload.full_name
            if "full_name" in changed_fields
            else employee.full_name
        )

        if code is None:
            raise ValidationError(
                "O código do funcionário não pode ser nulo."
            )

        if full_name is None:
            raise ValidationError(
                "O nome do funcionário não pode ser nulo."
            )

        branch_id = (
            payload.branch_id
            if "branch_id" in changed_fields
            else employee.branch_id
        )

        document_number = (
            payload.document_number
            if "document_number" in changed_fields
            else employee.document_number
        )

        email = (
            payload.email
            if "email" in changed_fields
            else employee.email
        )

        phone = (
            payload.phone
            if "phone" in changed_fields
            else employee.phone
        )

        job_title = (
            payload.job_title
            if "job_title" in changed_fields
            else employee.job_title
        )

        contract_type = (
            payload.contract_type
            if "contract_type" in changed_fields
            else employee.contract_type
        )

        birth_date = (
            payload.birth_date
            if "birth_date" in changed_fields
            else employee.birth_date
        )

        admission_date = (
            payload.admission_date
            if "admission_date" in changed_fields
            else employee.admission_date
        )

        if (
            branch_id is not None
            and not self._repository.branch_exists_for_tenant(
                tenant_id=tenant_id,
                branch_id=branch_id,
            )
        ):
            raise ValidationError(
                "A filial do funcionário não pertence "
                "ao tenant informado."
            )

        try:
            employee.update_details(
                code=code,
                full_name=full_name,
                branch_id=branch_id,
                document_number=document_number,
                email=email,
                phone=phone,
                job_title=job_title,
                contract_type=contract_type,
                birth_date=birth_date,
                admission_date=admission_date,
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
            exclude_employee_id=employee_id,
        ):
            raise ConflictError(
                "Já existe um funcionário com esse código."
            )

        if (
            employee.document_number is not None
            and self._repository.exists_by_document(
                tenant_id=tenant_id,
                document_number=employee.document_number,
                exclude_employee_id=employee_id,
            )
        ):
            raise ConflictError(
                "Já existe um funcionário com esse CPF."
            )

        return self._repository.save(
            employee
        )
