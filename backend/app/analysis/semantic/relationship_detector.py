import pandas as pd
from typing import Dict, Any, List

def discover_relationships(
    df: pd.DataFrame, 
    classified_features: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Identifies logical metrics, dimensions, forecasting timelines, and ML candidates from semantic definitions.
    """
    primary_metrics = []
    grouping_dimensions = []
    time_dimensions = []
    potential_targets = []
    categorical_dimensions = []
    
    # 1. Classify columns into base groups
    for feat in classified_features:
        name = feat["name"]
        sem_type = feat["semantic_type"]
        native_type = feat.get("native_type", "")
        
        if sem_type in ["Currency", "Numeric", "Percentage"] or native_type in ["integer", "float"]:
            primary_metrics.append(name)
        if sem_type in ["Categorical", "Location", "Boolean", "Target Label"] or native_type in ["categorical", "boolean"]:
            # If target label, only treat as categorical if it is text/categorical natively, OR has low unique cardinality (<= 10)
            unique_cnt = int(df[name].dropna().nunique()) if name in df.columns else 0
            if sem_type == "Target Label" and native_type not in ["categorical", "boolean", "string"] and unique_cnt > 10:
                pass
            else:
                categorical_dimensions.append(name)
                # Grouping dimension if low-to-medium cardinality
                if 1 < unique_cnt < 80:
                    grouping_dimensions.append(name)
        if sem_type == "Datetime" or native_type == "datetime":
            time_dimensions.append(name)
        if sem_type == "Target Label":
            potential_targets.append(name)
            
    # 2. Extract ML Candidates
    regression_candidates = []
    classification_candidates = []
    forecasting_candidates = []
    clustering_candidates = []
    recommendation_candidates = []
    
    # Target fallback: if no Target Label detected, look for default target fields like 'revenue', 'price', or any end labels
    if not potential_targets:
        for feat in classified_features:
            if feat["semantic_type"] in ["Currency", "Numeric"] and feat["name"].lower() in ["revenue", "price", "profit", "amount", "total"]:
                potential_targets.append(feat["name"])
            elif feat["semantic_type"] == "Categorical" and feat["name"].lower() in ["status", "attrition", "survived", "species", "category"]:
                potential_targets.append(feat["name"])
                
    # Regression Candidates
    numeric_targets = [t for t in potential_targets if t in primary_metrics]
    if numeric_targets and len(primary_metrics) > 1:
        for t in numeric_targets:
            feats = [c for c in primary_metrics if c != t]
            if feats:
                regression_candidates.append({
                    "target": t,
                    "features": feats
                })
                
    # Classification Candidates
    categorical_targets = [t for t in potential_targets if t in categorical_dimensions]
    if categorical_targets and (primary_metrics or len(categorical_dimensions) > 1):
        for t in categorical_targets:
            feats = [c for c in (primary_metrics + categorical_dimensions) if c != t]
            if feats:
                classification_candidates.append({
                    "target": t,
                    "features": feats
                })
                
    # Forecasting Candidates
    if time_dimensions and primary_metrics:
        for time_col in time_dimensions:
            for metric in primary_metrics:
                forecasting_candidates.append({
                    "time_column": time_col,
                    "metric_column": metric
                })
                
    # Clustering Candidates
    if len(primary_metrics) >= 2:
        clustering_candidates = primary_metrics
        
    # Recommendation Candidates
    user_col = None
    item_col = None
    for feat in classified_features:
        name_lower = feat["name"].lower()
        if "user" in name_lower or "customer" in name_lower or "client" in name_lower:
            user_col = feat["name"]
        elif "product" in name_lower or "item" in name_lower or "sku" in name_lower or "movie" in name_lower or "book" in name_lower:
            item_col = feat["name"]
            
    if user_col and item_col:
        recommendation_candidates = [user_col, item_col]

    return {
        "primary_metrics": primary_metrics,
        "grouping_dimensions": grouping_dimensions,
        "time_dimensions": time_dimensions,
        "potential_targets": potential_targets,
        "categorical_dimensions": categorical_dimensions,
        "regression_candidates": regression_candidates,
        "classification_candidates": classification_candidates,
        "forecasting_candidates": forecasting_candidates,
        "clustering_candidates": clustering_candidates,
        "recommendation_candidates": recommendation_candidates
    }
