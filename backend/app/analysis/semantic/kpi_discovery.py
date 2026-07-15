import pandas as pd
from typing import Dict, Any, List

def discover_kpis(
    df: pd.DataFrame,
    classified_features: List[Dict[str, Any]],
    relationships: Dict[str, Any],
    domain: str
) -> List[Dict[str, Any]]:
    """
    Examines feature types, cardinality, and dataset context to dynamically generate suggested KPI cards.
    Each suggested card explains what strategy (SUM/MEAN/COUNT) is matching and why.
    """
    suggested_kpis = []
    
    # Extract categories
    primary_keys = [f["name"] for f in classified_features if f["semantic_type"] == "Primary Key"]
    currencies = [f["name"] for f in classified_features if f["semantic_type"] == "Currency"]
    numerics = [f["name"] for f in classified_features if f["semantic_type"] in ["Numeric", "Percentage"] and f["name"] not in primary_keys]
    datetimes = [f["name"] for f in classified_features if f["semantic_type"] == "Datetime"]
    categories = [f["name"] for f in classified_features if f["semantic_type"] in ["Categorical", "Location", "Boolean"]]
    
    # 1. Total count of records / row entities
    row_count = len(df)
    key_col = primary_keys[0] if primary_keys else (classified_features[0]["name"] if classified_features else "id")
    entity_label = "Records"
    
    # Refine label by domain
    if domain == "Scientific":
        entity_label = "Samples"
    elif domain == "Healthcare":
        entity_label = "Patients"
    elif domain == "Machine Learning":
        entity_label = "Training Instances"
    elif domain == "Business":
        entity_label = "Transactions"
        if "employee" in "".join([f["name"].lower() for f in classified_features]):
            entity_label = "Employees"
        elif "customer" in "".join([f["name"].lower() for f in classified_features]):
            entity_label = "Customers"
            
    suggested_kpis.append({
        "metric_name": f"Total {entity_label}",
        "aggregation_strategy": "COUNT",
        "target_column": key_col,
        "reasoning": f"Calculates total row volume containing {row_count} mapped samples.",
        "selected_why": "Core structural dimension representing dataset record count."
    })
    
    # 2. Add Currency KPIs (Total Revenue, Margin etc.)
    for curr in currencies:
        name_clean = curr.replace("_", " ").title()
        suggested_kpis.append({
            "metric_name": f"Total {name_clean}",
            "aggregation_strategy": "SUM",
            "target_column": curr,
            "reasoning": f"Aggregates total cumulative values inside currency metric '{curr}'.",
            "selected_why": "Crucial financial metric tracking top-line economic performance."
        })
        
    # 3. Add Numeric KPIs
    for num in numerics:
        name_clean = num.replace("_", " ").title()
        # If it looks like average/rates or GPA/grade, do MEAN
        if any(kw in num.lower() for kw in ["rate", "margin", "grade", "score", "age", "average", "avg", "percent"]):
            suggested_kpis.append({
                "metric_name": f"Average {name_clean}",
                "aggregation_strategy": "MEAN",
                "target_column": num,
                "reasoning": f"Calculates standard statistical average mean value of '{num}'.",
                "selected_why": "Continuous metric representing diagnostic ratios or percentage performance."
            })
        else:
            suggested_kpis.append({
                "metric_name": f"Cumulative {name_clean}",
                "aggregation_strategy": "SUM",
                "target_column": num,
                "reasoning": f"Calculates sum totals of '{num}' values across all rows.",
                "selected_why": "Numeric capacity column tracking structural volumes."
            })
            
    # 4. Fallback if no numeric/currency columns: unique dimensions counters
    if len(suggested_kpis) < 3:
        for cat in categories[:2]:
            unique_cnt = df[cat].dropna().nunique() if cat in df.columns else 0
            name_clean = cat.replace("_", " ").title()
            suggested_kpis.append({
                "metric_name": f"Unique {name_clean}s",
                "aggregation_strategy": "COUNT_DISTINCT",
                "target_column": cat,
                "reasoning": f"Counts distinct category labels ({unique_cnt}) found inside column '{cat}'.",
                "selected_why": "Categorical dimension mapping unique segment groups."
            })
            
    # Return top 4 KPIs
    return suggested_kpis[:4]
