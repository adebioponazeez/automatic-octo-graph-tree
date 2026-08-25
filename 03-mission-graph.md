# 03-mission-graph.md · Sovereign OS Kit v1.0
<!-- Layer 3: Shared World Model — Entities, Edges, and File Layout -->
<!-- Target: Repository specification; agents read/write to ./graph/ directory. -->

# 1. Mission Graph Concept
The **Mission Graph** is the single source of truth for the entire operating system. It represents:
- **Projects:** Strategic initiatives currently in flight.
- **Goals:** Measurable outcomes tied to customer value or technical milestones.
- **Agents:** Active agent contracts and execution history.
- **Edges:** Explicit dependencies connecting tasks, agents, and outcomes.

All state resides in `./graph/*.yaml`. No invisible runtime state.

---

# 2. File Layout in `./graph/`

```
graph/
├── projects.yaml    # Active ventures and high-level deliverables
├── goals.yaml       # Measurable targets, metrics, and hard deadlines
├── agents.yaml      # Roster of active specialist agents and contracts
└── edges.yaml       # Directed dependency graph linking goals to tasks
```

---

# 3. Graph Schema Specifications

### `graph/projects.yaml`
```yaml
projects:
  - id: "PRJ-001"
    name: "Sovereign AI Router & Cowork Harness"
    status: "active" # active | paused | completed
    owner: "adebioponazeez"
    monthly_budget_usd: 50.00
    updated_at: "2026-08-25T17:00:00Z"
    updated_by: "Chief-of-Staff"
```

### `graph/goals.yaml`
```yaml
goals:
  - id: "G-001"
    project_id: "PRJ-001"
    title: "Zero-Downtime Multi-Model Routing with Grok Primary & ChatGPT Fallback"
    metric: "100% test pass rate & <$50/mo token spend"
    target_date: "2026-09-01"
    status: "in_progress"
    priority_ice: 95
```

### `graph/agents.yaml`
```yaml
agents:
  - id: "AGT-ORCH-001"
    name: "Azeez Jr. (Chief of Staff)"
    role: "orchestrator"
    platform: "grok" # grok | chatgpt | claude | local
    status: "active"
  - id: "AGT-CODE-001"
    name: "Junior (Principal Code Architect)"
    role: "coder"
    platform: "grok"
    status: "active"
  - id: "AGT-VERIFY-001"
    name: "Ahmed (Lead Verification Scout)"
    role: "verifier"
    platform: "chatgpt"
    status: "active"
```

### `graph/edges.yaml`
```yaml
edges:
  - source: "G-001"
    target: "PRJ-001"
    relationship: "belongs_to"
  - source: "AGT-VERIFY-001"
    target: "G-001"
    relationship: "verifies"
```
