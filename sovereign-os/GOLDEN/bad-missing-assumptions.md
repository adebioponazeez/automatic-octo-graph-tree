# GOLDEN · Bad Example — Missing Assumptions — v30

> Recognizable symptom: implicit context treated as known; no expiry, failure modes, or META.

**Tell-tale signs:**
- "Assume the usual budget" (no number, no ceiling).
- "Use our standard stack" (never stated).
- "The client wants X" (no source, no date, no ownership).
- No expiry date — "this holds forever."
- No failure modes, no META, no HANDOFF.

**Why it's rejected (CRITIC lens):**
- Violates C4 (explicitness) — implicit context is treated as missing.
- Unknowable to a future you in 7 years.
- Unauditable for drift because there's no baseline to compare against.

**Fix:** write assumptions, trade-offs, unknowns, and expiry explicitly; add META + HANDOFF; date everything.
