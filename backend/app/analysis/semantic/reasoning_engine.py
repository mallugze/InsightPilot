from typing import Dict, Any, List

def generate_understanding_explanation(
    domain: str,
    subdomain: str,
    entity: str,
    classified_features: List[Dict[str, Any]],
    relationships: Dict[str, Any],
    ml_readiness: Dict[str, Any]
) -> str:
    """
    Converts raw semantic profile tags and variables into a cohesive human-readable summary
    explaining what InsightPilot understood about the dataset and the rationale behind its suggestions.
    """
    total_cols = len(classified_features)
    metrics = relationships.get("primary_metrics", [])
    groupings = relationships.get("grouping_dimensions", [])
    dates = relationships.get("time_dimensions", [])
    targets = relationships.get("potential_targets", [])
    
    # 1. Base description
    intro = (
        f"InsightPilot analyzed this dataset and classified it under the '{domain}' domain, specifically as "
        f"'{subdomain}' data. Structurally, the dataset consists of {total_cols} columns where each row represents "
        f"an individual '{entity}' record."
    )
    
    # 2. Schema profiling description
    metrics_str = f"such as {', '.join(metrics[:2])}" if metrics else ""
    groupings_str = f"such as {', '.join(groupings[:2])}" if groupings else ""
    
    schema_desc = (
        f"We identified {len(metrics)} key metrics {metrics_str} to measure performance "
        f"and {len(groupings)} categorical dimensions {groupings_str} to group and slice data points."
    )
    
    # 3. Time Series Rationale
    if dates:
        date_col = dates[0]
        time_desc = (
            f"The presence of calendar timestamps in '{date_col}' enables time-series trend profiling, "
            f"allowing us to calculate sequential growth rates and moving average lines."
        )
    else:
        time_desc = "No datetime fields were detected, so time-series timeline graphs have been skipped."
        
    # 4. ML Readiness Rationale
    ml_feats = []
    for model_type, profile in ml_readiness.items():
        if profile.get("score", 0) >= 70:
            ml_feats.append(model_type.title())
            
    if ml_feats:
        ml_desc = (
            f"In terms of advanced modeling, this dataset has columns configured for "
            f"{', '.join(ml_feats)} tasks. Specifically, "
            f"{ml_readiness.get('classification', {}).get('reasoning') if 'Classification' in ml_feats else ml_readiness.get('regression', {}).get('reasoning')} "
        )
    else:
        ml_desc = "Structure limits machine learning modeling, fitting mostly general spreadsheet reports and histograms."
        
    # Combine sections into a clean text narrative
    explanation = f"{intro} {schema_desc} {time_desc} {ml_desc}"
    return explanation
