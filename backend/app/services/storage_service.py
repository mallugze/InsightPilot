import os
import shutil
import time
import logging
from fastapi import UploadFile

logger = logging.getLogger("storage_service")

# Base directory for temporary uploads
TEMP_UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "temp_uploads"))

def ensure_temp_dir():
    if not os.path.exists(TEMP_UPLOAD_DIR):
        os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)

def save_temp_file(file: UploadFile, session_id: str) -> str:
    """
    Saves an UploadFile temporarily to disk.
    Returns the absolute path to the saved file.
    """
    ensure_temp_dir()
    # Generate unique filename using timestamp and session_id
    timestamp = int(time.time())
    safe_filename = f"{session_id}_{timestamp}_{file.filename}"
    file_path = os.path.join(TEMP_UPLOAD_DIR, safe_filename)
    
    logger.info(f"Saving temporary upload: {file.filename} -> {file_path}")
    
    # Save the file using chunks
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
        
    return file_path

def cleanup_file(file_path: str):
    """
    Deletes a specific file from the temporary directory.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up temporary file: {file_path}")
    except Exception as e:
        logger.error(f"Error cleaning up file {file_path}: {str(e)}")

def cleanup_expired_files(max_age_seconds: int = 86400):
    """
    Deletes temporary files older than the specified max age in seconds (default 24h).
    """
    if not os.path.exists(TEMP_UPLOAD_DIR):
        return
        
    now = time.time()
    logger.info(f"Running expiration cleanup in {TEMP_UPLOAD_DIR} (max age: {max_age_seconds}s)")
    
    for filename in os.listdir(TEMP_UPLOAD_DIR):
        file_path = os.path.join(TEMP_UPLOAD_DIR, filename)
        if os.path.isfile(file_path):
            try:
                # Check modification time
                mtime = os.path.getmtime(file_path)
                if now - mtime > max_age_seconds:
                    os.remove(file_path)
                    logger.info(f"Expired and removed temporary file: {filename}")
            except Exception as e:
                logger.error(f"Error removing expired file {filename}: {str(e)}")
