# ARTIFACT: OPS 9-Day Operating Cadence — content-engine initiative

> Produced 2026-08-30 by OPS. Runs Workflow A/B/C across the 9-day cycle (2026-08-20 → 2026-09-06,
> with remaining execution days now active). Human time budget: 25 min/day, 40 min/week.

## 1. Trigger / day-by-day plan (batch-and-validate)
| Day | Phase | What happens | Human time |
|---|---|---|---|
| D1 | Wave 1 scoping | Confirm top 3–5 offers; write each as a task contract | 25 min |
| D1–3 | Wave 1 build+ship | SOFTWARE + PRODUCT-CONTENT produce offers; CRITIC gates each; ship | 25 min/day |
| D4 | Mid-cycle audit | CRITIC + OPS: evidence check, budget check, quality scan, freeze check | 40 min |
| D5–7 | Wave 2 (scale) | Add next offers based on wave-1 evidence; re-scope weak ones | 25 min/day |
| D8 | Final CRITIC sweep | Verify evidence on all offers; confirm 30/150/$50 trajectory | 25 min |
| D9 | Done + file | Count offers/users/spend; file final report; update State Pack | 25 min |

## 2. Budget guardrail (≤ $50 total)
- Checkpoint every day: cumulative spend in `cost_tracker`.
- If spend exceeds $50 on any day → **freeze routing**, re-plan, alert human (A2).
- Model tiering: never frontier models for formatting/scraping/restructuring.

## 3. Quality + evidence gate (every offer, before ship)
Each offer must pass, or it does not ship:
- [ ] Evidence block: real problem source, data/grounding, confidence 0–1, tokens+cost, tier
- [ ] Non-verbal/emotional professionalism: tone, polish, no hype (golden standard)
- [ ] META + HANDOFF present
- [ ] Human approval to publish (C1, A2+)
- [ ] Files filed same day

## 4. Freeze conditions (from FREEZE-CHECKLIST)
Freeze immediately if: can't state objective in one sentence · two operators contradict ·
outputs generic/hypey · chats used as memory · spend > $50 · >3 active sub-initiatives ·
about to make an irreversible decision.

## 5. Weekly/mid audit (D4)
Run the Weekly Audit checklist: Constitution obeyed? only-in-chat knowledge? drift scan?
vendor/model risk? one process change? → write note to `AUDITS/`.

## 6. Definition of done
By D9: 30 offers live, 150 active users, ≤ $50 spend, every offer evidence-verified and filed.
If evidence is weak on scale → re-scope honestly rather than fake 150 users.

## 7. Failure path
- Overload (capacity=medium) → one operator per day, maintenance-only if needed, never fake progress.
- Quality collapse → freeze, show golden example, re-certify.
- Budget breach → freeze routing.

---
**META**
- OS: v30 | Operator: OPS | Artifact type: 9-day operating cadence
- Date: 2026-08-30 | Confidence: high | Expiry: 2026-09-06
- Assumptions: wave-1 offers are user-selected; evidence bar applies everywhere
- Principles used: C1, C2, C5, C6, C8
- Sovereignty risks: none — human approval gates each ship
- Failure modes: skipping daily budget/quality checks
- What would make this false: user's cycle dates or targets change
- Next human action: name wave-1 offers
- Next operator: SOFTWARE / PRODUCT-CONTENT
