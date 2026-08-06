"""Establish the legacy database as the Alembic baseline.

Revision ID: acc9bffaedbc
Revises:
Create Date: 2026-08-05 11:39:30.962707

This revision intentionally performs no DDL. The OrganizeG3 migration strategy
starts from an existing legacy schema, which must be stamped at this revision
before incremental, non-destructive migrations are applied.
"""

from collections.abc import Sequence

revision: str = "acc9bffaedbc"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Preserve the pre-existing legacy schema without destructive DDL."""


def downgrade() -> None:
    """Keep the legacy schema intact when removing the baseline marker."""
