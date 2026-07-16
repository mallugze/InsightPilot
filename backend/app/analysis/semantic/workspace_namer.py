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
    if domain == "Biology" or subdomain == "Botanical Classification":
        suggested_name = "Iris Flower Classification Study" if "Iris" in use_case else f"{subdomain} Classification"
        short_desc = f"Experimental research tracking botanical observations and flower specimens."
        emoji = "🌸"
        color_theme = "pink"
        
    elif domain == "Machine Learning" or subdomain == "Survival Analysis":
        suggested_name = "Titanic Survival Study" if "Titanic" in use_case else f"{use_case} Study"
        short_desc = f"Training log benchmark analyzing classification model projections for {use_case.lower()}."
        emoji = "🚢" if "Titanic" in use_case else "🤖"
        color_theme = "slate"
        
    elif domain == "Business" or subdomain == "Retail Analytics":
        suggested_name = "Q3 Revenue Dashboard" if "Sales" in use_case or "Revenue" in use_case else f"{subdomain} Dashboard"
        short_desc = "Revenue performance dashboards mapping retail transactions and sales margins."
        emoji = "📈"
        color_theme = "emerald"
        
    elif domain == "Financial" or subdomain == "Financial Intelligence":
        suggested_name = "Expense Ledger Audit"
        short_desc = "Fiscal audit sheets tracking ledgers, credits, and balance flows."
        emoji = "💼"
        color_theme = "indigo"
        
    elif domain == "HR" or subdomain == "Human Resources":
        suggested_name = "Workforce Retention Dashboard"
        short_desc = "Staff turnover indices monitoring corporate employee headcounts."
        emoji = "👥"
        color_theme = "cyan"
            
    elif domain == "Healthcare" or subdomain == "Patient Analytics":
        suggested_name = "Patient Risk Analysis"
        short_desc = "Clinical charts tracking diagnosis anomalies and patient admissions safety."
        emoji = "🏥"
        color_theme = "red"
        
    elif domain == "Real Estate" or subdomain == "Price Prediction":
        suggested_name = "Housing Market Valuation"
        short_desc = "Listing prices regression and property attribute evaluations."
        emoji = "🏠"
        color_theme = "amber"
        
    elif domain == "Sensor" or subdomain == "IoT Monitoring":
        suggested_name = "Sensor Telemetry Feed"
        short_desc = "Real-time hardware sensor monitoring logs and anomaly alerts."
        emoji = "🌦"
        color_theme = "orange"
        
    elif domain == "Weather" or subdomain == "Climate Analytics":
        suggested_name = "Climate Trend Analysis"
        short_desc = "Temporal weather tracking and climate trend forecasting graphs."
        emoji = "🌦"
        color_theme = "teal"
        
    elif domain == "Student" or subdomain == "Educational Analytics":
        suggested_name = "Student Performance Analysis"
        short_desc = "Academic grade performance profiles and student GPA distributions."
        emoji = "🎓"
        color_theme = "blue"

    return {
        "suggested_workspace_name": suggested_name,
        "short_description": short_desc,
        "suggested_icon": emoji,
        "color_theme": color_theme
    }
