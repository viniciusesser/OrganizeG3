"""SQLAlchemy repository for tenant employees."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from organizeg3_api.domain.employee.entity import (
    Employee,
)
from organizeg3_api.domain.employee.repository import (
    EmployeeRepository,
)
from organizeg3_api.domain.employee.value_objects import (
    EmployeeCode,
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

        model = self._session.scalar(
            statement
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

        model = self._session.scalar(
            statement
        )

        if model is None:
            return None

        return self._to_domain(
            model
        )

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
        """List tenant employees using optional filters."""

        statement = select(
            EmployeeModel
        ).where(
            EmployeeModel.tenant_id
            == tenant_id
        )

        if not include_inactive:
            statement = statement.where(
                EmployeeModel.is_active.is_(
                    True
                )
            )

        if branch_id is not None:
            statement = statement.where(
                EmployeeModel.branch_id
                == branch_id
            )

        if status is not None:
            statement = statement.where(
                EmployeeModel.status
                == status.value
            )

        search_value = (
            search.strip()
            if search is not None
            else ""
        )

        if search_value:
            normalized_search = (
                search_value.lower()
            )

            text_pattern = (
                f"%{normalized_search}%"
            )

            document_pattern = (
                f"%{search_value}%"
            )

            statement = statement.where(
                or_(
                    func.lower(
                        EmployeeModel.code
                    ).like(
                        text_pattern
                    ),
                    func.lower(
                        EmployeeModel.full_name
                    ).like(
                        text_pattern
                    ),
                    func.lower(
                        EmployeeModel.email
                    ).like(
                        text_pattern
                    ),
                    EmployeeModel.document_number.like(
                        document_pattern
                    ),
                )
            )

        statement = (
            statement
            .order_by(
                EmployeeModel.full_name,
                EmployeeModel.code,
                EmployeeModel.id,
            )
            .limit(
                limit
            )
            .offset(
                offset
            )
        )

        models = self._session.scalars(
            statement
        ).all()

        return [
            self._to_domain(
                model
            )
            for model in models
        ]

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_employee_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a normalized employee code is used."""

        normalized_code = EmployeeCode(
            code
        ).value

        statement = select(
            EmployeeModel.id
        ).where(
            EmployeeModel.tenant_id
            == tenant_id,
            EmployeeModel.code
            == normalized_code,
        )

        if exclude_employee_id is not None:
            statement = statement.where(
                EmployeeModel.id
                != exclude_employee_id
            )

        return (
            self._session.scalar(
                statement.limit(1)
            )
            is not None
        )

    def exists_by_document(
        self,
        *,
        tenant_id: uuid.UUID,
        document_number: str,
        exclude_employee_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a normalized employee CPF is used."""

        normalized_document = EmployeeDocument(
            document_number
        ).value

        statement = select(
            EmployeeModel.id
        ).where(
            EmployeeModel.tenant_id
            == tenant_id,
            EmployeeModel.document_number
            == normalized_document,
        )

        if exclude_employee_id is not None:
            statement = statement.where(
                EmployeeModel.id
                != exclude_employee_id
            )

        return (
            self._session.scalar(
                statement.limit(1)
            )
            is not None
        )

    def branch_exists_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID,
    ) -> bool:
        """Return whether a branch belongs to the tenant."""

        statement = (
            select(
                BranchModel.id
            )
            .where(
                BranchModel.id
                == branch_id,
                BranchModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        return (
            self._session.scalar(
                statement
            )
            is not None
        )

    def add(
        self,
        employee: Employee,
    ) -> Employee:
        """Persist a new employee."""

        self._validate_branch_scope(
            employee
        )

        if employee.updated_at is None:
            raise ValueError(
                "Funcionário sem data de atualização "
                "não pode ser persistido."
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

    def save(
        self,
        employee: Employee,
    ) -> Employee:
        """Persist changes to an existing employee."""

        if employee.id is None:
            raise ValueError(
                "Funcionário sem identificador "
                "não pode ser atualizado."
            )

        if employee.updated_at is None:
            raise ValueError(
                "Funcionário sem data de atualização "
                "não pode ser atualizado."
            )

        self._validate_branch_scope(
            employee
        )

        statement = (
            select(
                EmployeeModel
            )
            .where(
                EmployeeModel.id
                == employee.id,
                EmployeeModel.tenant_id
                == employee.tenant_id,
            )
            .limit(1)
        )

        model = self._session.scalar(
            statement
        )

        if model is None:
            raise ValueError(
                "Funcionário não encontrado."
            )

        updated_at = employee.updated_at

        model.branch_id = employee.branch_id
        model.code = employee.code
        model.full_name = employee.full_name
        model.document_number = (
            employee.document_number
        )
        model.email = employee.email
        model.phone = employee.phone
        model.job_title = employee.job_title
        model.contract_type = (
            employee.contract_type
        )
        model.status = employee.status.value
        model.birth_date = employee.birth_date
        model.admission_date = (
            employee.admission_date
        )
        model.termination_date = (
            employee.termination_date
        )
        model.is_active = employee.is_active
        model.updated_at = updated_at

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

        if not self.branch_exists_for_tenant(
            tenant_id=employee.tenant_id,
            branch_id=employee.branch_id,
        ):
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
