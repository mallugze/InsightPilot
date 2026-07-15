from typing import Dict, Any, List

def build_executive_summary(
    domain: str,
    subdomain: str,
    entity: str,
    row_count: int,
    metrics: List[str],
    groups: List[str],
    ml_readiness: Dict[str, Any]
) -> str:
    """
    Constructs a textual summary addressing what was uploaded, what rows represent,
    what was discovered, what it's useful for, and what questions can be answered.
    """
    # Q1 & Q2: What was uploaded and row representation
    part1 = (
        f"This dataset is categorized under the '{domain}' domain, tracking '{subdomain}' data structures. "
        f"It contains a total of {row_count} samples, where each row records an individual '{entity}' entry."
    )
    
    # Q3: What was discovered (schema context)
    metrics_str = f"such as {', '.join(metrics[:2])}" if metrics else ""
    groups_str = f"such as {', '.join(groups[:2])}" if groups else ""
    
    if metrics and groups:
        part2 = (
            f"InsightPilot mapped several continuous metrics ({metrics_str}) "
            f"and categorical dimensions ({groups_str}) to slice performance variables."
        )
    elif metrics:
        part2 = f"InsightPilot extracted key numerical variables ({metrics_str}) across data points."
    else:
        part2 = f"InsightPilot extracted grouping variables ({groups_str}) from tabular cells."
        
    # Q4 & Q5: Utility and Questions answered
    ml_targets = [m for m, p in ml_readiness.items() if p["score"] >= 70]
    if ml_targets:
        utility = f"This dataset is highly useful for training predictive {', '.join(ml_targets).lower()} models."
    else:
        utility = "This dataset is suitable for loading spreadsheets, counting segment splits, and tracking distributions."
        
    questions = []
    if groups:
        questions.append(f"how outcomes distribute across category clusters like '{groups[0]}'")
    if metrics:
        questions.append(f"what basic averages and ranges represent baseline metrics for '{metrics[0]}'")
    if len(metrics) >= 2:
        questions.append("whether any strong positive or negative correlations exist between continuous measures")
        
    if questions:
        part3 = f"{utility} Specifically, it helps answer questions such as: {'; '.join(questions)}."
    else:
        part3 = f"{utility} It is designed to expose general data quality and tabular profiles."
        
    return f"{part1} {part2} {part3}"
