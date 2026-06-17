#!/usr/bin/env python3
"""
gate_utils.py - Shared utilities for Hermes Agent gate scripts.

Provides common operations used by gate-phaseN.py scripts:
- Gate state directory resolution
- Confirmation code generation (hash-based, unforgable)
- Marker file management
- File discovery in project changes
- Structured JSON output
- Config loading
"""

import hashlib
import json
import os
import re
import secrets
import sys
import time
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Gate directory resolution
# ---------------------------------------------------------------------------

def get_gate_dir() -> Path:
    """Resolve the gate-state directory.

    Order of precedence:
      1. GATE_DIR environment variable
      2. $HERMES_HOME/gate-state
      3. ~/.hermes/gate-state  (default)
    """
    env_gate = os.environ.get("GATE_DIR")
    if env_gate:
        return Path(env_gate)

    hermes_home = os.environ.get("HERMES_HOME", Path.home() / ".hermes")
    return Path(hermes_home) / "gate-state"


# ---------------------------------------------------------------------------
# 2. Confirmation code generation (hash-based)
# ---------------------------------------------------------------------------

def generate_code(project_dir: str, phase: str) -> str:
    """Generate a 6-char uppercase confirmation code.

    The code is the first 6 hex chars of:
        sha256(project_dir + phase + timestamp + random_salt)

    This makes codes deterministic for the same input but practically
    unforgable without knowing the exact salt and timestamp.
    """
    timestamp = str(int(time.time()))
    salt = secrets.token_hex(16)
    payload = f"{project_dir}{phase}{timestamp}{salt}"
    digest = hashlib.sha256(payload.encode()).hexdigest()
    return digest[:6].upper()


# ---------------------------------------------------------------------------
# 3. Marker file management
# ---------------------------------------------------------------------------

def write_marker(phase: str, project_dir: str, code: str,
                 meta: dict | None = None) -> Path:
    """Write a gate-state marker file.

    File location: <GATE_DIR>/<project_dir_slug>/<phase>.json

    The marker records:
      - phase name
      - project directory
      - confirmation code
      - ISO timestamp
      - optional extra metadata
    """
    gate_dir = get_gate_dir()
    slug = re.sub(r"[^a-zA-Z0-9_-]", "_", project_dir.rstrip("/"))
    marker_dir = gate_dir / slug
    marker_dir.mkdir(parents=True, exist_ok=True)

    marker_path = marker_dir / f"{phase}.json"
    marker = {
        "phase": phase,
        "project_dir": project_dir,
        "code": code,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    if meta:
        marker.update(meta)

    marker_path.write_text(json.dumps(marker, indent=2) + "\n")
    return marker_path


# ---------------------------------------------------------------------------
# 4. Find latest change directory
# ---------------------------------------------------------------------------

def find_latest_change(project_dir: str) -> Path | None:
    """Find the newest directory under <project_dir>/changes/.

    Returns the path to the most recently modified subdirectory,
    or None if no changes directory or no subdirectories exist.
    """
    changes_root = Path(project_dir) / "changes"
    if not changes_root.is_dir():
        return None

    dirs = sorted(
        [d for d in changes_root.iterdir() if d.is_dir()],
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    return dirs[0] if dirs else None


# ---------------------------------------------------------------------------
# 5. Find file in changes or project root
# ---------------------------------------------------------------------------

def find_file_in_changes(project_dir: str, names: list[str]) -> Path | None:
    """Search for the first matching file name in changes/*/ and project root.

    Search order:
      1. Newest changes/*/ directories first (via find_latest_change heuristic)
      2. Project root

    Args:
        project_dir: project root directory
        names: list of possible filenames to look for (e.g. ["overview.md", "PRODUCT.md"])

    Returns:
        Path to the first found file, or None.
    """
    project_root = Path(project_dir)

    # Search changes directories (newest first)
    changes_root = project_root / "changes"
    if changes_root.is_dir():
        change_dirs = sorted(
            [d for d in changes_root.iterdir() if d.is_dir()],
            key=lambda d: d.stat().st_mtime,
            reverse=True,
        )
        for cdir in change_dirs:
            for name in names:
                candidate = cdir / name
                if candidate.is_file():
                    return candidate

    # Search project root
    for name in names:
        candidate = project_root / name
        if candidate.is_file():
            return candidate

    return None


# ---------------------------------------------------------------------------
# 6. Structured JSON output
# ---------------------------------------------------------------------------

def output_result(gate_name: str, passed: bool, errors: list[str] | None = None,
                  code: str | None = None) -> None:
    """Print a structured JSON result to stdout.

    Always exits with the appropriate code:
        0 on PASS, 1 on FAIL
    """
    result = {
        "gate": gate_name,
        "passed": passed,
        "errors": errors or [],
    }
    if code:
        result["code"] = code

    print(json.dumps(result, indent=2))
    sys.exit(0 if passed else 1)


# ---------------------------------------------------------------------------
# 7. Config loading
# ---------------------------------------------------------------------------

def load_config() -> dict:
    """Load config.json from the skill directory.

    Searches for config.json in the same directory as this module (scripts/),
    then in the parent skill directory (e.g. skills/clsh-project/).

    Returns empty dict if not found.
    """
    module_dir = Path(__file__).resolve().parent
    skill_dir = module_dir.parent  # scripts/ -> skill root

    for candidate in [skill_dir / "config.json", module_dir / "config.json"]:
        if candidate.is_file():
            with open(candidate, "r", encoding="utf-8") as f:
                return json.load(f)

    return {}


# ---------------------------------------------------------------------------
# 8. Project docs directory resolution
# ---------------------------------------------------------------------------

def get_project_docs_dir(project_dir: str) -> Path:
    """Resolve the project docs directory.

    Order of precedence:
      1. PROJECT_DOCS_DIR environment variable
      2. project_docs_dir from config.json
      3. <project_dir>/changes/<latest>/  (fall back to latest change dir)
      4. <project_dir> itself
    """
    env_docs = os.environ.get("PROJECT_DOCS_DIR")
    if env_docs:
        return Path(env_docs)

    config = load_config()
    cfg_docs = config.get("project_docs_dir")
    if cfg_docs:
        p = Path(cfg_docs)
        if not p.is_absolute():
            p = Path(__file__).resolve().parent.parent / p
        if p.is_dir():
            return p

    latest = find_latest_change(project_dir)
    if latest:
        return latest

    return Path(project_dir)
