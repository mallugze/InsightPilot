import re
from typing import List

# Domain mapping keywords
CATEGORY_KEYWORDS = {
    "Sales": [
        "revenue", "sales", "profit", "customer", "transaction", "order", "sold", 
        "price", "quantity", "client", "invoice", "deal", "discount", "margin"
    ],
    "Finance": [
        "budget", "expense", "income", "cash", "asset", "liability", "equity", 
        "cost", "tax", "ebitda", "accounting", "ledger", "amortization", "depreciation"
    ],
    "HR": [
        "employee", "salary", "department", "role", "hire", "vacancy", "performance", 
        "payroll", "candidate", "termination", "leave", "onboarding", "recruitment"
    ],
    "Marketing": [
        "campaign", "click", "impression", "lead", "ad", "conversion", "reach", 
        "spend", "ctr", "roas", "funnel", "channel", "cpc", "bounce"
    ],
    "Inventory": [
        "stock", "sku", "warehouse", "supplier", "reorder", "product", "inventory", 
        "shipment", "restock", "bin", "location", "batch"
    ],
    "Healthcare": [
        "patient", "doctor", "clinic", "diagnosis", "treatment", "medical", 
        "prescription", "admission", "discharge", "physician", "disease", "health"
    ],
    "Education": [
        "student", "grade", "class", "course", "school", "enrollment", "teacher", 
        "curriculum", "gpa", "major", "semester", "exam"
    ]
}

def classify_dataset(column_names: List[str]) -> str:
    """
    Infers the category of a dataset by scanning its column names against category keywords.
    Returns the category name, defaulting to 'General Spreadsheet' if there are no matches.
    """
    category_scores = {category: 0 for category in CATEGORY_KEYWORDS}
    
    # Process column names for matching
    cleaned_cols = [str(col).lower().strip() for col in column_names]
    
    for col in cleaned_cols:
        # Split column name into words or substrings to scan
        words = re.findall(r'[a-z0-9]+', col)
        
        for category, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                # Add score if keyword matches column directly or matches any word in the column header
                if kw in col or kw in words:
                    category_scores[category] += 1
                    
    # Find category with highest positive score
    best_category = "General Spreadsheet"
    highest_score = 0
    
    for category, score in category_scores.items():
        if score > highest_score:
            highest_score = score
            best_category = category
            
    return best_category
