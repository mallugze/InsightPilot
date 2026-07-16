import pandas as pd
from typing import Dict, Any, List, Tuple

# Comprehensive multi-level registry covering all Sprint 9 domains
CLASSIFIER_REGISTRY = [
    {
        "domain": "Biology",
        "subdomain": "Botanical Classification",
        "use_case": "Iris Species Classification",
        "intent": "Flower Identification",
        "domain_kws": ["sepal", "petal", "iris", "species", "organism", "plant", "botany", "biology"],
        "subdomain_kws": ["sepal", "petal", "iris", "species", "plant", "botany", "biology"],
        "use_case_kws": ["sepal", "petal", "iris", "setosa", "versicolor", "virginica"],
        "intent_kws": ["species", "class", "prediction", "predict", "target", "identification"]
    },
    {
        "domain": "Machine Learning",
        "subdomain": "Survival Analysis",
        "use_case": "Titanic Passenger Outcomes",
        "intent": "Survival Prediction",
        "domain_kws": ["survived", "passenger", "titanic", "pclass", "sibling", "parent", "embarked", "ml", "classification"],
        "subdomain_kws": ["passenger", "titanic", "ticket", "cabin", "fare"],
        "use_case_kws": ["survived", "titanic", "pclass", "cabin"],
        "intent_kws": ["survived", "predict", "survival"]
    },
    {
        "domain": "Business",
        "subdomain": "Retail Analytics",
        "use_case": "Revenue Analytics",
        "intent": "Revenue Optimization",
        "domain_kws": ["revenue", "sales", "profit", "transaction", "order", "cost", "quantity", "price", "invoice", "deal", "margin"],
        "subdomain_kws": ["revenue", "sales", "transaction", "order", "invoice", "retail", "deals"],
        "use_case_kws": ["revenue", "profit", "cost", "margin", "forecast", "growth"],
        "intent_kws": ["optimization", "growth", "performance", "forecast", "planning"]
    },
    {
        "domain": "Sales",
        "subdomain": "Sales Performance",
        "use_case": "Sales Growth Forecasting",
        "intent": "Revenue Optimization",
        "domain_kws": ["sales_target", "quota", "leads", "revenue_projection", "sales_funnel"],
        "subdomain_kws": ["quota", "leads", "funnel", "pipeline"],
        "use_case_kws": ["leads", "funnel", "projections"],
        "intent_kws": ["optimization", "growth", "planning"]
    },
    {
        "domain": "Finance",
        "subdomain": "Corporate Finance",
        "use_case": "Financial Auditing",
        "intent": "Risk Assessment",
        "domain_kws": ["ledger", "debit", "credit", "tax", "accounting", "asset", "expense", "budget", "finance", "financial", "ebitda"],
        "subdomain_kws": ["ledger", "debit", "credit", "accounting", "finance", "corporate"],
        "use_case_kws": ["expense", "budget", "cost_center", "auditing"],
        "intent_kws": ["audit", "compliance", "cost_control", "risk", "valuation"]
    },
    {
        "domain": "Marketing",
        "subdomain": "Campaign Performance",
        "use_case": "Ad Spend Tracking",
        "intent": "ROI Optimization",
        "domain_kws": ["marketing", "campaign", "ad_spend", "clicks", "impressions", "ctr", "cpc", "lead", "conversion", "roi"],
        "subdomain_kws": ["campaign", "clicks", "impressions", "ctr", "ad_spend"],
        "use_case_kws": ["ad_spend", "budget", "spent", "roi"],
        "intent_kws": ["optimization", "performance", "return", "conversion"]
    },
    {
        "domain": "Retail",
        "subdomain": "Inventory Valuation",
        "use_case": "Inventory Management",
        "intent": "Stock Forecasting",
        "domain_kws": ["inventory", "stock", "warehouse", "reorder", "skus", "supplier", "product", "retail", "store"],
        "subdomain_kws": ["inventory", "stock", "skus", "warehouse"],
        "use_case_kws": ["reorder", "supplier", "store", "product_category"],
        "intent_kws": ["forecasting", "turnover", "stock_control", "replenishment"]
    },
    {
        "domain": "Healthcare",
        "subdomain": "Patient Analytics",
        "use_case": "Clinical Patient Records",
        "intent": "Risk Analysis",
        "domain_kws": ["patient", "diagnosis", "disease", "symptoms", "doctor", "admitted", "prescription", "clinic", "medical", "admissions", "mortality"],
        "subdomain_kws": ["patient", "clinical", "admitted", "discharge"],
        "use_case_kws": ["diagnosis", "disease", "symptoms", "treatment"],
        "intent_kws": ["risk", "prognosis", "outcome", "survival"]
    },
    {
        "domain": "Manufacturing",
        "subdomain": "Production Analytics",
        "use_case": "Quality Control",
        "intent": "Defect Reduction",
        "domain_kws": ["manufacturing", "production", "machine", "assembly", "defect", "yield", "output", "sensor", "factory"],
        "subdomain_kws": ["production", "factory", "assembly", "yield"],
        "use_case_kws": ["defect", "quality", "control", "maintenance"],
        "intent_kws": ["reduction", "optimization", "uptime", "efficiency"]
    },
    {
        "domain": "Agriculture",
        "subdomain": "Crop Yield Tracking",
        "use_case": "Yield Projections",
        "intent": "Harvest Scheduling",
        "domain_kws": ["agriculture", "crop", "yield", "harvest", "soil", "moisture", "farming", "farm", "fertilizer"],
        "subdomain_kws": ["crop", "yield", "harvest", "farming"],
        "use_case_kws": ["projection", "fertilizer", "moisture"],
        "intent_kws": ["scheduling", "optimization", "planning"]
    },
    {
        "domain": "Government",
        "subdomain": "Public Census",
        "use_case": "Population Demographics",
        "intent": "Resource Allocation",
        "domain_kws": ["government", "public", "census", "citizen", "population", "taxpayer", "district", "municipal", "demographics"],
        "subdomain_kws": ["census", "population", "demographics"],
        "use_case_kws": ["district", "municipal", "taxpayer"],
        "intent_kws": ["resource", "allocation", "planning", "policy"]
    },
    {
        "domain": "Weather",
        "subdomain": "Climate Analytics",
        "use_case": "Climate Trend Tracking",
        "intent": "Climate Trend Forecasting",
        "domain_kws": ["weather", "rain", "temperature", "humidity", "climate", "precipitation", "wind", "forecast"],
        "subdomain_kws": ["weather", "climate", "meteorological"],
        "use_case_kws": ["rain", "precipitation", "wind", "temp"],
        "intent_kws": ["forecast", "trends", "analysis"]
    },
    {
        "domain": "IoT",
        "subdomain": "Device Monitoring",
        "use_case": "IoT Sensor Logs",
        "intent": "Anomaly Detection",
        "domain_kws": ["sensor", "device", "temperature", "humidity", "telemetry", "timestamp", "voltage", "iot", "ping", "packet"],
        "subdomain_kws": ["sensor", "telemetry", "timestamp", "device", "reading", "iot"],
        "use_case_kws": ["temperature", "humidity", "voltage", "peak"],
        "intent_kws": ["anomaly", "alert", "monitoring", "failure", "detection"]
    },
    {
        "domain": "Education",
        "subdomain": "Academic Performance",
        "use_case": "Student Profiles",
        "intent": "Grade Projections",
        "domain_kws": ["student", "gpa", "score", "grade", "class", "enrollment", "course", "education", "school", "exam"],
        "subdomain_kws": ["student", "grade", "academic", "course", "education"],
        "use_case_kws": ["gpa", "score", "grade", "test"],
        "intent_kws": ["projection", "performance", "prediction"]
    },
    {
        "domain": "Scientific",
        "subdomain": "Experiment Analysis",
        "use_case": "Laboratory Measurement",
        "intent": "Hypothesis Testing",
        "domain_kws": ["scientific", "laboratory", "experiment", "sample", "control", "treatment", "trial", "observed"],
        "subdomain_kws": ["experiment", "sample", "laboratory", "scientific", "measurement"],
        "use_case_kws": ["control", "treatment", "trial", "observed"],
        "intent_kws": ["hypothesis", "significance", "p_value"]
    },
    {
        "domain": "Biology",
        "subdomain": "Genetics Analysis",
        "use_case": "Gene Expression",
        "intent": "Pathogenicity Identification",
        "domain_kws": ["gene", "protein", "cell", "dna", "rna", "sequence", "mutation", "pathogen", "chromosome", "biology"],
        "subdomain_kws": ["gene", "protein", "dna", "rna", "mutation", "biology"],
        "use_case_kws": ["sequence", "expression", "chromosome"],
        "intent_kws": ["pathogenicity", "identification", "disease"]
    },
    {
        "domain": "Transportation",
        "subdomain": "Logistics Routing",
        "use_case": "Fleet Delivery Logs",
        "intent": "Route Optimization",
        "domain_kws": ["transportation", "logistics", "fleet", "delivery", "route", "shipment", "carrier", "distance", "vehicle"],
        "subdomain_kws": ["logistics", "fleet", "delivery", "route"],
        "use_case_kws": ["shipment", "carrier", "distance"],
        "intent_kws": ["optimization", "efficiency", "cost_control"]
    },
    {
        "domain": "Sports",
        "subdomain": "Player Statistics",
        "use_case": "Athlete Performance Metrics",
        "intent": "Game Win Projection",
        "domain_kws": ["sports", "player", "athlete", "score", "game", "team", "points", "match", "win", "loss"],
        "subdomain_kws": ["player", "athlete", "stats", "sports"],
        "use_case_kws": ["score", "points", "goals", "assists"],
        "intent_kws": ["projection", "win", "prediction", "match_outcome"]
    },
    {
        "domain": "Energy",
        "subdomain": "Grid Telemetry",
        "use_case": "Power Consumption Analysis",
        "intent": "Demand Forecasting",
        "domain_kws": ["energy", "power", "grid", "consumption", "electricity", "watt", "utility", "load", "kw", "generator"],
        "subdomain_kws": ["power", "grid", "consumption"],
        "use_case_kws": ["load", "kw", "watt"],
        "intent_kws": ["forecasting", "demand", "peak"]
    },
    {
        "domain": "Economics",
        "subdomain": "Macroeconomic Indices",
        "use_case": "Inflation Analysis",
        "intent": "Market Projections",
        "domain_kws": ["economics", "inflation", "cpi", "gdp", "unemployment", "interest_rate", "macroeconomics", "index", "currency"],
        "subdomain_kws": ["inflation", "gdp", "unemployment", "macroeconomics"],
        "use_case_kws": ["index", "cpi", "rate"],
        "intent_kws": ["projections", "forecast", "trends"]
    },
    {
        "domain": "Customer Analytics",
        "subdomain": "User Cohort Audits",
        "use_case": "Customer Churn Analysis",
        "intent": "Churn Retention",
        "domain_kws": ["churn", "customer", "retention", "tenure", "activity", "subscription", "cohort", "user", "engagement"],
        "subdomain_kws": ["customer", "cohort", "retention"],
        "use_case_kws": ["tenure", "activity", "contract"],
        "intent_kws": ["churn", "retention", "prediction"]
    },
    {
        "domain": "Forecasting",
        "subdomain": "Time-series Models",
        "use_case": "Sales Projection",
        "intent": "Trend Strength Forecasting",
        "domain_kws": ["forecast", "projection", "trend", "seasonal", "arima", "prophet", "timeseries", "dates", "chronological"],
        "subdomain_kws": ["forecast", "projection", "trend"],
        "use_case_kws": ["arima", "prophet", "timeseries"],
        "intent_kws": ["forecasting", "strength", "trends"]
    }
]

