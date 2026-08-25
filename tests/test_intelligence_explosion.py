"""
Tests for Recursive Intelligence Explosion & Super-Fusion Engine.
"""

import pytest
from starlette.testclient import TestClient
from octo_harness.cli.main import main
from octo_harness.config import Settings
from octo_harness.cowork.intelligence_explosion import (
    IntelligenceExplosionEngine,
    IntelligenceExplosionResult,
)
from octo_harness.router.engine import RouterEngine
from octo_harness.server.app import create_app


@pytest.mark.asyncio
async def test_intelligence_explosion_execution():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)
    explosion_engine = IntelligenceExplosionEngine(router=engine)

    result = await explosion_engine.explode_intelligence(
        objective="Design zero-knowledge state machine with verifiable computation",
        target_epochs=2,
        artifact_type="code",
    )

    assert isinstance(result, IntelligenceExplosionResult)
    assert result.epochs_executed == 2
    assert result.capability_multiplier >= 1.0
    assert result.final_quality_score > result.initial_quality_score
    assert len(result.proof_hash) == 64
    assert len(result.trajectory_history) == 6  # 3 trajectories * 2 epochs
    assert len(result.meta_invariants_learned) > 0


def test_intelligence_explosion_api_endpoint():
    settings = Settings(mock_mode=True, server_api_key=None)
    engine = RouterEngine(settings=settings)
    app = create_app(settings=settings, engine=engine)
    client = TestClient(app)

    payload = {
        "objective": "Build self-healing distributed consensus protocol",
        "target_epochs": 2,
        "artifact_type": "code",
    }

    res = client.post("/cowork/explode", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "super_artifact" in data
    assert "capability_multiplier" in data
    assert "proof_hash" in data
    assert "explosion_certificate" in data


def test_intelligence_explosion_cli_command():
    ret = main(["--mock", "explode", "Design autonomous memory indexing pipeline", "--epochs", "1"])
    assert ret == 0

    ret_json = main(["--mock", "explode", "Design autonomous memory indexing pipeline", "--epochs", "1", "--json"])
    assert ret_json == 0
