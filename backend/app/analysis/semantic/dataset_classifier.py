import pandas as pd
from typing import Dict, Any, List, Tuple

# Comprehensive multi-level registry
CLASSIFIER_REGISTRY = [
    {
        "domain": "Biology",
        "subdomain": "Botanical Classification",
        "use_case": "Iris Species Classification",
        "intent": "Flower Identification",
        "domain_kws": ["sepal", "petal", "iris", "species", "organism", "gene", "protein", "cell", "dna", "rna", "scientific", "flower"],
        "subdomain_kws": ["sepal", "petal", "iris", "species", "plant", "botany", "biology", "classification"],
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
        "domain_kws": ["revenue", "sales", "profit", "transaction", "order", "cost", "quantity", "price", "invoice", "deal"],
        "subdomain_kws": ["revenue", "sales", "transaction", "order", "invoice", "retail"],
        "use_case_kws": ["revenue", "profit", "cost", "margin", "forecast"],
        "intent_kws": ["optimization", "growth", "performance", "forecast", "planning"]
    },
    {
        "domain": "Financial",
        "subdomain": "Financial Intelligence",
        "use_case": "Ledger Accounting",
        "intent": "Expense Auditing",
        "domain_kws": ["ledger", "debit", "credit", "tax", "accounting", "asset", "expense", "budget", "finance", "financial"],
        "subdomain_kws": ["ledger", "debit", "credit", "accounting", "finance"],
        "use_case_kws": ["expense", "budget", "cost_center"],
        "intent_kws": ["audit", "compliance", "cost_control", "risk"]
    },
    {
        "domain": "HR",
        "subdomain": "Human Resources",
        "use_case": "Employee Management",
        "intent": "Attrition Prediction",
        "domain_kws": ["employee", "staff", "salary", "wage", "attrition", "hiring", "tenure", "hr", "workforce"],
        "subdomain_kws": ["employee", "staff", "tenure", "hr", "resources"],
        "use_case_kws": ["salary", "wage", "compensation"],
        "intent_kws": ["attrition", "retention", "turnover"]
    },
    {
        "domain": "Healthcare",
        "subdomain": "Patient Analytics",
        "use_case": "Clinical Patient Records",
        "intent": "Risk Analysis",
        "domain_kws": ["patient", "diagnosis", "disease", "symptoms", "doctor", "admitted", "prescription", "clinic", "medical"],
        "subdomain_kws": ["patient", "clinical", "admitted", "discharge"],
        "use_case_kws": ["diagnosis", "disease", "symptoms", "treatment"],
        "intent_kws": ["risk", "prognosis", "outcome", "survival"]
    },
    {
        "domain": "Real Estate",
        "subdomain": "Price Prediction",
        "use_case": "Housing Prices Valuation",
        "intent": "Price Regression",
        "domain_kws": ["house", "price", "room", "bedroom", "bathroom", "sqft", "lot", "zipcode", "mortgage", "real_estate"],
        "subdomain_kws": ["house", "price", "valuation", "housing"],
        "use_case_kws": ["bedroom", "bathroom", "sqft", "lot"],
        "intent_kws": ["price", "value", "valuation", "predict"]
    },
    {
        "domain": "Sensor",
        "subdomain": "IoT Monitoring",
        "use_case": "Sensor Telemetry Logs",
        "intent": "Anomaly Telemetry Monitoring",
        "domain_kws": ["sensor", "device", "temperature", "humidity", "telemetry", "timestamp", "voltage", "iot"],
        "subdomain_kws": ["sensor", "telemetry", "timestamp", "device", "reading"],
        "use_case_kws": ["temperature", "humidity", "voltage", "peak"],
        "intent_kws": ["anomaly", "alert", "monitoring", "failure"]
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
        "domain": "Student",
        "subdomain": "Educational Analytics",
        "use_case": "Student Performance Profiles",
        "intent": "Grade Projections",
        "domain_kws": ["student", "gpa", "score", "grade", "class", "enrollment", "course", "education"],
        "subdomain_kws": ["student", "grade", "academic"],
        "use_case_kws": ["gpa", "score", "grade", "test"],
        "intent_kws": ["projection", "performance", "prediction"]
    },
    {
        "domain": "Chemical",
        "subdomain": "Chemical Analysis",
        "use_case": "Wine Quality Analysis",
        "intent": "Quality Classification",
        "domain_kws": ["wine", "acidity", "alcohol", "quality", "sulfate", "density"],
        "subdomain_kws": ["wine", "quality", "chemical"],
        "use_case_kws": ["alcohol", "sulfate", "acidity"],
        "intent_kws": ["quality", "rating", "classification"]
    },
    {
        "domain": "Customer",
        "subdomain": "Retention Model",
        "use_case": "Customer Churn Analysis",
        "intent": "Churn Prediction",
        "domain_kws": ["churn", "customer", "retention", "tenure", "activity"],
        "subdomain_kws": ["customer", "churn", "retention"],
        "use_case_kws": ["tenure", "activity", "contract"],
        "intent_kws": ["churn", "retention", "prediction"]
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
