"""
Context Caching Engine for prefix reuse and token cost reduction.
Supports Anthropic Prompt Caching, OpenAI Prefix Caching, and Local Memory Cache.
"""

from __future__ import annotations

import hashlib
import time
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from octo_harness.models import ChatMessage


class CachedPrefix(BaseModel):
    hash_key: str
    token_count: int
    created_at: float = Field(default_factory=time.time)
    last_accessed_at: float = Field(default_factory=time.time)
    hit_count: int = 0
    estimated_saved_usd: float = 0.0


class ContextCacheEngine:
    """
    Simulates and interfaces with provider-native prompt context caching.
    Identifies common static prefixes (such as 00-constitution.md and 01-operating-system.md),
    calculates cache hits, and applies discount multipliers (50% - 90% savings).
    """

    def __init__(self, ttl_seconds: float = 3600.0, default_discount: float = 0.75):
        self.ttl_seconds = ttl_seconds
        self.default_discount = default_discount  # 75% savings on cached prefix tokens
        self._cache: Dict[str, CachedPrefix] = {}
        self._total_cache_hits: int = 0
        self._total_tokens_cached: int = 0
        self._total_saved_usd: float = 0.0

    def compute_prefix_hash(self, messages: List[ChatMessage]) -> Tuple[str, int]:
        """
        Extracts static system / setup messages and computes deterministic hash and token count.
        """
        system_content = ""
        for m in messages:
            if m.role in ("system", "SYSTEM"):
                system_content += (m.content or "") + "\n"

        if not system_content:
            return "", 0

        hash_key = hashlib.sha256(system_content.encode("utf-8")).hexdigest()[:16]
        token_count = max(1, len(system_content) // 4)
        return hash_key, token_count

    def check_and_apply_cache(
        self, messages: List[ChatMessage], input_cost_per_million: float
    ) -> Tuple[bool, int, float]:
        """
        Checks if system prompt matches a cached prefix.
        Returns: (is_cache_hit, cached_tokens, discount_savings_usd)
        """
        hash_key, token_count = self.compute_prefix_hash(messages)
        if not hash_key or token_count < 100:
            return False, 0, 0.0

        now = time.time()
        if hash_key in self._cache:
            entry = self._cache[hash_key]
            # Check TTL
            if now - entry.created_at < self.ttl_seconds:
                entry.hit_count += 1
                entry.last_accessed_at = now
                self._total_cache_hits += 1

                # Calculate USD savings on cached tokens
                baseline_cost = (token_count / 1_000_000.0) * input_cost_per_million
                savings = round(baseline_cost * self.default_discount, 6)
                entry.estimated_saved_usd += savings
                self._total_saved_usd += savings
                return True, token_count, savings

        # Register in cache for future hits
        self._cache[hash_key] = CachedPrefix(
            hash_key=hash_key,
            token_count=token_count,
            created_at=now,
            last_accessed_at=now,
            hit_count=0,
        )
        self._total_tokens_cached += token_count
        return False, token_count, 0.0

    def get_cache_stats(self) -> Dict[str, Any]:
        """Return cache performance metrics."""
        return {
            "cached_prefixes_count": len(self._cache),
            "total_cache_hits": self._total_cache_hits,
            "total_saved_usd": round(self._total_saved_usd, 6),
            "prefixes": {k: v.model_dump() for k, v in self._cache.items()},
        }