def calculate_kws_confidence(col_names: List[str], keywords: List[str]) -> float:
    """
    Returns a confidence rating [0.0, 1.0] based on matching keyword overlaps.
    """
    matches = 0
    for name in col_names:
        if any(kw in name for kw in keywords):
            matches += 1
            
    if matches == 0:
        return 0.0
    ratio = matches / len(col_names)
    return round(min(0.99, 0.50 + (ratio * 0.49)), 2)

def classify_hierarchical_domain(df: pd.DataFrame, col_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classifies datasets hierarchically: Domain -> Subdomain -> Use Case -> Intent.
    Returns dictionaries of keys and independent confidence levels.
    """
    columns = col_metadata.get("columns", [])
    col_names_lower = [str(c["name"]).lower() for c in columns]
    
    best_match = {
        "domain": "Generic",
        "subdomain": "Generic Spreadsheet",
        "use_case": "General Analysis",
        "intent": "Spreadsheet Profiling",
        "domain_confidence": 0.50,
        "subdomain_confidence": 0.50,
        "use_case_confidence": 0.50,
        "intent_confidence": 0.50,
        "overall_confidence": 0.50
    }
    
    if not col_names_lower:
        return best_match
        
    highest_overall = 0.50
    
    for item in CLASSIFIER_REGISTRY:
        d_conf = calculate_kws_confidence(col_names_lower, item["domain_kws"])
        s_conf = calculate_kws_confidence(col_names_lower, item["subdomain_kws"])
        u_conf = calculate_kws_confidence(col_names_lower, item["use_case_kws"])
        i_conf = calculate_kws_confidence(col_names_lower, item["intent_kws"])
        
        overall = round((d_conf * 0.4) + (s_conf * 0.3) + (u_conf * 0.2) + (i_conf * 0.1), 2)
        
        if overall > highest_overall:
            highest_overall = overall
            best_match = {
                "domain": item["domain"],
                "subdomain": item["subdomain"],
                "use_case": item["use_case"],
                "intent": item["intent"],
                "domain_confidence": d_conf if d_conf > 0 else 0.50,
                "subdomain_confidence": s_conf if s_conf > 0 else 0.50,
                "use_case_confidence": u_conf if u_conf > 0 else 0.50,
                "intent_confidence": i_conf if i_conf > 0 else 0.50,
                "overall_confidence": overall
            }
            
    return best_match
