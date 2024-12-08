"""add meals

Revision ID: 7239603b23b2
Revises: 2e5033376bc4
Create Date: 2024-12-08 13:20:27.123237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7239603b23b2'
down_revision: Union[str, None] = '2e5033376bc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('week_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('day', sa.Enum('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY', name='day'), nullable=False),
    sa.Column('type', sa.Enum('BREAKFAST', 'LUNCH', 'SNACKS', 'DINNER', name='mealtype'), nullable=False),
    sa.Column('picture', sa.Text(), nullable=True),
    sa.Column('ingredients', sa.Text(), nullable=False),
    sa.Column('steps', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['week_id'], ['weeks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('meals')
    # ### end Alembic commands ###
