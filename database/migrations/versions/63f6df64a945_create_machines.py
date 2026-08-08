"""Create the tenant-scoped industrial machine catalog.

Revision ID: 63f6df64a945
Revises: 242d7df3df33
Create Date: 2026-08-07 14:44:25.852089
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "63f6df64a945"
down_revision: str | None = "242d7df3df33"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the modern tenant-scoped industrial machine catalog."""

    op.create_table(
        "machines",
        sa.Column(
            "branch_id",
            sa.Uuid(),
            nullable=True,
        ),
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
            "machine_type",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "manufacturer",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "model",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "serial_number",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.String(length=30),
            server_default=sa.text(
                "'AVAILABLE'"
            ),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text(
                "true"
            ),
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
            "TRIM(code) <> ''",
            name=op.f(
                "ck_machines_code_not_blank"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(machine_type) <> ''",
            name=op.f(
                "ck_machines_machine_type_not_blank"
            ),
        ),
        sa.CheckConstraint(
            "TRIM(name) <> ''",
            name=op.f(
                "ck_machines_name_not_blank"
            ),
        ),
        sa.CheckConstraint(
            (
                "status IN "
                "('AVAILABLE', 'IN_USE', "
                "'MAINTENANCE', 'OUT_OF_SERVICE')"
            ),
            name=op.f(
                "ck_machines_status_valid"
            ),
        ),
        sa.ForeignKeyConstraint(
            [
                "branch_id",
                "tenant_id",
            ],
            [
                "branches.id",
                "branches.tenant_id",
            ],
            name="fk_machines_branch_tenant",
        ),
        sa.ForeignKeyConstraint(
            [
                "tenant_id",
            ],
            [
                "tenants.id",
            ],
            name=op.f(
                "fk_machines_tenant_id_tenants"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_machines"
            ),
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "code",
            name="uq_machines_tenant_code",
        ),
    )

    op.create_index(
        "ix_machines_tenant_active",
        "machines",
        [
            "tenant_id",
            "is_active",
        ],
        unique=False,
    )

    op.create_index(
        "ix_machines_tenant_branch",
        "machines",
        [
            "tenant_id",
            "branch_id",
        ],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_machines_tenant_id"
        ),
        "machines",
        [
            "tenant_id",
        ],
        unique=False,
    )

    op.create_index(
        "ix_machines_tenant_name",
        "machines",
        [
            "tenant_id",
            "name",
        ],
        unique=False,
    )

    op.create_index(
        "ix_machines_tenant_status",
        "machines",
        [
            "tenant_id",
            "status",
        ],
        unique=False,
    )

    op.create_index(
        "ix_machines_tenant_type",
        "machines",
        [
            "tenant_id",
            "machine_type",
        ],
        unique=False,
    )


def downgrade() -> None:
    """Remove the modern industrial machine catalog."""

    op.drop_index(
        "ix_machines_tenant_type",
        table_name="machines",
    )

    op.drop_index(
        "ix_machines_tenant_status",
        table_name="machines",
    )

    op.drop_index(
        "ix_machines_tenant_name",
        table_name="machines",
    )

    op.drop_index(
        op.f(
            "ix_machines_tenant_id"
        ),
        table_name="machines",
    )

    op.drop_index(
        "ix_machines_tenant_branch",
        table_name="machines",
    )

    op.drop_index(
        "ix_machines_tenant_active",
        table_name="machines",
    )

    op.drop_table(
        "machines"
    )
