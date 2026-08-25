"""
Circuit breaker implementation for resilient model provider fault tolerance.
"""

from __future__ import annotations

import time
from enum import Enum
from typing import Dict, Optional


class CircuitState(str, Enum):
    CLOSED = "CLOSED"      # Normal healthy state
    OPEN = "OPEN"          # Tripped, rejecting calls
    HALF_OPEN = "HALF_OPEN"  # Testing recovery


class CircuitBreaker:
    """
    Protects downstream systems and fallback cascades by failing fast when
    an LLM provider experiences consecutive failures or outages.
    """

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_s: float = 30.0,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout_s = recovery_timeout_s
        self.state: CircuitState = CircuitState.CLOSED
        self.failure_count: int = 0
        self.success_count: int = 0
        self.last_state_change: float = time.time()
        self.last_failure_time: float = 0.0

    def can_execute(self) -> bool:
        """Check if execution is permitted under current circuit state."""
        now = time.time()
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            if now - self.last_state_change >= self.recovery_timeout_s:
                # Transition to HALF_OPEN to probe provider
                self.state = CircuitState.HALF_OPEN
                self.last_state_change = now
                return True
            return False

        if self.state == CircuitState.HALF_OPEN:
            # Allow limited probe requests
            return True

        return False

    def record_success(self) -> None:
        """Record a successful provider interaction."""
        now = time.time()
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            self.last_state_change = now
        elif self.state == CircuitState.CLOSED:
            self.failure_count = max(0, self.failure_count - 1)
        self.success_count += 1

    def record_failure(self) -> None:
        """Record a failed provider interaction."""
        now = time.time()
        self.failure_count += 1
        self.last_failure_time = now

        if self.state == CircuitState.CLOSED:
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                self.last_state_change = now
        elif self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.last_state_change = now

    def reset(self) -> None:
        """Manually reset circuit breaker to healthy CLOSED state."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_state_change = time.time()


class CircuitBreakerRegistry:
    """Registry maintaining circuit breakers for all registered providers and models."""

    def __init__(self, default_threshold: int = 5, default_timeout: float = 30.0):
        self.default_threshold = default_threshold
        self.default_timeout = default_timeout
        self._breakers: Dict[str, CircuitBreaker] = {}

    def get_breaker(self, key: str) -> CircuitBreaker:
        """Retrieve or create a circuit breaker for the specified key."""
        if key not in self._breakers:
            self._breakers[key] = CircuitBreaker(
                name=key,
                failure_threshold=self.default_threshold,
                recovery_timeout_s=self.default_timeout,
            )
        return self._breakers[key]

    def get_all_states(self) -> Dict[str, str]:
        """Return states of all registered circuit breakers."""
        return {k: v.state.value for k, v in self._breakers.items()}
