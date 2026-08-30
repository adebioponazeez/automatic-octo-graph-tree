# ARTIFACT: Workflow A — Exact First Operator Prompts — v30

> Produced 2026-08-30 by STRATEGIC for the real current initiative:
> **Sovereign Production OS v30 build-out + migration of the existing Octo Harness repo.**
> Copy each prompt into its own chat. Run in order: STRATEGIC → (SOFTWARE and/or PRODUCT-CONTENT) → CRITIC → OPS.

---

## Step 1 — STRATEGIC (chat: STRATEGIC)

```
OS v30. State Pack below.

STATE PACK:
Date: 2026-08-30
User capacity this week: medium
Active initiative: Ship Sovereign Production OS v30 and migrate the existing Octo Harness / OS Kit v1.0 repo into it.
90-day definition of done: v30 store is the daily driver; 5 operator chats live; one real product/customer initiative passed CRITIC; migration at Phase 5+; system rebuildable from files in one day.
Current governing principles (max 7): [paste PRINCIPLES.md current set]
Hard constraints: do not delete working Octo Harness code; ≤ $50/mo AI; 25 min/day budget; one active initiative.
Do-not-violate: C1 (no AI ships without human), C2 (files = truth), C5 (replaceable), C6 (7-year survival).
Last 3 accepted decisions: D-20260830-01 (adopt v30 store), D-20260830-02 (7-year horizon), D-20260830-03 (start build-out + migration).
Open risks: scope size; migration could outlast the 25-min/day budget; user overload.
What failed recently: (none yet — system is new)
What must not be re-litigated: store is source of truth; 7-year horizon; 5 operators stay specialized.
Preferred stacks / tools: TypeScript or Python, boring and replaceable; files/JSON; existing Octo Harness repo.
Forbidden vendors / lock-in: no capability that exists only inside one vendor's chat.
Next human action: fill a real STATE-PACK.md for next week and pick the first product/customer initiative.
Expiry of this pack: 2026-09-06.

New initiative: [the one real product/customer initiative the user wants to survive 7 years]
Constraints: [time, money, stack, audience, sovereignty]
Current assets: [existing repo, operators, golden examples, checklists]
Produce: governing principles (max 7), 90-day done, trade-off map, Mermaid system map, cheapest test, irreversible mistakes, exact files to write into the canonical store.
```

> If the user has **no** product/customer initiative yet, run STRATEGIC in **degraded mode** instead:
```
FREEZE-ADJACENT / DEGRADED MODE. OS v30.
I do not have a product/customer State Pack yet. Produce, max 5 clarifying questions, a temporary assumption set, and a freeze recommendation for anything high-impact. Do not invent a product.
```

---

## Step 2 — SOFTWARE (chat: SOFTWARE) — after STRATEGIC accepts

```
OS v30. Strategy accepted (paste STRATEGIC output).

Architect the migration of the existing Octo Harness repo into the v30 canonical store:
- Keep all working code and files (Do-not-violate: never delete).
- Produce: architecture text + Mermaid, interface contracts, data model/invariants, failure modes, 24/7 notes, replaceability notes, test strategy.
- Default stack: existing repo's stack; state it explicitly.
- Flag any lock-in, hidden cost, or unexportable state in the existing repo.
End with META + HANDOFF.
```

---

## Step 2b — PRODUCT-CONTENT (chat: PRODUCT-CONTENT) — only when the user has a real offer

```
OS v30. Accepted strategy below (paste STRATEGIC output).
Produce: audience, desired action, offer in one sentence, deliverable, why it might fail, repurposing notes.
No invented proof. If proof is missing, say so. End with META + HANDOFF.
```

---

## Step 3 — CRITIC (chat: CRITIC) — on the package before any accept

```
OS v30. Review this package for Constitution compliance, State Pack alignment, internal consistency, completeness, sovereignty/replaceability, hidden irreversibility, overconfidence, drift signals, and 7-year fit.
Output format — ALWAYS:
Verdict: READY / NEEDS WORK / REJECT / FREEZE
What works:
Critical gaps, most important first:
Specific fixes, not vibes:
Risk if used as-is:
Drift signals detected:
Expiry / staleness risk:
META + HANDOFF
```

---

## Step 4 — OPS (chat: OPS) — after user accepts

```
OS v30. The package below is approved (paste CRITIC verdict + accepted artifacts).
Turn it into: a one-page daily cheat sheet, freeze conditions, weekly audit checklist, and the SOP for the next 7 days.
Time budget: 25 min/day, 40 min/week.
End with META + HANDOFF.
```

---

## Where the outputs go (file the same day)
- Principles → `PRINCIPLES.md`
- Decisions → `DECISIONS.md` (append-only, supersede explicitly)
- Accepted package → `ARTIFACTS/YYYY-MM-DD--<type>--<slug>.md`
- Initiative → `INITIATIVES/<slug>.md`
- Audit → `AUDITS/YYYY-MM-DD.md`

---

**META**
- OS: v30 | Operator: STRATEGIC | Artifact type: Workflow A run + exact prompts
- Date: 2026-08-30 | Confidence: high (prompts are ready-to-run)
- Expiry: 2026-09-30 (prompts may be refined via EVOLUTION only)
- Assumptions: user has not yet supplied a product/customer initiative; degraded-mode branch covers that
- Principles used: C1–C10
- Sovereignty risks: none — no AI ships; prompts gate on human acceptance
- Failure modes: user runs PRODUCT-CONTENT without a real offer → invented product; guarded by degraded-mode note
- What would make this false: user wants a different workflow order
- Next human action: run Step 1 with a real initiative, or run the degraded-mode variant
- Next operator: STRATEGIC (execution), then SOFTWARE / PRODUCT-CONTENT

**HANDOFF**
- From: STRATEGIC | To: STRATEGIC (execution) then SOFTWARE / PRODUCT-CONTENT / CRITIC / OPS
- Original goal: produce exact first prompts for the current initiative
- Delivered: step-by-step prompts for all 5 operators, file destinations, degraded-mode branch
- Not delivered: a product/customer initiative (does not exist yet — user's call, not AI's)
- Assumptions: user drives acceptance gates
- Open questions: what is the first real product/customer initiative?
- Recommended next prompt: Step 1 above
- Do-not-violate: never delete working code; no invented product; 5 operators stay specialized
- Freeze recommended? no
