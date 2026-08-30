# PLAYBOOK: OPERATIONS — best of v1.0 folded into v30 — v30

> The concrete operational machinery inherited from Sovereign OS Kit v1.0 / Octo Harness,
> integrated into the v30 governance spine. These are the "how to run it" rules that make the
> governance real and the budget hold. Source files: `00–09`, `graph/*.yaml`, `src/octo_harness`.

## 1. Budget & priority (enforce the $50/mo reality)
- **Hard cap:** $50.00 USD/month (~$1.67/day). The runtime's `cost_tracker` enforces it; STRATEGIC/ICE uses it to prioritize.
- **ICE score:** `(Impact × Confidence × Ease) / (Cost + 0.1)`.
  - High (>100): do now. Medium (40–100): batch for 50% discount. Low (<40): park.
- **Model tiering:** never use frontier models for formatting/scraping/restructuring. Route those to cheap models or local.
- **Context caching + TOON:** static governance prefix (Constitution + State Pack) stays at top of prompts to trigger provider caching; TOON compresses repetitive JSON.

## 2. Autonomy tiers (complement C1)
| Tier | Permission | Escalation |
|---|---|---|
| A0 | Informational (read/report) | always |
| A1 | Draft/Propose (human executes) | any state mutation |
| A2 | Approval gate (default) | side effects, writes, API calls |
| A3 | Autonomous bounded (<$0.50, reversible) | breach or irreversibility |
| A4 | Unrestricted — **forbidden** except sandbox tests | any external boundary |

Default posture: **A2**. Human is the sole decider (C1). A3 is rare and reversible only.

## 3. Evidence contract (the v30 META's factual spine)
Every output must carry verified grounding. Unified footer order:
`META` (OS/operator/date/confidence/expiry/assumptions) **→** `EVIDENCE & VERIFICATION` (sources, confidence 0.0–1.0, tokens+cost, tier) **→** `HANDOFF`.
No evidence = unverified = reject (matches v1.0 Evidence-first + v30 C2/C4).

## 4. Runtime operating rules (from the harness)
- **Fallback cascades + circuit breakers:** CLOSED→OPEN→HALF_OPEN; zero dropped requests; multi-provider.
- **Guardrails:** prompt-injection scan, secret scrubbing (sk-, xai-, ant-, AKIA, ghp_, keys), SSRF/IP blocking — enforced on every call.
- **Idempotency + retries:** request IDs, replay-safe logs.
- **Health:** `/health` reports adapter + circuit state.
- **Secrets:** env vars only; `.env` gitignored; never in markdown/git/graph.

## 5. Mission Graph as machine state
`graph/*.yaml` (projects/goals/agents/edges) is the **machine-readable** state, written by the runtime under human approval (A2+). It is NOT the place human decisions are made — `sovereign-os/DECISIONS.md` is. Cross-reference: goals map to the active initiative's 90-day done.

## 6. Unified daily/weekly cadence
- **Daily (25 min):** update State Pack → one operator → one artifact → CRITIC if external/code → file. (`CHECKLISTS/DAILY-CHEAT-SHEET.md`)
- **Weekly (40 min):** CRITIC + OPS audit over BOTH governance and runtime; check budget, evidence, drift, freeze. (`CHECKLISTS/WEEKLY-AUDIT-CHECKLIST.md`)

## 7. Operations failure paths
- Budget breached → runtime blocks routed calls + alerts human (A2).
- All providers down → 503 + last-good cache; OPS runs fallback path (P3).
- Drift signals → freeze (see `FREEZE-CHECKLIST.md`), show a golden example, re-certify.

---
**META**
- OS: v30 | Operator: OPS | Artifact type: operations playbook (unified machinery)
- Date: 2026-08-30 | Confidence: high | Expiry: review with weekly audit
- Assumptions: runtime code is source (93/93 tests pass); real keys are human-step
- Principles used: C1, C2, C5, C6, C8
- Sovereignty risks: none — A4 forbidden, A3 bounded
- Failure modes: treating mission graph as the human truth instead of DECISIONS.md
- What would make this false: budget or tier rules change (via EVOLUTION)
- Next human action: adopt; run daily loop
- Next operator: CRITIC
