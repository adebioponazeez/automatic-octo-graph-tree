"""
Configuration settings for Octo Harness.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from octo_harness.models import ModelCapability, ModelSpec, ProviderType, RoutingStrategy


class ProviderConfig(BaseModel):
    api_key: Optional[str] = None
    base_url: str
    timeout_seconds: float = 30.0
    max_retries: int = 3
    enabled: bool = True
    rate_limit_rps: float = 20.0
    concurrency_limit: int = 10


class Settings(BaseModel):
    # App Information
    app_name: str = "Octo Harness - Cowork & Grok AI Router"
    version: str = "1.0.0"
    debug: bool = False
    mock_mode: bool = False

    # Server Settings
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    server_api_key: Optional[str] = None
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])

    # Routing Defaults
    default_strategy: RoutingStrategy = RoutingStrategy.GROK_PRIMARY
    default_grok_model: str = "grok-2-latest"
    default_openai_model: str = "gpt-4o"
    default_anthropic_model: str = "claude-3-5-sonnet-20241022"
    default_local_model: str = "qwen2.5:7b"

    # Circuit Breaker & Safety
    circuit_breaker_failure_threshold: int = 5
    circuit_breaker_recovery_timeout_s: float = 30.0
    budget_limit_usd: float = 50.0
    enforce_safety_guardrails: bool = True

    # Provider Configs
    grok: ProviderConfig = Field(
        default_factory=lambda: ProviderConfig(
            api_key=os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY"),
            base_url=os.getenv("GROK_BASE_URL", "https://api.x.ai/v1"),
            timeout_seconds=float(os.getenv("GROK_TIMEOUT", "30.0")),
            rate_limit_rps=float(os.getenv("GROK_RPS", "30.0")),
        )
    )

    openai: ProviderConfig = Field(
        default_factory=lambda: ProviderConfig(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            timeout_seconds=float(os.getenv("OPENAI_TIMEOUT", "30.0")),
            rate_limit_rps=float(os.getenv("OPENAI_RPS", "30.0")),
        )
    )

    anthropic: ProviderConfig = Field(
        default_factory=lambda: ProviderConfig(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            base_url=os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1"),
            timeout_seconds=float(os.getenv("ANTHROPIC_TIMEOUT", "30.0")),
            rate_limit_rps=float(os.getenv("ANTHROPIC_RPS", "20.0")),
        )
    )

    openrouter: ProviderConfig = Field(
        default_factory=lambda: ProviderConfig(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            timeout_seconds=float(os.getenv("OPENROUTER_TIMEOUT", "45.0")),
            rate_limit_rps=float(os.getenv("OPENROUTER_RPS", "30.0")),
        )
    )

    local: ProviderConfig = Field(
        default_factory=lambda: ProviderConfig(
            api_key=os.getenv("LOCAL_API_KEY", "local"),
            base_url=os.getenv("LOCAL_BASE_URL") or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            timeout_seconds=float(os.getenv("LOCAL_TIMEOUT", "60.0")),
            rate_limit_rps=float(os.getenv("LOCAL_RPS", "50.0")),
        )
    )

    # Standard Catalog of Supported Models
    model_catalog: Dict[str, ModelSpec] = Field(
        default_factory=lambda: {
            # xAI Grok Models
            "grok-3": ModelSpec(
                model_id="grok-3",
                provider_type=ProviderType.GROK,
                display_name="xAI Grok 3 Flagship",
                capabilities=[
                    ModelCapability.REASONING,
                    ModelCapability.CODE,
                    ModelCapability.MATH,
                    ModelCapability.LONG_CONTEXT,
                    ModelCapability.CREATIVE,
                ],
                context_window=131072,
                input_cost_per_million=3.00,
                output_cost_per_million=15.00,
                average_latency_ms=650.0,
                description="xAI's frontier reasoning and coding model",
            ),
            "grok-2-latest": ModelSpec(
                model_id="grok-2-latest",
                provider_type=ProviderType.GROK,
                display_name="xAI Grok 2",
                capabilities=[
                    ModelCapability.FAST_CHAT,
                    ModelCapability.CODE,
                    ModelCapability.REASONING,
                    ModelCapability.STRUCTURED_JSON,
                ],
                context_window=131072,
                input_cost_per_million=2.00,
                output_cost_per_million=10.00,
                average_latency_ms=450.0,
                description="xAI's fast general-purpose frontier model",
            ),
            "grok-2-vision-1212": ModelSpec(
                model_id="grok-2-vision-1212",
                provider_type=ProviderType.GROK,
                display_name="xAI Grok 2 Vision",
                capabilities=[
                    ModelCapability.MULTIMODAL,
                    ModelCapability.FAST_CHAT,
                    ModelCapability.EXTRACTION,
                ],
                context_window=32768,
                input_cost_per_million=2.00,
                output_cost_per_million=10.00,
                average_latency_ms=750.0,
                description="xAI multimodal vision understanding model",
            ),
            "grok-beta": ModelSpec(
                model_id="grok-beta",
                provider_type=ProviderType.GROK,
                display_name="xAI Grok Beta",
                capabilities=[
                    ModelCapability.FAST_CHAT,
                    ModelCapability.CREATIVE,
                ],
                context_window=131072,
                input_cost_per_million=5.00,
                output_cost_per_million=15.00,
                average_latency_ms=500.0,
                description="xAI Grok beta preview",
            ),
            # OpenAI Models
            "gpt-4o": ModelSpec(
                model_id="gpt-4o",
                provider_type=ProviderType.OPENAI,
                display_name="OpenAI GPT-4o",
                capabilities=[
                    ModelCapability.REASONING,
                    ModelCapability.CODE,
                    ModelCapability.MULTIMODAL,
                    ModelCapability.STRUCTURED_JSON,
                    ModelCapability.EXTRACTION,
                ],
                context_window=128000,
                input_cost_per_million=2.50,
                output_cost_per_million=10.00,
                average_latency_ms=520.0,
                description="OpenAI flagship omni-model",
            ),
            "gpt-4o-mini": ModelSpec(
                model_id="gpt-4o-mini",
                provider_type=ProviderType.OPENAI,
                display_name="OpenAI GPT-4o Mini",
                capabilities=[
                    ModelCapability.FAST_CHAT,
                    ModelCapability.EXTRACTION,
                    ModelCapability.STRUCTURED_JSON,
                ],
                context_window=128000,
                input_cost_per_million=0.15,
                output_cost_per_million=0.60,
                average_latency_ms=250.0,
                description="High-speed, cost-effective OpenAI model",
            ),
            "o3-mini": ModelSpec(
                model_id="o3-mini",
                provider_type=ProviderType.OPENAI,
                display_name="OpenAI o3-mini",
                capabilities=[
                    ModelCapability.REASONING,
                    ModelCapability.CODE,
                    ModelCapability.MATH,
                ],
                context_window=200000,
                input_cost_per_million=1.10,
                output_cost_per_million=4.40,
                average_latency_ms=950.0,
                description="Deep reasoning model optimized for STEM and code",
            ),
            # Anthropic Claude Models
            "claude-3-5-sonnet-20241022": ModelSpec(
                model_id="claude-3-5-sonnet-20241022",
                provider_type=ProviderType.ANTHROPIC,
                display_name="Claude 3.5 Sonnet",
                capabilities=[
                    ModelCapability.CODE,
                    ModelCapability.REASONING,
                    ModelCapability.MULTIMODAL,
                    ModelCapability.CREATIVE,
                    ModelCapability.LONG_CONTEXT,
                ],
                context_window=200000,
                input_cost_per_million=3.00,
                output_cost_per_million=15.00,
                average_latency_ms=620.0,
                description="Anthropic frontier coding and reasoning model",
            ),
            "claude-3-5-haiku-20241022": ModelSpec(
                model_id="claude-3-5-haiku-20241022",
                provider_type=ProviderType.ANTHROPIC,
                display_name="Claude 3.5 Haiku",
                capabilities=[
                    ModelCapability.FAST_CHAT,
                    ModelCapability.EXTRACTION,
                    ModelCapability.STRUCTURED_JSON,
                ],
                context_window=200000,
                input_cost_per_million=0.80,
                output_cost_per_million=4.00,
                average_latency_ms=280.0,
                description="Anthropic ultra-fast lightweight model",
            ),
            # OpenRouter Frontier & Open-Weight Models
            "moonshotai/kimi-k3": ModelSpec(
                model_id="moonshotai/kimi-k3",
                provider_type=ProviderType.OPENROUTER,
                display_name="Moonshot Kimi K3 (200k Context)",
                capabilities=[
                    ModelCapability.LONG_CONTEXT,
                    ModelCapability.REASONING,
                    ModelCapability.EXTRACTION,
                    ModelCapability.CODE,
                ],
                context_window=200000,
                input_cost_per_million=0.50,
                output_cost_per_million=2.00,
                average_latency_ms=700.0,
                description="Moonshot AI Kimi K3 long-context reasoning model",
            ),
            "deepseek/deepseek-r1": ModelSpec(
                model_id="deepseek/deepseek-r1",
                provider_type=ProviderType.OPENROUTER,
                display_name="DeepSeek R1 Frontier Reasoning",
                capabilities=[
                    ModelCapability.REASONING,
                    ModelCapability.MATH,
                    ModelCapability.CODE,
                ],
                context_window=128000,
                input_cost_per_million=0.55,
                output_cost_per_million=2.19,
                average_latency_ms=850.0,
                description="DeepSeek R1 frontier open reasoning model",
            ),
            "deepseek/deepseek-chat": ModelSpec(
                model_id="deepseek/deepseek-chat",
                provider_type=ProviderType.OPENROUTER,
                display_name="DeepSeek V3",
                capabilities=[
                    ModelCapability.FAST_CHAT,
                    ModelCapability.CODE,
                    ModelCapability.STRUCTURED_JSON,
                ],
                context_window=128000,
                input_cost_per_million=0.14,
                output_cost_per_million=0.28,
                average_latency_ms=380.0,
                description="DeepSeek V3 ultra-economical general model",
            ),
            "qwen/qwen-2.5-coder-32b-instruct": ModelSpec(
                model_id="qwen/qwen-2.5-coder-32b-instruct",
                provider_type=ProviderType.OPENROUTER,
                display_name="Qwen 2.5 Coder 32B Instruct",
                capabilities=[
                    ModelCapability.CODE,
                    ModelCapability.FAST_CHAT,
                    ModelCapability.STRUCTURED_JSON,
                ],
                context_window=131072,
                input_cost_per_million=0.18,
                output_cost_per_million=0.18,
                average_latency_ms=420.0,
                description="State of the art open code generation model",
            ),
            "meta-llama/llama-3.3-70b-instruct": ModelSpec(
                model_id="meta-llama/llama-3.3-70b-instruct",
                provider_type=ProviderType.OPENROUTER,
                display_name="Meta Llama 3.3 70B Instruct",
                capabilities=[
                    ModelCapability.FAST_CHAT,
                    ModelCapability.REASONING,
                    ModelCapability.CREATIVE,
                ],
                context_window=131072,
                input_cost_per_million=0.40,
                output_cost_per_million=0.40,
                average_latency_ms=480.0,
                description="Meta's top open-weight intelligence model",
            ),
            # Local / Open Models
            "qwen2.5-coder:7b": ModelSpec(
                model_id="qwen2.5-coder:7b",
                provider_type=ProviderType.LOCAL,
                display_name="Qwen 2.5 Coder 7B (Local)",
                capabilities=[
                    ModelCapability.CODE,
                    ModelCapability.FAST_CHAT,
                ],
                context_window=32768,
                input_cost_per_million=0.0,
                output_cost_per_million=0.0,
                average_latency_ms=300.0,
                description="Local high performance code generation model",
            ),
            "mock-frontier": ModelSpec(
                model_id="mock-frontier",
                provider_type=ProviderType.MOCK,
                display_name="Deterministic Mock Frontier",
                capabilities=[
                    ModelCapability.CODE,
                    ModelCapability.REASONING,
                    ModelCapability.FAST_CHAT,
                    ModelCapability.MULTIMODAL,
                    ModelCapability.STRUCTURED_JSON,
                    ModelCapability.LONG_CONTEXT,
                    ModelCapability.CREATIVE,
                    ModelCapability.MATH,
                    ModelCapability.EXTRACTION,
                ],
                context_window=128000,
                input_cost_per_million=0.0,
                output_cost_per_million=0.0,
                average_latency_ms=50.0,
                description="Zero-cost deterministic mock provider for testing and CI",
            ),
        }
    )


@lru_cache()
def get_settings() -> Settings:
    """Return cached Settings instance loaded from environment."""
    return Settings(
        debug=os.getenv("DEBUG", "false").lower() in ("true", "1", "yes"),
        mock_mode=os.getenv("OCTO_MOCK_MODE", "false").lower() in ("true", "1", "yes"),
        server_host=os.getenv("SERVER_HOST", "0.0.0.0"),
        server_port=int(os.getenv("SERVER_PORT", "8000")),
        server_api_key=os.getenv("SERVER_API_KEY"),
        budget_limit_usd=float(os.getenv("BUDGET_LIMIT_USD", "50.0")),
    )
