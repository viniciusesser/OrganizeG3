"""Service repository contracts."""

from __future__ import annotations

from typing import Protocol
import uuid

from organizeg3_api.domain.service.entity import (
    Service,
)
from organizeg3_api.domain.service.value_objects import (
    ServiceExecutionMode,
)


class ServiceRepository(Protocol):
    """Define persistence operations for services."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        service_id: uuid.UUID,
    ) -> Service | None:
        """Return one tenant-scoped service."""
        ...

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> Service | None:
        """Return one tenant-scoped service by code."""
        ...

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        category: str | None = None,
        execution_mode: ServiceExecutionMode | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Service]:
        """List tenant-scoped services."""
        ...

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_service_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a normalized code already exists."""
        ...

    def add(
        self,
        service: Service,
    ) -> Service:
        """Persist a new service."""
        ...

    def save(
        self,
        service: Service,
    ) -> Service:
        """Persist changes to an existing service."""
        ...
