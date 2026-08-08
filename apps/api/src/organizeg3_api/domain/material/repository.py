"""Material repository contracts."""

from __future__ import annotations

from typing import Protocol
import uuid

from organizeg3_api.domain.material.entity import (
    Material,
)


class MaterialRepository(Protocol):
    """Define persistence operations for materials."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        material_id: uuid.UUID,
    ) -> Material | None:
        """Return one tenant-scoped material."""
        ...

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> Material | None:
        """Return one material by normalized code."""
        ...

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        category: str | None = None,
        brand_id: uuid.UUID | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Material]:
        """List tenant materials using optional filters."""
        ...

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_material_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a normalized code is already in use."""
        ...

    def add(
        self,
        material: Material,
    ) -> Material:
        """Persist a new material."""
        ...

    def save(
        self,
        material: Material,
    ) -> Material:
        """Persist changes to an existing material."""
        ...
