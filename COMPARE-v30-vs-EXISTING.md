# Comparison: Existing Repo vs Sovereign Production OS v30

> Purpose: map the pre-existing Octo Harness / "Sovereign OS Kit v1.0" to the new v30 canonical store,
> name the gaps, and provide a **phased "phase-change rewrite" roadmap** (incremental, reversible — no big-bang rewrite).
> Nothing here deletes or rewrites existing files; it only plans and references them.

## 1. At a glance

| Concern | Existing repo | v30 canonical store (`sovereign-os/`) |
|---|---|---|
| Source of truth | `./graph/*.yaml` + numbered `.md` docs | `sovereign-os/` files (append-only decisions) |
| Identity framing | "Sovereign OS Kit v1.0", Azeez Jr. Chief of Staff, named subagents (Junior, Ahmed, 14 specialists) | 5 specialized operators (STRATEGIC, SOFTWARE, PRODUCT-CONTENT, OPS, CRITIC) |
| Constitution | `00-constitution.md` (5 invariants, autonomy tiers A0–A4) | `CONSTITUTION.md` (C1–C10) |
| Work loop | 10-phase daily operating cycle | Daily 25-min loop + weekly audit (Workflow B/C) |
| Agent contracts | YAML contract schema, autonomy tiers | Universal Output Contract (`META` + `HANDOFF`) |
| State pack | No equivalent | `STATE-PACK.md` — pasted every serious session |
| Freeze / huge problems | Not explicit | `FREEZE.md` + `HUGE-PROBLEMS.md` (P1–P8) |
| Change control | Not explicit | `EVOLUTION.md` (v30 → v31) |
| Quality standard | Verification Standard, Evidence block | `GOLDEN/` good/bad examples |
| Vendor routing | Octo Harness router (Grok/ChatGPT/Claude/local) | Replaceability + fallback model path (C5, P2/P3) |
| Autonomy tiers | A0–A4 | C1 human sovereignty + approval gates in HANDOFF |

**Shared DNA (keep):** external file truth, no sycophancy, least privilege, human-as-sole-authority, reversible designs, fallback/mock mode, verification over vibes. v30 is largely a re-frame + hardening of the same instincts.

## 2. Mapping table (existing → v30)

| Existing file | Maps to (v30) | Action |
|---|---|---|
| `00-constitution.md` | `CONSTITUTION.md` | Reconcile invariants/tiers into C1–C10 wording; keep tier table as a playbook note |
| `01-operating-system.md` | `PLAYBOOKS/DAILY.md` + `AUDITS/` | Rebuild 10-phase loop as the 25-min daily loop + weekly audit |
| `02-agent-contract.md` | `PLAYBOOKS/HANDOFF.md` (META/HANDOFF) | Fold YAML schema into the universal output contract |
| `03-mission-graph.md` | `INITIATIVES/` + `DECISIONS.md` | Mission Graph → one initiative per file + append-only decisions |
| `04-orchestrator-prompt.md` | `OPERATORS/*` (5 chats) | Split god-agent "Chief of Staff" into 5 single-job operators (C3) |
| `05-subagent-library.md` | `OPERATORS/` + `GOLDEN/` | De-silo the 14 specialists into the 5 operators + golden examples |
| `06-platform-adapters.md` | replaceability (C5), `EVOLUTION.md` | Keep as vendor wiring reference; add fallback path |
| `07-tools-and-mcp.md` | OPS/24/7 rules | Keep as tool registry reference |
| `08_roster_engine.py` | unchanged (build tool) | Keep; feeds operator/playbook bundles |
| `09-openrouter-cognitive-mesh.md` | fallback model path (P2/P3) | Keep as vendor fallback strategy |
| Octo Harness router (`src/`) | software platform | Keep; v30 governs how it's used, not the code itself |

