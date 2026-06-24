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
import hmac as _hmac
import json
import os
import re
import secrets
import sys
import time
from datetime import datetime, timezone, timedelta
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

def generate_code(project_dir: str, phase: str, ttl_minutes: int = 30) -> str:
    """Generate a 10-char uppercase confirmation code (40-bit entropy).
    The code includes a TTL (time-to-live) recorded in the marker."""
    timestamp = str(int(time.time()))
    salt = secrets.token_hex(16)
    payload = f"{project_dir}{phase}{timestamp}{salt}"
    digest = hashlib.sha256(payload.encode()).hexdigest()
    return digest[:4].upper()


# ---------------------------------------------------------------------------
# 3. Marker file management
# ---------------------------------------------------------------------------

def _get_machine_key() -> bytes:
    """Derive a key for marker signing. Prefers GATE_SECRET env var."""
    secret = os.environ.get("GATE_SECRET")
    if secret:
        raw = secret
    else:
        import platform
        raw = f"{platform.node()}-{os.getuid()}"
    return hashlib.sha256(raw.encode()).digest()


def _compute_hmac(marker: dict) -> str:
    """Compute HMAC-SHA256 for a marker dict (16 hex chars)."""
    key = _get_machine_key()
    signable = {k: v for k, v in marker.items() if k != "hmac"}
    payload = json.dumps(signable, sort_keys=True).encode()
    return _hmac.new(key, payload, hashlib.sha256).hexdigest()[:16]


def verify_marker(marker: dict) -> bool:
    """Verify a marker's HMAC signature. Returns True if valid."""
    stored = marker.get("hmac")
    if not stored:
        return False
    return _hmac.compare_digest(stored, _compute_hmac(marker))


def verify_marker_with_expiry(marker: dict) -> tuple[bool, str]:
    """Verify marker HMAC and TTL. Returns (valid, reason)."""
    # Check HMAC
    stored = marker.get("hmac")
    if not stored:
        return False, "missing hmac"
    if not _hmac.compare_digest(stored, _compute_hmac(marker)):
        return False, "hmac mismatch"
    # Check TTL
    expires_str = marker.get("expires_at")
    if expires_str:
        try:
            expires = datetime.fromisoformat(expires_str)
            if datetime.now(timezone.utc) > expires:
                return False, f"code expired at {expires_str}"
        except ValueError:
            return False, "invalid expires_at format"
    return True, "ok"


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
    slug = hashlib.sha256(project_dir.rstrip("/").encode()).hexdigest()[:16]
    marker_dir = gate_dir / slug
    marker_dir.mkdir(parents=True, exist_ok=True)

    marker_path = marker_dir / f"{phase}.json"
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    marker = {
        "phase": phase,
        "project_dir": project_dir,
        "code": code,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "expires_at": expires_at.isoformat(),
    }
    if meta:
        marker.update(meta)

    # HMAC signature (machine-bound, tamper-evident)
    marker["hmac"] = _compute_hmac(marker)
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
                  code: str | None = None, meta: dict | None = None) -> None:
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
        # Copy-friendly confirmation code
        print(f"\n📋 确认码（复制用）: {code}\n", file=sys.stderr)
    if meta:
        result["meta"] = meta

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
