"""SQLAlchemy models for profiles and granular permissions."""

from __future__ import annotations

from datetime import datetime
import uuid

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from organizeg3_api.domain.identity.enums import PermissionEffect
from organizeg3_api.infrastructure.database.base import (
    ActiveStatusMixin,
    Base,
    OptimisticLockMixin,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    utc_now,
)


class AccessProfileModel(
    Base,
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    SoftDeleteMixin,
    OptimisticLockMixin,
    ActiveStatusMixin,
):
    """Represent a reusable tenant-specific access profile."""

    __tablename__ = "access_profiles"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "tenants.id",
            name="fk_access_profiles_tenant_id_tenants",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_system: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_access_profiles_id_tenant",
        ),
        CheckConstraint(
            "TRIM(code) <> ''",
            name="code_not_blank",
        ),
        CheckConstraint(
            "TRIM(name) <> ''",
            name="name_not_blank",
        ),
        CheckConstraint(
            "row_version >= 1",
            name="row_version_positive",
        ),
        Index(
            "uq_access_profiles_tenant_code_normalized",
            "tenant_id",
            text("lower(TRIM(BOTH FROM code))"),
            unique=True,
        ).ddl_if(
            dialect="postgresql"
        ),
        Index(
            "ix_access_profiles_tenant_active",
            "tenant_id",
            "is_active",
        ),
    )


class PermissionModel(
    Base,
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    ActiveStatusMixin,
):
    """Represent the smallest reusable authorization capability."""

    __tablename__ = "permissions"

    code: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    module: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    resource: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    __table_args__ = (
        CheckConstraint(
            "TRIM(code) <> ''",
            name="code_not_blank",
        ),
        CheckConstraint(
            "TRIM(name) <> ''",
            name="name_not_blank",
        ),
        CheckConstraint(
            "TRIM(module) <> ''",
            name="module_not_blank",
        ),
        CheckConstraint(
            "TRIM(resource) <> ''",
            name="resource_not_blank",
        ),
        CheckConstraint(
            "TRIM(action) <> ''",
            name="action_not_blank",
        ),
        Index(
            "uq_permissions_code_normalized",
            text("lower(TRIM(BOTH FROM code))"),
            unique=True,
        ).ddl_if(
            dialect="postgresql"
        ),
        Index(
            "ix_permissions_module_resource",
            "module",
            "resource",
        ),
    )


class AccessProfilePermissionModel(Base):
    """Grant one permission to one access profile."""

    __tablename__ = "access_profile_permissions"

    access_profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "access_profiles.id",
            name=(
                "fk_access_profile_permissions_"
                "access_profile_id_access_profiles"
            ),
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    permission_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "permissions.id",
            name=(
                "fk_access_profile_permissions_"
                "permission_id_permissions"
            ),
            ondelete="RESTRICT",
        ),
        primary_key=True,
    )

    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )


class TenantMembershipProfileModel(Base):
    """Assign one tenant profile to one membership."""

    __tablename__ = "tenant_membership_profiles"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
    )

    membership_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
    )

    access_profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    __table_args__ = (
        ForeignKeyConstraint(
            [
                "membership_id",
                "tenant_id",
            ],
            [
                "tenant_memberships.id",
                "tenant_memberships.tenant_id",
            ],
            name=(
                "fk_tenant_membership_profiles_"
                "membership_tenant"
            ),
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            [
                "access_profile_id",
                "tenant_id",
            ],
            [
                "access_profiles.id",
                "access_profiles.tenant_id",
            ],
            name=(
                "fk_tenant_membership_profiles_"
                "profile_tenant"
            ),
            ondelete="RESTRICT",
        ),
        Index(
            "ix_tenant_membership_profiles_profile",
            "access_profile_id",
        ),
    )


class TenantMembershipPermissionOverrideModel(Base):
    """Explicitly allow or deny a permission for one membership."""

    __tablename__ = "tenant_membership_permission_overrides"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
    )

    membership_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
    )

    permission_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "permissions.id",
            name="fk_tm_permission_overrides_permission",
            ondelete="RESTRICT",
        ),
        primary_key=True,
    )

    effect: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    __table_args__ = (
        ForeignKeyConstraint(
            [
                "membership_id",
                "tenant_id",
            ],
            [
                "tenant_memberships.id",
                "tenant_memberships.tenant_id",
            ],
            name=(
                "fk_tenant_membership_permission_"
                "overrides_membership_tenant"
            ),
            ondelete="CASCADE",
        ),
        CheckConstraint(
            (
                "effect IN "
                f"('{PermissionEffect.ALLOW.value}', "
                f"'{PermissionEffect.DENY.value}')"
            ),
            name="effect_valid",
        ),
        Index(
            "ix_tenant_membership_permission_overrides_permission",
            "permission_id",
        ),
    )
