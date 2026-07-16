from typing import Dict, Any, List

def generate_insights(
    dataset_type: str,
    kpis: Dict[str, Any],
    pulse: Dict[str, Any],
    trends: Dict[str, Any],
    anomalies: Dict[str, Any],
    correlations: Dict[str, Any],
    hero_zero: Dict[str, Any]
) -> List[str]:
    """
    Generates deterministic, template-based insights and observations from statistical analysis,
    ensuring formatting (like dollar signs) only applies to currency-inferred columns.
    """
    insights = []
    
    # 1. Dataset size description
    # Dynamically extract record counts from various domain KPI keys
    record_count = next((v for k, v in kpis.items() if any(x in k for x in ["records", "samples", "logged", "patients", "instances", "readings", "days"])), len(df) if 'df' in locals() else 'N/A')
    
    insights.append(
        f"Analyzed '{dataset_type}' dataset. The analytical profile contains {record_count} observations "
        f"across continuous measures and categorical segment groups, yielding a data quality rating of {pulse.get('score', 100.0)}/100."
    )
    
    # 2. Key KPI findings for business domains
    if dataset_type == "Sales":
        insights.append(
            f"Total gross sales revenue amounted to ${kpis.get('total_revenue', 0.0):,.2f} "
            f"across {kpis.get('total_orders', 0)} transactions, averaging ${kpis.get('average_order_value', 0.0):,.2f} per order."
        )
        insights.append(
            f"Profit margin stands at a {kpis.get('profit_margin', 0.0)}% average, "
            f"yielding a cumulative net profit of ${kpis.get('total_profit', 0.0):,.2f} across the customer base."
        )
    elif dataset_type == "HR":
        insights.append(
            f"Active employee headcount is {kpis.get('employee_count', 0)} staff members, "
            f"with salary ranges averaging ${kpis.get('average_salary', 0.0):,.2f} per employee."
        )
        if kpis.get("attrition_rate", 0.0) > 0:
            insights.append(
                f"Statistical attrition rate sits at {kpis.get("attrition_rate", 0.0)}%, "
                f"which marks the percentage of left/terminated staff contracts."
            )
    elif dataset_type == "Finance":
        insights.append(
            f"Total tracked cash inflows reached ${kpis.get('total_income', 0.0):,.2f} "
            f"against total operating outflows of ${kpis.get('total_expense', 0.0):,.2f}."
        )
        insights.append(
            f"Net operating surplus is ${kpis.get('net_profit', 0.0):,.2f}, representing a {kpis.get('profit_margin', 0.0)}% operational yield."
        )
        
    # 3. Performance bounds (Hero/Zero)
    if hero_zero.get("metric_name") != "None":
        metric_name = hero_zero.get("metric_name", "")
        # Apply currency formatting only if metric has currency-related name
        is_money = any(m in metric_name.lower() for m in ["revenue", "profit", "cost", "price", "wage", "salary", "expense", "fare"])
        
        hero_val = hero_zero.get("hero_value", 0.0)
        zero_val = hero_zero.get("zero_value", 0.0)
        
        hero_formatted = f"${hero_val:,.2f}" if is_money else f"{hero_val:,.2f}"
        zero_formatted = f"${zero_val:,.2f}" if is_money else f"{zero_val:,.2f}"
        
        insights.append(
            f"Outliers breakdown: '{hero_zero.get('hero_name')}' registered the highest "
            f"{metric_name} ({hero_formatted}), whereas '{hero_zero.get('zero_name')}' represented the lowest ({zero_formatted})."
        )
        
    # 4. Trend trajectory
    if trends.get("has_trends"):
        dir_val = trends.get("trend_direction", "Stable")
        growth = trends.get("growth_percent", 0.0)
        insights.append(
            f"Chronological trend: '{trends.get('metric_name')}' displays a '{dir_val}' trajectory "
            f"with an overall growth deviation of {growth:+.1f}% across the timeline."
        )
        
    # 5. Correlation observations
    corrs = correlations.get("correlations", [])
    if corrs:
        top_corr = corrs[0]
        insights.append(
            f"Statistical correlation: Column '{top_corr['column_a']}' has a '{top_corr['strength']}' "
            f"link ({top_corr['coefficient']:+.2f}) with '{top_corr['column_b']}'."
        )
        
    # 6. Anomaly alerts
    anom_cnt = anomalies.get("anomalies_count", 0)
    if anom_cnt > 0:
        insights.append(
            f"Outlier diagnostics: Identified {anom_cnt} values deviating outside typical ranges (Z-score > 2.0) "
            f"consisting of {anomalies.get('high_anomalies', 0)} positive spikes and {anomalies.get('low_anomalies', 0)} drops."
        )
        
    return insights
