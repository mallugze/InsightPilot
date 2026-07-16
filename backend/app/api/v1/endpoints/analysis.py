from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any

from app.database.session import get_db
from app.schemas.analysis_result import AnalysisResultInDB
from app.analysis.analysis_service import run_dataset_analysis, get_cached_analysis
from app.models.dataset import Dataset
from app.models.analysis_result import AnalysisResult
from app.models.workspace import Workspace

router = APIRouter()

@router.get("/history", response_model=List[Dict[str, Any]])
def get_analysis_history(db: Session = Depends(get_db)):
    """
    Returns unified historical analysis results joined with dataset metadata.
    """
    from app.models.workspace import WorkspaceState
    results = (
        db.query(Dataset, AnalysisResult, Workspace)
        .join(AnalysisResult, Dataset.id == AnalysisResult.dataset_id)
        .join(Workspace, Dataset.workspace_id == Workspace.id)
        .filter(Workspace.status == WorkspaceState.READY)
        .order_by(Dataset.uploaded_at.desc())
        .all()
    )
    
    history_list = []
    for dataset, analysis, workspace in results:
        overall_conf = 0.50
        insights_count = 0
        domain = dataset.dataset_type
        
        if analysis:
            overall_conf = analysis.business_pulse / 100.0
            if analysis.semantic_profile:
                overall_conf = analysis.semantic_profile.get("overall_confidence", overall_conf)
                domain = analysis.semantic_profile.get("domain", domain)
            if analysis.insights:
                insights_count = len(analysis.insights)
                
        history_list.append({
            "dataset_id": dataset.id,
            "dataset_name": dataset.original_filename,
            "workspace_id": dataset.workspace_id,
            "workspace_name": workspace.workspace_name if workspace else "Default Workspace",
            "domain": domain,
            "upload_date": dataset.uploaded_at.isoformat() if dataset.uploaded_at else None,
            "business_pulse": analysis.business_pulse if analysis else None,
            "overall_confidence": overall_conf,
            "insights_count": insights_count,
            "status": dataset.status.value,
            "rows": dataset.rows,
            "columns": dataset.columns
        })
    return history_list

@router.post("/{dataset_id}", response_model=AnalysisResultInDB, status_code=status.HTTP_201_CREATED)
def trigger_analysis(dataset_id: int, db: Session = Depends(get_db)):
    """
    Executes the deterministic business metrics analytical pipeline for a dataset.
    Returns the computed and cached AnalysisResult.
    """
    return run_dataset_analysis(dataset_id=dataset_id, db=db)

@router.get("/{dataset_id}", response_model=AnalysisResultInDB)
def get_analysis_cache(dataset_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the cached business analysis reports for a dataset.
    """
    cached = get_cached_analysis(dataset_id=dataset_id, db=db)
    if not cached:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis report has not been generated for this dataset yet. Please run POST /api/v1/analyze/{dataset_id} first."
        )
    return cached
