"""add_semantic_fields_to_analysis_results

Revision ID: 9014f41ae9e3
Revises: 4cca489f25bd
Create Date: 2026-07-15 19:32:20.422583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9014f41ae9e3'
down_revision: Union[str, None] = '4cca489f25bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('analysis_results', sa.Column('semantic_profile', sa.JSON(), nullable=True))
    op.add_column('analysis_results', sa.Column('dataset_domain', sa.String(), nullable=True))
    op.add_column('analysis_results', sa.Column('entity', sa.String(), nullable=True))
    op.add_column('analysis_results', sa.Column('feature_metadata', sa.JSON(), nullable=True))
    op.add_column('analysis_results', sa.Column('relationship_metadata', sa.JSON(), nullable=True))
    op.add_column('analysis_results', sa.Column('ml_readiness', sa.JSON(), nullable=True))
    op.add_column('analysis_results', sa.Column('chart_suggestions', sa.JSON(), nullable=True))
    op.add_column('analysis_results', sa.Column('kpi_suggestions', sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column('analysis_results', 'kpi_suggestions')
    op.drop_column('analysis_results', 'chart_suggestions')
    op.drop_column('analysis_results', 'ml_readiness')
    op.drop_column('analysis_results', 'relationship_metadata')
    op.drop_column('analysis_results', 'feature_metadata')
    op.drop_column('analysis_results', 'entity')
    op.drop_column('analysis_results', 'dataset_domain')
    op.drop_column('analysis_results', 'semantic_profile')
