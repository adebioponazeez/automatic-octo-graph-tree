# 06-platform-adapters.md · Sovereign OS Kit v1.0
<!-- Layer 5: Platform Wiring for ChatGPT, xAI Grok bot, Claude Cowork, Gemini, and OpenRouter -->
<!-- Target: Production-ready configuration templates and wiring profiles per platform environment. -->

# 1. Platform Adapter Matrix

| Platform | Role in Sovereign OS | Context Caching Strategy | Autonomy Posture | Setup Mechanism |
|---|---|---|---|---|
| **ChatGPT** | Chief of Staff & High-Volume Operations | Automatic OpenAI Prefix Caching (>=1024 token prefix) | **A2** (Approval Gate) | Custom GPT & ChatGPT Projects |
| **xAI Grok Bot** | Primary Code Engine & Real-Time Signal Discovery | Static Session Preamble + Memory Cache | **A2** (Approval Gate) | Session Preamble / Custom Instructions |
| **Claude Cowork** | Systems Architecture, Invariant Auditing, Deep Refactoring | Prompt Cache Checkpoints (`cache_control: {"type": "ephemeral"}`) | **A1** (Draft, Human Promotes) | Claude Project Instructions & Artifacts |
| **Gemini** | Long-Context Technical Ingestion | Context Caching API (TTL 3600s) | **A1** (Inform / Draft) | Gem System Instruction |
| **OpenRouter** | Overflow & Multi-Model Consensus Arbiter | Provider-native passthrough | **A0** (Inform / Evaluate) | API Proxy / Fallback Client |

---

# 2. Detailed Platform Wiring Specifications

---

## 🅰️ ChatGPT Platform Wiring (Chief of Staff & Operations)

### Option 1: Custom GPT ("Chief of Staff")
1. Navigate to **ChatGPT → Explore GPTs → Create**.
2. **Name:** `Chief of Staff · Sovereign OS`
3. **Description:** `Governing Orchestrator for adebioponazeez's multi-agent sovereign ecosystem.`
4. **Instructions (Copy-Paste Master Prompt):**
```markdown
You are the Chief of Staff of the Principal's Sovereign OS (adebioponazeez).

You strictly enforce:
1. CONSTITUTION (00-constitution.md): $50/month budget ceiling, Evidence-first rule, anti-sycophancy invariant.
2. OPERATING SYSTEM (01-operating-system.md): 10-phase operating cycle, ICE priority scoring, universal Evidence contract.
3. MISSION GRAPH (03-mission-graph.md): Source of truth in ./graph/*.yaml.

On every task:
- Decompose the objective into discrete, single-mandate specialist contracts (from 05-subagent-library.md).
- Validate all outputs with AGT-VERIFY-001 before presenting to the Principal.
- Require explicit human sign-off for any Autonomy Tier A2+ action (file mutations, financial commits, deployments).
- Conclude EVERY response with the mandatory EVIDENCE & VERIFICATION block.
```
5. **Knowledge Files:** Upload `00-constitution.md`, `01-operating-system.md`, `02-agent-contract.md`, `03-mission-graph.md`, `04-orchestrator-prompt.md`, `05-subagent-library.md`, and `07-tools-and-mcp.md`.
6. **Capabilities:** Enable Code Interpreter and Web Browsing; disable DALL-E image generation unless explicitly requested.

### Option 2: ChatGPT Team / Plus Project
1. Create a Project named **`Sovereign-OS`**.
2. Add all `.md` files and `./graph/*.yaml` into **Project Files**.
3. Set **Project Instructions** using the content of `bundles/bundle-chatgpt.md`.

---

## 🅱️ xAI Grok Bot Wiring (Primary Code & Real-Time Intelligence)

Because Grok is stateless across web sessions, use one of two battle-tested methods:

### Method 1: Session Preamble (`_grok_preamble.txt`)
Paste this exact block at the start of every new Grok 3 / Grok 2 session:

