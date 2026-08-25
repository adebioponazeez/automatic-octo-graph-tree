# Octo Harness · Grok & ChatGPT Setup and Configuration Guide

This guide details how to configure, calibrate, and operate the **Octo Harness Router Engine** across **xAI Grok**, **OpenAI ChatGPT**, **Anthropic Claude**, and local self-hosted inference models (Ollama / vLLM).

---

## 1. Quick Setup Checklist

1. **Clone and Install**:
   ```bash
   git clone https://github.com/adebioponazeez/automatic-octo-graph-tree.git
   cd automatic-octo-graph-tree
   pip install -e '.[dev]'
   ```

2. **Configure Environment Keys**:
   ```bash
   cp .env.example .env
   # Edit .env with your provider credentials
   ```

3. **Verify Health & Circuits**:
   ```bash
   octo-harness pulse
   ```

4. **Launch Server & Live Web Console**:
   ```bash
   octo-harness serve --port 8000
   # Open http://localhost:8000 in your browser
   ```

---

## 2. Provider Configuration

### A. xAI Grok Configuration

Octo Harness treats **xAI Grok** as the primary frontier engine for reasoning, deep code synthesis, and multi-modal understanding.

- **Obtain API Key**: Visit the [xAI Console](https://console.x.ai/) and generate an API key (`xai-...`).
- **Environment Variables**:
  ```bash
  export GROK_API_KEY="xai-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  export GROK_BASE_URL="https://api.x.ai/v1"
  export GROK_TIMEOUT="30.0"
  export GROK_RPS="30.0"
  ```
- **Supported Grok Models in Catalog**:
  - `grok-3`: Flagship frontier model for multi-step reasoning, mathematical proof, and complex system design.
  - `grok-2-latest`: Fast, highly capable code and general-purpose conversational model.
  - `grok-2-vision-1212`: Multimodal visual extraction and document parsing.
  - `grok-beta`: Experimental preview model.

### B. OpenAI ChatGPT Configuration

OpenAI models serve as high-tier fallback and cost-effective task offloading.

- **Obtain API Key**: Visit [OpenAI API Keys](https://platform.openai.com/api-keys) and generate an API key (`sk-...`).
- **Environment Variables**:
  ```bash
  export OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  export OPENAI_BASE_URL="https://api.openai.com/v1"
  export OPENAI_TIMEOUT="30.0"
  ```
- **Supported OpenAI Models in Catalog**:
  - `gpt-4o`: Flagship omni-model for code, vision, and structured JSON output.
  - `gpt-4o-mini`: Ultra-fast, low-cost model for high-volume chat and classification.
  - `o3-mini`: Specialized deep reasoning model for STEM and algorithmic logic.

### C. Anthropic Claude Configuration

- **Obtain API Key**: Visit [Anthropic Console](https://console.anthropic.com/) and generate an API key (`ant-...`).
- **Environment Variables**:
  ```bash
  export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  export ANTHROPIC_BASE_URL="https://api.anthropic.com/v1"
  ```
- **Supported Claude Models in Catalog**:
  - `claude-3-5-sonnet-20241022`: Frontier coding and nuanced synthesis.
  - `claude-3-5-haiku-20241022`: Rapid classification and summarization.

### D. OpenRouter Configuration (Kimi K3, DeepSeek R1/V3, Qwen 2.5 Coder, Llama 3.3)

OpenRouter provides access to **Moonshot Kimi K3**, **DeepSeek R1**, **Qwen 2.5 Coder**, and top open-weight models at significant cost savings ($0.14 - $0.55 / 1M tokens).

- **Obtain API Key**: Visit [OpenRouter Keys](https://openrouter.ai/keys) and generate an API key (`sk-or-v1-...`).
- **Environment Variables**:
  ```bash
  export OPENROUTER_API_KEY="sk-or-v1-xxxxxxxxxxxxxxxxxxxx"
  export OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"
  ```
- **Supported OpenRouter Models**:
  - `moonshotai/kimi-k3`: 200,000 token context window with deep Chinese/English document reasoning.
  - `deepseek/deepseek-r1`: Open reasoning and mathematical derivation frontier model.
  - `deepseek/deepseek-chat`: DeepSeek V3 general intelligence at $0.14/1M tokens.
  - `qwen/qwen-2.5-coder-32b-instruct`: State-of-the-art open code generation model.
  - `meta-llama/llama-3.3-70b-instruct`: 70B parameter open frontier intelligence.

### E. Local & Offline Mode (Zero Token Spend)

When running in CI/CD, local air-gapped environments, or developing without paid API credits:

- **Local Ollama / vLLM**:
  ```bash
  export LOCAL_BASE_URL="http://localhost:11434/v1"
  export LOCAL_API_KEY="local"
  ```
- **Deterministic Mock Mode**:
  ```bash
  export OCTO_MOCK_MODE=true
  # Or pass --mock flag to CLI
  octo-harness --mock route "Explain Python generators"
  ```

---

## 3. Router Engine Policies & Fallbacks

Octo Harness dynamically routes prompts based on detected intent, cost targets, and live provider health:

| Strategy | Primary Model | Fallback Cascade Sequence | Ideal Use Case |
|---|---|---|---|
| `grok_primary` | `grok-3` / `grok-2-latest` | `gpt-4o` → `claude-3-5-sonnet` → `gpt-4o-mini` → `mock` | Default production routing |
| `quality_first` | Highest benchmark model | `claude-3-5-sonnet` / `grok-3` → `gpt-4o` → `o3-mini` | Complex architecture & security audits |
| `cost_optimized` | Lowest cost meeting threshold | `gpt-4o-mini` / `claude-3-5-haiku` → `grok-2-latest` | High-throughput batch processing |
| `latency_optimized`| Lowest historical latency | `gpt-4o-mini` → `grok-2-latest` → `claude-3-5-haiku` | Real-time interactive UI agents |
| `fallback_cascade`| User-specified list | Custom array of model IDs | Exact deterministic fallback chains |

---

## 4. Circuit Breakers & Fault Tolerance

Each upstream model and provider is wrapped with an active circuit breaker:

- **State Transitions**:
  - `CLOSED`: Normal operation. Consecutive failures increment error count.
  - `OPEN`: After 5 consecutive failures, the circuit trips OPEN. Requests bypass the degraded provider immediately without waiting for timeouts.
  - `HALF_OPEN`: After a 30-second recovery timeout, a probe request tests provider recovery. If successful, resets to `CLOSED`.

- **Configuration**:
  ```bash
  export CIRCUIT_BREAKER_FAIL_MAX=5
  export CIRCUIT_BREAKER_RESET_TIMEOUT=30.0
  ```

---

## 5. Multi-Agent Cowork DAG Execution

The Cowork framework coordinates multiple specialized agent personas across a Directed Acyclic Graph (DAG):

1. **Planner Agent** (`quality_first`): Decomposes objectives into discrete tasks with dependencies.
2. **Coder Agent** (`grok_primary`): Generates idiomatic, typed, and tested code.
3. **Critic Agent** (`quality_first`): Rigorous adversarial review for edge cases and security.
4. **Synthesizer Agent** (`cost_optimized`): Consolidates findings and outputs final deliverables.

Run from CLI:
```bash
octo-harness cowork "Build an automated cache warmer and Prometheus metrics exporter"
```

---

## 6. Multi-Model Debate & Consensus

Run parallel cross-examination across Grok, ChatGPT, and Claude:

```bash
octo-harness consensus "Compare memory safety in Rust vs modern C++23"
```

The router engine will:
1. Dispatch parallel queries to `grok-3`, `gpt-4o`, and `claude-3-5-sonnet`.
2. Compute agreement scores.
3. Use an arbiter model to synthesize a single verified consensus verdict.

---

## 7. Drop-In OpenAI SDK Integration

Because Octo Harness exposes standard `/v1/chat/completions` and `/v1/models` endpoints, you can use any existing OpenAI SDK without code changes:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="local-development-key",
)

response = client.chat.completions.create(
    model="grok-3",
    messages=[
        {"role": "system", "content": "You are an expert engineer."},
        {"role": "user", "content": "Write a high-performance LRU cache in Python."},
    ],
    extra_body={"strategy": "grok_primary"}
)

print(response.choices[0].message.content)
```
