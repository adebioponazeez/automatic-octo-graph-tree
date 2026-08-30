# PLAYBOOK: EVOLUTION — Change Control (v30 → v31) — v30

> Never edit operator prompts live because a single answer was annoying.
> This is the ONLY way to change the system.

## Rules
- **Constitution** changes are rare and dated.
- **Operator prompt** changes need: reason, expected gain, regression test, rollback.
- Keep previous operator files: `SOFTWARE.v30.md`, `SOFTWARE.v31.md`.
- **One change at a time.**
- Recertify with golden tasks before using in production.

## Evolution prompt (to STRATEGIC + CRITIC)

```
Propose a change to operator [X].
Current failure evidence:
Desired gain:
Risk to sovereignty/reliability:
Regression tests:
Rollback:
If this is a tactic, do not touch the Constitution.
```

## Rule of thumb
If you cannot explain the change in **8 lines**, you are not ready to change it.

## Operator version history
| Operator | Version | Date | Change | Regression test | Rollback plan |
|---|---|---|---|---|---|
| STRATEGIC | v30 | 2026-08-30 | 7-year survivability framing | golden one-pager | revert wording |
| SOFTWARE | v30 | 2026-08-30 | "future you in 7 years" | golden architecture | revert wording |
| CRITIC | v30 | 2026-08-30 | "12 months and 7 years" | golden rejection | revert wording |

## Recorded amendments
- **D-20260830-02**: survival horizon set to 7 years (from the default 3-year framing). Constitution C6 and operator prompts updated. This is a framing amendment, not a Constitution article change; logged in `../DECISIONS.md`.
