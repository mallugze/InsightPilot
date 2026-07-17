from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class Citation(BaseModel):
    sentence: str = Field(description="The statement or claim referenced from LLM output")
    source: str = Field(description="The source engine (e.g. 'KPI Engine', 'Business Pulse')")
    details: str = Field(description="Explainable backend metrics or facts supporting the source citation")

class AIAnalysisContext(BaseModel):
    context_version: str = "1.0.0"
    analysis_id: int
    dataset_id: int
    workspace_id: Optional[int] = None
    dataset_name: str
    dataset_type: str
    dataset_domain: str
    entity: Optional[str] = None
    
    # Ingestion & Quality metrics
    rows_count: int
    cols_count: int
    missing_values_count: int
    duplicate_rows_count: int
    quality_score: float
    validation_report: Optional[Dict[str, Any]] = None
    
    # Analytics Facts
    business_pulse: float
    health_label: str
    pulse_breakdown: Optional[Dict[str, Any]] = None
    kpis: Optional[List[Dict[str, Any]]] = None
    hero_metric: Optional[Dict[str, Any]] = None
    zero_metric: Optional[Dict[str, Any]] = None
    trends: Optional[List[Dict[str, Any]]] = None
    anomalies: Optional[List[Dict[str, Any]]] = None
    correlations: Optional[List[Dict[str, Any]]] = None
    recommendations: Optional[List[Dict[str, Any]]] = None
    insights: Optional[List[Dict[str, Any]]] = None
    
    # Semantic & Readiness Suggestion models
    feature_metadata: Optional[List[Dict[str, Any]]] = None
    ml_readiness: Optional[Dict[str, Any]] = None
    chart_suggestions: Optional[List[Dict[str, Any]]] = None
    kpi_suggestions: Optional[List[Dict[str, Any]]] = None

class AIReport(BaseModel):
    executive_summary: str
    business_health: str
    key_findings: List[str]
    critical_risks: List[str]
    growth_opportunities: List[str]
    recommendations: List[str]
    action_items: List[str]
