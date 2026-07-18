import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Dict, Any, List

from app.models.analysis_result import AnalysisResult
from app.models.dataset import Dataset
from app.services.ai.models import AIAnalysisContext
from app.services.ai.context_providers import (
    BaseContextProvider,
    DatasetProvider,
    KPIProvider,
    TrendProvider,
    RecommendationProvider,
    ValidationProvider,
    DashboardProvider,
    MetadataProvider
)

logger = logging.getLogger("context_builder")

class ContextBuilder:
    """
    Assembles modular context providers to build a unified AIAnalysisContext.
    """
    def __init__(self):
        self.providers: List[BaseContextProvider] = [
            DatasetProvider(),
            KPIProvider(),
            TrendProvider(),
            RecommendationProvider(),
            ValidationProvider(),
            DashboardProvider(),
            MetadataProvider()
        ]
        logger.info(f"ContextBuilder initialized with {len(self.providers)} providers.")

    def build_context(self, analysis_id: int, db: Session) -> AIAnalysisContext:
        logger.info(f"Building AI context for analysis ID: {analysis_id}")
        
        # 1. Query database for AnalysisResult
        analysis = db.query(AnalysisResult).filter(
            (AnalysisResult.id == analysis_id) | (AnalysisResult.dataset_id == analysis_id)
        ).first()
        if not analysis:
            logger.error(f"Analysis result ID {analysis_id} not found in database.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Analysis result ID {analysis_id} was not found."
            )
            
        # 2. Query database for corresponding Dataset
        dataset = db.query(Dataset).filter(Dataset.id == analysis.dataset_id).first()
        if not dataset:
            logger.warning(f"Associated Dataset ID {analysis.dataset_id} not found for analysis {analysis_id}.")

        # 3. Aggregate provider context
        context_data: Dict[str, Any] = {
            "analysis_id": analysis.id,
            "dataset_id": analysis.dataset_id,
            "workspace_id": analysis.workspace_id,
            "business_pulse": analysis.business_pulse,
            "health_label": analysis.health_label,
            "pulse_breakdown": analysis.pulse_breakdown
        }

        for provider in self.providers:
            provider_name = provider.__class__.__name__
            try:
                logger.debug(f"Executing context provider: {provider_name}")
                chunk = provider.provide(analysis, dataset)
                context_data.update(chunk)
            except Exception as e:
                logger.error(f"Error executing provider {provider_name}: {str(e)}")
                # Continue other providers to be resilient

        logger.info(f"Successfully compiled AI context for analysis ID {analysis_id}")
        return AIAnalysisContext(**context_data)
