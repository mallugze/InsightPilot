import logging
import json
from typing import Dict, Any

from app.services.ai.models import AIAnalysisContext, AIReport
from app.services.ai.gemini_service import BaseLLMProvider
from app.services.ai.prompt_manager import PromptManager
from app.services.ai.response_validator import ResponseValidator

logger = logging.getLogger("report_generator")

class ReportGenerator:
    """
    Generates structured AIReport objects from analysis context.
    """
    def __init__(self, provider: BaseLLMProvider, prompt_manager: PromptManager, validator: ResponseValidator):
        self.provider = provider
        self.prompt_manager = prompt_manager
        self.validator = validator
        logger.info("ReportGenerator successfully initialized.")

    def generate_report(self, context: AIAnalysisContext) -> AIReport:
        logger.info(f"Generating structured AI report for analysis ID: {context.analysis_id}")
        
        # 1. Format the executive_report template
        context_dump = json.dumps(context.model_dump(), indent=2, default=str)
        prompt = self.prompt_manager.format_prompt("executive_report", context=context_dump)

        # 2. Get LLM response
        raw_response = self.provider.generate(prompt, context=context)

        # 3. Validate response text against facts (prevent hallucinations)
        try:
            self.validator.validate(raw_response, context)
        except Exception as e:
            logger.error(f"Response validation failed during report generation: {str(e)}")
            # Raise validator errors or re-raise
            raise e

        # 4. Parse response as JSON to fill AIReport structure
        try:
            # Strip any markdown backticks if returned by LLM
            clean_json = raw_response.strip()
            if clean_json.startswith("```json"):
                clean_json = clean_json[7:]
            if clean_json.startswith("```"):
                clean_json = clean_json[3:]
            if clean_json.endswith("```"):
                clean_json = clean_json[:-3]
            clean_json = clean_json.strip()

            parsed = json.loads(clean_json)
            logger.info("Successfully parsed LLM report response into JSON structure.")
            
            # Map fields safely
            return AIReport(
                executive_summary=parsed.get("executive_summary", ""),
                business_health=parsed.get("business_health", ""),
                key_findings=parsed.get("key_findings", []),
                critical_risks=parsed.get("critical_risks", []),
                growth_opportunities=parsed.get("growth_opportunities", []),
                recommendations=parsed.get("recommendations", []),
                action_items=parsed.get("action_items", [])
            )
        except Exception as e:
            logger.error(f"Failed to parse LLM response into structured AIReport: {str(e)}. Raw text: {raw_response}")
            # Generate a structured report based on fallback metrics
            return AIReport(
                executive_summary=f"Analysis report for dataset '{context.dataset_name}'. Business Pulse is {context.business_pulse} ({context.health_label}).",
                business_health=f"The quality score is {context.quality_score}%. Data shows {context.missing_values_count} missing cells.",
                key_findings=[
                    f"Parsed row count: {context.rows_count}.",
                    f"Parsed columns: {context.cols_count}."
                ],
                critical_risks=[f"Duplicate rows detected: {context.duplicate_rows_count}."],
                growth_opportunities=["Optimize data quality structures."],
                recommendations=[r.get("text", "Drop empty columns") for r in (context.recommendations or [])],
                action_items=["Analyze anomalies", "Perform feature engineering"]
            )
        
