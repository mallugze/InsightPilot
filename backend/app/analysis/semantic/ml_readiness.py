import pandas as pd
from typing import Dict, Any, List

def evaluate_ml_readiness(
    df: pd.DataFrame,
    relationships: Dict[str, Any],
    classified_features: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Evaluates dataset readiness (0-100) for ML tasks based on numeric density,
    missing value rates, and class targets.
    """
    total_rows = len(df)
    missing_ratio = df.isnull().sum().sum() / (df.size if df.size > 0 else 1)
    
    # 1. Classification Suitability
    class_cand = relationships.get("classification_candidates", [])
    if class_cand:
        target = class_cand[0]["target"]
        unique_classes = int(df[target].dropna().nunique()) if target in df.columns else 0
        missing_target = df[target].isnull().sum() / total_rows if total_rows > 0 else 0
        
        # Calculation: higher class clarity + low target missingness = near 100%
        if unique_classes >= 2 and unique_classes <= 15:
            conf = int(98 - (missing_target * 50) - (missing_ratio * 10))
        else:
            conf = int(80 - (missing_target * 40))
        conf = max(10, min(99, conf))
        
        reasoning = (
            f"Classification readiness is {conf}%. Target variable '{target}' contains {unique_classes} discrete "
            f"categorical classes with {len(class_cand[0]['features'])} numerical/categorical predictors."
        )
    else:
        conf = 0
        reasoning = "Not suitable for classification. No discrete categorical target variable could be identified."
        
    classification_profile = {"score": conf, "reasoning": reasoning}

    # 2. Regression Suitability
    reg_cand = relationships.get("regression_candidates", [])
    if reg_cand:
        target = reg_cand[0]["target"]
        missing_target = df[target].isnull().sum() / total_rows if total_rows > 0 else 0
        
        # High score (96%) for continuous numeric targets with few missing values
        conf = int(96 - (missing_target * 60) - (missing_ratio * 15))
        conf = max(10, min(99, conf))
        
        reasoning = (
            f"Regression readiness is {conf}%. Continuous target '{target}' has been mapped "
            f"against {len(reg_cand[0]['features'])} continuous predictors."
        )
    else:
        conf = 0
        reasoning = "Not suitable for regression. No continuous numerical target column could be identified."
        
    regression_profile = {"score": conf, "reasoning": reasoning}

    # 3. Time Series Forecasting Suitability
    fc_cand = relationships.get("forecasting_candidates", [])
    has_date = any(f["semantic_type"] == "Datetime" for f in classified_features)
    
    if (fc_cand or has_date) and total_rows >= 10:
        time_col = fc_cand[0]["time_column"] if fc_cand else next((f["name"] for f in classified_features if f["semantic_type"] == "Datetime"), "date")
        metric_col = fc_cand[0]["metric_column"] if fc_cand else next((f["name"] for f in classified_features if f["semantic_type"] == "Numeric"), "value")
        
        conf = int(95 - (missing_ratio * 40))
        conf = max(10, min(99, conf))
        
        reasoning = (
            f"Forecasting readiness is {conf}%. Identified chronological timestamps in '{time_col}' "
            f"paired with continuous metric target '{metric_col}'."
        )
    else:
        conf = 0
        reasoning = "Not suitable for forecasting. Requires a Datetime column and at least one continuous measure."
        
    forecasting_profile = {"score": conf, "reasoning": reasoning}

    # 4. Clustering Suitability
    clust_cols = relationships.get("clustering_candidates", [])
    if len(clust_cols) >= 2 and total_rows >= 5:
        # Score depends on numeric density
        numeric_density = 1.0 - missing_ratio
        conf = int(80 + (numeric_density * 18))
        conf = max(10, min(98, conf))
        
        reasoning = (
            f"Clustering suitability is {conf}%. Found {len(clust_cols)} continuous numeric fields "
            f"available to cluster coordinates in multi-dimensional space."
        )
    else:
        conf = 0
        reasoning = "Not suitable for clustering. Requires at least 2 clean numeric variables."
        
    clustering_profile = {"score": conf, "reasoning": reasoning}

    # 5. Recommender Suitability
    rec_cols = relationships.get("recommendation_candidates", [])
    if rec_cols:
        conf = int(90 - (missing_ratio * 30))
        conf = max(10, min(99, conf))
        
        reasoning = (
            f"Recommendation system readiness is {conf}%. Mapped distinct user key '{rec_cols[0]}' "
            f"and product/item index '{rec_cols[1]}' to build rating matrices."
        )
    else:
        conf = 0
        reasoning = "Not suitable for recommendation models. Requires user/customer and item/product identifiers."
        
    recommendation_profile = {"score": conf, "reasoning": reasoning}

    # 6. NLP Suitability
    text_cols = [f["name"] for f in classified_features if f["semantic_type"] in ["Text", "Categorical"]]
    nlp_suitable = False
    nlp_col = None
    
    # Check for text keywords
    for col in text_cols:
        col_lower = col.lower()
        if any(kw in col_lower for kw in ["review", "comment", "feedback", "text", "description", "message", "headline"]):
            nlp_suitable = True
            nlp_col = col
            break
            
    if nlp_suitable:
        conf = int(92 - (missing_ratio * 30))
        conf = max(10, min(99, conf))
        reasoning = f"NLP readiness is {conf}%. Text column '{nlp_col}' contains descriptive natural text attributes."
    else:
        # Check high cardinality text
        for col in text_cols:
            if col in df.columns:
                uniques = int(df[col].dropna().nunique())
                if uniques / total_rows > 0.40 and uniques > 5:
                    nlp_suitable = True
                    nlp_col = col
                    break
        if nlp_suitable:
            conf = int(80 - (missing_ratio * 20))
            reasoning = f"NLP readiness is {conf}%. Found high-cardinality text categories in '{nlp_col}'."
        else:
            conf = 0
            reasoning = "Not suitable for NLP. No long-form text fields or feedback comments identified."
        
    nlp_profile = {"score": conf, "reasoning": reasoning}

    return {
        "classification": classification_profile,
        "regression": regression_profile,
        "forecasting": forecasting_profile,
        "clustering": clustering_profile,
        "recommendation": recommendation_profile,
        "nlp": nlp_profile
    }
