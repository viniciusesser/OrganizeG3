"""SQLAlchemy repository for local identity authorization."""

from __future__ import annotations

from typing import cast
import uuid

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from organizeg3_api.domain.identity.enums import (
    MembershipStatus,
    PermissionEffect,
)
from organizeg3_api.domain.identity.repository import (
    AccessibleTenant,
    IdentityAccess,
    IdentityRepository,
)
from organizeg3_api.infrastructure.persistence.models.authorization import (
    AccessProfileModel,
    AccessProfilePermissionModel,
    PermissionModel,
    TenantMembershipPermissionOverrideModel,
    TenantMembershipProfileModel,
)
from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.models.user import (
    TenantMembershipModel,
    UserModel,
)


class SqlAlchemyIdentityRepository(
    IdentityRepository,
):
    """Resolve local identity and effective permissions."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def list_accessible_tenants(
        self,
        *,
        auth_user_id: uuid.UUID,
    ) -> tuple[AccessibleTenant, ...]:
        """List active tenant memberships for one authenticated user."""

        statement = (
            select(
                TenantRecordModel.id.label(
                    "tenant_id"
                ),
                TenantRecordModel.name.label(
                    "tenant_name"
                ),
                TenantMembershipModel.id.label(
                    "membership_id"
                ),
            )
            .select_from(UserModel)
            .join(
                TenantMembershipModel,
                TenantMembershipModel.user_id
                == UserModel.id,
            )
            .join(
                TenantRecordModel,
                TenantRecordModel.id
                == TenantMembershipModel.tenant_id,
            )
            .where(
                UserModel.auth_user_id
                == auth_user_id,
                UserModel.is_active.is_(
                    True
                ),
                UserModel.deleted_at.is_(
                    None
                ),
                TenantMembershipModel.status
                == MembershipStatus.ACTIVE.value,
                TenantRecordModel.is_active.is_(
                    True
                ),
            )
            .order_by(
                TenantRecordModel.name.asc(),
                TenantRecordModel.id.asc(),
            )
        )

        rows = self._session.execute(
            statement
        ).all()

        return tuple(
            AccessibleTenant(
                tenant_id=cast(
                    uuid.UUID,
                    row.tenant_id,
                ),
                membership_id=cast(
                    uuid.UUID,
                    row.membership_id,
                ),
                name=cast(
                    str,
                    row.tenant_name,
                ),
            )
            for row in rows
        )

    def resolve_active_access(
        self,
        *,
        auth_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> IdentityAccess | None:
        """Resolve active user membership and permissions."""

        identity_statement = (
            select(
                UserModel.id.label(
                    "user_id"
                ),
                UserModel.auth_user_id.label(
                    "auth_user_id"
                ),
                UserModel.email.label(
                    "email"
                ),
                UserModel.display_name.label(
                    "display_name"
                ),
                TenantMembershipModel.id.label(
                    "membership_id"
                ),
            )
            .select_from(UserModel)
            .join(
                TenantMembershipModel,
                TenantMembershipModel.user_id
                == UserModel.id,
            )
            .where(
                UserModel.auth_user_id
                == auth_user_id,
                UserModel.is_active.is_(
                    True
                ),
                UserModel.deleted_at.is_(
                    None
                ),
                TenantMembershipModel.tenant_id
                == tenant_id,
                TenantMembershipModel.status
                == MembershipStatus.ACTIVE.value,
            )
        )

        identity_row = (
            self._session
            .execute(identity_statement)
            .one_or_none()
        )

        if identity_row is None:
            return None

        user_id = cast(
            uuid.UUID,
            identity_row.user_id,
        )

        membership_id = cast(
            uuid.UUID,
            identity_row.membership_id,
        )

        profile_permission_codes = (
            self._load_profile_permissions(
                tenant_id=tenant_id,
                membership_id=membership_id,
            )
        )

        (
            explicitly_allowed,
            explicitly_denied,
        ) = self._load_permission_overrides(
            tenant_id=tenant_id,
            membership_id=membership_id,
        )

        effective_permissions = (
            profile_permission_codes
            | explicitly_allowed
        ) - explicitly_denied

        return IdentityAccess(
            user_id=user_id,
            membership_id=membership_id,
            auth_user_id=cast(
                uuid.UUID,
                identity_row.auth_user_id,
            ),
            email=cast(
                str,
                identity_row.email,
            ),
            display_name=cast(
                str,
                identity_row.display_name,
            ),
            permission_codes=frozenset(
                effective_permissions
            ),
        )

    def _load_profile_permissions(
        self,
        *,
        tenant_id: uuid.UUID,
        membership_id: uuid.UUID,
    ) -> set[str]:
        statement = (
            select(
                PermissionModel.code
            )
            .select_from(
                TenantMembershipProfileModel
            )
            .join(
                AccessProfileModel,
                and_(
                    AccessProfileModel.id
                    == TenantMembershipProfileModel.access_profile_id,
                    AccessProfileModel.tenant_id
                    == TenantMembershipProfileModel.tenant_id,
                ),
            )
            .join(
                AccessProfilePermissionModel,
                AccessProfilePermissionModel.access_profile_id
                == AccessProfileModel.id,
            )
            .join(
                PermissionModel,
                PermissionModel.id
                == AccessProfilePermissionModel.permission_id,
            )
            .where(
                TenantMembershipProfileModel.tenant_id
                == tenant_id,
                TenantMembershipProfileModel.membership_id
                == membership_id,
                AccessProfileModel.is_active.is_(
                    True
                ),
                AccessProfileModel.deleted_at.is_(
                    None
                ),
                PermissionModel.is_active.is_(
                    True
                ),
            )
        )

        return set(
            self._session.scalars(
                statement
            ).all()
        )

    def _load_permission_overrides(
        self,
        *,
        tenant_id: uuid.UUID,
        membership_id: uuid.UUID,
    ) -> tuple[
        set[str],
        set[str],
    ]:
        statement = (
            select(
                PermissionModel.code,
                TenantMembershipPermissionOverrideModel.effect,
            )
            .select_from(
                TenantMembershipPermissionOverrideModel
            )
            .join(
                PermissionModel,
                PermissionModel.id
                == TenantMembershipPermissionOverrideModel.permission_id,
            )
            .where(
                TenantMembershipPermissionOverrideModel.tenant_id
                == tenant_id,
                TenantMembershipPermissionOverrideModel.membership_id
                == membership_id,
                PermissionModel.is_active.is_(
                    True
                ),
            )
        )

        allowed: set[str] = set()
        denied: set[str] = set()

        for permission_code, effect in (
            self._session.execute(
                statement
            )
        ):
            if (
                effect
                == PermissionEffect.DENY.value
            ):
                denied.add(
                    permission_code
                )
                continue

            if (
                effect
                == PermissionEffect.ALLOW.value
            ):
                allowed.add(
                    permission_code
                )

        return allowed, denied

