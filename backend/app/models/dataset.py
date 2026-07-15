import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Enum
from datetime import datetime
from app.database.session import Base

class ProcessingState(str, enum.Enum):
    UPLOADING = "UPLOADING"
    VALIDATING = "VALIDATING"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=True)
    session_id = Column(String, nullable=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    dataset_type = Column(String, nullable=False)
    rows = Column(Integer, nullable=False)
    columns = Column(Integer, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(Enum(ProcessingState), default=ProcessingState.READY, nullable=False)
    first_5_rows_json = Column(JSON, nullable=True)
    missing_values = Column(Integer, default=0, nullable=False)
    duplicate_rows = Column(Integer, default=0, nullable=False)
    column_metadata = Column(JSON, nullable=True)  # Store column schema and data types

    def to_dict(self):
        return {
            "id": self.id,
            "workspace_id": self.workspace_id,
            "session_id": self.session_id,
            "filename": self.filename,
            "original_filename": self.original_filename,
            "dataset_type": self.dataset_type,
            "rows": self.rows,
            "columns": self.columns,
            "size_bytes": self.size_bytes,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
            "status": self.status.value,
            "first_5_rows_json": self.first_5_rows_json,
            "missing_values": self.missing_values,
            "duplicate_rows": self.duplicate_rows,
            "column_metadata": self.column_metadata,
        }
