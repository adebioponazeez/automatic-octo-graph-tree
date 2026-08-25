"""
Tests for Deterministic Invariant Prover & Verification Engine.
"""

import pytest
from starlette.testclient import TestClient
from octo_harness.cli.main import main
from octo_harness.config import Settings
from octo_harness.cowork.invariant_verifier import (
    InvariantCheck,
    InvariantType,
    InvariantVerifierEngine,
    VerificationProof,
)
from octo_harness.router.engine import RouterEngine
from octo_harness.server.app import create_app


@pytest.mark.asyncio
async def test_invariant_prover_clean_code():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)
    verifier = InvariantVerifierEngine(router=engine)

    code = "def fibonacci(n: int) -> int:\n    if n <= 1: return n\n    return fibonacci(n-1) + fibonacci(n-2)"
    proof = await verifier.verify_and_prove(
        objective="Implement recursive fibonacci in Python",
        candidate_artifact=code,
        expected_output_type="code",
    )

    assert proof.passed_all_gates is True
    assert len(proof.proof_hash) == 64  # valid SHA-256
    assert len(proof.invariant_checks) >= 3


@pytest.mark.asyncio
async def test_invariant_prover_catches_syntax_error():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)
    verifier = InvariantVerifierEngine(router=engine)

    malformed_code = "def bad_fn(x, y:\n    return x +"
    proof = await verifier.verify_and_prove(
        objective="Implement addition",
        candidate_artifact=malformed_code,
        expected_output_type="code",
        max_remediation_rounds=1,
    )

    # Catches syntax error and logs defect
    assert len(proof.falsifying_vectors_identified) > 0
    assert any(c.invariant_type == InvariantType.SYNTAX_AND_AST for c in proof.invariant_checks)


@pytest.mark.asyncio
async def test_invariant_prover_json_schema():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)
    verifier = InvariantVerifierEngine(router=engine)

    json_payload = '{"status": "active", "nodes": [1, 2, 3]}'
    proof = await verifier.verify_and_prove(
        objective="Emit cluster status payload",
        candidate_artifact=json_payload,
        expected_output_type="json",
    )

    assert proof.passed_all_gates is True


def test_verify_api_endpoint():
    settings = Settings(mock_mode=True, server_api_key=None)
    engine = RouterEngine(settings=settings)
    app = create_app(settings=settings, engine=engine)
    client = TestClient(app)

    payload = {
        "objective": "Verify rate limiter state machine",
        "candidate_artifact": "def limit(): return True",
        "expected_output_type": "code",
    }
    res = client.post("/cowork/verify", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "proof_hash" in data
    assert "invariant_checks" in data


@pytest.mark.asyncio
async def test_invariant_prover_secret_leak():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)
    verifier = InvariantVerifierEngine(router=engine)

    leaky_code = "API_KEY = 'sk-proj-1234567890abcdef1234567890abcdef1234567890ab'\ndef run(): pass"
    proof = await verifier.verify_and_prove(
        objective="Implement credential store",
        candidate_artifact=leaky_code,
        expected_output_type="code",
        max_remediation_rounds=0,
    )

    assert proof.passed_all_gates is False
    assert any(c.invariant_type == InvariantType.SECURITY_INTEGRITY and not c.passed for c in proof.invariant_checks)


@pytest.mark.asyncio
async def test_invariant_prover_falsification_trigger():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)
    verifier = InvariantVerifierEngine(router=engine)

    # Trigger defect when mock returns falsification
    proof = await verifier.verify_and_prove(
        objective="Calculate balance",
        candidate_artifact="def calc(): return 0",
        expected_output_type="architectural_plan",
    )
    assert proof.proof_hash is not None


def test_verify_cli_command():
    ret = main(["--mock", "verify", "Calculate factorial", "def fact(n): return 1 if n <= 1 else n * fact(n-1)"])
    assert ret == 0

    ret_json = main(["--mock", "verify", "Calculate factorial", "def fact(n): return 1", "--json"])
    assert ret_json == 0
