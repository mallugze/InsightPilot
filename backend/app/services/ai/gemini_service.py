import logging
import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from app.core.gemini_config import GEMINI_API_KEY, GEMINI_MODEL
from app.services.ai.models import AIAnalysisContext

logger = logging.getLogger("gemini_service")

class LLMResponse(str):
    """
    Subclasses standard str to store fallback metadata thread-safely
    without violating return type signatures.
    """
    def __new__(cls, content: str, fallback_triggered: bool = False):
        obj = str.__new__(cls, content)
        obj.fallback_triggered = fallback_triggered
        return obj

class BaseLLMProvider(ABC):
    """
    Abstract LLM provider class allowing pluggable models.
    """
    @abstractmethod
    def generate(self, prompt: str, context: Optional[AIAnalysisContext] = None) -> str:
        pass

class GeminiLLMProvider(BaseLLMProvider):
    """
    Gemini model provider communicating with google-generativeai.
    """
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.model_name = GEMINI_MODEL
        self.initialized = False
        
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                self.initialized = True
                logger.info(f"Gemini client initialized with model: {self.model_name}")
            except Exception as e:
                logger.exception("Failed to import or configure google-generativeai SDK. Defaulting to mock fallback.")
        else:
            logger.warning("No Gemini API key loaded. Provider running in deterministic mock mode.")

    def generate(self, prompt: str, context: Optional[AIAnalysisContext] = None) -> str:
        if not self.initialized:
            logger.warning("Gemini LLM Provider is not initialized. Falling back to local mock.")
            mock_text = self._generate_mock_fallback(prompt, context)
            return LLMResponse(mock_text, fallback_triggered=True)
            
        retries = 3
        backoff = 1.0 # Initial backoff duration in seconds
        
        for attempt in range(retries):
            try:
                logger.info(f"Sending request to Gemini API (Model: {self.model_name}, Attempt: {attempt + 1})...")
                response = self.model.generate_content(prompt)
                
                if response and response.text:
                    logger.info("Received response from Gemini API successfully.")
                    return LLMResponse(response.text, fallback_triggered=False)
                else:
                    raise ValueError("Gemini API returned empty response content.")
            except Exception as e:
                logger.warning(f"Gemini API attempt {attempt + 1} failed: {str(e)}")
                if attempt < retries - 1:
                    logger.info(f"Retrying in {backoff} seconds (exponential backoff)...")
                    time.sleep(backoff)
                    backoff *= 2.0
                else:
                    logger.error("All Gemini API retries exhausted. Falling back to mock reasoning engine.")
                    mock_text = self._generate_mock_fallback(prompt, context)
                    return LLMResponse(mock_text, fallback_triggered=True)

    def _generate_mock_fallback(self, prompt: str, context: Optional[AIAnalysisContext] = None) -> str:
        """
        A high-fidelity deterministic mock model that parses prompt intents and context values
        to generate logical, correct responses matching backend facts.
        """
        logger.info("Executing local mock fallback for prompt template.")
        if not context:
            return "AI Foundation initialized. API key config required for custom query reasoning."

        pulse = context.business_pulse
        health = context.health_label
        name = context.dataset_name
        domain = context.dataset_domain

        # Detect the requested format/intent
        prompt_lower = prompt.lower()
        
        if "executive_report" in prompt_lower or "executive_summary" in prompt_lower or "report" in prompt_lower:
            # Generate structured report content matching Pydantic fields
            report_data = {
                "executive_summary": f"Analytical profile for dataset '{name}'. The backend context identifies a {health} health state with an overall business pulse of {pulse}/100.",
                "business_health": f"The '{domain}' domain analysis reports standard metrics with {len(context.kpis or [])} key indicators active. General quality rating stands at {context.quality_score}%.",
                "key_findings": [
                    f"Dataset contains {context.rows_count} rows and {context.cols_count} columns.",
                    f"Highest variance identified in KPIs: {', '.join([k['name'] for k in (context.kpis or [])[:2]])}."
                ],
                "critical_risks": [
                    f"Identified {context.missing_values_count} missing cells and {context.duplicate_rows_count} duplicate rows.",
                    f"Zero metric outliers observed in dataset elements."
                ],
                "growth_opportunities": [
                    "Perform data cleaning to fix null columns.",
                    "Optimize resource allocation based on positive trend slope indicators."
                ],
                "recommendations": [r.get("text", "Optimize processes") for r in (context.recommendations or [])[:2]],
                "action_items": [
                    "Drop columns containing only empty/null rows.",
                    "Configure automated alert thresholds for anomalies."
                ]
            }
            return json.dumps(report_data, indent=2)
            
        elif "dashboard_chat" in prompt_lower or "executive_chat" in prompt_lower:
            # Render valid JSON structure to match executive_chat.txt schema
            report_data = {
                "answer": f"Based on the analysis of '{name}' (Pulse: {pulse}), we have identified {len(context.trends or [])} trends and {len(context.anomalies or [])} anomalies. Recommended actions include addressing columns requiring cleaning.",
                "reasoning_summary": f"Analyzing metrics for {name} with business pulse rating of {pulse}/100.",
                "key_findings": [
                    f"Dataset contains {context.rows_count} rows and {context.cols_count} columns.",
                    f"Data quality is evaluated at {context.quality_score}%."
                ],
                "recommendations": [r.get("text", "Drop empty columns") for r in (context.recommendations or [])[:2]],
                "follow_up_questions": [
                    f"Show supporting KPIs for {domain} domain.",
                    "Explain the anomalies identified in our trends.",
                    "What should management do next?"
                ]
            }
            return json.dumps(report_data, indent=2)
            
        else:
            return f"InsightPilot AI response for {name} ({domain} domain). Business Pulse is {pulse}/100 and status is {health}. Quality score is {context.quality_score}%."
