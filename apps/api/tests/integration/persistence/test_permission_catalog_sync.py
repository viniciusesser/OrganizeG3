"""Integration tests for the canonical permission catalog sync."""

from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from organizeg3_api.domain.identity.permissions import (
    PERMISSION_CATALOG,
    BranchPermissions,
    permission_codes,
)
from organizeg3_api.infrastructure.persistence.authorization import (
    sync_permission_catalog,
)
from organizeg3_api.infrastructure.persistence.models.authorization import (
    PermissionModel,
)


def test_creates_all_canonical_permissions(
    session: Session,
) -> None:
    """Create every missing canonical permission."""

    result = sync_permission_catalog(
        session
    )

    stored_codes = set(
        session.scalars(
            select(
                PermissionModel.code
            )
        ).all()
    )

    assert stored_codes == permission_codes()

    assert result.created == len(
        PERMISSION_CATALOG
    )
    assert result.updated == 0
    assert result.reactivated == 0
    assert result.unchanged == 0
    assert result.total == len(
        PERMISSION_CATALOG
    )


def test_sync_is_idempotent_and_preserves_ids(
    session: Session,
) -> None:
    """Repeated synchronization must preserve permission identities."""

    first_result = sync_permission_catalog(
        session
    )

    session.flush()

    first_ids = {
        permission.code: permission.id
        for permission in session.scalars(
            select(
                PermissionModel
            )
        ).all()
    }

    second_result = sync_permission_catalog(
        session
    )

    second_ids = {
        permission.code: permission.id
        for permission in session.scalars(
            select(
                PermissionModel
            )
        ).all()
    }

    assert first_result.created == len(
        PERMISSION_CATALOG
    )

    assert second_result.created == 0
    assert second_result.updated == 0
    assert second_result.reactivated == 0
    assert second_result.unchanged == len(
        PERMISSION_CATALOG
    )

    assert second_ids == first_ids


def test_repairs_canonical_metadata(
    session: Session,
) -> None:
    """Restore metadata that diverged from the canonical catalog."""

    sync_permission_catalog(
        session
    )

    permission = session.scalar(
        select(
            PermissionModel
        ).where(
            PermissionModel.code
            == BranchPermissions.READ
        )
    )

    assert permission is not None

    original_id = permission.id

    permission.name = "Nome incorreto"
    permission.module = "incorrect"
    permission.resource = "incorrect"
    permission.action = "incorrect"
    permission.description = "Descrição incorreta"

    session.flush()

    result = sync_permission_catalog(
        session
    )

    session.refresh(
        permission
    )

    assert permission.id == original_id
    assert permission.code == BranchPermissions.READ
    assert permission.name == "Visualizar filiais"
    assert permission.module == "branches"
    assert permission.resource == "branches"
    assert permission.action == "read"
    assert (
        permission.description
        == "Permite consultar filiais do tenant."
    )

    assert result.updated == 1


def test_reactivates_canonical_permission(
    session: Session,
) -> None:
    """Reactivate canonical permissions without changing their IDs."""

    sync_permission_catalog(
        session
    )

    permission = session.scalar(
        select(
            PermissionModel
        ).where(
            PermissionModel.code
            == BranchPermissions.CREATE
        )
    )

    assert permission is not None

    original_id = permission.id

    permission.is_active = False

    session.flush()

    result = sync_permission_catalog(
        session
    )

    session.refresh(
        permission
    )

    assert permission.id == original_id
    assert permission.is_active is True
    assert result.reactivated == 1


def test_does_not_remove_unknown_permissions(
    session: Session,
) -> None:
    """Preserve permissions outside the canonical catalog."""

    external_permission = PermissionModel(
        id=uuid.uuid4(),
        code="external.custom",
        name="External permission",
        module="external",
        resource="external",
        action="custom",
        description=None,
        is_active=True,
    )

    session.add(
        external_permission
    )

    session.flush()

    external_id = external_permission.id

    sync_permission_catalog(
        session
    )

    stored_external = session.scalar(
        select(
            PermissionModel
        ).where(
            PermissionModel.id
            == external_id
        )
    )

    assert stored_external is not None
    assert (
        stored_external.code
        == "external.custom"
    )


def test_matches_permission_codes_case_insensitively(
    session: Session,
) -> None:
    """Reuse existing permission rows with normalized equivalent codes."""

    permission = PermissionModel(
        id=uuid.uuid4(),
        code="  BRANCHES.READ  ",
        name="Legacy branch read",
        module="legacy",
        resource="legacy",
        action="legacy",
        description=None,
        is_active=True,
    )

    session.add(
        permission
    )

    session.flush()

    original_id = permission.id

    result = sync_permission_catalog(
        session
    )

    matching_permissions = session.scalars(
        select(
            PermissionModel
        ).where(
            func.lower(
                func.trim(
                    PermissionModel.code
                )
            )
            == BranchPermissions.READ
        )
    ).all()

    assert len(
        matching_permissions
    ) == 1

    stored_permission = (
        matching_permissions[0]
    )

    assert stored_permission.id == original_id
    assert (
        stored_permission.code
        == BranchPermissions.READ
    )
    assert result.updated >= 1
