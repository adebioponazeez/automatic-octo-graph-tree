"""
Central Router Engine orchestrating multi-model dispatch, fallbacks, circuit breaking,
rate limiting, token cost tracking, and streaming.
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, AsyncIterator, Dict, List, Optional

from octo_harness.config import Settings, get_settings
from octo_harness.models import (
    ChatMessage,
    CompletionRequest,
    CompletionResponse,
    ModelSpec,
    ProviderHealth,
    ProviderType,
    RouteDecision,
    RoutingStrategy,
)
from octo_harness.providers.anthropic_provider import AnthropicProvider
from octo_harness.providers.base import BaseProvider
from octo_harness.providers.grok import GrokProvider
from octo_harness.providers.local_provider import LocalProvider
from octo_harness.providers.mock_provider import MockProvider
from octo_harness.providers.openai_provider import OpenAIProvider
from octo_harness.providers.openrouter_provider import OpenRouterProvider
from octo_harness.router.batch_processor import BatchJob, BatchProcessor
from octo_harness.router.circuit_breaker import CircuitBreakerRegistry
from octo_harness.router.context_cache import ContextCacheEngine
from octo_harness.router.cost_tracker import BudgetExceededError, CostTracker
from octo_harness.router.rate_limiter import ProviderRateLimiter
from octo_harness.router.rules import RoutingRuleEngine

logger = logging.getLogger("octo_harness.router")


class RouterEngine:
    """
    High-performance Multi-Model Router Harness for xAI Grok, OpenAI ChatGPT, Anthropic Claude,
    and Local LLMs.
    """

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self.catalog: Dict[str, ModelSpec] = dict(self.settings.model_catalog)
        self.rule_engine = RoutingRuleEngine(self.catalog)
        self.circuit_breakers = CircuitBreakerRegistry(
            default_threshold=self.settings.circuit_breaker_failure_threshold,
            default_timeout=self.settings.circuit_breaker_recovery_timeout_s,
        )
        self.rate_limiter = ProviderRateLimiter()
        self.cost_tracker = CostTracker(budget_limit_usd=self.settings.budget_limit_usd)
        self.context_cache = ContextCacheEngine()
        self.batch_processor = BatchProcessor(self)
        self.providers: Dict[ProviderType, BaseProvider] = {}

        self._init_providers()

    def _init_providers(self) -> None:
        """Initialize provider adapters based on environment settings."""
        # xAI Grok Provider
        self.providers[ProviderType.GROK] = GrokProvider(
            api_key=self.settings.grok.api_key,
            base_url=self.settings.grok.base_url,
            timeout_seconds=self.settings.grok.timeout_seconds,
        )

        # OpenAI Provider
        self.providers[ProviderType.OPENAI] = OpenAIProvider(
            api_key=self.settings.openai.api_key,
            base_url=self.settings.openai.base_url,
            timeout_seconds=self.settings.openai.timeout_seconds,
        )

        # Anthropic Claude Provider
        self.providers[ProviderType.ANTHROPIC] = AnthropicProvider(
            api_key=self.settings.anthropic.api_key,
            base_url=self.settings.anthropic.base_url,
            timeout_seconds=self.settings.anthropic.timeout_seconds,
        )

        # OpenRouter Provider (Kimi K3, DeepSeek R1/V3, Qwen 2.5, Llama 3.3)
        self.providers[ProviderType.OPENROUTER] = OpenRouterProvider(
            api_key=self.settings.openrouter.api_key,
            base_url=self.settings.openrouter.base_url,
            timeout_seconds=self.settings.openrouter.timeout_seconds,
        )

        # Local Provider (Ollama / vLLM)
        self.providers[ProviderType.LOCAL] = LocalProvider(
            api_key=self.settings.local.api_key,
            base_url=self.settings.local.base_url,
            timeout_seconds=self.settings.local.timeout_seconds,
        )

        # Mock Provider (Always available for tests and fallback safety)
        self.providers[ProviderType.MOCK] = MockProvider(
            name="Mock-Frontier",
            simulate_latency_ms=10.0 if not self.settings.mock_mode else 5.0,
        )

    def register_provider(self, provider_type: ProviderType, provider: BaseProvider) -> None:
        """Register or override a provider implementation."""
        self.providers[provider_type] = provider

    def register_model(self, model_spec: ModelSpec) -> None:
        """Add or update a model specification in the catalog."""
        self.catalog[model_spec.model_id] = model_spec
        self.rule_engine = RoutingRuleEngine(self.catalog)

    def route_request(self, request: CompletionRequest) -> RouteDecision:
        """Analyze request and return route decision without executing."""
        return self.rule_engine.resolve_route(request)

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """
        Executes a completion with dynamic routing, circuit breaking,
        rate limiting, and multi-tier fallback cascade.
        """
        start_time = time.time()

        # 1. Check budget ceiling
        if not self.cost_tracker.check_budget_available():
            raise BudgetExceededError(
                f"Budget limit of ${self.settings.budget_limit_usd:.2f} exceeded. Current spent: ${self.cost_tracker._total_cost_usd:.2f}"
            )

        # 2. Determine routing decision
        decision = self.route_request(request)

        # 3. Build candidate trial chain
        candidates: List[str] = [decision.primary_model]
        if request.allow_fallback:
            for fb in decision.fallback_chain:
                if fb not in candidates:
                    candidates.append(fb)

        # Always append mock fallback in test or mock mode
        if self.settings.mock_mode or "mock-frontier" not in candidates:
            candidates.append("mock-frontier")

        fallback_history: List[str] = []
        last_exception: Optional[Exception] = None

        for model_id in candidates:
            if model_id not in self.catalog:
                continue

            model_spec = self.catalog[model_id]
            provider_type = model_spec.provider_type
            provider = self.providers.get(provider_type)

            if not provider:
                fallback_history.append(f"Model {model_id} skipped: provider {provider_type} not registered")
                continue

            # Check if mock mode is globally forced
            if self.settings.mock_mode and provider_type != ProviderType.MOCK:
                # In mock mode, swap to mock provider
                provider = self.providers[ProviderType.MOCK]

            # Check provider configured API key
            if not self.settings.mock_mode and not provider.api_key and provider_type not in (ProviderType.LOCAL, ProviderType.MOCK):
                fallback_history.append(f"Model {model_id} skipped: {provider_type.value} API key not set")
                continue

            # Check Circuit Breaker
            breaker = self.circuit_breakers.get_breaker(f"{provider_type.value}:{model_id}")
            if not breaker.can_execute():
                fallback_history.append(f"Model {model_id} skipped: circuit breaker {breaker.state.value}")
                continue

            # Rate Limiter
            limiter = self.rate_limiter.get_limiter(provider_type.value)
            acquired = await limiter.acquire(tokens_needed=1.0, wait=True, timeout_s=1.0)
            if not acquired:
                fallback_history.append(f"Model {model_id} skipped: rate limit saturated")
                continue

            # Attempt Execution
            try:
                logger.info(f"Attempting dispatch to {model_id} ({provider_type.value})")
                response = await asyncio.wait_for(
                    provider.complete(request, model_spec),
                    timeout=request.timeout_seconds,
                )

                # Record Success & Costs
                breaker.record_success()

                # Check context caching savings
                is_hit, cached_toks, saved_usd = self.context_cache.check_and_apply_cache(
                    request.messages, model_spec.input_cost_per_million
                )
                if is_hit and saved_usd > 0:
                    response.usage.estimated_cost_usd = max(0.0, response.usage.estimated_cost_usd - saved_usd)

                self.cost_tracker.record_usage(
                    model_spec,
                    response.usage.prompt_tokens,
                    response.usage.completion_tokens,
                )

                # Annotate response with routing telemetry
                response.route_decision = decision
                response.fallback_occurred = (model_id != decision.primary_model)
                response.fallback_history = fallback_history
                response.latency_ms = round((time.time() - start_time) * 1000.0, 2)

                return response

            except Exception as exc:
                last_exception = exc
                breaker.record_failure()
                fallback_history.append(f"Model {model_id} failed: {type(exc).__name__} ({str(exc)[:100]})")
                logger.warning(f"Execution failed on {model_id}, falling back: {exc}")
                continue

        # If all candidates in chain failed, synthesize emergency mock response
        logger.error(f"All models in fallback chain failed: {fallback_history}")
        mock_spec = self.catalog.get("mock-frontier", list(self.catalog.values())[0])
        mock_provider = self.providers.get(ProviderType.MOCK, MockProvider())
        emergency_response = await mock_provider.complete(request, mock_spec)
        emergency_response.route_decision = decision
        emergency_response.fallback_occurred = True
        emergency_response.fallback_history = fallback_history + ["Emergency fallback to mock provider"]
        emergency_response.latency_ms = round((time.time() - start_time) * 1000.0, 2)
        return emergency_response

    async def stream(self, request: CompletionRequest) -> AsyncIterator[str]:
        """Stream tokens from primary or fallback model."""
        decision = self.route_request(request)
        model_id = decision.primary_model
        model_spec = self.catalog.get(model_id, self.catalog["mock-frontier"])
        provider = self.providers.get(model_spec.provider_type, self.providers[ProviderType.MOCK])

        if self.settings.mock_mode or not provider.api_key and model_spec.provider_type not in (ProviderType.LOCAL, ProviderType.MOCK):
            provider = self.providers[ProviderType.MOCK]

        async for chunk in provider.stream(request, model_spec):
            yield chunk

    async def get_health_status(self) -> Dict[str, Any]:
        """Collect live health status from all registered providers and circuits."""
        provider_health_tasks = [provider.check_health() for provider in self.providers.values()]
        results = await asyncio.gather(*provider_health_tasks, return_exceptions=True)

        health_map: Dict[str, Any] = {}
        for provider_type, res in zip(self.providers.keys(), results):
            if isinstance(res, ProviderHealth):
                health_map[provider_type.value] = res.model_dump()
            else:
                health_map[provider_type.value] = {
                    "status": "error",
                    "error": str(res),
                }

        return {
            "status": "healthy" if any(h.get("status") == "healthy" for h in health_map.values() if isinstance(h, dict)) else "degraded",
            "providers": health_map,
            "circuit_breakers": self.circuit_breakers.get_all_states(),
            "cost_summary": self.cost_tracker.get_summary(),
            "context_cache": self.context_cache.get_cache_stats(),
            "batch_queue": self.batch_processor.get_queue_status(),
            "active_models_count": len([m for m in self.catalog.values() if m.is_active]),
            "timestamp": time.time(),
        }
