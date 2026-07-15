import pandas as pd
from typing import Dict, Any, List

ENTITY_KEYWORDS = [
    ("patient", "Patient"),
    ("employee", "Employee"),
    ("staff", "Employee"),
    ("student", "Student"),
    ("customer", "Customer"),
    ("client", "Customer"),
    ("flower", "Flower"),
    ("sepal", "Flower"),
    ("petal", "Flower"),
    ("iris", "Flower"),
    ("passenger", "Passenger"),
    ("survived", "Passenger"),
    ("order", "Order"),
    ("invoice", "Order"),
    ("transaction", "Transaction"),
    ("product", "Product"),
    ("sku", "Product"),
    ("vehicle", "Vehicle"),
    ("car", "Vehicle"),
    ("sensor", "Sensor"),
    ("house", "Property"),
    ("home", "Property"),
    ("building", "Property")
]

def detect_entity(df: pd.DataFrame, col_metadata: Dict[str, Any]) -> str:
    """
    Scans column names to determine what each row in the dataset represents (e.g. Patient, Customer).
    Defaults to 'Generic Record' if no matching entity keywords are identified.
    """
    col_names_lower = [str(c["name"]).lower() for c in col_metadata.get("columns", [])]
    
    # Track votes for entity types based on column headers
    votes = {}
    for col_name in col_names_lower:
        for kw, entity_type in ENTITY_KEYWORDS:
            if kw in col_name:
                votes[entity_type] = votes.get(entity_type, 0) + 1
                
    if votes:
        # Sort by votes descending and get highest matching entity
        sorted_votes = sorted(votes.items(), key=lambda x: x[1], reverse=True)
        return sorted_votes[0][0]
        
    return "Generic Record"
