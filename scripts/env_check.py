#!/usr/bin/env python3
"""Environment check for clsh-project-mimo on MiMo Desktop."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

VAULT = Path(r"\\192.168.0.123\data\Obsidian")


def check(name: str, ok: bool, detail: str = "") -> bool:
    mark = "OK" if ok else "MISSING"
    extra = f" — {detail}" if detail else ""
    print(f"  [{mark}] {name}{extra}")
    return ok


def main() -> int:
    print("=" * 60)
    print("  clsh-project-mimo Environment Check")
    print("=" * 60)

    py_ok = sys.version_info >= (3, 8)
    check("python>=3.8", py_ok, f"v{sys.version.split()[0]}")

    mimo_py = os.environ.get("MIMO_PYTHON")
    check(
        "MIMO_PYTHON",
        bool(mimo_py and Path(mimo_py).exists()),
        mimo_py or "unset — falling back to PATH python",
    )

    home = Path.home()
    skill_dir = home / ".claude" / "skills" / "clsh-project-mimo"
    check("skill_dir", skill_dir.is_dir(), str(skill_dir))
    check("gate_phase.py", (skill_dir / "scripts" / "gate_phase.py").is_file())
    check("phase0_scan.py", (skill_dir / "scripts" / "phase0_scan.py").is_file())
    check("bootstrap_roles.py", (skill_dir / "scripts" / "bootstrap_roles.py").is_file())
    check("check_agents.py", (skill_dir / "scripts" / "check_agents.py").is_file())

    for tmpl in ("overview.md", "conversation.md", "proposal.md", "tasks.md", "ledger.md"):
        check(f"template:{tmpl}", (skill_dir / "templates" / tmpl).is_file())

    for rep in ("coder-report.md", "artist-report.md", "tester-report.md", "reviewer-report.md"):
        check(f"report:{rep}", (skill_dir / "templates" / "reports" / rep).is_file())

    check(
        "workflow:clsh-task-pipeline.js",
        (skill_dir / "workflows" / "clsh-task-pipeline.js").is_file(),
    )

    for ref in (
        "phases.md",
        "pitfalls.md",
        "wiki-search.md",
        "mimo-capabilities.md",
        "superpowers-diff.md",
        "pipeline-runtime.md",
    ):
        check(f"reference:{ref}", (skill_dir / "references" / ref).is_file())

    for agent in ("clsh-coder.md", "clsh-artist.md", "clsh-tester.md", "clsh-reviewer.md", "clsh-scout.md"):
        check(f"agent:{agent}", (skill_dir / "agents" / agent).is_file())

    locales = skill_dir / "locales"
    check("locales/zh-CN.json", (locales / "zh-CN.json").is_file())
    check("locales/en-US.json", (locales / "en-US.json").is_file())

    vault_ok = False
    try:
        vault_ok = VAULT.is_dir()
    except OSError:
        vault_ok = False
    check("vault_root", vault_ok, str(VAULT))
    if vault_ok:
        check("vault/raw/projects", (VAULT / "raw" / "projects").is_dir())
        check("vault/wiki", (VAULT / "wiki").is_dir())
        check("vault/wiki/INDEX.md", (VAULT / "wiki" / "INDEX.md").is_file())
        check("vault/wiki/hot.md", (VAULT / "wiki" / "hot.md").is_file())
        check("vault/SCHEMA.md", (VAULT / "SCHEMA.md").is_file())

    check("git", shutil.which("git") is not None)

    print()
    if not py_ok:
        print("Result: FAIL — Python 3.8+ required")
        return 1
    if not vault_ok:
        print("Result: DEGRADED — vault unreachable; local coding still possible, Obsidian docs blocked")
        return 1

    print("Result: READY — Level B+ (gates + role agents + scout evidence + Obsidian vault)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
