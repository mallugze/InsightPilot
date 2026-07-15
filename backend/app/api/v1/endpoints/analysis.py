from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database.session import get_db
from app.schemas.analysis_result import AnalysisResultInDB
from app.analysis.analysis_service import run_dataset_analysis, get_cached_analysis

router = APIRouter()

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
