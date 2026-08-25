"""
Tests for Token Bucket Rate Limiter and Concurrency Controls.
"""

import asyncio
import pytest
from octo_harness.router.rate_limiter import ProviderRateLimiter, TokenBucketLimiter


@pytest.mark.asyncio
async def test_token_bucket_acquire():
    limiter = TokenBucketLimiter(rate_per_second=10.0, capacity=2.0)
    # Acquire available burst
    assert await limiter.acquire(1.0, wait=False) is True
    assert await limiter.acquire(1.0, wait=False) is True
    # Capacity depleted
    assert await limiter.acquire(1.0, wait=False) is False

    # Wait for refill
    await asyncio.sleep(0.15)
    assert await limiter.acquire(1.0, wait=True, timeout_s=0.5) is True


@pytest.mark.asyncio
async def test_provider_rate_limiter_manager():
    mgr = ProviderRateLimiter(default_rps=20.0)
    limiter = mgr.get_limiter("grok")
    assert limiter is not None
    sem = mgr.get_semaphore("grok", max_concurrent=5)
    assert sem is not None
