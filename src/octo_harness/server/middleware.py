"""
Middleware components for ASGI / FastAPI control plane.
"""

from __future__ import annotations

import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class OctoSecurityAndTracingMiddleware(BaseHTTPMiddleware):
    """
    Handles request tracing, latency tracking, CORS headers, and optional API key auth.
    """

    def __init__(self, app, api_key: str | None = None):
        super().__init__(app)
        self.api_key = api_key

    async def dispatch(self, request: Request, call_next) -> Response:
        req_id = request.headers.get("X-Request-ID") or f"req_{uuid.uuid4().hex[:10]}"
        start_time = time.time()

        # Public paths exempt from authentication
        public_paths = {"/", "/health", "/ready", "/pulse", "/metrics", "/favicon.ico", "/static"}
        is_public = any(request.url.path == p or request.url.path.startswith("/static/") for p in public_paths)

        if self.api_key and not is_public:
            auth_header = request.headers.get("Authorization", "")
            token = auth_header.replace("Bearer ", "").strip()
            if token != self.api_key:
                return JSONResponse(
                    status_code=401,
                    content={"error": {"message": "Invalid or missing API key", "type": "authentication_error"}},
                    headers={"X-Request-ID": req_id},
                )

        try:
            response = await call_next(request)
            elapsed_ms = round((time.time() - start_time) * 1000.0, 2)
            response.headers["X-Request-ID"] = req_id
            response.headers["X-Response-Time-Ms"] = str(elapsed_ms)
            return response

        except Exception as exc:
            elapsed_ms = round((time.time() - start_time) * 1000.0, 2)
            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "message": str(exc),
                        "type": "internal_server_error",
                    }
                },
                headers={"X-Request-ID": req_id, "X-Response-Time-Ms": str(elapsed_ms)},
            )
