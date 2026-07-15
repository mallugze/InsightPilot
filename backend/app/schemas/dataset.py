from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.models.dataset import ProcessingState

class DatasetBase(BaseModel):
    filename: str
    original_filename: str
    dataset_type: str
    rows: int
    columns: int
    size_bytes: int
    status: ProcessingState
    missing_values: int
    duplicate_rows: int

class DatasetCreate(DatasetBase):
    workspace_id: Optional[int] = None
    session_id: Optional[str] = None
    first_5_rows_json: Optional[List[Dict[str, Any]]] = None
    column_metadata: Optional[Dict[str, Any]] = None

class DatasetUpdate(BaseModel):
    workspace_id: Optional[int] = None
    status: Optional[ProcessingState] = None

class DatasetInDB(DatasetBase):
    id: int
    workspace_id: Optional[int]
    session_id: Optional[str]
    uploaded_at: datetime
    first_5_rows_json: Optional[List[Dict[str, Any]]]
    column_metadata: Optional[Dict[str, Any]]

    model_config = ConfigDict(from_attributes=True)

class DatasetSummary(BaseModel):
    status: str = "success"
    dataset_id: int
    workspace_id: Optional[int] = None
    dataset_type: str
    rows: int
    columns: int
    missing_values: int
    duplicates: int
    preview: List[Dict[str, Any]]
    column_metadata: Dict[str, Any]
