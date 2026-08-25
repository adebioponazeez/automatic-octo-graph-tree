"""
Octo Harness - High-performance Cowork & Grok / Multi-Model AI Router Engine.

Provides unified routing, multi-tier fallback cascades, circuit breaking,
cost optimization, guardrails, multi-agent Cowork DAG execution, and an
OpenAI-compatible proxy server.
"""

__version__ = "1.0.0"
__author__ = "adebioponazeez"

from octo_harness.config import Settings, get_settings
from octo_harness.models import (
    ChatMessage,
    ChatRole,
    CompletionRequest,
    CompletionResponse,
    ModelCapability,
    ProviderType,
    RouteDecision,
    RoutingStrategy,
)
from octo_harness.router.engine import RouterEngine

__all__ = [
    "__version__",
    "Settings",
    "get_settings",
    "ChatMessage",
    "ChatRole",
    "CompletionRequest",
    "CompletionResponse",
    "ModelCapability",
    "ProviderType",
    "RouteDecision",
    "RoutingStrategy",
    "RouterEngine",
]
