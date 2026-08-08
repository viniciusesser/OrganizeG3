"""Machine repository contracts."""

from __future__ import annotations

from typing import Protocol
import uuid

from organizeg3_api.domain.machine.entity import (
    Machine,
)


class MachineRepository(Protocol):
    """Define persistence operations for machines."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        machine_id: uuid.UUID,
    ) -> Machine | None:
        """Return one tenant-scoped machine."""
        ...

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> Machine | None:
        """Return one tenant-scoped machine by code."""
        ...

    def add(
        self,
        machine: Machine,
    ) -> Machine:
        """Persist a new machine."""
        ...
