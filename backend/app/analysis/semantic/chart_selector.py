import pandas as pd
from typing import Dict, Any, List

def select_charts(
    df: pd.DataFrame,
    classified_features: List[Dict[str, Any]],
    relationships: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Selects optimal visualization layout cards based on semantic columns.
    Returns: intent, reasoning, confidence, suggested_columns, and chart_type recommendation.
    """
    recommendations = []
    
    dates = relationships.get("time_dimensions", [])
    metrics = relationships.get("primary_metrics", [])
    groups = relationships.get("grouping_dimensions", [])
    
    # 1. Timeline Trend Selection
    if dates and metrics:
        recommendations.append({
            "intent": "Trend",
            "chart_type": "Line Chart",
            "reasoning": f"Temporal variable '{dates[0]}' enables tracing chronological changes in metric '{metrics[0]}'.",
            "confidence": 0.98,
            "suggested_columns": [dates[0], metrics[0]]
        })
        
    # 2. Categorical Distribution / Ranking Selection
    if groups and metrics:
        recommendations.append({
            "intent": "Comparison",
            "chart_type": "Bar Chart",
            "reasoning": f"Enables discrete group rankings of '{groups[0]}' segments by continuous measure '{metrics[0]}'.",
            "confidence": 0.95,
            "suggested_columns": [groups[0], metrics[0]]
        })
        
        recommendations.append({
            "intent": "Composition",
            "chart_type": "Pie Chart",
            "reasoning": f"Exposes percentage slice allocations of '{groups[0]}' across total metric distributions.",
            "confidence": 0.88,
            "suggested_columns": [groups[0], metrics[0]]
        })
        
    # 3. Two continuous numerical variables ➔ Relationship Scatter Plot
    if len(metrics) >= 2:
        recommendations.append({
            "intent": "Relationship",
            "chart_type": "Scatter Plot",
            "reasoning": f"Maps linear scatter values between metrics '{metrics[0]}' and '{metrics[1]}' to trace dependency clustering.",
            "confidence": 0.92,
            "suggested_columns": [metrics[0], metrics[1]]
        })
        
        # 4. Multi-numerics ➔ Correlation Heatmap
        if len(metrics) >= 3:
            recommendations.append({
                "intent": "Correlation Matrix",
                "chart_type": "Heatmap",
                "reasoning": "Illustrates linear Pearson correlation coefficients between continuous variables in a layout grid.",
                "confidence": 0.90,
                "suggested_columns": metrics[:4]
            })
            
    # 5. Fallback histogram
    if metrics and not dates and not groups:
        recommendations.append({
            "intent": "Distribution",
            "chart_type": "Histogram",
            "reasoning": f"Shows value spread variance and statistical distribution shapes of numeric variable '{metrics[0]}'.",
            "confidence": 0.85,
            "suggested_columns": [metrics[0]]
        })
        
    return recommendations
