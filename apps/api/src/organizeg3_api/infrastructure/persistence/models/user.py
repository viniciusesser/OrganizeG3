"""SQLAlchemy models for users and tenant memberships."""

from __future__ import annotations

from datetime import datetime
import uuid

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from organizeg3_api.domain.identity.enums import MembershipStatus
from organizeg3_api.infrastructure.database.base import (
    ActiveStatusMixin,
    Base,
    OptimisticLockMixin,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    utc_now,
)


class UserModel(
    Base,
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    SoftDeleteMixin,
    OptimisticLockMixin,
    ActiveStatusMixin,
):
    """Represent one application identity backed by Supabase Auth."""

    __tablename__ = "users"

    auth_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
    )

    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "auth_user_id",
            name="uq_users_auth_user_id",
        ),
        CheckConstraint(
            "TRIM(email) <> ''",
            name="email_not_blank",
        ),
        CheckConstraint(
            "TRIM(display_name) <> ''",
            name="display_name_not_blank",
        ),
        CheckConstraint(
            "row_version >= 1",
            name="row_version_positive",
        ),
        Index(
            "uq_users_email_normalized",
            text("lower(TRIM(BOTH FROM email))"),
            unique=True,
        ).ddl_if(
            dialect="postgresql"
        ),
        Index(
            "ix_users_active_deleted",
            "is_active",
            "deleted_at",
        ),
    )


class TenantMembershipModel(
    Base,
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    OptimisticLockMixin,
):
    """Associate one application user with one tenant."""

    __tablename__ = "tenant_memberships"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "tenants.id",
            name="fk_tenant_memberships_tenant_id_tenants",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "users.id",
            name="fk_tenant_memberships_user_id_users",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=MembershipStatus.INVITED.value,
    )

    invited_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    joined_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    suspended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "user_id",
            name="uq_tenant_memberships_tenant_user",
        ),
        UniqueConstraint(
            "id",
            "tenant_id",
            name="uq_tenant_memberships_id_tenant",
        ),
        CheckConstraint(
            (
                "status IN "
                "('INVITED', 'ACTIVE', 'SUSPENDED', 'REVOKED')"
            ),
            name="status_valid",
        ),
        CheckConstraint(
            "row_version >= 1",
            name="row_version_positive",
        ),
        Index(
            "ix_tenant_memberships_tenant_status",
            "tenant_id",
            "status",
        ),
        Index(
            "ix_tenant_memberships_user_id",
            "user_id",
        ),
    )
