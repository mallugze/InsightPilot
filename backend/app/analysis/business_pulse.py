import pandas as pd
from typing import Dict, Any, List
from app.analysis.utils import get_columns_by_type

def calculate_business_pulse(
    df: pd.DataFrame, 
    dataset_type: str, 
    column_metadata: Dict[str, Any],
    kpis: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Computes a deterministic overall business health score (0-100), health labels,
    and returns a normalized breakdown of quality, completeness, consistency, and performance.
    """
    rows = len(df)
    cols = len(df.columns)
    total_cells = rows * cols
    
    # 1. Data Quality Score
    missing_count = int(df.isnull().sum().sum())
    dup_rows = int(df.duplicated().sum())
    dup_cells = dup_rows * cols
    
    quality_score = 100.0 * (1.0 - (missing_count + dup_cells) / (total_cells or 1))
    quality_score = round(max(0.0, min(100.0, quality_score)), 1)
    
    # 2. Completeness Score (percentage of records without any missing cells)
    complete_rows = len(df.dropna())
    completeness_score = (complete_rows / rows) * 100.0 if rows > 0 else 100.0
    completeness_score = round(max(0.0, min(100.0, completeness_score)), 1)
    
    # 3. Consistency Score (checking data variance and outlier ratios)
    # Check what ratio of data points lie within 2.5 standard deviations (typical Z-score)
    numeric_cols = get_columns_by_type(column_metadata, "is_numeric")
    id_cols = get_columns_by_type(column_metadata, "is_primary_key")
    
    anomaly_cells = 0
    total_numeric_cells = 0
    for col in numeric_cols:
        if col in id_cols or "id" in str(col).lower():
            continue
        series = df[col].dropna()
        if len(series) > 3:
            std = float(series.std())
            mean = float(series.mean())
            if std > 0:
                # Count elements outside 2.5 std devs
                outliers = ((series - mean).abs() > (2.5 * std)).sum()
                anomaly_cells += int(outliers)
                total_numeric_cells += len(series)
                
    anomaly_ratio = anomaly_cells / total_numeric_cells if total_numeric_cells > 0 else 0.0
    consistency_score = 100.0 * (1.0 - (anomaly_ratio * 3.0))  # penalize anomalies heavily
    consistency_score = round(max(0.0, min(100.0, consistency_score)), 1)
    
    # 4. Business Performance Score
    # Infer based on KPIs
    performance_score = 80.0  # default baseline
    if dataset_type == "Sales":
        margin = kpis.get("profit_margin", 20.0)
        # Margin <= 0 -> 40, margin >= 40 -> 98
        performance_score = 50.0 + (margin * 1.2)
    elif dataset_type == "HR":
        attrition = kpis.get("attrition_rate", 10.0)
        # Attrition <= 5 -> 95, attrition >= 30 -> 35
        performance_score = max(30.0, 95.0 - (attrition * 2.0))
    elif dataset_type == "Finance":
        margin = kpis.get("profit_margin", 20.0)
        performance_score = 50.0 + (margin * 1.2)
        
    performance_score = round(max(0.0, min(100.0, performance_score)), 1)
    
    # 5. Overall Weighted Pulse
    # Weights: Quality (25%), Completeness (25%), Consistency (20%), Performance (30%)
    overall = (0.25 * quality_score + 
               0.25 * completeness_score + 
               0.20 * consistency_score + 
               0.30 * performance_score)
    overall_score = round(max(0.0, min(100.0, overall)), 1)
    
    # Define health labels
    if overall_score >= 90:
        health_label = "Excellent"
    elif overall_score >= 75:
        health_label = "Good"
    elif overall_score >= 50:
        health_label = "Average"
    elif overall_score >= 30:
        health_label = "Poor"
    else:
        health_label = "Critical"
        
    return {
        "score": overall_score,
        "health_label": health_label,
        "breakdown": {
            "data_quality": quality_score,
            "completeness": completeness_score,
            "consistency": consistency_score,
            "business_performance": performance_score
        }
    }
