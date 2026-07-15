from typing import Dict, Any, List

def compose_dashboard(
    domain: str,
    subdomain: str,
    metrics: List[str],
    groups: List[str],
    time_cols: List[str]
) -> List[Dict[str, Any]]:
    """
    Composes a list of reusable dashboard sections to render dynamically on the frontend.
    Sections: header, kpis, primary_chart, secondary_charts, insights, recommendations, ml_readiness, developer_panel.
    """
    sections = []
    
    # 1. Header Section
    sections.append({
        "id": "header",
        "type": "header_block",
        "title": "Adaptive Executive Brief",
        "visible": True
    })
    
    # 2. KPI Section
    sections.append({
        "id": "kpis",
        "type": "kpis_grid",
        "title": "Core Domain KPIs",
        "visible": True
    })
    
    # 3. Primary Chart Section
    primary_chart_type = "Histogram"
    if time_cols:
        primary_chart_type = "Line Chart"
    elif groups:
        primary_chart_type = "Bar Chart"
        
    sections.append({
        "id": "primary_chart",
        "type": "chart_widget",
        "title": f"Primary {primary_chart_type} Visualization",
        "chart_type": primary_chart_type,
        "visible": True
    })
    
    # 4. Secondary Charts (Outliers, Correlations etc.)
    secondary_widgets = []
    if len(metrics) >= 2:
        secondary_widgets.append("Correlation Heatmap")
    secondary_widgets.append("Statistical Outliers Alerts")
    
    sections.append({
        "id": "secondary_charts",
        "type": "charts_split_grid",
        "title": "Supporting Analytical Inferences",
        "widgets": secondary_widgets,
        "visible": True
    })
    
    # 5. Insights
    sections.append({
        "id": "insights",
        "type": "bullet_insights",
        "title": "Deterministic Insights Log",
        "visible": True
    })
    
    # 6. Recommendations
    sections.append({
        "id": "recommendations",
        "type": "advisory_list",
        "title": "Adaptive Action Recommendations",
        "visible": True
    })
    
    # 7. ML Readiness
    sections.append({
        "id": "ml_readiness",
        "type": "ml_suitability_matrix",
        "title": "Machine Learning Readiness Evaluation",
        "visible": True
    })
    
    # 8. Developer Inspector Panel
    sections.append({
        "id": "developer_panel",
        "type": "dataset_intelligence_panel",
        "title": "Dataset Intelligence Panel",
        "visible": True
    })
    
    return sections
