"""Production repository contracts."""

from __future__ import annotations

from typing import Protocol
import uuid

from organizeg3_api.domain.production.assignment import (
    ProductionAssignment,
)
from organizeg3_api.domain.production.checklist import (
    ProductionChecklistItem,
)
from organizeg3_api.domain.production.event import (
    ProductionEvent,
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


class ProductionOrderRepository(Protocol):
    """Persistence contract for production orders."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        production_order_id: uuid.UUID,
    ) -> ProductionOrder | None:
        ...

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> ProductionOrder | None:
        ...

    def add(
        self,
        order: ProductionOrder,
    ) -> ProductionOrder:
        ...


class ProductionOperationRepository(Protocol):
    """Persistence contract for production operations."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        operation_id: uuid.UUID,
    ) -> ProductionOperation | None:
        ...

    def add(
        self,
        operation: ProductionOperation,
    ) -> ProductionOperation:
        ...


class ProductionAssignmentRepository(Protocol):
    """Persistence contract for operation employee assignments."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        assignment_id: uuid.UUID,
    ) -> ProductionAssignment | None:
        ...

    def list_by_operation_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        production_operation_id: uuid.UUID,
        active_only: bool = False,
    ) -> list[ProductionAssignment]:
        ...

    def add(
        self,
        assignment: ProductionAssignment,
    ) -> ProductionAssignment:
        ...

    def save(
        self,
        assignment: ProductionAssignment,
    ) -> ProductionAssignment:
        ...


class ProductionChecklistItemRepository(Protocol):
    """Persistence contract for production operation checklist items."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        checklist_item_id: uuid.UUID,
    ) -> ProductionChecklistItem | None:
        ...

    def list_by_operation_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        production_operation_id: uuid.UUID,
    ) -> list[ProductionChecklistItem]:
        ...

    def add(
        self,
        item: ProductionChecklistItem,
    ) -> ProductionChecklistItem:
        ...

    def save(
        self,
        item: ProductionChecklistItem,
    ) -> ProductionChecklistItem:
        ...


class ProductionExecutionRepository(Protocol):
    """Persistence contract for operation executions."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        execution_id: uuid.UUID,
    ) -> ProductionExecution | None:
        ...

    def add(
        self,
        execution: ProductionExecution,
    ) -> ProductionExecution:
        ...


class ProductionPauseRepository(Protocol):
    """Persistence contract for measurable execution pauses."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        pause_id: uuid.UUID,
    ) -> ProductionPause | None:
        ...

    def add(
        self,
        pause: ProductionPause,
    ) -> ProductionPause:
        ...


class ProductionEventRepository(Protocol):
    """Persistence contract for production operational events."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        event_id: uuid.UUID,
    ) -> ProductionEvent | None:
        ...

    def add(
        self,
        event: ProductionEvent,
    ) -> ProductionEvent:
        ...
