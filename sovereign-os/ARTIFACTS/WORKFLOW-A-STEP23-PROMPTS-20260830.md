# ARTIFACT: Workflow A Step 2/3 — SOFTWARE + PRODUCT-CONTENT handoff prompts — v30

> Produced 2026-08-30. These are turnkey: paste into the matching chat **after the user names
> the wave-1 offers** (3–5 offers, days 1–3). Do NOT fill the offer list yourself — that is the
> user's sovereign choice (C1). Each output must pass the CRITIC evidence/quality gate before ship.

---

## Step 2 — SOFTWARE (chat: SOFTWARE)

```
OS v30. Strategy accepted. Wave-1 scope below.

STATE PACK (summary):
- 9-day done: 30 offers live, 150 active users, ≤ $50 AI spend, by 2026-09-06.
- Capacity: medium. Batch-and-validate: ship top 3–5 offers days 1–3, then scale.
- Do-not-violate: evidence-first; human approval to publish; ≤ $50; never delete the
  unified Octo Harness code; no invented metrics/testimonials.
- Method: Siraj Raval Vibe Coding Playbook (Plan → Execute → Verify) + Mo Gawdat.

WAVE-1 OFFERS (user-selected — INSERT):
1.
2.
3.
4.
5.

For each offer produce:
- Architecture in text + Mermaid (if code/digital product)
- Interface contracts: inputs, outputs, errors
- Data model + invariants (esp. any user tracking that counts "active users")
- Failure modes
- 24/7 notes: retries, idempotency, logging, health, secrets, graceful degradation
- Replaceability notes: what if this vendor/model/API dies
- Test strategy
- Evidence + META + HANDOFF

Do NOT invent features or metrics beyond the user's offer list. Flag lock-in, hidden
cost, or unexportable state. If an offer is ambiguous, ask (degraded mode) — do not assume.
```

---

## Step 2b — PRODUCT-CONTENT (chat: PRODUCT-CONTENT)

```
OS v30. Strategy accepted. Wave-1 scope below.

STATE PACK (summary):
- 9-day done: 30 offers live, 150 active users, ≤ $50 AI spend, by 2026-09-06.
- Quality bar: extreme — professional at the non-verbal/emotional level, no hype.
- Do-not-violate: no invented testimonials/metrics/urgency; human approval to publish.
- Method: Siraj Raval Vibe Coding Playbook + Mo Gawdat "Scary Smart".

WAVE-1 OFFERS (user-selected — INSERT):
1.
2.
3.
4.
5.

For each offer produce:
1. Audience
2. Desired action
3. Offer/message in one sentence
4. Deliverable (copy/YouTube script/landing)
5. Why it might fail
6. Repurposing notes
7. Evidence + META + HANDOFF

Claim rules: no invented results/numbers/capabilities. If proof is missing, say so and
write around verified facts only. Flag any copy that overpromises or creates lock-in.
```

---

## Step 3 — CRITIC (chat: CRITIC) — run on each offer before ship

```
OS v30. Review this offer for ship-readiness.
Check: Constitution compliance, State Pack alignment, internal consistency, completeness
(can it ship tomorrow?), evidence (real problem + data), sovereignty/replaceability,
hidden irreversibility, overconfidence, drift, and 9-day fit.
Output ALWAYS: Verdict (READY/NEEDS WORK/REJECT/FREEZE) · What works · Critical gaps
(most important first) · Specific fixes · Risk if used as-is · Drift signals · Expiry.
Then META + HANDOFF.
```

---

## After each wave: OPS (chat: OPS)
```
OS v30. Wave results below (paste CRITIC verdicts + shipped offers).
Update the 9-day cadence: budget spent so far, offers live, users acquired, next wave.
Adjust wave-2 scope per evidence. Flag any freeze condition.
End with META + HANDOFF.
```

---

## Where outputs go (same day)
- Each shipped offer → `ARTIFACTS/2026-09-0X--offer--<slug>.md` with evidence block
- CRITIC verdicts → same artifact or `AUDITS/`
- Budget/users tallies → `STATE-PACK.md` + initiative file
- Any re-scope → a superseding `DECISIONS.md` entry

---
**META**
- OS: v30 | Operator: STRATEGIC (handoff prep) | Artifact type: Workflow A Step 2/3 prompts
- Date: 2026-08-30 | Confidence: high (prompts ready) | Expiry: 2026-09-06
- Assumptions: user supplies wave-1 offers + definitions + recent-failure note
- Principles used: C1, C2, C3, C4, C6
- Sovereignty risks: none — offers are user-selected; no invented scope
- Failure modes: operator assumes an offer without user selection
- What would make this false: user wants a different offer structure
- Next human action: insert wave-1 offers into Step 2/2b
- Next operator: SOFTWARE / PRODUCT-CONTENT
