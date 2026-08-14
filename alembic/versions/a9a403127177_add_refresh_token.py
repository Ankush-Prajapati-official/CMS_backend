"""add refresh token

Revision ID: a9a403127177
Revises: d52eca7bfb14
Create Date: 2026-08-13 20:47:25.161519

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a9a403127177"
down_revision: Union[str, Sequence[str], None] = "d52eca7bfb14"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass