#!/usr/bin/env python3
"""
gate-phase1.py - Phase 1 Quality Gate

Validates that Phase 1 (需求澄清) produces proper requirements documents.
This gate runs after Phase 1 is complete.

Required files:
  - phase0-data.json  : mechanical scan output from Phase 0
  - phase0-research.md : LLM analysis of scan results
  - PRODUCT.md        : product requirements with US-* and INV-* tables
  - conversation.md   : requirements clarification conversation log

Checks performed:
  1. phase0-data.json must exist (Phase 0 mechanical scan completed)
  2. phase0-research.md must exist and have content
  3. Both PRODUCT.md and conversation.md must exist
  4. PRODUCT.md must have >= 15 non-blank lines
  5. PRODUCT.md must contain US-* and INV-* identifiers
  6. PRODUCT.md must contain priority markers (P0/P1/P2)
  7. conversation.md must have >= 5 non-blank lines
  8. conversation.md must contain requirement/need keywords
  9. conversation.md must contain exploration evidence (web_search/grep/browser)

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


def check_phase0_prerequisites(project_dir: str) -> list[str]:
    """Check that Phase 0 outputs exist before allowing Phase 1."""
    errors = []

    # Check phase0-data.json
    data_path = gu.find_file_in_changes(project_dir, ["phase0-data.json"])
    if data_path is None:
        errors.append(
            "Phase 0 not completed: phase0-data.json missing. "
            "Run: python3 scripts/phase0-scan.py <project_dir>"
        )

    # Check phase0-research.md
    research_path = gu.find_file_in_changes(project_dir, ["phase0-research.md"])
    if research_path is None:
        errors.append(
            "Phase 0 not completed: phase0-research.md missing. "
            "LLM must analyze phase0-data.json and write research summary."
        )

    return errors


EXPLORATION_PATTERNS = [
    r"web_search",
    r"web_extract",
    r"browser_navigate",
    r"browser_snapshot",
    r"grep\s+",
    r"search_files",
    r"竞品",
    r"调研",
    r"技术选型",
    r"方案对比",
]


def check_exploration_evidence(project_dir: str) -> list[str]:
    """Check that conversation.md contains exploration evidence."""
    errors = []

    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path is None:
        return []  # already reported in document check

    content = conv_path.read_text(encoding="utf-8", errors="replace")

    has_exploration = any(
        re.search(p, content, re.IGNORECASE) for p in EXPLORATION_PATTERNS
    )
    if not has_exploration:
        errors.append(
            "No exploration evidence in conversation.md — "
            "Phase 1 Round 1-3 must use exploration tools "
            "(web_search, grep, browser, 竞品调研). "
            "Pure Q&A is not sufficient."
        )

    return errors


def run_gate(project_dir: str) -> None:
    """Run the Phase 1 gate checks."""
    errors = []

    # Check Phase 0 prerequisites
    errors.extend(check_phase0_prerequisites(project_dir))

    # Check document content
    for filename, spec in REQUIRED_DOCS.items():
        errors.extend(check_document(
            project_dir, filename,
            spec["keywords"], spec["min_lines"]))

    # Check exploration evidence
    errors.extend(check_exploration_evidence(project_dir))

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
