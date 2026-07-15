from typing import List, Dict, Any

def get_columns_by_type(column_metadata: Dict[str, Any], feature_flag: str) -> List[str]:
    """
    Retrieves column names matching a specific feature flag from the dataset column_metadata.
    Example flags: 'is_numeric', 'is_categorical', 'is_date', 'is_primary_key', 'is_currency', 'is_percentage'.
    """
    columns = column_metadata.get("columns", [])
    return [col["name"] for col in columns if col.get(feature_flag) is True]

def get_column_inferred_type(column_metadata: Dict[str, Any], col_name: str) -> str:
    """
    Returns the inferred type for a given column name (e.g. 'integer', 'float', 'categorical', 'datetime').
    """
    columns = column_metadata.get("columns", [])
    for col in columns:
        if col["name"] == col_name:
            return col.get("type", "string")
    return "string"
