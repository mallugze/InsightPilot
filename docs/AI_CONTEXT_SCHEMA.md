# AI Context Schema Specification

This document specifies the fields and schemas of the `AIAnalysisContext` Python object.

## Schema Details (`AIAnalysisContext`)

The compiled context contains the following properties:

| Property | Type | Description |
| :--- | :--- | :--- |
| `context_version` | `str` | Version identifier of the context object format (e.g. `1.0.0`) |
| `analysis_id` | `int` | Primary key of the analysis results entry in PostgreSQL |
| `dataset_id` | `int` | Primary key of the dataset entry in PostgreSQL |
| `workspace_id` | `Optional[int]` | Owning workspace ID |
| `dataset_name` | `str` | Original filename uploaded by the user |
| `dataset_type` | `str` | Classification category (e.g., 'Retail', 'Sensor', 'Iris') |
| `dataset_domain` | `str` | Top-level semantic classification domain (e.g., 'Business', 'Scientific') |
| `entity` | `Optional[str]` | Detected row entity (e.g., 'Transaction', 'Species') |
| `rows_count` | `int` | Number of rows parsed in the dataset |
| `cols_count` | `int` | Number of columns parsed in the dataset |
| `missing_values_count` | `int` | Count of empty cells in the dataset |
| `duplicate_rows_count` | `int` | Count of duplicate rows in the dataset |
| `quality_score` | `float` | Ingestion quality score derived from duplicates and empty cells |
| `validation_report` | `Optional[dict]` | Encoding, delimiter, warnings, and recommended corrections |
| `business_pulse` | `float` | Overall computed health rating score (0 - 100) |
| `health_label` | `str` | Categorical health state (e.g., 'READY', 'WARNING') |
| `pulse_breakdown` | `Optional[dict]` | Score breakdown (quality, completeness, consistency) |
| `kpis` | `Optional[list]` | Evaluated key indicators (name, value, unit, change rate) |
| `hero_metric` | `Optional[dict]` | Highest performing KPI |
| `zero_metric` | `Optional[dict]` | Lowest performing KPI |
| `trends` | `Optional[list]` | Segment trends, regression slopes, and intervals |
| `anomalies` | `Optional[list]` | Identified outliers |
| `correlations` | `Optional[list]` | Correlation coefficient pairs |
| `recommendations` | `Optional[list]` | Decision suggestions |
| `insights` | `Optional[list]` | General data insights |
| `feature_metadata` | `Optional[list]` | Column types, constraints, and statistical summaries |
| `ml_readiness` | `Optional[dict]` | ML preparation metrics and predictions confidence |
| `chart_suggestions` | `Optional[list]` | Visualization intents and visual types |
| `kpi_suggestions` | `Optional[list]` | Sugggested additional KPIs, formulas, and reasoning |

---

## Example Schema Object

```json
{
  "context_version": "1.0.0",
  "analysis_id": 12,
  "dataset_id": 5,
  "workspace_id": 2,
  "dataset_name": "sales_metrics.csv",
  "dataset_type": "Sales",
  "dataset_domain": "Business",
  "rows_count": 150,
  "cols_count": 5,
  "missing_values_count": 0,
  "duplicate_rows_count": 0,
  "quality_score": 100.0,
  "business_pulse": 93.3,
  "health_label": "READY",
  "pulse_breakdown": {
    "quality": 100.0,
    "completeness": 95.0,
    "consistency": 90.0
  },
  "kpis": [
    {
      "name": "revenue_usd",
      "value": 750.75,
      "aggregation": "sum"
    }
  ],
  "validation_report": {
    "encoding": "utf-8",
    "delimiter": ",",
    "validation_status": "success",
    "warnings": [],
    "recommended_fixes": []
  }
}
```
