"""
Tests for FastAPI server endpoints and OpenAI-compatible proxy.
"""

import pytest
from starlette.testclient import TestClient
from octo_harness.config import Settings
from octo_harness.router.engine import RouterEngine
from octo_harness.server.app import create_app


@pytest.fixture
def client():
    settings = Settings(mock_mode=True, server_api_key=None)
    engine = RouterEngine(settings=settings)
    app = create_app(settings=settings, engine=engine)
    return TestClient(app)


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_ready_endpoint(client):
    resp = client.get("/ready")
    assert resp.status_code == 200
    assert resp.json()["ready"] is True


def test_pulse_endpoint(client):
    resp = client.get("/pulse")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert "providers" in data


def test_list_models_endpoint(client):
    resp = client.get("/v1/models")
    assert resp.status_code == 200
    data = resp.json()
    assert data["object"] == "list"
    assert len(data["data"]) > 0


def test_route_inspect_endpoint(client):
    payload = {
        "messages": [{"role": "user", "content": "Write a python function"}],
        "strategy": "grok_primary",
    }
    resp = client.post("/v1/route", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "primary_model" in data
    assert "fallback_chain" in data


def test_chat_completions_proxy(client):
    payload = {
        "messages": [{"role": "user", "content": "Hello from OpenAI client"}],
        "model": "grok-2-latest",
        "temperature": 0.7,
    }
    resp = client.post("/v1/chat/completions", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "choices" in data
    assert len(data["choices"]) > 0
    assert data["choices"][0]["message"]["content"] != ""


def test_cowork_run_endpoint(client):
    payload = {"objective": "Automate database migration checks"}
    resp = client.post("/cowork/run", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "completed"
    assert len(data["tasks"]) == 4


def test_cowork_consensus_endpoint(client):
    payload = {"query": "Pros and cons of microservices vs monoliths"}
    resp = client.post("/cowork/consensus", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "consensus_summary" in data


def test_metrics_endpoint(client):
    resp = client.get("/metrics?format=json")
    assert resp.status_code == 200
    data = resp.json()
    assert "metrics" in data

    resp_prom = client.get("/metrics?format=prometheus")
    assert resp_prom.status_code == 200
    assert "octo_requests_total" in resp_prom.text
