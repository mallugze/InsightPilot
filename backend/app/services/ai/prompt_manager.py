import os
import logging
from typing import Dict

logger = logging.getLogger("prompt_manager")

class PromptManager:
    """
    Manages loading and formatting prompt templates from the prompts directory.
    """
    def __init__(self, prompts_dir: str = None):
        if not prompts_dir:
            prompts_dir = os.path.join(os.path.dirname(__file__), "prompts")
        self.prompts_dir = prompts_dir
        self.cache: Dict[str, str] = {}
        logger.info(f"PromptManager initialized. Directing templates from: {self.prompts_dir}")

    def load_template(self, template_name: str) -> str:
        """
        Loads the template text from the prompts directory, caching reads.
        """
        if template_name in self.cache:
            return self.cache[template_name]

        # Standardize name extension
        if not template_name.endswith(".txt"):
            filename = f"{template_name}.txt"
        else:
            filename = template_name

        filepath = os.path.join(self.prompts_dir, filename)
        if not os.path.exists(filepath):
            logger.error(f"Prompt template file not found: {filepath}")
            raise FileNotFoundError(f"Prompt template '{template_name}' not found at {filepath}")

        try:
            logger.info(f"Loading prompt template file: {filename}")
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            self.cache[template_name] = content
            return content
        except Exception as e:
            logger.error(f"Failed to read prompt template {filename}: {str(e)}")
            raise e

    def format_prompt(self, template_name: str, **kwargs) -> str:
        """
        Loads a template and formats it with variables.
        """
        template = self.load_template(template_name)
        logger.info(f"Formatting template '{template_name}' with {list(kwargs.keys())} keys.")
        return template.format(**kwargs)
