# 02-agent-contract.md · Sovereign OS Kit v1.0
<!-- Layer 3: The Universal Schema Every Agent is Spawned With -->
<!-- Target: Reference doc; copy and instantiate per task or subagent spawn. -->

# Universal Agent Contract Schema

When spawning any subagent, the Orchestrator instantiates this standard YAML contract:

```yaml
contract_version: "1.0"
agent_id: "AGT-<<ROLE>>-<<NUM>>" # e.g. AGT-CODE-001, AGT-VERIFY-001
agent_name: "<<AGENT_NAME>>"
owner: "Chief-of-Staff"
model_preferred: "grok-3" # grok-3 | gpt-4o | gpt-4o-mini | claude-3-5-sonnet | qwen2.5-coder:7b
autonomy_tier: "A2" # A0 (inform), A1 (draft), A2 (approval gate), A3 (bounded auto)
max_budget_per_run_usd: 0.10

mandate:
  objective: "<<CLEAR_SINGLE_OUTCOME>>"
  success_criteria:
    - "<<MEASURABLE_CRITERIA_1>>"
    - "<<MEASURABLE_CRITERIA_2>>"
  not_in_scope: # Explicit negative bounds to prevent mission creep
    - "<<EXPLICIT_EXCLUSION_1>>"
    - "No direct external network calls without approval"
    - "No self-delegation or subagent spawning without may_delegate: true"

permissions:
  may_delegate: false # Only true if explicitly granted
  allowed_tools:
    - "<<TOOL_1>>"
    - "<<TOOL_2>>"
  read_paths:
    - "./graph/*.yaml"
    - "./src/**"
  write_paths:
    - "./graph/tasks.yaml"
    - "./generated_assets/**"

io_specification:
  input_schema:
    required_context: ["objective", "constraints", "reference_files"]
  output_schema:
    format: "markdown" # markdown | json | diff
    requires_evidence_block: true

rollback_procedure:
  on_failure: "abort_and_revert"
  revert_command: "git restore ."
```

---

# Mandatory Agent Lifecycle States

```
[SPAWNED] ──► [INGEST_CONTRACT] ──► [EXECUTE_TASK] ──► [SELF_VERIFY] ──► [ATTACH_EVIDENCE] ──► [SUBMIT_TO_CHIEF]
                                                                                                      │
                                              [ESCALATE_IF_BLOCKED] ◄─────────────────────────────────┘
```

1. **SPAWNED:** Agent initialized with contract and inherited Constitution.
2. **INGEST_CONTRACT:** Agent acknowledges scope and negative boundaries (`not_in_scope`).
3. **EXECUTE_TASK:** Runs reasoning/code/analysis using least-privilege tools.
4. **SELF_VERIFY:** Checks code syntax, test cases, and empirical grounding.
5. **ATTACH_EVIDENCE:** Formats the required Evidence Block with confidence and token cost.
6. **SUBMIT_TO_CHIEF:** Emits structured output back to Orchestrator for review and state commit.
