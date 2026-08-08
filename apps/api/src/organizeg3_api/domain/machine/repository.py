"""Machine repository contracts."""

from __future__ import annotations

from typing import Protocol
import uuid

from organizeg3_api.domain.machine.entity import (
    Machine,
)
from organizeg3_api.domain.machine.value_objects import (
    MachineStatus,
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

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        machine_type: str | None = None,
        status: MachineStatus | None = None,
        branch_id: uuid.UUID | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Machine]:
        """List tenant-scoped machines with optional filters."""
        ...

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_machine_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a machine code already exists."""
        ...

    def add(
        self,
        machine: Machine,
    ) -> Machine:
        """Persist a new machine."""
        ...

    def save(
        self,
        machine: Machine,
    ) -> Machine:
        """Persist changes to an existing machine."""
        ...
