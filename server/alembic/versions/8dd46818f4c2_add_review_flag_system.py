"""add review flag system

Revision ID: 8dd46818f4c2
Revises: bfd801ceb4f2
Create Date: 2025-12-10 20:13:40.217884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8dd46818f4c2'
down_revision: Union[str, None] = 'bfd801ceb4f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create review_flags table
    op.create_table(
        'review_flags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('review_id', sa.Integer(), nullable=False),
        sa.Column('reason', sa.String(500), nullable=True),
        sa.Column('flagged_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'review_id', name='unique_user_review_flag')
    )
    op.create_index('idx_review_flags_review_id', 'review_flags', ['review_id'])
    op.create_index('idx_review_flags_user_id', 'review_flags', ['user_id'])
    
    # Add flag tracking to reviews table
    op.add_column('reviews', sa.Column('is_flagged', sa.Boolean(), nullable=False, server_default='0'))
    op.add_column('reviews', sa.Column('flag_count', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    # Remove flag columns from reviews
    op.drop_column('reviews', 'flag_count')
    op.drop_column('reviews', 'is_flagged')
    
    # Drop review_flags table
    op.drop_index('idx_review_flags_user_id', 'review_flags')
    op.drop_index('idx_review_flags_review_id', 'review_flags')
    op.drop_table('review_flags')
