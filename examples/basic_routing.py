"""
Basic Routing Example using Octo Harness.
"""

import asyncio
from octo_harness import ChatMessage, ChatRole, CompletionRequest, RouterEngine, RoutingStrategy


async def main():
    engine = RouterEngine()

    print("--- 1. Testing Code Generation Routing (Auto-classified to Code) ---")
    req_code = CompletionRequest(
        messages=[
            ChatMessage(
                role=ChatRole.USER,
                content="Write a Python async function to batch process jobs concurrently.",
            )
        ],
        strategy=RoutingStrategy.GROK_PRIMARY,
    )
    res_code = await engine.complete(req_code)
    print(f"Selected Model: {res_code.model} ({res_code.provider.value})")
    print(f"Detected Intent: {res_code.route_decision.detected_intent.value}")
    print(f"Response:\n{res_code.content}\n")

    print("--- 2. Testing Cost-Optimized Fast Chat Routing ---")
    req_chat = CompletionRequest(
        messages=[
            ChatMessage(
                role=ChatRole.USER,
                content="Hi there! What is the capital of Nigeria?",
            )
        ],
        strategy=RoutingStrategy.COST_OPTIMIZED,
    )
    res_chat = await engine.complete(req_chat)
    print(f"Selected Model: {res_chat.model} ({res_chat.provider.value})")
    print(f"Estimated Cost: ${res_chat.usage.estimated_cost_usd:.6f}")
    print(f"Response:\n{res_chat.content}\n")


if __name__ == "__main__":
    asyncio.run(main())
