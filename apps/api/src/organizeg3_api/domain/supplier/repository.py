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

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Supplier]:
        """List tenant suppliers using optional filters."""
        ...

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_supplier_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether the normalized code is already used."""
        ...

    def exists_by_document(
        self,
        *,
        tenant_id: uuid.UUID,
        document_number: str,
        exclude_supplier_id: uuid.UUID | None = None,
    ) -> bool:
        """Return whether a document is already used."""
        ...

    def add(
        self,
        supplier: Supplier,
    ) -> Supplier:
        """Persist a new supplier."""
        ...

    def save(
        self,
        supplier: Supplier,
    ) -> Supplier:
        """Persist changes to an existing supplier."""
        ...
