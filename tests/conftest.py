"""
Pytest configuration and test fixtures for Octo Harness.
"""

import pytest
from octo_harness.config import Settings
from octo_harness.models import ChatMessage, ChatRole, CompletionRequest, RoutingStrategy
from octo_harness.providers.mock_provider import MockProvider
from octo_harness.router.engine import RouterEngine


@pytest.fixture
def mock_settings() -> Settings:
    """Fixture providing a mock-first Settings instance."""
    return Settings(
        app_name="Octo Harness Test",
        mock_mode=True,
        budget_limit_usd=10.0,
    )


@pytest.fixture
def router_engine(mock_settings: Settings) -> RouterEngine:
    """Fixture providing an initialized RouterEngine."""
    engine = RouterEngine(settings=mock_settings)
    # Ensure MockProvider is active for all provider slots
    mock = MockProvider(name="TestMockProvider", simulate_latency_ms=1.0)
    for ptype in engine.providers:
        engine.register_provider(ptype, mock)
    return engine


@pytest.fixture
def sample_chat_request() -> CompletionRequest:
    """Fixture providing a basic chat CompletionRequest."""
    return CompletionRequest(
        messages=[
            ChatMessage(role=ChatRole.SYSTEM, content="You are a helpful assistant."),
            ChatMessage(role=ChatRole.USER, content="Explain quantum entanglement briefly."),
        ],
        strategy=RoutingStrategy.GROK_PRIMARY,
    )


@pytest.fixture
def sample_code_request() -> CompletionRequest:
    """Fixture providing a code generation CompletionRequest."""
    return CompletionRequest(
        messages=[
            ChatMessage(
                role=ChatRole.USER,
                content="Write a Python function to compute fibonacci numbers with memoization: def fib(n):",
            )
        ],
        strategy=RoutingStrategy.QUALITY_FIRST,
    )
