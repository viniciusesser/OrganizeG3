"""Supplier domain definitions."""

from organizeg3_api.domain.supplier.entity import (
    Supplier,
)
from organizeg3_api.domain.supplier.repository import (
    SupplierRepository,
)
from organizeg3_api.domain.supplier.value_objects import (
    SupplierCode,
    SupplierDocument,
    SupplierEmail,
    SupplierPhone,
    SupplierPostalCode,
    SupplierState,
)

__all__ = [
    "Supplier",
    "SupplierCode",
    "SupplierDocument",
    "SupplierEmail",
    "SupplierPhone",
    "SupplierPostalCode",
    "SupplierRepository",
    "SupplierState",
]
