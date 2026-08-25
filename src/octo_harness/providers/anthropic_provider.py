"""
Anthropic Claude Provider implementation for Octo Harness.
"""

from __future__ import annotations

import json
import time
from typing import Any, AsyncIterator, Dict, List, Optional
import httpx

from octo_harness.models import (
    ChatMessage,
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


class AnthropicProvider(BaseProvider):
    """
    Anthropic API provider for Claude 3.5 Sonnet, Claude 3.5 Haiku, etc.
    Converts between unified message schema and Anthropic Messages API.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.anthropic.com/v1",
        timeout_seconds: float = 30.0,
        http_client: Optional[httpx.AsyncClient] = None,
    ):
        super().__init__(
            name="Anthropic",
            provider_type=ProviderType.ANTHROPIC,
            api_key=api_key,
            base_url=base_url,
        )
        self.timeout_seconds = timeout_seconds
        self._custom_client = http_client

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
            "User-Agent": "OctoHarness-Anthropic/1.0",
        }
        if self.api_key:
            headers["x-api-key"] = self.api_key
        return headers

    async def complete(self, request: CompletionRequest, model_spec: ModelSpec) -> CompletionResponse:
        start_time = time.time()
        url = f"{self.base_url}/messages"

        # Separate system message from conversation messages
        system_prompt = ""
        conversation: List[Dict[str, Any]] = []

        for msg in request.messages:
            if msg.role in ("system", "SYSTEM"):
                system_prompt += (msg.content or "") + "\n"
            else:
                role = "user" if msg.role in ("user", "USER") else "assistant"
                conversation.append({
                    "role": role,
                    "content": msg.content or "",
                })

        if not conversation:
            conversation.append({"role": "user", "content": "Hello"})

        payload: Dict[str, Any] = {
            "model": model_spec.model_id,
            "messages": conversation,
            "max_tokens": request.max_tokens or 2048,
            "temperature": request.temperature,
        }
        if system_prompt.strip():
            payload["system"] = system_prompt.strip()

        try:
            client = self._custom_client or httpx.AsyncClient(timeout=self.timeout_seconds)
            try:
                resp = await client.post(url, headers=self._get_headers(), json=payload)
            finally:
                if not self._custom_client:
                    await client.aclose()

            latency_ms = round((time.time() - start_time) * 1000.0, 2)

            if resp.status_code != 200:
                err_text = f"Anthropic API error {resp.status_code}: {resp.text}"
                self.record_failure(err_text)
                raise RuntimeError(err_text)

            data = resp.json()
            content_blocks = data.get("content", [])
            full_text = "".join(b.get("text", "") for b in content_blocks if b.get("type") == "text")

            usage_data = data.get("usage", {})
            prompt_tokens = usage_data.get("input_tokens", self.estimate_tokens(request.messages))
            completion_tokens = usage_data.get("output_tokens", 0)
            cost_usd = model_spec.calculate_cost(prompt_tokens, completion_tokens)

            self.record_success(latency_ms)

            choice = Choice(
                index=0,
                message=ChatMessage(role="assistant", content=full_text),
                finish_reason=data.get("stop_reason", "stop"),
            )

            return CompletionResponse(
                id=data.get("id", f"msg-{int(time.time())}"),
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

        except Exception as exc:
            self.record_failure(str(exc))
            raise

    async def stream(self, request: CompletionRequest, model_spec: ModelSpec) -> AsyncIterator[str]:
        response = await self.complete(request, model_spec)
        for chunk in (response.content or "").split(" "):
            yield chunk + " "

    async def check_health(self) -> ProviderHealth:
        health = self.get_health()
        if not self.api_key:
            health.status = "unconfigured"
            return health
        health.models_available = ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022"]
        health.status = "healthy"
        return health
