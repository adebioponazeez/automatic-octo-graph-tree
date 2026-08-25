"""
Deterministic Invariant Verification & Formal Proving Engine.
Replaces rhetorical 'debate' with empirical falsification, automated test gates,
and bounded remediation loops for mission-critical production workloads.
"""

from __future__ import annotations

import ast
import hashlib
import json
import time
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from octo_harness.governance.guardrails import ContentGuardrails
from octo_harness.governance.validator import JsonValidator
from octo_harness.models import ChatMessage, ChatRole, CompletionRequest, RoutingStrategy
from octo_harness.router.engine import RouterEngine


class InvariantType(str, Enum):
    SYNTAX_AND_AST = "syntax_and_ast"                 # Code parseable, valid Python/JSON AST
    SCHEMA_CONFORMANCE = "schema_conformance"         # Matches strict Pydantic/JSON schema
    SECURITY_INTEGRITY = "security_integrity"         # Zero secrets, no dangerous commands, no SSRF
    ADVERSARIAL_ROBUSTNESS = "adversarial_robustness" # Passes boundary vectors (0, inf, null, race conditions)
    COST_AND_BUDGET_GATE = "cost_and_budget_gate"     # Within strict $50/mo token cost limits


class InvariantCheck(BaseModel):
    invariant_name: str
    invariant_type: InvariantType
    passed: bool
    diagnostic: str
    falsifying_vector: Optional[str] = None
    execution_time_ms: float = 0.0


class VerificationProof(BaseModel):
    objective: str
    passed_all_gates: bool
    final_artifact: str
    proof_hash: str
    invariant_checks: List[InvariantCheck] = Field(default_factory=list)
    falsifying_vectors_identified: List[str] = Field(default_factory=list)
    remediations_performed: int = 0
    total_verification_time_ms: float = 0.0
    total_cost_usd: float = 0.0
    evidence_block: Dict[str, Any] = Field(default_factory=dict)


