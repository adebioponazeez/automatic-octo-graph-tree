"""
Tests for TOON Encoding, Semantic Symbol Anchoring, and Token Compression Engine.
"""

import pytest
from starlette.testclient import TestClient
from octo_harness.config import Settings
from octo_harness.router.engine import RouterEngine
from octo_harness.router.token_compressor import (
    CompressionStats,
    SemanticPromptCompressor,
    TOONEncoder,
    TokenOptimizer,
)
from octo_harness.server.app import create_app


def test_toon_encoding_uniform_array():
    data = [
        {"id": 1, "name": "Azeez Jr.", "role": "admin"},
        {"id": 2, "name": "Junior", "role": "engineer"},
        {"id": 3, "name": "Ahmed", "role": "reviewer"},
    ]

    toon_result = TOONEncoder.encode(data)
    assert "[3]{id,name,role}:" in toon_result
    assert "1,Azeez Jr.,admin" in toon_result
    assert "2,Junior,engineer" in toon_result
    assert "3,Ahmed,reviewer" in toon_result

    # Character count of TOON must be significantly less than formatted JSON
    import json
    json_str = json.dumps(data, indent=2)
    assert len(toon_result) < len(json_str)


def test_semantic_prompt_compressor():
    verbose_prompt = (
        "PRIMARY OBJECTIVE AND GOAL:\nBuild an ultra-fast Redis cache gateway.\n\n"
        "CRITICAL SYSTEM INVARIANT (DO NOT VIOLATE):\nEnsure all connections are TLS encrypted.\n\n"
        "PERFORMANCE AND LATENCY REQUIREMENT:\nMust respond in <10ms.\n\n"
        "SECURITY AND SECRET SCANNING:\nDo not expose passwords in plaintext."
    )

    compressed = SemanticPromptCompressor.compress_prompt(verbose_prompt)
    assert "🎯 GOAL:" in compressed
    assert "🔒 INVARIANT:" in compressed
    assert "⚡ PERF:" in compressed
    assert "🛡️ SEC:" in compressed
    assert len(compressed) < len(verbose_prompt)


def test_token_optimizer_unified():
    optimizer = TokenOptimizer()
    prompt = "PRIMARY OBJECTIVE: Process user analytics.\nCRITICAL INVARIANT: Zero data loss."
    context = [
        {"user_id": 101, "event": "click", "timestamp": 1724600000},
        {"user_id": 102, "event": "view", "timestamp": 1724600001},
        {"user_id": 103, "event": "signup", "timestamp": 1724600002},
    ]

    opt_text, stats = optimizer.optimize_payload(prompt=prompt, structured_context=context)
    assert isinstance(stats, CompressionStats)
    assert stats.tokens_saved > 0
    assert stats.compression_ratio_percent > 20.0
    assert "🎯 GOAL:" in opt_text
    assert "[CONTEXT (TOON)]:" in opt_text


def test_compress_api_endpoints():
    settings = Settings(mock_mode=True, server_api_key=None)
    engine = RouterEngine(settings=settings)
    app = create_app(settings=settings, engine=engine)
    client = TestClient(app)

    # 1. /compress/toon
    payload_toon = {
        "data": [
            {"id": 1, "status": "active"},
            {"id": 2, "status": "inactive"},
        ]
    }
    res_toon = client.post("/compress/toon", json=payload_toon)
    assert res_toon.status_code == 200
    data_toon = res_toon.json()
    assert "toon_encoded" in data_toon
    assert data_toon["char_reduction_percent"] > 0

    # 2. /compress/prompt
    payload_prompt = {
        "prompt": "CRITICAL INVARIANT: Maintain database consistency at all times.",
        "context": [{"node": "primary", "healthy": True}],
    }
    res_prompt = client.post("/compress/prompt", json=payload_prompt)
    assert res_prompt.status_code == 200
    data_prompt = res_prompt.json()
    assert "optimized_text" in data_prompt
    assert "stats" in data_prompt
