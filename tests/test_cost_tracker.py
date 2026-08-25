"""
Tests for CostTracker and budget enforcement.
"""

from octo_harness.models import ModelSpec, ProviderType
from octo_harness.router.cost_tracker import CostTracker


def test_cost_tracker_record_usage():
    tracker = CostTracker(budget_limit_usd=1.0)
    spec = ModelSpec(
        model_id="grok-3",
        provider_type=ProviderType.GROK,
        display_name="Grok 3",
        input_cost_per_million=3.00,
        output_cost_per_million=15.00,
    )

    cost1 = tracker.record_usage(spec, prompt_tokens=1000, completion_tokens=1000)
    # (1000/1M * 3) + (1000/1M * 15) = 0.003 + 0.015 = 0.018
    assert cost1 == 0.018

    summary = tracker.get_summary()
    assert summary["total_cost_usd"] == 0.018
    assert summary["total_tokens"] == 2000
    assert summary["total_requests"] == 1
    assert "grok-3" in summary["models"]


def test_cost_tracker_budget_check():
    tracker = CostTracker(budget_limit_usd=0.05)
    spec = ModelSpec(
        model_id="test",
        provider_type=ProviderType.MOCK,
        display_name="Test",
        input_cost_per_million=1000.0,
        output_cost_per_million=1000.0,
    )
    assert tracker.check_budget_available() is True
    # Spend $0.04
    tracker.record_usage(spec, prompt_tokens=20, completion_tokens=20)
    assert tracker.check_budget_available() is True

    # Spend another $0.04 -> total $0.08 > $0.05
    tracker.record_usage(spec, prompt_tokens=20, completion_tokens=20)
    assert tracker.check_budget_available() is False
