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


def _get_slug(project_dir: str) -> str:
    """Compute SHA256 hash slug for a project directory (16 hex chars)."""
    return hashlib.sha256(project_dir.rstrip("/").encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# 2. Confirmation code generation (hash-based)
# ---------------------------------------------------------------------------

def generate_code(project_dir: str, phase: str, ttl_minutes: int = 30) -> str:
    """Generate an 8-char uppercase hex confirmation code (32-bit entropy).
    The code includes a TTL (time-to-live) recorded in the marker."""
    timestamp = str(int(time.time()))
    salt = secrets.token_hex(16)
    payload = f"{project_dir}{phase}{timestamp}{salt}"
    digest = hashlib.sha256(payload.encode()).hexdigest()
    return digest[:8].upper()


# ---------------------------------------------------------------------------
# 3. Marker file management
# ---------------------------------------------------------------------------

def _get_machine_key() -> bytes:
    """Derive a key for marker signing.

    Order of precedence:
      1. GATE_SECRET env var (for CI/testing)
      2. Persisted random key at <GATE_DIR>/.hmac_key
      3. Generate + persist a new random key (first run)

    The persisted key ensures HMAC is unpredictable even if hostname/uid
    are known, and survives across sessions.
    """
    secret = os.environ.get("GATE_SECRET")
    if secret:
        return hashlib.sha256(secret.encode()).digest()

    key_file = get_gate_dir() / ".hmac_key"
    if key_file.is_file():
        try:
            raw = key_file.read_text(encoding="utf-8").strip()
            if len(raw) >= 64:  # at least 32 bytes hex-encoded
                return bytes.fromhex(raw)
        except (ValueError, OSError):
            pass  # corrupt file, regenerate below

    # Generate random key and persist
    key_bytes = secrets.token_bytes(32)
    try:
        key_file.parent.mkdir(parents=True, exist_ok=True)
        key_file.write_text(key_bytes.hex() + "\n", encoding="utf-8")
        key_file.chmod(0o600)  # owner-only read/write
    except OSError:
        pass  # non-fatal: key still works for this session

    return key_bytes


def _get_legacy_key() -> bytes:
    """Get the legacy key (hostname+uid) for backward compatibility."""
    import platform
    raw = f"{platform.node()}-{os.getuid()}"
    return hashlib.sha256(raw.encode()).digest()


def _compute_hmac_with_key(marker: dict, key: bytes) -> str:
    """Compute HMAC-SHA256 for a marker dict with a specific key."""
    signable = {k: v for k, v in marker.items() if k != "hmac"}
    payload = json.dumps(signable, sort_keys=True).encode()
    return _hmac.new(key, payload, hashlib.sha256).hexdigest()[:16]


def _compute_hmac(marker: dict) -> str:
    """Compute HMAC-SHA256 for a marker dict (16 hex chars)."""
    key = _get_machine_key()
    return _compute_hmac_with_key(marker, key)


def verify_marker(marker: dict) -> bool:
    """Verify a marker's HMAC signature. Returns True if valid.

    Tries new key first, then legacy key for backward compatibility.
    """
    stored = marker.get("hmac")
    if not stored:
        return False
    # Try new key
    if _hmac.compare_digest(stored, _compute_hmac(marker)):
        return True
    # Try legacy key
    legacy = _compute_hmac_with_key(marker, _get_legacy_key())
    if _hmac.compare_digest(stored, legacy):
        return True
    return False


def verify_marker_with_expiry(marker: dict) -> tuple[bool, str]:
    """Verify marker HMAC and TTL. Returns (valid, reason).

    Tries new key first, then legacy key for backward compatibility.
    """
    # Check HMAC (try new key, then legacy)
    stored = marker.get("hmac")
    if not stored:
        return False, "missing hmac"

    new_hmac = _compute_hmac(marker)
    legacy_hmac = _compute_hmac_with_key(marker, _get_legacy_key())

    hmac_valid = (_hmac.compare_digest(stored, new_hmac) or
                  _hmac.compare_digest(stored, legacy_hmac))

    if not hmac_valid:
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


def write_pending(phase: str, project_dir: str, code: str,
                  meta: dict | None = None) -> Path:
    """Write a .pending file for two-step confirmation.

    The pending file records the code but NO HMAC — it is not a valid marker.
    The LLM must present the code to the user, then call verify_and_write_marker().
    """
    gate_dir = get_gate_dir()
    slug = _get_slug(project_dir)
    marker_dir = gate_dir / slug
    marker_dir.mkdir(parents=True, exist_ok=True)

    pending_path = marker_dir / f"{phase}.pending"
    pending = {
        "phase": phase,
        "project_dir": project_dir,
        "code": code,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if meta:
        pending["meta"] = meta
    pending_path.write_text(json.dumps(pending, indent=2) + "\n")
    return pending_path


def verify_and_write_marker(phase: str, project_dir: str,
                            user_code: str) -> tuple[bool, str, Path | None]:
    """Verify user-provided code against .pending file, then write marker.

    Returns (success, message, marker_path).
    On success: marker is written, .pending is deleted.
    On failure: no marker written, .pending preserved.
    """
    gate_dir = get_gate_dir()
    slug = hashlib.sha256(project_dir.rstrip("/").encode()).hexdigest()[:16]
    marker_dir = gate_dir / slug
    pending_path = marker_dir / f"{phase}.pending"

    if not pending_path.is_file():
        return False, f"No pending confirmation for {phase}. Run gate-phaseN.py first.", None

    try:
        pending = json.loads(pending_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return False, f"Corrupt pending file: {e}", None

    # Verify code matches
    if not _hmac.compare_digest(pending.get("code", ""), user_code.upper()):
        return False, "Confirmation code mismatch.", None

    # Code matches — write the real marker
    meta = pending.get("meta") or {}
    if not isinstance(meta, dict):
        meta = {}
    marker_path = write_marker(phase, project_dir, user_code, meta=meta)

    # Clean up .pending
    try:
        pending_path.unlink()
    except OSError:
        pass  # non-fatal

    return True, "Phase confirmed.", marker_path


def is_marker_valid(marker: dict) -> tuple[bool, str]:
    """Check if a marker has a valid HMAC, ignoring TTL expiry.

    Tries new key first, then legacy key for backward compatibility.

    Returns (valid, reason).
    - (True, "ok") — HMAC valid, not expired
    - (True, "expired but valid") — HMAC valid but TTL expired (phase was completed)
    - (False, ...) — HMAC invalid or missing
    """
    stored = marker.get("hmac")
    if not stored:
        return False, "missing hmac"

    # Try new key, then legacy
    new_hmac = _compute_hmac(marker)
    legacy_hmac = _compute_hmac_with_key(marker, _get_legacy_key())

    hmac_valid = (_hmac.compare_digest(stored, new_hmac) or
                  _hmac.compare_digest(stored, legacy_hmac))

    if not hmac_valid:
        return False, "hmac mismatch"

    # HMAC is valid — check TTL separately
    expires_str = marker.get("expires_at")
    if expires_str:
        try:
            expires = datetime.fromisoformat(expires_str)
            if datetime.now(timezone.utc) > expires:
                return True, "expired but valid"  # HMAC OK, just expired
        except ValueError:
            pass  # bad format, but HMAC is valid
    return True, "ok"


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
                  code: str | None = None, meta: dict | None = None,
                  pending: bool = False) -> None:
    """Print a structured JSON result to stdout.

    Always exits with the appropriate code:
        0 on PASS, 1 on FAIL

    When pending=True, the result signals that a confirmation code was
    generated but NO marker was written yet. The LLM must present the
    code to the user, then run: gate-phaseN.py <dir> --verify <code>
    """
    result = {
        "gate": gate_name,
        "passed": passed,
        "errors": errors or [],
    }
    if code:
        result["code"] = code
        # Copy-friendly confirmation code (stderr is user-visible)
        print(f"\n📋 确认码（复制用）: {code}\n", file=sys.stderr)
    if pending:
        result["pending"] = True
        result["instruction"] = (
            f"MANDATORY: Present the code to the user and wait for them to "
            f"confirm. Then run: gate-{gate_name}.py <project_dir> --verify <code>"
        )
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
