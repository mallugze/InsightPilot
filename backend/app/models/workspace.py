import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from app.database.session import Base

class WorkspaceState(str, enum.Enum):
    NEW = "NEW"
    UPLOADING = "UPLOADING"
    ANALYZING = "ANALYZING"
    READY = "READY"
    ARCHIVED = "ARCHIVED"

class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    workspace_name = Column(String, nullable=False)
    session_id = Column(String, nullable=False, index=True)
    status = Column(Enum(WorkspaceState), default=WorkspaceState.NEW, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "workspace_name": self.workspace_name,
            "session_id": self.session_id,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
