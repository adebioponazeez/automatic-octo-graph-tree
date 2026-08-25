"""
Tests for Sovereign OS Kit v1.0 specifications, Roster Engine, Context Cache, and Batch Processor.
"""

import importlib.util
from pathlib import Path
import pytest

spec = importlib.util.spec_from_file_location(
    "roster_engine", Path(__file__).parent.parent / "08_roster_engine.py"
)
roster_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(roster_mod)
generate_bundles = roster_mod.generate_bundles
PLATFORM_MAPPINGS = roster_mod.PLATFORM_MAPPINGS

from octo_harness.config import Settings
from octo_harness.models import ChatMessage, ChatRole, CompletionRequest, RoutingStrategy
from octo_harness.router.batch_processor import BatchProcessor
from octo_harness.router.context_cache import ContextCacheEngine
from octo_harness.router.engine import RouterEngine


def test_sovereign_os_files_exist():
    root = Path(__file__).parent.parent
    expected_files = [
        "00-constitution.md",
        "01-operating-system.md",
        "02-agent-contract.md",
        "03-mission-graph.md",
        "04-orchestrator-prompt.md",
        "05-subagent-library.md",
        "06-platform-adapters.md",
        "07-tools-and-mcp.md",
        "08_roster_engine.py",
        "graph/projects.yaml",
        "graph/goals.yaml",
        "graph/agents.yaml",
        "graph/edges.yaml",
    ]
    for rel_path in expected_files:
        p = root / rel_path
        assert p.exists(), f"Missing required Sovereign OS file: {rel_path}"
        assert p.stat().st_size > 0, f"File is empty: {rel_path}"


def test_roster_engine_generates_all_bundles():
    generated = generate_bundles()
    assert len(generated) >= 5
    for p in generated:
        assert p.exists()
        content = p.read_text(encoding="utf-8")
        assert len(content) > 1000


def test_context_cache_engine_hit_and_savings():
    cache_engine = ContextCacheEngine(ttl_seconds=3600.0, default_discount=0.75)

    system_text = "You are the Chief of Staff operating under the Sovereign OS Constitution. " * 20
    messages = [
        ChatMessage(role=ChatRole.SYSTEM, content=system_text),
        ChatMessage(role=ChatRole.USER, content="Query 1"),
    ]

    # First access: cache miss (registers prefix)
    is_hit_1, tok_1, saved_1 = cache_engine.check_and_apply_cache(messages, input_cost_per_million=3.0)
    assert is_hit_1 is False
    assert tok_1 > 100
    assert saved_1 == 0.0

    # Second access: cache hit (75% savings applied)
    is_hit_2, tok_2, saved_2 = cache_engine.check_and_apply_cache(messages, input_cost_per_million=3.0)
    assert is_hit_2 is True
    assert tok_2 == tok_1
    assert saved_2 > 0.0

    stats = cache_engine.get_cache_stats()
    assert stats["total_cache_hits"] == 1
    assert stats["total_saved_usd"] == saved_2


@pytest.mark.asyncio
async def test_batch_processor_queue_and_flush():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)
    batch_proc = BatchProcessor(engine=engine)

    req1 = CompletionRequest(messages=[ChatMessage(role=ChatRole.USER, content="Batch Job 1")])
    req2 = CompletionRequest(messages=[ChatMessage(role=ChatRole.USER, content="Batch Job 2")])

    j1 = batch_proc.submit_job(req1, priority=100)
    j2 = batch_proc.submit_job(req2, priority=50)

    status = batch_proc.get_queue_status()
    assert status["queued_jobs_count"] == 2

    # Flush batch
    processed = await batch_proc.flush_batch(max_jobs=5)
    assert len(processed) == 2
    assert processed[0].id == j1.id  # higher priority processed first
    assert processed[0].status == "completed"
    assert processed[1].status == "completed"

    assert batch_proc._total_jobs_processed == 2
    assert batch_proc.get_queue_status()["queued_jobs_count"] == 0
