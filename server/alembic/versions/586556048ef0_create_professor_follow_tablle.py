"""create professor follow tablle

Revision ID: 586556048ef0
Revises: edba7c9e2ccd
Create Date: 2025-12-09 17:51:53.595394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '586556048ef0'
down_revision: Union[str, None] = 'edba7c9e2ccd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create professor_follows table
    op.create_table(
        'professor_follows',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('professor_id', sa.Integer(), nullable=False),
        sa.Column('followed_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['professor_id'], ['professors.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'professor_id', name='unique_user_professor_follow')
    )
    
    # Create indexes for better query performance
    op.create_index('ix_professor_follows_user_id', 'professor_follows', ['user_id'])
    op.create_index('ix_professor_follows_professor_id', 'professor_follows', ['professor_id'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_professor_follows_professor_id', table_name='professor_follows')
    op.drop_index('ix_professor_follows_user_id', table_name='professor_follows')
    
    # Drop table
    op.drop_table('professor_follows')
