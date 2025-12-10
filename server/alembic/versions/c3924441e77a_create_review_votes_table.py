"""create review votes table

Revision ID: c3924441e77a
Revises: 586556048ef0
Create Date: 2025-12-10 19:21:13.866195

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3924441e77a'
down_revision: Union[str, None] = '586556048ef0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create review_votes table
    op.create_table(
        'review_votes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('review_id', sa.Integer(), nullable=False),
        sa.Column('vote_type', sa.String(20), nullable=False, server_default='helpful'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'review_id', name='unique_user_review_vote')
    )
    op.create_index('idx_review_votes_review_id', 'review_votes', ['review_id'])
    op.create_index('idx_review_votes_user_id', 'review_votes', ['user_id'])
    
    # Add helpful_count column to reviews table
    op.add_column('reviews', sa.Column('helpful_count', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    # Remove helpful_count column from reviews
    op.drop_column('reviews', 'helpful_count')
    
    # Drop indexes
    op.drop_index('idx_review_votes_user_id', 'review_votes')
    op.drop_index('idx_review_votes_review_id', 'review_votes')
    
    # Drop review_votes table
    op.drop_table('review_votes')
