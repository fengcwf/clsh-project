#!/usr/bin/env python3
"""
clsh-project 环境自检脚本
检查当前环境能力，输出可用功能等级。

用法: python3 env-check.py [--config config.json]
输出: JSON 格式检查结果 + 人类可读摘要
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

def check_python():
    v = sys.version_info
    ok = v.major >= 3 and v.minor >= 8
    return {"name": "python3", "ok": ok, "version": f"{v.major}.{v.minor}.{v.micro}",
            "required": ">=3.8", "critical": True}

def check_hermes():
    has_delegate = shutil.which("hermes") is not None
    return {"name": "hermes_agent", "ok": has_delegate, "critical": True,
            "note": "Required for delegate_task (subagent spawning)"}

def check_kanban():
    try:
        r = subprocess.run(["hermes", "kanban", "--help"], capture_output=True, timeout=10)
        ok = r.returncode == 0
    except Exception:
        ok = False
    return {"name": "kanban", "ok": ok, "critical": False,
            "note": "Enhanced task dispatch with skill injection. Falls back to delegate_task if missing."}

def check_obsidian_vault():
    vault = os.environ.get("OBSIDIAN_VAULT", "")
    if not vault:
        # Try common locations
        for p in ["/mnt/obsidian", os.path.expanduser("~/Obsidian"), os.path.expanduser("~/obsidian")]:
            if os.path.isdir(p):
                vault = p
                break
    exists = vault and os.path.isdir(vault)
    return {"name": "obsidian_vault", "ok": exists, "critical": False,
            "path": vault or "not found",
            "note": "Optional. Used for wiki archiving. Falls back to local docs/ if missing."}

def check_gate_enforcer():
    """Check if Gate Enforcer plugin is loaded (Hermes-specific)."""
    config_path = os.path.expanduser("~/.hermes/config.yaml")
    if not os.path.exists(config_path):
        return {"name": "gate_enforcer_plugin", "ok": False, "critical": False,
                "note": "Optional. Physical block on code generation without gate pass."}
    try:
        with open(config_path) as f:
            content = f.read()
        ok = "gate-enforcer" in content or "gate_enforcer" in content
    except Exception:
        ok = False
    return {"name": "gate_enforcer_plugin", "ok": ok, "critical": False,
            "note": "Optional. Physical block on code generation without gate pass."}

def check_project_docs_dir(config):
    docs_dir = config.get("project_docs_dir", "./project-docs")
    if not os.path.isabs(docs_dir):
        docs_dir = os.path.abspath(docs_dir)
    writable = os.access(os.path.dirname(docs_dir) if not os.path.exists(docs_dir) else docs_dir, os.W_OK)
    return {"name": "project_docs_dir", "ok": writable, "critical": True,
            "path": docs_dir, "writable": writable,
            "note": "Where project documentation is stored."}

def check_terminal():
    return {"name": "terminal", "ok": True, "critical": True,
            "note": "Shell execution (required for gate scripts)"}

def check_file_ops():
    return {"name": "file_ops", "ok": True, "critical": True,
            "note": "File read/write (required for docs)"}

def determine_level(checks):
    """Determine capability level from check results."""
    critical_ok = all(c["ok"] for c in checks if c.get("critical"))
    if not critical_ok:
        return "UNAVAILABLE", "Missing critical dependencies"

    has_kanban = next(c for c in checks if c["name"] == "kanban")["ok"]
    has_enforcer = next(c for c in checks if c["name"] == "gate_enforcer_plugin")["ok"]

    if has_kanban and has_enforcer:
        return "A", "Full capability (kanban + gate-enforcer + mechanical gates)"
    elif has_kanban or has_enforcer:
        return "B", "Standard capability (delegate_task + mechanical gates)"
    else:
        return "B", "Standard capability (delegate_task + mechanical gates)"

def load_config(config_path):
    if config_path and os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return {"project_docs_dir": "./project-docs"}

def main():
    config_path = None
    if len(sys.argv) > 2 and sys.argv[1] == "--config":
        config_path = sys.argv[2]
    config = load_config(config_path)

    checks = [
        check_python(),
        check_terminal(),
        check_file_ops(),
        check_hermes(),
        check_kanban(),
        check_obsidian_vault(),
        check_gate_enforcer(),
        check_project_docs_dir(config),
    ]

    level, level_desc = determine_level(checks)

    result = {
        "level": level,
        "level_description": level_desc,
        "checks": checks,
        "config_loaded": config_path or "defaults",
    }

    # Human-readable output
    print("=" * 60)
    print("  clsh-project Environment Check")
    print("=" * 60)
    print()
    for c in checks:
        icon = "✅" if c["ok"] else ("❌" if c.get("critical") else "⚠️")
        name = c["name"].ljust(25)
        note = c.get("note", "")
        extra = ""
        if "version" in c:
            extra = f" (v{c['version']})"
        if "path" in c and isinstance(c["path"], str) and c["path"] not in ("not found",):
            extra += f" [{c['path']}]"
        print(f"  {icon} {name}{extra}")
        if not c["ok"] and note:
            print(f"     → {note}")
    print()
    print(f"  Capability Level: {level} — {level_desc}")
    print()

    if level == "UNAVAILABLE":
        print("  ⚠️  Cannot run clsh-project. Install missing critical dependencies.")
        sys.exit(1)
    elif level == "A":
        print("  🚀 Full capability. All features available.")
    elif level == "B":
        print("  ✅ Standard capability. Core workflow + mechanical gates work.")
        missing = [c["name"] for c in checks if not c["ok"] and not c.get("critical")]
        if missing:
            print(f"  💡 Optional features not available: {', '.join(missing)}")

    # JSON output for programmatic use
    print()
    print("--- JSON ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
