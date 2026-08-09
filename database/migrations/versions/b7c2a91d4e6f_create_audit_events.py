"""create audit events

Revision ID: b7c2a91d4e6f
Revises: 6f217e7442e3
Create Date: 2026-08-08
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "b7c2a91d4e6f"
down_revision: str | Sequence[str] | None = "6f217e7442e3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the append-only business audit trail."""

    op.create_table(
        "audit_events",
        sa.Column(
            "tenant_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "branch_id",
            sa.UUID(),
            nullable=True,
        ),
        sa.Column(
            "actor_user_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "membership_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "auth_user_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "action",
            sa.String(
                length=50
            ),
            nullable=False,
        ),
        sa.Column(
            "resource",
            sa.String(
                length=100
            ),
            nullable=False,
        ),
        sa.Column(
            "resource_id",
            sa.String(
                length=255
            ),
            nullable=False,
        ),
        sa.Column(
            "correlation_id",
            sa.String(
                length=255
            ),
            nullable=False,
        ),
        sa.Column(
            "device_id",
            sa.String(
                length=255
            ),
            nullable=True,
        ),
        sa.Column(
            "before",
            sa.JSON(),
            nullable=True,
        ),
        sa.Column(
            "after",
            sa.JSON(),
            nullable=True,
        ),
        sa.Column(
            "metadata",
            sa.JSON(),
            nullable=True,
        ),
        sa.Column(
            "occurred_at",
            sa.DateTime(
                timezone=True
            ),
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "TRIM(action) <> ''",
            name=op.f(
                "ck_audit_events_action_not_blank"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(resource) <> ''",
            name=op.f(
                "ck_audit_events_resource_not_blank"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(resource_id) <> ''",
            name=op.f(
                "ck_audit_events_resource_id_not_blank"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(correlation_id) <> ''",
            name=op.f(
                "ck_audit_events_correlation_id_not_blank"
            ),
        ),
        sa.ForeignKeyConstraint(
            [
                "tenant_id",
            ],
            [
                "tenants.id",
            ],
            name=op.f(
                "fk_audit_events_tenant_id_tenants"
            ),
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_audit_events"
            ),
        ),
    )

    op.create_index(
        op.f(
            "ix_audit_events_tenant_id"
        ),
        "audit_events",
        [
            "tenant_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_audit_events_tenant_occurred",
        "audit_events",
        [
            "tenant_id",
            "occurred_at",
        ],
        unique=False,
    )

    op.create_index(
        "ix_audit_events_tenant_resource",
        "audit_events",
        [
            "tenant_id",
            "resource",
            "resource_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_audit_events_tenant_actor",
        "audit_events",
        [
            "tenant_id",
            "actor_user_id",
            "occurred_at",
        ],
        unique=False,
    )

    op.create_index(
        "ix_audit_events_tenant_correlation",
        "audit_events",
        [
            "tenant_id",
            "correlation_id",
        ],
        unique=False,
    )


def downgrade() -> None:
    """Remove the business audit trail."""

    op.drop_index(
        "ix_audit_events_tenant_correlation",
        table_name="audit_events",
    )

    op.drop_index(
        "ix_audit_events_tenant_actor",
        table_name="audit_events",
    )

    op.drop_index(
        "ix_audit_events_tenant_resource",
        table_name="audit_events",
    )

    op.drop_index(
        "ix_audit_events_tenant_occurred",
        table_name="audit_events",
    )

    op.drop_index(
        op.f(
            "ix_audit_events_tenant_id"
        ),
        table_name="audit_events",
    )

    op.drop_table(
        "audit_events"
    )
