from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.workspace import Workspace
from app.schemas.workspace import WorkspaceCreate, WorkspaceInDB, WorkspaceUpdate

router = APIRouter()

@router.post("/", response_model=WorkspaceInDB, status_code=status.HTTP_201_CREATED)
def create_workspace(workspace_in: WorkspaceCreate, db: Session = Depends(get_db)):
    """
    Creates a new Workspace associated with an anonymous session_id.
    """
    # Create new workspace db record
    db_workspace = Workspace(
        workspace_name=workspace_in.workspace_name,
        session_id=workspace_in.session_id
    )
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    return db_workspace

from app.models.workspace import Workspace, WorkspaceState

@router.get("/", response_model=List[WorkspaceInDB])
def get_workspaces(
    session_id: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    """
    Retrieves all workspaces. Can be filtered by query parameter session_id.
    """
    query = db.query(Workspace).filter(Workspace.status == WorkspaceState.READY)
    if session_id:
        query = query.filter(Workspace.session_id == session_id)
    return query.all()

@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workspace(workspace_id: int, db: Session = Depends(get_db)):
    """
    Deletes a specific workspace by ID.
    """
    db_workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not db_workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )
    db.delete(db_workspace)
    db.commit()
    return None