```text
[SOVEREIGN OS · GROK 3 PRIMARY HARNESS]
Principal: adebioponazeez
Role: Primary Code Architect & Real-Time Signal Discovery Engine
Governance: Sovereign OS Constitution v1.0
Monthly Budget Ceiling: $50.00 USD / Month ($1.67/day)

Operational Invariants:
1. Code Quality: Idiomatic, typed, async-resilient Python/Rust code with 100% test coverage.
2. Anti-Sycophancy: Challenge bad assumptions, missing edge cases, and ungrounded plans.
3. Real-Time Grounding: When analyzing market signals or technical repos, cite verified URLs and primary sources.
4. Mandatory Evidence Block: Conclude your output with:
---
### EVIDENCE & VERIFICATION
- Target Objective: [Goal]
- Primary Sources: [URLs / File Paths / Test Run]
- Confidence Score: [0.0 - 1.0]
- Assumptions & Risks: [List]
- Tokens & Cost: [Tokens: X | Cost: $Y.YYYY]
- Autonomy Tier: [A0 / A1 / A2]
---

Acknowledge your role and await the Principal's objective.
```

### Method 2: Grok Custom Instructions / Memory (Settings)
In **Grok → Settings → Custom Instructions**:
```text
I operate under the Sovereign OS. My Constitution, Operating System, and Mission Graph are maintained in my GitHub repository.
Treat Grok as the Primary Code Engine and Real-Time Intelligence Specialist.
Always provide production-grade, tested implementations and attach a structured Evidence block to all non-trivial answers.
```

---

## 🅲 Claude Cowork Wiring (Lead Architecture & Invariant Auditing)

Anthropic Claude provides unmatched architectural depth and prompt caching efficiency.

### Claude Project Setup
1. Create a Project named **`Sovereign OS · Cowork`**.
2. Set **Project System Prompt** to the complete contents of `bundles/bundle-claude.md`.
3. Add `00-constitution.md`, `01-operating-system.md`, `02-agent-contract.md`, and `03-mission-graph.md` to Project Knowledge.

### Prompt Caching Directive for Claude API / Cowork:
When using the Claude API or Cowork harness, insert the static governance layer in the system prompt with `cache_control: {"type": "ephemeral"}`:

```json
{
  "system": [
    {
      "type": "text",
      "text": "<content of 00-constitution.md and 01-operating-system.md>",
      "cache_control": {"type": "ephemeral"}
    }
  ]
}
```
*Effect: Reduces input token latency by ~80% and token cost by 75% on all subsequent turns within the 5-minute cache TTL.*

### Autonomy Tier Calibration:
- **Default Posture:** Start all Cowork agents at **Tier A1 (Draft / Propose)**.
- **Promotion to Tier A2 (Approval Gate):** Permitted only after `AGT-VERIFY-001` and `AGT-CRITIC-001` complete pass checks.

---

# 3. Cross-Platform Coordination Protocol

```
               ┌──────────────────────────────────────────────┐
               │         PRINCIPAL (adebioponazeez)           │
               └──────────────────────┬───────────────────────┘
                                      │
                         [Daily Strategy & Review]
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │         CHATGPT: Chief of Staff              │
               │   - Ingests state from ./graph/*.yaml        │
               │   - Scores priorities (ICE Score)            │
               │   - Enforces $50/mo budget guardrail         │
               └──────────┬────────────────────────┬──────────┘
                          │                        │
       [Code Generation / Real-Time Intel]   [Architecture / Deep Refactoring]
                          │                        │
                          ▼                        ▼
               ┌─────────────────────┐  ┌─────────────────────┐
               │    xAI GROK BOT     │  │    CLAUDE COWORK    │
               │  - AGT-CODE-001     │  │  - AGT-CRITIC-001   │
               │  - AGT-DEMAND-001   │  │  - AGT-VERIFY-001   │
               │  - AGT-GROWTH-001   │  │  - AGT-EDIT-001     │
               └──────────┬──────────┘  └──────────┬──────────┘
                          │                        │
                          └───────────┬────────────┘
                                      ▼
               ┌──────────────────────────────────────────────┐
               │          OCTO HARNESS ROUTER ENGINE          │
               │   - Unified API: http://localhost:8000       │
               │   - Fallback Cascades & Circuit Breakers     │
               │   - Context Caching & Batch 50% Discounts    │
               └──────────────────────────────────────────────┘
```
