import pandas as pd
import numpy as np
from typing import Dict, Any, List
from app.analysis.utils import get_columns_by_type

def detect_anomalies(df: pd.DataFrame, column_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scans numerical columns for values that deviate from the mean by more than 2.0 standard deviations.
    Returns lists of outliers with row indicators, values, and explanations.
    """
    numeric_cols = get_columns_by_type(column_metadata, "is_numeric")
    currency_cols = get_columns_by_type(column_metadata, "is_currency")
    id_cols = get_columns_by_type(column_metadata, "is_primary_key")
    
    anomalies_list = []
    high_count = 0
    low_count = 0
    
    # Restrict to primary numeric columns (skip identifiers, preserve currencies)
    eval_cols = currency_cols + [c for c in numeric_cols if c not in id_cols and c not in currency_cols and "id" not in str(c).lower()]
    
    for col in eval_cols:
        series = df[col].dropna()
        if len(series) < 5:
            continue
            
        mean = float(series.mean())
        std = float(series.std())
        
        if std == 0:
            continue
            
        # Calculate Z-scores
        z_scores = (series - mean) / std
        outliers_mask = z_scores.abs() > 2.0
        
        outliers = series[outliers_mask]
        outliers_z = z_scores[outliers_mask]
        
        col_disp = col.replace("_", " ").title()
        
        for idx, val in outliers.items():
            z_val = float(outliers_z[idx])
            direction = "spike" if z_val > 0 else "drop"
            
            if z_val > 0:
                high_count += 1
                desc = f"Value {val:,.2f} in '{col_disp}' represents an unusual spike (+{z_val:.1f} standard deviations above average)."
            else:
                low_count += 1
                desc = f"Value {val:,.2f} in '{col_disp}' represents an unusual drop ({z_val:.1f} standard deviations below average)."
                
            anomalies_list.append({
                "column_name": col_disp,
                "row_index": int(idx) + 1,  # 1-indexed for business users
                "value": round(float(val), 2),
                "z_score": round(z_val, 2),
                "type": direction,
                "description": desc
            })
            
            # Limit total list length to protect performance
            if len(anomalies_list) >= 15:
                break
                
        if len(anomalies_list) >= 15:
            break
            
    return {
        "anomalies_count": len(anomalies_list),
        "high_anomalies": high_count,
        "low_anomalies": low_count,
        "anomalies": anomalies_list
    }
