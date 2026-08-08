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

    def get_by_code_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
    ) -> Brand | None:
        """Return one tenant-scoped brand by normalized code."""
        ...

    def get_by_name_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        name: str,
    ) -> Brand | None:
        """Return one tenant-scoped brand by normalized name."""
        ...

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Brand]:
        """List tenant-scoped brands."""
        ...

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_brand_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a normalized code already exists."""
        ...

    def exists_by_name(
        self,
        *,
        tenant_id: uuid.UUID,
        name: str,
        exclude_brand_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a normalized name already exists."""
        ...

    def add(
        self,
        brand: Brand,
    ) -> Brand:
        """Persist a new brand."""
        ...

    def save(
        self,
        brand: Brand,
    ) -> Brand:
        """Persist changes to an existing brand."""
        ...
