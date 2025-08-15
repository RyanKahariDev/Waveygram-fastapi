"""lets add content

Revision ID: 1b7041ec6712
Revises: 6ef1040dd955
Create Date: 2025-08-15 00:46:18.146613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b7041ec6712'
down_revision: Union[str, Sequence[str], None] = '6ef1040dd955'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
