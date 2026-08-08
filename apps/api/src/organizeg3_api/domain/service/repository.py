"""Service repository contracts."""

from __future__ import annotations

from typing import Protocol
import uuid

from organizeg3_api.domain.service.entity import (
    Service,
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

    def add(
        self,
        service: Service,
    ) -> Service:
        """Persist a new service."""
        ...
