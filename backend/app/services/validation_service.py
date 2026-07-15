import os
import pandas as pd
from fastapi import HTTPException, status
from typing import Tuple

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB
SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

def validate_file_metadata(filename: str, size_bytes: int) -> str:
    """
    Validates file extension and size before reading file.
    Returns the file extension in lowercase (e.g., '.csv').
    """
    # 1. Validate File Extension
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{ext}'. Only CSV, XLSX, and XLS files are allowed."
        )

    # 2. Validate Size Limit
    if size_bytes > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File is too large ({size_bytes / 1024 / 1024:.1f}MB). Maximum allowed size is 50MB."
        )
        
    if size_bytes == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty (0 bytes)."
        )
        
    return ext

def load_and_validate_dataframe(file_path: str, ext: str) -> pd.DataFrame:
    """
    Reads the file path into a Pandas DataFrame and validates data integrity.
    Returns a loaded DataFrame, or raises HTTP exceptions on errors.
    """
    try:
        if ext == ".csv":
            # Read CSV with fallback encodings
            try:
                df = pd.read_csv(file_path, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding="latin-1")
        else:
            # Excel files
            df = pd.read_excel(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The file could not be parsed. It may be corrupted or unreadable. Details: {str(e)}"
        )

    # 3. Check for empty dataframe (no rows or columns)
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded dataset is empty (has no rows or data)."
        )

    if len(df.columns) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The dataset does not contain any columns."
        )

    # 4. Check for blank or unnamed column headers
    # Unnamed columns in Pandas typically start with "Unnamed:"
    unnamed_cols = [c for c in df.columns if str(c).strip() == "" or str(c).startswith("Unnamed:")]
    if len(unnamed_cols) == len(df.columns):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The dataset is missing valid column headers."
        )

    # 5. Check for duplicate headers
    # Pandas automatically renames duplicate headers by appending .1, .2, etc.
    # We inspect if any column matches this renamed structure and check if its base exists.
    for col in df.columns:
        col_str = str(col).strip()
        parts = col_str.rsplit('.', 1)
        if len(parts) == 2 and parts[1].isdigit():
            base = parts[0]
            if base in df.columns:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"The dataset contains duplicate column headers: '{base}'."
                )

    return df
