# Prompt Guide & Templates

This document details prompt templates used by the InsightPilot generative analytics pipeline.

## Template Registry

All templates are text files located under `backend/app/services/ai/prompts/`.

### 1. Executive Summary (`executive_summary.txt`)
- **Purpose:** Composes high-level business narratives for the executive view.
- **Variables:**
  - `{business_pulse}`: Overall computed score.
  - `{health_label}`: Overall health string state.
  - `{rows_count}`: Number of rows.
  - `{cols_count}`: Number of columns.
  - `{hero_metric}`: Highest performing KPI metric details.
  - `{zero_metric}`: Underperforming metric details.
  - `{context}`: Serialized JSON dataset metrics.

### 2. Business Analyst (`business_analyst.txt`)
- **Purpose:** Composes deeper explanations describing trend drivers, correlation dynamics, and recommendations.
- **Variables:**
  - `{context}`: Serialized JSON dataset metrics.
  - `{recommendations}`: Context decision-making suggestions list.

### 3. Dashboard Chat (`dashboard_chat.txt`)
- **Purpose:** Backs conversational workspace query interfaces.
- **Variables:**
  - `{question}`: User query input prompt.
  - `{context}`: Serialized JSON dataset metrics.

### 4. Executive Report (`executive_report.txt`)
- **Purpose:** Generates structured report objects.
- **Variables:**
  - `{context}`: Serialized JSON dataset metrics.
- **Expected Return JSON Fields:**
  - `executive_summary`
  - `business_health`
  - `key_findings` (array)
  - `critical_risks` (array)
  - `growth_opportunities` (array)
  - `recommendations` (array)
  - `action_items` (array)

### 5. Forecast Explainer (`forecast_explainer.txt`)
- **Purpose:** Explains forecasts and prediction readiness metrics.
- **Variables:**
  - `{context}`: Serialized JSON dataset metrics.

### 6. Dataset Summary (`dataset_summary.txt`)
- **Purpose:** Explains the schema, identity, and raw layout metadata.
- **Variables:**
  - `{context}`: Serialized JSON dataset metrics.

---

## Design Principles

1. **Deterministic Containment:** Prompts must instruct models to only formulate statements containing numbers present in the context.
2. **Context Separation:** Always inject context variables separately. Avoid mingling template logic with raw data dumps.
3. **No Math:** Instruct the model to explain and summarize, never calculate.
