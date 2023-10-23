"""add content column to posts table

Revision ID: 60eb2f124363
Revises: 8b6703283857
Create Date: 2023-10-23 09:17:51.050830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60eb2f124363'
down_revision: Union[str, None] = '8b6703283857'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
