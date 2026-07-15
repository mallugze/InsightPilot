import pandas as pd
from typing import Dict, Any, List

def evaluate_ml_readiness(
    df: pd.DataFrame,
    relationships: Dict[str, Any],
    classified_features: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Examines structural properties of the dataset to calculate suitability scores (0-100)
    and detailed reasoning text for different machine learning tasks.
    """
    total_rows = len(df)
    
    # 1. Classification Suitability
    class_cand = relationships.get("classification_candidates", [])
    if class_cand:
        target = class_cand[0]["target"]
        unique_classes = int(df[target].dropna().nunique()) if target in df.columns else 0
        conf = 95 if unique_classes <= 10 else 75
        reasoning = (
            f"Strong classification candidate. Target variable '{target}' has {unique_classes} discrete "
            f"categorical classes, and there are {len(class_cand[0]['features'])} predictors to model relationships."
        )
    else:
        conf = 0
        reasoning = "Not suitable for classification. No discrete categorical target output variable could be inferred."
        
    classification_profile = {"score": conf, "reasoning": reasoning}

    # 2. Regression Suitability
    reg_cand = relationships.get("regression_candidates", [])
    if reg_cand:
        target = reg_cand[0]["target"]
        conf = 90
        reasoning = (
            f"Suitable for regression models. Target variable '{target}' is continuous numeric, "
            f"paired with {len(reg_cand[0]['features'])} numerical feature variables."
        )
    else:
        conf = 0
        reasoning = "Not suitable for regression. No continuous numeric target output column is available."
        
    regression_profile = {"score": conf, "reasoning": reasoning}

    # 3. Forecasting Suitability
    fc_cand = relationships.get("forecasting_candidates", [])
    if fc_cand and total_rows >= 10:
        time_col = fc_cand[0]["time_column"]
        metric_col = fc_cand[0]["metric_column"]
        conf = 85
        reasoning = (
            f"Suitable for time-series forecasting. Has datetime variable '{time_col}' and "
            f"continuous numeric metric '{metric_col}' over a historical timeline."
        )
    else:
        conf = 0
        reasoning = "Not suitable for forecasting. Requires at least one Datetime column and one continuous numeric metric."
        
    forecasting_profile = {"score": conf, "reasoning": reasoning}

    # 4. Clustering Suitability
    clust_cols = relationships.get("clustering_candidates", [])
    if len(clust_cols) >= 2 and total_rows >= 5:
        conf = 80
        reasoning = (
            f"Suitable for clustering (K-Means/DBSCAN). Found {len(clust_cols)} numeric fields "
            f"({', '.join(clust_cols)}) available to map distance coordinates."
        )
    else:
        conf = 0
        reasoning = "Not suitable for clustering. Requires at least 2 numeric feature dimensions."
        
    clustering_profile = {"score": conf, "reasoning": reasoning}

    # 5. Recommendation Suitability
    rec_cols = relationships.get("recommendation_candidates", [])
    if rec_cols:
        conf = 85
        reasoning = (
            f"Suitable for recommendation algorithms (Collaborative Filtering). Identifies user interaction keys "
            f"'{rec_cols[0]}' and item target indices '{rec_cols[1]}' to reconstruct utility matrices."
        )
    else:
        conf = 0
        reasoning = "Not suitable for recommender systems. Requires distinct customer/user and product/item column keys."
        
    recommendation_profile = {"score": conf, "reasoning": reasoning}

    # 6. NLP Suitability
    text_cols = [f["name"] for f in classified_features if f["semantic_type"] == "Text"]
    # Check if text columns have high unique values indicating long content text rather than simple categories
    nlp_suitable = False
    nlp_col = None
    for col in text_cols:
        if col in df.columns:
            uniques = int(df[col].dropna().nunique())
            if uniques / total_rows > 0.40 and uniques > 3:
                nlp_suitable = True
                nlp_col = col
                break
                
    if nlp_suitable:
        conf = 80
        reasoning = f"Suitable for NLP analysis. Text column '{nlp_col}' contains high cardinality descriptive content labels."
    else:
        conf = 0
        reasoning = "Not suitable for NLP. No long-form text fields or high-cardinality descriptions identified."
        
    nlp_profile = {"score": conf, "reasoning": reasoning}

    return {
        "classification": classification_profile,
        "regression": regression_profile,
        "forecasting": forecasting_profile,
        "clustering": clustering_profile,
        "recommendation": recommendation_profile,
        "nlp": nlp_profile
    }
