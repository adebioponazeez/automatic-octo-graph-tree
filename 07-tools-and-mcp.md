# 07-tools-and-mcp.md · Sovereign OS Kit v1.0
<!-- Layer 5: Tool Registry Contract, MCP Server List, and Compliance Rules -->
<!-- Target: Orchestrator and any tool-using agent. -->

# 1. Tool Declaration & Least Privilege Contract

Every tool callable by an agent MUST be explicitly registered in this registry with declared parameters, timeout limits, and idempotency guarantees.

```yaml
tools_registry:
  - name: "bash_sandbox"
    description: "Executes local bash command in sandboxed environment"
    timeout_seconds: 30
    requires_approval_for: ["rm -rf", "git push --force", "drop database"]
    autonomy_tier_required: "A2"

  - name: "web_search"
    description: "Queries public web indexes for real-time fact checking"
    timeout_seconds: 15
    autonomy_tier_required: "A0"

  - name: "graph_writer"
    description: "Mutates nodes and edges in ./graph/*.yaml"
    timeout_seconds: 5
    autonomy_tier_required: "A2"

  - name: "code_linter"
    description: "Runs pytest and ruff syntax checks"
    timeout_seconds: 60
    autonomy_tier_required: "A1"
```

---

# 2. Model Context Protocol (MCP) Server Configuration

When integrating external tools via MCP (Model Context Protocol):

| MCP Server | Capability | Security Posture |
|---|---|---|
| **Filesystem MCP** | Scoped read/write to project root only (`./`) | Read/Write restricted to working repo |
| **Git MCP** | Git log, status, branch, commit, diff | Write operations require Tier A2 approval |
| **PostgreSQL MCP** | Structured query execution on analytics database | Read-only permissions (`SELECT` only) |
| **Fetch / Puppeteer MCP** | Headless browser for ground-truth verification | SSRF-filtered, private IPs blocked |

---

# 3. Security, Credentials & Secret Handling

1. **Zero Plaintext Secrets:** Never write API keys, database credentials, or tokens in Markdown, Git history, or graph files.
2. **Environment Variable Reference:** Always reference keys via environment variables (e.g. `process.env.GROK_API_KEY`, `$OPENAI_API_KEY`).
3. **Automated Scrubbing:** The `ContentGuardrails` layer scans and masks all outputs matching key patterns (`sk-...`, `xai-...`, `ant-...`, `ghp_...`).
4. **Network Boundaries:** Agents are forbidden from making outbound HTTP requests to internal IP ranges (`127.0.0.1`, `10.0.0.0/8`, `192.168.0.0/16`, `169.254.169.254`).

---

# 4. Token Compression Tools (TOON & Semantic Anchors)

### A. TOON (Token-Oriented Object Notation)
- **Problem:** Sending large JSON arrays repeats field keys for every single record, wasting 40–60% of prompt tokens on `{ "id": ..., "name": ... }`.
- **Solution:** Converts uniform JSON structures into compact tabular TOON format (`[N]{keys}: values`).
- **Endpoint:** `POST /compress/toon`

```
# Raw JSON (180 characters / ~45 tokens):
[
  {"id": 1, "role": "planner", "status": "active"},
  {"id": 2, "role": "coder", "status": "active"}
]

# TOON Compressed (65 characters / ~16 tokens - 64% savings):
[2]{id,role,status}:
  1,planner,active
  2,coder,active
```

### B. Single-Token Atomic Semantic Anchors
- **Problem:** Verbose prompt instruction headers (`CRITICAL SYSTEM INVARIANT (DO NOT VIOLATE):`) consume 8–15 tokens per section.
- **Solution:** Replaced with verified 1-token atomic Unicode/ASCII anchors (`🔒 INVARIANT:`, `🎯 GOAL:`, `⚡ PERF:`, `🛡️ SEC:`, `📦 FORMAT:`).
- **Endpoint:** `POST /compress/prompt`
