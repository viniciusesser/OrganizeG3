"""Integration tests for identity persistence models."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy.exc import IntegrityError
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


def create_tenant(
    session: Session,
    *,
    name: str,
) -> TenantModel:
    tenant = TenantModel(
        id=uuid.uuid4(),
        name=name,
        status="ACTIVE",
        is_active=True,
    )

    session.add(tenant)
    session.flush()

    return tenant


def test_creates_identity_authorization_graph(
    session: Session,
) -> None:
    tenant = create_tenant(
        session,
        name="Empresa Identidade",
    )

    user = UserModel(
        id=uuid.uuid4(),
        auth_user_id=uuid.uuid4(),
        email="admin@example.com",
        display_name="Administrador",
        is_active=True,
    )

    session.add(user)
    session.flush()

    membership = TenantMembershipModel(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        user_id=user.id,
        status=MembershipStatus.ACTIVE.value,
    )

    session.add(membership)
    session.flush()

    profile = AccessProfileModel(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        code="ADMINISTRATOR",
        name="Administrador",
        is_system=True,
        is_active=True,
    )

    permission = PermissionModel(
        id=uuid.uuid4(),
        code="customers.read",
        name="Consultar clientes",
        module="customers",
        resource="customer",
        action="read",
        is_active=True,
    )

    session.add_all(
        [
            profile,
            permission,
        ]
    )

    session.flush()

    profile_permission = (
        AccessProfilePermissionModel(
            access_profile_id=profile.id,
            permission_id=permission.id,
        )
    )

    membership_profile = (
        TenantMembershipProfileModel(
            tenant_id=tenant.id,
            membership_id=membership.id,
            access_profile_id=profile.id,
        )
    )

    override = (
        TenantMembershipPermissionOverrideModel(
            tenant_id=tenant.id,
            membership_id=membership.id,
            permission_id=permission.id,
            effect=PermissionEffect.ALLOW.value,
        )
    )

    session.add_all(
        [
            profile_permission,
            membership_profile,
            override,
        ]
    )

    session.flush()

    assert membership.tenant_id == tenant.id
    assert membership.user_id == user.id
    assert membership.status == "ACTIVE"
    assert profile.tenant_id == tenant.id
    assert permission.code == "customers.read"
    assert override.effect == "ALLOW"


def test_same_user_can_have_multiple_tenant_memberships(
    session: Session,
) -> None:
    first_tenant = create_tenant(
        session,
        name="Empresa A",
    )

    second_tenant = create_tenant(
        session,
        name="Empresa B",
    )

    user = UserModel(
        id=uuid.uuid4(),
        auth_user_id=uuid.uuid4(),
        email="multiempresa@example.com",
        display_name="Usuário Multiempresa",
        is_active=True,
    )

    session.add(user)
    session.flush()

    session.add_all(
        [
            TenantMembershipModel(
                id=uuid.uuid4(),
                tenant_id=first_tenant.id,
                user_id=user.id,
                status=MembershipStatus.ACTIVE.value,
            ),
            TenantMembershipModel(
                id=uuid.uuid4(),
                tenant_id=second_tenant.id,
                user_id=user.id,
                status=MembershipStatus.ACTIVE.value,
            ),
        ]
    )

    session.flush()


def test_rejects_duplicate_membership(
    session: Session,
) -> None:
    tenant = create_tenant(
        session,
        name="Empresa Única",
    )

    user = UserModel(
        id=uuid.uuid4(),
        auth_user_id=uuid.uuid4(),
        email="duplicate@example.com",
        display_name="Usuário Duplicado",
        is_active=True,
    )

    session.add(user)
    session.flush()

    session.add_all(
        [
            TenantMembershipModel(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                user_id=user.id,
                status=MembershipStatus.ACTIVE.value,
            ),
            TenantMembershipModel(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                user_id=user.id,
                status=MembershipStatus.ACTIVE.value,
            ),
        ]
    )

    with pytest.raises(
        IntegrityError
    ):
        session.flush()
