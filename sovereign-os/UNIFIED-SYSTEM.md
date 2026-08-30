# UNIFIED SYSTEM — Sovereign OS v30 + Octo Harness — ONE SOURCE OF TRUTH

> This is the single entry point that makes everything one. Read this first.
> It resolves the split sources of truth, merges the best of both systems, and fixes the cross-checked drift.
> Supersedes the "two separate systems" mental model. There is now ONE system with two layers:
> **Governance (v30 store)** + **Execution (Octo Harness runtime)**.

## 1. Naming resolution (kill the "v1.0 vs v30" split)
| Old name | New unified name |
|---|---|
| "Sovereign OS Kit v1.0" (docs 00–09) | **Sovereign OS v30 — design layer** (retained as reference; not the live truth) |
| "Sovereign Production OS v30" (`sovereign-os/`) | **Sovereign OS v30 — governance layer** (THE source of truth) |
| "Octo Harness" (`src/octo_harness`, `graph/*.yaml`) | **Sovereign OS v30 — execution/runtime layer** (working code + machine state) |
| "Azeez Jr. Chief of Staff" / 14 specialists | **5 specialized operators** (STRATEGIC, SOFTWARE, PRODUCT-CONTENT, OPS, CRITIC) + the runtime's mechanical roles |

**Rule:** there is one system. `sovereign-os/` is the human source of truth (C2). `src/octo_harness` + `graph/*.yaml` are the machine that executes it. Neither is independent; together they are whole.

## 2. Authority / source-of-truth precedence (resolve the conflict)
When two files disagree, this order wins:
1. `sovereign-os/CONSTITUTION.md` — immutable.
2. `sovereign-os/STATE-PACK.md` — the live state (rewritten weekly).
3. `sovereign-os/DECISIONS.md` — append-only; latest explicit supersede wins (P6).
4. `sovereign-os/PRINCIPLES.md` — current initiative principles.
5. `graph/*.yaml` — **machine-readable state** only (what the runtime tracks), never the place human decisions are made.
6. Existing `00–09` + `bundles/*.md` — **reference/design** only; regenerate from source, do not hand-edit.

**Fix applied:** the orchestrator-platform contradiction — the graph said Chief of Staff runs on `grok` while platform adapters say ChatGPT. Resolution: the 5 operators are **platform-agnostic roles**, not bound to one provider. The runtime routes each operator's work across the best available provider via the Octo Harness router. Provider choice is a tactic (routing config), not a role identity.

## 3. One architecture (both layers)
```
                PRINCIPAL (human) — sole authority (C1)
                         │
              ┌──────────▼──────────┐
              │  GOVERNANCE LAYER   │  sovereign-os/  (files = truth)
              │  State Pack + 5     │
              │  operators +        │
              │  playbooks +        │
              │  decisions + golden │
              └──────────┬──────────┘
                         │ accepted work
              ┌──────────▼──────────┐
              │  EXECUTION LAYER    │  src/octo_harness/ + graph/*.yaml
              │  Octo Harness router│  (circuit breakers, fallback,
              │  + coworkers +      │   budget, guardrails, TOON)
              │  platform adapters  │
              └──────────┬──────────┘
                         ▼
                  delivery / publish (human-approved, A2+)
```

## 4. Best-of-both selection (what survives)
### From v30 (governance — KEEP as spine)
State Pack · 5 specialized operators · append-only decisions · freeze/huge-problems · golden standard · weekly audit · evolution/change-control · 7-year horizon.

### From v1.0/Octo Harness (execution — KEEP as machinery)
- **Autonomy tiers A0–A4** → folded into OPS/approval gates (complements C1).
- **$50/mo budget + ICE scoring + model tiering + batch/caching** → `PLAYBOOKS/OPERATIONS.md`.
- **Evidence contract** (EVIDENCE & VERIFICATION block) → the v30 META footer's factual spine.
- **Mission Graph `graph/*.yaml`** → machine state; reads/writes via the runtime, human-approved (A2+).
- **Guardrails** (prompt injection, secret scrubbing, SSRF) → enforced by the runtime on every call.
- **Multi-provider fallback + circuit breakers** → the concrete vendor-independence that satisfies C5/P2/P3.
- **TOON compression + context caching** → cost machinery under the $50 cap.

