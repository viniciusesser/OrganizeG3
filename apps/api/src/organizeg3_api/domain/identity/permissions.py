"""Canonical permission codes used by OrganizeG3 authorization."""

from __future__ import annotations


class CustomerPermissions:
    """Permission codes for customer operations."""

    READ = "customers.read"
    CREATE = "customers.create"
    UPDATE = "customers.update"
    ARCHIVE = "customers.archive"
    REACTIVATE = "customers.reactivate"


__all__ = [
    "CustomerPermissions",
]
