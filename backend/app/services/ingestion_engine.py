import os
import re
import csv
import logging
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, List

from app.exceptions import DatasetValidationError

logger = logging.getLogger("ingestion_engine")

def detect_encoding(file_path: str) -> str:
    """
    Detects file encoding by testing common encodings against the file head.
    """
    logger.info("Detecting encoding...")
    encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "utf-16"]
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                f.read(1024 * 1024)  # Read up to 1MB
            logger.info(f"Detected encoding: {enc}")
            return enc
        except (UnicodeDecodeError, LookupError):
            continue
    logger.warning("Defaulting to latin-1 encoding fallback.")
    return "latin-1"

def detect_delimiter(file_path: str, encoding: str) -> str:
    """
    Detects delimiter by inspecting consistency across the first 15 lines.
    """
    logger.info("Detecting delimiter...")
    delimiters = [",", ";", "\t", "|"]
    try:
        with open(file_path, "r", encoding=encoding) as f:
            lines = [f.readline() for _ in range(15)]
    except Exception as e:
        logger.error(f"Failed to read file for delimiter detection: {str(e)}")
        return ","

    lines = [l for l in lines if l.strip()]
    if not lines:
        return ","

    counts = {d: [] for d in delimiters}
    for line in lines:
        for d in delimiters:
            counts[d].append(line.count(d))

    best_d = ","
    max_score = -1.0
    for d, cts in counts.items():
        if not cts:
            continue
        avg = sum(cts) / len(cts)
        if avg == 0:
            continue
        variance = sum((x - avg) ** 2 for x in cts) / len(cts)
        if variance == 0:
            score = avg * 1000.0  # Perfect consistency
        else:
            score = avg / (1.0 + variance)
        if score > max_score:
            max_score = score
            best_d = d

    logger.info(f"Detected delimiter: {repr(best_d)}")
    return best_d

def is_numeric(val: str) -> bool:
    if not val or not val.strip():
        return False
    try:
        float(val.strip())
        return True
    except ValueError:
        return False

def detect_header(rows: List[List[str]], consensus_len: int) -> Tuple[bool, int]:
    """
    Analyzes rows to find the start index of data and checks if the first row is a header.
    Returns (has_header, start_row_index)
    """
    logger.info("Detecting header presence and data offset...")
    if not rows:
        return False, 0

    # 1. Skip blank rows and find first row matching the consensus length
    start_idx = 0
    while start_idx < len(rows) and len(rows[start_idx]) != consensus_len:
        start_idx += 1

    if start_idx >= len(rows):
        return False, 0

    candidate_row = rows[start_idx]

    # 2. Collect preview rows to compare formats
    preview_rows = []
    idx = start_idx + 1
    while idx < len(rows) and len(preview_rows) < 5:
        if len(rows[idx]) == consensus_len:
            preview_rows.append(rows[idx])
        idx += 1

    if not preview_rows:
        all_alpha = all(isinstance(val, str) and not is_numeric(val) for val in candidate_row)
        return all_alpha, start_idx

    numeric_cols = 0
    candidate_numeric_matches = 0

    for col_idx in range(consensus_len):
        preview_vals = [r[col_idx] for r in preview_rows]
        # A column is numeric-dominated if 60% of preview values parse as float
        is_num_col = sum(1 for val in preview_vals if is_numeric(val)) >= len(preview_vals) * 0.6
        if is_num_col:
            numeric_cols += 1
            if is_numeric(candidate_row[col_idx]):
                candidate_numeric_matches += 1

    # Heuristic check
    if numeric_cols > 0:
        # If candidate row contains numeric values in numeric columns, it is data, not a header
        has_header = (candidate_numeric_matches == 0)
    else:
        # Check if candidate row is all strings and preview rows also strings
        has_header = all(not is_numeric(val) for val in candidate_row)

    logger.info(f"Header detection result: has_header={has_header}, start_row_index={start_idx}")
    return has_header, start_idx

