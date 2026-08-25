"""
Token-bucket rate limiter and concurrency controller for AI model providers.
"""

from __future__ import annotations

import asyncio
import time
from typing import Dict, Optional


class TokenBucketLimiter:
    """
    Standard token bucket rate limiter allowing bursts up to capacity
    and refilling at rate_per_second.
    """

    def __init__(self, rate_per_second: float = 20.0, capacity: Optional[float] = None):
        self.rate_per_second = max(0.1, rate_per_second)
        self.capacity = capacity if capacity is not None else max(1.0, self.rate_per_second * 2.0)
        self.tokens = self.capacity
        self.last_refill = time.time()
        self._lock = asyncio.Lock()

    def _refill(self) -> None:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.rate_per_second))
        self.last_refill = now

    async def acquire(self, tokens_needed: float = 1.0, wait: bool = True, timeout_s: float = 5.0) -> bool:
        """
        Attempt to acquire tokens. If wait=True, asynchronously sleeps until tokens available.
        """
        start_time = time.time()
        while True:
            async with self._lock:
                self._refill()
                if self.tokens >= tokens_needed:
                    self.tokens -= tokens_needed
                    return True

            if not wait:
                return False

            if time.time() - start_time > timeout_s:
                return False

            await asyncio.sleep(0.05)


class ProviderRateLimiter:
    """Manages rate limiters and concurrency locks across all providers."""

    def __init__(self, default_rps: float = 30.0):
        self.default_rps = default_rps
        self._limiters: Dict[str, TokenBucketLimiter] = {}
        self._semaphores: Dict[str, asyncio.Semaphore] = {}

    def get_limiter(self, provider_name: str, rps: Optional[float] = None) -> TokenBucketLimiter:
        if provider_name not in self._limiters:
            self._limiters[provider_name] = TokenBucketLimiter(rate_per_second=rps or self.default_rps)
        return self._limiters[provider_name]

    def get_semaphore(self, provider_name: str, max_concurrent: int = 10) -> asyncio.Semaphore:
        if provider_name not in self._semaphores:
            self._semaphores[provider_name] = asyncio.Semaphore(max_concurrent)
        return self._semaphores[provider_name]
