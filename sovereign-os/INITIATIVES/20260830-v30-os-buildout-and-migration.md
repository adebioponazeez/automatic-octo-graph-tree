# INITIATIVE: v30 OS build-out + migration — v30

```
INITIATIVE: Sovereign Production OS v30 build-out + migration of the existing repo
Owner: adebioponazeez
Date created: 2026-08-30
Status: active

ONE SENTENCE:
Ship the Sovereign Production OS v30 as a working, owner-controlled system with a full canonical store, and migrate the existing Octo Harness / OS Kit v1.0 repo into it without destroying the working code.

90-DAY DEFINITION OF DONE (testable):
By day 90: (a) the v30 store is the daily driver (State Pack updated weekly, audit run weekly); (b) the 5 operator chats are created from OPERATORS/*; (c) at least one real product/customer initiative has completed Workflow A through CRITIC; (d) the migration plan (COMPARE-v30-vs-EXISTING.md) is at Phase 5+; (e) the whole system can be rebuilt from files in one day.

GOVERNING PRINCIPLES (max 7) — see PRINCIPLES.md:
1. Files are the source of truth; chat is disposable (C2).
2. One job per operator; no god-agent, no overlap (C3).
3. 7-year survival: boring, replaceable, vendor-independent (C6, C5).
4. Human approval before any ship/publish/spend (C1).
5. Evidence and explicit assumptions over assertion (C4, C2).
6. One active initiative; incremental reversible phases (C8).
7. Survival over peak performance (C6).

TRADE-OFFS:
- control: files + own code → more human time
- complexity: boring stack → less cleverness
- cost: ≤ $50/mo AI → fewer calls
- speed: MVP in 90d → less polish
- durability: replaceable → slower first build
- replaceability: no lock-in → decline vendor-specific features

CHEAPEST TEST:
Day 1–7: use the daily loop (CHECKLISTS/DAILY-CHEAT-SHEET.md) for a week. If the loop is skipped 3+ days, the cadence is wrong for the user → adjust via OPS, not by dropping it.

BIGGEST IRREVERSIBLE MISTAKE:
Deleting the working Octo Harness code while migrating. Cheapest reversal: never delete; supersede via dated decision.

FILES IN THE STORE:
- PRINCIPLES.md: updated 2026-08-30
- DECISIONS.md: D-20260830-01, D-20260830-02, D-20260830-03
- ARTIFACTS/: WORKFLOW-A-PROMPTS-20260830.md
- INITIATIVES/: this file

CRITIC VERDICT:
NEEDS WORK (scope is large; see ARTIFACTS/WORKFLOW-A-PROMPTS-20260830.md META)

NEXT ACTION:
User runs the STRATEGIC prompt below with a filled STATE-PACK.md; else degrade to the provided prompts.

EXPIRY / REVIEW DATE:
2026-10-30 (90 days from creation) or next weekly audit, whichever is first.
```
