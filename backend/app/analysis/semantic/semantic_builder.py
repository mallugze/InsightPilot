import pandas as pd
from typing import Dict, Any, List

from app.analysis.semantic.dataset_classifier import classify_dataset_domain
from app.analysis.semantic.entity_detector import detect_entity
from app.analysis.semantic.feature_classifier import classify_features
from app.analysis.semantic.relationship_detector import discover_relationships
from app.analysis.semantic.ml_readiness import evaluate_ml_readiness
from app.analysis.semantic.reasoning_engine import generate_understanding_explanation

def build_semantic_profile(df: pd.DataFrame, col_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ties together all modular semantic analyzers to output a comprehensive Semantic Profile
    describing domains, subdomains, features, relationships, visualizations, and ML readiness.
    """
    # 1. Hierarchical Domain & Subdomain classification
    domain, subdomain, characteristics, domain_conf = classify_dataset_domain(df, col_metadata)
    
    # 2. Row Entity Detector
    entity = detect_entity(df, col_metadata)
    
    # 3. Column Feature Categorizer
    features = classify_features(df, col_metadata)
    
    # 4. Structural Relationship Discovery
    relationships = discover_relationships(df, features)
    
    # 5. ML Suitability & Explainable Reasoning
    ml_readiness = evaluate_ml_readiness(df, relationships, features)
    
    # 6. Natural Reasoning summary explanation
    explanation = generate_understanding_explanation(
        domain, subdomain, entity, features, relationships, ml_readiness
    )

    # 7. Visualization Intent
    viz_intents = []
    dates = relationships.get("time_dimensions", [])
    metrics = relationships.get("primary_metrics", [])
    groups = relationships.get("grouping_dimensions", [])
    
    if dates and metrics:
        viz_intents.append({
            "intent": "Trend",
            "reasoning": f"Plotting timeline trend curves for metrics grouped by calendar stamps in '{dates[0]}'.",
            "suggested_columns": [dates[0]] + metrics[:1]
        })
    if groups and metrics:
        viz_intents.append({
            "intent": "Comparison",
            "reasoning": f"Comparing and ranking metrics against categorical dimensions such as '{groups[0]}'.",
            "suggested_columns": [groups[0]] + metrics[:1]
        })
        viz_intents.append({
            "intent": "Composition",
            "reasoning": f"Visualizing percentage share composition of '{groups[0]}' groups.",
            "suggested_columns": [groups[0]] + metrics[:1]
        })
    if len(metrics) >= 2:
        viz_intents.append({
            "intent": "Relationship",
            "reasoning": "Investigating linear correlations and relationships between continuous measures.",
            "suggested_columns": metrics[:2]
        })
    if metrics:
        viz_intents.append({
            "intent": "Distribution",
            "reasoning": f"Visualizing standard value spreads and outlier distribution ranges of '{metrics[0]}'.",
            "suggested_columns": metrics[:1]
        })

    # 8. KPI suggestions with aggregation strategy and reasoning
    kpi_suggs = []
    for feat in features:
        name = feat["name"]
        sem_type = feat["semantic_type"]
        
        if sem_type == "Currency":
            kpi_suggs.append({
                "metric_name": f"Total {name.replace('_', ' ').title()}",
                "aggregation_strategy": "SUM",
                "target_column": name,
                "reasoning": f"Summing values in '{name}' calculates the total cumulative currency yield."
            })
        elif sem_type == "Numeric" and "id" not in name.lower() and "no" not in name.lower():
            # Check if name looks like cost/expense or score
            if any(k in name.lower() for k in ["score", "grade", "gpa", "age", "rate", "percent", "margin"]):
                kpi_suggs.append({
                    "metric_name": f"Average {name.replace('_', ' ').title()}",
                    "aggregation_strategy": "MEAN",
                    "target_column": name,
                    "reasoning": f"Calculating the mean of '{name}' gauges normal baseline rates."
                })
            else:
                kpi_suggs.append({
                    "metric_name": f"Cumulative {name.replace('_', ' ').title()}",
                    "aggregation_strategy": "SUM",
                    "target_column": name,
                    "reasoning": f"Aggregating total '{name}' logs cumulative volume levels."
                })
        elif sem_type == "Primary Key":
            kpi_suggs.append({
                "metric_name": f"Total {entity} Count",
                "aggregation_strategy": "COUNT",
                "target_column": name,
                "reasoning": f"Counting unique row keys in '{name}' logs the total headcount volume."
            })

    # Limit to top 5 suggested KPIs
    kpi_suggs = kpi_suggs[:5]
    if not kpi_suggs:
        kpi_suggs.append({
            "metric_name": "Total Records",
            "aggregation_strategy": "COUNT",
            "target_column": columns[0]["name"] if columns else "id",
            "reasoning": "Fallback count of dataset row records."
        })

    # 9. Dashboard Layout Suggestions
    layout = "Metric Groupings Grid"
    if dates:
        layout = "Chronological Timeline"
    elif len(metrics) >= 3:
        layout = "Multi-variable Metrics Spread"
        
    dash_suggestions = {
        "layout": layout,
        "primary_widget": "Timeline Line Chart" if dates else "Categorical Bar Distribution",
        "secondary_widgets": ["KPI Metrics Cards Grid", "Pearson Correlation Heatmap", "Anomaly Outliers Alerts List"]
    }

    # 10. Report layout sections
    report_suggs = ["Executive Dataset Overview Profile", "Data Quality & Completeness Audit"]
    if dates:
        report_suggs.append("Historical Trend Timeline Analysis")
    if groups:
        report_suggs.append("Categorical Groupings & Segment Breakdown")
    if len(metrics) >= 2:
        report_suggs.append("Metric Correlations & Linear Relationships Matrix")
        
    ml_feats = [m for m, p in ml_readiness.items() if p["score"] >= 70]
    if ml_feats:
        report_suggs.append(f"Predictive Suitability & ML {', '.join([m.title() for m in ml_feats])} Projections")

    # 11. Chat Context metadata
    chat_context = {
        "dataset_domain": domain,
        "dataset_subdomain": subdomain,
        "row_entity": entity,
        "total_rows": len(df),
        "total_columns": len(features),
        "primary_keys": relationships.get("potential_targets", []),
        "timeline_keys": dates,
        "key_metrics": metrics[:4]
    }

    return {
        "domain": domain,
        "subdomain": subdomain,
        "characteristics": characteristics,
        "domain_confidence": domain_conf,
        "entity": entity,
        "features": features,
        "relationships": relationships,
        "ml_readiness": ml_readiness,
        "understanding_reasoning": explanation,
        "visualization_intent": viz_intents,
        "kpi_suggestions": kpi_suggs,
        "dashboard_suggestions": dash_suggestions,
        "report_suggestions": report_suggs,
        "chat_context": chat_context
    }
