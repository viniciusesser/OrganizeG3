"""SQLAlchemy repositories for production core."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from organizeg3_api.domain.production.event import (
    ProductionEvent,
    ProductionEventType,
)
from organizeg3_api.domain.production.execution import (
    ProductionExecution,
)
from organizeg3_api.domain.production.operation import (
    ProductionOperation,
)
from organizeg3_api.domain.production.order import (
    ProductionOrder,
)
from organizeg3_api.domain.production.pause import (
    ProductionPause,
)
from organizeg3_api.domain.production.repository import (
    ProductionEventRepository,
    ProductionExecutionRepository,
    ProductionOperationRepository,
    ProductionOrderRepository,
    ProductionPauseRepository,
)
from organizeg3_api.domain.production.value_objects import (
    ProductionCode,
    ProductionExecutionStatus,
    ProductionOperationStatus,
    ProductionOrderStatus,
    ProductionPriority,
)
from organizeg3_api.infrastructure.persistence.models.branch import (
    BranchModel,
)
from organizeg3_api.infrastructure.persistence.models.employee import (
    EmployeeModel,
)
from organizeg3_api.infrastructure.persistence.models.machine import (
    MachineModel,
)
from organizeg3_api.infrastructure.persistence.models.production import (
    ProductionEventModel,
    ProductionExecutionModel,
    ProductionOperationModel,
    ProductionOrderModel,
    ProductionPauseModel,
)
from organizeg3_api.infrastructure.persistence.models.service import (
    ServiceModel,
)


class SQLAlchemyProductionOrderRepository(
    ProductionOrderRepository
):
    """Persist production orders."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        production_order_id: uuid.UUID,
    ) -> ProductionOrder | None:
        statement = (
            select(ProductionOrderModel)
            .where(
                ProductionOrderModel.id
                == production_order_id,
                ProductionOrderModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> ProductionOrder | None:
        normalized_code = ProductionCode(
            code
        ).value

        statement = (
            select(ProductionOrderModel)
            .where(
                ProductionOrderModel.tenant_id
                == tenant_id,
                ProductionOrderModel.code
                == normalized_code,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def add(
        self,
        order: ProductionOrder,
    ) -> ProductionOrder:
        self._validate_branch_scope(
            tenant_id=order.tenant_id,
            branch_id=order.branch_id,
        )

        model = ProductionOrderModel(
            id=order.id,
            tenant_id=order.tenant_id,
            branch_id=order.branch_id,
            code=order.code,
            title=order.title,
            status=order.status.value,
            priority=order.priority.value,
            planned_start_at=order.planned_start_at,
            planned_end_at=order.planned_end_at,
            is_active=order.is_active,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    def _validate_branch_scope(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID | None,
    ) -> None:
        if branch_id is None:
            return

        statement = (
            select(BranchModel.id)
            .where(
                BranchModel.id == branch_id,
                BranchModel.tenant_id == tenant_id,
            )
            .limit(1)
        )

        if (
            self._session.execute(statement)
            .scalar_one_or_none()
            is None
        ):
            raise ValueError(
                "A filial da ordem de produção "
                "não pertence ao tenant informado."
            )

    @staticmethod
    def _to_domain(
        model: ProductionOrderModel,
    ) -> ProductionOrder:
        return ProductionOrder(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            branch_id=model.branch_id,
            code=model.code,
            title=model.title,
            status=ProductionOrderStatus(
                model.status
            ),
            priority=ProductionPriority(
                model.priority
            ),
            planned_start_at=model.planned_start_at,
            planned_end_at=model.planned_end_at,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyProductionOperationRepository(
    ProductionOperationRepository
):
    """Persist production operations."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        operation_id: uuid.UUID,
    ) -> ProductionOperation | None:
        statement = (
            select(ProductionOperationModel)
            .where(
                ProductionOperationModel.id
                == operation_id,
                ProductionOperationModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def add(
        self,
        operation: ProductionOperation,
    ) -> ProductionOperation:
        self._validate_order_scope(
            operation
        )

        if operation.service_id is not None:
            self._validate_service_scope(
                operation
            )

        if operation.machine_id is not None:
            self._validate_machine_scope(
                operation
            )

        model = ProductionOperationModel(
            id=operation.id,
            tenant_id=operation.tenant_id,
            production_order_id=(
                operation.production_order_id
            ),
            sequence=operation.sequence,
            name=operation.name,
            service_id=operation.service_id,
            machine_id=operation.machine_id,
            status=operation.status.value,
            is_applicable=operation.is_applicable,
            created_at=operation.created_at,
            updated_at=operation.updated_at,
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    def _validate_order_scope(
        self,
        operation: ProductionOperation,
    ) -> None:
        statement = (
            select(ProductionOrderModel.id)
            .where(
                ProductionOrderModel.id
                == operation.production_order_id,
                ProductionOrderModel.tenant_id
                == operation.tenant_id,
            )
            .limit(1)
        )

        if (
            self._session.execute(statement)
            .scalar_one_or_none()
            is None
        ):
            raise ValueError(
                "A ordem de produção não pertence "
                "ao tenant informado."
            )

    def _validate_service_scope(
        self,
        operation: ProductionOperation,
    ) -> None:
        statement = (
            select(ServiceModel.id)
            .where(
                ServiceModel.id
                == operation.service_id,
                ServiceModel.tenant_id
                == operation.tenant_id,
            )
            .limit(1)
        )

        if (
            self._session.execute(statement)
            .scalar_one_or_none()
            is None
        ):
            raise ValueError(
                "O serviço da operação não pertence "
                "ao tenant informado."
            )

    def _validate_machine_scope(
        self,
        operation: ProductionOperation,
    ) -> None:
        statement = (
            select(MachineModel.id)
            .where(
                MachineModel.id
                == operation.machine_id,
                MachineModel.tenant_id
                == operation.tenant_id,
            )
            .limit(1)
        )

        if (
            self._session.execute(statement)
            .scalar_one_or_none()
            is None
        ):
            raise ValueError(
                "A máquina da operação não pertence "
                "ao tenant informado."
            )

    @staticmethod
    def _to_domain(
        model: ProductionOperationModel,
    ) -> ProductionOperation:
        return ProductionOperation(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            production_order_id=(
                model.production_order_id
            ),
            sequence=model.sequence,
            name=model.name,
            service_id=model.service_id,
            machine_id=model.machine_id,
            status=ProductionOperationStatus(
                model.status
            ),
            is_applicable=model.is_applicable,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyProductionExecutionRepository(
    ProductionExecutionRepository
):
    """Persist operation executions."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        execution_id: uuid.UUID,
    ) -> ProductionExecution | None:
        statement = (
            select(ProductionExecutionModel)
            .where(
                ProductionExecutionModel.id
                == execution_id,
                ProductionExecutionModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def add(
        self,
        execution: ProductionExecution,
    ) -> ProductionExecution:
        self._validate_operation_scope(
            execution
        )

        self._validate_employee_scope(
            execution
        )

        model = ProductionExecutionModel(
            id=execution.id,
            tenant_id=execution.tenant_id,
            operation_id=execution.operation_id,
            employee_id=execution.employee_id,
            status=execution.status.value,
            started_at=execution.started_at,
            finished_at=execution.finished_at,
            created_at=execution.created_at,
            updated_at=execution.updated_at,
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    def _validate_operation_scope(
        self,
        execution: ProductionExecution,
    ) -> None:
        statement = (
            select(ProductionOperationModel.id)
            .where(
                ProductionOperationModel.id
                == execution.operation_id,
                ProductionOperationModel.tenant_id
                == execution.tenant_id,
            )
            .limit(1)
        )

        if (
            self._session.execute(statement)
            .scalar_one_or_none()
            is None
        ):
            raise ValueError(
                "A operação da execução não pertence "
                "ao tenant informado."
            )

    def _validate_employee_scope(
        self,
        execution: ProductionExecution,
    ) -> None:
        statement = (
            select(EmployeeModel.id)
            .where(
                EmployeeModel.id
                == execution.employee_id,
                EmployeeModel.tenant_id
                == execution.tenant_id,
            )
            .limit(1)
        )

        if (
            self._session.execute(statement)
            .scalar_one_or_none()
            is None
        ):
            raise ValueError(
                "O funcionário da execução não pertence "
                "ao tenant informado."
            )

    @staticmethod
    def _to_domain(
        model: ProductionExecutionModel,
    ) -> ProductionExecution:
        return ProductionExecution(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            operation_id=model.operation_id,
            employee_id=model.employee_id,
            status=ProductionExecutionStatus(
                model.status
            ),
            started_at=model.started_at,
            finished_at=model.finished_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyProductionPauseRepository(
    ProductionPauseRepository
):
    """Persist measurable production pauses."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        pause_id: uuid.UUID,
    ) -> ProductionPause | None:
        statement = (
            select(ProductionPauseModel)
            .where(
                ProductionPauseModel.id
                == pause_id,
                ProductionPauseModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def add(
        self,
        pause: ProductionPause,
    ) -> ProductionPause:
        self._validate_execution_scope(
            pause
        )

        model = ProductionPauseModel(
            id=pause.id,
            tenant_id=pause.tenant_id,
            execution_id=pause.execution_id,
            reason_code=pause.reason_code,
            notes=pause.notes,
            started_at=pause.started_at,
            ended_at=pause.ended_at,
            created_at=pause.created_at,
            updated_at=pause.updated_at,
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    def _validate_execution_scope(
        self,
        pause: ProductionPause,
    ) -> None:
        statement = (
            select(ProductionExecutionModel.id)
            .where(
                ProductionExecutionModel.id
                == pause.execution_id,
                ProductionExecutionModel.tenant_id
                == pause.tenant_id,
            )
            .limit(1)
        )

        if (
            self._session.execute(statement)
            .scalar_one_or_none()
            is None
        ):
            raise ValueError(
                "A execução da pausa não pertence "
                "ao tenant informado."
            )

    @staticmethod
    def _to_domain(
        model: ProductionPauseModel,
    ) -> ProductionPause:
        return ProductionPause(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            execution_id=model.execution_id,
            reason_code=model.reason_code,
            notes=model.notes,
            started_at=model.started_at,
            ended_at=model.ended_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyProductionEventRepository(
    ProductionEventRepository
):
    """Persist operational production events."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        event_id: uuid.UUID,
    ) -> ProductionEvent | None:
        statement = (
            select(ProductionEventModel)
            .where(
                ProductionEventModel.id
                == event_id,
                ProductionEventModel.tenant_id
                == tenant_id,
            )
            .limit(1)
        )

        model = (
            self._session.execute(statement)
            .scalar_one_or_none()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def add(
        self,
        event: ProductionEvent,
    ) -> ProductionEvent:
        self._validate_order_scope(
            event
        )

        if event.operation_id is not None:
            self._validate_operation_scope(
                event
            )

        if event.execution_id is not None:
            self._validate_execution_scope(
                event
            )

        if event.employee_id is not None:
            self._validate_employee_scope(
                event
            )

        model = ProductionEventModel(
            id=event.id,
            tenant_id=event.tenant_id,
            production_order_id=(
                event.production_order_id
            ),
            operation_id=event.operation_id,
            execution_id=event.execution_id,
            employee_id=event.employee_id,
            event_type=event.event_type.value,
            reason_code=event.reason_code,
            notes=event.notes,
            occurred_at=event.occurred_at,
            created_at=event.created_at,
            updated_at=event.updated_at,
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    def _validate_order_scope(
        self,
        event: ProductionEvent,
    ) -> None:
        statement = (
            select(ProductionOrderModel.id)
            .where(
                ProductionOrderModel.id
                == event.production_order_id,
                ProductionOrderModel.tenant_id
                == event.tenant_id,
            )
            .limit(1)
        )

        if (
            self._session.execute(statement)
            .scalar_one_or_none()
            is None
        ):
            raise ValueError(
                "A ordem do evento não pertence "
                "ao tenant informado."
            )

    def _validate_operation_scope(
        self,
        event: ProductionEvent,
    ) -> None:
        statement = (
            select(ProductionOperationModel.id)
            .where(
                ProductionOperationModel.id
                == event.operation_id,
                ProductionOperationModel.production_order_id
                == event.production_order_id,
                ProductionOperationModel.tenant_id
                == event.tenant_id,
            )
            .limit(1)
        )

        if (
            self._session.execute(statement)
            .scalar_one_or_none()
            is None
        ):
            raise ValueError(
                "A operação do evento não pertence "
                "à ordem e ao tenant informados."
            )

    def _validate_execution_scope(
        self,
        event: ProductionEvent,
    ) -> None:
        statement = (
            select(ProductionExecutionModel.id)
            .where(
                ProductionExecutionModel.id
                == event.execution_id,
                ProductionExecutionModel.operation_id
                == event.operation_id,
                ProductionExecutionModel.tenant_id
                == event.tenant_id,
            )
            .limit(1)
        )

        if (
            self._session.execute(statement)
            .scalar_one_or_none()
            is None
        ):
            raise ValueError(
                "A execução do evento não pertence "
                "à operação e ao tenant informados."
            )

    def _validate_employee_scope(
        self,
        event: ProductionEvent,
    ) -> None:
        statement = (
            select(EmployeeModel.id)
            .where(
                EmployeeModel.id
                == event.employee_id,
                EmployeeModel.tenant_id
                == event.tenant_id,
            )
            .limit(1)
        )

        if (
            self._session.execute(statement)
            .scalar_one_or_none()
            is None
        ):
            raise ValueError(
                "O funcionário do evento não pertence "
                "ao tenant informado."
            )

    @staticmethod
    def _to_domain(
        model: ProductionEventModel,
    ) -> ProductionEvent:
        return ProductionEvent(
            id=model.id,
            tenant_id=cast(
                uuid.UUID,
                model.tenant_id,
            ),
            production_order_id=(
                model.production_order_id
            ),
            operation_id=model.operation_id,
            execution_id=model.execution_id,
            employee_id=model.employee_id,
            event_type=ProductionEventType(
                model.event_type
            ),
            reason_code=model.reason_code,
            notes=model.notes,
            occurred_at=model.occurred_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
