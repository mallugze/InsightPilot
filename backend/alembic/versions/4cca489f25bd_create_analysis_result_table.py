"""create_analysis_result_table

Revision ID: 4cca489f25bd
Revises: 847ade44efee
Create Date: 2026-07-15 14:11:46.259433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cca489f25bd'
down_revision: Union[str, None] = '847ade44efee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'analysis_results',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('workspace_id', sa.Integer(), nullable=True),
        sa.Column('dataset_id', sa.Integer(), nullable=False),
        sa.Column('business_pulse', sa.Float(), nullable=False),
        sa.Column('health_label', sa.String(), nullable=False),
        sa.Column('pulse_breakdown', sa.JSON(), nullable=True),
        sa.Column('kpis', sa.JSON(), nullable=True),
        sa.Column('hero', sa.JSON(), nullable=True),
        sa.Column('zero', sa.JSON(), nullable=True),
        sa.Column('trends', sa.JSON(), nullable=True),
        sa.Column('anomalies', sa.JSON(), nullable=True),
        sa.Column('correlations', sa.JSON(), nullable=True),
        sa.Column('recommendations', sa.JSON(), nullable=True),
        sa.Column('insights', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('dataset_id')
    )
    op.create_index(op.f('ix_analysis_results_id'), 'analysis_results', ['id'], unique=False)
    op.create_index(op.f('ix_analysis_results_dataset_id'), 'analysis_results', ['dataset_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_analysis_results_dataset_id'), table_name='analysis_results')
    op.drop_index(op.f('ix_analysis_results_id'), table_name='analysis_results')
    op.drop_table('analysis_results')
