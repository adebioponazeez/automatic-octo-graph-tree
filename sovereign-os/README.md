# Sovereign Production OS — v30 Canonical Store

This folder is the **canonical store** for the Sovereign Production OS v30. It is the source of truth. Chats are disposable; files are not.

> Core rule: **If it matters in 90 days, it goes in the store the same day.**

## ⭐ READ THIS FIRST
**`UNIFIED-SYSTEM.md` is the single entry point** that makes this store and the existing
Octo Harness runtime **ONE system**. It defines authority precedence, the best-of-both merge,
and the cross-checked fixes. Start there, then this README.

- `UNIFIED-SYSTEM.md` — one source of truth, authority precedence, best-of-both, cross-check fixes
- `OPERATORS/SPECIALIST-MAP.md` — merges the 14 v1.0 specialists into the 5 operators (no overlap)
- `PLAYBOOKS/OPERATIONS.md` — v1.0 machinery (budget $50/mo, ICE, tiers, evidence, guardrails) folded in
- `AUDITS/2026-08-30-seven-horizon-recheck.md` — the 7-horizon cross-check of both systems

## Structure

```
sovereign-os/
  CONSTITUTION.md          — immutable rules (C1–C10). Amend only via EVOLUTION.
  STATE-PACK.md            — paste at the start of every serious session. Update weekly.
  PRINCIPLES.md            — current initiative governing principles (max 7). Supersede, don't rewrite.
  DECISIONS.md             — append-only decision log. Never silently rewrite history.
  INITIATIVES/             — one initiative per file, with its own 90-day done.
  OPERATORS/               — one prompt per file; copy each into its own chat.
    STRATEGIC.md
    SOFTWARE.md
    PRODUCT-CONTENT.md
    OPS.md
    CRITIC.md
  PLAYBOOKS/
    DAILY.md               — 25-min survival cadence
    HANDOFF.md             — META + HANDOFF output contract
    FREEZE.md              — freeze conditions + 90-min recovery
    HUGE-PROBLEMS.md       — P1–P8 problem catalog + responses
    EVOLUTION.md           — change control (v30 → v31)
  GOLDEN/
    good-examples.md       — index of the standard
    bad-examples.md        — index of known failure modes
    strategic-good.md, architecture-good.md, content-good.md,
    sop-good.md, critic-good.md, bad-generic-strategy.md,
    bad-fake-247.md, bad-hype-copy.md, bad-missing-assumptions.md
  AUDITS/                  — weekly audit notes (Workflow C)
    WEEKLY-AUDIT-TEMPLATE.md
  ARTIFACTS/               — shipped/approved outputs, filed the same day
    README.md (index)
  CHECKLISTS/
    DAILY-CHEAT-SHEET.md        — 25-min survival cadence
    FREEZE-CHECKLIST.md         — freeze conditions + 90-min recovery
    WEEKLY-AUDIT-CHECKLIST.md   — 40-min weekly audit
    7-YEAR-SURVIVAL-CHECKLIST.md — monthly health review
  INITIATIVES/
    INITIATIVE-TEMPLATE.md
  START-NOW.md             — the 60–90 min first-run checklist
```

## Start here (Workflow A — New initiative)
1. Update `STATE-PACK.md` first. **If you skip this, stop.**
2. STRATEGIC → produces principles, 90-day done, trade-off map, Mermaid map, cheapest test, irreversible mistakes, exact files to write.
3. User accepts/amends principles → write into `PRINCIPLES.md` + `DECISIONS.md`.
4. SOFTWARE and/or PRODUCT-CONTENT with the accepted strategy only.
5. CRITIC on the package.
6. User accepts.
7. OPS → SOP + checklist + freeze conditions.
8. Write artifacts into the store the same day.

See also `PLAYBOOKS/WORKFLOWS.md` (Workflows A–D), `START-NOW.md`, and `CHECKLISTS/`.

## Build-out status
| Piece | Status |
|---|---|
| Constitution / State Pack / Principles / Decisions | ✅ |
| 5 operators | ✅ |
| Playbooks (DAILY, HANDOFF, FREEZE, HUGE-PROBLEMS, EVOLUTION, WORKFLOWS) | ✅ |
| Golden examples (5 good + 4 bad) | ✅ |
| Checklists (daily / freeze / weekly audit / 7-year survival) | ✅ |
| Initiative + audit templates | ✅ |
| DECISIONS entries | ✅ (D-20260830-01 … D-20260830-04) |
| **UNIFIED system (one source of truth)** | ✅ `UNIFIED-SYSTEM.md` + `OPERATORS/SPECIALIST-MAP.md` + `PLAYBOOKS/OPERATIONS.md` + 7-horizon recheck |
| Workflow A run + exact prompts | ✅ `ARTIFACTS/WORKFLOW-A-PROMPTS-20260830.md` |
| Initiative + first CRITIC audit | ✅ `INITIATIVES/20260830-v30-os-buildout-and-migration.md`, `AUDITS/2026-08-30-workflow-a-package-critic.md` |
| Comparison + migration roadmap | ✅ `../COMPARE-v30-vs-EXISTING.md` |

## Comparison with the existing repo
See `../COMPARE-v30-vs-EXISTING.md` for how this v30 store relates to the pre-existing
Octo Harness / "Sovereign OS Kit v1.0" files, and the phased migration roadmap.
