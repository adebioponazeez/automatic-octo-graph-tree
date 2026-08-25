"""
Tests for Cowork Multi-Agent Framework, DAG execution, and consensus.
"""

import pytest
from octo_harness.config import Settings
from octo_harness.cowork.consensus import ModelDebateConsensus
from octo_harness.cowork.graph import CoworkGraph, CyclicDependencyError
from octo_harness.cowork.memory import CoworkMemory
from octo_harness.models import CoworkTask, CoworkTaskStatus
from octo_harness.router.engine import RouterEngine


def test_cowork_memory():
    mem = CoworkMemory(session_id="test-session")
    mem.set("test_key", {"status": "ok"}, author_agent="planner")
    assert mem.contains("test_key") is True
    assert mem.get("test_key") == {"status": "ok"}
    snap = mem.snapshot()
    assert snap["entries_count"] == 1


def test_cowork_graph_cycle_detection():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)
    graph = CoworkGraph(router=engine)

    t1 = CoworkTask(id="task-1", name="Task 1", description="desc", assigned_role="planner", dependencies=["task-2"])
    t2 = CoworkTask(id="task-2", name="Task 2", description="desc", assigned_role="coder", dependencies=["task-1"])
    graph.add_task(t1)
    graph.add_task(t2)

    with pytest.raises(CyclicDependencyError):
        graph._validate_dag()


@pytest.mark.asyncio
async def test_cowork_pipeline_execution():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)

    pipeline = CoworkGraph.create_standard_pipeline(
        router=engine, objective="Build a rate-limited cache gateway in Python"
    )

    result = await pipeline.execute("Build a rate-limited cache gateway in Python")
    assert result["status"] == "completed"
    assert result["completed_tasks"] == 4
    assert result["final_deliverable"] != ""
    assert len(result["tasks"]) == 4


@pytest.mark.asyncio
async def test_multi_model_consensus():
    settings = Settings(mock_mode=True)
    engine = RouterEngine(settings=settings)
    debate = ModelDebateConsensus(router=engine)

    res = await debate.run_consensus(
        prompt="Explain the advantages of event-driven architecture",
        target_models=["mock-frontier"],
        judge_model="mock-frontier",
    )
    assert res.agreement_score > 0.8
    assert res.consensus_summary != ""
    assert len(res.opinions) >= 1
