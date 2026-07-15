from fastapi import APIRouter, Depends, UploadFile, File, Form, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.session import get_db
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetInDB, DatasetSummary
from app.services.upload_service import process_dataset_upload

router = APIRouter()

@router.post("/upload", response_model=DatasetSummary, status_code=status.HTTP_201_CREATED)
def upload_dataset(
    file: UploadFile = File(...),
    workspace_id: Optional[int] = Form(None),
    x_session_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Upload and ingest a dataset file (CSV, XLSX, XLS).
    Validates data headers, size boundaries, classification categories, and creates database records.
    """
    if not x_session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Header 'X-Session-ID' is required."
        )
        
    return process_dataset_upload(
        file=file,
        session_id=x_session_id,
        db=db,
        workspace_id=workspace_id
    )

@router.get("/datasets/{workspace_id}", response_model=List[DatasetInDB])
def get_workspace_datasets(
    workspace_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieves all datasets metadata processed for a specific workspace.
    """
    datasets = db.query(Dataset).filter(Dataset.workspace_id == workspace_id).all()
    return datasets
