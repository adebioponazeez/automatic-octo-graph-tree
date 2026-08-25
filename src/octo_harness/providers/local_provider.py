"""
Local Provider implementation for Ollama, vLLM, and llama.cpp endpoints.
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
    UsageInfo,
)
from octo_harness.providers.base import BaseProvider


class LocalProvider(BaseProvider):
    """
    Local / self-hosted inference provider (Ollama, vLLM, llama.cpp, LocalAI).
    Default base URL: http://localhost:11434/v1
    """

    def __init__(
        self,
        api_key: Optional[str] = "local",
        base_url: str = "http://localhost:11434/v1",
        timeout_seconds: float = 60.0,
        http_client: Optional[httpx.AsyncClient] = None,
    ):
        super().__init__(
            name="Local-Engine",
            provider_type=ProviderType.LOCAL,
            api_key=api_key or "local",
            base_url=base_url,
        )
        self.timeout_seconds = timeout_seconds
        self._custom_client = http_client

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
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

        try:
            client = self._custom_client or httpx.AsyncClient(timeout=self.timeout_seconds)
            try:
                resp = await client.post(url, headers=self._get_headers(), json=payload)
            finally:
                if not self._custom_client:
                    await client.aclose()

            latency_ms = round((time.time() - start_time) * 1000.0, 2)

            if resp.status_code != 200:
                err_text = f"Local provider error {resp.status_code}: {resp.text}"
                self.record_failure(err_text)
                raise RuntimeError(err_text)

            data = resp.json()
            choices_data = data.get("choices", [])
            choices: List[Choice] = []

            for c in choices_data:
                msg_data = c.get("message", {})
                choices.append(
                    Choice(
                        index=c.get("index", 0),
                        message=ChatMessage(
                            role=msg_data.get("role", "assistant"),
                            content=msg_data.get("content", ""),
                        ),
                        finish_reason=c.get("finish_reason", "stop"),
                    )
                )

            usage_data = data.get("usage", {})
            prompt_tokens = usage_data.get("prompt_tokens", self.estimate_tokens(request.messages))
            completion_tokens = usage_data.get("completion_tokens", 0)

            self.record_success(latency_ms)

            return CompletionResponse(
                id=data.get("id", f"local-{int(time.time())}"),
                model=model_spec.model_id,
                provider=self.provider_type,
                choices=choices,
                usage=UsageInfo(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens,
                    estimated_cost_usd=0.0,
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
        try:
            client = self._custom_client or httpx.AsyncClient(timeout=3.0)
            try:
                resp = await client.get(f"{self.base_url}/models", headers=self._get_headers())
                if resp.status_code == 200:
                    health.status = "healthy"
                else:
                    health.status = "degraded"
            finally:
                if not self._custom_client:
                    await client.aclose()
        except Exception:
            health.status = "offline"
        return health
