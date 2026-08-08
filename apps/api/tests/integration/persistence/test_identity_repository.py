"""Integration tests for identity authorization resolution."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from organizeg3_api.domain.identity.enums import (
    MembershipStatus,
    PermissionEffect,
)
from organizeg3_api.infrastructure.persistence.models import (
    AccessProfileModel,
    AccessProfilePermissionModel,
    PermissionModel,
    TenantMembershipModel,
    TenantMembershipPermissionOverrideModel,
    TenantMembershipProfileModel,
    TenantModel,
    UserModel,
)
from organizeg3_api.infrastructure.persistence.repositories.identity_repository import (
    SqlAlchemyIdentityRepository,
)


def test_resolves_effective_permissions(
    session: Session,
) -> None:
    tenant = TenantModel(
        id=uuid.uuid4(),
        name="Empresa Autorização",
        status="ACTIVE",
        is_active=True,
    )

    user = UserModel(
        id=uuid.uuid4(),
        auth_user_id=uuid.uuid4(),
        email="admin@example.com",
        display_name="Administrador",
        is_active=True,
    )

    session.add_all(
        [
            tenant,
            user,
        ]
    )
    session.flush()

    membership = TenantMembershipModel(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        user_id=user.id,
        status=MembershipStatus.ACTIVE.value,
    )

    profile = AccessProfileModel(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        code="ADMINISTRATOR",
        name="Administrador",
        is_system=True,
        is_active=True,
    )

    read_permission = PermissionModel(
        id=uuid.uuid4(),
        code="customers.read",
        name="Consultar clientes",
        module="customers",
        resource="customer",
        action="read",
        is_active=True,
    )

    update_permission = PermissionModel(
        id=uuid.uuid4(),
        code="customers.update",
        name="Alterar clientes",
        module="customers",
        resource="customer",
        action="update",
        is_active=True,
    )

    archive_permission = PermissionModel(
        id=uuid.uuid4(),
        code="customers.archive",
        name="Arquivar clientes",
        module="customers",
        resource="customer",
        action="archive",
        is_active=True,
    )

    session.add_all(
        [
            membership,
            profile,
            read_permission,
            update_permission,
            archive_permission,
        ]
    )
    session.flush()

    session.add_all(
        [
            TenantMembershipProfileModel(
                tenant_id=tenant.id,
                membership_id=membership.id,
                access_profile_id=profile.id,
            ),
            AccessProfilePermissionModel(
                access_profile_id=profile.id,
                permission_id=read_permission.id,
            ),
            AccessProfilePermissionModel(
                access_profile_id=profile.id,
                permission_id=update_permission.id,
            ),
            TenantMembershipPermissionOverrideModel(
                tenant_id=tenant.id,
                membership_id=membership.id,
                permission_id=archive_permission.id,
                effect=PermissionEffect.ALLOW.value,
            ),
            TenantMembershipPermissionOverrideModel(
                tenant_id=tenant.id,
                membership_id=membership.id,
                permission_id=update_permission.id,
                effect=PermissionEffect.DENY.value,
            ),
        ]
    )
    session.flush()

    repository = SqlAlchemyIdentityRepository(
        session
    )

    access = repository.resolve_active_access(
        auth_user_id=user.auth_user_id,
        tenant_id=tenant.id,
    )

    assert access is not None

    assert access.permission_codes == frozenset(
        {
            "customers.read",
            "customers.archive",
        }
    )


def test_rejects_suspended_membership(
    session: Session,
) -> None:
    tenant = TenantModel(
        id=uuid.uuid4(),
        name="Empresa Suspensa",
        status="ACTIVE",
        is_active=True,
    )

    user = UserModel(
        id=uuid.uuid4(),
        auth_user_id=uuid.uuid4(),
        email="suspended@example.com",
        display_name="Usuário Suspenso",
        is_active=True,
    )

    session.add_all(
        [
            tenant,
            user,
        ]
    )
    session.flush()

    session.add(
        TenantMembershipModel(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            user_id=user.id,
            status=(
                MembershipStatus
                .SUSPENDED
                .value
            ),
        )
    )
    session.flush()

    repository = SqlAlchemyIdentityRepository(
        session
    )

    access = repository.resolve_active_access(
        auth_user_id=user.auth_user_id,
        tenant_id=tenant.id,
    )

    assert access is None
