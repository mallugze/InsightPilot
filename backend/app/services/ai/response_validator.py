import re
import logging
from typing import List

from app.services.ai.models import AIAnalysisContext

logger = logging.getLogger("response_validator")

class AIValidationException(ValueError):
    """Exception raised when the AI response contradicts backend facts."""
    def __init__(self, message: str, details: List[str]):
        super().__init__(message)
        self.details = details

class ResponseValidator:
    """
    Validates AI responses against backend facts to prevent hallucinations.
    """
    def __init__(self):
        logger.info("ResponseValidator initialized.")

    def validate(self, response_text: str, context: AIAnalysisContext) -> str:
        """
        Validates the response text against context metrics.
        Returns the validated response_text if correct, otherwise raises AIValidationException.
        """
        logger.info("Executing response validation against backend facts...")
        contradictions = []

        # Split text into sentences for granular checking
        sentences = re.split(r'(?<=[.!?])\s+', response_text)

        for sentence in sentences:
            sentence_clean = sentence.lower()
            numbers = self._extract_numbers(sentence_clean)
            if not numbers:
                continue

            # 1. Validate Business Pulse / Health Score
            if "pulse" in sentence_clean or "health score" in sentence_clean or "health rating" in sentence_clean:
                true_pulse = context.business_pulse
                # Check if any number in the sentence matches true_pulse (+/- 1.0 tolerance)
                matches = any(abs(num - true_pulse) <= 1.0 for num in numbers)
                if not matches:
                    contradictions.append(
                        f"Sentence contradicts Business Pulse: '{sentence.strip()}' (Expected around {true_pulse})"
                    )

            # 2. Validate Quality Score
            if "quality" in sentence_clean:
                true_quality = context.quality_score
                matches = any(abs(num - true_quality) <= 1.0 for num in numbers)
                if not matches:
                    contradictions.append(
                        f"Sentence contradicts Data Quality Score: '{sentence.strip()}' (Expected around {true_quality})"
                    )

            # 3. Validate Row / Record counts
            if "row" in sentence_clean or "record" in sentence_clean or "sample" in sentence_clean:
                true_rows = context.rows_count
                # Integers check
                matches = any(int(num) == true_rows for num in numbers if num.is_integer())
                if not matches and true_rows not in [int(num) for num in numbers if num.is_integer()]:
                    contradictions.append(
                        f"Sentence contradicts row count: '{sentence.strip()}' (Expected {true_rows})"
                    )

            # 4. Validate Columns / Features count
            if "column" in sentence_clean or "feature" in sentence_clean:
                true_cols = context.cols_count
                matches = any(int(num) == true_cols for num in numbers if num.is_integer())
                if not matches and true_cols not in [int(num) for num in numbers if num.is_integer()]:
                    # Ignore single/common numbers like 1 or 2 to avoid false positives
                    big_cols_nums = [int(num) for num in numbers if num.is_integer() and int(num) > 2]
                    if big_cols_nums and all(n != true_cols for n in big_cols_nums):
                        contradictions.append(
                            f"Sentence contradicts column count: '{sentence.strip()}' (Expected {true_cols})"
                        )

            # 5. Validate Missing / Null cells
            if "missing" in sentence_clean or "null" in sentence_clean or "empty" in sentence_clean:
                true_nulls = context.missing_values_count
                matches = any(int(num) == true_nulls for num in numbers if num.is_integer())
                if not matches and true_nulls > 0 and all(int(num) != true_nulls for num in numbers if num.is_integer()):
                    contradictions.append(
                        f"Sentence contradicts missing values count: '{sentence.strip()}' (Expected {true_nulls})"
                    )

        if contradictions:
            logger.error(f"Response validation failed with {len(contradictions)} contradictions.")
            raise AIValidationException(
                message="AI response contains hallucinated values contradicting backend facts.",
                details=contradictions
            )

        logger.info("AI response validation successful. No contradictions detected.")
        return response_text

    def _extract_numbers(self, text: str) -> List[float]:
        """
        Helper to extract integer and float values from text.
        """
        # Find numeric expressions like 93.3 or 100 or 5,000
        clean_text = text.replace(",", "")
        pattern = r"\b\d+\.\d+|\b\d+\b"
        matches = re.findall(pattern, clean_text)
        return [float(x) for x in matches]
