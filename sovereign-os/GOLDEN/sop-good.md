# GOLDEN · Good SOP — v30

> The standard for OPS output. Uses the required OPS format: Trigger, Steps, Definition of done, Failure path, What gets written to the store, Time budget.

## SOP: Weekly audit (Workflow C)
- **Trigger:** Every week, fixed time, or after any model/vendor change.
- **Steps:**
  1. Update `STATE-PACK.md` capacity + one objective (3 min).
  2. Run CRITIC on the last week's artifacts and on the whole system (25 min).
  3. Run OPS to convert findings into one process fix (10 min).
  4. File audit note in `AUDITS/` and update `STATE-PACK.md` (2 min).
- **Definition of done:** `AUDITS/YYYY-MM-DD.md` exists; State Pack current; ≤1 process change identified.
- **Failure path:** If overloaded (capacity=low) → do steps 1 and 4 only, flag freeze if any drift signal.
- **What gets written to the store:** audit note, updated State Pack, any superseding decision.
- **Time budget:** 40 minutes.

---
**META**
- OS: v30 | Operator: OPS | Artifact type: SOP (golden example)
- Date: 2026-08-30 | Confidence: high | Expiry: example
- Assumptions: generic weekly cadence
- Principles used: C7, C8, C9
- Sovereignty risks: none
- Failure modes: none in the example
- What would make this false: cadence/timing differs for the user
- Next human action: adopt the cadence
- Next operator: CRITIC
