import logging
from typing import List, Dict, Any

logger = logging.getLogger("history_builder")

class ConversationHistoryBuilder:
    """
    Intelligently selects and structures conversation history context for LLM prompts,
    architected to support future summarization limits and streaming context.
    """
    def __init__(self, max_raw_turns: int = 3, token_limit_approx: int = 1000):
        self.max_raw_turns = max_raw_turns
        self.token_limit_approx = token_limit_approx
        logger.info(f"ConversationHistoryBuilder initialized. Raw turns limit: {self.max_raw_turns}")

    def build_history_context(self, messages: List[Dict[str, Any]], current_question: str) -> str:
        """
        Processes message history list to select the most relevant dialog exchanges.
        Returns a formatted dialogue string block.
        """
        logger.info(f"Selecting relevant conversation history from {len(messages)} past messages.")
        
        if not messages:
            logger.info("No past messages to build history.")
            return "No previous dialogue history."

        # Filter out empty or system-level messages
        valid_messages = [
            msg for msg in messages 
            if msg.get("role") in ["user", "model", "assistant"] and msg.get("content")
        ]

        if not valid_messages:
            return "No previous dialogue history."

        # Architecture for Future Summarization Fallback:
        # If history is too long (e.g. > 8 messages), we split it:
        # - Summarize the first N messages (represented as a static summary prefix).
        # - Keep the last M messages as raw dialogue turns.
        summary_prefix = ""
        raw_turns = valid_messages
        
        if len(valid_messages) > self.max_raw_turns * 2:
            logger.info(f"History length {len(valid_messages)} exceeds raw limit. Compressing older turns.")
            older_turns = valid_messages[:-self.max_raw_turns * 2]
            raw_turns = valid_messages[-self.max_raw_turns * 2:]
            
            # Formulate simple bulleted summary of older conversations (supports future LLM summary model)
            summary_bullets = []
            for msg in older_turns:
                role_label = "User" if msg["role"] == "user" else "AI"
                snippet = msg["content"][:60].replace("\n", " ")
                summary_bullets.append(f"- {role_label} discussed: \"{snippet}...\"")
            
            summary_prefix = "[Older Conversation Summary]\n" + "\n".join(summary_bullets) + "\n\n"

        # Intelligently check keyword relevance:
        # Highlight previous messages matching current question keywords
        keywords = set(current_question.lower().split())
        highlighted_history = []
        
        for msg in raw_turns:
            content_lower = msg["content"].lower()
            relevance_score = sum(1 for kw in keywords if len(kw) > 3 and kw in content_lower)
            
            role_label = "User" if msg["role"] == "user" else "AI"
            line = f"{role_label}: {msg['content']}"
            if relevance_score > 0:
                line += " (Relevant Context)"
            highlighted_history.append(line)

        # Assemble final context
        history_text = summary_prefix + "\n".join(highlighted_history)
        logger.debug(f"Compiled history context block:\n{history_text}")
        return history_text
