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

    def add(
        self,
        material: Material,
    ) -> Material:
        """Persist a new material."""
        ...
