"""create_dataset_table

Revision ID: 847ade44efee
Revises: 6469234af0e7
Create Date: 2026-07-15 13:29:17.516998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '847ade44efee'
down_revision: Union[str, None] = '6469234af0e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # processing_state_enum = sa.Enum('UPLOADING', 'VALIDATING', 'PROCESSING', 'READY', 'FAILED', name='processingstate')
    # processing_state_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'datasets',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('workspace_id', sa.Integer(), nullable=True),
        sa.Column('session_id', sa.String(), nullable=True),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('original_filename', sa.String(), nullable=False),
        sa.Column('dataset_type', sa.String(), nullable=False),
        sa.Column('rows', sa.Integer(), nullable=False),
        sa.Column('columns', sa.Integer(), nullable=False),
        sa.Column('size_bytes', sa.Integer(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        sa.Column('status', sa.Enum('UPLOADING', 'VALIDATING', 'PROCESSING', 'READY', 'FAILED', name='processingstate'), nullable=False),
        sa.Column('first_5_rows_json', sa.JSON(), nullable=True),
        sa.Column('missing_values', sa.Integer(), nullable=False),
        sa.Column('duplicate_rows', sa.Integer(), nullable=False),
        sa.Column('column_metadata', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_datasets_id'), 'datasets', ['id'], unique=False)
    op.create_index(op.f('ix_datasets_session_id'), 'datasets', ['session_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_datasets_session_id'), table_name='datasets')
    op.drop_index(op.f('ix_datasets_id'), table_name='datasets')
    op.drop_table('datasets')
    
    # Drop enum type
    processing_state_enum = sa.Enum('UPLOADING', 'VALIDATING', 'PROCESSING', 'READY', 'FAILED', name='processingstate')
    processing_state_enum.drop(op.get_bind(), checkfirst=True)
