"""SQLAlchemy repository for tenant employees."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.employee.entity import (
    Employee,
)
from organizeg3_api.domain.employee.repository import (
    EmployeeRepository,
)
from organizeg3_api.domain.employee.value_objects import (
    EmployeeDocument,
    EmploymentStatus,
)
from organizeg3_api.infrastructure.persistence.models.branch import (
    BranchModel,
)
from organizeg3_api.infrastructure.persistence.models.employee import (
    EmployeeModel,
)


class SQLAlchemyEmployeeRepository(
    EmployeeRepository
):
    """Persist employee data using SQLAlchemy."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        employee_id: uuid.UUID,
    ) -> Employee | None:
        """Return one employee belonging to a tenant."""

        statement = (
            select(
                EmployeeModel
            )
            .where(
                EmployeeModel.id
                == employee_id,
                EmployeeModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(
                statement
            )
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(
            model
        )

    def get_by_document_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        document_number: str,
    ) -> Employee | None:
        """Return one employee by CPF within a tenant."""

        normalized_document = EmployeeDocument(
            document_number
        ).value

        statement = (
            select(
                EmployeeModel
            )
            .where(
                EmployeeModel.tenant_id
                == tenant_id,
                EmployeeModel.document_number
                == normalized_document,
            )
            .limit(1)
        )

        model = (
            self._session.execute(
                statement
            )
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(
            model
        )

    def add(
        self,
        employee: Employee,
    ) -> Employee:
        """Persist a new employee."""

        self._validate_branch_scope(
            employee
        )

        model = EmployeeModel(
            id=employee.id,
            tenant_id=employee.tenant_id,
            branch_id=employee.branch_id,
            code=employee.code,
            full_name=employee.full_name,
            document_number=(
                employee.document_number
            ),
            email=employee.email,
            phone=employee.phone,
            job_title=employee.job_title,
            contract_type=employee.contract_type,
            status=employee.status.value,
            birth_date=employee.birth_date,
            admission_date=employee.admission_date,
            termination_date=(
                employee.termination_date
            ),
            is_active=employee.is_active,
            created_at=employee.created_at,
            updated_at=employee.updated_at,
        )

        self._session.add(
            model
        )
        self._session.flush()

        return self._to_domain(
            model
        )

    def _validate_branch_scope(
        self,
        employee: Employee,
    ) -> None:
        """Ensure the selected branch belongs to the employee tenant."""

        if employee.branch_id is None:
            return

        statement = (
            select(
                BranchModel.id
            )
            .where(
                BranchModel.id
                == employee.branch_id,
                BranchModel.tenant_id
                == employee.tenant_id,
            )
            .limit(1)
        )

        branch_id = (
            self._session.execute(
                statement
            )
            .scalar_one_or_none()
        )

        if branch_id is None:
            raise ValueError(
                "A filial do funcionário não pertence "
                "ao tenant informado."
            )

    @staticmethod
    def _to_domain(
        model: EmployeeModel,
    ) -> Employee:
        """Convert persistence model to domain entity."""

        return Employee(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            branch_id=model.branch_id,
            code=model.code,
            full_name=model.full_name,
            document_number=model.document_number,
            email=model.email,
            phone=model.phone,
            job_title=model.job_title,
            contract_type=model.contract_type,
            status=EmploymentStatus(
                model.status
            ),
            birth_date=model.birth_date,
            admission_date=model.admission_date,
            termination_date=model.termination_date,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
