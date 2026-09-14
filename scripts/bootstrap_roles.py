#!/usr/bin/env python3
"""Bootstrap clsh role agents + workflow into a code project.

Usage:
  python bootstrap_roles.py <code_project_dir> [--force]

Copies:
  agents/clsh-*.md           -> <code>/.mimocode/agent/
  workflows/clsh-task-pipeline.js -> <code>/.mimocode/workflows/

Does NOT copy into Obsidian vault containers.
Exit 0 = copied/skipped-ok, 1 = error.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def skill_root() -> Path:
    return Path.home() / ".claude" / "skills" / "clsh-project-mimo"


def copy_tree(src_files: list[Path], dest: Path, force: bool) -> list[str]:
    dest.mkdir(parents=True, exist_ok=True)
    actions = []
    for src in src_files:
        tgt = dest / src.name
        if tgt.exists() and not force:
            actions.append(f"SKIP {tgt}")
            continue
        shutil.copy2(src, tgt)
        actions.append(f"COPY {src.name} -> {tgt}")
    return actions


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("code_project_dir")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    root = skill_root()
    proj = Path(args.code_project_dir).expanduser().resolve()
    if not proj.is_dir():
        print(f"ERROR: not a directory: {proj}")
        return 1

    agents_src = root / "agents"
    wf_src = root / "workflows" / "clsh-task-pipeline.js"
    if not agents_src.is_dir():
        print(f"ERROR: missing {agents_src}")
        return 1

    agent_files = sorted(agents_src.glob("clsh-*.md"))
    if not agent_files:
        print(f"ERROR: no clsh-*.md under {agents_src}")
        return 1

    print(f"project: {proj}")
    print(f"skill:   {root}")
    for line in copy_tree(agent_files, proj / ".mimocode" / "agent", args.force):
        print(line)

    if wf_src.is_file():
        for line in copy_tree([wf_src], proj / ".mimocode" / "workflows", args.force):
            print(line)
    else:
        print(f"WARN: workflow missing {wf_src}")

    reports = proj / ".clsh" / "reports"
    reviews = proj / ".clsh" / "reviews"
    reports.mkdir(parents=True, exist_ok=True)
    reviews.mkdir(parents=True, exist_ok=True)
    print(f"MKDIR {reports}")
    print(f"MKDIR {reviews}")

    gitignore = proj / ".gitignore"
    note = ".clsh/reports/\n.clsh/reviews/\n"
    try:
        existing = gitignore.read_text(encoding="utf-8") if gitignore.is_file() else ""
        if ".clsh/" not in existing and ".clsh/reports/" not in existing:
            gitignore.write_text(existing + ("\n" if existing and not existing.endswith("\n") else "") + note, encoding="utf-8")
            print(f"APPEND {gitignore} (.clsh/reports|reviews)")
        else:
            print(f"SKIP gitignore already mentions .clsh")
    except OSError as exc:
        print(f"WARN: could not update .gitignore ({exc})")

    print()
    print("Next:")
    print("  1) Restart conversation or verify agent list / @ autocomplete for clsh-coder")
    print("  2) Copy agents into every other code project you run in parallel")
    print("  3) Phase 4: install done before first pipeline run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
