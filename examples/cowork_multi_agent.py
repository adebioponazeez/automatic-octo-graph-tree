"""
Cowork Multi-Agent DAG Pipeline Example.
"""

import asyncio
import json
from octo_harness import RouterEngine
from octo_harness.cowork.graph import CoworkGraph


async def main():
    engine = RouterEngine()

    objective = (
        "Design and implement an asynchronous WebSocket pub-sub broadcaster in Python "
        "with dead-letter queue and message deduplication."
    )

    print(f"[*] Starting Cowork Swarm DAG for objective:\n    {objective}\n")

    pipeline = CoworkGraph.create_standard_pipeline(router=engine, objective=objective)
    result = await pipeline.execute(objective)

    print("=" * 70)
    print(f" Pipeline Status:       {result['status'].upper()}")
    print(f" Total Duration:        {result['total_execution_time_s']}s")
    print(f" Tasks Finished:        {result['completed_tasks']}/{result['tasks_count']}")
    print("=" * 70)

    for task in result["tasks"]:
        print(f"\n[Node: {task['name']}] (Role: {task['assigned_role']})")
        print(f"Status: {task['status']} in {task['execution_time_s']}s")
        print(f"Output snippet:\n{task['result'][:150]}...\n")

    print("=" * 70)
    print(" FINAL SYNTHESIZED DELIVERABLE:")
    print("=" * 70)
    print(result["final_deliverable"])


if __name__ == "__main__":
    asyncio.run(main())