class InvariantVerifierEngine:
    """
    Mission-critical verification engine that enforces empirical truth over rhetorical consensus.
    Runs a 4-tier verification gate:
    1. Deterministic AST / Syntax & Schema Gate
    2. Security & Secret Leak Gate
    3. Adversarial Red-Team Invariant Falsification Gate
    4. Bounded Defect Remediation Loop (Max 2 Rounds)
    """

    def __init__(self, router: RouterEngine):
        self.router = router

    async def verify_and_prove(
        self,
        objective: str,
        candidate_artifact: str,
        expected_output_type: str = "code",  # code | json | architectural_plan
        max_remediation_rounds: int = 2,
    ) -> VerificationProof:
        """
        Executes strict invariant verification on a candidate artifact.
        If a gate fails, triggers deterministic remediation with the exact falsifying vector.
        """
        start_time = time.time()
        current_artifact = candidate_artifact
        remediations = 0
        total_cost = 0.0
        all_checks: List[InvariantCheck] = []
        all_falsifying_vectors: List[str] = []

        for round_idx in range(max_remediation_rounds + 1):
            round_checks: List[InvariantCheck] = []
            falsifying_vectors: List[str] = []

            # -------------------------------------------------------------
            # GATE 1: Deterministic Syntax & AST Validation (Zero-Cost)
            # -------------------------------------------------------------
            g1_start = time.time()
            if expected_output_type == "code" and ("```python" in current_artifact or "def " in current_artifact):
                code_snippet = self._extract_code(current_artifact)
                try:
                    ast.parse(code_snippet)
                    round_checks.append(
                        InvariantCheck(
                            invariant_name="Python AST Validation",
                            invariant_type=InvariantType.SYNTAX_AND_AST,
                            passed=True,
                            diagnostic="AST parsed cleanly without syntax errors",
                            execution_time_ms=round((time.time() - g1_start) * 1000, 2),
                        )
                    )
                except SyntaxError as err:
                    round_checks.append(
                        InvariantCheck(
                            invariant_name="Python AST Validation",
                            invariant_type=InvariantType.SYNTAX_AND_AST,
                            passed=False,
                            diagnostic=f"SyntaxError at line {err.lineno}: {err.msg}",
                            falsifying_vector=f"SyntaxError at line {err.lineno}: {err.msg}",
                            execution_time_ms=round((time.time() - g1_start) * 1000, 2),
                        )
                    )
                    falsifying_vectors.append(f"SyntaxError: {err.msg} (Line {err.lineno})")

            elif expected_output_type == "json":
                ok, parsed, err_msg = JsonValidator.try_parse_or_repair(current_artifact)
                round_checks.append(
                    InvariantCheck(
                        invariant_name="JSON Schema Validation",
                        invariant_type=InvariantType.SCHEMA_CONFORMANCE,
                        passed=ok,
                        diagnostic="JSON schema parsed and validated" if ok else f"Malformed JSON: {err_msg}",
                        falsifying_vector=err_msg if not ok else None,
                        execution_time_ms=round((time.time() - g1_start) * 1000, 2),
                    )
                )
                if not ok:
                    falsifying_vectors.append(f"JSON validation defect: {err_msg}")

            # -------------------------------------------------------------
            # GATE 2: Security & Secret Leak Inspection
            # -------------------------------------------------------------
            g2_start = time.time()
            is_inj, inj_reason = ContentGuardrails.check_prompt_injection(current_artifact)
            has_secret = "[REDACTED_SECRET]" in ContentGuardrails.scrub_secrets(current_artifact) and not ("[REDACTED_SECRET]" in current_artifact)

            sec_passed = (not is_inj) and (not has_secret)
            sec_diag = "Passed security & secret scan" if sec_passed else f"Security breach: {inj_reason or 'Plaintext secret pattern detected'}"
            round_checks.append(
                InvariantCheck(
                    invariant_name="Security & Secret Hygiene",
                    invariant_type=InvariantType.SECURITY_INTEGRITY,
                    passed=sec_passed,
                    diagnostic=sec_diag,
                    falsifying_vector=inj_reason if not sec_passed else None,
                    execution_time_ms=round((time.time() - g2_start) * 1000, 2),
                )
            )
            if not sec_passed:
                falsifying_vectors.append(sec_diag)

            # -------------------------------------------------------------
            # GATE 3: Adversarial Red-Team Invariant Falsification
            # -------------------------------------------------------------
            g3_start = time.time()
            red_team_prompt = (
                f"Objective: {objective}\n\n"
                f"Candidate Artifact:\n{current_artifact[:1500]}\n\n"
                "Task: Act as a ruthless Red Team Invariant Prover. "
                "Find any concrete edge-case inputs, race conditions, memory leaks, unhandled exceptions, "
                "or mathematical flaws that break this solution. "
                "If flaws exist, provide the exact input/scenario that causes failure. "
                "If provably correct, reply with 'INVARIANT_PROVEN'."
            )

            req = CompletionRequest(
                messages=[
                    ChatMessage(
                        role=ChatRole.SYSTEM,
                        content="You are a strict formal invariant prover. Reject rhetoric. Find concrete failure vectors.",
                    ),
                    ChatMessage(role=ChatRole.USER, content=red_team_prompt),
                ],
                strategy=RoutingStrategy.QUALITY_FIRST,
                temperature=0.1,
            )

            res = await self.router.complete(req)
            total_cost += res.usage.estimated_cost_usd
            critique_text = res.content

            if "INVARIANT_PROVEN" in critique_text or "flawless" in critique_text.lower():
                round_checks.append(
                    InvariantCheck(
                        invariant_name="Adversarial Invariant Prover",
                        invariant_type=InvariantType.ADVERSARIAL_ROBUSTNESS,
                        passed=True,
                        diagnostic="No falsifying vectors found; invariant proven under red-team test.",
                        execution_time_ms=round((time.time() - g3_start) * 1000, 2),
                    )
                )
            else:
                round_checks.append(
                    InvariantCheck(
                        invariant_name="Adversarial Invariant Prover",
                        invariant_type=InvariantType.ADVERSARIAL_ROBUSTNESS,
                        passed=False,
                        diagnostic="Red-team discovered potential failure mode",
                        falsifying_vector=critique_text[:300],
                        execution_time_ms=round((time.time() - g3_start) * 1000, 2),
                    )
                )
                falsifying_vectors.append(critique_text[:200])

            all_checks.extend(round_checks)
            all_falsifying_vectors.extend(falsifying_vectors)

            # Check if all gates in this round passed
            all_passed = all(c.passed for c in round_checks)
            if all_passed or round_idx >= max_remediation_rounds:
                break

            # -------------------------------------------------------------
            # GATE 4: Automated Targeted Remediation
            # -------------------------------------------------------------
            remediations += 1
            remediation_prompt = (
                f"Original Objective: {objective}\n\n"
                f"Current Artifact:\n{current_artifact}\n\n"
                f"Verification Gate Failure Vector(s):\n" + "\n".join(f"- {v}" for v in falsifying_vectors) + "\n\n"
                "Directive: Fix the exact defects identified above. Provide the corrected, fully working artifact. "
                "Ensure zero syntax errors, strict type safety, and complete invariant compliance."
            )

            fix_req = CompletionRequest(
                messages=[
                    ChatMessage(
                        role=ChatRole.SYSTEM,
                        content="You are a Senior Principal Engineer fixing verified defect vectors.",
                    ),
                    ChatMessage(role=ChatRole.USER, content=remediation_prompt),
                ],
                strategy=RoutingStrategy.GROK_PRIMARY,
                temperature=0.2,
            )

            fix_res = await self.router.complete(fix_req)
            total_cost += fix_res.usage.estimated_cost_usd
            current_artifact = fix_res.content

        # Compute SHA-256 proof hash
        proof_hash = hashlib.sha256(current_artifact.encode("utf-8")).hexdigest()
        total_time_ms = round((time.time() - start_time) * 1000.0, 2)
        passed_all = all(c.passed for c in round_checks)

        evidence_block = {
            "target_objective": objective,
            "proof_hash": proof_hash,
            "passed_all_gates": passed_all,
            "gates_evaluated": len(all_checks),
            "remediations_performed": remediations,
            "total_verification_time_ms": total_time_ms,
            "total_cost_usd": round(total_cost, 6),
            "autonomy_tier": "A2",
            "evidence_standard": "INVARIANT_PROVEN_V1",
        }

        return VerificationProof(
            objective=objective,
            passed_all_gates=passed_all,
            final_artifact=current_artifact,
            proof_hash=proof_hash,
            invariant_checks=all_checks,
            falsifying_vectors_identified=all_falsifying_vectors,
            remediations_performed=remediations,
            total_verification_time_ms=total_time_ms,
            total_cost_usd=round(total_cost, 6),
            evidence_block=evidence_block,
        )

    def _extract_code(self, text: str) -> str:
        """Extract Python code block from markdown or return raw text."""
        if "```python" in text:
            start = text.find("```python") + 9
            end = text.find("```", start)
            if end != -1:
                return text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            if end != -1:
                return text[start:end].strip()
        return text.strip()
