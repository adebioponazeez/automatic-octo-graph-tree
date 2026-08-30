# GOLDEN · Good Critic Rejection — v30

> The standard for CRITIC when work is not ready. Direct, specific, no invented problems.

**Verdict: NEEDS WORK**

**What works:** The 90-day done is testable; the replaceability section is strong; it obeys C5 and C9.

**Critical gaps, most important first:**
1. No State Pack was supplied — the artifact assumes initiative context that doesn't exist in the store (violates C2/C4).
2. The "5 real users" done-criteria has no defined measurement method or data source.
3. Trade-off map lists trades but never names a single irreversible decision with its fallback.
4. The Mermaid system map shows no human approval gate (violates C1).

**Specific fixes, not vibes:**
- Write the State Pack first, then re-run the artifact against it.
- Define "real user" (e.g., ≥1 active session/week for 2 weeks) and where the count comes from.
- Add one explicit "biggest irreversible mistake → cheapest reversal" line.
- Add an approval gate node between CRITIC and OPS in the map.

**Risk if used as-is:** SOFTWARE would build against invented constraints; the user could commit to a direction that isn't actually decided.

**Drift signals detected:** Missing State Pack; map omits C1 gate.

**Expiry / staleness risk:** Medium — the artifact is 1 step from usable after fixes.

---
**META**
- OS: v30 | Operator: CRITIC | Artifact type: critic rejection (golden example)
- Date: 2026-08-30 | Confidence: high | Expiry: example
- Assumptions: reviewing a representative strategic artifact
- Principles used: C1, C2, C4
- Sovereignty risks: none — no new work created
- Failure modes: none in the example
- What would make this false: the real artifact under review differs
- Next human action: fix the State Pack gap first
- Next operator: STRATEGIC
