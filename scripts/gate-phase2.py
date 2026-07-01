#!/usr/bin/env python3
"""
gate-phase2.py - Phase 2 Quality Gate

Validates that TECH.md exists and contains meaningful technical design content.
This gate runs after Phase 2 (方案设计与技术验证).

Required files:
  - TECH.md : technical design document

Checks performed:
  1. TECH.md must exist (in changes/*/ or project root)
  2. TECH.md must have >= 10 non-blank lines
  3. TECH.md must contain architecture/design keywords
  4. TECH.md must contain at least 2 approach/option keywords (2-3 方案)

Usage:
    python gate-phase2.py <project_dir>

Output: JSON to stdout, exit 0 on PASS, 1 on FAIL.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

REQUIRED_DOCS = {
    "TECH.md": [
        r"(?:architecture|design|stack|component|implementation|架构|技术选型|方案)",
        r"(?:option|alternative|trade.?off|方案[ABCD]|备选|权衡|对比)",
    ],
}

MIN_NONBLANK_LINES = 10
GATE_NAME = "phase2"


def check_document(project_dir: str, filename: str,
                   keyword_patterns: list[str]) -> list[str]:
    """Check a single document. Returns list of error strings (empty = pass)."""
    errors = []
    fpath = gu.find_file_in_changes(project_dir, [filename])
    if fpath is None:
        errors.append(f"{filename}: NOT FOUND")
        return errors

    text = fpath.read_text(encoding="utf-8", errors="replace")
    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) < MIN_NONBLANK_LINES:
        errors.append(f"{filename}: only {len(lines)} non-blank lines "
                      f"(need >= {MIN_NONBLANK_LINES})")

    for pat in keyword_patterns:
        if not re.search(pat, text, re.IGNORECASE):
            errors.append(f"{filename}: missing keyword pattern {pat}")

    return errors


def run_gate(project_dir: str) -> None:
    """Run Phase 2 gate checks."""
    all_errors = []

    for filename, patterns in REQUIRED_DOCS.items():
        all_errors.extend(check_document(project_dir, filename, patterns))

    if not all_errors:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_pending(GATE_NAME, project_dir, code)
        gu.output_result(GATE_NAME, True, code=code, pending=True)
    else:
        gu.output_result(GATE_NAME, False, errors=all_errors)


def main() -> None:
    if len(sys.argv) < 2:
        gu.output_result(GATE_NAME, False,
                         errors=["Usage: gate-phase2.py <project_dir> [--verify CODE]"])

    project_dir = sys.argv[1]
    if not Path(project_dir).is_dir():
        gu.output_result(GATE_NAME, False,
                         errors=[f"Project directory not found: {project_dir}"])

    # --verify subcommand: confirm code and write marker
    if len(sys.argv) >= 4 and sys.argv[2] == "--verify":
        code = sys.argv[3]
        ok, msg, _ = gu.verify_and_write_marker(GATE_NAME, project_dir, code)
        gu.output_result(GATE_NAME, ok, errors=[msg] if not ok else None,
                         code=code if ok else None)
        return

    run_gate(project_dir)


if __name__ == "__main__":
    main()
