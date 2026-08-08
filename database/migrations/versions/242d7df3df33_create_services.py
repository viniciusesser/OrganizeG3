"""Create the tenant-scoped service catalog.

Revision ID: 242d7df3df33
Revises: ab28ad8ed9ed
Create Date: 2026-08-07 14:33:59.098459
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "242d7df3df33"
down_revision: str | None = "ab28ad8ed9ed"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the modern tenant-scoped service catalog."""

    op.create_table(
        "services",
        sa.Column(
            "code",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "category",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "unit",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "execution_mode",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "estimated_duration_minutes",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.CheckConstraint(
            "TRIM(category) <> ''",
            name=op.f(
                "ck_services_category_not_blank"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(code) <> ''",
            name=op.f(
                "ck_services_code_not_blank"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(name) <> ''",
            name=op.f(
                "ck_services_name_not_blank"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(unit) <> ''",
            name=op.f(
                "ck_services_unit_not_blank"
            ),
        ),
        sa.CheckConstraint(
            (
                "execution_mode IN "
                "('INTERNAL', 'EXTERNAL', 'BOTH')"
            ),
            name=op.f(
                "ck_services_execution_mode_valid"
            ),
        ),
        sa.CheckConstraint(
            (
                "estimated_duration_minutes IS NULL "
                "OR estimated_duration_minutes > 0"
            ),
            name=op.f(
                "ck_services_estimated_duration_positive"
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
                "fk_services_tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_services"
            ),
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_services_tenant_code",
        ),
    )

    op.create_index(
        "ix_services_tenant_active",
        "services",
        [
            "tenant_id",
            "is_active",
        ],
        unique=False,
    )

    op.create_index(
        "ix_services_tenant_category",
        "services",
        [
            "tenant_id",
            "category",
        ],
        unique=False,
    )

    op.create_index(
        "ix_services_tenant_execution_mode",
        "services",
        [
            "tenant_id",
            "execution_mode",
        ],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_services_tenant_id"
        ),
        "services",
        [
            "tenant_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_services_tenant_name",
        "services",
        [
            "tenant_id",
            "name",
        ],
        unique=False,
    )


def downgrade() -> None:
    """Remove the modern service catalog."""

    op.drop_index(
        "ix_services_tenant_name",
        table_name="services",
    )

    op.drop_index(
        op.f(
            "ix_services_tenant_id"
        ),
        table_name="services",
    )

    op.drop_index(
        "ix_services_tenant_execution_mode",
        table_name="services",
    )

    op.drop_index(
        "ix_services_tenant_category",
        table_name="services",
    )

    op.drop_index(
        "ix_services_tenant_active",
        table_name="services",
    )

    op.drop_table(
        "services"
    )
