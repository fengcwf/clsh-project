#!/usr/bin/env python3
"""
gate-phase7.py - Phase 7 Quality Gate (C7 Fresh-Context Review)

Validates that a fresh-context reviewer report exists with coverage
across defined review dimensions. This gate runs after the C7
fresh-context review phase.

Checks performed:
  1. Reviewer report must exist (review-report.md or similar)
  2. Report must contain multiple review dimensions/sections
  3. Each dimension must have substantive content (not just a heading)
  4. Report must contain an overall assessment
  5. Report must have minimum content length

Usage:
    python gate-phase7.py <project_dir>

Output: JSON to stdout, exit 0 on PASS, 1 on FAIL.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

GATE_NAME = "phase7"

REVIEW_FILENAMES = [
    "review-report.md",
    "c7-review.md",
    "fresh-context-review.md",
    "review.md",
    "reviewer-report.md",
]

# Review dimensions expected in a C7 fresh-context review
EXPECTED_DIMENSIONS = [
    r"completeness",
    r"correctness",
    r"consistency",
    r"clarity",
    r"feasibility",
    r"risks?",
    r"security",
    r"performance",
    r"maintainab",
    r"testab",
    r"coverage",
]

MIN_DIMENSIONS = 5
MIN_NONBLANK_LINES = 15


def check_review_report(project_dir: str) -> list[str]:
    """Validate the C7 fresh-context review report.

    Returns a list of error strings (empty = pass).
    """
    errors = []

    # --- File existence ---
    report_path = gu.find_file_in_changes(project_dir, REVIEW_FILENAMES)
    if report_path is None:
        errors.append(
            f"Missing review report. Looked for: {', '.join(REVIEW_FILENAMES)}"
        )
        return errors

    content = report_path.read_text(encoding="utf-8", errors="replace")

    # --- Line count ---
    lines = [l for l in content.splitlines() if l.strip()]
    if len(lines) < MIN_NONBLANK_LINES:
        errors.append(
            f"{report_path.name}: too short ({len(lines)} non-blank lines, "
            f"minimum {MIN_NONBLANK_LINES})"
        )

    # --- Dimension coverage ---
    content_lower = content.lower()
    found_dimensions = []
    for dim_pattern in EXPECTED_DIMENSIONS:
        if re.search(dim_pattern, content_lower):
            found_dimensions.append(dim_pattern)

    if len(found_dimensions) < MIN_DIMENSIONS:
        errors.append(
            f"{report_path.name}: insufficient dimension coverage "
            f"({len(found_dimensions)}/{MIN_DIMENSIONS} required dimensions found). "
            f"Expected dimensions like: completeness, correctness, consistency, "
            f"clarity, feasibility, risks, security, performance"
        )

    # --- Section/subsection check ---
    # Ensure dimensions are structured (not just mentioned in passing)
    sections = re.findall(r"^##\s+.+", content, re.MULTILINE)
    if len(sections) < 2:
        # Fallback: check for ### headings or numbered items
        subsections = re.findall(r"^#{2,3}\s+.+|^\d+\.\s+.+", content, re.MULTILINE)
        if len(subsections) < MIN_DIMENSIONS:
            errors.append(
                f"{report_path.name}: lacks structured review sections "
                f"(found {len(subsections)} section headings, "
                f"expected at least {MIN_DIMENSIONS})"
            )

    # --- Overall assessment check ---
    assessment_patterns = [
        r"(?:overall|final|summary)\s+(?:assessment|verdict|conclusion|recommendation)",
        r"(?:approved|rejected|conditional|needs?\s+(?:revision|work))",
        r"(?:GO|NO\s*GO|CONDITIONAL\s+GO)",
    ]
    has_assessment = any(
        re.search(p, content_lower) for p in assessment_patterns
    )
    if not has_assessment:
        errors.append(
            f"{report_path.name}: no overall assessment/conclusion found"
        )

    # --- Severity classification (FAIL if missing) ---
    SEVERITY_PATTERN = re.compile(
        r'\b(Critical|Major|Minor|Suggestion)\b', re.IGNORECASE
    )
    severities = SEVERITY_PATTERN.findall(content)
    if not severities:
        errors.append(
            f"{report_path.name}: no severity classification found. "
            f"Each finding must be tagged Critical/Major/Minor/Suggestion"
        )

    # --- Evidence references (FAIL if < 3) ---
    EVIDENCE_PATTERN = re.compile(r'\[[\w\-./]+:\d+(?:-\d+)?\]')
    evidence_refs = EVIDENCE_PATTERN.findall(content)
    if len(evidence_refs) < 3:
        errors.append(
            f"{report_path.name}: insufficient evidence references "
            f"({len(evidence_refs)} found, need >=3). "
            f"Format: [filename:line_number]"
        )

    return errors


def run_gate(project_dir: str) -> None:
    """Run the Phase 7 gate checks."""
    errors = check_review_report(project_dir)

    if not errors:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_marker(GATE_NAME, project_dir, code)
        gu.output_result(GATE_NAME, True, code=code)
    else:
        gu.output_result(GATE_NAME, False, errors=errors)


def main():
    if len(sys.argv) < 2:
        gu.output_result(GATE_NAME, False,
                         errors=["Usage: gate-phase7.py <project_dir>"])

    project_dir = sys.argv[1]
    if not Path(project_dir).is_dir():
        gu.output_result(GATE_NAME, False,
                         errors=[f"Project directory not found: {project_dir}"])

    run_gate(project_dir)


if __name__ == "__main__":
    main()
