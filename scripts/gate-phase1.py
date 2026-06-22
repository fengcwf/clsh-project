#!/usr/bin/env python3
"""
gate-phase1.py - Phase 1 Quality Gate

Validates that Phase 1 (需求澄清) produces proper requirements documents.
This gate runs after Phase 1 is complete.

Required files:
  - PRODUCT.md    : product requirements with US-* and INV-* tables
  - conversation.md : requirements clarification conversation log

Checks performed:
  1. Both files must exist (in changes/*/ or project root)
  2. PRODUCT.md must have >= 15 non-blank lines
  3. PRODUCT.md must contain US-* and INV-* identifiers
  4. PRODUCT.md must contain priority markers (P0/P1/P2)
  5. conversation.md must have >= 5 non-blank lines
  6. conversation.md must contain requirement/need keywords

Usage:
    python gate-phase1.py <project_dir>

Output: JSON to stdout, exit 0 on PASS, 1 on FAIL.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

REQUIRED_DOCS = {
    "PRODUCT.md": {
        "keywords": [
            r"(?:user.story|用户故事|US-\d+)",
            r"(?:INV-|不变量|invariant)",
            r"(?:P[012]|优先级|priority)",
        ],
        "min_lines": 15,
    },
    "conversation.md": {
        "keywords": [
            r"(?:requirement|need|question|需求|场景|问题|用户)",
        ],
        "min_lines": 5,
    },
}

GATE_NAME = "phase1"


def check_document(project_dir: str, filename: str,
                   keyword_patterns: list[str],
                   min_lines: int) -> list[str]:
    """Check a single document. Returns list of error strings (empty = pass)."""
    errors = []
    fpath = gu.find_file_in_changes(project_dir, [filename])
    if fpath is None:
        errors.append(f"{filename}: NOT FOUND")
        return errors

    text = fpath.read_text(encoding="utf-8", errors="replace")
    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) < min_lines:
        errors.append(f"{filename}: only {len(lines)} non-blank lines "
                      f"(need >= {min_lines})")

    for pat in keyword_patterns:
        if not re.search(pat, text, re.IGNORECASE):
            errors.append(f"{filename}: missing keyword pattern {pat}")

    return errors


def run_gate(project_dir: str) -> None:
    """Run the Phase 1 gate checks."""
    errors = []
    for filename, spec in REQUIRED_DOCS.items():
        errors.extend(check_document(
            project_dir, filename,
            spec["keywords"], spec["min_lines"]))

    if not errors:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_marker(GATE_NAME, project_dir, code,
                        {"checked": list(REQUIRED_DOCS.keys())})
        gu.output_result(GATE_NAME, True, code=code)
    else:
        gu.output_result(GATE_NAME, False, errors=errors)


def main():
    if len(sys.argv) < 2:
        gu.output_result(GATE_NAME, False,
                         errors=["Usage: gate-phase1.py <project_dir>"])

    project_dir = sys.argv[1]
    if not Path(project_dir).is_dir():
        gu.output_result(GATE_NAME, False,
                         errors=[f"Project directory not found: {project_dir}"])

    run_gate(project_dir)


if __name__ == "__main__":
    main()
