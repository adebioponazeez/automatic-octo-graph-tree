"""
Tests for Circuit Breaker and CircuitBreakerRegistry.
"""

import time
from octo_harness.router.circuit_breaker import CircuitBreaker, CircuitBreakerRegistry, CircuitState


def test_circuit_breaker_initial_state():
    cb = CircuitBreaker(name="test", failure_threshold=3, recovery_timeout_s=0.5)
    assert cb.state == CircuitState.CLOSED
    assert cb.can_execute() is True


def test_circuit_breaker_trips_to_open():
    cb = CircuitBreaker(name="test", failure_threshold=3, recovery_timeout_s=0.5)
    cb.record_failure()
    assert cb.state == CircuitState.CLOSED
    cb.record_failure()
    assert cb.state == CircuitState.CLOSED
    cb.record_failure()
    assert cb.state == CircuitState.OPEN
    assert cb.can_execute() is False


def test_circuit_breaker_half_open_recovery():
    cb = CircuitBreaker(name="test", failure_threshold=2, recovery_timeout_s=0.05)
    cb.record_failure()
    cb.record_failure()
    assert cb.state == CircuitState.OPEN

    # Wait for recovery timeout
    time.sleep(0.06)
    assert cb.can_execute() is True
    assert cb.state == CircuitState.HALF_OPEN

    # On success, transitions back to CLOSED
    cb.record_success()
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0


def test_circuit_breaker_registry():
    registry = CircuitBreakerRegistry(default_threshold=2, default_timeout=1.0)
    cb1 = registry.get_breaker("grok:grok-3")
    cb2 = registry.get_breaker("openai:gpt-4o")

    assert cb1.name == "grok:grok-3"
    assert cb2.name == "openai:gpt-4o"
    states = registry.get_all_states()
    assert states["grok:grok-3"] == "CLOSED"
    assert states["openai:gpt-4o"] == "CLOSED"
