"""
Base Abstract Provider Interface for Octo Harness.
"""

from __future__ import annotations

import abc
import time
from typing import Any, AsyncIterator, Dict, List, Optional

from octo_harness.models import (
    ChatMessage,
    CompletionRequest,
    CompletionResponse,
    ModelSpec,
    ProviderHealth,
    ProviderType,
)


class BaseProvider(abc.ABC):
    """Abstract class for all LLM providers (xAI Grok, OpenAI, Anthropic, Local, Mock)."""

    def __init__(self, name: str, provider_type: ProviderType, api_key: Optional[str] = None, base_url: str = ""):
        self.name = name
        self.provider_type = provider_type
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._total_requests: int = 0
        self._successful_requests: int = 0
        self._failed_requests: int = 0
        self._total_latency_ms: float = 0.0
        self._last_checked: float = time.time()
        self._last_error: Optional[str] = None

    @abc.abstractmethod
    async def complete(self, request: CompletionRequest, model_spec: ModelSpec) -> CompletionResponse:
        """Execute a full completion request."""
        pass

    @abc.abstractmethod
    async def stream(self, request: CompletionRequest, model_spec: ModelSpec) -> AsyncIterator[str]:
        """Stream completion tokens."""
        pass

    @abc.abstractmethod
    async def check_health(self) -> ProviderHealth:
        """Perform a live health and liveness probe."""
        pass

    def estimate_tokens(self, messages: List[ChatMessage]) -> int:
        """Heuristic token estimator (approx. 4 chars per token)."""
        char_count = sum(len(m.content or "") + len(m.role or "") + 10 for m in messages)
        return max(1, char_count // 4)

    def record_success(self, latency_ms: float) -> None:
        """Record successful request metrics."""
        self._total_requests += 1
        self._successful_requests += 1
        self._total_latency_ms += latency_ms
        self._last_checked = time.time()
        self._last_error = None

    def record_failure(self, error: str) -> None:
        """Record failed request metrics."""
        self._total_requests += 1
        self._failed_requests += 1
        self._last_checked = time.time()
        self._last_error = error

    def get_health(self) -> ProviderHealth:
        """Return cached health metrics."""
        avg_latency = (
            (self._total_latency_ms / self._successful_requests)
            if self._successful_requests > 0
            else 0.0
        )
        error_rate = (
            (self._failed_requests / self._total_requests)
            if self._total_requests > 0
            else 0.0
        )

        if not self.api_key and self.provider_type not in (ProviderType.LOCAL, ProviderType.MOCK):
            status = "unconfigured"
        elif error_rate > 0.5:
            status = "down"
        elif error_rate > 0.1:
            status = "degraded"
        else:
            status = "healthy"

        return ProviderHealth(
            provider_name=self.name,
            provider_type=self.provider_type,
            status=status,
            latency_ms=round(avg_latency, 2),
            last_checked=self._last_checked,
            error_rate=round(error_rate, 4),
            total_requests=self._total_requests,
            successful_requests=self._successful_requests,
            failed_requests=self._failed_requests,
        )
