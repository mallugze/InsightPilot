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
    Generates deterministic, structured recommendations based on dataset metrics.
    """
    recommendations = []
    
    # 1. Quality & Data Completeness checks (applicable to all datasets)
    data_quality = pulse.get("breakdown", {}).get("data_quality", 100.0)
    completeness = pulse.get("breakdown", {}).get("completeness", 100.0)
    
    if completeness < 90.0:
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
        
    # 2. Specific domain business recommendations
    if dataset_type == "Sales":
        margin = kpis.get("profit_margin", 0.0)
        aov = kpis.get("average_order_value", 0.0)
        
        if margin < 15.0:
            recommendations.append({
                "priority": "HIGH",
                "category": "Finance",
                "recommendation": "Conduct pricing audits and operational cost reviews",
                "reason": f"Profit margin is currently low ({margin:.1f}%). High logistics expenses or low-priced items could be compressing profits."
            })
        elif margin > 40.0:
            recommendations.append({
                "priority": "LOW",
                "category": "Finance",
                "recommendation": "Leverage healthy margins to run volume expansion promotions",
                "reason": f"Outstanding profit margin ({margin:.1f}%) provides buffer to absorb price reductions in exchange for market share."
            })
            
        if aov > 0:
            # Check for negative correlation between discount and margin
            discount_corr = False
            for corr in correlations.get("correlations", []):
                if "discount" in corr["column_a"].lower() or "discount" in corr["column_b"].lower():
                    if corr["coefficient"] < -0.3:
                        discount_corr = True
                        break
            if discount_corr:
                recommendations.append({
                    "priority": "HIGH",
                    "category": "Sales",
                    "recommendation": "Restructure promotional discount bounds",
                    "reason": "Promotional discounts correlate negatively with profitability margins, indicating margin erosion."
                })
                
    elif dataset_type == "HR":
        attrition = kpis.get("attrition_rate", 0.0)
        salary = kpis.get("average_salary", 0.0)
        
        if attrition > 12.0:
            recommendations.append({
                "priority": "HIGH",
                "category": "HR",
                "recommendation": "Conduct talent retention surveys and adjust salary bounds",
                "reason": f"Employee attrition is high ({attrition:.1f}%), which increases replacement costs and impacts team cohesion."
            })
        else:
            recommendations.append({
                "priority": "LOW",
                "category": "HR",
                "recommendation": "Maintain baseline cultural programs and document retention practices",
                "reason": f"Excellent employee attrition rate ({attrition:.1f}%) proves workplace consistency."
            })
            
    elif dataset_type == "Finance":
        income = kpis.get("total_income", 0.0)
        expense = kpis.get("total_expense", 0.0)
        
        if expense > income * 0.8:
            recommendations.append({
                "priority": "HIGH",
                "category": "Finance",
                "recommendation": "Implement strict budget caps and expense audits",
                "reason": f"Operating expenses absorb { (expense/income)*100.0:.1f}% of total gross income, limiting cash flow buffers."
            })
            
    # 3. Trend based recommendations
    if trends.get("has_trends"):
        direction = trends.get("trend_direction", "Stable")
        metric_name = trends.get("metric_name", "Value")
        
        if direction == "Downward":
            recommendations.append({
                "priority": "HIGH",
                "category": "Sales",
                "recommendation": f"Diagnose drop-offs in seasonal demand and launch sales sprints",
                "reason": f"The aggregate trend for '{metric_name}' is showing a Downward trajectory."
            })
        elif direction == "Upward":
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Marketing",
                "recommendation": f"Scale marketing spends to maximize return in a growing demand period",
                "reason": f"Positive trend momentum ({trends.get('growth_percent', 0.0):+.1f}%) presents opportunities to scale volume."
            })
            
    # 4. Anomaly based recommendations
    anomalies_count = anomalies.get("anomalies_count", 0)
    if anomalies_count > 3:
        recommendations.append({
            "priority": "MEDIUM",
            "category": "Operations",
            "recommendation": "Audit data entry protocols and flag Z-score spikes",
            "reason": f"Found {anomalies_count} records exhibiting high deviations, indicating erratic operations or entry inconsistencies."
        })
        
    # Default fallback if no critical recommendations matched
    if not recommendations:
        recommendations.append({
            "priority": "LOW",
            "category": "General",
            "recommendation": "Maintain standard business operating parameters",
            "reason": "Business Pulse indicators, quality metrics, and performance columns show normal stability."
        })
        
    return recommendations
