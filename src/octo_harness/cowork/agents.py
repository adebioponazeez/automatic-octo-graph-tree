"""
Specialized AI Agent roles for collaborative Cowork workflows.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from octo_harness.cowork.memory import CoworkMemory
from octo_harness.models import ChatMessage, ChatRole, CompletionRequest, RoutingStrategy
from octo_harness.router.engine import RouterEngine


class BaseCoworkAgent:
    """Base class for all collaborative Cowork agents."""

    def __init__(
        self,
        name: str,
        role: str,
        system_prompt: str,
        router: RouterEngine,
        model_preference: Optional[str] = None,
        strategy: RoutingStrategy = RoutingStrategy.GROK_PRIMARY,
    ):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.router = router
        self.model_preference = model_preference
        self.strategy = strategy

    async def execute(self, prompt: str, memory: CoworkMemory, context: Optional[Dict[str, Any]] = None) -> str:
        """Run agent task through the router engine."""
        messages = [
            ChatMessage(role=ChatRole.SYSTEM, content=self.system_prompt),
            ChatMessage(role=ChatRole.USER, content=prompt),
        ]

        # If previous context is provided, attach to prompt
        if context:
            ctx_summary = "\n".join(f"- {k}: {v}" for k, v in context.items())
            messages.insert(1, ChatMessage(role=ChatRole.SYSTEM, content=f"Working Context:\n{ctx_summary}"))

        req = CompletionRequest(
            messages=messages,
            model=self.model_preference,
            strategy=self.strategy,
            temperature=0.4,
        )

        response = await self.router.complete(req)
        output = response.content

        # Record in memory
        memory.set(f"agent_output:{self.name}", output, author_agent=self.name)
        memory.log(f"Agent '{self.name}' completed task with model '{response.model}' ({response.latency_ms}ms)")

        return output


class PlannerAgent(BaseCoworkAgent):
    """Decomposes complex problems into concrete, dependency-ordered tasks."""

    def __init__(self, router: RouterEngine, model_preference: Optional[str] = None):
        super().__init__(
            name="Planner",
            role="planner",
            system_prompt=(
                "You are an expert Systems Architect & Lead Planner. "
                "Analyze the goal, identify core invariants, break down the work into discrete, "
                "logical tasks, and specify required dependencies and verification gates."
            ),
            router=router,
            model_preference=model_preference,
            strategy=RoutingStrategy.QUALITY_FIRST,
        )


class CoderAgent(BaseCoworkAgent):
    """Generates robust, production-grade, tested implementations."""

    def __init__(self, router: RouterEngine, model_preference: Optional[str] = None):
        super().__init__(
            name="Coder",
            role="coder",
            system_prompt=(
                "You are a Senior Principal Software Engineer. "
                "Write clean, idiomatic, fully tested, and resilient code. "
                "Adhere to strict type hints, error handling, and zero undefined behavior."
            ),
            router=router,
            model_preference=model_preference,
            strategy=RoutingStrategy.GROK_PRIMARY,
        )


class CriticAgent(BaseCoworkAgent):
    """Conducts adversarial reviews, edge case detection, and invariant verification."""

    def __init__(self, router: RouterEngine, model_preference: Optional[str] = None):
        super().__init__(
            name="Critic",
            role="critic",
            system_prompt=(
                "You are a Rigorous Code Reviewer and Red Team Critic. "
                "Scrutinize plans, designs, and code for logic gaps, security flaws, race conditions, "
                "unhandled exceptions, and edge cases. Demand concrete proofs and tests."
            ),
            router=router,
            model_preference=model_preference,
            strategy=RoutingStrategy.QUALITY_FIRST,
        )


class SynthesizerAgent(BaseCoworkAgent):
    """Consolidates cross-agent outputs into final unified deliverables."""

    def __init__(self, router: RouterEngine, model_preference: Optional[str] = None):
        super().__init__(
            name="Synthesizer",
            role="synthesizer",
            system_prompt=(
                "You are a Lead Solutions Synthesizer. "
                "Combine intermediate agent findings, resolve any debates, and format the "
                "final deliverable with clarity, executive summaries, and action steps."
            ),
            router=router,
            model_preference=model_preference,
            strategy=RoutingStrategy.COST_OPTIMIZED,
        )


class SafetyAuditorAgent(BaseCoworkAgent):
    """Audits solutions for security, safety, credential leaks, and harmful actions."""

    def __init__(self, router: RouterEngine, model_preference: Optional[str] = None):
        super().__init__(
            name="SafetyAuditor",
            role="auditor",
            system_prompt=(
                "You are a DevSecOps & AI Safety Auditor. "
                "Inspect all generated outputs for exposed secrets, malicious payloads, "
                "unauthorized network commands, and policy violations."
            ),
            router=router,
            model_preference=model_preference,
            strategy=RoutingStrategy.QUALITY_FIRST,
        )


class GrokbotAgent(BaseCoworkAgent):
    """Real-time world-state grounding, adversarial probing, and anti-sycophancy review."""

    def __init__(self, router: RouterEngine, model_preference: Optional[str] = "grok-3"):
        super().__init__(
            name="Grokbot",
            role="grounding_adversary",
            system_prompt=(
                "You are Grokbot (AGT-GROK-001) · Real-Time Grounding & Adversarial Probe. "
                "Your mission is live world-state verification, breaking API drift detection, "
                "and ruthless anti-sycophantic challenge. Probe all hidden assumptions, cross-reference "
                "real-time ecosystem trends, and state unvarnished technical realities with zero fluff."
            ),
            router=router,
            model_preference=model_preference,
            strategy=RoutingStrategy.GROK_PRIMARY,
        )


class KimiContextAgent(BaseCoworkAgent):
    """Ultra-long context corpus distillation, repository ingestion, and dependency indexing."""

    def __init__(self, router: RouterEngine, model_preference: Optional[str] = "moonshotai/kimi-k3"):
        super().__init__(
            name="KimiContextEngine",
            role="context_synthesizer",
            system_prompt=(
                "You are Kimi Context Engine (AGT-KIMI-001) · 2M+ Token Corpus Synthesizer. "
                "Your role is massive codebase ingestion, hierarchical dependency mapping, and lossless 100:1 "
                "context distillation. Extract exact symbol definitions, types, schemas, and invariants into dense, "
                "actionable execution capsules for downstream specialist workers."
            ),
            router=router,
            model_preference=model_preference,
            strategy=RoutingStrategy.COST_OPTIMIZED,
        )
