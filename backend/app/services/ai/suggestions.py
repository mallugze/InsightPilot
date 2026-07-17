import logging
from typing import List
from app.services.ai.models import AIAnalysisContext

logger = logging.getLogger("suggestions")

class DynamicSuggestionsGenerator:
    """
    Dynamically generates contextual suggested questions based on the dataset's
    semantic profile, business domain, anomalies, and quality score.
    """
    def __init__(self):
        logger.info("DynamicSuggestionsGenerator initialized.")

    def generate_suggestions(self, context: AIAnalysisContext) -> List[str]:
        logger.info(f"Generating dynamic suggestions for domain '{context.dataset_domain}'...")
        suggestions: List[str] = []

        domain = context.dataset_domain.lower()
        entity = context.entity or "records"
        pulse = context.business_pulse

        # 1. Base Domain-Specific Suggestions
        if "sales" in domain or "business" in domain or "marketing" in domain or "retail" in domain:
            suggestions.append(f"Explain the overall Business Pulse of {pulse}/100.")
            if context.hero_metric:
                suggestions.append(f"What insights explain the hero metric '{context.hero_metric.get('name')}'?")
            if context.zero_metric:
                suggestions.append(f"What caused the underperformance in zero metric '{context.zero_metric.get('name')}'?")
            suggestions.append(f"What are the biggest growth opportunities for {entity}?")
            
        elif "biology" in domain or "scientific" in domain or "medical" in domain or "healthcare" in domain:
            suggestions.append(f"Summarize the experimental scientific observations in {context.dataset_name}.")
            suggestions.append("Which features show the strongest correlation coefficients?")
            suggestions.append("What patterns distinguish different entity classifications?")
            if context.ml_readiness and context.ml_readiness.get("readiness_score", 0) > 50:
                suggestions.append(f"Are features ready for training model predictions?")
                
        else:
            # Fallback for generic domains (IoT, Weather, Manufacturing, Energy, etc.)
            suggestions.append(f"Explain the dataset quality rating of {context.quality_score}%.")
            suggestions.append(f"What are the primary operational recommendations for {entity}?")
            suggestions.append(f"What anomalies exist in the trends of the dataset features?")

        # 2. Add Conditional Suggestions based on Data Quality & Integrity
        if context.missing_values_count > 0:
            suggestions.append("Which columns require clean-up or contain empty cells?")
            
        if context.anomalies and len(context.anomalies) > 0:
            suggestions.append("What critical risks do the anomalies expose in the data?")

        if context.recommendations and len(context.recommendations) > 0:
            suggestions.append("Summarize the top recommended action items for management.")

        # Ensure we return a distinct, limited list (max 5 suggestions)
        unique_suggestions = []
        for s in suggestions:
            if s not in unique_suggestions:
                unique_suggestions.append(s)
                
        logger.info(f"Dynamically formulated {len(unique_suggestions[:5])} suggested questions.")
        return unique_suggestions[:5]
