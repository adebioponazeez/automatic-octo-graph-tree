"""
Tests for central RouterEngine routing strategies, fallbacks, and execution.
"""

import pytest
from octo_harness.config import Settings
from octo_harness.models import (
    ChatMessage,
    ChatRole,
    CompletionRequest,
    ModelCapability,
    ModelSpec,
    ProviderType,
    RoutingStrategy,
)
from octo_harness.providers.mock_provider import MockProvider
from octo_harness.router.engine import RouterEngine


@pytest.mark.asyncio
async def test_router_grok_primary_strategy():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)

    req = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content="Hello Grok router")],
        strategy=RoutingStrategy.GROK_PRIMARY,
    )
    decision = engine.route_request(req)
    assert decision.strategy == RoutingStrategy.GROK_PRIMARY
    assert decision.primary_model in ("grok-2-latest", "grok-3")

    response = await engine.complete(req)
    assert response.choices is not None
    assert response.route_decision is not None


@pytest.mark.asyncio
async def test_router_quality_first_strategy():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)

    req = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content="def solve_complex_graph_coloring():")],
        strategy=RoutingStrategy.QUALITY_FIRST,
    )
    decision = engine.route_request(req)
    assert decision.detected_intent == ModelCapability.CODE
    assert decision.strategy == RoutingStrategy.QUALITY_FIRST

    response = await engine.complete(req)
    assert response.content != ""


@pytest.mark.asyncio
async def test_router_fallback_cascade_on_failure():
    settings = Settings(mock_mode=False)
    engine = RouterEngine(settings=settings)

    # Inject failure into primary mock
    failing_provider = MockProvider(name="FailingGrok")
    failing_provider.inject_failure(count=1, message="500 Internal Error")
    engine.register_provider(ProviderType.GROK, failing_provider)

    # Register healthy backup
    healthy_backup = MockProvider(name="HealthyBackup")
    engine.register_provider(ProviderType.OPENAI, healthy_backup)

    req = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content="Critical task")],
        strategy=RoutingStrategy.GROK_PRIMARY,
        fallback_models=["gpt-4o", "mock-frontier"],
        allow_fallback=True,
    )

    response = await engine.complete(req)
    assert response is not None
    assert response.fallback_occurred is True
    assert len(response.fallback_history) > 0


@pytest.mark.asyncio
async def test_router_streaming():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)

    req = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content="Stream test query")],
    )

    chunks = []
    async for chunk in engine.stream(req):
        chunks.append(chunk)

    assert len(chunks) > 0


@pytest.mark.asyncio
async def test_router_health_status():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)

    health = await engine.get_health_status()
    assert health["status"] in ("healthy", "degraded")
    assert "providers" in health
    assert "cost_summary" in health
    assert health["active_models_count"] > 0
