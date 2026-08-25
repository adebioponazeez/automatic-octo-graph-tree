"""
FastAPI application entrypoint for Octo Harness Server.
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from octo_harness.config import Settings, get_settings
from octo_harness.router.engine import RouterEngine
from octo_harness.server.middleware import OctoSecurityAndTracingMiddleware
from octo_harness.server.routes import create_router

STATIC_DIR = Path(__file__).parent / "static"


def create_app(settings: Settings | None = None, engine: RouterEngine | None = None) -> FastAPI:
    """Factory creating configured FastAPI app with Octo Harness router engine."""
    app_settings = settings or get_settings()
    router_engine = engine or RouterEngine(settings=app_settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup hook
        yield
        # Shutdown hook

    app = FastAPI(
        title=app_settings.app_name,
        version=app_settings.version,
        description="Unified Multi-Model Router & Cowork Harness for xAI Grok, OpenAI ChatGPT, and Anthropic Claude",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Tracing and Auth
    app.add_middleware(
        OctoSecurityAndTracingMiddleware,
        api_key=app_settings.server_api_key,
    )

    # Mount static assets
    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

        @app.get("/", include_in_schema=False)
        async def root_ui():
            index_path = STATIC_DIR / "index.html"
            return FileResponse(str(index_path))

    # Mount API routes
    api_router = create_router(router_engine)
    app.include_router(api_router)

    # Attach router engine instance for direct access in tests
    app.state.engine = router_engine

    return app


# Default app instance for ASGI runners (uvicorn, gunicorn, granian)
app = create_app()
