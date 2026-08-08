"""Repositories for production assignments and checklist items."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import cast
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.production.assignment import (
    ProductionAssignment,
)
from organizeg3_api.domain.production.checklist import (
    ProductionChecklistItem,
)
from organizeg3_api.domain.production.repository import (
    ProductionAssignmentRepository,
    ProductionChecklistItemRepository,
)
from organizeg3_api.infrastructure.persistence.models.employee import (
    EmployeeModel,
)
from organizeg3_api.infrastructure.persistence.models.production import (
    ProductionOperationModel,
)
from organizeg3_api.infrastructure.persistence.models.production_controls import (
    ProductionAssignmentModel,
    ProductionChecklistItemModel,
)
from organizeg3_api.infrastructure.persistence.models.user import (
    UserModel,
)


def _as_utc(
    value: datetime,
) -> datetime:
    """Restore UTC information lost by SQLite datetime storage."""

    if value.tzinfo is None:
        return value.replace(
            tzinfo=UTC
        )

    return value.astimezone(
        UTC
    )


def _optional_as_utc(
    value: datetime | None,
) -> datetime | None:
    """Restore UTC for an optional persisted datetime."""

    if value is None:
        return None

    return _as_utc(
        value
    )

def _require_operation(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    production_operation_id: uuid.UUID,
) -> ProductionOperationModel:
    model = session.scalar(
        select(
            ProductionOperationModel
        ).where(
            ProductionOperationModel.id
            == production_operation_id,
            ProductionOperationModel.tenant_id
            == tenant_id,
        )
    )

    if model is None:
        raise ValueError(
            "A operação de produção não pertence ao tenant."
        )

    return model


def _require_employee(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    employee_id: uuid.UUID,
) -> EmployeeModel:
    model = session.scalar(
        select(
            EmployeeModel
        ).where(
            EmployeeModel.id == employee_id,
            EmployeeModel.tenant_id == tenant_id,
        )
    )

    if model is None:
        raise ValueError(
            "O funcionário não pertence ao tenant."
        )

    return model


def _require_user(
    session: Session,
    *,
    user_id: uuid.UUID,
) -> UserModel:
    model = session.scalar(
        select(
            UserModel
        ).where(
            UserModel.id == user_id
        )
    )

    if model is None:
        raise ValueError(
            "O usuário responsável pela atribuição "
            "não foi encontrado."
        )

    return model


def _assignment_to_domain(
    model: ProductionAssignmentModel,
) -> ProductionAssignment:
    return ProductionAssignment(
        id=model.id,
        tenant_id=cast(
            uuid.UUID,
            model.tenant_id,
        ),
        production_operation_id=(
            model.production_operation_id
        ),
        employee_id=model.employee_id,
        assigned_at=_as_utc(
            model.assigned_at
        ),
        assigned_by_user_id=(
            model.assigned_by_user_id
        ),
        unassigned_at=_optional_as_utc(
            model.unassigned_at
        ),
        is_active=model.is_active,
        created_at=_optional_as_utc(
            model.created_at
        ),
        updated_at=_optional_as_utc(
            model.updated_at
        ),
    )


def _checklist_to_domain(
    model: ProductionChecklistItemModel,
) -> ProductionChecklistItem:
    return ProductionChecklistItem(
        id=model.id,
        tenant_id=cast(
            uuid.UUID,
            model.tenant_id,
        ),
        production_operation_id=(
            model.production_operation_id
        ),
        sequence=model.sequence,
        title=model.title,
        is_required=model.is_required,
        is_applicable=model.is_applicable,
        completed_at=_optional_as_utc(
            model.completed_at
        ),
        completed_by_employee_id=(
            model.completed_by_employee_id
        ),
        notes=model.notes,
        created_at=_optional_as_utc(
            model.created_at
        ),
        updated_at=_optional_as_utc(
            model.updated_at
        ),
    )


class SQLAlchemyProductionAssignmentRepository(
    ProductionAssignmentRepository
):
    """Persist production employee assignments."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        assignment_id: uuid.UUID,
    ) -> ProductionAssignment | None:
        model = self._session.scalar(
            select(
                ProductionAssignmentModel
            ).where(
                ProductionAssignmentModel.id
                == assignment_id,
                ProductionAssignmentModel.tenant_id
                == tenant_id,
            )
        )

        if model is None:
            return None

        return _assignment_to_domain(
            model
        )

    def list_by_operation_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        production_operation_id: uuid.UUID,
        active_only: bool = False,
    ) -> list[ProductionAssignment]:
        statement = (
            select(
                ProductionAssignmentModel
            )
            .where(
                ProductionAssignmentModel.tenant_id
                == tenant_id,
                ProductionAssignmentModel.production_operation_id
                == production_operation_id,
            )
            .order_by(
                ProductionAssignmentModel.assigned_at,
                ProductionAssignmentModel.id,
            )
        )

        if active_only:
            statement = statement.where(
                ProductionAssignmentModel.is_active.is_(
                    True
                )
            )

        models = self._session.scalars(
            statement
        ).all()

        return [
            _assignment_to_domain(model)
            for model in models
        ]

    def add(
        self,
        assignment: ProductionAssignment,
    ) -> ProductionAssignment:
        _require_operation(
            self._session,
            tenant_id=assignment.tenant_id,
            production_operation_id=(
                assignment.production_operation_id
            ),
        )

        _require_employee(
            self._session,
            tenant_id=assignment.tenant_id,
            employee_id=assignment.employee_id,
        )

        if assignment.assigned_by_user_id is not None:
            _require_user(
                self._session,
                user_id=assignment.assigned_by_user_id,
            )

        if assignment.is_active:
            duplicate = self._session.scalar(
                select(
                    ProductionAssignmentModel.id
                ).where(
                    ProductionAssignmentModel.tenant_id
                    == assignment.tenant_id,
                    ProductionAssignmentModel.production_operation_id
                    == assignment.production_operation_id,
                    ProductionAssignmentModel.employee_id
                    == assignment.employee_id,
                    ProductionAssignmentModel.is_active.is_(
                        True
                    ),
                )
            )

            if duplicate is not None:
                raise ValueError(
                    "O funcionário já possui uma atribuição "
                    "ativa para esta operação."
                )

        model = ProductionAssignmentModel(
            id=assignment.id,
            tenant_id=assignment.tenant_id,
            production_operation_id=(
                assignment.production_operation_id
            ),
            employee_id=assignment.employee_id,
            assigned_at=assignment.assigned_at,
            assigned_by_user_id=(
                assignment.assigned_by_user_id
            ),
            unassigned_at=assignment.unassigned_at,
            is_active=assignment.is_active,
            created_at=assignment.created_at,
            updated_at=assignment.updated_at,
        )

        self._session.add(
            model
        )
        self._session.flush()
        self._session.refresh(
            model
        )

        return _assignment_to_domain(
            model
        )

    def save(
        self,
        assignment: ProductionAssignment,
    ) -> ProductionAssignment:
        if assignment.id is None:
            raise ValueError(
                "A atribuição deve possuir identificador."
            )

        model = self._session.scalar(
            select(
                ProductionAssignmentModel
            ).where(
                ProductionAssignmentModel.id
                == assignment.id,
                ProductionAssignmentModel.tenant_id
                == assignment.tenant_id,
            )
        )

        if model is None:
            raise ValueError(
                "A atribuição não foi encontrada no tenant."
            )

        model.unassigned_at = assignment.unassigned_at
        model.is_active = assignment.is_active

        if assignment.updated_at is not None:
            model.updated_at = assignment.updated_at

        self._session.flush()
        self._session.refresh(
            model
        )

        return _assignment_to_domain(
            model
        )


