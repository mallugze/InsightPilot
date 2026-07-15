from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any, List

class AnalysisResultBase(BaseModel):
    business_pulse: float
    health_label: str
    pulse_breakdown: Optional[Dict[str, Any]] = None
    kpis: Optional[Dict[str, Any]] = None
    hero: Optional[Dict[str, Any]] = None
    zero: Optional[Dict[str, Any]] = None
    trends: Optional[Dict[str, Any]] = None
    anomalies: Optional[Dict[str, Any]] = None
    correlations: Optional[Dict[str, Any]] = None
    recommendations: Optional[List[Dict[str, Any]]] = None
    insights: Optional[List[str]] = None

class AnalysisResultCreate(AnalysisResultBase):
    workspace_id: Optional[int] = None
    dataset_id: int

class AnalysisResultInDB(AnalysisResultBase):
    id: int
    workspace_id: Optional[int]
    dataset_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
