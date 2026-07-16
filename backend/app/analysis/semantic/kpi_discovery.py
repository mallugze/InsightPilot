import pandas as pd
from typing import Dict, Any, List

def discover_kpis(
    df: pd.DataFrame,
    classified_features: List[Dict[str, Any]],
    relationships: Dict[str, Any],
    domain: str
) -> List[Dict[str, Any]]:
    """
    Examines features and dataset context to dynamically generate domain-specific KPI cards.
    """
    suggested_kpis = []
    
    # 1. Biology/Botanical Classification (e.g. Iris)
    if domain == "Biology":
        suggested_kpis.append({
            "metric_name": "Flower Samples",
            "aggregation_strategy": "COUNT",
            "target_column": "species" if "species" in df.columns else (classified_features[0]["name"] if classified_features else "id"),
            "reasoning": f"Calculates total botanical flower specimens observed.",
            "selected_why": "Core count of biological samples."
        })
        
        # Check if sepal/petal columns exist
        for col in df.columns:
            if "sepal_length" in col.lower() or "sepallength" in col.lower():
                suggested_kpis.append({
                    "metric_name": "Average Sepal Length",
                    "aggregation_strategy": "MEAN",
                    "target_column": col,
                    "reasoning": "Calculates standard mean sepal length of specimens.",
                    "selected_why": "Core structural botanical indicator."
                })
            if "petal_width" in col.lower() or "petalwidth" in col.lower():
                suggested_kpis.append({
                    "metric_name": "Average Petal Width",
                    "aggregation_strategy": "MEAN",
                    "target_column": col,
                    "reasoning": "Calculates standard mean petal width of specimens.",
                    "selected_why": "Botanical width threshold identifier."
                })
        
        # Add Species Unique Count if missing
        if "species" in df.columns:
            suggested_kpis.append({
                "metric_name": "Flower Species",
                "aggregation_strategy": "COUNT_DISTINCT",
                "target_column": "species",
                "reasoning": "Counts unique flower taxonomic groups.",
                "selected_why": "Target classification label."
            })
            
    # 2. Machine Learning / Survival Analysis (e.g. Titanic)
    elif domain == "Machine Learning" or domain == "Survival Analysis":
        suggested_kpis.append({
            "metric_name": "Passengers Logged",
            "aggregation_strategy": "COUNT",
            "target_column": "passenger_id" if "passenger_id" in df.columns else "id",
            "reasoning": "Tracks total passenger records boarded.",
            "selected_why": "ML dataset instance count."
        })
        if "survived" in df.columns:
            suggested_kpis.append({
                "metric_name": "Survival Rate",
                "aggregation_strategy": "MEAN",
                "target_column": "survived",
                "reasoning": "Calculates the average survival percentage.",
                "selected_why": "Primary target label prediction."
            })
        if "sex" in df.columns:
            suggested_kpis.append({
                "metric_name": "Distinct Genders",
                "aggregation_strategy": "COUNT_DISTINCT",
                "target_column": "sex",
                "reasoning": "Identifies gender distributions.",
                "selected_why": "Categorical feature split indicator."
            })

    # 3. Healthcare / Patient Analytics
    elif domain == "Healthcare":
        suggested_kpis.append({
            "metric_name": "Patients Registered",
            "aggregation_strategy": "COUNT",
            "target_column": "patient_id" if "patient_id" in df.columns else "id",
            "reasoning": "Aggregates total clinical admissions records.",
            "selected_why": "Core clinical headcount tracking."
        })
        # Try to find age
        age_col = next((c["name"] for c in classified_features if "age" in c["name"].lower()), None)
        if age_col:
            suggested_kpis.append({
                "metric_name": "Average Patient Age",
                "aggregation_strategy": "MEAN",
                "target_column": age_col,
                "reasoning": "Calculates the average age of admitted patient groups.",
                "selected_why": "Major healthcare demographic variable."
            })
        # Try to find diagnosis
        diag_col = next((c["name"] for c in classified_features if "diag" in c["name"].lower() or "disease" in c["name"].lower()), None)
        if diag_col:
            suggested_kpis.append({
                "metric_name": "Unique Diagnoses",
                "aggregation_strategy": "COUNT_DISTINCT",
                "target_column": diag_col,
                "reasoning": "Identifies diverse disease classes registered.",
                "selected_why": "Clinical categories mapping."
            })

    # 4. Real Estate / Price Prediction (Housing)
    elif domain == "Real Estate":
        price_col = next((c["name"] for c in classified_features if "price" in c["name"].lower() or "value" in c["name"].lower()), None)
        if price_col:
            suggested_kpis.append({
                "metric_name": "Average Home Price",
                "aggregation_strategy": "MEAN",
                "target_column": price_col,
                "reasoning": "Calculates the average real estate list price.",
                "selected_why": "Continuous target valuation."
            })
        area_col = next((c["name"] for c in classified_features if "sqft" in c["name"].lower() or "area" in c["name"].lower() or "size" in c["name"].lower()), None)
        if area_col:
            suggested_kpis.append({
                "metric_name": "Average Lot Area",
                "aggregation_strategy": "MEAN",
                "target_column": area_col,
                "reasoning": "Calculates average square footage / listing size.",
                "selected_why": "Core price regression predictor."
            })
        rooms_col = next((c["name"] for c in classified_features if "room" in c["name"].lower() or "bed" in c["name"].lower()), None)
        if rooms_col:
            suggested_kpis.append({
                "metric_name": "Average Bedrooms",
                "aggregation_strategy": "MEAN",
                "target_column": rooms_col,
                "reasoning": "Calculates average room counts.",
                "selected_why": "Housing structural predictor."
            })

    # 5. Weather / Climate Analytics
    elif domain == "Weather":
        temp_col = next((c["name"] for c in classified_features if "temp" in c["name"].lower()), None)
        if temp_col:
            suggested_kpis.append({
                "metric_name": "Average Temperature",
                "aggregation_strategy": "MEAN",
                "target_column": temp_col,
                "reasoning": "Calculates the average weather temperature.",
                "selected_why": "Core climate indicator."
            })
        rain_col = next((c["name"] for c in classified_features if "rain" in c["name"].lower() or "precip" in c["name"].lower()), None)
        if rain_col:
            suggested_kpis.append({
                "metric_name": "Total Rainfall Amount",
                "aggregation_strategy": "SUM",
                "target_column": rain_col,
                "reasoning": "Aggregates total cumulative precipitation volume.",
                "selected_why": "Climate moisture measurement."
            })
        hum_col = next((c["name"] for c in classified_features if "hum" in c["name"].lower()), None)
        if hum_col:
            suggested_kpis.append({
                "metric_name": "Average Humidity",
                "aggregation_strategy": "MEAN",
                "target_column": hum_col,
                "reasoning": "Calculates standard atmospheric relative humidity.",
                "selected_why": "Weather density measurement."
            })

    # 6. Sensor / IoT Monitoring
    elif domain == "Sensor":
        reading_col = next((c["name"] for c in classified_features if "reading" in c["name"].lower() or "val" in c["name"].lower() or "temp" in c["name"].lower()), None)
        if reading_col:
            suggested_kpis.append({
                "metric_name": "Average Sensor Telemetry",
                "aggregation_strategy": "MEAN",
                "target_column": reading_col,
                "reasoning": "Calculates average telemetry value.",
                "selected_why": "IoT signals normal baseline."
            })
            suggested_kpis.append({
                "metric_name": "Peak Telemetry Value",
                "aggregation_strategy": "MAX",
                "target_column": reading_col,
                "reasoning": "Identifies peak maximum sensor spike recorded.",
                "selected_why": "Fault tolerance diagnostics."
            })
        device_col = next((c["name"] for c in classified_features if "device" in c["name"].lower() or "id" in c["name"].lower()), None)
        if device_col:
            suggested_kpis.append({
                "metric_name": "Hardware Devices",
                "aggregation_strategy": "COUNT_DISTINCT",
                "target_column": device_col,
                "reasoning": "Counts distinct reporting hardware device instances.",
                "selected_why": "IoT hardware volume."
            })

    # 7. Default Generic / Business KPI Fallbacks
    if len(suggested_kpis) < 2:
        # Extract metadata categories
        primary_keys = [f["name"] for f in classified_features if f["semantic_type"] == "Primary Key"]
        currencies = [f["name"] for f in classified_features if f["semantic_type"] == "Currency"]
        numerics = [f["name"] for f in classified_features if f["semantic_type"] in ["Numeric", "Percentage"] and f["name"] not in primary_keys]
        categories = [f["name"] for f in classified_features if f["semantic_type"] in ["Categorical", "Location", "Boolean"]]
        
        row_count = len(df)
        key_col = primary_keys[0] if primary_keys else (classified_features[0]["name"] if classified_features else "id")
        
        suggested_kpis.append({
            "metric_name": "Total Records",
            "aggregation_strategy": "COUNT",
            "target_column": key_col,
            "reasoning": f"Calculates total row volume containing {row_count} mapped samples.",
            "selected_why": "Core structural dimension representing dataset record count."
        })
        
        for curr in currencies:
            suggested_kpis.append({
                "metric_name": f"Total {curr.replace('_', ' ').title()}",
                "aggregation_strategy": "SUM",
                "target_column": curr,
                "reasoning": f"Aggregates total cumulative values inside currency metric '{curr}'.",
                "selected_why": "Crucial financial metric tracking top-line economic performance."
            })
            
        for num in numerics:
            name_clean = num.replace("_", " ").title()
            if any(kw in num.lower() for kw in ["rate", "margin", "grade", "score", "age", "average", "avg", "percent"]):
                suggested_kpis.append({
                    "metric_name": f"Average {name_clean}",
                    "aggregation_strategy": "MEAN",
                    "target_column": num,
                    "reasoning": f"Calculates standard statistical average mean value of '{num}'.",
                    "selected_why": "Continuous metric representing diagnostic ratios or percentage performance."
                })
            else:
                suggested_kpis.append({
                    "metric_name": f"Cumulative {name_clean}",
                    "aggregation_strategy": "SUM",
                    "target_column": num,
                    "reasoning": f"Calculates sum totals of '{num}' values across all rows.",
                    "selected_why": "Numeric capacity column tracking structural volumes."
                })
                
        if len(suggested_kpis) < 3:
            for cat in categories[:2]:
                unique_cnt = df[cat].dropna().nunique() if cat in df.columns else 0
                suggested_kpis.append({
                    "metric_name": f"Unique {cat.replace('_', ' ').title()}s",
                    "aggregation_strategy": "COUNT_DISTINCT",
                    "target_column": cat,
                    "reasoning": f"Counts distinct category labels ({unique_cnt}) found inside column '{cat}'.",
                    "selected_why": "Categorical dimension mapping unique segment groups."
                })
                
    return suggested_kpis[:4]

