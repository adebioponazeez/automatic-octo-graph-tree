"""
API route definitions for Octo Harness Server.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from octo_harness.cowork.consensus import ModelDebateConsensus
from octo_harness.cowork.fusion import FrontierHarnessFusion, FusionParameter
from octo_harness.cowork.graph import CoworkGraph
from octo_harness.cowork.invariant_verifier import InvariantVerifierEngine, VerificationProof
from octo_harness.models import (
    ChatMessage,
    CompletionRequest,
    CompletionResponse,
    ModelSpec,
    RouteDecision,
    RoutingStrategy,
)
from octo_harness.router.engine import RouterEngine


class CoworkRunPayload(BaseModel):
    objective: str
    custom_tasks: Optional[List[Dict[str, Any]]] = None
    session_id: Optional[str] = None


class ConsensusPayload(BaseModel):
    query: str
    target_models: Optional[List[str]] = None
    judge_model: str = "grok-3"


class FusionPayload(BaseModel):
    objective: str
    parameters: Optional[List[FusionParameter]] = None
    arbiter_model: str = "grok-3"


class InvariantVerifyPayload(BaseModel):
    objective: str
    candidate_artifact: str
    expected_output_type: str = "code"  # code | json | architectural_plan
    max_remediation_rounds: int = 2


def create_router(engine: RouterEngine) -> APIRouter:
    api = APIRouter()
    consensus_engine = ModelDebateConsensus(engine)
    fusion_engine = FrontierHarnessFusion(engine)
    verifier_engine = InvariantVerifierEngine(engine)

    # 1. Health & Liveness
    @api.get("/health")
    async def health_check() -> Dict[str, str]:
        return {"status": "ok", "service": "octo-harness", "version": engine.settings.version}

    @api.get("/ready")
    async def ready_check() -> Dict[str, Any]:
        catalog_count = len(engine.catalog)
        return {
            "ready": catalog_count > 0,
            "catalog_count": catalog_count,
            "providers_registered": list(engine.providers.keys()),
        }

    @api.get("/pulse")
    async def pulse() -> Dict[str, Any]:
        return await engine.get_health_status()

    # 2. OpenAI-Compatible Models Endpoint
    @api.get("/v1/models")
    async def list_models() -> Dict[str, Any]:
        data = []
        for m in engine.catalog.values():
            data.append({
                "id": m.model_id,
                "object": "model",
                "created": 1700000000,
                "owned_by": m.provider_type.value,
                "permission": [],
                "root": m.model_id,
                "parent": None,
                "capabilities": [c.value for c in m.capabilities],
                "pricing": {
                    "input_per_million": m.input_cost_per_million,
                    "output_per_million": m.output_cost_per_million,
                },
                "latency_ms": m.average_latency_ms,
            })
        return {"object": "list", "data": data}

    # 3. Route Inspection Endpoint
    @api.post("/v1/route")
    async def inspect_route(request: CompletionRequest) -> RouteDecision:
        return engine.route_request(request)

    # 4. OpenAI-Compatible Chat Completions Proxy
    @api.post("/v1/chat/completions")
    async def chat_completions(raw_req: Dict[str, Any]) -> Any:
        try:
            # Parse messages
            raw_messages = raw_req.get("messages", [])
            messages = [
                ChatMessage(
                    role=m.get("role", "user"),
                    content=m.get("content", ""),
                    name=m.get("name"),
                )
                for m in raw_messages
            ]

            # Parse strategy if passed
            raw_strategy = raw_req.get("strategy", "grok_primary")
            try:
                strategy = RoutingStrategy(raw_strategy)
            except ValueError:
                strategy = RoutingStrategy.GROK_PRIMARY

            req = CompletionRequest(
                messages=messages,
                model=raw_req.get("model"),
                strategy=strategy,
                temperature=float(raw_req.get("temperature", 0.7)),
                max_tokens=raw_req.get("max_tokens"),
                stream=bool(raw_req.get("stream", False)),
                tools=raw_req.get("tools"),
                response_format=raw_req.get("response_format"),
                fallback_models=raw_req.get("fallback_models"),
                allow_fallback=raw_req.get("allow_fallback", True),
            )

            if req.stream:
                async def event_generator():
                    async for chunk in engine.stream(req):
                        chunk_payload = {
                            "id": f"chatcmpl-{int(time.time())}",
                            "object": "chat.completion.chunk",
                            "created": int(time.time()),
                            "model": req.model or "grok-2-latest",
                            "choices": [{"index": 0, "delta": {"content": chunk}, "finish_reason": None}],
                        }
                        yield f"data: {json.dumps(chunk_payload)}\n\n"
                    yield "data: [DONE]\n\n"

                return StreamingResponse(event_generator(), media_type="text/event-stream")

            res = await engine.complete(req)
            return res.model_dump()

        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

    # 5. Cowork DAG Workflow Runner
    @api.post("/cowork/run")
    async def run_cowork(payload: CoworkRunPayload) -> Dict[str, Any]:
        pipeline = CoworkGraph.create_standard_pipeline(
            router=engine, objective=payload.objective
        )
        result = await pipeline.execute(payload.objective)
        return result

    # 6. Multi-Model Debate & Consensus
    @api.post("/cowork/consensus")
    async def run_consensus(payload: ConsensusPayload) -> Dict[str, Any]:
        result = await consensus_engine.run_consensus(
            prompt=payload.query,
            target_models=payload.target_models,
            judge_model=payload.judge_model,
        )
        return result.model_dump()

    # 7. Frontier Model Harness Fusion
    @api.post("/cowork/fusion")
    async def run_fusion(payload: FusionPayload) -> Dict[str, Any]:
        result = await fusion_engine.execute_fusion(
            objective=payload.objective,
            parameters=payload.parameters,
            arbiter_model=payload.arbiter_model,
        )
        return result.model_dump()

    # 8. Deterministic Invariant Prover & Gate
    @api.post("/cowork/verify")
    async def run_invariant_verification(payload: InvariantVerifyPayload) -> Dict[str, Any]:
        result = await verifier_engine.verify_and_prove(
            objective=payload.objective,
            candidate_artifact=payload.candidate_artifact,
            expected_output_type=payload.expected_output_type,
            max_remediation_rounds=payload.max_remediation_rounds,
        )
        return result.model_dump()

    # 9. Batch Processing Endpoints
    @api.post("/batch/submit")
    async def submit_batch(request: CompletionRequest, priority: int = Query(50)) -> Dict[str, Any]:
        job = engine.batch_processor.submit_job(request, priority=priority)
        return job.model_dump()

    @api.post("/batch/flush")
    async def flush_batch(max_jobs: int = Query(10)) -> Dict[str, Any]:
        processed = await engine.batch_processor.flush_batch(max_jobs=max_jobs)
        return {
            "processed_count": len(processed),
            "jobs": [j.model_dump() for j in processed],
            "total_batch_savings_usd": engine.batch_processor._total_batch_savings_usd,
        }

    @api.get("/batch/status")
    async def batch_status() -> Dict[str, Any]:
        return engine.batch_processor.get_queue_status()

    # 8. Metrics Endpoint
    @api.get("/metrics")
    async def metrics(format: str = Query("json", enum=["json", "prometheus"])) -> Any:
        summary = engine.cost_tracker.get_summary()
        health = await engine.get_health_status()

        if format == "prometheus":
            lines = [
                "# HELP octo_requests_total Total requests processed by router",
                "# TYPE octo_requests_total counter",
                f"octo_requests_total {summary['total_requests']}",
                "# HELP octo_cost_usd_total Estimated total cost in USD",
                "# TYPE octo_cost_usd_total counter",
                f"octo_cost_usd_total {summary['total_cost_usd']}",
                "# HELP octo_tokens_total Total tokens processed",
                "# TYPE octo_tokens_total counter",
                f"octo_tokens_total {summary['total_tokens']}",
            ]
            return HTMLResponse(content="\n".join(lines), media_type="text/plain")

        return {
            "metrics": summary,
            "health": health,
        }

    return api
