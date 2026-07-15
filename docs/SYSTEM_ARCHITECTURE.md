# System Architecture

*Content to be populated.*
# InsightPilot — System Architecture

Version: 0.1 Alpha

Status: Draft

Last Updated: July 2026

---

# 1. Overview

InsightPilot is an AI-powered Decision Intelligence Platform designed to transform raw business data into clear insights, actionable recommendations, and executive-ready reports.

Unlike traditional Business Intelligence platforms that primarily visualize data, InsightPilot combines statistical analysis with Large Language Models (LLMs) to explain business performance in natural language.

The architecture is designed to be modular, scalable, maintainable, and AI-first.

---

# 2. System Goals

The system should:

- Accept structured datasets (CSV, Excel)
- Automatically understand dataset type
- Perform statistical analysis
- Generate AI-powered executive summaries
- Recommend business actions
- Support conversational analytics
- Export executive reports
- Protect user data

---

# 3. High-Level Architecture

                Browser
                    │
                    ▼
          React + TypeScript Frontend
                    │
             REST API (FastAPI)
                    │
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
 Upload Engine   Analysis Engine   Chat Engine
                     │
                     ▼
             Insight Engine (LLM)
                     │
                     ▼
          Recommendation Engine
                     │
                     ▼
           Visualization Engine
                     │
                     ▼
             PostgreSQL Database
                     │
                     ▼
            Report Generation Engine

---

# 4. Technology Stack

## Frontend

- React
- TypeScript
- Tailwind CSS
- React Router
- Axios
- Recharts

---

## Backend

- FastAPI
- Python
- Pandas
- NumPy
- Pydantic

---

## AI Layer

- LLM Provider (Replaceable)
- Prompt Templates
- Business Insight Engine

---

## Database

- PostgreSQL

---

## Deployment

Development

- Local Machine
- Docker

Production (Future)

- AWS EC2
- AWS S3
- Nginx

---

# 5. Request Lifecycle

The following sequence describes the complete user journey after uploading a dataset.

User Uploads CSV

↓

Upload Engine validates file

↓

Dataset Profiling

↓

Data Cleaning

↓

Statistical Analysis

↓

Dataset Classification

↓

Visualization Selection

↓

Insight Generation

↓

Recommendation Generation

↓

Business Pulse Calculation

↓

Executive Brief Generation

↓

Dashboard Response

↓

Chat Ready

↓

Optional Report Generation

---

# 6. Backend Engines

InsightPilot is divided into independent processing engines.

Each engine has a single responsibility.

## Upload Engine

Responsible for

- CSV Upload
- Excel Upload
- File Validation
- File Size Check
- Column Validation

Output

Validated dataset

---

## Dataset Profiling Engine

Responsible for automatically identifying dataset type.

Examples

- Sales
- Finance
- Marketing
- HR
- Operations
- Generic

The detected profile influences

- Charts
- KPIs
- Recommendations
- Suggested Questions

---

## Analysis Engine

Pure statistical analysis.

No LLM usage.

Responsibilities

- Missing Value Analysis
- Descriptive Statistics
- Correlation
- Trend Detection
- Outlier Detection
- KPI Calculation

Output

Structured Business Metrics

---

## Insight Engine

Uses an LLM.

Transforms statistical outputs into human-readable insights.

Generates

- Executive Brief
- Business Pulse Explanation
- Key Insights

---

## Recommendation Engine

Responsible only for actions.

Example

Increase inventory.

Improve customer retention.

Reduce logistics costs.

Each recommendation includes

- Priority
- Business Reason
- Expected Impact
- AI Confidence

---

## Visualization Engine

Chooses appropriate visualizations.

Examples

Line Chart

Bar Chart

Pie Chart

Heatmap

Scatter Plot

Charts are selected automatically according to dataset profile.

---

## Chat Engine

Allows users to ask questions regarding uploaded datasets.

The engine receives

Dataset

+

Previous Analysis

+

Conversation History

Returns

Business-focused answers.

---

## Report Engine

Creates executive-ready reports.

Supported exports

- PDF
- Future: PowerPoint
- Future: Excel

---

# 7. AI Pipeline

The AI layer should never receive raw files directly.

Pipeline

Dataset

↓

Cleaning

↓

Statistical Analysis

↓

Business Metrics

↓

Insight Generation

↓

Recommendation Generation

↓

Business Pulse

↓

Dashboard

This architecture minimizes hallucinations by ensuring the LLM explains facts instead of calculating them.

---

# 8. Data Flow

User

↓

Frontend

↓

Upload API

↓

Validation

↓

Analysis Engine

↓

Insight Engine

↓

Recommendation Engine

↓

Database

↓

Frontend Dashboard

↓

Chat Engine

↓

Reports

---

# 9. Security Flow

Security is a core design principle.

Upload

↓

Validation

↓

Temporary Processing

↓

Analysis

↓

Results Stored

↓

Raw File Deleted (configurable)

All communication should occur over HTTPS in production.

Sensitive files should never be permanently stored unless explicitly requested by the user.

---

# 10. Database Responsibilities

The database stores

Users

Workspaces

Datasets

Analysis Results

Chat History

Generated Reports

Raw uploaded files are not intended for permanent storage.

---

# 11. Scalability Strategy

Future versions should support

- Authentication
- Multi-user collaboration
- Google Sheets integration
- SQL database connections
- Cloud storage
- Team workspaces
- Forecasting
- Scheduled reports

The architecture should allow new engines to be added without modifying existing components.

---

# 12. Error Handling

Every processing stage should return meaningful errors.

Examples

- Invalid file format
- Missing required columns
- Empty dataset
- Analysis failure
- AI service unavailable

Errors should be understandable by non-technical users.

---

# 13. Logging

Every analysis should create logs containing

- Analysis ID
- Dataset Name
- Upload Time
- Processing Time
- Model Used
- Errors
- Status

Logs support debugging and future analytics.

---

# 14. Design Principles

The architecture follows these principles

- Modular
- Explainable
- AI-first
- Secure
- Maintainable
- Scalable
- Replaceable AI Provider

Every component should have one clearly defined responsibility.

---

# 15. Future Architecture

Future releases may introduce

Authentication Service

Notification Service

Forecasting Engine

Integration Engine

Collaboration Engine

Plugin System

The existing architecture should support these additions without requiring major redesign.