class SQLAlchemyProductionChecklistItemRepository(
    ProductionChecklistItemRepository
):
    """Persist production operation checklist items."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        checklist_item_id: uuid.UUID,
    ) -> ProductionChecklistItem | None:
        model = self._session.scalar(
            select(
                ProductionChecklistItemModel
            ).where(
                ProductionChecklistItemModel.id
                == checklist_item_id,
                ProductionChecklistItemModel.tenant_id
                == tenant_id,
            )
        )

        if model is None:
            return None

        return _checklist_to_domain(
            model
        )

    def list_by_operation_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        production_operation_id: uuid.UUID,
    ) -> list[ProductionChecklistItem]:
        models = self._session.scalars(
            select(
                ProductionChecklistItemModel
            )
            .where(
                ProductionChecklistItemModel.tenant_id
                == tenant_id,
                ProductionChecklistItemModel.production_operation_id
                == production_operation_id,
            )
            .order_by(
                ProductionChecklistItemModel.sequence,
                ProductionChecklistItemModel.id,
            )
        ).all()

        return [
            _checklist_to_domain(model)
            for model in models
        ]

    def add(
        self,
        item: ProductionChecklistItem,
    ) -> ProductionChecklistItem:
        _require_operation(
            self._session,
            tenant_id=item.tenant_id,
            production_operation_id=(
                item.production_operation_id
            ),
        )

        if item.completed_by_employee_id is not None:
            _require_employee(
                self._session,
                tenant_id=item.tenant_id,
                employee_id=(
                    item.completed_by_employee_id
                ),
            )

        model = ProductionChecklistItemModel(
            id=item.id,
            tenant_id=item.tenant_id,
            production_operation_id=(
                item.production_operation_id
            ),
            sequence=item.sequence,
            title=item.title,
            is_required=item.is_required,
            is_applicable=item.is_applicable,
            completed_at=item.completed_at,
            completed_by_employee_id=(
                item.completed_by_employee_id
            ),
            notes=item.notes,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )

        self._session.add(
            model
        )
        self._session.flush()
        self._session.refresh(
            model
        )

        return _checklist_to_domain(
            model
        )

    def save(
        self,
        item: ProductionChecklistItem,
    ) -> ProductionChecklistItem:
        if item.id is None:
            raise ValueError(
                "O item de checklist deve possuir identificador."
            )

        model = self._session.scalar(
            select(
                ProductionChecklistItemModel
            ).where(
                ProductionChecklistItemModel.id
                == item.id,
                ProductionChecklistItemModel.tenant_id
                == item.tenant_id,
            )
        )

        if model is None:
            raise ValueError(
                "O item de checklist não foi encontrado no tenant."
            )

        if item.completed_by_employee_id is not None:
            _require_employee(
                self._session,
                tenant_id=item.tenant_id,
                employee_id=(
                    item.completed_by_employee_id
                ),
            )

        model.sequence = item.sequence
        model.title = item.title
        model.is_required = item.is_required
        model.is_applicable = item.is_applicable
        model.completed_at = item.completed_at
        model.completed_by_employee_id = (
            item.completed_by_employee_id
        )
        model.notes = item.notes
        if item.updated_at is not None:
            model.updated_at = item.updated_at

        self._session.flush()
        self._session.refresh(
            model
        )

        return _checklist_to_domain(
            model
        )
