import pandas as pd
from typing import Dict, Any, List, Tuple

# Registry of domain classifiers. Extensible design.
DOMAIN_REGISTRY = [
    {
        "domain": "Scientific",
        "subdomain": "Biology",
        "keywords": ["sepal", "petal", "species", "iris", "organism", "gene", "protein", "dna", "rna", "cell", "scientific"],
        "characteristics": "Biological measurements or taxonomy classifications with numerical attributes."
    },
    {
        "domain": "Machine Learning",
        "subdomain": "Classification Benchmark",
        "keywords": ["survived", "passenger", "titanic", "class", "target", "label", "iris", "species", "feature", "prediction"],
        "characteristics": "Benchmark datasets with clear independent variables and categorical labels."
    },
    {
        "domain": "Business",
        "subdomain": "Sales",
        "keywords": ["revenue", "sales", "revenue_usd", "amount", "profit", "transaction", "order", "cost", "quantity", "price"],
        "characteristics": "Transactional records tracing consumer transactions and profitability metrics."
    },
    {
        "domain": "Business",
        "subdomain": "Finance",
        "keywords": ["income", "receipt", "debit", "credit", "expense", "budget", "ledger", "tax", "accounting"],
        "characteristics": "Corporate ledgers tracking financial inflows, outflows, and fiscal accounts."
    },
    {
        "domain": "Business",
        "subdomain": "Human Resources",
        "keywords": ["employee", "attrition", "staff", "salary", "wage", "department", "tenure", "hr", "workforce", "hiring"],
        "characteristics": "Corporate staff logs monitoring headcount, attrition, and compensation distributions."
    },
    {
        "domain": "Business",
        "subdomain": "Inventory",
        "keywords": ["stock", "quantity", "warehouse", "sku", "supplier", "reorder", "inventory", "product_id"],
        "characteristics": "Logistics stock files monitoring product availability and shelf levels."
    },
    {
        "domain": "Healthcare",
        "subdomain": "Clinical Records",
        "keywords": ["patient", "diagnosis", "doctor", "disease", "treatment", "admitted", "symptoms", "prescription", "clinic"],
        "characteristics": "Patient records tracing clinical status, diagnostics, and treatments."
    },
    {
        "domain": "Education",
        "subdomain": "Student Performance",
        "keywords": ["student", "grade", "score", "class", "course", "teacher", "enrollment", "gpa", "exam", "school"],
        "characteristics": "Academic score registries tracking student progress and subject assessments."
    },
    {
        "domain": "Real Estate",
        "subdomain": "Housing Prices",
        "keywords": ["house", "price", "room", "bedroom", "bathroom", "sqft", "lot", "zipcode", "mortgage", "real_estate"],
        "characteristics": "Property listings tracking housing attributes and market pricing valuations."
    },
    {
        "domain": "IoT",
        "subdomain": "Sensor Telemetry",
        "keywords": ["sensor", "temperature", "humidity", "device_id", "value", "telemetry", "metric", "timestamp"],
        "characteristics": "Time series logs capturing machine sensor readings and environment telemetry."
    }
]

def classify_dataset_domain(df: pd.DataFrame, col_metadata: Dict[str, Any]) -> Tuple[str, str, str, float]:
    """
    Analyzes columns, types, and keyword associations to classify the dataset.
    Returns: (domain, subdomain, characteristics, confidence_score)
    """
    col_names_lower = [str(c["name"]).lower() for c in col_metadata.get("columns", [])]
    total_cols = len(col_names_lower)
    
    if total_cols == 0:
        return "Generic", "Generic Spreadsheet", "Generic tabular data structure.", 0.50

    best_domain = "Generic"
    best_subdomain = "Generic Spreadsheet"
    best_char = "Generic tabular data structure with no strongly matched semantic keywords."
    max_confidence = 0.50

    for registry_item in DOMAIN_REGISTRY:
        matches = 0
        keywords = registry_item["keywords"]
        
        # Count keyword overlap in column headers
        for col_name in col_names_lower:
            if any(kw in col_name for kw in keywords):
                matches += 1
                
        # Confidence logic: ratio of matching columns + base weight
        if matches > 0:
            match_ratio = matches / total_cols
            # Calculate a confidence score bounded by [0.6, 0.99]
            confidence = min(0.99, 0.60 + (match_ratio * 0.40))
            
            if confidence > max_confidence:
                max_confidence = confidence
                best_domain = registry_item["domain"]
                best_subdomain = registry_item["subdomain"]
                best_char = registry_item["characteristics"]
                
    return best_domain, best_subdomain, best_char, round(max_confidence, 2)
