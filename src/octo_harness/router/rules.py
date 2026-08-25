"""
Routing rules and strategy decision logic for Octo Harness.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from octo_harness.models import (
    ChatMessage,
    CompletionRequest,
    ModelCapability,
    ModelSpec,
    ProviderType,
    RouteDecision,
    RoutingStrategy,
)
from octo_harness.router.classifier import PromptClassifier


class RoutingRuleEngine:
    """
    Evaluates incoming completion requests, classified intents, and available model catalog
    to synthesize an optimal RouteDecision and resilient fallback chain.
    """

    def __init__(self, catalog: Dict[str, ModelSpec]):
        self.catalog = catalog
        self.classifier = PromptClassifier()

    def resolve_route(self, request: CompletionRequest) -> RouteDecision:
        """Determines the primary model and ordered fallback sequence for a request."""
        # 1. Intent & capability classification
        intent, confidence, reason = self.classifier.classify_prompt(request.messages)

        # If user explicitly requested capabilities, merge/override
        if request.required_capabilities:
            intent = request.required_capabilities[0]
            confidence = 1.0
            reason = f"Explicitly requested capability: {intent.value}"

        strategy = request.strategy

        # 2. If user explicitly specified a model, honor it with default fallback
        if request.model and request.model in self.catalog:
            primary_spec = self.catalog[request.model]
            fallback_chain = self._build_default_fallbacks(primary_spec.model_id, intent)
            if request.fallback_models:
                fallback_chain = [m for m in request.fallback_models if m in self.catalog and m != primary_spec.model_id]

            return RouteDecision(
                primary_model=primary_spec.model_id,
                primary_provider=primary_spec.provider_type,
                fallback_chain=fallback_chain,
                strategy=strategy,
                detected_intent=intent,
                confidence=confidence,
                reason=f"Explicit model '{request.model}' requested. {reason}",
            )

        # 3. Strategy resolution
        if strategy == RoutingStrategy.GROK_PRIMARY:
            return self._resolve_grok_primary(intent, confidence, reason, request)
        elif strategy == RoutingStrategy.QUALITY_FIRST:
            return self._resolve_quality_first(intent, confidence, reason, request)
        elif strategy == RoutingStrategy.COST_OPTIMIZED:
            return self._resolve_cost_optimized(intent, confidence, reason, request)
        elif strategy == RoutingStrategy.LATENCY_OPTIMIZED:
            return self._resolve_latency_optimized(intent, confidence, reason, request)
        elif strategy == RoutingStrategy.FALLBACK_CASCADE:
            return self._resolve_custom_cascade(intent, confidence, reason, request)
        else:
            return self._resolve_grok_primary(intent, confidence, reason, request)

    def _resolve_grok_primary(
        self, intent: ModelCapability, confidence: float, reason: str, request: CompletionRequest
    ) -> RouteDecision:
        """Route to xAI Grok as primary, with seamless ChatGPT / Claude / OpenRouter / Local fallbacks."""
        if intent in (ModelCapability.REASONING, ModelCapability.CODE, ModelCapability.MATH) and "grok-3" in self.catalog:
            primary_model = "grok-3"
            fallbacks = ["gpt-4o", "deepseek/deepseek-r1", "claude-3-5-sonnet-20241022", "qwen/qwen-2.5-coder-32b-instruct", "grok-2-latest", "mock-frontier"]
        elif intent == ModelCapability.MULTIMODAL and "grok-2-vision-1212" in self.catalog:
            primary_model = "grok-2-vision-1212"
            fallbacks = ["gpt-4o", "claude-3-5-sonnet-20241022", "mock-frontier"]
        elif intent == ModelCapability.LONG_CONTEXT and "moonshotai/kimi-k3" in self.catalog:
            primary_model = "moonshotai/kimi-k3"
            fallbacks = ["grok-3", "claude-3-5-sonnet-20241022", "gpt-4o", "mock-frontier"]
        else:
            primary_model = "grok-2-latest" if "grok-2-latest" in self.catalog else "grok-3"
            fallbacks = ["gpt-4o", "deepseek/deepseek-chat", "gpt-4o-mini", "claude-3-5-haiku-20241022", "mock-frontier"]

        # Filter available in catalog
        fallbacks = [m for m in fallbacks if m in self.catalog and m != primary_model]
        if request.fallback_models:
            fallbacks = [m for m in request.fallback_models if m in self.catalog and m != primary_model]

        spec = self.catalog.get(primary_model, list(self.catalog.values())[0])
        return RouteDecision(
            primary_model=spec.model_id,
            primary_provider=spec.provider_type,
            fallback_chain=fallbacks,
            strategy=RoutingStrategy.GROK_PRIMARY,
            detected_intent=intent,
            confidence=confidence,
            reason=f"Grok-Primary policy applied for {intent.value}. {reason}",
        )

    def _resolve_quality_first(
        self, intent: ModelCapability, confidence: float, reason: str, request: CompletionRequest
    ) -> RouteDecision:
        """Route to highest benchmark capability model for the detected task."""
        if intent in (ModelCapability.CODE, ModelCapability.REASONING):
            primary_model = "claude-3-5-sonnet-20241022" if "claude-3-5-sonnet-20241022" in self.catalog else "grok-3"
            fallbacks = ["grok-3", "gpt-4o", "o3-mini", "mock-frontier"]
        elif intent == ModelCapability.MATH:
            primary_model = "o3-mini" if "o3-mini" in self.catalog else "grok-3"
            fallbacks = ["grok-3", "gpt-4o", "claude-3-5-sonnet-20241022", "mock-frontier"]
        else:
            primary_model = "gpt-4o" if "gpt-4o" in self.catalog else "grok-3"
            fallbacks = ["grok-3", "claude-3-5-sonnet-20241022", "mock-frontier"]

        fallbacks = [m for m in fallbacks if m in self.catalog and m != primary_model]
        spec = self.catalog.get(primary_model, list(self.catalog.values())[0])
        return RouteDecision(
            primary_model=spec.model_id,
            primary_provider=spec.provider_type,
            fallback_chain=fallbacks,
            strategy=RoutingStrategy.QUALITY_FIRST,
            detected_intent=intent,
            confidence=confidence,
            reason=f"Quality-First frontier selection for {intent.value}. {reason}",
        )

    def _resolve_cost_optimized(
        self, intent: ModelCapability, confidence: float, reason: str, request: CompletionRequest
    ) -> RouteDecision:
        """Route to cheapest model that satisfies minimum capability threshold."""
        if intent == ModelCapability.CODE and "qwen2.5-coder:7b" in self.catalog:
            primary_model = "qwen2.5-coder:7b"
            fallbacks = ["gpt-4o-mini", "claude-3-5-haiku-20241022", "grok-2-latest", "mock-frontier"]
        elif intent in (ModelCapability.FAST_CHAT, ModelCapability.EXTRACTION):
            primary_model = "gpt-4o-mini" if "gpt-4o-mini" in self.catalog else "claude-3-5-haiku-20241022"
            fallbacks = ["claude-3-5-haiku-20241022", "grok-2-latest", "mock-frontier"]
        else:
            primary_model = "gpt-4o-mini" if "gpt-4o-mini" in self.catalog else "grok-2-latest"
            fallbacks = ["claude-3-5-haiku-20241022", "grok-2-latest", "gpt-4o", "mock-frontier"]

        fallbacks = [m for m in fallbacks if m in self.catalog and m != primary_model]
        spec = self.catalog.get(primary_model, list(self.catalog.values())[0])
        return RouteDecision(
            primary_model=spec.model_id,
            primary_provider=spec.provider_type,
            fallback_chain=fallbacks,
            strategy=RoutingStrategy.COST_OPTIMIZED,
            detected_intent=intent,
            confidence=confidence,
            reason=f"Cost-Optimized economic route for {intent.value}. {reason}",
        )

    def _resolve_latency_optimized(
        self, intent: ModelCapability, confidence: float, reason: str, request: CompletionRequest
    ) -> RouteDecision:
        """Route to lowest average latency model."""
        # Find active model with lowest latency
        candidates = sorted(
            [s for s in self.catalog.values() if s.is_active and s.provider_type != ProviderType.MOCK],
            key=lambda s: s.average_latency_ms
        )
        primary_spec = candidates[0] if candidates else list(self.catalog.values())[0]
        fallbacks = [s.model_id for s in candidates[1:]] + ["mock-frontier"]

        return RouteDecision(
            primary_model=primary_spec.model_id,
            primary_provider=primary_spec.provider_type,
            fallback_chain=fallbacks[:4],
            strategy=RoutingStrategy.LATENCY_OPTIMIZED,
            detected_intent=intent,
            confidence=confidence,
            reason=f"Latency-Optimized route (avg {primary_spec.average_latency_ms}ms). {reason}",
        )

    def _resolve_custom_cascade(
        self, intent: ModelCapability, confidence: float, reason: str, request: CompletionRequest
    ) -> RouteDecision:
        """Custom user specified fallback chain."""
        models = request.fallback_models or ["grok-2-latest", "gpt-4o", "mock-frontier"]
        valid_models = [m for m in models if m in self.catalog]
        if not valid_models:
            valid_models = ["mock-frontier"]

        primary_model = valid_models[0]
        fallbacks = valid_models[1:]
        spec = self.catalog[primary_model]

        return RouteDecision(
            primary_model=spec.model_id,
            primary_provider=spec.provider_type,
            fallback_chain=fallbacks,
            strategy=RoutingStrategy.FALLBACK_CASCADE,
            detected_intent=intent,
            confidence=confidence,
            reason=f"Custom cascade sequence: {' -> '.join(valid_models)}",
        )

    def _build_default_fallbacks(self, primary_model_id: str, intent: ModelCapability) -> List[str]:
        defaults = ["grok-2-latest", "gpt-4o", "claude-3-5-sonnet-20241022", "gpt-4o-mini", "mock-frontier"]
        return [m for m in defaults if m in self.catalog and m != primary_model_id]
