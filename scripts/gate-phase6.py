#!/usr/bin/env python3
"""
gate-phase6.py - Phase 6 Quality Gate

Validates that a tester report exists with a clear PASS/FAIL judgment
and supporting evidence. This gate runs after testing is complete.

Checks performed:
  1. Tester report file must exist (tester-report.md, test-report.md, or similar)
  2. Report must contain an explicit PASS or FAIL judgment
  3. Report must contain evidence (test results, logs, screenshots, etc.)
  4. Report must have minimum content (>= 10 non-blank lines)

Usage:
    python gate-phase6.py <project_dir>

Output: JSON to stdout, exit 0 on PASS, 1 on FAIL.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

GATE_NAME = "phase6"

REPORT_FILENAMES = [
    "tester-report.md",
    "test-report.md",
    "test-results.md",
    "testing-report.md",
    "report.md",
]

JUDGMENT_PATTERNS = [
    r"\b(?:TEST\s+)?(?:RESULT|VERDICT|JUDGMENT)\s*[:=]\s*\b(PASS|FAIL)\b",
    r"^\s*#\s*(?:Test\s+)?(?:Result|Verdict|Judgment)\s*[:=]?\s*(PASS|FAIL)",
    r"\b(?:overall|final)\s+(?:result|verdict|judgment)\s*[:=]?\s*(PASS|FAIL)",
    r"##\s+(?:Test\s+)?Result\s*\n.*?(PASS|FAIL)",
]

EVIDENCE_PATTERNS = [
    r"(?:evidence|proof|test\s*(?:result|output|log|case))",
    r"(?:screenshot|capture|traceback|stack\s*trace)",
    r"```[\s\S]{20,}```",         # code blocks with substantial content
    r"\b\d+\s+(?:test|assert|check)s?\s+passed\b",
    r"(?:PASS|FAIL)\s*\d+/\d+",
]

MIN_NONBLANK_LINES = 10


def check_tester_report(project_dir: str) -> list[str]:
    """Validate the tester report.

    Returns a list of error strings (empty = pass).
    """
    errors = []

    # --- File existence ---
    report_path = gu.find_file_in_changes(project_dir, REPORT_FILENAMES)
    if report_path is None:
        errors.append(
            f"Missing tester report. Looked for: {', '.join(REPORT_FILENAMES)}"
        )
        return errors

    content = report_path.read_text(encoding="utf-8", errors="replace")
    content_upper = content.upper()

    # --- Line count ---
    lines = [l for l in content.splitlines() if l.strip()]
    if len(lines) < MIN_NONBLANK_LINES:
        errors.append(
            f"{report_path.name}: too short ({len(lines)} non-blank lines, "
            f"minimum {MIN_NONBLANK_LINES})"
        )

    # --- Judgment check ---
    has_judgment = False
    for pattern in JUDGMENT_PATTERNS:
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
        if match:
            has_judgment = True
            verdict = match.group(1).upper()
            if verdict == "FAIL":
                errors.append(
                    f"Tester report contains FAIL judgment - "
                    f"review before proceeding"
                )
            break

    if not has_judgment:
        # Fallback: check for standalone PASS/FAIL keywords
        if re.search(r"\bPASS\b", content_upper):
            has_judgment = True
        elif re.search(r"\bFAIL\b", content_upper):
            has_judgment = True
            errors.append("Tester report contains FAIL judgment")
        else:
            errors.append(
                f"{report_path.name}: no PASS/FAIL judgment found"
            )

    # --- Evidence check ---
    has_evidence = False
    for pattern in EVIDENCE_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            has_evidence = True
            break

    if not has_evidence:
        errors.append(
            f"{report_path.name}: no test evidence found "
            f"(expected test results, logs, code blocks, or assertions)"
        )

    return errors


def run_gate(project_dir: str) -> None:
    """Run the Phase 6 gate checks."""
    errors = check_tester_report(project_dir)

    if not errors:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_marker(GATE_NAME, project_dir, code)
        gu.output_result(GATE_NAME, True, code=code)
    else:
        gu.output_result(GATE_NAME, False, errors=errors)


def main():
    if len(sys.argv) < 2:
        gu.output_result(GATE_NAME, False,
                         errors=["Usage: gate-phase6.py <project_dir>"])

    project_dir = sys.argv[1]
    if not Path(project_dir).is_dir():
        gu.output_result(GATE_NAME, False,
                         errors=[f"Project directory not found: {project_dir}"])

    run_gate(project_dir)


if __name__ == "__main__":
    main()
