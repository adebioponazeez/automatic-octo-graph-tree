"""
Multi-agent DAG Graph Execution Engine for Octo Harness Cowork workflows.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any, Dict, List, Optional, Set

from octo_harness.cowork.agents import (
    BaseCoworkAgent,
    CoderAgent,
    CriticAgent,
    PlannerAgent,
    SafetyAuditorAgent,
    SynthesizerAgent,
)
from octo_harness.cowork.memory import CoworkMemory
from octo_harness.models import CoworkTask, CoworkTaskStatus
from octo_harness.router.engine import RouterEngine


class CyclicDependencyError(ValueError):
    """Raised when task dependency graph contains a cycle."""
    pass


class CoworkGraph:
    """
    Direct Acyclic Graph (DAG) orchestrator executing multi-agent collaborative workflows
    with parallel execution branches, dependency tracking, and shared memory.
    """

    def __init__(self, router: RouterEngine, session_id: Optional[str] = None):
        self.router = router
        self.memory = CoworkMemory(session_id=session_id)
        self.tasks: Dict[str, CoworkTask] = {}
        self.agents: Dict[str, BaseCoworkAgent] = {
            "planner": PlannerAgent(router),
            "coder": CoderAgent(router),
            "critic": CriticAgent(router),
            "synthesizer": SynthesizerAgent(router),
            "auditor": SafetyAuditorAgent(router),
        }

    def register_agent(self, role: str, agent: BaseCoworkAgent) -> None:
        """Register custom agent for a given role."""
        self.agents[role] = agent

    def add_task(self, task: CoworkTask) -> None:
        """Add a task node to the execution graph."""
        self.tasks[task.id] = task

    def _validate_dag(self) -> None:
        """Check for cycles and missing dependency IDs."""
        for tid, task in self.tasks.items():
            for dep in task.dependencies:
                if dep not in self.tasks:
                    raise ValueError(f"Task '{tid}' has unknown dependency '{dep}'")

        # Cycle detection using DFS
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node_id: str) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)

            for dep_id in self.tasks[node_id].dependencies:
                if dep_id not in visited:
                    if dfs(dep_id):
                        return True
                elif dep_id in rec_stack:
                    return True

            rec_stack.remove(node_id)
            return False

        for node_id in self.tasks:
            if node_id not in visited:
                if dfs(node_id):
                    raise CyclicDependencyError(f"Cycle detected in task graph involving task '{node_id}'")

    async def execute(self, objective: str) -> Dict[str, Any]:
        """
        Executes all tasks in the DAG according to dependency ordering.
        Tasks with all dependencies fulfilled execute concurrently.
        """
        self._validate_dag()
        self.memory.set("workflow_objective", objective, author_agent="orchestrator")
        start_time = time.time()

        completed_task_ids: Set[str] = set()
        failed_task_ids: Set[str] = set()

        while len(completed_task_ids) + len(failed_task_ids) < len(self.tasks):
            # Find all tasks ready to run (dependencies satisfied)
            ready_tasks: List[CoworkTask] = []
            for tid, task in self.tasks.items():
                if task.status == CoworkTaskStatus.PENDING:
                    if all(dep in completed_task_ids for dep in task.dependencies):
                        ready_tasks.append(task)

            if not ready_tasks:
                # No tasks are ready to run, but some are unfinished -> blocked by failures
                for tid, task in self.tasks.items():
                    if task.status == CoworkTaskStatus.PENDING:
                        task.status = CoworkTaskStatus.SKIPPED
                        failed_task_ids.add(tid)
                break

            # Execute ready tasks concurrently
            async def run_single_task(t: CoworkTask) -> None:
                t.status = CoworkTaskStatus.IN_PROGRESS
                t_start = time.time()
                agent = self.agents.get(t.assigned_role, self.agents.get("synthesizer"))

                # Gather context from dependency outputs
                dep_contexts: Dict[str, Any] = {}
                for dep_id in t.dependencies:
                    dep_task = self.tasks[dep_id]
                    dep_contexts[dep_task.name] = dep_task.result

                prompt = (
                    f"Objective: {objective}\n\n"
                    f"Current Task: {t.name}\n"
                    f"Description: {t.description}\n"
                )

                try:
                    res = await agent.execute(prompt=prompt, memory=self.memory, context=dep_contexts)
                    t.result = res
                    t.status = CoworkTaskStatus.COMPLETED
                    t.execution_time_s = round(time.time() - t_start, 3)
                    completed_task_ids.add(t.id)
                except Exception as exc:
                    t.result = f"Error: {exc}"
                    t.status = CoworkTaskStatus.FAILED
                    t.execution_time_s = round(time.time() - t_start, 3)
                    failed_task_ids.add(t.id)

            await asyncio.gather(*(run_single_task(t) for t in ready_tasks))

        total_time_s = round(time.time() - start_time, 3)

        # Collect final deliverable
        final_deliverable = ""
        for t in reversed(list(self.tasks.values())):
            if t.status == CoworkTaskStatus.COMPLETED and t.result:
                final_deliverable = t.result
                break

        return {
            "objective": objective,
            "status": "completed" if not failed_task_ids else "partial_failure",
            "total_execution_time_s": total_time_s,
            "tasks_count": len(self.tasks),
            "completed_tasks": len(completed_task_ids),
            "failed_tasks": len(failed_task_ids),
            "tasks": [t.model_dump() for t in self.tasks.values()],
            "final_deliverable": final_deliverable,
            "memory_snapshot": self.memory.snapshot(),
        }

    @classmethod
    def create_standard_pipeline(cls, router: RouterEngine, objective: str) -> CoworkGraph:
        """Factory creating a standard 4-stage pipeline (Plan -> Code -> Critic -> Synthesis)."""
        graph = cls(router=router)

        t1 = CoworkTask(
            id="task-1-plan",
            name="Strategic Planning & Decomposition",
            description=f"Decompose the objective into architecture, components, and validation rules: {objective}",
            assigned_role="planner",
        )
        t2 = CoworkTask(
            id="task-2-code",
            name="Implementation & Code Generation",
            description="Generate the core code and data structures implementing the plan.",
            assigned_role="coder",
            dependencies=["task-1-plan"],
        )
        t3 = CoworkTask(
            id="task-3-review",
            name="Adversarial Critic & Security Audit",
            description="Review generated code for edge cases, performance bottlenecks, and security gaps.",
            assigned_role="critic",
            dependencies=["task-2-code"],
        )
        t4 = CoworkTask(
            id="task-4-synthesis",
            name="Final Executive Deliverable Synthesis",
            description="Synthesize final approved code, instructions, and execution summary.",
            assigned_role="synthesizer",
            dependencies=["task-3-review"],
        )

        graph.add_task(t1)
        graph.add_task(t2)
        graph.add_task(t3)
        graph.add_task(t4)
        return graph
