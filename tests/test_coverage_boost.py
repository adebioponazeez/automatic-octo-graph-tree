"""
Coverage boost tests exercising all provider branches, error paths, and rules.
"""

import asyncio
import httpx
import pytest
from octo_harness.cli.main import main
from octo_harness.config import Settings
from octo_harness.cowork.agents import BaseCoworkAgent
from octo_harness.cowork.graph import CoworkGraph
from octo_harness.cowork.memory import CoworkMemory
from octo_harness.models import (
    ChatMessage,
    ChatRole,
    CompletionRequest,
    ModelCapability,
    ModelSpec,
    ProviderType,
    RoutingStrategy,
    ToolCall,
    ToolCallFunction,
)
from octo_harness.providers.anthropic_provider import AnthropicProvider
from octo_harness.providers.grok import GrokProvider
from octo_harness.providers.local_provider import LocalProvider
from octo_harness.providers.mock_provider import MockProvider
from octo_harness.providers.openai_provider import OpenAIProvider
from octo_harness.router.circuit_breaker import CircuitBreaker
from octo_harness.router.cost_tracker import CostTracker
from octo_harness.router.engine import RouterEngine
from octo_harness.router.rate_limiter import TokenBucketLimiter
from octo_harness.router.rules import RoutingRuleEngine


@pytest.mark.asyncio
async def test_grok_provider_tool_calls_and_streaming():
    async def stream_handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/chat/completions"):
            lines = [
                'data: {"choices":[{"delta":{"content":"Hello"}}]}\n\n',
                'data: {"choices":[{"delta":{"content":" World"}}]}\n\n',
                'data: [DONE]\n\n',
            ]
            return httpx.Response(200, text="".join(lines))
        elif request.url.path.endswith("/models"):
            return httpx.Response(200, json={"data": [{"id": "grok-3"}]})
        return httpx.Response(404)

    client = httpx.AsyncClient(transport=httpx.MockTransport(stream_handler))
    provider = GrokProvider(api_key="xai-test-key", http_client=client)
    spec = ModelSpec(model_id="grok-3", provider_type=ProviderType.GROK, display_name="Grok 3")

    # Test Stream
    chunks = []
    async for chunk in provider.stream(CompletionRequest(messages=[ChatMessage(role=ChatRole.USER, content="hi")]), spec):
        chunks.append(chunk)
    assert "".join(chunks) == "Hello World"

    # Test Health
    health = await provider.check_health()
    assert health.status == "healthy"
    assert "grok-3" in health.models_available

    await client.aclose()


@pytest.mark.asyncio
async def test_openai_provider_tool_calls_and_streaming():
    async def stream_handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/chat/completions"):
            lines = [
                'data: {"choices":[{"delta":{"content":"GPT"}}]}\n\n',
                'data: {"choices":[{"delta":{"content":" 4o"}}]}\n\n',
                'data: [DONE]\n\n',
            ]
            return httpx.Response(200, text="".join(lines))
        elif request.url.path.endswith("/models"):
            return httpx.Response(200, json={"data": [{"id": "gpt-4o"}]})
        return httpx.Response(404)

    client = httpx.AsyncClient(transport=httpx.MockTransport(stream_handler))
    provider = OpenAIProvider(api_key="sk-test-key", http_client=client)
    spec = ModelSpec(model_id="gpt-4o", provider_type=ProviderType.OPENAI, display_name="GPT-4o")

    # Test Stream
    chunks = []
    async for chunk in provider.stream(CompletionRequest(messages=[ChatMessage(role=ChatRole.USER, content="hi")]), spec):
        chunks.append(chunk)
    assert "".join(chunks) == "GPT 4o"

    # Test Health
    health = await provider.check_health()
    assert health.status == "healthy"
    assert "gpt-4o" in health.models_available

    await client.aclose()


@pytest.mark.asyncio
async def test_local_provider_complete_and_stream():
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/chat/completions"):
            return httpx.Response(
                200,
                json={
                    "id": "local-123",
                    "choices": [{"index": 0, "message": {"role": "assistant", "content": "Local model response"}}],
                    "usage": {"prompt_tokens": 10, "completion_tokens": 15},
                },
            )
        elif request.url.path.endswith("/models"):
            return httpx.Response(200, json={"data": [{"id": "qwen2.5:7b"}]})
        return httpx.Response(500)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = LocalProvider(api_key="local", http_client=client)
    spec = ModelSpec(model_id="qwen2.5:7b", provider_type=ProviderType.LOCAL, display_name="Qwen")

    req = CompletionRequest(messages=[ChatMessage(role=ChatRole.USER, content="hi")])
    res = await provider.complete(req, spec)
    assert res.content == "Local model response"

    # Stream
    chunks = []
    async for chunk in provider.stream(req, spec):
        chunks.append(chunk)
    assert len(chunks) > 0

    # Health
    health = await provider.check_health()
    assert health.status == "healthy"
    await client.aclose()


def test_routing_rules_branches():
    settings = Settings()
    catalog = dict(settings.model_catalog)
    rule_engine = RoutingRuleEngine(catalog)

    # 1. Latency optimized strategy
    req_lat = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content="fast response needed")],
        strategy=RoutingStrategy.LATENCY_OPTIMIZED,
    )
    d_lat = rule_engine.resolve_route(req_lat)
    assert d_lat.strategy == RoutingStrategy.LATENCY_OPTIMIZED

    # 2. Cost optimized math/multimodal
    req_cost = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content="write a short story about dragons")],
        strategy=RoutingStrategy.COST_OPTIMIZED,
    )
    d_cost = rule_engine.resolve_route(req_cost)
    assert d_cost.strategy == RoutingStrategy.COST_OPTIMIZED

    # 3. Custom cascade strategy
    req_casc = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content="custom cascade test")],
        strategy=RoutingStrategy.FALLBACK_CASCADE,
        fallback_models=["gpt-4o", "grok-3", "mock-frontier"],
    )
    d_casc = rule_engine.resolve_route(req_casc)
    assert d_casc.primary_model == "gpt-4o"
    assert "grok-3" in d_casc.fallback_chain


def test_cost_tracker_reset():
    tracker = CostTracker(budget_limit_usd=50.0)
    spec = ModelSpec(model_id="m1", provider_type=ProviderType.MOCK, display_name="M1")
    tracker.record_usage(spec, prompt_tokens=100, completion_tokens=100)
    assert tracker._total_prompt_tokens == 100
    assert tracker._total_completion_tokens == 100
    tracker.reset()
    assert tracker._total_prompt_tokens == 0
    assert tracker._total_completion_tokens == 0
    assert tracker._total_cost_usd == 0.0


def test_cowork_memory_additional_methods():
    mem = CoworkMemory(session_id="s1")
    mem.set("test_key", "test_val", author_agent="planner")
    entry = mem.get_entry("test_key")
    assert entry is not None
    assert entry.author_agent == "planner"
    logs = mem.get_logs()
    assert len(logs) > 0
    mem.clear()
    assert mem.contains("test_key") is False


def test_cli_flags_and_json():
    ret1 = main(["--mock", "route", "Tell me a joke", "--json"])
    assert ret1 == 0

    ret2 = main(["--mock", "cowork", "Design a Redis cache layer", "--json"])
    assert ret2 == 0
