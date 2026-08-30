# DECISIONS — Sovereign Production OS v30

> **Append-only.** Never silently rewrite history.
> Supersede an old decision with a new dated decision that explicitly names what it supersedes.
> Latest accepted decision wins ONLY if it explicitly supersedes the prior one. If not, freeze and resolve (see `PLAYBOOKS/HUGE-PROBLEMS.md` P6).

## Format

```
## D-<YYYYMMDD>-<nn> — <title>
- Status: accepted / deferred / superseded-by D-...
- Date:
- Supersedes:
- Decided by: (user, after operator: [operator])
- Decision:
- Rationale / trade-offs:
- Assumptions:
- Principles used:
- Risks / sovereignty notes:
- Expiry / review date:
```

---

## Decision log (append newest at bottom)

## D-20260830-01 — Adopt v30 canonical store as the source of truth
- Status: accepted
- Date: 2026-08-30
- Supersedes: (none; establishes the store)
- Decided by: user, after operator: STRATEGIC (scaffold request)
- Decision: `sovereign-os/` is the canonical store for the Sovereign Production OS v30. Chats are disposable; files are the system of record. Existing repo files (Octo Harness / OS Kit v1.0) are retained as reference, not deleted. See `../COMPARE-v30-vs-EXISTING.md` for the migration map.
- Rationale / trade-offs: single external truth (C2) outweighs keeping scattered chat context; cost is human time to file things the same day.
- Assumptions: user owns the store; migration is phased, not a big-bang rewrite.
- Principles used: C2, C3, C5, C6.
- Risks / sovereignty notes: none — nothing deleted; store is files the user controls.
- Expiry / review date: review at each phase gate.

## D-20260830-02 — Timeframe is 7 years, not 3
- Status: accepted
- Date: 2026-08-30
- Supersedes: any "3-year" framing in the scaffolded v30 copies
- Decided by: user (explicit instruction), after operator: OPS
- Decision: The survival horizon for the v30 system is 7 years. All scaffolded operator prompts, Constitution C6, and playbooks now use 7-year language. Cadences (90-day done, weekly audit, monthly checklist) are unchanged.
- Rationale / trade-offs: longer horizon raises the bar for replaceability and anti-drift; cost is stricter standards now.
- Assumptions: "7 years" is the intended production horizon.
- Principles used: C6, C7.
- Risks / sovereignty notes: none.
- Expiry / review date: revisit if the user changes the horizon (would be a new superseding decision).
