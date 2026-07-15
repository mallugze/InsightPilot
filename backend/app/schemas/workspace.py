from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class WorkspaceBase(BaseModel):
    workspace_name: str

class WorkspaceCreate(WorkspaceBase):
    session_id: str

class WorkspaceUpdate(BaseModel):
    workspace_name: str

class WorkspaceInDB(WorkspaceBase):
    id: int
    session_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
