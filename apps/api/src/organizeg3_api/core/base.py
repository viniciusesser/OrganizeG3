"""Compatibility exports for the canonical SQLAlchemy base.

Persistence primitives live in :mod:`organizeg3_api.infrastructure.database.base`.
This module remains only to preserve imports created before the consolidation.
"""

from organizeg3_api.infrastructure.database.base import (
    NAMING_CONVENTION,
    ActiveStatusMixin,
    ActorAuditMixin,
    ArchivableMixin,
    Base,
    CodeMixin,
    OptimisticLockMixin,
    SoftDeleteMixin,
    TenantModel,
    TenantScopedMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    metadata,
    utc_now,
)

__all__ = [
    "NAMING_CONVENTION",
    "ActiveStatusMixin",
    "ActorAuditMixin",
    "ArchivableMixin",
    "Base",
    "CodeMixin",
    "OptimisticLockMixin",
    "SoftDeleteMixin",
    "TenantModel",
    "TenantScopedMixin",
    "TimestampMixin",
    "UUIDPrimaryKeyMixin",
    "metadata",
    "utc_now",
]
