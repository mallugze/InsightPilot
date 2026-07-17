import re
import logging
from typing import List

from app.services.ai.models import AIAnalysisContext, Citation

logger = logging.getLogger("citation_builder")

class CitationBuilder:
    """
    Scans AI responses to compile structured references linking claims to backend engines.
    """
    def __init__(self):
        logger.info("CitationBuilder initialized.")

    def build_citations(self, response_text: str, context: AIAnalysisContext) -> List[Citation]:
        logger.info("Constructing structured citations from AI response...")
        citations: List[Citation] = []
        
        # Split response into clean sentences
        sentences = re.split(r'(?<=[.!?])\s+', response_text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            sentence_lower = sentence.lower()
            
            # 1. Match Business Pulse engine
            if any(x in sentence_lower for x in ["pulse", "health", "score", "label", "overall status"]):
                citations.append(
                    Citation(
                        sentence=sentence,
                        source="Business Pulse",
                        details=f"Calculated overall health score of {context.business_pulse}/100 and label '{context.health_label}'"
                    )
                )
                continue  # Avoid duplicate citation for same sentence to keep it clean

            # 2. Match KPI Engine
            if any(x in sentence_lower for x in ["kpi", "metric", "measure", "value"]):
                kpi_names = [k.get("name", "") for k in (context.kpis or [])]
                citations.append(
                    Citation(
                        sentence=sentence,
                        source="KPI Engine",
                        details=f"Detected {len(context.kpis or [])} active metrics. Primary: {', '.join(kpi_names[:2])}"
                    )
                )
                continue

            # 3. Match Trend & Anomaly Engine
            if any(x in sentence_lower for x in ["trend", "slope", "anomaly", "anomalies", "outlier", "outliers", "deviation"]):
                citations.append(
                    Citation(
                        sentence=sentence,
                        source="Trend & Anomaly Engine",
                        details=f"Identified {len(context.trends or [])} main trends and {len(context.anomalies or [])} outliers"
                    )
                )
                continue

            # 4. Match Correlation Engine
            if any(x in sentence_lower for x in ["correlation", "relationship", "correlated", "association", "linked"]):
                citations.append(
                    Citation(
                        sentence=sentence,
                        source="Correlation Engine",
                        details=f"Determined {len(context.correlations or [])} pairwise relationship coefficients"
                    )
                )
                continue

            # 5. Match Recommendation Engine
            if any(x in sentence_lower for x in ["recommend", "opportunity", "action", "action items"]):
                citations.append(
                    Citation(
                        sentence=sentence,
                        source="Recommendation Engine",
                        details=f"Extracted {len(context.recommendations or [])} decisions and {len(context.insights or [])} insights"
                    )
                )
                continue

            # 6. Match Ingestion & Validation report
            if any(x in sentence_lower for x in ["missing", "null", "duplicate", "validation", "headers"]):
                citations.append(
                    Citation(
                        sentence=sentence,
                        source="Validation Engine",
                        details=f"Dataset contains {context.missing_values_count} nulls and {context.duplicate_rows_count} duplicates"
                    )
                )
                continue

        logger.info(f"Generated {len(citations)} source citations successfully.")
        return citations
