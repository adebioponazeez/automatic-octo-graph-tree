"""
Batch Processing Queue for non-urgent background tasks with 50% cost discounts.
"""

from __future__ import annotations

import asyncio
import time
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from octo_harness.models import CompletionRequest, CompletionResponse


class BatchJob(BaseModel):
    id: str = Field(default_factory=lambda: f"batch_{uuid.uuid4().hex[:8]}")
    request: CompletionRequest
    priority: int = 50  # Higher = runs sooner in batch
    created_at: float = Field(default_factory=time.time)
    status: str = "queued"  # queued | processing | completed | failed
    response: Optional[CompletionResponse] = None
    discount_applied_percent: float = 50.0  # 50% off for batch processing
    cost_saved_usd: float = 0.0
    error: Optional[str] = None


class BatchProcessor:
    """
    Manages asynchronous batch execution queues for background agent tasks.
    Applies a 50% discount factor corresponding to provider Batch APIs (e.g. OpenAI / Anthropic Batches).
    """

    def __init__(self, engine: Any):
        self.engine = engine
        self._queue: List[BatchJob] = []
        self._completed_jobs: Dict[str, BatchJob] = {}
        self._total_jobs_processed: int = 0
        self._total_batch_savings_usd: float = 0.0

    def submit_job(self, request: CompletionRequest, priority: int = 50) -> BatchJob:
        """Enqueue a new completion request for batch processing."""
        job = BatchJob(request=request, priority=priority)
        self._queue.append(job)
        # Sort queue by priority descending
        self._queue.sort(key=lambda j: j.priority, reverse=True)
        return job

    async def flush_batch(self, max_jobs: int = 10) -> List[BatchJob]:
        """Process pending batch jobs concurrently with discount applied."""
        jobs_to_process = self._queue[:max_jobs]
        self._queue = self._queue[max_jobs:]

        if not jobs_to_process:
            return []

        async def run_single_job(job: BatchJob) -> BatchJob:
            job.status = "processing"
            try:
                # Execute request through the router engine
                res = await self.engine.complete(job.request)

                # Apply 50% batch discount savings
                baseline_cost = res.usage.estimated_cost_usd
                discounted_cost = baseline_cost * 0.5
                savings = baseline_cost - discounted_cost

                # Update usage
                res.usage.estimated_cost_usd = discounted_cost
                job.cost_saved_usd = round(savings, 6)
                job.response = res
                job.status = "completed"

                self._total_jobs_processed += 1
                self._total_batch_savings_usd += savings
                self._completed_jobs[job.id] = job
            except Exception as exc:
                job.status = "failed"
                job.error = str(exc)
                self._completed_jobs[job.id] = job
            return job

        return await asyncio.gather(*(run_single_job(j) for j in jobs_to_process))

    def get_queue_status(self) -> Dict[str, Any]:
        """Return status of pending queue and batch metrics."""
        return {
            "queued_jobs_count": len(self._queue),
            "completed_jobs_count": len(self._completed_jobs),
            "total_jobs_processed": self._total_jobs_processed,
            "total_batch_savings_usd": round(self._total_batch_savings_usd, 6),
            "pending_job_ids": [j.id for j in self._queue],
        }

    def get_job(self, job_id: str) -> Optional[BatchJob]:
        """Lookup job by ID."""
        for j in self._queue:
            if j.id == job_id:
                return j
        return self._completed_jobs.get(job_id)
