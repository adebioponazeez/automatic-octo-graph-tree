"""
Deterministic Mock Provider for unit testing, CI/CD, and offline demonstration.
"""

from __future__ import annotations

import asyncio
import json
import time
import uuid
from typing import Any, AsyncIterator, Dict, List, Optional

from octo_harness.models import (
    ChatMessage,
    ChatRole,
    Choice,
    CompletionRequest,
    CompletionResponse,
    ModelCapability,
    ModelSpec,
    ProviderHealth,
    ProviderType,
    ToolCall,
    ToolCallFunction,
    UsageInfo,
)
from octo_harness.providers.base import BaseProvider


class MockProvider(BaseProvider):
    """
    Simulated LLM provider for zero-cost offline testing, CI gates, and resilience verification.
    Supports fault injection (simulated timeouts, HTTP 500s, rate limits).
    """

    def __init__(
        self,
        name: str = "MockProvider",
        api_key: Optional[str] = "mock-key",
        simulate_latency_ms: float = 10.0,
        fail_next_n_requests: int = 0,
        fail_error_message: str = "Simulated upstream provider error (503 Service Unavailable)",
    ):
        super().__init__(name=name, provider_type=ProviderType.MOCK, api_key=api_key, base_url="http://mock-api.local")
        self.simulate_latency_ms = simulate_latency_ms
        self.fail_next_n_requests = fail_next_n_requests
        self.fail_error_message = fail_error_message
        self._mock_responses: Dict[str, str] = {}

    def set_mock_response(self, prompt_substring: str, response_text: str) -> None:
        """Register a canned response for a specific prompt substring."""
        self._mock_responses[prompt_substring] = response_text

    def inject_failure(self, count: int = 1, message: str = "Simulated provider failure") -> None:
        """Force the next N requests to fail for circuit breaker & fallback testing."""
        self.fail_next_n_requests = count
        self.fail_error_message = message

    async def complete(self, request: CompletionRequest, model_spec: ModelSpec) -> CompletionResponse:
        start_time = time.time()

        if self.simulate_latency_ms > 0:
            await asyncio.sleep(self.simulate_latency_ms / 1000.0)

        if self.fail_next_n_requests > 0:
            self.fail_next_n_requests -= 1
            err_msg = self.fail_error_message
            self.record_failure(err_msg)
            raise RuntimeError(f"MockProvider error: {err_msg}")

        # Extract last user message
        last_user_msg = ""
        for m in reversed(request.messages):
            if m.role in (ChatRole.USER, "user") and m.content:
                last_user_msg = m.content
                break

        # Check canned responses
        content = None
        for pattern, canned in self._mock_responses.items():
            if pattern.lower() in last_user_msg.lower():
                content = canned
                break

        # Generate intelligent mock content based on prompt keywords
        if content is None:
            content = self._generate_synthetic_response(last_user_msg, request, model_spec)

        latency_ms = round((time.time() - start_time) * 1000.0, 2)
        prompt_tokens = self.estimate_tokens(request.messages)
        completion_tokens = max(10, len(content) // 4)
        cost_usd = model_spec.calculate_cost(prompt_tokens, completion_tokens)

        self.record_success(latency_ms)

        # Check for tool calling request
        tool_calls = None
        if request.tools and "calculator" in last_user_msg.lower():
            tool_calls = [
                ToolCall(
                    id=f"call_{uuid.uuid4().hex[:8]}",
                    type="function",
                    function=ToolCallFunction(
                        name="calculator",
                        arguments=json.dumps({"expression": "42 * 2"}),
                    ),
                )
            ]

        choice = Choice(
            index=0,
            message=ChatMessage(
                role=ChatRole.ASSISTANT,
                content=content if not tool_calls else None,
                tool_calls=tool_calls,
            ),
            finish_reason="tool_calls" if tool_calls else "stop",
        )

        return CompletionResponse(
            id=f"mock-{uuid.uuid4().hex[:10]}",
            model=model_spec.model_id,
            provider=self.provider_type,
            choices=[choice],
            usage=UsageInfo(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
                estimated_cost_usd=cost_usd,
            ),
            latency_ms=latency_ms,
        )

    async def stream(self, request: CompletionRequest, model_spec: ModelSpec) -> AsyncIterator[str]:
        response = await self.complete(request, model_spec)
        text = response.content or ""
        words = text.split(" ")
        for word in words:
            if self.simulate_latency_ms > 0:
                await asyncio.sleep(min(0.01, self.simulate_latency_ms / 1000.0 / len(words)))
            yield word + " "

    async def check_health(self) -> ProviderHealth:
        if self.simulate_latency_ms > 0:
            await asyncio.sleep(0.005)
        health = self.get_health()
        health.status = "healthy"
        health.models_available = ["mock-frontier", "mock-fast", "mock-code"]
        return health

    def _generate_synthetic_response(
        self, prompt: str, request: CompletionRequest, model_spec: ModelSpec
    ) -> str:
        prompt_lower = prompt.lower()

        # Invariant prover response
        if "invariant prover" in prompt_lower or "falsifying vector" in prompt_lower:
            return "INVARIANT_PROVEN: All boundary conditions, typings, and runtime invariants verified without defect."

        if "json" in prompt_lower or (request.response_format and request.response_format.get("type") == "json_object"):
            return json.dumps({
                "status": "success",
                "message": "Processed successfully by Octo Harness",
                "model": model_spec.model_id,
                "data": {"result": "sample structured output", "score": 0.98},
            }, indent=2)

        if "code" in prompt_lower or "python" in prompt_lower or "function" in prompt_lower:
            return (
                "```python\n"
                "def solve_task(data: list) -> dict:\n"
                "    \"\"\"Generated solution by Octo Harness Grok/Cowork router.\"\"\"\n"
                "    return {'processed': len(data), 'status': 'ok'}\n"
                "```"
            )

        if "reason" in prompt_lower or "step by step" in prompt_lower or "math" in prompt_lower:
            return (
                "**Step 1: Problem Decomposition**\n"
                "We analyze the input constraints and target invariants.\n\n"
                "**Step 2: Execution Logic**\n"
                "Evaluate intermediate nodes and confirm boundary conditions.\n\n"
                "**Step 3: Verification & Conclusion**\n"
                "The invariant holds across all evaluated test vectors."
            )

        return (
            f"Response synthesized by {model_spec.display_name} via Octo Harness Router. "
            f"Query processed: '{prompt[:60]}...'"
        )
