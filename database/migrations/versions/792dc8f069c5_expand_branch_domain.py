"""Expand branch domain.

Revision ID: 792dc8f069c5
Revises: e47492c9a55a
Create Date: 2026-08-07 13:13:42.947339
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "792dc8f069c5"
down_revision: str | None = "e47492c9a55a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "branches",
        sa.Column(
            "state_registration",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "branches",
        sa.Column(
            "email",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "branches",
        sa.Column(
            "phone",
            sa.String(length=20),
            nullable=True,
        ),
    )

    op.add_column(
        "branches",
        sa.Column(
            "website",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "branches",
        sa.Column(
            "street",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "branches",
        sa.Column(
            "number",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "branches",
        sa.Column(
            "district",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "branches",
        sa.Column(
            "city",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "branches",
        sa.Column(
            "state",
            sa.String(length=2),
            nullable=True,
        ),
    )

    op.add_column(
        "branches",
        sa.Column(
            "postal_code",
            sa.String(length=8),
            nullable=True,
        ),
    )

    op.create_index(
        "uq_branches_tenant_headquarters",
        "branches",
        ["tenant_id"],
        unique=True,
        postgresql_where=sa.text(
            "is_headquarters = true"
        ),
        sqlite_where=sa.text(
            "is_headquarters = 1"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "uq_branches_tenant_headquarters",
        table_name="branches",
        postgresql_where=sa.text(
            "is_headquarters = true"
        ),
        sqlite_where=sa.text(
            "is_headquarters = 1"
        ),
    )

    op.drop_column(
        "branches",
        "postal_code",
    )

    op.drop_column(
        "branches",
        "state",
    )

    op.drop_column(
        "branches",
        "city",
    )

    op.drop_column(
        "branches",
        "district",
    )

    op.drop_column(
        "branches",
        "number",
    )

    op.drop_column(
        "branches",
        "street",
    )

    op.drop_column(
        "branches",
        "website",
    )

    op.drop_column(
        "branches",
        "phone",
    )

    op.drop_column(
        "branches",
        "email",
    )

    op.drop_column(
        "branches",
        "state_registration",
    )
