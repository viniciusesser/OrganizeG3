"""Brand repository contracts."""

from __future__ import annotations

from typing import Protocol
import uuid

from organizeg3_api.domain.brand.entity import (
    Brand,
)


class BrandRepository(Protocol):
    """Define persistence operations for brands."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        brand_id: uuid.UUID,
    ) -> Brand | None:
        """Return one tenant-scoped brand."""
        ...

    def get_by_name_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        name: str,
    ) -> Brand | None:
        """Return one tenant-scoped brand by name."""
        ...

    def add(
        self,
        brand: Brand,
    ) -> Brand:
        """Persist a new brand."""
        ...