def infer_column_type(series: pd.Series) -> str:
    """
    Rich data type inference covering all 12 platform classes.
    """
    non_null = series.dropna()
    if non_null.empty:
        return "Text"

    total_count = len(non_null)
    unique_vals = set(non_null.unique())
    unique_vals_lower = {str(x).lower().strip() for x in unique_vals}

    # Boolean
    if unique_vals_lower.issubset({"true", "false", "1", "0", "1.0", "0.0", "t", "f", "y", "n", "yes", "no"}):
        return "Boolean"

    # Percentage strings
    if all(isinstance(x, str) and x.strip().endswith("%") for x in non_null):
        try:
            pd.to_numeric(non_null.str.replace("%", "", regex=False))
            return "Percentage"
        except Exception:
            pass

    # Currency strings
    currency_symbols = ("$", "€", "£", "¥", "₹")
    if all(isinstance(x, str) and (x.strip().startswith(currency_symbols) or any(x.strip().endswith(sym) for sym in currency_symbols)) for x in non_null):
        try:
            cleaned = non_null.str.replace(r"[^\d.-]", "", regex=True)
            pd.to_numeric(cleaned)
            return "Currency"
        except Exception:
            pass

    # Try Numeric
    try:
        numeric_series = pd.to_numeric(non_null)
        # Check if all values are integers
        if all(numeric_series % 1 == 0):
            # Check if it looks like an identifier/ID
            is_increasing = False
            if len(numeric_series) > 1:
                diffs = numeric_series.diff().dropna()
                is_increasing = (diffs == 1).all()
            if is_increasing or all(100000 <= val <= 99999999 for val in numeric_series.iloc[:20]):
                return "Identifier"
            return "Integer"
        return "Float"
    except Exception:
        pass

    # Try Datetime
    try:
        parsed = pd.to_datetime(non_null.iloc[:50], errors='coerce')
        if parsed.notna().sum() / min(50, total_count) >= 0.8:
            return "Datetime"
    except Exception:
        pass

    # Alphanumeric patterns
    email_regex = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    if all(isinstance(x, str) and email_regex.match(x.strip()) for x in non_null.iloc[:50]):
        return "Email"

    url_regex = re.compile(r"^(https?://)?(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    if all(isinstance(x, str) and url_regex.match(x.strip()) for x in non_null.iloc[:50]):
        return "URL"

    phone_regex = re.compile(r"^\+?[\d\s()\-]{7,15}$")
    if all(isinstance(x, str) and phone_regex.match(x.strip()) for x in non_null.iloc[:50]):
        return "Phone Number"

    # Geo Coordinates (e.g. "45.123, -122.456")
    geo_regex = re.compile(r"^-?\d{1,3}\.\d+,\s*-?\d{1,3}\.\d+$")
    if all(isinstance(x, str) and geo_regex.match(x.strip()) for x in non_null.iloc[:50]):
        return "Geographic coordinates"

    # Categorical classification
    unique_count = len(unique_vals)
    if unique_count == 1:
        return "Category"
    if unique_count / total_count < 0.20 or unique_count < 30:
        return "Category"

    return "Text"

def clean_and_validate_dataframe(
    df: pd.DataFrame, 
    filename: str, 
    encoding: str, 
    delimiter: str, 
    has_header: bool
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Cleans DataFrame in-place and constructs the structural/schema validation report.
    Raises DatasetValidationError on fatal errors.
    """
    logger.info("Cleaning dataset and creating validation report...")
    warnings = []
    recommended_fixes = []
    
    # 1. Structural dimensions check
    rows_count = len(df)
    cols_count = len(df.columns)
    if rows_count == 0:
        raise DatasetValidationError(
            reason="The uploaded dataset is empty.",
            details=["Row count is 0. Upload a valid CSV containing records."]
        )
    if cols_count == 0:
        raise DatasetValidationError(
            reason="The dataset does not contain columns.",
            details=["Column count is 0. Ensure fields are delimited correctly."]
        )

    # 2. Check for empty or unnamed column headers
    unnamed_count = 0
    cleaned_columns = []
    for idx, col in enumerate(df.columns):
        col_str = str(col).strip()
        if not col_str or col_str.startswith("Unnamed:"):
            # Recover placeholders
            unnamed_count += 1
            # Infer datatype for name prefix
            col_type = infer_column_type(df.iloc[:, idx])
            prefix = "numeric" if col_type in ["Integer", "Float"] else "datetime" if col_type == "Datetime" else "categorical"
            new_name = f"unnamed_{prefix}_{idx + 1}"
            cleaned_columns.append(new_name)
        else:
            cleaned_columns.append(col_str)

    if unnamed_count > 0:
        warnings.append(f"Identified {unnamed_count} unnamed/empty column headers.")
        recommended_fixes.append("Automatically assigned type-based placeholder names for empty headers.")
        df.columns = cleaned_columns

    # 3. Duplicate columns validation
    seen = {}
    duplicate_cols = []
    for col in df.columns:
        col_str = str(col).strip()
        parts = col_str.rsplit('.', 1)
        is_pandas_dup = len(parts) == 2 and parts[1].isdigit() and parts[0] in seen
        if col_str in seen or is_pandas_dup:
            duplicate_cols.append(parts[0] if is_pandas_dup else col_str)
        seen[col_str] = True

    if duplicate_cols:
        raise DatasetValidationError(
            reason="The dataset contains duplicate column headers.",
            details=[f"Duplicate columns found: {', '.join(list(set(duplicate_cols)))}"]
        )

    # 4. Column data validation & coercion
    inferred_types = {}
    total_nulls = 0
    columns_requiring_cleaning = []
    
    for col in df.columns:
        # Inferred type
        col_type = infer_column_type(df[col])
        inferred_types[col] = col_type

        # Check for all nulls
        null_count = df[col].isna().sum()
        total_nulls += null_count
        if null_count == len(df):
            columns_requiring_cleaning.append(col)
            warnings.append(f"Column '{col}' contains only empty/null values.")
            recommended_fixes.append(f"Consider deleting the empty column '{col}'.")

        # Mixed types numeric checks & infinite cleanups
        if col_type in ["Integer", "Float", "Currency", "Percentage"]:
            # Replace inf values
            inf_mask = np.isinf(df[col]) if df[col].dtype in [np.float64, np.int64] else pd.Series([False] * len(df))
            if inf_mask.any():
                df.loc[inf_mask, col] = np.nan
                warnings.append(f"Column '{col}' contains infinite values.")
                recommended_fixes.append("Replaced infinite metrics with blank values.")

            # Coerce mixed numbers & strings
            non_numeric_count = 0
            if df[col].dtype == object:
                # Count non-numeric strings
                string_mask = df[col].apply(lambda x: isinstance(x, str) and not is_numeric(x) and str(x).strip() != "")
                non_numeric_count = string_mask.sum()
                if non_numeric_count > 0:
                    # Coerce them to floats
                    cleaned_col = pd.to_numeric(df[col], errors='coerce')
                    df[col] = cleaned_col
                    warnings.append(f"Column '{col}' had {non_numeric_count} corrupted/text values.")
                    recommended_fixes.append(f"Coerced mixed text data in '{col}' to numeric nulls.")

        # Datetime validations
        if col_type == "Datetime":
            try:
                parsed_dates = pd.to_datetime(df[col], errors='coerce')
                malformed_dates = parsed_dates.isna().sum() - df[col].isna().sum()
                if malformed_dates > 0:
                    df[col] = parsed_dates
                    warnings.append(f"Column '{col}' contains {malformed_dates} malformed date strings.")
                    recommended_fixes.append(f"Parsed malformed dates in '{col}' into standard ISO format.")
            except Exception:
                pass

    # Missing Value summaries
    total_cells = rows_count * cols_count
    null_percentage = (total_nulls / total_cells * 100) if total_cells > 0 else 0.0
    completeness_score = 100.0 - null_percentage

    report = {
        "dataset_name": filename,
        "encoding": encoding,
        "delimiter": delimiter,
        "header_detected": has_header,
        "rows": rows_count,
        "columns": cols_count,
        "duplicate_columns": duplicate_cols,
        "missing_values": {
            "total_nulls": int(total_nulls),
            "null_percentage": float(round(null_percentage, 2)),
            "completeness_score": float(round(completeness_score, 2)),
            "columns_requiring_cleaning": columns_requiring_cleaning
        },
        "inferred_types": inferred_types,
        "validation_status": "success",
        "warnings": warnings,
        "recommended_fixes": recommended_fixes
    }

    logger.info("Ingestion dataset cleanup and reporting complete.")
    return df, report

def load_and_validate_dataset(
    file_path: str, 
    ext: str, 
    original_filename: str
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    High-level entry point to ingest any supported files (CSV, TSV, TXT, XLS, XLSX)
    automatically detecting encoding, delimiter, header state, and running schema validations.
    """
    logger.info(f"Ingesting file: {original_filename}")
    encoding = None
    delimiter = None
    has_header = True
    start_row_index = 0

    if ext in [".csv", ".tsv", ".txt"]:
        # 1. Detect encoding
        encoding = detect_encoding(file_path)

        # 2. Detect delimiter
        delimiter = detect_delimiter(file_path, encoding)

        # 3. Read preview rows for header validation
        preview_rows = parse_raw_rows(file_path, encoding, delimiter, max_rows=20)
        
        if not preview_rows:
            raise DatasetValidationError(
                reason="Unreadable or empty CSV file.",
                details=["The file does not contain text characters or rows."]
            )

        # 4. Mode columns count
        col_counts = [len(r) for r in preview_rows if r]
        if not col_counts:
            raise DatasetValidationError(
                reason="Structural parsing error.",
                details=["Unable to identify columns in the dataset lines."]
            )
            
        consensus_len = max(set(col_counts), key=col_counts.count)

        # 5. Run intelligent header detection
        has_header, start_row_index = detect_header(preview_rows, consensus_len)

        # 6. Parse full dataframe
        try:
            if has_header:
                df = pd.read_csv(file_path, sep=delimiter, encoding=encoding, skiprows=start_row_index, header=0)
            else:
                df = pd.read_csv(file_path, sep=delimiter, encoding=encoding, skiprows=start_row_index, header=None)
        except Exception as e:
            logger.exception("Pandas CSV reading exception occurred")
            raise DatasetValidationError(
                reason="CSV structure parsing failed.",
                details=[f"Row parsing failed: {str(e)}"]
            )
            
    elif ext in [".xlsx", ".xls"]:
        # Excel Ingestion
        encoding = "binary"
        delimiter = "N/A"
        try:
            # Read preview of Excel
            df_preview = pd.read_excel(file_path, nrows=20, header=None)
            preview_rows = df_preview.values.tolist()
            preview_rows = [[str(cell) if not pd.isna(cell) else "" for cell in r] for r in preview_rows]

            col_counts = [len(r) for r in preview_rows if r]
            consensus_len = max(set(col_counts), key=col_counts.count) if col_counts else 0

            has_header, start_row_index = detect_header(preview_rows, consensus_len)

            if has_header:
                df = pd.read_excel(file_path, skiprows=start_row_index, header=0)
            else:
                df = pd.read_excel(file_path, skiprows=start_row_index, header=None)
        except Exception as e:
            logger.exception("Pandas Excel reading exception occurred")
            raise DatasetValidationError(
                reason="Excel workbook parsing failed.",
                details=[f"Ensure file is not corrupted and sheet is readable: {str(e)}"]
            )
    else:
        raise DatasetValidationError(
            reason="Unsupported extension schema.",
            details=[f"File type extension '{ext}' is not supported."]
        )

    # If df columns have no names (from header=None), name them based on type recovery
    if not has_header:
        type_counts = {}
        col_names = []
        for i in range(len(df.columns)):
            col_type = infer_column_type(df.iloc[:, i])
            prefix = col_type.lower()
            if prefix in ["integer", "float"]:
                prefix = "numeric"
            elif prefix in ["text", "category"]:
                prefix = "categorical"
            elif prefix == "datetime":
                prefix = "datetime"
            else:
                prefix = "feature"
            count = type_counts.get(prefix, 0) + 1
            type_counts[prefix] = count
            col_names.append(f"{prefix}_{count}")
        df.columns = col_names

    # Clean & validate fields
    df, report = clean_and_validate_dataframe(df, original_filename, encoding, delimiter, has_header)
    return df, report

def parse_raw_rows(file_path: str, encoding: str, delimiter: str, max_rows: int = 20) -> List[List[str]]:
    rows = []
    with open(file_path, "r", encoding=encoding) as f:
        reader = csv.reader(f, delimiter=delimiter)
        try:
            for _ in range(max_rows):
                row = next(reader)
                rows.append(row)
        except StopIteration:
            pass
        except Exception:
            pass
    return rows
