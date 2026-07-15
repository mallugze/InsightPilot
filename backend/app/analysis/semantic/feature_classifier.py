import pandas as pd
from typing import Dict, Any, List

def classify_features(df: pd.DataFrame, col_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Examines every column in the dataset metadata to determine its advanced semantic classification.
    Returns lists of: Column Name, Semantic Type, Native Data Type, Confidence, and Possible Meaning.
    """
    classified_cols = []
    columns = col_metadata.get("columns", [])
    
    # 1. Gather all column names to check for targets and identifiers
    col_names = [str(c["name"]) for c in columns]
    col_names_lower = [name.lower() for name in col_names]
    
    # Detect target label candidates (typical in ML classification/regression datasets)
    target_keywords = {"target", "label", "class", "survived", "species", "outcome", "price", "y"}
    possible_targets = [name for name in col_names if any(kw == name.lower() or name.lower().endswith("_" + kw) for kw in target_keywords)]
    
    for col_info in columns:
        name = col_info["name"]
        name_lower = name.lower()
        native_type = col_info["type"]
        
        is_num = col_info.get("is_numeric", False)
        is_cat = col_info.get("is_categorical", False)
        is_dt = col_info.get("is_date", False)
        is_pk = col_info.get("is_primary_key", False)
        is_curr = col_info.get("is_currency", False)
        is_pct = col_info.get("is_percentage", False)
        
        semantic_type = "Text"
        confidence = 0.70
        meaning = "General text labels or comments."
        
        # Rule cascades
        if is_pk and not is_curr and not any(kw in name_lower for kw in ["revenue", "cost", "price", "amount", "sales"]):
            semantic_type = "Primary Key"
            confidence = 0.95
            meaning = "Unique row identifier index key."
        elif name in possible_targets and (is_cat or is_num) and name_lower not in ["id", "transaction_id", "order_id"]:
            semantic_type = "Target Label"
            confidence = 0.90
            meaning = "Dependent target output variable for machine learning analyses."
        elif is_curr:
            semantic_type = "Currency"
            confidence = 0.95
            meaning = "Monetary financial valuation metrics."
        elif is_pct:
            semantic_type = "Percentage"
            confidence = 0.95
            meaning = "Proportional ratios or percentage indices."
        elif is_dt:
            semantic_type = "Datetime"
            confidence = 0.95
            meaning = "Chronological calendar timestamps."
        elif "id" in name_lower or "code" in name_lower or "key" in name_lower or name_lower.endswith("_no") or name_lower.endswith("num"):
            semantic_type = "Identifier"
            confidence = 0.85
            meaning = "Reference codes or foreign keys indicating relational mappings."
        elif "lat" in name_lower or "lon" in name_lower or "zip" in name_lower or "postal" in name_lower or "country" in name_lower or "city" in name_lower or "region" in name_lower:
            semantic_type = "Location"
            confidence = 0.80
            meaning = "Geographic locations or region indices."
        elif is_num:
            semantic_type = "Numeric"
            confidence = 0.90
            meaning = "Quantitative continuous values or metrics."
        elif native_type == "boolean" or (is_cat and set(df[name].dropna().unique()) <= {0, 1, True, False, "0", "1"}):
            semantic_type = "Boolean"
            confidence = 0.90
            meaning = "Binary flags or logical True/False switches."
        elif is_cat:
            semantic_type = "Categorical"
            confidence = 0.90
            meaning = "Discrete groupings or labels used for classification."
            
        classified_cols.append({
            "name": name,
            "semantic_type": semantic_type,
            "native_type": native_type,
            "confidence": confidence,
            "possible_meaning": meaning
        })
        
    return classified_cols
