"""add_workspace_status

Revision ID: 7d14d2115ee4
Revises: 9014f41ae9e3
Create Date: 2026-07-16 18:00:42.521794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d14d2115ee4'
down_revision: Union[str, None] = '9014f41ae9e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum type first in PostgreSQL schema
    workspace_state = sa.Enum('NEW', 'UPLOADING', 'ANALYZING', 'READY', 'ARCHIVED', name='workspacestate')
    workspace_state.create(op.get_bind(), checkfirst=True)
    
    # Safely drop constraint checkfirst
    try:
        op.drop_constraint('analysis_results_dataset_id_key', 'analysis_results', type_='unique')
    except Exception:
        pass
        
    op.add_column('workspaces', sa.Column('status', workspace_state, nullable=False, server_default='NEW'))


def downgrade() -> None:
    op.drop_column('workspaces', 'status')
    
    # Drop enum type in PostgreSQL
    workspace_state = sa.Enum('NEW', 'UPLOADING', 'ANALYZING', 'READY', 'ARCHIVED', name='workspacestate')
    workspace_state.drop(op.get_bind(), checkfirst=True)
    
    try:
        op.create_unique_constraint('analysis_results_dataset_id_key', 'analysis_results', ['dataset_id'])
    except Exception:
        pass