### From neither — rejected
- God-agent "Chief of Staff" (violates C3). → replaced by 5 operators.
- Unbounded specialist overlap → replaced by one non-overlapping role map.
- Split source-of-truth → resolved by §2 precedence.

## 5. Cross-check findings + fixes (this session)
| # | Finding | Severity | Fix (applied in unified layer) |
|---|---|---|---|
| C1 | Chief of Staff platform: graph=grok vs adapters=ChatGPT | High | Operators are provider-agnostic; routing is config (§2, §3) |
| C2 | `REVIEW-AND-MERGE.md` G1 says header "says 12"; file now lists 14 | Low | Accept 14; supersede G1 via this doc + decision |
| C3 | 14 specialists overlap; no map to 5 operators | High | `OPERATORS/SPECIALIST-MAP.md` assigns each to exactly one operator |
| C4 | Three sources of truth with no entry point | High | This file is THE entry point; §2 precedence |
| C5 | v1.0 lacks State Pack / freeze / golden / audit / evolution | Medium | Provided by v30 playbooks + checklists |
| C6 | `bundles/*.md` hand-editable → drift | Medium | Rule: regenerate via `08_roster_engine.py`, never hand-edit |
| C7 | `REVIEW-AND-MERGE` branch target is a different branch (`arena/01a039d4…`) | Info | Current session branch `arena/01a05282…` is the live line |

## 6. What "one system" means operationally
- **One daily loop** (`CHECKLISTS/DAILY-CHEAT-SHEET.md`): one State Pack, one operator, one artifact, CRITIC, file it.
- **One weekly audit** (`CHECKLISTS/WEEKLY-AUDIT-CHECKLIST.md`): CRITIC + OPS over both layers.
- **One operator per task**: use `OPERATORS/SPECIALIST-MAP.md` to route a request to exactly one operator; the runtime picks the provider.
- **One cost reality**: $50/mo enforced by the runtime's cost tracker; ICE used by STRATEGIC to prioritize.
- **One memory**: files only. State Pack (human) + Mission Graph (machine). Chat is disposable.

## 7. Rebuild-in-one-day test (C5/C6, H7 gate)
To rebuild the whole OS on a new tool:
1. `git clone` this repo (files ARE the system).
2. Read `sovereign-os/UNIFIED-SYSTEM.md` + `CONSTITUTION.md`.
3. Paste the 5 `OPERATORS/*.md` prompts into new chats.
4. Fill `STATE-PACK.md`.
5. `pip install -e '.[dev]'` then `octo-harness serve` for the runtime.
6. Run Workflow A on the current initiative.
Done in a day. No chat history required.

---
**META**
- OS: v30 | Operator: STRATEGIC (consolidation) | Artifact type: unified system / single source of truth
- Date: 2026-08-30 | Confidence: high | Expiry: review at each weekly audit
- Assumptions: existing files remain as reference; no live keys in sandbox
- Principles used: C1, C2, C3, C5, C6, C8
- Sovereignty risks: none — nothing deleted; precedence is explicit and reversible
- Failure modes: operators read old 00–09 as live truth instead of reference
- What would make this false: user wants a literal rewrite deleting the runtime
- Next human action: accept unification (D-20260830-04)
- Next operator: OPS (finalize OPERATIONS.md)

**HANDOFF**
- From: STRATEGIC | To: user / OPS
- Original goal: consolidate scattered systems into one resilient whole
- Delivered: single source of truth, precedence, best-of-both, cross-check fixes
- Not delivered: a real product/customer initiative (user's call)
- Assumptions: merging > rewriting; existing code preserved
- Open questions: which initiative first uses the unified system?
- Recommended next prompt: read OPERATORS/SPECIALIST-MAP.md + PLAYBOOKS/OPERATIONS.md
- Do-not-violate: never delete working runtime; 5 operators stay specialized; provider is config, not identity
- Freeze recommended? no
