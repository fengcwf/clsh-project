#!/usr/bin/env python3
"""
gate-phase4.py - Phase 4 Quality Gate

Validates that core project documentation exists and contains meaningful
content (keywords, sufficient length). This gate runs after initial
document creation in Phase 4.

Required files (all must exist and pass content checks):
  - overview.md       : project overview document
  - conversation.md   : initial conversation / requirements discussion
  - proposal.md       : project proposal
  - constitution.md   : project constitution / guidelines
  - PRODUCT.md        : product requirements document
  - TECH.md           : technical design document

Checks performed:
  1. Each file must exist (in changes/*/ or project root)
  2. Each file must have >= 5 non-blank lines
  3. Each file must contain at least one relevant keyword

Usage:
    python gate-phase4.py <project_dir>

Output: JSON to stdout, exit 0 on PASS, 1 on FAIL.
"""

import re
import sys
from pathlib import Path

# Ensure scripts dir is on import path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

# Files to check and their required keyword patterns
REQUIRED_DOCS = {
    "overview.md":       [r"(?:goal|purpose|scope|background|目标|范围|背景|overview)"],
    "conversation.md":   [r"(?:requirement|user.story|need|question|需求|用户|场景|问题)"],
    "proposal.md":       [r"(?:approach|option|trade.?off|方案|选型|权衡|设计|决策)"],
    "constitution.md":   [r"(?:constraint|must.not|forbidden|验收|约束|禁止|标准)"],
    "PRODUCT.md":        [r"(?:goal|requirement|scope|objective|deliverable|用户故事|不变量)"],
    "TECH.md":           [r"(?:architecture|design|stack|component|implementation|架构|技术选型)"],
}

MIN_NONBLANK_LINES = 5
GATE_NAME = "phase4"


def check_document(project_dir: str, filename: str,
                   keywords: list[str]) -> list[str]:
    """Check a single document for existence and content quality.

    Returns a list of error strings (empty = pass).
    """
    errors = []
    filepath = gu.find_file_in_changes(project_dir, [filename])

    if filepath is None:
        errors.append(f"Missing file: {filename}")
        return errors

    content = filepath.read_text(encoding="utf-8", errors="replace")
    lines = [l for l in content.splitlines() if l.strip()]

    if len(lines) < MIN_NONBLANK_LINES:
        errors.append(
            f"{filename}: too short ({len(lines)} non-blank lines, "
            f"minimum {MIN_NONBLANK_LINES})"
        )

    if keywords:
        text_lower = content.lower()
        matched = any(re.search(kw, text_lower) for kw in keywords)
        if not matched:
            kw_display = " or ".join(keywords[:3])
            errors.append(
                f"{filename}: missing required content "
                f"(expected keywords like: {kw_display})"
            )

    return errors


def run_gate(project_dir: str) -> None:
    """Run the Phase 4 gate checks."""
    errors = []

    for filename, keywords in REQUIRED_DOCS.items():
        errors.extend(check_document(project_dir, filename, keywords))

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
                         errors=["Usage: gate-phase4.py <project_dir>"])

    project_dir = sys.argv[1]
    if not Path(project_dir).is_dir():
        gu.output_result(GATE_NAME, False,
                         errors=[f"Project directory not found: {project_dir}"])

    run_gate(project_dir)


if __name__ == "__main__":
    main()
