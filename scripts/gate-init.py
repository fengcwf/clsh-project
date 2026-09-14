#!/usr/bin/env python3
"""
gate-init.py - Project Infrastructure Init Gate (项目基础设施初始化门禁)

Validates that project infrastructure was created and CONFIRMED by the user
before Phase 0 may start. Checks:
  1. <project_dir>/.cp-init.json exists and has all required fields
  2. user_confirmed is true (directory was confirmed with the user)
  3. kanban board actually exists (hermes kanban boards list)
  4. all 5 project bots exist (hermes profile list)
  5. hermes project is registered (hermes project list)

Usage:
    python gate-init.py <project_dir>            # run checks, emit pending code
    python gate-init.py <project_dir> --verify CODE

Output: JSON to stdout, exit 0 on PASS, 1 on FAIL.
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

GATE_NAME = "init"
MANIFEST_NAME = ".cp-init.json"
REQUIRED_ROLES = ["artist", "coder", "scout", "tester", "reviewer"]
REQUIRED_FIELDS = ["project_name", "slug", "directory", "board", "bots",
                   "user_confirmed", "created_at"]
HERMES_TIMEOUT = 30


def run_hermes(args: list[str]) -> tuple[bool, str]:
    """Run a hermes CLI command. Returns (ok, combined_output)."""
    try:
        proc = subprocess.run(
            ["hermes"] + args,
            capture_output=True, text=True, timeout=HERMES_TIMEOUT,
        )
        return proc.returncode == 0, (proc.stdout or "") + (proc.stderr or "")
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        return False, str(e)


def load_manifest(project_dir: str) -> tuple[dict | None, list[str]]:
    """Load and structurally validate .cp-init.json."""
    errors = []
    manifest_path = Path(project_dir) / MANIFEST_NAME
    if not manifest_path.is_file():
        return None, [
            f"{MANIFEST_NAME} NOT FOUND in {project_dir} — "
            "run the init flow (init-project.md) before Phase 0. "
            "Directory must be confirmed with the user every time."
        ]

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return None, [f"{MANIFEST_NAME} parse error: {e}"]

    for field in REQUIRED_FIELDS:
        if field not in data or data[field] in (None, "", []):
            errors.append(f"{MANIFEST_NAME}: missing/empty field '{field}'")

    if data.get("user_confirmed") is not True:
        errors.append(
            f"{MANIFEST_NAME}: user_confirmed must be true — "
            "project directory must be confirmed with the user (IL-INIT-1)"
        )

    bots = data.get("bots", {})
    if isinstance(bots, dict):
        for role in REQUIRED_ROLES:
            if not bots.get(role):
                errors.append(f"{MANIFEST_NAME}: bots.{role} missing")
    return data, errors


def check_directory(project_dir: str, manifest: dict) -> list[str]:
    """Directory in manifest must match the actual project dir."""
    errors = []
    declared = str(Path(manifest.get("directory", "")).resolve())
    actual = str(Path(project_dir).resolve())
    if declared != actual:
        errors.append(
            f"{MANIFEST_NAME}: directory '{declared}' does not match "
            f"actual project dir '{actual}'"
        )
    return errors


def check_board(manifest: dict) -> list[str]:
    """Verify the kanban board exists."""
    board = manifest.get("board", "")
    ok, out = run_hermes(["kanban", "boards", "list"])
    if not ok:
        return [f"hermes kanban boards list failed: {out.strip()[:200]}"]
    if board not in out:
        return [f"kanban board '{board}' NOT FOUND — create it: "
                f"hermes kanban boards create {board}"]
    return []


def check_bots(manifest: dict) -> list[str]:
    """Verify all 5 project bot profiles exist."""
    ok, out = run_hermes(["profile", "list"])
    if not ok:
        return [f"hermes profile list failed: {out.strip()[:200]}"]
    errors = []
    for role in REQUIRED_ROLES:
        bot = manifest.get("bots", {}).get(role, "")
        if bot and bot not in out:
            errors.append(
                f"bot profile '{bot}' NOT FOUND — create it: "
                f"hermes profile create {bot} --clone-from {role}"
            )
    return errors


def check_project(manifest: dict) -> list[str]:
    """Verify the hermes project is registered."""
    ok, out = run_hermes(["project", "list"])
    if not ok:
        return [f"hermes project list failed: {out.strip()[:200]}"]
    slug = manifest.get("slug", "")
    if slug and slug not in out:
        return [f"hermes project '{slug}' NOT FOUND — create it: "
                f"hermes project create \"{manifest.get('project_name', slug)}\" "
                f"--slug {slug} --primary {manifest.get('directory', '')} "
                f"--board {manifest.get('board', slug)} --use"]
    return []


def run_gate(project_dir: str) -> None:
    """Run all init gate checks."""
    all_errors = []

    manifest, errors = load_manifest(project_dir)
    all_errors.extend(errors)

    if manifest is not None:
        all_errors.extend(check_directory(project_dir, manifest))
        all_errors.extend(check_board(manifest))
        all_errors.extend(check_bots(manifest))
        all_errors.extend(check_project(manifest))

    if not all_errors and manifest is not None:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_pending(GATE_NAME, project_dir, code)
        gu.output_result(GATE_NAME, True, code=code, pending=True,
                         meta={"slug": manifest.get("slug"),
                               "board": manifest.get("board"),
                               "bots": manifest.get("bots")})
    else:
        gu.output_result(GATE_NAME, False, errors=all_errors)


def main():
    if len(sys.argv) < 2:
        gu.output_result(GATE_NAME, False,
                         errors=["Usage: gate-init.py <project_dir> [--verify CODE]"])

    project_dir = sys.argv[1]
    if not Path(project_dir).is_dir():
        gu.output_result(GATE_NAME, False,
                         errors=[f"Project directory not found: {project_dir} — "
                                 "create it and confirm with the user first "
                                 "(init-project.md Step 1-2)"])

    if len(sys.argv) >= 4 and sys.argv[2] == "--verify":
        code = sys.argv[3]
        ok, msg, _ = gu.verify_and_write_marker(GATE_NAME, project_dir, code)
        if ok:
            # Record user confirmation time in the manifest
            manifest_path = Path(project_dir) / MANIFEST_NAME
            try:
                data = json.loads(manifest_path.read_text(encoding="utf-8"))
                data["verified_at"] = datetime.now(timezone.utc).isoformat()
                manifest_path.write_text(
                    json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")
            except (json.JSONDecodeError, OSError):
                pass  # marker already written; manifest edit is cosmetic
        gu.output_result(GATE_NAME, ok, errors=[msg] if not ok else None,
                         code=code if ok else None)
        return

    run_gate(project_dir)


if __name__ == "__main__":
    main()
