#!/usr/bin/env python3
"""
phase0-scan.py — Phase 0 纯机械扫描脚本

零 LLM 依赖。扫描项目目录和 Obsidian 知识库，输出结构化 JSON。
LLM 在后续步骤中读取此 JSON 做分析，不参与扫描本身。

Usage:
    python3 phase0-scan.py <project_dir> [--obsidian PATH]

Output: JSON to stdout + 写入 <project_dir>/changes/<latest>/phase0-data.json
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. 项目目录扫描
# ---------------------------------------------------------------------------

def scan_project_dir(project_dir: str) -> dict:
    """扫描项目目录结构和关键文件。"""
    root = Path(project_dir)
    result = {
        "project_dir": str(root),
        "exists": root.is_dir(),
        "is_new_project": True,
        "file_count": 0,
        "dir_count": 0,
        "key_files": {},
        "tech_stack": [],
        "languages": [],
    }

    if not root.is_dir():
        return result

    # Count files and dirs
    for item in root.rglob("*"):
        if item.is_file():
            result["file_count"] += 1
        elif item.is_dir():
            result["dir_count"] += 1

    # Check key files
    KEY_FILES = {
        "package.json": "node",
        "requirements.txt": "python",
        "pyproject.toml": "python",
        "Cargo.toml": "rust",
        "go.mod": "go",
        "Dockerfile": "docker",
        "docker-compose.yml": "docker",
        "Makefile": "make",
        ".gitignore": "git",
        "README.md": "docs",
        "PRODUCT.md": "clsh-project",
        "TECH.md": "clsh-project",
        "overview.md": "clsh-project",
        "tasks.md": "clsh-project",
    }

    for fname, category in KEY_FILES.items():
        fpath = root / fname
        if fpath.is_file():
            result["key_files"][fname] = {
                "category": category,
                "size": fpath.stat().st_size,
                "modified": datetime.fromtimestamp(
                    fpath.stat().st_mtime, tz=timezone.utc
                ).isoformat(),
            }

    # Detect if this is an optimization project (has clsh-project artifacts)
    clsh_artifacts = ["PRODUCT.md", "TECH.md", "overview.md", "tasks.md"]
    found_artifacts = [f for f in clsh_artifacts if (root / f).is_file()]
    if found_artifacts:
        result["is_new_project"] = False
        result["existing_artifacts"] = found_artifacts

    # Detect tech stack from key files
    if "package.json" in result["key_files"]:
        try:
            pkg = json.loads((root / "package.json").read_text(encoding="utf-8"))
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if any(k in deps for k in ["vue", "nuxt"]):
                result["tech_stack"].append("vue")
            if any(k in deps for k in ["react", "next"]):
                result["tech_stack"].append("react")
            if any(k in deps for k in ["express", "fastify", "koa"]):
                result["tech_stack"].append("node-backend")
            if "typescript" in deps:
                result["tech_stack"].append("typescript")
        except (json.JSONDecodeError, OSError):
            pass

    if "requirements.txt" in result["key_files"] or "pyproject.toml" in result["key_files"]:
        result["tech_stack"].append("python")

    # Detect languages by file extensions
    LANG_EXTS = {
        ".py": "python", ".js": "javascript", ".ts": "typescript",
        ".vue": "vue", ".jsx": "react", ".tsx": "react",
        ".go": "go", ".rs": "rust", ".php": "php",
        ".java": "java", ".rb": "ruby", ".sh": "shell",
        ".html": "html", ".css": "css", ".scss": "scss",
        ".sql": "sql", ".yaml": "yaml", ".json": "json",
    }
    lang_counts: dict[str, int] = {}
    for item in root.rglob("*"):
        if item.is_file() and item.suffix in LANG_EXTS:
            lang = LANG_EXTS[item.suffix]
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
    result["languages"] = sorted(lang_counts.keys(), key=lambda k: -lang_counts[k])[:5]

    # Scan changes/ directory
    changes_dir = root / "changes"
    if changes_dir.is_dir():
        change_dirs = sorted(
            [d for d in changes_dir.iterdir() if d.is_dir()],
            key=lambda d: d.stat().st_mtime,
            reverse=True,
        )
        result["changes_dirs"] = [d.name for d in change_dirs[:5]]

    return result


# ---------------------------------------------------------------------------
# 2. Obsidian 知识库扫描
# ---------------------------------------------------------------------------

OBSIDIAN_DEFAULT = "/mnt/unraid_data/Obsidian"

def scan_obsidian(project_data: dict, obsidian_path: str) -> dict:
    """用项目数据中的关键词 grep Obsidian 知识库。"""
    result = {
        "obsidian_path": obsidian_path,
        "available": Path(obsidian_path).is_dir(),
        "grep_results": [],
        "solutions_matches": [],
        "project_matches": [],
    }

    if not result["available"]:
        return result

    # Build search keywords from project data
    keywords = set()

    # From tech stack
    keywords.update(project_data.get("tech_stack", []))

    # From languages
    keywords.update(project_data.get("languages", []))

    # From key file categories
    for fname, info in project_data.get("key_files", {}).items():
        keywords.add(info["category"])

    # From project dir name
    project_name = Path(project_data["project_dir"]).name
    # Split on common separators
    for part in re.split(r"[-_/]", project_name):
        if len(part) > 2:
            keywords.add(part.lower())

    if not keywords:
        result["note"] = "No keywords extracted from project data"
        return result

    result["keywords_used"] = sorted(keywords)

    # Grep wiki/solutions/
    solutions_dir = Path(obsidian_path) / "wiki" / "solutions"
    if solutions_dir.is_dir():
        for kw in keywords:
            try:
                proc = subprocess.run(
                    ["grep", "-rl", "-i", kw, str(solutions_dir)],
                    capture_output=True, text=True, timeout=10,
                )
                for line in proc.stdout.strip().split("\n"):
                    if line and line not in [r["path"] for r in result["solutions_matches"]]:
                        fpath = Path(line)
                        result["solutions_matches"].append({
                            "path": line,
                            "keyword": kw,
                            "name": fpath.stem,
                        })
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

    # Grep raw/projects/
    raw_projects = Path(obsidian_path) / "raw" / "projects"
    if raw_projects.is_dir():
        for kw in list(keywords)[:5]:  # Limit to 5 keywords to avoid spam
            try:
                proc = subprocess.run(
                    ["grep", "-rl", "-i", kw, str(raw_projects)],
                    capture_output=True, text=True, timeout=15,
                )
                for line in proc.stdout.strip().split("\n"):
                    if line and line not in [r["path"] for r in result["project_matches"]]:
                        result["project_matches"].append({
                            "path": line,
                            "keyword": kw,
                        })
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

    # Read wiki/INDEX.md if exists
    index_path = Path(obsidian_path) / "wiki" / "INDEX.md"
    if index_path.is_file():
        try:
            content = index_path.read_text(encoding="utf-8", errors="replace")
            # Find sections matching keywords
            for kw in keywords:
                if kw.lower() in content.lower():
                    result["grep_results"].append({
                        "source": "wiki/INDEX.md",
                        "keyword": kw,
                        "matched": True,
                    })
        except OSError:
            pass

    # Limit results
    result["solutions_matches"] = result["solutions_matches"][:20]
    result["project_matches"] = result["project_matches"][:20]

    return result


# ---------------------------------------------------------------------------
# 3. 历史教训扫描
# ---------------------------------------------------------------------------

def scan_learnings(project_dir: str) -> dict:
    """扫描项目 learnings/ 和 clsh-project pitfalls。"""
    result = {
        "learnings_files": [],
        "pitfalls_count": 0,
        "matched_pitfalls": [],
    }

    # Scan project learnings/
    learnings_dir = Path(project_dir) / "learnings"
    if learnings_dir.is_dir():
        for f in sorted(learnings_dir.glob("*.md")):
            result["learnings_files"].append({
                "name": f.name,
                "size": f.stat().st_size,
            })

    # Scan clsh-project pitfalls
    pitfalls_path = Path.home() / ".hermes" / "skills" / "productivity" / "clsh-project" / "references" / "pitfalls-common.md"
    if pitfalls_path.is_file():
        try:
            content = pitfalls_path.read_text(encoding="utf-8", errors="replace")
            # Count pitfall entries (lines starting with | #)
            pitfall_lines = [l for l in content.splitlines() if re.match(r"\|\s*\d+\s*\|", l)]
            result["pitfalls_count"] = len(pitfall_lines)
        except OSError:
            pass

    return result


# ---------------------------------------------------------------------------
# 4. Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python3 phase0-scan.py <project_dir> [--obsidian PATH]"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    project_dir = sys.argv[1]
    obsidian_path = OBSIDIAN_DEFAULT

    if "--obsidian" in sys.argv:
        idx = sys.argv.index("--obsidian")
        if idx + 1 < len(sys.argv):
            obsidian_path = sys.argv[idx + 1]

    # Run scans
    project_data = scan_project_dir(project_dir)
    obsidian_data = scan_obsidian(project_data, obsidian_path)
    learnings_data = scan_learnings(project_dir)

    # Combine results
    result = {
        "scan_time": datetime.now(timezone.utc).isoformat(),
        "scanner_version": "1.0.0",
        "project": project_data,
        "obsidian": obsidian_data,
        "learnings": learnings_data,
    }

    # Write to project directory
    changes_dir = Path(project_dir) / "changes"
    if not changes_dir.is_dir():
        changes_dir.mkdir(parents=True, exist_ok=True)

    # Find or create latest change dir
    change_dirs = sorted(
        [d for d in changes_dir.iterdir() if d.is_dir()],
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    if change_dirs:
        output_dir = change_dirs[0]
    else:
        output_dir = changes_dir / datetime.now().strftime("%Y%m%d-phase0")
        output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "phase0-data.json"
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    result["output_file"] = str(output_path)

    # Print to stdout
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
