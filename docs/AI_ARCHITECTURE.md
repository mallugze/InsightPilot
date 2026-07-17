# AI Foundation & Context Architecture

This document describes the AI architecture of the InsightPilot Decision Intelligence Platform.

## System Architecture

InsightPilot separates statistical analytics (deterministic engine) from generative reasoning and explanation (generative AI engine). 

```
                                  +-----------------------+
                                  |   Uploaded Dataset    |
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------+-----------+
                                  |  Ingestion & Profiler |
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------+-----------+
                                  |   SQL DB (PostgreSQL) |
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------+-----------+
                                  |  AI Context Builder   |
                                  +-----------+-----------+
                                              |
                     +------------------------+-----------------------+
                     | (Prompt Template)                              | (Context Hashed)
                     v                                                v
          +----------+----------+                           +---------+---------+
          |    Prompt Manager   |                           |     AI Cache      |
          +----------+----------+                           +---------+---------+
                     |                                                |
                     +------------------------+-----------------------+
                                              |
                                              v
                                  +-----------+-----------+
                                  |   Gemini Service /    |
                                  |   LLM Abstraction     |
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------+-----------+
                                  |   Response Validator  |
                                  +-----------+-----------+
                                              |
                     +------------------------+-----------------------+
                     |                                                |
                     v                                                v
          +----------+----------+                           +---------+---------+
          |   Citation Builder  |                           |Conversation Memory|
          +---------------------+                           +-------------------+
```

### Core Tenets

1. **Deterministic Single Source of Truth:** The backend performs all math, aggregates, anomalies, and correlations. The AI model is strictly prohibited from executing statistical computations or inventing parameters.
2. **Contextual Reasoning:** All LLM prompts are populated with structural context metadata (`AIAnalysisContext`) generated directly from PostgreSQL facts.
3. **Hallucination Prevention:** The validator reviews response claims against context bounds before delivery. If contradictions are found, they are blocked.
4. **Explainable AI:** Responses are parsed and linked to source engines via citations.

---

## Component Specifications

### 1. Context Builder & Providers
Located in `app/services/ai/context_builder.py`. Composed of modular context providers:
- `DatasetProvider`: Extracts row/col counts, missing values, duplicates, and quality parameters.
- `KPIProvider`: Extracts aggregate key indicators and hero/zero metrics.
- `TrendProvider`: Gathers computed linear trend slopes, correlation pairs, and anomaly outliers.
- `RecommendationProvider`: Gathers recommended actions and operational insights.
- `ValidationProvider`: Ingests dataset ingestion reports (encoding, delimiter state).
- `DashboardProvider`: Captures layout suggestions and intents.
- `MetadataProvider`: Ingests column types and classifications.

### 2. Provider Abstraction for LLM Integrations
Located in `app/services/ai/gemini_service.py`. Extends `BaseLLMProvider` using the Google Generative AI APIs. Falls back to local deterministic responses when API configuration keys are absent.

### 3. Prompt Manager
Located in `app/services/ai/prompt_manager.py`. Reads parameterized text templates from `prompts/` and manages variable rendering.

### 4. Cache Engine & Memory Repositories
- `AICache`: Hashes the compiled context payload (SHA-256) together with prompt signatures to ensure cache validity.
- `ConversationMemoryManager`: Manages chat logs, persisting conversations to PostgreSQL tables (`ai_conversations`/`ai_chat_messages`) with automatic thread-safe in-memory fallbacks.
