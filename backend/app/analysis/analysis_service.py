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
            
        # Coerce column data types based on validation profile to eliminate mixed type crashes
        col_metadata = dataset.column_metadata or {"columns": []}
        for col_info in col_metadata.get("columns", []):
            col_name = col_info.get("name")
            if col_name in df.columns:
                if col_info.get("is_numeric") or col_info.get("type") in ["integer", "float"]:
                    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
                elif col_info.get("is_date") or col_info.get("type") == "datetime":
                    df[col_name] = pd.to_datetime(df[col_name], errors='coerce')
                    
        return df
    except Exception as e:
        logger.error(f"Error loading temporary dataset file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not load dataset file for analysis. Details: {str(e)}"
        )

def serialize_pandas_objects(obj):
    """
    Recursively converts Pandas/NumPy objects (like Timestamp or np.int64) 
    into standard Python JSON-serializable types.
    """
    if isinstance(obj, dict):
        return {k: serialize_pandas_objects(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_pandas_objects(v) for v in obj]
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif hasattr(obj, "item") and hasattr(obj, "dtype"):  # Convert NumPy scalars to native Python types
        try:
            return obj.item()
        except Exception:
            return str(obj)
    elif not isinstance(obj, (dict, list, str)) and pd.isna(obj):
        return None
    return obj

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

    # Ensure dataset is associated with a workspace
    from app.models.workspace import Workspace, WorkspaceState
    if not dataset.workspace_id:
        # Check if there is an existing workspace for this session
        workspace = db.query(Workspace).filter(Workspace.session_id == dataset.session_id).first()
        if not workspace:
            # Create a default workspace for this session
            workspace = Workspace(
                workspace_name="My Workspace",
                session_id=dataset.session_id,
                status=WorkspaceState.NEW
            )
            db.add(workspace)
            db.commit()
            db.refresh(workspace)
        dataset.workspace_id = workspace.id
        db.add(dataset)
        db.commit()
        db.refresh(dataset)

    # Update Workspace status to ANALYZING
    if dataset.workspace_id:
        workspace = db.query(Workspace).filter(Workspace.id == dataset.workspace_id).first()
        if workspace:
            workspace.status = WorkspaceState.ANALYZING
            db.add(workspace)
            db.commit()

    # 3. Load DataFrame (I/O abstraction)
    df = load_dataframe_from_dataset(dataset)
    col_metadata = dataset.column_metadata or {"columns": []}
    dataset_type = dataset.dataset_type

    try:
        # 4. Run Semantic Understanding Engine upstream
        from app.analysis.semantic.semantic_builder import build_semantic_profile
        sem_profile = build_semantic_profile(df, col_metadata)
        inferred_domain = sem_profile.get("domain", dataset_type)

        # 5. Dynamic KPI selection based on inferred domain
        if inferred_domain in ["Business", "Sales", "Retail Analytics"]:
            kpis = calculate_kpis(df, "Sales", col_metadata)
        elif inferred_domain in ["HR", "Human Resources"]:
            kpis = calculate_kpis(df, "HR", col_metadata)
        elif inferred_domain in ["Finance", "Financial Intelligence", "Financial"]:
            kpis = calculate_kpis(df, "Finance", col_metadata)
        else:
            from app.analysis.semantic.kpi_discovery import calculate_discovered_kpis
            kpis = calculate_discovered_kpis(df, sem_profile.get("kpi_suggestions", []))

        pulse = calculate_business_pulse(df, inferred_domain, col_metadata, kpis)
        hero_zero = detect_hero_zero(df, col_metadata)
        trends = analyze_trends(df, col_metadata)
        anomalies = detect_anomalies(df, col_metadata)
        correlations = analyze_correlations(df, col_metadata)
        
        recommendations = generate_recommendations(inferred_domain, kpis, pulse, trends, anomalies, correlations)
        insights = generate_insights(inferred_domain, kpis, pulse, trends, anomalies, correlations, hero_zero)

        import json
        if dataset.first_5_rows_json:
            try:
                sem_profile["first_5_rows"] = json.loads(dataset.first_5_rows_json)
            except Exception:
                sem_profile["first_5_rows"] = df.head(5).to_dict(orient="records")
        else:
            sem_profile["first_5_rows"] = df.head(5).to_dict(orient="records")

        # Clean Pandas and NumPy objects to guarantee JSON-serializability
        kpis = serialize_pandas_objects(kpis)
        hero_zero = serialize_pandas_objects(hero_zero)
        trends = serialize_pandas_objects(trends)
        anomalies = serialize_pandas_objects(anomalies)
        correlations = serialize_pandas_objects(correlations)
        recommendations = serialize_pandas_objects(recommendations)
        insights = serialize_pandas_objects(insights)
        sem_profile = serialize_pandas_objects(sem_profile)

        # 6. Save and Cache the analysis results (Idempotent update/insert)
        existing_result = db.query(AnalysisResult).filter(AnalysisResult.dataset_id == dataset.id).first()
        if existing_result:
            existing_result.workspace_id = dataset.workspace_id
            existing_result.business_pulse = pulse["score"]
            existing_result.health_label = pulse["health_label"]
            existing_result.pulse_breakdown = pulse["breakdown"]
            existing_result.kpis = kpis
            existing_result.hero = hero_zero
            existing_result.zero = hero_zero
            existing_result.trends = trends
            existing_result.anomalies = anomalies
            existing_result.correlations = correlations
            existing_result.recommendations = recommendations
            existing_result.insights = insights
            existing_result.semantic_profile = sem_profile
            existing_result.dataset_domain = sem_profile["domain"]
            existing_result.entity = sem_profile["entity"]
            existing_result.feature_metadata = sem_profile["features"]
            existing_result.relationship_metadata = sem_profile["relationships"]
            existing_result.ml_readiness = sem_profile["ml_readiness"]
            existing_result.chart_suggestions = sem_profile["visualization_intent"]
            existing_result.kpi_suggestions = sem_profile["kpi_suggestions"]
            analysis_result = existing_result
        else:
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
        
        # Auto-rename associated Workspace and mark status as READY
        if dataset.workspace_id:
            workspace = db.query(Workspace).filter(Workspace.id == dataset.workspace_id).first()
            if workspace:
                workspace.workspace_name = sem_profile.get("suggested_workspace_name", workspace.workspace_name)
                workspace.status = WorkspaceState.READY
                db.add(workspace)
                
        try:
            db.add(analysis_result)
            db.commit()
            db.refresh(analysis_result)
            logger.info(f"Successfully calculated and cached analysis report for dataset {dataset_id}")
            return analysis_result
        except Exception as commit_error:
            db.rollback()
            logger.warning(f"Commit conflict for dataset {dataset_id}, fetching existing AnalysisResult: {str(commit_error)}")
            existing = db.query(AnalysisResult).filter(AnalysisResult.dataset_id == dataset.id).first()
            if existing:
                # Also ensure the workspace status is set to READY
                if dataset.workspace_id:
                    workspace = db.query(Workspace).filter(Workspace.id == dataset.workspace_id).first()
                    if workspace and workspace.status != WorkspaceState.READY:
                        workspace.status = WorkspaceState.READY
                        db.add(workspace)
                        db.commit()
                return existing
            raise commit_error

    except Exception as e:
        logger.exception(f"Unexpected exception during dataset analysis pipeline for dataset ID {dataset_id}")
        db.rollback()
        
        # Update dataset status to FAILED, reset workspace status to NEW
        from app.models.dataset import ProcessingState
        dataset.status = ProcessingState.FAILED
        if dataset.workspace_id:
            workspace = db.query(Workspace).filter(Workspace.id == dataset.workspace_id).first()
            if workspace:
                workspace.status = WorkspaceState.NEW
                db.add(workspace)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis pipeline execution failed: {str(e)}"
        )
