#!/usr/bin/env python3
"""Mechanical Phase 0 scan — zero LLM. Mirrors clsh phase0-scan.py idea.

Usage:
  python phase0_scan.py <project_dir> [--out phase0-data.json]

Writes JSON next to the project container (or --out) describing:
  structure, tech stack hints, vault project presence, open-question seed tags.

LLM must READ this JSON and cite it in phase0-research.md / overview.md.
Inventing stack/structure not present in JSON is forbidden.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

STACK_MARKERS = {
    "python": ["pyproject.toml", "requirements.txt", "setup.py", "Pipfile"],
    "node": ["package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"],
    "go": ["go.mod"],
    "rust": ["Cargo.toml"],
    "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
    "dotnet": ["*.csproj", "*.sln"],
    "php": ["composer.json"],
    "docker": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
}

DOC_MARKERS = ["README.md", "README.rst", "AGENTS.md", "CLAUDE.md", "docs"]


def list_dirs(root: Path, limit: int = 40) -> list[str]:
    out = []
    try:
        for p in sorted(root.iterdir()):
            if p.name.startswith("."):
                continue
            if p.is_dir():
                out.append(p.name + "/")
            else:
                out.append(p.name)
            if len(out) >= limit:
                out.append("...")
                break
    except OSError:
        pass
    return out


def detect_stack(root: Path) -> list[str]:
    found = []
    for stack, markers in STACK_MARKERS.items():
        for m in markers:
            if "*" in m:
                if any(root.glob(m)):
                    found.append(stack)
                    break
            elif (root / m).exists():
                found.append(stack)
                break
    return found


def detect_vault(project_dir: Path) -> dict:
    # project_dir may already be the vault project container
    info = {
        "is_vault_container": False,
        "has_overview": False,
        "has_sot": False,
        "has_changes": False,
        "wiki_sibling": False,
    }
    if project_dir.name == "projects" or (project_dir / "overview.md").is_file():
        info["is_vault_container"] = True
    info["has_overview"] = (project_dir / "overview.md").is_file()
    info["has_sot"] = (project_dir / "source-of-truth").is_dir()
    info["has_changes"] = (project_dir / "changes").is_dir()
    # heuristic: walk up for Obsidian wiki
    for parent in project_dir.parents:
        if parent.name == "Obsidian" or (parent / "wiki" / "INDEX.md").is_file():
            info["wiki_sibling"] = (parent / "wiki" / "INDEX.md").is_file()
            break
    return info


def seed_questions(root: Path, stack: list[str]) -> list[dict]:
    """Mechanical seeds — not answers. LLM expands; gate checks count/dims."""
    q: list[dict] = [
        {"id": 1, "dim": "功能", "text": "目标用户与核心使用场景是什么？"},
        {"id": 2, "dim": "功能", "text": "本次变更的输入/输出契约是什么？"},
        {"id": 3, "dim": "边界", "text": "明确不做什么（Non-goals）？"},
        {"id": 4, "dim": "异常", "text": "失败/超时/部分成功时用户看到什么？"},
        {"id": 5, "dim": "约束", "text": "性能上限、数据量、并发要求？"},
        {"id": 6, "dim": "约束", "text": "安全/权限/合规硬约束？"},
        {"id": 7, "dim": "技术", "text": "必须兼容的现有接口或数据格式？"},
        {"id": 8, "dim": "技术", "text": "验收如何被机械验证（测试/脚本）？"},
    ]
    if "python" in stack:
        q.append({"id": 9, "dim": "技术", "text": "Python 最低版本与依赖锁定策略？"})
    if "node" in stack:
        q.append({"id": 9, "dim": "技术", "text": "Node/包管理器与构建命令是什么？"})
    if not stack:
        q.append({"id": 9, "dim": "技术", "text": "技术栈选型依据与备选方案？"})
    q.append({"id": 10, "dim": "边界", "text": "与现有模块的边界在哪、谁负责？"})
    return q


def scan(project_dir: Path) -> dict:
    root = project_dir.resolve()
    if not root.is_dir():
        raise SystemExit(f"not a directory: {root}")

    git_info: dict = {"present": False}
    git_dir = root / ".git"
    if git_dir.exists():
        git_info["present"] = True
        # branch via HEAD file if possible
        head = git_dir / "HEAD"
        try:
            text = head.read_text(encoding="utf-8", errors="replace").strip()
            if text.startswith("ref:"):
                git_info["branch"] = text.split("/", 2)[-1]
            else:
                git_info["head"] = text[:12]
        except OSError:
            pass

    stack = detect_stack(root)
    md_files = 0
    code_files = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", ".venv", "venv", "__pycache__"}]
        for fn in filenames:
            if fn.endswith(".md"):
                md_files += 1
            elif fn.endswith((".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".php")):
                code_files += 1

    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project_dir": str(root),
        "top_level": list_dirs(root),
        "tech_stack": stack,
        "git": git_info,
        "docs": [m for m in DOC_MARKERS if (root / m).exists() or (root / m).is_dir()],
        "counts": {"markdown": md_files, "code": code_files},
        "vault": detect_vault(root),
        "seed_open_questions": seed_questions(root, stack),
        "notes": [
            "This file is mechanical. Do not invent structure not listed here.",
            "phase0-research.md must reference project_dir, tech_stack, and cite this JSON.",
        ],
    }
    return data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--out", default=None, help="output json path (default: <project>/phase0-data.json)")
    args = ap.parse_args()
    root = Path(args.project_dir).expanduser()
    data = scan(root)
    out = Path(args.out) if args.out else root / "phase0-data.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"WROTE {out}")
    print(f"  tech_stack={data['tech_stack']}")
    print(f"  seed_questions={len(data['seed_open_questions'])}")
    print(f"  vault={data['vault']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
