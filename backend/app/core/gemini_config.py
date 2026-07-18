import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger("gemini_config")
load_dotenv()

# API Keys & Configuration Parameters
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", os.getenv("GEMINI_MODEL_NAME", "gemini-3.5-flash"))

if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment. AI features will run in mock/preview fallback mode.")
else:
    logger.info(f"Gemini API key loaded. Configured model: {GEMINI_MODEL}")
