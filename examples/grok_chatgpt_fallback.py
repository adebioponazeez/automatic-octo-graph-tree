"""
Resilient Grok -> ChatGPT Fallback Cascade Example.
"""

import asyncio
from octo_harness import ChatMessage, ChatRole, CompletionRequest, RouterEngine, RoutingStrategy
from octo_harness.models import ProviderType
from octo_harness.providers.mock_provider import MockProvider


async def main():
    engine = RouterEngine()

    # 1. Simulate fault on Grok Primary provider
    print("[*] Simulating upstream 503 outage on xAI Grok provider...")
    failing_grok = MockProvider(name="Simulated-Failing-Grok")
    failing_grok.provider_type = ProviderType.GROK
    failing_grok.inject_failure(count=2, message="503 Service Unavailable: Grok Cluster Overload")
    engine.register_provider(ProviderType.GROK, failing_grok)

    # 2. Register healthy OpenAI fallback provider
    print("[*] Registering healthy OpenAI ChatGPT fallback provider...")
    healthy_openai = MockProvider(name="Healthy-OpenAI-GPT4o")
    healthy_openai.provider_type = ProviderType.OPENAI
    healthy_openai.set_mock_response(
        "dijkstra",
        "Dijkstra algorithm analysis:\n"
        "- Binary Heap: O((V + E) log V)\n"
        "- Fibonacci Heap: O(E + V log V) with amortized O(1) decrease-key operations.",
    )
    engine.register_provider(ProviderType.OPENAI, healthy_openai)

    # Dispatch request
    req = CompletionRequest(
        messages=[
            ChatMessage(
                role=ChatRole.USER,
                content="Analyze Dijkstra with Fibonacci heap vs binary heap.",
            )
        ],
        strategy=RoutingStrategy.GROK_PRIMARY,
        fallback_models=["gpt-4o", "claude-3-5-sonnet-20241022", "mock-frontier"],
        allow_fallback=True,
    )

    print("[*] Dispatching request through Router Engine with automatic fallback...")
    response = await engine.complete(req)

    print("\n" + "=" * 60)
    print(" EXECUTION TELEMETRY:")
    print("=" * 60)
    print(f" Final Model Responded: {response.model} ({response.provider.value})")
    print(f" Fallback Occurred:     {response.fallback_occurred}")
    print(" Fallback Trace:")
    for step in response.fallback_history:
        print(f"   -> {step}")
    print("=" * 60)
    print(" RESPONSE CONTENT:")
    print("=" * 60)
    print(response.content)
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