## 3. Gaps in the existing repo that v30 fills
1. No State Pack (no per-session memory paste) → v30 `STATE-PACK.md`.
2. God-agent orchestrator ("Chief of Staff") violates C3 specialization → v30 5 operators.
3. No append-only decision log → v30 `DECISIONS.md`.
4. No freeze / huge-problems protocol → v30 `FREEZE.md` + `HUGE-PROBLEMS.md`.
5. No change-control/versioning for prompts → v30 `EVOLUTION.md`.
6. No golden examples as a drift standard → v30 `GOLDEN/`.
7. No scheduled weekly audit → v30 `AUDITS/`.
8. 14 overlapping specialist prompts → overlap risk; collapse into 5 hard-contract operators.

## 4. Phased "phase-change rewrite" roadmap (incremental, reversible)

Each phase is one small, testable, reversible change — run CRITIC after each. Do NOT do a big-bang rewrite.
Treat these as micro-phases ("60" is a target granularity; the phase list is extendable — each can be split further).

**Phase 0 — Adopt (done now)**
- [x] Scaffold `sovereign-os/` with Constitution, State Pack, 5 operators, playbooks, golden scaffolding.
- [x] Nothing existing deleted; this comparison doc is the migration index.

**Phase 1 — Seed the store**
- [ ] Write a real `STATE-PACK.md` (one initiative).
- [ ] First `DECISIONS.md` entries: "adopt v30 canonical store", "existing repo retained as reference".
- [ ] File this comparison doc in `ARTIFACTS/` or link from README.

**Phase 2 — Constitution reconciliation**
- [ ] Draft mapping `00-constitution.md` invariants (A0–A4, evidence-first) into C1–C10 annotations.
- [ ] Decide: keep autonomy tiers as an OPS playbook note (they complement C1), don't delete.

**Phase 3 — Operatorization (Workflow D)**
- [ ] Map each of the 14 specialists + Chief of Staff into exactly one of the 5 v30 operators. Kill overlaps.
- [ ] Produce per-specialist → per-operator migration notes. Run CRITIC.

**Phase 4 — Contract adoption**
- [ ] Fold the agent YAML schema into `PLAYBOOKS/HANDOFF.md` (META + HANDOFF).
- [ ] Require META+HANDOFF on all new outputs.

**Phase 5 — Cadence**
- [ ] Replace the 10-phase daily loop with the 25-min daily loop + weekly audit.
- [ ] Add audit note template to `AUDITS/`.

**Phase 6 — Golden standard**
- [ ] Capture 1 real good example per operator from existing work → `GOLDEN/good-examples.md`.
- [ ] Capture 1 real bad example per failure family → `GOLDEN/bad-examples.md`.

**Phase 7 — Reliability hardening**
- [ ] Document fallback model path (reuse `09`/router) for P2/P3.
- [ ] Add vendor/data-control inventory (P7).

**Phase 8 — Governance**
- [ ] First EVOLUTION entry; set the 8-line change rule.
- [ ] Decide the autonomy-tier question (keep A0–A4 vs. C1-only) via a dated decision.

**Phase 9 — Operate**
- [ ] Run Workflow B daily loop for one week; weekly audit (Workflow C).
- [ ] Adjust only via EVOLUTION protocol.

> After Phase 9 the system is "live." Further rewrites happen one phase at a time, versioned
> (`OPERATORS/SOFTWARE.v30.md`, `.v31.md`), and never by live prompt edits.

## 5. What NOT to do
- Do not delete existing files "to clean up" — keep them as reference unless a dated decision supersedes them.
- Do not merge all 5 operators back into one god-agent.
- Do not skip the State Pack. Without it, v30 runs in degraded mode.
- Do not tune prompts "by vibe" — only via `EVOLUTION.md`.

---
**META**
- OS: v30
- Operator: STRATEGIC (comparison + roadmap) / this doc
- Artifact type: migration index + phase-change roadmap
- Date: 2026-08-30
- Confidence: medium
- Expiry: re-review at each phase gate
- Assumptions: existing repo remains reference; user drives each phase; "60 phase-change rewrites" = fine-grained incremental phases
- Principles used: C1–C10
- Sovereignty risks: none — nothing deleted or bound
- Failure modes: migration stalls at phase 2 (constitution reconciliation) if user overloaded
- What would make this false: user wants a big-bang rewrite instead
- Next human action: fill `STATE-PACK.md`; choose first initiative
- Next operator: OPS (turn Phase 1–9 into SOPs + freeze conditions)
