#!/usr/bin/env python3
"""Probe whether clsh role agents + workflow are installed in a code project.

Usage:
  python check_agents.py <code_project_dir>

Exit 0 = ready for Phase 4 A″; 1 = missing pieces (print remediation).
Does not spawn LLM agents; filesystem only.
"""

from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_AGENTS = [
    "clsh-coder.md",
    "clsh-artist.md",
    "clsh-tester.md",
    "clsh-reviewer.md",
    "clsh-scout.md",
]
WORKFLOW = "clsh-task-pipeline.js"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    proj = Path(sys.argv[1]).expanduser().resolve()
    if not proj.is_dir():
        print(f"ERROR: not a directory: {proj}")
        return 1

    print(f"code project: {proj}")
    agent_dir = proj / ".mimocode" / "agent"
    wf_dir = proj / ".mimocode" / "workflows"
    reports = proj / ".clsh" / "reports"

    missing = []
    for name in REQUIRED_AGENTS:
        p = agent_dir / name
        ok = p.is_file()
        print(f"  [{'OK' if ok else 'MISSING'}] {p}")
        if not ok:
            missing.append(name)

    wf = wf_dir / WORKFLOW
    print(f"  [{'OK' if wf.is_file() else 'MISSING'}] {wf}")
    if not wf.is_file():
        missing.append(WORKFLOW)

    print(f"  [{'OK' if reports.is_dir() else 'MISSING'}] {reports}")
    if not reports.is_dir():
        missing.append(".clsh/reports/")

    print()
    if missing:
        print("Result: NOT READY")
        print("Remediation:")
        print(
            f'  & $env:MIMO_PYTHON "$env:USERPROFILE\\.claude\\skills\\clsh-project-mimo\\scripts\\bootstrap_roles.py" "{proj}"'
        )
        print("  Then start a NEW conversation and confirm @ autocomplete / mimo agent list shows clsh-coder.")
        print("  If role agents cannot load, set pipeline args.useRoleAgents=false (general + contract).")
        return 1

    print("Result: READY (files present)")
    print("Note: filesystem OK does not prove engine registered agentType — still verify @ autocomplete once.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
