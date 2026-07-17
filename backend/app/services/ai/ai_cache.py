import hashlib
import json
import logging
import time
from typing import Dict, Any, Optional

from app.services.ai.models import AIAnalysisContext

logger = logging.getLogger("ai_cache")

class AICache:
    """
    In-memory caching engine that includes the SHA256 context hash
    in cache keys to prevent stale AI responses when data changes.
    """
    _cache: Dict[str, Dict[str, Any]] = {}

    def __init__(self, default_ttl_seconds: int = 3600):
        self.default_ttl = default_ttl_seconds
        logger.info(f"AICache initialized. Default TTL: {self.default_ttl} seconds.")

    def compute_context_hash(self, context: AIAnalysisContext) -> str:
        """
        Generates a unique SHA-256 hash of the entire analysis context.
        """
        try:
            # Dump fields sorted by key to guarantee consistency
            context_dict = context.model_dump()
            serialized = json.dumps(context_dict, sort_keys=True, default=str)
            hashed = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
            logger.debug(f"Computed context SHA-256 hash: {hashed}")
            return hashed
        except Exception as e:
            logger.error(f"Failed to hash context details: {str(e)}")
            # Fail-safe hash
            return "stale_safe_fallback"

    def make_key(self, prompt: str, context: AIAnalysisContext) -> str:
        """
        Creates a compound cache key containing the prompt details and context hash.
        """
        context_hash = self.compute_context_hash(context)
        prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
        compound = f"{context.analysis_id}:{prompt_hash}:{context_hash}"
        logger.debug(f"Created compound cache key: {compound}")
        return compound

    def get(self, prompt: str, context: AIAnalysisContext) -> Optional[str]:
        key = self.make_key(prompt, context)
        cached = self._cache.get(key)
        
        if not cached:
            logger.info("Cache miss. Prompt results not cached.")
            return None
            
        # Check TTL
        if time.time() > cached["expires_at"]:
            logger.info("Cache hit but entry is expired.")
            self._cache.pop(key, None)
            return None

        logger.info("Cache hit! Returning cached response text.")
        return cached["value"]

    def set(self, prompt: str, context: AIAnalysisContext, value: str, ttl: Optional[int] = None) -> None:
        key = self.make_key(prompt, context)
        ttl = ttl if ttl is not None else self.default_ttl
        expires_at = time.time() + ttl
        
        logger.info(f"Caching generated response. Expires in {ttl} seconds.")
        self._cache[key] = {
            "value": value,
            "expires_at": expires_at
        }

    def clear(self) -> None:
        logger.info("Clearing all cache entries.")
        self._cache.clear()
