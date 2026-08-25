"""
Command-line interface (CLI) for Octo Harness.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from typing import List, Optional

from octo_harness import __version__
from octo_harness.config import Settings, get_settings
from octo_harness.cowork.consensus import ModelDebateConsensus
from octo_harness.cowork.fusion import FrontierHarnessFusion, FusionParameter
from octo_harness.cowork.graph import CoworkGraph
from octo_harness.cowork.intelligence_explosion import IntelligenceExplosionEngine
from octo_harness.cowork.invariant_verifier import InvariantVerifierEngine
from octo_harness.models import ChatMessage, ChatRole, CompletionRequest, RoutingStrategy
from octo_harness.router.engine import RouterEngine


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="octo-harness",
        description="Octo Harness: Cowork & Grok Multi-Model AI Router Engine",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--mock", action="store_true", help="Force deterministic mock mode (offline)")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # 1. route
    route_parser = subparsers.add_parser("route", help="Route and execute a prompt")
    route_parser.add_argument("prompt", type=str, help="Prompt text to process")
    route_parser.add_argument(
        "--strategy",
        "-s",
        type=str,
        default="grok_primary",
        choices=["grok_primary", "quality_first", "cost_optimized", "latency_optimized"],
        help="Routing policy strategy",
    )
    route_parser.add_argument("--model", "-m", type=str, default=None, help="Explicit model override")
    route_parser.add_argument("--stream", action="store_true", help="Stream response tokens")
    route_parser.add_argument("--json", action="store_true", help="Emit raw JSON response")

    # 2. cowork
    cowork_parser = subparsers.add_parser("cowork", help="Execute multi-agent collaborative DAG pipeline")
    cowork_parser.add_argument("objective", type=str, help="High-level objective or problem statement")
    cowork_parser.add_argument("--json", action="store_true", help="Emit raw JSON output")

    # 3. consensus
    consensus_parser = subparsers.add_parser("consensus", help="Run multi-model cross-examination debate")
    consensus_parser.add_argument("query", type=str, help="Query topic for debate")
    consensus_parser.add_argument(
        "--models",
        nargs="+",
        default=["grok-2-latest", "gpt-4o", "mock-frontier"],
        help="Models to participate in debate",
    )

    # 4. fusion
    fusion_parser = subparsers.add_parser("fusion", help="Run multi-frontier model harness fusion")
    fusion_parser.add_argument("objective", type=str, help="High-impact objective to fuse across models")
    fusion_parser.add_argument("--json", action="store_true", help="Emit raw JSON output")

    # 5. verify (Deterministic Invariant Prover Gate)
    verify_parser = subparsers.add_parser("verify", help="Execute deterministic invariant proving and defect remediation")
    verify_parser.add_argument("objective", type=str, help="Target objective / contract specification")
    verify_parser.add_argument("artifact", type=str, help="Code, JSON, or architectural plan to formally verify")
    verify_parser.add_argument("--type", "-t", default="code", choices=["code", "json", "architectural_plan"], help="Expected artifact type")
    verify_parser.add_argument("--json", action="store_true", help="Emit raw JSON proof output")

    # 6. explode (Recursive Intelligence Explosion & Super-Fusion)
    explode_parser = subparsers.add_parser("explode", help="Launch recursive intelligence explosion super-harness")
    explode_parser.add_argument("objective", type=str, help="Strategic objective for superhuman intelligence amplification")
    explode_parser.add_argument("--epochs", "-e", type=int, default=3, help="Amplification epochs (default: 3)")
    explode_parser.add_argument("--type", "-t", default="code", choices=["code", "json", "architectural_plan"], help="Artifact type")
    explode_parser.add_argument("--json", action="store_true", help="Emit raw JSON report")

    # 7. pulse
    subparsers.add_parser("pulse", help="Display live provider health and cost analytics")

    # 5. models
    subparsers.add_parser("models", help="List supported models and capabilities")

    # 6. serve
    serve_parser = subparsers.add_parser("serve", help="Launch FastAPI server & web console")
    serve_parser.add_argument("--host", type=str, default="0.0.0.0", help="Bind host (default: 0.0.0.0)")
    serve_parser.add_argument("--port", "-p", type=int, default=8000, help="Bind port (default: 8000)")
    serve_parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")

    return parser


async def handle_route(engine: RouterEngine, args: argparse.Namespace) -> int:
    try:
        strat = RoutingStrategy(args.strategy)
    except ValueError:
        strat = RoutingStrategy.GROK_PRIMARY

    req = CompletionRequest(
        messages=[ChatMessage(role=ChatRole.USER, content=args.prompt)],
        strategy=strat,
        model=args.model,
    )

    if args.stream:
        print(f"[*] Streaming response via Octo Router ({args.strategy})...")
        async for chunk in engine.stream(req):
            sys.stdout.write(chunk)
            sys.stdout.flush()
        print("\n")
        return 0

    res = await engine.complete(req)

    if args.json:
        print(json.dumps(res.model_dump(), indent=2))
        return 0

    print("=" * 60)
    print(f" Model:     {res.model} ({res.provider.value})")
    print(f" Strategy:  {res.route_decision.strategy.value if res.route_decision else 'default'}")
    print(f" Latency:   {res.latency_ms} ms")
    print(f" Tokens:    {res.usage.total_tokens} (Cost: ${res.usage.estimated_cost_usd:.5f})")
    if res.fallback_occurred:
        print(f" Fallback:  YES ({' -> '.join(res.fallback_history)})")
    print("=" * 60)
    print(res.content)
    print("=" * 60)
    return 0


async def handle_cowork(engine: RouterEngine, args: argparse.Namespace) -> int:
    print(f"[*] Initializing Cowork Multi-Agent Workflow DAG for objective:")
    print(f"    '{args.objective}'\n")

    pipeline = CoworkGraph.create_standard_pipeline(router=engine, objective=args.objective)
    result = await pipeline.execute(args.objective)

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print("=" * 60)
    print(f" Cowork Pipeline Execution: {result['status'].upper()}")
    print(f" Total Duration: {result['total_execution_time_s']} seconds")
    print(f" Tasks Finished: {result['completed_tasks']} / {result['tasks_count']}")
    print("=" * 60)

    for t in result["tasks"]:
        print(f" [{t['status'].upper():9s}] Task: {t['name']} (Role: {t['assigned_role']})")

    print("\n" + "=" * 60)
    print(" FINAL SYNTHESIZED DELIVERABLE:")
    print("=" * 60)
    print(result["final_deliverable"])
    return 0


async def handle_consensus(engine: RouterEngine, args: argparse.Namespace) -> int:
    print(f"[*] Launching Multi-Model Cross-Examination for query:\n    '{args.query}'\n")
    debate = ModelDebateConsensus(engine)
    res = await debate.run_consensus(prompt=args.query, target_models=args.models)

    print("=" * 60)
    print(f" Multi-Model Opinions Collected ({len(res.opinions)} models):")
    for op in res.opinions:
        print(f"\n--- Model [{op.model_id}] ({op.latency_ms}ms, ${op.cost_usd:.5f}) ---")
        print(op.content[:200] + ("..." if len(op.content) > 200 else ""))

    print("\n" + "=" * 60)
    print(" SYNTHESIZED CONSENSUS VERDICT:")
    print("=" * 60)
    print(res.consensus_summary)
    return 0


async def handle_fusion(engine: RouterEngine, args: argparse.Namespace) -> int:
    print(f"[*] Launching Frontier Model Harness Fusion for:\n    '{args.objective}'\n")
    fusion = FrontierHarnessFusion(engine)
    res = await fusion.execute_fusion(objective=args.objective)

    if args.json:
        print(json.dumps(res.model_dump(), indent=2))
        return 0

    print("=" * 70)
    print(f" FRONTIER FUSION COMPLETE | Composite Quality Score: {res.composite_quality_score:.2f}")
    print(f" Total Duration: {res.total_latency_ms}ms | Cost: ${res.total_cost_usd:.5f}")
    print("=" * 70)

    print("\n[1] SPECIALIZED FRONTIER PROPOSALS:")
    for prop in res.proposals:
        print(f"  - Model: {prop.model_id:25s} | Focus: {prop.parameter_targeted.value}")

    print("\n[2] ADVERSARIAL RED TEAM CRITIQUES:")
    for c in res.critiques:
        print(f"  - Auditor: {c.critic_model:20s} on {c.proposer_model}")

    print("\n" + "=" * 70)
    print(" [3] DEFINITIVE FUSED DELIVERABLE:")
    print("=" * 70)
    print(res.fused_deliverable)
    print("=" * 70)
    return 0


async def handle_pulse(engine: RouterEngine) -> int:
    health = await engine.get_health_status()
    print("=" * 60)
    print(f" Octo Harness Status: {health['status'].upper()}")
    print("=" * 60)
    print(" PROVIDERS:")
    for pname, pdata in health["providers"].items():
        st = pdata.get("status", "unknown")
        lat = pdata.get("latency_ms", 0)
        reqs = pdata.get("total_requests", 0)
        print(f"  - {pname:12s}: {st.upper():10s} (Latency: {lat}ms, Total: {reqs})")

    print("\n CIRCUITS:")
    for cname, state in health["circuit_breakers"].items():
        print(f"  - {cname:25s}: [{state}]")

    print("\n BUDGET & COSTS:")
    csum = health["cost_summary"]
    print(f"  - Total Spent:   ${csum['total_cost_usd']:.4f} / ${csum['budget_limit_usd']:.2f}")
    print(f"  - Total Tokens:  {csum['total_tokens']:,}")
    print(f"  - Total Queries: {csum['total_requests']}")
    print("=" * 60)
    return 0


async def handle_verify(engine: RouterEngine, args: argparse.Namespace) -> int:
    print(f"[*] Launching Deterministic Invariant Prover Gate for:\n    Objective: '{args.objective}'\n")
    verifier = InvariantVerifierEngine(engine)
    proof = await verifier.verify_and_prove(
        objective=args.objective,
        candidate_artifact=args.artifact,
        expected_output_type=args.type,
    )

    if args.json:
        print(json.dumps(proof.model_dump(), indent=2))
        return 0

    status_str = "PASSED (INVARIANT PROVEN)" if proof.passed_all_gates else "FAILED"
    print("=" * 70)
    print(f" INVARIANT PROVING RESULT: {status_str}")
    print(f" Proof Hash:    {proof.proof_hash[:16]}...")
    print(f" Duration:      {proof.total_verification_time_ms}ms | Cost: ${proof.total_cost_usd:.5f}")
    print(f" Remediations:  {proof.remediations_performed}")
    print("=" * 70)

    print("\n GATES EVALUATED:")
    for chk in proof.invariant_checks:
        st = "PASS" if chk.passed else "FAIL"
        print(f"  [{st:4s}] {chk.invariant_name:30s}: {chk.diagnostic} ({chk.execution_time_ms}ms)")

    if proof.falsifying_vectors_identified:
        print("\n FALSIFYING DEFECT VECTORS:")
        for fv in proof.falsifying_vectors_identified:
            print(f"  - {fv}")

    print("\n" + "=" * 70)
    print(" FINAL VERIFIED ARTIFACT:")
    print("=" * 70)
    print(proof.final_artifact)
    print("=" * 70)
    return 0 if proof.passed_all_gates else 1


async def handle_explode(engine: RouterEngine, args: argparse.Namespace) -> int:
    print("=" * 80)
    print(" [*] INITIATING SOVEREIGN INTELLIGENCE EXPLOSION SUPER-HARNESS")
    print(f"     Objective: '{args.objective}' | Target Epochs: {args.epochs}")
    print("=" * 80 + "\n")

    explosion_engine = IntelligenceExplosionEngine(engine)
    res = await explosion_engine.explode_intelligence(
        objective=args.objective,
        target_epochs=args.epochs,
        artifact_type=args.type,
    )

    if args.json:
        print(json.dumps(res.model_dump(), indent=2))
        return 0

    print("=" * 80)
    print(f" INTELLIGENCE EXPLOSION COMPLETE | Capability Multiplier: {res.capability_multiplier}x")
    print(f" Quality Curve: {res.initial_quality_score:.2f} -> {res.final_quality_score:.2f}")
    print(f" Total Time:    {res.total_execution_time_ms}ms | Cost: ${res.total_cost_usd:.5f}")
    print(f" Proof Hash:    {res.proof_hash[:20]}...")
    print("=" * 80)

    if res.synthesized_tools:
        print("\n [AUTONOMOUS TOOLS SYNTHESIZED]:")
        for st in res.synthesized_tools:
            print(f"  + {st.tool_name:25s}: {st.description}")

    print("\n [META-INVARIANTS CRYSTALLIZED]:")
    for mi in res.meta_invariants_learned:
        print(f"  * {mi}")

    print("\n" + "=" * 80)
    print(" SUPER-ARTIFACT DELIVERABLE:")
    print("=" * 80)
    print(res.super_artifact)
    print("=" * 80)
    return 0


def handle_models(engine: RouterEngine) -> int:
    print("=" * 80)
    print(f" {'MODEL ID':30s} | {'PROVIDER':10s} | {'LATENCY':8s} | {'CAPABILITIES'}")
    print("=" * 80)
    for m in engine.catalog.values():
        caps = ", ".join(c.value for c in m.capabilities[:3])
        print(f" {m.model_id:30s} | {m.provider_type.value:10s} | {m.average_latency_ms:5.0f}ms   | {caps}")
    print("=" * 80)
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    settings = get_settings()
    if args.mock:
        settings.mock_mode = True

    engine = RouterEngine(settings=settings)

    if args.command == "serve":
        import uvicorn
        from octo_harness.server.app import create_app

        app = create_app(settings=settings, engine=engine)
        print(f"[*] Starting Octo Harness Server on {args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)
        return 0

    if args.command == "models":
        return handle_models(engine)

    if args.command == "pulse":
        return asyncio.run(handle_pulse(engine))

    if args.command == "route":
        return asyncio.run(handle_route(engine, args))

    if args.command == "cowork":
        return asyncio.run(handle_cowork(engine, args))

    if args.command == "consensus":
        return asyncio.run(handle_consensus(engine, args))

    if args.command == "fusion":
        return asyncio.run(handle_fusion(engine, args))

    if args.command == "verify":
        return asyncio.run(handle_verify(engine, args))

    if args.command == "explode":
        return asyncio.run(handle_explode(engine, args))

    return 0


if __name__ == "__main__":
    sys.exit(main())
