"""
Tests for provider adapters (Mock, Grok, OpenAI, Anthropic, Local).
"""

import pytest
import httpx
from octo_harness.models import ChatMessage, ChatRole, CompletionRequest, ModelCapability, ModelSpec, ProviderType
from octo_harness.providers.anthropic_provider import AnthropicProvider
from octo_harness.providers.grok import GrokProvider
from octo_harness.providers.local_provider import LocalProvider
from octo_harness.providers.mock_provider import MockProvider
from octo_harness.providers.openai_provider import OpenAIProvider


@pytest.mark.asyncio
async def test_mock_provider_complete():
    provider = MockProvider(simulate_latency_ms=0.0)
    spec = ModelSpec(
        model_id="mock-frontier",
        provider_type=ProviderType.MOCK,
        display_name="Mock Frontier",
    )
    req = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content="Write Python code for sorting list")],
    )

    resp = await provider.complete(req, spec)
    assert resp.model == "mock-frontier"
    assert resp.provider == ProviderType.MOCK
    assert "def " in resp.content
    assert resp.usage.total_tokens > 0


@pytest.mark.asyncio
async def test_mock_provider_canned_response():
    provider = MockProvider(simulate_latency_ms=0.0)
    provider.set_mock_response("special query", "Custom canned answer 123")
    spec = ModelSpec(
        model_id="mock-frontier",
        provider_type=ProviderType.MOCK,
        display_name="Mock Frontier",
    )
    req = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content="This is a special query test")],
    )

    resp = await provider.complete(req, spec)
    assert resp.content == "Custom canned answer 123"


@pytest.mark.asyncio
async def test_mock_provider_fault_injection():
    provider = MockProvider(simulate_latency_ms=0.0)
    provider.inject_failure(count=1, message="Injected Outage")
    spec = ModelSpec(
        model_id="mock-frontier",
        provider_type=ProviderType.MOCK,
        display_name="Mock Frontier",
    )
    req = CompletionRequest(messages=[ChatMessage(role=ChatRole.USER, content="test")])

    with pytest.raises(RuntimeError) as exc_info:
        await provider.complete(req, spec)
    assert "Injected Outage" in str(exc_info.value)

    # Next request succeeds
    resp = await provider.complete(req, spec)
    assert resp.content != ""


@pytest.mark.asyncio
async def test_mock_provider_stream():
    provider = MockProvider(simulate_latency_ms=0.0)
    spec = ModelSpec(
        model_id="mock-frontier",
        provider_type=ProviderType.MOCK,
        display_name="Mock Frontier",
    )
    req = CompletionRequest(messages=[ChatMessage(role=ChatRole.USER, content="hello")])

    chunks = []
    async for chunk in provider.stream(req, spec):
        chunks.append(chunk)

    assert len(chunks) > 0
    full_text = "".join(chunks)
    assert len(full_text) > 0


@pytest.mark.asyncio
async def test_grok_provider_mock_client():
    # Test GrokProvider with mocked HTTP transport
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "id": "grok-mock-123",
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": "Grok 3 reasoning result"},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {"prompt_tokens": 15, "completion_tokens": 20},
            },
        )

    mock_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = GrokProvider(api_key="xai-test-key", http_client=mock_client)
    spec = ModelSpec(
        model_id="grok-3",
        provider_type=ProviderType.GROK,
        display_name="Grok 3",
    )
    req = CompletionRequest(messages=[ChatMessage(role=ChatRole.USER, content="Hello Grok")])

    resp = await provider.complete(req, spec)
    assert resp.content == "Grok 3 reasoning result"
    assert resp.provider == ProviderType.GROK
    assert resp.usage.prompt_tokens == 15
    await mock_client.aclose()


@pytest.mark.asyncio
async def test_openai_provider_mock_client():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "id": "chatcmpl-openai-mock",
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": "GPT-4o output"},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {"prompt_tokens": 10, "completion_tokens": 15},
            },
        )

    mock_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = OpenAIProvider(api_key="sk-test-key", http_client=mock_client)
    spec = ModelSpec(
        model_id="gpt-4o",
        provider_type=ProviderType.OPENAI,
        display_name="GPT-4o",
    )
    req = CompletionRequest(messages=[ChatMessage(role=ChatRole.USER, content="Hello OpenAI")])

    resp = await provider.complete(req, spec)
    assert resp.content == "GPT-4o output"
    assert resp.provider == ProviderType.OPENAI
    await mock_client.aclose()


@pytest.mark.asyncio
async def test_anthropic_provider_mock_client():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "id": "msg-anthropic-mock",
                "content": [{"type": "text", "text": "Claude 3.5 Sonnet analysis"}],
                "stop_reason": "end_turn",
                "usage": {"input_tokens": 12, "output_tokens": 25},
            },
        )

    mock_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = AnthropicProvider(api_key="ant-test-key", http_client=mock_client)
    spec = ModelSpec(
        model_id="claude-3-5-sonnet-20241022",
        provider_type=ProviderType.ANTHROPIC,
        display_name="Claude 3.5 Sonnet",
    )
    req = CompletionRequest(
        messages=[
            ChatMessage(role=ChatRole.SYSTEM, content="System guidelines"),
            ChatMessage(role=ChatRole.USER, content="Perform analysis"),
        ]
    )

    resp = await provider.complete(req, spec)
    assert resp.content == "Claude 3.5 Sonnet analysis"
    assert resp.provider == ProviderType.ANTHROPIC
    await mock_client.aclose()
