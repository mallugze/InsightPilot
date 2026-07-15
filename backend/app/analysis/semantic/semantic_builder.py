import pandas as pd
from typing import Dict, Any, List

from app.analysis.semantic.dataset_classifier import classify_hierarchical_domain
from app.analysis.semantic.entity_detector import detect_entity
from app.analysis.semantic.feature_classifier import classify_features
from app.analysis.semantic.relationship_detector import discover_relationships
from app.analysis.semantic.ml_readiness import evaluate_ml_readiness
from app.analysis.semantic.kpi_discovery import discover_kpis
from app.analysis.semantic.chart_selector import select_charts
from app.analysis.semantic.workspace_namer import suggest_workspace_details
from app.analysis.semantic.summary_builder import build_executive_summary
from app.analysis.semantic.dashboard_builder import compose_dashboard

def build_semantic_profile(df: pd.DataFrame, col_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assembles a complete Semantic Profile by orchestrating the hierarchical domain classifiers,
    dynamic KPI discovery engines, chart selectors, workspace namers, and summary generators.
    """
    # 1. Multi-Level Dataset Classification
    domain_match = classify_hierarchical_domain(df, col_metadata)
    domain = domain_match["domain"]
    subdomain = domain_match["subdomain"]
    use_case = domain_match["use_case"]
    intent = domain_match["intent"]
    
    # 2. Row Entity Detector
    entity = detect_entity(df, col_metadata)
    
    # 3. Feature Classifications
    features = classify_features(df, col_metadata)
    
    # 4. Relationships discovery
    relationships = discover_relationships(df, features)
    
    # 5. ML suitability
    ml_readiness = evaluate_ml_readiness(df, relationships, features)
    
    # 6. KPI Discovery Engine (returns aggregation strategy, reasoning, and selection explanation)
    kpis = discover_kpis(df, features, relationships, domain)
    
    # 7. Chart Selection Engine
    chart_recommendations = select_charts(df, features, relationships)
    
    # 8. Workspace Naming Engine
    workspace_suggestions = suggest_workspace_details(domain, subdomain, use_case, intent)
    
    # 9. Adaptive Executive Summary Generator
    exec_summary = build_executive_summary(
        domain,
        subdomain,
        entity,
        len(df),
        relationships.get("primary_metrics", []),
        relationships.get("grouping_dimensions", []),
        ml_readiness
    )
    
    # 10. Dashboard Composition Builder
    dashboard_sections = compose_dashboard(
        domain,
        subdomain,
        relationships.get("primary_metrics", []),
        relationships.get("grouping_dimensions", []),
        relationships.get("time_dimensions", [])
    )
    
    # 11. Multi-level Confidence Mapping
    target_confidence = 0.50
    targets = relationships.get("potential_targets", [])
    if targets:
        target_confidence = next((f["confidence"] for f in features if f["name"] == targets[0]), 0.90)
        
    chart_confidence = max([c["confidence"] for c in chart_recommendations]) if chart_recommendations else 0.50
    ml_confidence = max([m["score"] / 100.0 for m in ml_readiness.values()]) if ml_readiness else 0.50
    entity_confidence = 0.90 if entity != "Generic Record" else 0.50
    
    overall_confidence = round(
        (domain_match["overall_confidence"] * 0.3) +
        (entity_confidence * 0.2) +
        (target_confidence * 0.2) +
        (chart_confidence * 0.15) +
        (ml_confidence * 0.15),
        2
    )
    
    # 12. Quality Metric Heuristics
    missing_ratio = df.isnull().sum().sum() / (df.size if df.size > 0 else 1)
    if missing_ratio < 0.01:
        quality = "Excellent"
    elif missing_ratio < 0.05:
        quality = "Good"
    elif missing_ratio < 0.15:
        quality = "Fair"
    else:
        quality = "Poor"
        
    # 13. Suggested ML Algorithms reasoning list
    suggested_models = []
    if ml_readiness.get("classification", {}).get("score", 0) >= 70:
        suggested_models.extend(["Random Forest Classifier", "XGBoost", "Logistic Regression"])
    if ml_readiness.get("regression", {}).get("score", 0) >= 70:
        suggested_models.extend(["Linear Regression", "Ridge Regression", "Gradient Boosting Regressor"])
    if ml_readiness.get("forecasting", {}).get("score", 0) >= 70:
        suggested_models.extend(["Prophet", "ARIMA", "Exponential Smoothing"])
    if ml_readiness.get("clustering", {}).get("score", 0) >= 70:
        suggested_models.extend(["K-Means", "DBSCAN"])
        
    if not suggested_models:
        suggested_models = ["Descriptive Aggregations", "Frequency Histograms"]

    # 14. Suggestions lists
    report_suggestions = ["Executive Dataset Overview Profile", "Data Quality & Completeness Audit"]
    if relationships.get("time_dimensions", []):
        report_suggestions.append("Historical Trend Timeline Analysis")
    if relationships.get("grouping_dimensions", []):
        report_suggestions.append("Categorical Groupings & Segment Breakdown")
    if ml_readiness.get("classification", {}).get("score", 0) >= 70 or ml_readiness.get("regression", {}).get("score", 0) >= 70:
        report_suggestions.append("Predictive Suitability & ML Projections")

    # Combine into a unified Semantic Profile
    profile = {
        # Hierarchical domain classification
        "domain": domain,
        "subdomain": subdomain,
        "use_case": use_case,
        "intent": intent,
        "characteristics": domain_match["domain"] + " tabular data file supporting " + domain_match["use_case"],
        
        # Identity
        "entity": entity,
        "features": features,
        "relationships": relationships,
        "ml_readiness": ml_readiness,
        "understanding_reasoning": exec_summary,
        "visualization_intent": chart_recommendations,
        "kpi_suggestions": kpis,
        
        # Dynamic Dashboard layouts
        "dashboard_sections": dashboard_sections,
        
        # Workspace Suggestion Info
        "suggested_workspace_name": workspace_suggestions["suggested_workspace_name"],
        "short_description": workspace_suggestions["short_description"],
        "suggested_icon": workspace_suggestions["suggested_icon"],
        "color_theme": workspace_suggestions["color_theme"],
        
        # ML Algorithms suggestions
        "suggested_models": suggested_models,
        
        # Quality
        "quality": quality,
        
        # Multi-level Confidence scores
        "domain_confidence": domain_match["domain_confidence"],
        "subdomain_confidence": domain_match["subdomain_confidence"],
        "use_case_confidence": domain_match["use_case_confidence"],
        "intent_confidence": domain_match["intent_confidence"],
        "entity_confidence": entity_confidence,
        "target_confidence": target_confidence,
        "chart_confidence": chart_confidence,
        "ml_readiness_confidence": ml_confidence,
        "overall_confidence": overall_confidence,
        
        # Context mappings for reports
        "report_suggestions": report_suggestions,
        "chat_context": {
            "dataset_domain": domain,
            "dataset_subdomain": subdomain,
            "row_entity": entity,
            "total_rows": len(df),
            "total_columns": len(features)
        }
    }
    
    return profile
