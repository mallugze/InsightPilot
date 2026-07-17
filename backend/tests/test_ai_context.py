import pytest
from unittest.mock import MagicMock
from app.services.ai.context_builder import ContextBuilder
from app.services.ai.models import AIAnalysisContext
from app.models.analysis_result import AnalysisResult
from app.models.dataset import Dataset

def test_context_builder_success():
    # 1. Create mocks for Database objects
    mock_analysis = MagicMock(spec=AnalysisResult)
    mock_analysis.id = 42
    mock_analysis.dataset_id = 99
    mock_analysis.workspace_id = 1
    mock_analysis.business_pulse = 95.0
    mock_analysis.health_label = "READY"
    mock_analysis.pulse_breakdown = {"quality": 98}
    mock_analysis.kpis = [{"name": "Revenue", "value": 500}]
    mock_analysis.hero = {"name": "Revenue"}
    mock_analysis.zero = {"name": "Cost"}
    mock_analysis.trends = [{"direction": "up"}]
    mock_analysis.anomalies = []
    mock_analysis.correlations = []
    mock_analysis.recommendations = [{"text": "Action"}]
    mock_analysis.insights = []
    mock_analysis.dataset_domain = "Sales"
    mock_analysis.entity = "Executive"
    mock_analysis.feature_metadata = []
    mock_analysis.ml_readiness = {}
    mock_analysis.chart_suggestions = []
    mock_analysis.kpi_suggestions = []

    mock_dataset = MagicMock(spec=Dataset)
    mock_dataset.id = 99
    mock_dataset.rows = 150
    mock_dataset.columns = 5
    mock_dataset.missing_values = 10
    mock_dataset.duplicate_rows = 2
    mock_dataset.original_filename = "sales_test.csv"
    mock_dataset.dataset_type = "Sales Ingestion"
    mock_dataset.column_metadata = {"validation_report": {"encoding": "utf-8", "delimiter": ","}}

    # 2. Mock Database session
    mock_db = MagicMock()
    # Mock chain db.query().filter().first()
    mock_db.query.return_value.filter.return_value.first.side_effect = [mock_analysis, mock_dataset]

    # 3. Execute Builder
    builder = ContextBuilder()
    context = builder.build_context(analysis_id=42, db=mock_db)

    # 4. Verify context attributes
    assert isinstance(context, AIAnalysisContext)
    assert context.analysis_id == 42
    assert context.dataset_id == 99
    assert context.business_pulse == 95.0
    assert context.health_label == "READY"
    assert context.rows_count == 150
    assert context.cols_count == 5
    assert context.dataset_name == "sales_test.csv"
    assert context.validation_report["encoding"] == "utf-8"
