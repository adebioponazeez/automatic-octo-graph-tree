# Octo Harness · Cowork & Grok AI Router Engine

[![Python 3.9+](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-93%2F93%20passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-verified-green.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A high-throughput, fault-tolerant **Multi-Model AI Router & Multi-Agent Cowork Harness** designed for **xAI Grok** (Grok 3, Grok 2, Grok Vision), **OpenAI ChatGPT** (GPT-4o, GPT-4o-mini, o3-mini), **Anthropic Claude** (Claude 3.5 Sonnet/Haiku), and **Local Models** (Ollama, vLLM).

> ## 🎯 One System
> This repo is **ONE system**: the Octo Harness runtime (below) is the **execution layer**, and
> `sovereign-os/` is the **governance layer** (Constitution, State Pack, 5 operators, playbooks, decisions).
> **Start at [`sovereign-os/UNIFIED-SYSTEM.md`](sovereign-os/UNIFIED-SYSTEM.md)** — the single source of truth
> that merges both into one resilient, 7-year system. See also the seven-horizon recheck
> (`sovereign-os/AUDITS/2026-08-30-seven-horizon-recheck.md`).

---

## Key Features

- **Intelligent Prompt Intent Routing**: Heuristic and semantic classifier detecting code, deep reasoning, mathematical logic, structured JSON schema, extraction, and creative tasks.
- **Resilient Fallback Cascades**: Automatic failover (e.g., `Grok-3` → `GPT-4o` → `Claude 3.5 Sonnet` → `Local / Mock`) with zero request drops.
- **Per-Provider Circuit Breakers**: `CLOSED` → `OPEN` → `HALF_OPEN` state machine preventing cascading failures and eliminating latency stalls during upstream outages.
- **Token Bucket Rate Limiting & Concurrency Locks**: Burst-tolerant RPS protection and concurrency gates per upstream provider.
- **Dynamic Cost Tracker & Budget Guardrail**: Real-time USD token cost computation with configurable hard budget caps.
- **Multi-Agent Cowork DAG Framework**: Directed Acyclic Graph execution engine with role-separated agents (**Planner**, **Coder**, **Critic**, **Synthesizer**, **Safety Auditor**) and shared blackboard memory.
- **Multi-Model Debate & Consensus**: Parallel query cross-examination between Grok, ChatGPT, and Claude with automated consensus arbitration.
- **OpenAI-Compatible Proxy Endpoint**: Drop-in replacement for `https://api.openai.com/v1/chat/completions` and `/v1/models`.
- **Embedded Operator Web Dashboard**: Real-time routing visualization, provider liveness metrics, circuit states, and interactive prompt testing console.
- **Zero-Dependency Mock Mode**: Deterministic offline execution for CI/CD gates and zero-token test runs.

---

## Architecture Overview

```
                          ┌────────────────────────┐
                          │   Client Application   │
                          │ (OpenAI SDK / Web / CLI│
                          └───────────┬────────────┘
                                      │
                         HTTP / CLI / Python API
                                      │
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │            OCTO HARNESS ROUTER ENGINE            │
             │                                                  │
             │  ┌────────────────────┐   ┌───────────────────┐  │
             │  │ Intent Classifier  │   │  Routing Rules    │  │
             │  │ (Code, Math, JSON) │   │ (Grok, Cost, Lat) │  │
             │  └─────────┬──────────┘   └─────────┬─────────┘  │
             │            └───────────┬────────────┘            │
             │                        ▼                         │
             │  ┌────────────────────────────────────────────┐  │
             │  │       Circuit Breaker & Rate Limiter       │  │
             │  └─────────────────────┬──────────────────────┘  │
             │                        │                         │
             │  ┌─────────────────────┴──────────────────────┐  │
             │  │              Fallback Cascade              │  │
             │  └─┬──────────────┬──────────────┬──────────┬─┘  │
             └────┼──────────────┼──────────────┼──────────┼────┘
                  │              │              │          │
                  ▼              ▼              ▼          ▼
            ┌───────────┐  ┌───────────┐  ┌──────────┐  ┌─────────┐
            │ xAI Grok  │  │  OpenAI   │  │Anthropic │  │ Local / │
            │ (Grok 3)  │  │ (GPT-4o)  │  │ (Claude) │  │ Ollama  │
            └───────────┘  └───────────┘  └──────────┘  └─────────┘
```

---

## Quick Start

### 1. Installation

Requires Python 3.9+.

```bash
# Clone the repository
git clone https://github.com/adebioponazeez/automatic-octo-graph-tree.git
cd automatic-octo-graph-tree

# Install in editable mode with development dependencies
pip install -e '.[dev]'
```

### 2. Configuration

Copy the example environment file and add your provider keys:

```bash
cp .env.example .env
```

Annotated sample:
```bash
GROK_API_KEY=xai-your-grok-key
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=ant-your-anthropic-key
BUDGET_LIMIT_USD=100.00
DEFAULT_STRATEGY=grok_primary
```

*(See [SETUP-GROK-CHATGPT.md](SETUP-GROK-CHATGPT.md) for full provider setup instructions).*

### 3. Launch Operator Server & Web Console

```bash
octo-harness serve --port 8000
```
Open **`http://localhost:8000`** in your browser to access the live dashboard, provider monitors, routing playground, and Cowork DAG launcher.

---

## CLI Usage

Octo Harness comes with a rich command-line tool `octo-harness` (also aliased as `grok-harness`):

```bash
# 1. Route a prompt with Grok Primary strategy
octo-harness route "Write an async Python event loop" --strategy grok_primary

# 2. Inspect live system pulse & budget usage
octo-harness pulse

# 3. List catalog models with capabilities and pricing
octo-harness models

# 4. Run a 4-stage Multi-Agent Cowork DAG
octo-harness cowork "Build a Redis rate-limiter with exponential backoff"

# 5. Run Multi-Model Cross-Examination & Consensus
octo-harness consensus "Compare ASGI vs WSGI for high-throughput LLM streaming"

# 6. Stream tokens to stdout
octo-harness route "Explain Raft consensus protocol" --stream

# 7. Run in deterministic offline mock mode (zero cost)
octo-harness --mock route "Test prompt"
```

---

## Python API Usage

### Basic Routing

```python
import asyncio
from octo_harness import ChatMessage, ChatRole, CompletionRequest, RouterEngine, RoutingStrategy

async def run():
    engine = RouterEngine()

    req = CompletionRequest(
        messages=[
            ChatMessage(role=ChatRole.USER, content="Write a Python script to parse JSON streams")
        ],
        strategy=RoutingStrategy.GROK_PRIMARY,
    )

    response = await engine.complete(req)
    print(f"Model: {response.model} ({response.provider.value})")
    print(f"Latency: {response.latency_ms}ms | Cost: ${response.usage.estimated_cost_usd:.5f}")
    print(f"Content:\n{response.content}")

if __name__ == "__main__":
    asyncio.run(run())
```

### Multi-Agent Cowork Workflow DAG

```python
import asyncio
from octo_harness import RouterEngine
from octo_harness.cowork.graph import CoworkGraph

async def run_swarm():
    engine = RouterEngine()
    pipeline = CoworkGraph.create_standard_pipeline(
        router=engine,
        objective="Design an idempotent webhook delivery worker in Python"
    )

    result = await pipeline.execute("Design an idempotent webhook delivery worker in Python")
    print(f"Workflow status: {result['status']}")
    print(f"Synthesized deliverable:\n{result['final_deliverable']}")

if __name__ == "__main__":
    asyncio.run(run_swarm())
```

---

## HTTP REST & OpenAI Proxy Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Live Operator Web Console |
| `GET` | `/health` | Fast O(1) liveness probe |
| `GET` | `/ready` | Readiness check (validates catalog & providers) |
| `GET` | `/pulse` | Full telemetry pulse: providers, circuits, token costs |
| `GET` | `/v1/models` | OpenAI-compatible models listing |
| `POST` | `/v1/chat/completions`| OpenAI-compatible proxy with dynamic routing & streaming |
| `POST` | `/v1/route` | Route inspection endpoint (without execution) |
| `POST` | `/cowork/run` | Execute multi-agent Cowork DAG |
| `POST` | `/cowork/consensus` | Run multi-model debate & consensus arbitration |
| `GET` | `/metrics` | Prometheus metrics and JSON telemetry summary |

---

## Testing & Quality Assurance

Run the comprehensive test suite with 100% passing gates:

```bash
# Run all tests
make test
# Or with pytest directly
python -m pytest -v

# Run with test coverage report
make test-cov
```

---

## Docker Deployment

```bash
# Build and run with Docker Compose
docker compose up --build

# Or build container directly
docker build -t octo-harness:latest .
docker run -p 8000:8000 --env-file .env octo-harness:latest
```

---

## License

MIT License. Developed by [@adebioponazeez](https://github.com/adebioponazeez).
