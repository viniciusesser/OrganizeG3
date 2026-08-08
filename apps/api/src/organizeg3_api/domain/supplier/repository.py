"""Supplier repository contracts."""

from __future__ import annotations

from typing import Protocol
import uuid

from organizeg3_api.domain.supplier.entity import (
    Supplier,
)


class SupplierRepository(Protocol):
    """Define persistence operations for suppliers."""

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        supplier_id: uuid.UUID,
    ) -> Supplier | None:
        """Return one tenant-scoped supplier."""
        ...

    def get_by_document_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        document_number: str,
    ) -> Supplier | None:
        """Return one supplier by CPF or CNPJ."""
        ...

    def add(
        self,
        supplier: Supplier,
    ) -> Supplier:
        """Persist a new supplier."""
        ...
