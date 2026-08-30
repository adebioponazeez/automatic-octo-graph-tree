# PLAYBOOK: HUGE PROBLEMS — Problem Catalog & Response — v30

> Copy from Section 7 of the v30 document. Freeze conditions live in `FREEZE.md`.

## Problem catalog and response

**P1. Quality collapse / prompt rot**
Symptoms: longer answers, vaguer structure, missing META, generic tone, principles ignored.
Action: Freeze. Paste Constitution + State Pack + one golden example. Run CRITIC on last 5 artifacts. Revert operator prompt to the v30 text exactly. Do not “tune by vibe.”

**P2. Model or vendor change**
Action: Assume behavior changed. Run a regression pack:
- one strategy task
- one architecture task
- one content task
- one critic task
Compare to `GOLDEN/`. If deviation is high, freeze shipping and recertify operators.

**P3. Vendor death, rate limits, outage, policy shift**
Action: Canonical store must still make sense. Rebuild operators on a fallback model using the same Constitution and files. No unique capability should exist only inside one vendor’s chat.

**P4. Human overload (most common early-year failure)**
Action: Capacity = low. One initiative. Daily loop only. OPS redesigns for 15-minute days. Kill work that is not in the 90-day done.

**P5. Scope explosion**
Action: STRATEGIC must cut to one 90-day done. Everything else goes to a dated parking list. Parking list is not work.

**P6. Contradictory decisions**
Action: Open `DECISIONS.md`. Latest accepted decision wins only if it explicitly supersedes the old one. If not, freeze and resolve. Do not let chats vote.

**P7. Silent data/control failure**
Action: SOFTWARE + CRITIC. Inventory: where data lives, who can train on it, what is exportable, what is lost if the account dies. If unknown, treat as high risk.

**P8. The system is producing a lot and compounding nothing**
Action: CRITIC. Count artifacts that were actually used. If use-rate is low, halt generation. OPS creates a “finish and file” week.

## Parking list (for P5)
| Date | Parked idea/scope | Why parked | Revisit date |
|---|---|---|---|
| | | | |
