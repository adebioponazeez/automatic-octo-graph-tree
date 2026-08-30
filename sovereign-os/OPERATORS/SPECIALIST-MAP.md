# OPERATORS: Specialist-to-Operator Merge Map — v30

> Resolves the 14-specialist / 5-operator overlap (cross-check finding C3).
> **Rule: exactly ONE operator owns each specialist's mandate.** The 5 v30 operators are the live roles;
> the 14 v1.0 specialists survive as **specialties (tactics) inside** their owning operator — never as separate chats.
> This removes god-agent and overlap while keeping the useful specialization.

## The map
| v1.0 Specialist | Owning v30 operator | Why (no overlap after merge) |
|---|---|---|
| AGT-DEMAND-001 Demand Intelligence | **STRATEGIC** | demand signals feed strategy/cheapest-test, not content |
| AGT-ROUTER-001 Model Router | **SOFTWARE** | routing/fallback is architecture + execution config |
| AGT-CODE-001 Junior | **SOFTWARE** | code = software operator's job |
| AGT-DATA-001 Schema & Graph | **SOFTWARE** | data model + mission-graph schema = software |
| AGT-SECURITY-001 DevSecOps | **SOFTWARE** | guardrails/secret hygiene = runtime software concern |
| AGT-KIMI-001 Long-Context Ingest | **SOFTWARE** | corpus ingestion is an implementation tactic |
| AGT-COST-001 Budget/Cache | **OPS** | budget + caching = operational/cost discipline |
| AGT-OVERFLOW-001 Consensus/Overflow | **OPS** | fallback + consensus = resilience/ops |
| AGT-CRITIC-001 Red Team | **CRITIC** | adversarial review = critic operator |
| AGT-VERIFY-001 Ahmed Verification | **CRITIC** | evidence/invariant checking = critic operator |
| AGT-GROK-001 Grounding/Adversarial | **CRITIC** | live grounding + anti-sycophancy = critic operator |
| AGT-EDIT-001 Editorial | **PRODUCT-CONTENT** | editing/technical writing = content |
| AGT-GROWTH-001 Distribution | **PRODUCT-CONTENT** | distribution tactics = content |
| AGT-SYNTH-001 Executive Synthesizer | **OPS** (delivery) | synthesis of final report for human = ops delivery; else CRITIC for verification |

> Note on AGT-SYNTH: synthesis of a *final report for human sign-off* is an OPS delivery function; if the task is *verifying* a report, route to CRITIC. Do not create a 15th chat — pick the operator by task intent.

## Non-overlap proof
- Every specialist maps to exactly **one** operator.
- No operator is a "god-agent": STRATEGIC (decide), SOFTWARE (build), PRODUCT-CONTENT (communicate), OPS (run), CRITIC (verify).
- Provider is config, not role (see `UNIFIED-SYSTEM.md` §2) — so specialists are not split across "Grok vs ChatGPT."

## Anti-patterns to reject
- Spawning "Azeez Jr. Chief of Staff" as a god-agent (C3).
- Running 14 separate chats with overlapping mandates.
- Treating provider/model preference as an operator identity.
- Hand-editing `bundles/*.md` (C6).

---
**META**
- OS: v30 | Operator: STRATEGIC | Artifact type: operator/specialist merge map
- Date: 2026-08-30 | Confidence: high | Expiry: on next specialist addition (via EVOLUTION)
- Assumptions: specialist roles are preserved as tactics inside operators
- Principles used: C3, C5
- Sovereignty risks: none
- Failure modes: someone re-opens 14 chats instead of 5
- What would make this false: a genuinely new role with no operator home
- Next human action: accept; create 5 chats, not 14
- Next operator: OPS
