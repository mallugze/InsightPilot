from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, JSON
from datetime import datetime
from app.database.session import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    business_pulse = Column(Float, nullable=False)
    health_label = Column(String, nullable=False)
    pulse_breakdown = Column(JSON, nullable=True)
    kpis = Column(JSON, nullable=True)
    hero = Column(JSON, nullable=True)
    zero = Column(JSON, nullable=True)
    trends = Column(JSON, nullable=True)
    anomalies = Column(JSON, nullable=True)
    correlations = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    insights = Column(JSON, nullable=True)
    
    # Semantic fields
    semantic_profile = Column(JSON, nullable=True)
    dataset_domain = Column(String, nullable=True)
    entity = Column(String, nullable=True)
    feature_metadata = Column(JSON, nullable=True)
    relationship_metadata = Column(JSON, nullable=True)
    ml_readiness = Column(JSON, nullable=True)
    chart_suggestions = Column(JSON, nullable=True)
    kpi_suggestions = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "workspace_id": self.workspace_id,
            "dataset_id": self.dataset_id,
            "business_pulse": self.business_pulse,
            "health_label": self.health_label,
            "pulse_breakdown": self.pulse_breakdown,
            "kpis": self.kpis,
            "hero": self.hero,
            "zero": self.zero,
            "trends": self.trends,
            "anomalies": self.anomalies,
            "correlations": self.correlations,
            "recommendations": self.recommendations,
            "insights": self.insights,
            "semantic_profile": self.semantic_profile,
            "dataset_domain": self.dataset_domain,
            "entity": self.entity,
            "feature_metadata": self.feature_metadata,
            "relationship_metadata": self.relationship_metadata,
            "ml_readiness": self.ml_readiness,
            "chart_suggestions": self.chart_suggestions,
            "kpi_suggestions": self.kpi_suggestions,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
