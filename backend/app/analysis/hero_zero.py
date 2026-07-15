import pandas as pd
from typing import Dict, Any, List, Optional
from app.analysis.utils import get_columns_by_type

def detect_hero_zero(df: pd.DataFrame, column_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Identifies the top performing (Hero) and worst performing (Zero) category groupings.
    Picks numerical metrics (Revenue, Amount, Sales, Profit) and groups by categorical keys.
    """
    numeric_cols = get_columns_by_type(column_metadata, "is_numeric")
    currency_cols = get_columns_by_type(column_metadata, "is_currency")
    categorical_cols = get_columns_by_type(column_metadata, "is_categorical")
    id_cols = get_columns_by_type(column_metadata, "is_primary_key")
    
    metric_candidates = currency_cols + [c for c in numeric_cols if c not in id_cols and c not in currency_cols and "id" not in str(c).lower()]
    
    metric_col = None
    # Pick first matching column
    for col in ["revenue", "sales_amount", "sales", "amount", "profit", "salary", "expense", "budget", "total"]:
        matching = [c for c in metric_candidates if col in str(c).lower()]
        if matching:
            metric_col = matching[0]
            break
            
    if not metric_col and metric_candidates:
        metric_col = metric_candidates[0]
        
    # 2. Select the category grouping key
    # Prioritize text columns like Product, Category, Region, Department, Channel, Employee
    group_candidates = [c for c in categorical_cols if c not in id_cols]
    
    group_col = None
    for col in ["product", "category", "region", "department", "channel", "name", "employee", "city", "state", "country"]:
        matching = [c for c in group_candidates if col in str(c).lower()]
        if matching:
            group_col = matching[0]
            break
            
    if not group_col and group_candidates:
        group_col = group_candidates[0]
        
    # 3. Default empty response structure
    empty_result = {
        "metric_name": "None",
        "group_by_column": "None",
        "hero_name": "N/A",
        "hero_value": 0.0,
        "zero_name": "N/A",
        "zero_value": 0.0,
        "reason": "Could not identify distinct comparative column pairs to group."
    }
    
    if not metric_col or not group_col:
        return empty_result
        
    try:
        # Group and sum metrics
        grouped = df.groupby(group_col)[metric_col].sum().reset_index()
        
        # Drop rows with null category names
        grouped = grouped.dropna()
        
        if grouped.empty:
            return empty_result
            
        # Find maximum and minimum indices
        max_idx = grouped[metric_col].idxmax()
        min_idx = grouped[metric_col].idxmin()
        
        hero_name = str(grouped.loc[max_idx, group_col])
        hero_value = float(grouped.loc[max_idx, metric_col])
        
        zero_name = str(grouped.loc[min_idx, group_col])
        zero_value = float(grouped.loc[min_idx, metric_col])
        
        metric_disp = metric_col.replace("_", " ").title()
        group_disp = group_col.replace("_", " ").title()
        
        # Deterministic comparative reason
        reason = (
            f"Comparing {metric_disp} grouped by {group_disp}: "
            f"'{hero_name}' was the top performer with a total of {hero_value:,.2f}, "
            f"while '{zero_name}' was the lowest performer with a total of {zero_value:,.2f}."
        )
        
        return {
            "metric_name": metric_disp,
            "group_by_column": group_disp,
            "hero_name": hero_name,
            "hero_value": round(hero_value, 2),
            "zero_name": zero_name,
            "zero_value": round(zero_value, 2),
            "reason": reason
        }
    except Exception as e:
        return {
            **empty_result,
            "reason": f"Calculation failed during performance aggregation: {str(e)}"
        }
