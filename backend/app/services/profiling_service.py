import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Any

logger = logging.getLogger("profiling_service")

def detect_column_features(df: pd.DataFrame, col: str) -> Dict[str, Any]:
    """
    Analyzes a column's values and name to detect:
    is_numeric, is_categorical, is_date, is_primary_key, is_currency, is_percentage.
    Returns a dictionary of boolean attributes and count details.
    """
    series = df[col]
    dtype_str = str(series.dtype)
    col_lower = str(col).lower()
    
    unique_count = int(series.nunique(dropna=True))
    null_count = int(series.isnull().sum())
    total_rows = len(df)
    
    # 1. Base detections
    is_numeric = False
    is_categorical = False
    is_date = False
    is_primary_key = False
    is_currency = False
    is_percentage = False
    
    # Inferred Data Type (defaults to string)
    inferred_type = "string"

    # Numeric check
    if pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series):
        is_numeric = True
        inferred_type = "float" if "float" in dtype_str else "integer"
    
    # Categorical check: is_bool OR is_object/category with low cardinality
    if pd.api.types.is_bool_dtype(series):
        is_categorical = True
        inferred_type = "boolean"
    elif pd.api.types.is_categorical_dtype(series) or ((pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series)) and unique_count > 0):
        # Cardinally check: less than 15 unique values OR unique values take up less than 10% of dataset
        if unique_count <= 15 or (unique_count / total_rows < 0.1):
            is_categorical = True
            inferred_type = "categorical"
            
    # Date check
    if pd.api.types.is_datetime64_any_dtype(series):
        is_date = True
        inferred_type = "datetime"
    elif (pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series)) and unique_count > 0:
        # Sample non-null values to test date parsing speed
        non_null_samples = series.dropna().head(10)
        if len(non_null_samples) >= 3:
            try:
                parsed = pd.to_datetime(non_null_samples, errors='coerce')
                # If more than 80% of samples parsed successfully, mark as date candidate
                if parsed.notnull().sum() / len(non_null_samples) >= 0.8:
                    is_date = True
                    inferred_type = "datetime"
            except Exception:
                pass

    # 2. Currency check
    # Check column name keywords or if string elements contain currency symbols
    currency_keywords = {"price", "revenue", "cost", "spent", "profit", "fee", "amount", "budget", "salary", "wage", "currency"}
    if any(kw in col_lower for kw in currency_keywords):
        is_currency = True
    elif pd.api.types.is_object_dtype(series):
        sample_vals = series.dropna().head(10).astype(str)
        currency_symbols = {"$", "€", "£", "¥", "₹"}
        if any(any(sym in val for sym in currency_symbols) for val in sample_vals):
            is_currency = True
            
    # 3. Percentage check
    # Check column name keywords or if string elements contain '%' symbol
    pct_keywords = {"rate", "percentage", "pct", "ratio", "margin", "tax_rate", "discount_rate", "percent"}
    if any(kw in col_lower for kw in pct_keywords):
        is_percentage = True
    elif pd.api.types.is_object_dtype(series):
        sample_vals = series.dropna().head(10).astype(str)
        if any("%" in val for val in sample_vals):
            is_percentage = True

    # 4. Primary Key check
    # No null values, highly unique, and name looks like ID
    is_id_name = "id" in col_lower or "code" in col_lower or "key" in col_lower or "number" in col_lower
    if null_count == 0 and unique_count == total_rows:
        if is_id_name or is_numeric or inferred_type == "string":
            is_primary_key = True

    return {
        "name": col,
        "type": inferred_type,
        "original_dtype": dtype_str,
        "is_numeric": is_numeric,
        "is_categorical": is_categorical,
        "is_date": is_date,
        "is_primary_key": is_primary_key,
        "is_currency": is_currency,
        "is_percentage": is_percentage,
        "unique_values_count": unique_count,
        "null_values_count": null_count
    }

def profile_dataset(df: pd.DataFrame, dataset_type: str) -> Dict[str, Any]:
    """
    Profiles a pandas DataFrame.
    Returns a dictionary of:
    - rows, columns
    - missing_values, duplicate_rows
    - first_5_rows_json
    - column_metadata (structured schema details)
    - quality_score
    """
    rows = len(df)
    cols = len(df.columns)
    
    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())
    
    # 1. Quality Score computation
    total_cells = rows * cols
    dup_cells = duplicate_rows * cols
    raw_score = 100.0 * (1.0 - (missing_values + dup_cells) / (total_cells or 1))
    quality_score = round(max(0.0, min(100.0, raw_score)), 1)
    
    # 2. Extract column metadata
    columns_list = []
    for col in df.columns:
        col_features = detect_column_features(df, col)
        columns_list.append(col_features)
        
    column_metadata = {"columns": columns_list}
    
    # 3. Clean and extract first 5 rows (safely replace NaN with None for valid JSON serialization)
    clean_preview_df = df.head(5).where(pd.notnull(df), None)
    first_5_rows = clean_preview_df.to_dict(orient="records")
    
    return {
        "rows": rows,
        "columns": cols,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "quality_score": quality_score,
        "column_metadata": column_metadata,
        "first_5_rows_json": first_5_rows
    }
