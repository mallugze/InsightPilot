import pandas as pd
from typing import Dict, Any, List
from app.analysis.utils import get_columns_by_type

def analyze_correlations(df: pd.DataFrame, column_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes Pearson correlation matrix on numeric fields.
    Flags significant linear relationships (absolute coefficient >= 0.3).
    """
    numeric_cols = get_columns_by_type(column_metadata, "is_numeric")
    currency_cols = get_columns_by_type(column_metadata, "is_currency")
    id_cols = get_columns_by_type(column_metadata, "is_primary_key")
    
    correlation_list = []
    
    # Filter numeric fields (skip row indexes / ID codes, preserve currencies)
    eval_cols = currency_cols + [c for c in numeric_cols if c not in id_cols and c not in currency_cols and "id" not in str(c).lower()]
    
    if len(eval_cols) < 2:
        return {"correlations": []}
        
    try:
        # Compute Pearson correlation matrix
        corr_matrix = df[eval_cols].corr(method="pearson")
        
        # Track processed pairs to avoid listing duplicates (e.g., A-B and B-A)
        seen_pairs = set()
        
        for col_a in eval_cols:
            for col_b in eval_cols:
                if col_a == col_b:
                    continue
                    
                pair_key = tuple(sorted([col_a, col_b]))
                if pair_key in seen_pairs:
                    continue
                    
                seen_pairs.add(pair_key)
                
                coef = float(corr_matrix.loc[col_a, col_b])
                
                # Check for NaN correlations
                if pd.isna(coef):
                    continue
                    
                abs_coef = abs(coef)
                
                # We register correlations with absolute value >= 0.3 as significant
                if abs_coef >= 0.30:
                    if coef >= 0.7:
                        strength = "Strong Positive"
                        verbal = "strong direct relationship"
                    elif coef >= 0.3:
                        strength = "Moderate Positive"
                        verbal = "moderate direct relationship"
                    elif coef <= -0.7:
                        strength = "Strong Negative"
                        verbal = "strong inverse relationship"
                    else:
                        strength = "Moderate Negative"
                        verbal = "moderate inverse relationship"
                        
                    disp_a = col_a.replace("_", " ").title()
                    disp_b = col_b.replace("_", " ").title()
                    
                    desc = f"'{disp_a}' shows a {verbal} ({coef:+.2f}) with '{disp_b}'."
                    
                    correlation_list.append({
                        "column_a": disp_a,
                        "column_b": disp_b,
                        "coefficient": round(coef, 3),
                        "strength": strength,
                        "description": desc
                    })
                    
        # Sort by absolute strength of correlation (descending)
        correlation_list.sort(key=lambda x: abs(x["coefficient"]), reverse=True)
        
        return {
            "correlations": correlation_list
        }
    except Exception as e:
        return {
            "correlations": [],
            "error": f"Correlation matrix computation failed: {str(e)}"
        }
