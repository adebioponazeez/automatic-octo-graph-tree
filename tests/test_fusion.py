"""
Tests for Frontier Model Harness Fusion engine, API endpoint, and CLI.
"""

import pytest
from starlette.testclient import TestClient
from octo_harness.cli.main import main
from octo_harness.config import Settings
from octo_harness.cowork.fusion import FrontierHarnessFusion, FusionParameter
from octo_harness.router.engine import RouterEngine
from octo_harness.server.app import create_app


@pytest.mark.asyncio
async def test_frontier_fusion_execution():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)
    fusion = FrontierHarnessFusion(router=engine)

    result = await fusion.execute_fusion(
        objective="Architect a distributed, zero-loss message bus with idempotency keys",
        parameters=[
            FusionParameter.ALGORITHMIC_RIGOR,
            FusionParameter.CODE_ARCHITECTURE,
            FusionParameter.STRUCTURAL_SCHEMA,
        ],
    )

    assert result.composite_quality_score >= 0.95
    assert len(result.proposals) >= 1
    assert result.fused_deliverable != ""
    assert result.evidence_block["audit_passed"] is True
    assert "target_objective" in result.evidence_block


def test_fusion_api_endpoint():
    settings = Settings(mock_mode=True, server_api_key=None)
    engine = RouterEngine(settings=settings)
    app = create_app(settings=settings, engine=engine)
    client = TestClient(app)

    payload = {
        "objective": "Build high-throughput streaming proxy",
        "parameters": ["algorithmic_rigor", "code_architecture"],
    }
    res = client.post("/cowork/fusion", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "fused_deliverable" in data
    assert "evidence_block" in data
    assert data["composite_quality_score"] > 0.9


def test_fusion_cli_command():
    ret = main(["--mock", "fusion", "Build an async cache layer with Raft consensus"])
    assert ret == 0

    ret_json = main(["--mock", "fusion", "Build an async cache layer with Raft consensus", "--json"])
    assert ret_json == 0
