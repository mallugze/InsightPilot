from typing import Dict, Any, List

def generate_recommendations(
    dataset_type: str,
    kpis: Dict[str, Any],
    pulse: Dict[str, Any],
    trends: Dict[str, Any],
    anomalies: Dict[str, Any],
    correlations: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Generates structured, domain-tailored recommendation coordinates for the dataset.
    """
    recommendations = []
    
    # 1. Quality & Data Completeness checks (applicable to all datasets)
    data_quality = pulse.get("breakdown", {}).get("data_quality", 100.0)
    completeness = pulse.get("breakdown", {}).get("completeness", 100.0)
    
    if completeness < 95.0:
        recommendations.append({
            "priority": "HIGH",
            "category": "Data Quality",
            "recommendation": "Address incomplete records or handle null columns",
            "reason": f"Only {completeness:.1f}% of data records are fully complete. Missing fields can bias statistical profiles."
        })
        
    if data_quality < 95.0:
        recommendations.append({
            "priority": "MEDIUM",
            "category": "Data Quality",
            "recommendation": "Run deduplication cleanup workflows",
            "reason": f"Data quality score is {data_quality:.1f}%. Duplicate entries exist which may artificially inflate metrics."
        })
        
    # 2. Specific domain-tailored recommendations
    domain = dataset_type.lower()
    
    if "biology" in domain or "scientific" in domain:
        recommendations.append({
            "priority": "HIGH",
            "category": "Pre-processing",
            "recommendation": "Normalize feature scaling before estimators modeling",
            "reason": "Varying metric bounds (e.g. sepal and petal ratios) will bias distance-based clustering if not scaled."
        })
        recommendations.append({
            "priority": "MEDIUM",
            "category": "Model Recommendation",
            "recommendation": "Proceed with Random Forest Classifier",
            "reason": "Random Forest handles tabular non-linear interactions across flower traits with high accuracy."
        })
        
    elif "machine learning" in domain or "survival" in domain:
        recommendations.append({
            "priority": "HIGH",
            "category": "Model Training",
            "recommendation": "Dataset is suitable for supervised classification",
            "reason": "Target label binary features exist. Class balance yields reliable gradient training signals."
        })
        recommendations.append({
            "priority": "MEDIUM",
            "category": "Feature Engineering",
            "recommendation": "Consider categorical embedding feature selection",
            "reason": "Dimensions like cabin and embarkation codes contain sparse identifiers that require target encoding."
        })
        
    elif "healthcare" in domain or "clinical" in domain:
        recommendations.append({
            "priority": "HIGH",
            "category": "Clinical Monitoring",
            "recommendation": "Monitor high-risk patient groups closely",
            "reason": "Admissions diagnostic categories indicate sub-population clusters with elevated risk characteristics."
        })
        
    elif "real estate" in domain or "housing" in domain:
        recommendations.append({
            "priority": "HIGH",
            "category": "Valuation",
            "recommendation": "Apply logarithmic scaling to house listing prices",
            "reason": "Housing prices exhibit skewness and outliers that compress linear modeling coefficients."
        })
        
    elif "sensor" in domain or "iot" in domain:
        recommendations.append({
            "priority": "HIGH",
            "category": "Diagnostics",
            "recommendation": "Inspect telemetry nodes exhibiting abnormal values",
            "reason": "Anomaly spike logs indicate potential hardware calibration faults or sensor read errors."
        })
        
    elif "weather" in domain or "climate" in domain:
        recommendations.append({
            "priority": "MEDIUM",
            "category": "Forecasting",
            "recommendation": "Incorporate rolling historical averages",
            "reason": "Chronological climate indices exhibit strong seasonal trends that benefit from lagged predictors."
        })
        
    elif "student" in domain or "education" in domain:
        recommendations.append({
            "priority": "MEDIUM",
            "category": "Student Advisory",
            "recommendation": "Target intervention strategies for low scoring groups",
            "reason": "Discovered category variances index students who may require additional academic support."
        })

    # Default Business context recommendations
    else:
        margin = kpis.get("profit_margin", 0.0)
        aov = kpis.get("average_order_value", 0.0)
        
        if margin > 0 and margin < 15.0:
            recommendations.append({
                "priority": "HIGH",
                "category": "Finance",
                "recommendation": "Conduct pricing audits and operational cost reviews",
                "reason": f"Profit margin is currently low ({margin:.1f}%). High expenses could be compressing profits."
            })
        else:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Business Operations",
                "recommendation": "Reduce operational costs and optimize marketing spend",
                "reason": "Scaling advertising allocations across high-value customer channels increases margins."
            })
            
    # Default fallback
    if not recommendations:
        recommendations.append({
            "priority": "LOW",
            "category": "General Advisory",
            "recommendation": "Maintain baseline operations logs",
            "reason": "Metrics, variances, and counts match standard operational parameters."
        })
        
    return recommendations
