"""
Tests for domain schemas and cost calculations.
"""

from octo_harness.models import (
    ChatMessage,
    ChatRole,
    CompletionRequest,
    ModelCapability,
    ModelSpec,
    ProviderType,
    RoutingStrategy,
    ToolCall,
    ToolCallFunction,
)


def test_chat_message_dict_conversion():
    msg = ChatMessage(
        role=ChatRole.USER,
        content="Hello world",
        name="tester",
        tool_calls=[
            ToolCall(
                id="call_1",
                function=ToolCallFunction(name="test_fn", arguments="{}"),
            )
        ],
    )
    d = msg.to_provider_dict()
    assert d["role"] == "user"
    assert d["content"] == "Hello world"
    assert d["name"] == "tester"
    assert len(d["tool_calls"]) == 1


def test_model_spec_cost_calculation():
    spec = ModelSpec(
        model_id="test-model",
        provider_type=ProviderType.GROK,
        display_name="Test Model",
        input_cost_per_million=2.00,
        output_cost_per_million=10.00,
    )
    # 1000 prompt tokens (0.002) + 500 completion tokens (0.005) = 0.007
    cost = spec.calculate_cost(prompt_tokens=1000, completion_tokens=500)
    assert cost == 0.007


def test_completion_request_defaults():
    req = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content="test")],
    )
    assert req.strategy == RoutingStrategy.GROK_PRIMARY
    assert req.allow_fallback is True
    assert req.temperature == 0.7
