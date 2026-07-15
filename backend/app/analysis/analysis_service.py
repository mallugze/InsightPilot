import os
import logging
import pandas as pd
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.dataset import Dataset
from app.models.analysis_result import AnalysisResult
from app.services.storage_service import TEMP_UPLOAD_DIR

# Import computational engines
from app.analysis.kpi_engine import calculate_kpis
from app.analysis.business_pulse import calculate_business_pulse
from app.analysis.hero_zero import detect_hero_zero
from app.analysis.trend_analysis import analyze_trends
from app.analysis.anomaly_detection import detect_anomalies
from app.analysis.correlation import analyze_correlations
from app.analysis.recommendation_engine import generate_recommendations
from app.analysis.insight_engine import generate_insights

logger = logging.getLogger("analysis_service")

def get_cached_analysis(dataset_id: int, db: Session) -> Optional[AnalysisResult]:
    """
    Retrieves the cached AnalysisResult for a dataset if it exists.
    """
    return db.query(AnalysisResult).filter(AnalysisResult.dataset_id == dataset_id).first()

def load_dataframe_from_dataset(dataset: Dataset) -> pd.DataFrame:
    """
    Resolves the temp upload path for a dataset and loads it into a Pandas DataFrame.
    Keeps I/O logic modular and isolated.
    """
    file_path = os.path.join(TEMP_UPLOAD_DIR, dataset.filename)
    if not os.path.exists(file_path):
        # Retry looking in backend/temp_uploads directly if relative path shifted
        fallback_path = os.path.abspath(os.path.join(os.getcwd(), "temp_uploads", dataset.filename))
        if os.path.exists(fallback_path):
            file_path = fallback_path
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Original dataset file '{dataset.original_filename}' was not found in temporary uploads."
            )
            
    _, ext = os.path.splitext(dataset.filename)
    ext = ext.lower()
    
    try:
        if ext == ".csv":
            try:
                df = pd.read_csv(file_path, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding="latin-1")
        else:
            df = pd.read_excel(file_path)
        return df
    except Exception as e:
        logger.error(f"Error loading temporary dataset file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not load dataset file for analysis. Details: {str(e)}"
        )

def run_dataset_analysis(dataset_id: int, db: Session) -> AnalysisResult:
    """
    Executes the analytical pipeline for a dataset:
    - Checks database cache first
    - Loads the temporary raw file into memory
    - Calculates semantic KPIs, health pulse, hero/zero bounds, trend timelines, correlations, anomalies, recommendations, and insights
    - Saves the results and returns them
    """
    # 1. Check cache first
    cached = get_cached_analysis(dataset_id, db)
    if cached:
        logger.info(f"Returning cached analysis result for dataset ID {dataset_id}")
        return cached

    # 2. Fetch dataset model record
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
        
    logger.info(f"Running analytical profiling on dataset ID {dataset_id} ({dataset.original_filename})")

    # 3. Load DataFrame (I/O abstraction)
    df = load_dataframe_from_dataset(dataset)
    col_metadata = dataset.column_metadata or {"columns": []}
    dataset_type = dataset.dataset_type

    # 4. Run computational sub-engines
    kpis = calculate_kpis(df, dataset_type, col_metadata)
    pulse = calculate_business_pulse(df, dataset_type, col_metadata, kpis)
    hero_zero = detect_hero_zero(df, col_metadata)
    trends = analyze_trends(df, col_metadata)
    anomalies = detect_anomalies(df, col_metadata)
    correlations = analyze_correlations(df, col_metadata)
    recommendations = generate_recommendations(dataset_type, kpis, pulse, trends, anomalies, correlations)
    insights = generate_insights(dataset_type, kpis, pulse, trends, anomalies, correlations, hero_zero)

    # 5. Run Semantic Understanding Engine
    from app.analysis.semantic.semantic_builder import build_semantic_profile
    sem_profile = build_semantic_profile(df, col_metadata)

    # 6. Save and Cache the analysis results
    analysis_result = AnalysisResult(
        workspace_id=dataset.workspace_id,
        dataset_id=dataset.id,
        business_pulse=pulse["score"],
        health_label=pulse["health_label"],
        pulse_breakdown=pulse["breakdown"],
        kpis=kpis,
        hero=hero_zero,
        zero=hero_zero,  # Hero and zero combined inside hero_zero dict for simple caching
        trends=trends,
        anomalies=anomalies,
        correlations=correlations,
        recommendations=recommendations,
        insights=insights,
        semantic_profile=sem_profile,
        dataset_domain=sem_profile["domain"],
        entity=sem_profile["entity"],
        feature_metadata=sem_profile["features"],
        relationship_metadata=sem_profile["relationships"],
        ml_readiness=sem_profile["ml_readiness"],
        chart_suggestions=sem_profile["visualization_intent"],
        kpi_suggestions=sem_profile["kpi_suggestions"]
    )
    
    try:
        # Auto-rename associated Workspace
        from app.models.workspace import Workspace
        if dataset.workspace_id:
            workspace = db.query(Workspace).filter(Workspace.id == dataset.workspace_id).first()
            if workspace:
                workspace.workspace_name = sem_profile.get("suggested_workspace_name", workspace.workspace_name)
                db.add(workspace)
                
        db.add(analysis_result)
        db.commit()
        db.refresh(analysis_result)
        logger.info(f"Successfully calculated and cached analysis report for dataset {dataset_id}")
        return analysis_result
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to cache analysis result: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save analysis report to database."
        )
