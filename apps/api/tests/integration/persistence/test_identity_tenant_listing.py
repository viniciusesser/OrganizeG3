"""Persistence tests for accessible tenant discovery."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from organizeg3_api.domain.identity.enums import (
    MembershipStatus,
)
from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.models.user import (
    TenantMembershipModel,
    UserModel,
)
from organizeg3_api.infrastructure.persistence.repositories.identity_repository import (
    SqlAlchemyIdentityRepository,
)


def test_lists_active_tenants_for_auth_user(
    session: Session,
) -> None:
    auth_user_id = uuid.uuid4()

    user = UserModel(
        id=uuid.uuid4(),
        auth_user_id=auth_user_id,
        email="tenant-list@example.com",
        display_name="Tenant List",
        is_active=True,
    )

    tenant_b = TenantRecordModel(
        id=uuid.uuid4(),
        name="Empresa B",
        is_active=True,
    )

    tenant_a = TenantRecordModel(
        id=uuid.uuid4(),
        name="Empresa A",
        is_active=True,
    )

    session.add_all(
        [
            user,
            tenant_b,
            tenant_a,
        ]
    )
    session.flush()

    membership_b = TenantMembershipModel(
        id=uuid.uuid4(),
        tenant_id=tenant_b.id,
        user_id=user.id,
        status=MembershipStatus.ACTIVE.value,
    )

    membership_a = TenantMembershipModel(
        id=uuid.uuid4(),
        tenant_id=tenant_a.id,
        user_id=user.id,
        status=MembershipStatus.ACTIVE.value,
    )

    session.add_all(
        [
            membership_b,
            membership_a,
        ]
    )
    session.flush()

    repository = SqlAlchemyIdentityRepository(
        session
    )

    result = repository.list_accessible_tenants(
        auth_user_id=auth_user_id,
    )

    assert len(result) == 2

    assert [
        tenant.name
        for tenant in result
    ] == [
        "Empresa A",
        "Empresa B",
    ]

    assert result[0].tenant_id == tenant_a.id
    assert result[0].membership_id == membership_a.id

    assert result[1].tenant_id == tenant_b.id
    assert result[1].membership_id == membership_b.id


def test_excludes_non_active_memberships(
    session: Session,
) -> None:
    auth_user_id = uuid.uuid4()

    user = UserModel(
        id=uuid.uuid4(),
        auth_user_id=auth_user_id,
        email="inactive-membership@example.com",
        display_name="Inactive Membership",
        is_active=True,
    )

    tenant = TenantRecordModel(
        id=uuid.uuid4(),
        name="Empresa",
        is_active=True,
    )

    session.add_all(
        [
            user,
            tenant,
        ]
    )
    session.flush()

    membership = TenantMembershipModel(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        user_id=user.id,
        status=MembershipStatus.SUSPENDED.value,
    )

    session.add(membership)
    session.flush()

    repository = SqlAlchemyIdentityRepository(
        session
    )

    result = repository.list_accessible_tenants(
        auth_user_id=auth_user_id,
    )

    assert result == ()