def calculate_discovered_kpis(
    df: pd.DataFrame,
    suggested_kpis: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Computes the actual values for the dynamically suggested KPIs using Pandas.
    """
    results = {}
    for kpi in suggested_kpis:
        name = kpi["metric_name"]
        col = kpi["target_column"]
        strategy = kpi["aggregation_strategy"]
        
        # Clean formatting
        name_key = name.replace(" ", "_").lower()
        
        if col not in df.columns:
            # Fallback row count
            if strategy == "COUNT":
                results[name_key] = len(df)
            continue
            
        series = df[col].dropna()
        if series.empty:
            results[name_key] = 0
            continue
            
        val = 0
        if strategy == "COUNT":
            val = int(len(df))
        elif strategy == "COUNT_DISTINCT":
            val = int(series.nunique())
        elif strategy == "SUM":
            try:
                val = float(series.sum())
            except:
                val = len(df)
        elif strategy == "MEAN":
            try:
                # If binary survived column
                if col == "survived":
                    val = float(series.mean() * 100) # survival rate percentage
                else:
                    val = float(series.mean())
            except:
                val = 0
        elif strategy == "MAX":
            try:
                val = float(series.max())
            except:
                val = 0
        elif strategy == "MIN":
            try:
                val = float(series.min())
            except:
                val = 0
        else:
            val = int(len(df))
            
        if isinstance(val, float):
            results[name_key] = round(val, 2)
        else:
            results[name_key] = val
            
    return results
