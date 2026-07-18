from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

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
            "quality_score": getattr(analysis, "business_pulse", 100.0)
        }

class KPIProvider(BaseContextProvider):
    def provide(self, analysis: Any, dataset: Any) -> Dict[str, Any]:
        raw_kpis = getattr(analysis, "kpis", [])
        kpis_list = []
        if isinstance(raw_kpis, dict):
            kpis_list = raw_kpis.get("kpi_list", [])
        elif isinstance(raw_kpis, list):
            kpis_list = raw_kpis
            
        return {
            "kpis": kpis_list,
            "hero_metric": getattr(analysis, "hero", {}),
            "zero_metric": getattr(analysis, "zero", {})
        }

class TrendProvider(BaseContextProvider):
    def provide(self, analysis: Any, dataset: Any) -> Dict[str, Any]:
        raw_trends = getattr(analysis, "trends", [])
        trends_list = []
        if isinstance(raw_trends, dict):
            trends_list = raw_trends.get("trends", [])
        elif isinstance(raw_trends, list):
            trends_list = raw_trends
            
        raw_anomalies = getattr(analysis, "anomalies", [])
        anomalies_list = []
        if isinstance(raw_anomalies, dict):
            anomalies_list = raw_anomalies.get("anomaly_list", raw_anomalies.get("anomalies", []))
        elif isinstance(raw_anomalies, list):
            anomalies_list = raw_anomalies

        raw_correlations = getattr(analysis, "correlations", [])
        correlations_list = []
        if isinstance(raw_correlations, dict):
            correlations_list = raw_correlations.get("correlations", [])
        elif isinstance(raw_correlations, list):
            correlations_list = raw_correlations

        return {
            "trends": trends_list,
            "anomalies": anomalies_list,
            "correlations": correlations_list
        }

class RecommendationProvider(BaseContextProvider):
    def provide(self, analysis: Any, dataset: Any) -> Dict[str, Any]:
        raw_recommendations = getattr(analysis, "recommendations", [])
        recs_list = []
        if isinstance(raw_recommendations, dict):
            recs_list = raw_recommendations.get("recommendations", [])
        elif isinstance(raw_recommendations, list):
            recs_list = raw_recommendations

        raw_insights = getattr(analysis, "insights", [])
        insights_list = []
        if isinstance(raw_insights, list):
            for item in raw_insights:
                if isinstance(item, str):
                    insights_list.append({"text": item})
                else:
                    insights_list.append(item)
        elif isinstance(raw_insights, dict):
            insights_list = raw_insights.get("insights", [])

        return {
            "recommendations": recs_list,
            "insights": insights_list
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
