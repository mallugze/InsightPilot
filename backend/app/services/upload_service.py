import os
import logging
from typing import Optional, Dict, Any
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.models.dataset import Dataset, ProcessingState
from app.services.storage_service import save_temp_file, cleanup_file
from app.services.validation_service import validate_file_metadata, load_and_validate_dataframe
from app.services.dataset_classifier import classify_dataset
from app.services.profiling_service import profile_dataset

logger = logging.getLogger("upload_service")

def process_dataset_upload(
    file: UploadFile, 
    session_id: str, 
    db: Session, 
    workspace_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Orchestrates the entire upload dataset ingestion pipeline:
    1. Validates size & extension
    2. Saves file temporarily
    3. Reads and parses with Pandas, executing integrity validations
    4. Automatically classifies dataset domain type
    5. Profiles data (categorical/numeric column flags, duplicates, nulls, quality score)
    6. Stores metadata inside the database
    """
    # Get file size using stream seek
    try:
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
    except Exception as e:
        logger.error(f"Failed to seek upload file stream: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not read the uploaded file stream size."
        )

    logger.info(f"Processing upload for '{file.filename}' (size: {file_size} bytes) for session {session_id}")

    # 1. Base Metadata Validation
    ext = validate_file_metadata(file.filename, file_size)

    # 2. Save file to temporary directory
    temp_file_path = save_temp_file(file, session_id)
    
    db_dataset = None
    try:
        # Update Workspace status to UPLOADING if workspace exists
        from app.models.workspace import Workspace, WorkspaceState
        if not workspace_id:
            # Check if there is an existing workspace for this session
            workspace = db.query(Workspace).filter(Workspace.session_id == session_id).first()
            if not workspace:
                # Create a default workspace for this session
                workspace = Workspace(
                    workspace_name="My Workspace",
                    session_id=session_id,
                    status=WorkspaceState.NEW
                )
                db.add(workspace)
                db.commit()
                db.refresh(workspace)
            workspace_id = workspace.id

        workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
        if workspace:
            workspace.status = WorkspaceState.UPLOADING
            db.add(workspace)
            db.commit()

        # Create database entry in VALIDATING state
        db_dataset = Dataset(
            workspace_id=workspace_id,
            session_id=session_id,
            filename=os.path.basename(temp_file_path),
            original_filename=file.filename,
            dataset_type="Unknown",
            rows=0,
            columns=0,
            size_bytes=file_size,
            status=ProcessingState.VALIDATING,
            missing_values=0,
            duplicate_rows=0,
            column_metadata={"columns": []}
        )
        db.add(db_dataset)
        db.commit()
        db.refresh(db_dataset)

        # 3. Load & Validate Pandas DataFrame
        df = load_and_validate_dataframe(temp_file_path, ext)

        # Update state to PROCESSING
        db_dataset.status = ProcessingState.PROCESSING
        db.commit()

        # 4. Classify dataset domain
        dataset_type = classify_dataset(list(df.columns))

        # 5. Profile dataset
        profile_results = profile_dataset(df, dataset_type)

        # 6. Save final profiled metadata inside the database and mark as READY
        db_dataset.dataset_type = dataset_type
        db_dataset.rows = profile_results["rows"]
        db_dataset.columns = profile_results["columns"]
        db_dataset.status = ProcessingState.READY
        db_dataset.first_5_rows_json = profile_results["first_5_rows_json"]
        db_dataset.missing_values = profile_results["missing_values"]
        db_dataset.duplicate_rows = profile_results["duplicate_rows"]
        db_dataset.column_metadata = profile_results["column_metadata"]
        db.commit()
        db.refresh(db_dataset)

        # Generate summary object
        summary = {
            "status": "success",
            "dataset_id": db_dataset.id,
            "workspace_id": db_dataset.workspace_id,
            "dataset_type": db_dataset.dataset_type,
            "rows": db_dataset.rows,
            "columns": db_dataset.columns,
            "missing_values": db_dataset.missing_values,
            "duplicates": db_dataset.duplicate_rows,
            "quality_score": profile_results["quality_score"],
            "preview": db_dataset.first_5_rows_json,
            "column_metadata": db_dataset.column_metadata
        }
        
        return summary

    except HTTPException as he:
        # Expected HTTP Validation Exceptions
        logger.error(f"HTTP Validation exception during upload processing: {he.detail}")
        if db_dataset:
            db_dataset.status = ProcessingState.FAILED
            db.commit()
        # Cleanup file on validation failure
        cleanup_file(temp_file_path)
        raise he
        
    except Exception as e:
        # Unexpected Internal Server Exceptions
        logger.exception("Unexpected error processing dataset upload")
        if db_dataset:
            db_dataset.status = ProcessingState.FAILED
            db.commit()
        # Cleanup file on failure
        cleanup_file(temp_file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected parsing error occurred: {str(e)}"
        )
