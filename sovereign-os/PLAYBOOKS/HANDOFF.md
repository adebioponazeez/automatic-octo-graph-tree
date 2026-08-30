# PLAYBOOK: HANDOFF — v30

> Mandatory on every non-trivial output, from every operator, appended after `META`.

## Universal Output Contract footer

Every non-trivial output must include this `META` block. If missing, treat the output as incomplete.

```
META
OS: v30
Operator:
Artifact type:
Date:
Confidence: high / medium / low
Expiry:
Assumptions:
Principles used:
Sovereignty risks:
Failure modes:
What would make this false:
Next human action:
Next operator:
HANDOFF block follows
```

## Mandatory HANDOFF block

```
HANDOFF
From:
To:
Original goal:
Delivered:
Not delivered:
Assumptions:
Open questions:
Recommended next prompt:
Do-not-violate:
Freeze recommended? yes/no
```

## Rules
- If `META` or `HANDOFF` is missing → output is incomplete; run CRITIC / freeze.
- `Freeze recommended? yes/no` must be answered honestly per FREEZE conditions.
