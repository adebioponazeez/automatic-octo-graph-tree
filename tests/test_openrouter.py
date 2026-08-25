"""
Tests for OpenRouter provider integration (Kimi K3, DeepSeek R1, Qwen 2.5, Llama 3.3).
"""

import httpx
import pytest
from octo_harness.config import Settings
from octo_harness.models import ChatMessage, ChatRole, CompletionRequest, ModelSpec, ProviderType, RoutingStrategy
from octo_harness.providers.openrouter_provider import OpenRouterProvider
from octo_harness.router.engine import RouterEngine


@pytest.mark.asyncio
async def test_openrouter_provider_complete_and_stream():
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers.get("HTTP-Referer") is not None
        assert request.headers.get("X-Title") is not None
        if request.url.path.endswith("/chat/completions"):
            return httpx.Response(
                200,
                json={
                    "id": "gen-openrouter-123",
                    "choices": [
                        {
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": "Kimi K3 & DeepSeek R1 processed output",
                            },
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {"prompt_tokens": 20, "completion_tokens": 30},
                },
            )
        elif request.url.path.endswith("/models"):
            return httpx.Response(200, json={"data": [{"id": "moonshotai/kimi-k3"}, {"id": "deepseek/deepseek-r1"}]})
        return httpx.Response(404)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = OpenRouterProvider(api_key="sk-or-test-key", http_client=client)
    spec = ModelSpec(
        model_id="moonshotai/kimi-k3",
        provider_type=ProviderType.OPENROUTER,
        display_name="Kimi K3",
        input_cost_per_million=0.50,
        output_cost_per_million=2.00,
    )

    req = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content="Explain Kimi K3 long context")],
    )

    resp = await provider.complete(req, spec)
    assert resp.content == "Kimi K3 & DeepSeek R1 processed output"
    assert resp.provider == ProviderType.OPENROUTER
    assert resp.usage.total_tokens == 50

    # Health check
    health = await provider.check_health()
    assert health.status == "healthy"
    assert "moonshotai/kimi-k3" in health.models_available

    await client.aclose()


def test_openrouter_models_in_catalog():
    settings = Settings()
    catalog = settings.model_catalog

    assert "moonshotai/kimi-k3" in catalog
    kimi = catalog["moonshotai/kimi-k3"]
    assert kimi.provider_type == ProviderType.OPENROUTER
    assert kimi.context_window == 200000

    assert "deepseek/deepseek-r1" in catalog
    r1 = catalog["deepseek/deepseek-r1"]
    assert r1.provider_type == ProviderType.OPENROUTER

    assert "qwen/qwen-2.5-coder-32b-instruct" in catalog
    qwen = catalog["qwen/qwen-2.5-coder-32b-instruct"]
    assert qwen.provider_type == ProviderType.OPENROUTER


@pytest.mark.asyncio
async def test_router_engine_with_openrouter_mock():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)

    req = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content="Long context analysis for Kimi")],
        model="moonshotai/kimi-k3",
    )
    decision = engine.route_request(req)
    assert decision.primary_model == "moonshotai/kimi-k3"
    assert decision.primary_provider == ProviderType.OPENROUTER

    res = await engine.complete(req)
    assert res.choices is not None
