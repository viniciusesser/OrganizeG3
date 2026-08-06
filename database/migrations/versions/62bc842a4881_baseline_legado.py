"""baseline_legado

Revision ID: 62bc842a4881
Revises: acc9bffaedbc
Create Date: 2026-08-05 11:41:01.616187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62bc842a4881'
down_revision: Union[str, Sequence[str], None] = 'acc9bffaedbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
