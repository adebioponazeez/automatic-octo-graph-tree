"""
xAI Grok Provider implementation for Octo Harness.
"""

from __future__ import annotations

import json
import time
from typing import Any, AsyncIterator, Dict, List, Optional
import httpx

from octo_harness.models import (
    ChatMessage,
    ChatRole,
    Choice,
    CompletionRequest,
    CompletionResponse,
    ModelSpec,
    ProviderHealth,
    ProviderType,
    ToolCall,
    ToolCallFunction,
    UsageInfo,
)
from octo_harness.providers.base import BaseProvider


class GrokProvider(BaseProvider):
    """
    xAI Grok API provider. Connects to https://api.x.ai/v1 with Grok 2, Grok 3, and Grok Vision models.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.x.ai/v1",
        timeout_seconds: float = 30.0,
        http_client: Optional[httpx.AsyncClient] = None,
    ):
        super().__init__(
            name="xAI-Grok",
            provider_type=ProviderType.GROK,
            api_key=api_key,
            base_url=base_url,
        )
        self.timeout_seconds = timeout_seconds
        self._custom_client = http_client

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "OctoHarness-GrokRouter/1.0",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def complete(self, request: CompletionRequest, model_spec: ModelSpec) -> CompletionResponse:
        start_time = time.time()
        url = f"{self.base_url}/chat/completions"

        payload: Dict[str, Any] = {
            "model": model_spec.model_id,
            "messages": [m.to_provider_dict() for m in request.messages],
            "temperature": request.temperature,
            "stream": False,
        }
        if request.max_tokens:
            payload["max_tokens"] = request.max_tokens
        if request.tools:
            payload["tools"] = request.tools
        if request.response_format:
            payload["response_format"] = request.response_format

        try:
            client = self._custom_client or httpx.AsyncClient(timeout=self.timeout_seconds)
            try:
                resp = await client.post(url, headers=self._get_headers(), json=payload)
            finally:
                if not self._custom_client:
                    await client.aclose()

            latency_ms = round((time.time() - start_time) * 1000.0, 2)

            if resp.status_code != 200:
                err_text = f"xAI Grok API error {resp.status_code}: {resp.text}"
                self.record_failure(err_text)
                raise RuntimeError(err_text)

            data = resp.json()
            choices_data = data.get("choices", [])
            choices: List[Choice] = []

            for c in choices_data:
                msg_data = c.get("message", {})
                tool_calls = None
                if "tool_calls" in msg_data and msg_data["tool_calls"]:
                    tool_calls = [
                        ToolCall(
                            id=tc.get("id", "call_unknown"),
                            type=tc.get("type", "function"),
                            function=ToolCallFunction(
                                name=tc.get("function", {}).get("name", ""),
                                arguments=tc.get("function", {}).get("arguments", "{}"),
                            ),
                        )
                        for tc in msg_data["tool_calls"]
                    ]

                choices.append(
                    Choice(
                        index=c.get("index", 0),
                        message=ChatMessage(
                            role=msg_data.get("role", "assistant"),
                            content=msg_data.get("content", ""),
                            tool_calls=tool_calls,
                        ),
                        finish_reason=c.get("finish_reason", "stop"),
                    )
                )

            usage_data = data.get("usage", {})
            prompt_tokens = usage_data.get("prompt_tokens", self.estimate_tokens(request.messages))
            completion_tokens = usage_data.get("completion_tokens", 0)
            cost_usd = model_spec.calculate_cost(prompt_tokens, completion_tokens)

            self.record_success(latency_ms)

            return CompletionResponse(
                id=data.get("id", f"grok-{int(time.time())}"),
                model=model_spec.model_id,
                provider=self.provider_type,
                choices=choices,
                usage=UsageInfo(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens,
                    estimated_cost_usd=cost_usd,
                ),
                latency_ms=latency_ms,
            )

        except Exception as exc:
            self.record_failure(str(exc))
            raise

    async def stream(self, request: CompletionRequest, model_spec: ModelSpec) -> AsyncIterator[str]:
        url = f"{self.base_url}/chat/completions"
        payload: Dict[str, Any] = {
            "model": model_spec.model_id,
            "messages": [m.to_provider_dict() for m in request.messages],
            "temperature": request.temperature,
            "stream": True,
        }
        if request.max_tokens:
            payload["max_tokens"] = request.max_tokens

        client = self._custom_client or httpx.AsyncClient(timeout=self.timeout_seconds)
        try:
            async with client.stream("POST", url, headers=self._get_headers(), json=payload) as response:
                if response.status_code != 200:
                    raise RuntimeError(f"Grok stream error: {response.status_code}")
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            delta = chunk.get("choices", [{}])[0].get("delta", {})
                            content = delta.get("content")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue
        finally:
            if not self._custom_client:
                await client.aclose()

    async def check_health(self) -> ProviderHealth:
        health = self.get_health()
        if not self.api_key:
            health.status = "unconfigured"
            return health

        try:
            client = self._custom_client or httpx.AsyncClient(timeout=5.0)
            try:
                resp = await client.get(f"{self.base_url}/models", headers=self._get_headers())
                if resp.status_code == 200:
                    data = resp.json()
                    models = [m.get("id") for m in data.get("data", []) if "id" in m]
                    health.models_available = models
                    health.status = "healthy"
                else:
                    health.status = "degraded"
            finally:
                if not self._custom_client:
                    await client.aclose()
        except Exception:
            health.status = "down"
        return health
