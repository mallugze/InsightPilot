from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseContextProvider(ABC):
    """
    Abstract base class for modular context builders extracting facts
    from AnalysisResult and Dataset entities.
    """
    @abstractmethod
    def provide(self, analysis: Any, dataset: Any) -> Dict[str, Any]:
        pass

class DatasetProvider(BaseContextProvider):
    def provide(self, analysis: Any, dataset: Any) -> Dict[str, Any]:
        return {
            "rows_count": dataset.rows if dataset else 0,
            "cols_count": dataset.columns if dataset else 0,
            "missing_values_count": dataset.missing_values if dataset else 0,
            "duplicate_rows_count": dataset.duplicate_rows if dataset else 0,
            "quality_score": getattr(analysis, "business_pulse", 100.0)  # Default fallback or derived from dataset
        }

class KPIProvider(BaseContextProvider):
    def provide(self, analysis: Any, dataset: Any) -> Dict[str, Any]:
        return {
            "kpis": getattr(analysis, "kpis", []),
            "hero_metric": getattr(analysis, "hero", {}),
            "zero_metric": getattr(analysis, "zero", {})
        }

class TrendProvider(BaseContextProvider):
    def provide(self, analysis: Any, dataset: Any) -> Dict[str, Any]:
        return {
            "trends": getattr(analysis, "trends", []),
            "anomalies": getattr(analysis, "anomalies", []),
            "correlations": getattr(analysis, "correlations", [])
        }

class RecommendationProvider(BaseContextProvider):
    def provide(self, analysis: Any, dataset: Any) -> Dict[str, Any]:
        return {
            "recommendations": getattr(analysis, "recommendations", []),
            "insights": getattr(analysis, "insights", [])
        }

class ValidationProvider(BaseContextProvider):
    def provide(self, analysis: Any, dataset: Any) -> Dict[str, Any]:
        val_report = None
        if dataset and dataset.column_metadata:
            val_report = dataset.column_metadata.get("validation_report")
        return {
            "validation_report": val_report
        }

class DashboardProvider(BaseContextProvider):
    def provide(self, analysis: Any, dataset: Any) -> Dict[str, Any]:
        return {
            "chart_suggestions": getattr(analysis, "chart_suggestions", [])
        }

class MetadataProvider(BaseContextProvider):
    def provide(self, analysis: Any, dataset: Any) -> Dict[str, Any]:
        return {
            "dataset_name": dataset.original_filename if dataset else "Unknown File",
            "dataset_type": dataset.dataset_type if dataset else "Unknown",
            "dataset_domain": getattr(analysis, "dataset_domain", "Unknown"),
            "entity": getattr(analysis, "entity", "None"),
            "feature_metadata": getattr(analysis, "feature_metadata", []),
            "ml_readiness": getattr(analysis, "ml_readiness", {}),
            "kpi_suggestions": getattr(analysis, "kpi_suggestions", [])
        }
