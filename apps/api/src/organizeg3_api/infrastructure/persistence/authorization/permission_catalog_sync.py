"""Synchronize canonical permissions with persistent authorization data."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from organizeg3_api.domain.identity.permissions import (
    PERMISSION_CATALOG,
    PermissionDefinition,
)
from organizeg3_api.infrastructure.database.base import (
    utc_now,
)
from organizeg3_api.infrastructure.persistence.models.authorization import (
    PermissionModel,
)


@dataclass(frozen=True, slots=True)
class PermissionCatalogSyncResult:
    """Summarize one permission catalog synchronization."""

    created: int = 0
    updated: int = 0
    reactivated: int = 0
    unchanged: int = 0

    @property
    def total(self) -> int:
        """Return the number of canonical permissions processed."""

        return (
            self.created
            + self.updated
            + self.reactivated
            + self.unchanged
        )


def sync_permission_catalog(
    session: Session,
    *,
    catalog: tuple[
        PermissionDefinition,
        ...,
    ] = PERMISSION_CATALOG,
) -> PermissionCatalogSyncResult:
    """Synchronize canonical permissions idempotently."""

    created = 0
    updated = 0
    reactivated = 0
    unchanged = 0

    for definition in catalog:
        permission = _find_permission(
            session,
            definition.code,
        )

        if permission is None:
            session.add(
                PermissionModel(
                    code=definition.code,
                    name=definition.name,
                    module=definition.module,
                    resource=definition.resource,
                    action=definition.action,
                    description=definition.description,
                    is_active=True,
                )
            )
            created += 1
            continue

        fields_changed = _synchronize_fields(
            permission,
            definition,
        )

        was_reactivated = False

        if not permission.is_active:
            permission.is_active = True
            was_reactivated = True

        if fields_changed:
            permission.updated_at = utc_now()
            updated += 1
        elif was_reactivated:
            permission.updated_at = utc_now()
            reactivated += 1
        else:
            unchanged += 1

    session.flush()

    return PermissionCatalogSyncResult(
        created=created,
        updated=updated,
        reactivated=reactivated,
        unchanged=unchanged,
    )


def _find_permission(
    session: Session,
    code: str,
) -> PermissionModel | None:
    """Find a permission using the canonical normalized code."""

    normalized_code = code.strip().lower()

    statement = (
        select(
            PermissionModel
        )
        .where(
            func.lower(
                func.trim(
                    PermissionModel.code
                )
            )
            == normalized_code
        )
        .limit(1)
    )

    return session.scalar(
        statement
    )


def _synchronize_fields(
    permission: PermissionModel,
    definition: PermissionDefinition,
) -> bool:
    """Apply canonical metadata while preserving the permission identity."""

    changed = False

    canonical_fields: dict[
        str,
        str | None,
    ] = {
        "code": definition.code,
        "name": definition.name,
        "module": definition.module,
        "resource": definition.resource,
        "action": definition.action,
        "description": definition.description,
    }

    for field_name, canonical_value in canonical_fields.items():
        current_value = getattr(
            permission,
            field_name,
        )

        if current_value == canonical_value:
            continue

        setattr(
            permission,
            field_name,
            canonical_value,
        )

        changed = True

    return changed


__all__ = [
    "PermissionCatalogSyncResult",
    "sync_permission_catalog",
]
