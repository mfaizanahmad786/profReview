"""add professor claim system

Revision ID: bfd801ceb4f2
Revises: c3924441e77a
Create Date: 2025-12-10 19:39:28.794492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bfd801ceb4f2'
down_revision: Union[str, None] = 'c3924441e77a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create professor_claim_requests table
    op.create_table(
        'professor_claim_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('professor_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('request_message', sa.Text(), nullable=True),
        sa.Column('requested_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('reviewed_at', sa.DateTime(), nullable=True),
        sa.Column('reviewed_by', sa.Integer(), nullable=True),
        sa.Column('rejection_reason', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['professor_id'], ['professors.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['reviewed_by'], ['users.id'], ondelete='SET NULL'),
        sa.UniqueConstraint('user_id', 'professor_id', name='unique_user_professor_claim')
    )
    op.create_index('idx_claim_requests_user_id', 'professor_claim_requests', ['user_id'])
    op.create_index('idx_claim_requests_professor_id', 'professor_claim_requests', ['professor_id'])
    op.create_index('idx_claim_requests_status', 'professor_claim_requests', ['status'])
    
    # Add new claim fields to professors table (claimed_by_user_id already exists)
    op.add_column('professors', sa.Column('is_claimed', sa.Boolean(), nullable=False, server_default='0'))
    op.add_column('professors', sa.Column('claimed_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    # Drop new claim fields from professors table
    op.drop_column('professors', 'claimed_at')
    op.drop_column('professors', 'is_claimed')
    
    # Drop professor_claim_requests table
    op.drop_index('idx_claim_requests_status', 'professor_claim_requests')
    op.drop_index('idx_claim_requests_professor_id', 'professor_claim_requests')
    op.drop_index('idx_claim_requests_user_id', 'professor_claim_requests')
    op.drop_table('professor_claim_requests')
