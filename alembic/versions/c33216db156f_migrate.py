"""migrate

Revision ID: c33216db156f
Revises: 
Create Date: 2024-07-06 14:01:39.742236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c33216db156f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('productrecommendations', 'id', existing_type=sa.Integer(), type_=sa.String())

def downgrade() -> None:
    pass
