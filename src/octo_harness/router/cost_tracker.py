"""
Dynamic Token Cost Tracking and Budget Enforcement for Octo Harness.
"""

from __future__ import annotations

import time
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from octo_harness.models import ModelSpec


class ModelUsageRecord(BaseModel):
    model_id: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    request_count: int = 0


class BudgetExceededError(RuntimeError):
    """Raised when a request exceeds the allocated budget limit."""
    pass


class CostTracker:
    """
    Tracks token usage and estimated USD costs per model and session.
    Enforces maximum budget limits.
    """

    def __init__(self, budget_limit_usd: float = 100.0):
        self.budget_limit_usd = budget_limit_usd
        self._usage_by_model: Dict[str, ModelUsageRecord] = {}
        self._total_cost_usd: float = 0.0
        self._total_prompt_tokens: int = 0
        self._total_completion_tokens: int = 0
        self._total_requests: int = 0
        self._created_at: float = time.time()

    def record_usage(self, model_spec: ModelSpec, prompt_tokens: int, completion_tokens: int) -> float:
        """Record usage and return the incremental USD cost."""
        cost = model_spec.calculate_cost(prompt_tokens, completion_tokens)
        model_id = model_spec.model_id

        if model_id not in self._usage_by_model:
            self._usage_by_model[model_id] = ModelUsageRecord(model_id=model_id)

        rec = self._usage_by_model[model_id]
        rec.prompt_tokens += prompt_tokens
        rec.completion_tokens += completion_tokens
        rec.total_tokens += (prompt_tokens + completion_tokens)
        rec.total_cost_usd += cost
        rec.request_count += 1

        self._total_cost_usd += cost
        self._total_prompt_tokens += prompt_tokens
        self._total_completion_tokens += completion_tokens
        self._total_requests += 1

        return cost

    def check_budget_available(self, estimated_additional_cost: float = 0.0) -> bool:
        """Check if executing the next request is within budget."""
        return (self._total_cost_usd + estimated_additional_cost) <= self.budget_limit_usd

    def get_summary(self) -> Dict[str, Any]:
        """Return full usage and cost analytics."""
        return {
            "budget_limit_usd": self.budget_limit_usd,
            "total_cost_usd": round(self._total_cost_usd, 6),
            "remaining_budget_usd": round(max(0.0, self.budget_limit_usd - self._total_cost_usd), 6),
            "budget_utilized_percent": round((self._total_cost_usd / max(0.01, self.budget_limit_usd)) * 100.0, 2),
            "total_requests": self._total_requests,
            "total_prompt_tokens": self._total_prompt_tokens,
            "total_completion_tokens": self._total_completion_tokens,
            "total_tokens": self._total_prompt_tokens + self._total_completion_tokens,
            "models": {k: v.model_dump() for k, v in self._usage_by_model.items()},
        }

    def reset(self) -> None:
        """Reset all tracked usage counters."""
        self._usage_by_model.clear()
        self._total_cost_usd = 0.0
        self._total_prompt_tokens = 0
        self._total_completion_tokens = 0
        self._total_requests = 0
        self._created_at = time.time()
