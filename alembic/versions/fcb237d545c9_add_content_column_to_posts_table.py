"""add content column to posts table

Revision ID: fcb237d545c9
Revises: ab8eaac43443
Create Date: 2025-08-15 00:16:48.412435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcb237d545c9'
down_revision: Union[str, Sequence[str], None] = 'ab8eaac43443'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
