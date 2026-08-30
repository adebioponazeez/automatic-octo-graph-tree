# GOLDEN · Bad Example — Fake 24/7 — v30

> Recognizable symptom: a chatbot is presented as an unattended production system with no operational split.

**Tell-tale phrases:**
- "This AI will work 24/7 for you."
- "Fully autonomous — it runs while you sleep."
- "Set it and forget it."

**Why it's rejected (CRITIC lens):**
- Collapses the required 24/7 split: A) on-demand operators, B) scheduled/automated jobs, C) human approval gates, D) monitoring & recovery.
- No retries, idempotency, health checks, secrets, or graceful degradation.
- Hides operational burden and the human bottleneck.
- No failure path.

**Fix:** separate the four 24/7 categories; define triggers, logging, approvals, monitoring, freeze conditions, and recovery steps. Never pretend conversational availability is production.
