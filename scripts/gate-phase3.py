#!/usr/bin/env python3
"""
gate-phase3.py - Phase 3 Quality Gate

Validates that proposal.md and constitution.md exist and contain
meaningful design content. This gate runs after Phase 3 (设计文档与自检).

Required files:
  - proposal.md     : design proposal (must contain design decisions, not implementation)
  - constitution.md : project constitution / constraints

Checks performed:
  1. Both files must exist (in changes/*/ or project root)
  2. proposal.md must have >= 10 non-blank lines
  3. constitution.md must have >= 5 non-blank lines
  4. proposal.md must contain design-decision keywords (not just implementation details)
  5. constitution.md must contain constraint/forbidden keywords

Usage:
    python gate-phase3.py <project_dir>

Output: JSON to stdout, exit 0 on PASS, 1 on FAIL.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

REQUIRED_DOCS = {
    "proposal.md": {
        "keywords": [
            r"(?:approach|option|trade.?off|方案|选型|权衡|设计|决策)",
            r"(?:constraint|scope|boundary|约束|范围|边界|不在范围)",
        ],
        "min_lines": 10,
    },
    "constitution.md": {
        "keywords": [
            r"(?:constraint|must.not|forbidden|验收|约束|禁止|标准|不变量)",
            r"(?:INV-|验收标准|acceptance)",
        ],
        "min_lines": 5,
    },
}

GATE_NAME = "phase3"


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
    """Run Phase 3 gate checks."""
    all_errors = []

    for filename, spec in REQUIRED_DOCS.items():
        all_errors.extend(check_document(
            project_dir, filename,
            spec["keywords"], spec["min_lines"]))

    if not all_errors:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_pending(GATE_NAME, project_dir, code)
        gu.output_result(GATE_NAME, True, code=code, pending=True)
    else:
        gu.output_result(GATE_NAME, False, errors=all_errors)


def main() -> None:
    if len(sys.argv) < 2:
        gu.output_result(GATE_NAME, False,
                         errors=["Usage: gate-phase3.py <project_dir> [--verify CODE]"])

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
