"""Authorization persistence services."""

from organizeg3_api.infrastructure.persistence.authorization.permission_catalog_sync import (
    PermissionCatalogSyncResult,
    sync_permission_catalog,
)

__all__ = [
    "PermissionCatalogSyncResult",
    "sync_permission_catalog",
]
