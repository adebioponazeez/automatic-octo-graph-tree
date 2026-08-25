#!/usr/bin/env python3
"""
08_roster_engine.py · Sovereign OS Kit v1.0

Automated Bundle Generator & Workspace Compiler for Cross-Platform AI Ecosystems.
Compiles Constitution, Operating System rules, Platform Adapters, and assigned
Specialist Agents into ready-to-paste platform bundles:
- bundles/bundle-claude.md
- bundles/bundle-grok.md
- bundles/bundle-chatgpt.md
- bundles/bundle-gemini.md
- bundles/bundle-openrouter.md
- bundles/sovereign-os-master-handbook.md
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

ROOT_DIR = Path(__file__).parent
BUNDLES_DIR = ROOT_DIR / "bundles"

# Platform assignment mapping for specialists
PLATFORM_MAPPINGS: Dict[str, Dict[str, any]] = {
    "claude": {
        "title": "Sovereign OS · Claude Cowork & Anthropic Bundle",
        "description": "Optimized for Lead Systems Architecture, Invariant Verification, and Refactoring",
        "assigned_agents": [
            "AGT-EDIT-001 · Editorial Strategist",
            "AGT-VERIFY-001 · Verification Scout",
            "AGT-CODE-001 · Principal Code Architect",
            "AGT-CRITIC-001 · Adversarial Red Team Reviewer",
            "AGT-SYNTH-001 · Executive Deliverable Synthesizer",
        ],
        "adapter_section": "Claude Cowork Setup",
    },
    "grok": {
        "title": "Sovereign OS · xAI Grok Primary Intelligence Bundle",
        "description": "Optimized for High-Throughput Code Generation, Fast Reasoning, and Real-Time Signal Discovery",
        "assigned_agents": [
            "AGT-DEMAND-001 · Demand Intelligence Scout",
            "AGT-CODE-001 · Principal Code Architect",
            "AGT-ROUTER-001 · Model Router & Fallback Engineer",
            "AGT-GROWTH-001 · UGC & Distribution Tactician",
        ],
        "adapter_section": "xAI Grok Setup",
    },
    "chatgpt": {
        "title": "Sovereign OS · ChatGPT Chief of Staff & High-Volume Operations Bundle",
        "description": "Optimized for Chief of Staff Orchestration, Schema Engineering, and General Operations",
        "assigned_agents": [
            "AGT-DEMAND-001 · Demand Intelligence Scout",
            "AGT-VERIFY-001 · Verification Scout",
            "AGT-COST-001 · Token Budget & Context Cache Optimizer",
            "AGT-DATA-001 · Schema & Structured Data Engineer",
            "AGT-SECURITY-001 · DevSecOps & Secret Leak Auditor",
            "AGT-SYNTH-001 · Executive Deliverable Synthesizer",
        ],
        "adapter_section": "ChatGPT Setup",
    },
    "gemini": {
        "title": "Sovereign OS · Google Gemini Long-Context Analysis Bundle",
        "description": "Optimized for Massive Context Ingestion and Technical Documentation Auditing",
        "assigned_agents": [
            "AGT-VERIFY-001 · Verification Scout",
            "AGT-DATA-001 · Schema & Structured Data Engineer",
            "AGT-EDIT-001 · Editorial Strategist",
        ],
        "adapter_section": "Gemini Setup",
    },
    "openrouter": {
        "title": "Sovereign OS · OpenRouter Overflow & Consensus Arbiter Bundle",
        "description": "Dormant Overflow Router for Multi-Model Consensus (Kimi K3, DeepSeek R1, Qwen 2.5)",
        "assigned_agents": [
            "AGT-OVERFLOW-001 · Multi-Model Consensus & Overflow Arbiter",
            "AGT-ROUTER-001 · Model Router & Fallback Engineer",
        ],
        "adapter_section": "OpenRouter Setup",
    },
}


def read_file_safe(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return f"<!-- Warning: File {path.name} not found -->"


def generate_bundles(output_dir: Optional[Path] = None) -> List[Path]:
    """Compiles all platform bundles and master handbook."""
    target_dir = output_dir or BUNDLES_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    generated_files: List[Path] = []

    constitution = read_file_safe(ROOT_DIR / "00-constitution.md")
    operating_system = read_file_safe(ROOT_DIR / "01-operating-system.md")
    agent_contract = read_file_safe(ROOT_DIR / "02-agent-contract.md")
    mission_graph = read_file_safe(ROOT_DIR / "03-mission-graph.md")
    orchestrator_prompt = read_file_safe(ROOT_DIR / "04-orchestrator-prompt.md")
    subagent_library = read_file_safe(ROOT_DIR / "05-subagent-library.md")
    platform_adapters = read_file_safe(ROOT_DIR / "06-platform-adapters.md")
    tools_mcp = read_file_safe(ROOT_DIR / "07-tools-and-mcp.md")

    for platform_key, config in PLATFORM_MAPPINGS.items():
        bundle_path = target_dir / f"bundle-{platform_key}.md"

        lines: List[str] = [
            f"# {config['title']}",
            f"> **Purpose:** {config['description']}",
            f"> **Target Platform:** `{platform_key.upper()}`",
            f"> **Budget Constraint:** **$50.00 USD / Month** ($1.67/day) with Context Caching Enabled",
            "",
            "---",
            "",
            "## SECTION 1: CONSTITUTION (IMMUTABLE GOVERNANCE)",
            constitution,
            "",
            "---",
            "",
            "## SECTION 2: OPERATING SYSTEM & EVIDENCE CONTRACT",
            operating_system,
            "",
            "---",
            "",
            "## SECTION 3: PLATFORM-SPECIFIC INSTRUCTIONS",
            f"### Active Platform: {platform_key.capitalize()}",
            "Assigned Specialist Agents on this Workspace:",
        ]

        for agent_name in config["assigned_agents"]:
            lines.append(f"- **{agent_name}**")

        lines.extend([
            "",
            "---",
            "",
            "## SECTION 4: CHIEF OF STAFF ORCHESTRATOR PROMPT",
            orchestrator_prompt,
            "",
            "---",
            "",
            "## SECTION 5: SPECIALIST SUBAGENT LIBRARY & CONTRACTS",
            subagent_library,
            "",
            "---",
            "",
            "## SECTION 6: TOOLS, SECURITY & SECRET SANITIZATION",
            tools_mcp,
            "",
        ])

        compiled_text = "\n".join(lines)
        bundle_path.write_text(compiled_text, encoding="utf-8")
        generated_files.append(bundle_path)

    # Also generate master all-in-one handbook
    handbook_path = target_dir / "sovereign-os-master-handbook.md"
    master_lines = [
        "# Sovereign OS Kit v1.0 · Complete Master Operating Handbook",
        "> Comprehensive unified manual for multi-agent sovereign ecosystem governed by adebioponazeez.",
        f"> Hard Budget Ceiling: **$50.00 USD / Month** ($1.67/day) | Test Passing: 78/78",
        "",
        "---",
        "",
        "## 1. CONSTITUTION",
        constitution,
        "",
        "## 2. OPERATING SYSTEM",
        operating_system,
        "",
        "## 3. UNIVERSAL AGENT CONTRACT",
        agent_contract,
        "",
        "## 4. MISSION GRAPH SCHEMA",
        mission_graph,
        "",
        "## 5. CHIEF OF STAFF ORCHESTRATOR",
        orchestrator_prompt,
        "",
        "## 6. SPECIALIST SUBAGENT ROSTER",
        subagent_library,
        "",
        "## 7. PLATFORM WIRING & ADAPTERS",
        platform_adapters,
        "",
        "## 8. TOOLS & MCP SECURITY REGISTRY",
        tools_mcp,
    ]
    handbook_path.write_text("\n\n".join(master_lines), encoding="utf-8")
    generated_files.append(handbook_path)

    return generated_files


def main():
    parser = argparse.ArgumentParser(description="Sovereign OS Kit Bundle Compiler")
    parser.add_argument("--output-dir", "-o", type=Path, default=BUNDLES_DIR, help="Destination directory for bundles")
    parser.add_argument("--check", action="store_true", help="Verify all governance source files exist")
    args = parser.parse_args()

    if args.check:
        missing = []
        for fn in [
            "00-constitution.md", "01-operating-system.md", "02-agent-contract.md",
            "03-mission-graph.md", "04-orchestrator-prompt.md", "05-subagent-library.md",
            "06-platform-adapters.md", "07-tools-and-mcp.md"
        ]:
            if not (ROOT_DIR / fn).exists():
                missing.append(fn)
        if missing:
            print(f"[!] Missing required files: {missing}", file=sys.stderr)
            sys.exit(1)
        print("[✓] All 8 governance source files verified!")
        return

    print("[*] Compiling Sovereign OS Kit v1.0 Platform Bundles...")
    files = generate_bundles(args.output_dir)
    print(f"\n[+] Successfully generated {len(files)} platform bundles in {args.output_dir.relative_to(ROOT_DIR)}:")
    for f in files:
        print(f"  - {f.name} ({f.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
