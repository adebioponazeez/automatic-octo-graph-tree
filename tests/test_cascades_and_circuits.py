"""
Tests for complex multi-tier fallback cascades and circuit breaker interactions.
"""

import pytest
from octo_harness.config import Settings
from octo_harness.models import ChatMessage, ChatRole, CompletionRequest, ProviderType, RoutingStrategy
from octo_harness.providers.mock_provider import MockProvider
from octo_harness.router.engine import RouterEngine


@pytest.mark.asyncio
async def test_four_tier_fallback_cascade():
    settings = Settings(mock_mode=False)
    engine = RouterEngine(settings=settings)

    # Provider 1: Grok fails
    grok_mock = MockProvider(name="GrokFail")
    grok_mock.inject_failure(count=5, message="Grok 503 Outage")
    engine.register_provider(ProviderType.GROK, grok_mock)

    # Provider 2: OpenAI fails
    openai_mock = MockProvider(name="OpenAIFail")
    openai_mock.inject_failure(count=5, message="OpenAI 429 RateLimit")
    engine.register_provider(ProviderType.OPENAI, openai_mock)

    # Provider 3: Anthropic succeeds
    anthropic_mock = MockProvider(name="AnthropicSuccess")
    anthropic_mock.set_mock_response("cascade test", "Successfully processed by Anthropic Claude fallback")
    engine.register_provider(ProviderType.ANTHROPIC, anthropic_mock)

    req = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content="This is a cascade test query")],
        strategy=RoutingStrategy.FALLBACK_CASCADE,
        fallback_models=["grok-3", "gpt-4o", "claude-3-5-sonnet-20241022", "mock-frontier"],
    )

    resp = await engine.complete(req)

    assert resp.model == "claude-3-5-sonnet-20241022"
    assert resp.fallback_occurred is True
    assert len(resp.fallback_history) >= 2
    assert "Successfully processed by Anthropic" in resp.content


@pytest.mark.asyncio
async def test_circuit_breaker_tripping_and_skipping():
    settings = Settings(mock_mode=False)
    engine = RouterEngine(settings=settings)

    # Force Grok circuit breaker to trip OPEN
    grok_mock = MockProvider(name="GrokFail")
    grok_mock.inject_failure(count=10, message="Persistent Outage")
    engine.register_provider(ProviderType.GROK, grok_mock)

    # Healthy fallback
    healthy = MockProvider(name="HealthyFallback")
    engine.register_provider(ProviderType.MOCK, healthy)

    req = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content="Task 1")],
        model="grok-3",
        fallback_models=["mock-frontier"],
    )

    # Trip the breaker by failing enough times
    for _ in range(settings.circuit_breaker_failure_threshold):
        await engine.complete(req)

    breaker = engine.circuit_breakers.get_breaker("grok:grok-3")
    assert breaker.state.value == "OPEN"

    # Next request should immediately skip grok without executing it
    resp_skipped = await engine.complete(req)
    assert resp_skipped.model == "mock-frontier"
    assert any("circuit breaker OPEN" in step for step in resp_skipped.fallback_history)
