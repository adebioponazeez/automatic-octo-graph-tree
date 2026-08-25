"""
Integration tests for FastAPI application server with simulated client calls.
"""

import pytest
from starlette.testclient import TestClient
from octo_harness.config import Settings
from octo_harness.router.engine import RouterEngine
from octo_harness.server.app import create_app


@pytest.fixture
def test_app():
    settings = Settings(mock_mode=True, server_api_key="test-secret-token")
    engine = RouterEngine(settings=settings)
    app = create_app(settings=settings, engine=engine)
    return app


def test_auth_protected_endpoints(test_app):
    client = TestClient(test_app)

    # Public endpoints work without auth
    r_health = client.get("/health")
    assert r_health.status_code == 200

    r_ready = client.get("/ready")
    assert r_ready.status_code == 200

    r_pulse = client.get("/pulse")
    assert r_pulse.status_code == 200

    # Protected endpoint without auth -> 401
    r_unauth = client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "Hi"}]},
    )
    assert r_unauth.status_code == 401

    # Protected endpoint with valid Bearer token -> 200
    r_auth = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer test-secret-token"},
        json={"messages": [{"role": "user", "content": "Hi authenticated"}]},
    )
    assert r_auth.status_code == 200
    assert r_auth.json()["choices"][0]["message"]["content"] != ""


def test_streaming_chat_completions(test_app):
    client = TestClient(test_app)
    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer test-secret-token"},
        json={
            "messages": [{"role": "user", "content": "Write a short stream test"}],
            "stream": True,
        },
    )
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    lines = [line for line in response.iter_lines() if line]
    assert any("data: " in l for l in lines)
    assert any("[DONE]" in l for l in lines)
