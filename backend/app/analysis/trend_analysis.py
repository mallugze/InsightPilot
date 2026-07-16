import pandas as pd
import numpy as np
from typing import Dict, Any, List
from app.analysis.utils import get_columns_by_type

def analyze_trends(df: pd.DataFrame, column_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Examines date/time columns to group numeric metrics sequentially.
    Computes daily/weekly/monthly charts data, moving averages, and growth margins.
    """
    date_cols = get_columns_by_type(column_metadata, "is_date")
    numeric_cols = get_columns_by_type(column_metadata, "is_numeric")
    currency_cols = get_columns_by_type(column_metadata, "is_currency")
    id_cols = get_columns_by_type(column_metadata, "is_primary_key")
    
    empty_result = {
        "has_trends": False,
        "trend_direction": "Stable",
        "growth_percent": 0.0,
        "chart_data": [],
        "metric_name": "None",
        "date_column": "None",
        "period": "None"
    }
    
    if not date_cols or not (currency_cols + numeric_cols):
        return empty_result
        
    date_col = date_cols[0]
    
    # Prioritize metric column
    metric_candidates = currency_cols + [c for c in numeric_cols if c not in id_cols and c not in currency_cols and "id" not in str(c).lower()]
    if not metric_candidates:
        return empty_result
    metric_col = metric_candidates[0]
    
    try:
        # Convert date column to pandas datetime in a copy
        df_clean = df.copy()
        df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')
        df_clean = df_clean.dropna(subset=[date_col])
        
        if df_clean.empty:
            return empty_result
            
        # Sort chronologically
        df_clean = df_clean.sort_values(by=date_col)
        
        # Calculate date range span to decide grouping frequency
        min_date = df_clean[date_col].min()
        max_date = df_clean[date_col].max()
        days_span = (max_date - min_date).days
        
        if days_span <= 35:
            # Group by Day: format as YYYY-MM-DD
            period = "daily"
            df_clean["group_key"] = df_clean[date_col].dt.strftime("%Y-%m-%d")
        elif days_span <= 180:
            # Group by Week: format as Year-Week
            period = "weekly"
            df_clean["group_key"] = df_clean[date_col].dt.to_period("W").astype(str)
        else:
            # Group by Month: format as YYYY-MM
            period = "monthly"
            df_clean["group_key"] = df_clean[date_col].dt.strftime("%Y-%m")
            
        # Group and aggregate sum
        timeline = df_clean.groupby("group_key")[metric_col].sum().reset_index()
        timeline.columns = ["date", "value"]
        
        # Chronological sort of the grouped timelines
        timeline = timeline.sort_values(by="date")
        
        if timeline.empty:
            return empty_result
            
        # Coerce any null/NaN aggregates to 0 prior to regression calculations
        timeline = timeline.fillna(0)
        
        # 1. Calculate Growth Percent
        first_val = float(timeline["value"].iloc[0])
        last_val = float(timeline["value"].iloc[-1])
        growth_pct = ((last_val - first_val) / first_val * 100.0) if first_val > 0 else 0.0
        
        # 2. Compute 3-period Rolling Moving Average
        timeline["moving_avg"] = timeline["value"].rolling(window=min(3, len(timeline)), min_periods=1).mean()
        
        # 3. Calculate simple Trend Direction using linear regression slope
        x = np.arange(len(timeline))
        y = timeline["value"].values
        trend_direction = "Stable"
        
        if len(timeline) > 1:
            slope = np.polyfit(x, y, 1)[0]
            # Normalize slope by average value
            mean_y = y.mean() if y.mean() > 0 else 1.0
            normalized_slope = slope / mean_y
            
            if normalized_slope > 0.01:
                trend_direction = "Upward"
            elif normalized_slope < -0.01:
                trend_direction = "Downward"
                
        # 4. Format chart-ready output array (safe-serialize NaN values)
        chart_data = []
        for _, row in timeline.iterrows():
            chart_data.append({
                "date": str(row["date"]),
                "value": round(float(row["value"]), 2),
                "moving_avg": round(float(row["moving_avg"]), 2)
            })
            
        return {
            "has_trends": True,
            "trend_direction": trend_direction,
            "growth_percent": round(growth_pct, 1),
            "chart_data": chart_data,
            "metric_name": metric_col.replace("_", " ").title(),
            "date_column": date_col.replace("_", " ").title(),
            "period": period
        }
    except Exception as e:
        return {
            **empty_result,
            "reason": f"Calculation failed during trend grouping: {str(e)}"
        }
