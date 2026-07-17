import pytest
from app.services.ai.response_validator import ResponseValidator, AIValidationException
from app.services.ai.models import AIAnalysisContext

def test_response_validator_success():
    context = AIAnalysisContext(
        analysis_id=1,
        dataset_id=2,
        dataset_name="test.csv",
        dataset_type="Sales",
        dataset_domain="Business",
        rows_count=150,
        cols_count=5,
        missing_values_count=0,
        duplicate_rows_count=0,
        quality_score=100.0,
        business_pulse=95.0,
        health_label="READY"
    )

    validator = ResponseValidator()

    # Case 1: Factual match
    valid_text = "The overall business pulse stands at 95.0. Total row count is 150 with 5 columns. Data quality score is 100.0."
    result = validator.validate(valid_text, context)
    assert result == valid_text

    # Case 2: General text without numbers
    no_num_text = "The dataset has positive growth indicators and recommendations are active."
    assert validator.validate(no_num_text, context) == no_num_text

def test_response_validator_hallucination_pulse():
    context = AIAnalysisContext(
        analysis_id=1,
        dataset_id=2,
        dataset_name="test.csv",
        dataset_type="Sales",
        dataset_domain="Business",
        rows_count=150,
        cols_count=5,
        missing_values_count=0,
        duplicate_rows_count=0,
        quality_score=100.0,
        business_pulse=95.0,
        health_label="READY"
    )

    validator = ResponseValidator()

    # Hallucinated business pulse (80.0 instead of 95.0)
    invalid_pulse = "The business pulse is 80.0. Total row count is 150."
    with pytest.raises(AIValidationException) as exc_info:
        validator.validate(invalid_pulse, context)
    
    assert "Sentence contradicts Business Pulse" in exc_info.value.details[0]

def test_response_validator_hallucination_rows():
    context = AIAnalysisContext(
        analysis_id=1,
        dataset_id=2,
        dataset_name="test.csv",
        dataset_type="Sales",
        dataset_domain="Business",
        rows_count=150,
        cols_count=5,
        missing_values_count=0,
        duplicate_rows_count=0,
        quality_score=100.0,
        business_pulse=95.0,
        health_label="READY"
    )

    validator = ResponseValidator()

    # Hallucinated row count (500 instead of 150)
    invalid_rows = "The dataset contains 500 records. Overall business pulse is 95.0."
    with pytest.raises(AIValidationException) as exc_info:
        validator.validate(invalid_rows, context)
    
    assert "Sentence contradicts row count" in exc_info.value.details[0]
