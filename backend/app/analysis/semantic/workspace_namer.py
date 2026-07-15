from typing import Dict, Any

def suggest_workspace_details(
    domain: str,
    subdomain: str,
    use_case: str,
    intent: str
) -> Dict[str, Any]:
    """
    Suggests user-friendly workspace branding coordinates: name, description, emoji icon, and color scheme.
    """
    suggested_name = "Analytics Workspace"
    short_desc = "Explore and segment data tables dynamically."
    emoji = "📊"
    color_theme = "blue"
    
    # Custom mappings
    if domain == "Scientific":
        suggested_name = f"{subdomain} Classification Study"
        short_desc = f"Experimental research tracking {subdomain.lower()} observations."
        emoji = "🌸" if subdomain == "Biology" else "🧪"
        color_theme = "pink" if subdomain == "Biology" else "teal"
        
    elif domain == "Machine Learning":
        suggested_name = f"{use_case} Study"
        short_desc = f"Training log benchmark analyzing label projections for {use_case.lower()}."
        emoji = "🚢" if "Titanic" in use_case else "🤖"
        color_theme = "slate"
        
    elif domain == "Business":
        if subdomain == "Sales":
            suggested_name = f"Q3 {subdomain} Analysis"
            short_desc = "Revenue performance dashboards mapping financial aggregates."
            emoji = "📈"
            color_theme = "emerald"
        elif subdomain == "Finance":
            suggested_name = "Expense Ledger Audit"
            short_desc = "Fiscal audit sheets tracking ledgers and balance flows."
            emoji = "💼"
            color_theme = "indigo"
        elif subdomain == "Human Resources":
            suggested_name = "Workforce Retention Dashboard"
            short_desc = "Staff turnover indices monitoring corporate headcounts."
            emoji = "👥"
            color_theme = "cyan"
            
    elif domain == "Healthcare":
        suggested_name = "Patient Risk Analysis"
        short_desc = "Clinical charts tracking diagnosis anomalies and patient safety."
        emoji = "🏥"
        color_theme = "red"
        
    elif domain == "Real Estate":
        suggested_name = "Housing Market Valuation"
        short_desc = "Listing prices regression and property attribute evaluations."
        emoji = "🏠"
        color_theme = "amber"
        
    elif domain == "IoT":
        suggested_name = "Sensor Telemetry Feed"
        short_desc = "Real-time hardware sensor monitoring logs and anomaly alerts."
        emoji = "🌦"
        color_theme = "orange"

    return {
        "suggested_workspace_name": suggested_name,
        "short_description": short_desc,
        "suggested_icon": emoji,
        "color_theme": color_theme
    }
