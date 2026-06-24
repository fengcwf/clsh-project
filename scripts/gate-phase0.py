#!/usr/bin/env python3
"""
gate-phase0.py - Phase 0 Quality Gate

Validates that Phase 0 mechanical scan was completed.
Checks:
  1. phase0-data.json must exist
  2. phase0-data.json must have valid structure (project, obsidian, learnings)
  3. phase0-research.md must exist (LLM analysis output)
  4. phase0-research.md must have minimum content

Usage:
    python gate-phase0.py <project_dir>

Output: JSON to stdout, exit 0 on PASS, 1 on FAIL.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

GATE_NAME = "phase0"
MIN_RESEARCH_LINES = 10


def check_phase0_data(project_dir: str) -> list[str]:
    """Check that phase0-data.json exists and has valid structure."""
    errors = []

    data_path = gu.find_file_in_changes(project_dir, ["phase0-data.json"])
    if data_path is None:
        errors.append("phase0-data.json NOT FOUND — run phase0-scan.py first")
        return errors

    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        errors.append(f"phase0-data.json parse error: {e}")
        return errors

    # Check required top-level keys
    required_keys = ["project", "obsidian", "learnings"]
    for key in required_keys:
        if key not in data:
            errors.append(f"phase0-data.json missing key: {key}")

    # Check project section
    proj = data.get("project", {})
    if not proj.get("project_dir"):
        errors.append("phase0-data.json: project.project_dir is empty")
    if not proj.get("languages") and not proj.get("tech_stack"):
        errors.append("phase0-data.json: no languages or tech_stack detected")

    return errors


def check_phase0_research(project_dir: str) -> list[str]:
    """Check that phase0-research.md exists and has content."""
    errors = []

    research_path = gu.find_file_in_changes(project_dir, ["phase0-research.md"])
    if research_path is None:
        errors.append(
            "phase0-research.md NOT FOUND — LLM must analyze phase0-data.json "
            "and write research summary before entering Phase 1"
        )
        return errors

    content = research_path.read_text(encoding="utf-8", errors="replace")
    lines = [l for l in content.splitlines() if l.strip()]

    if len(lines) < MIN_RESEARCH_LINES:
        errors.append(
            f"phase0-research.md too short ({len(lines)} lines, "
            f"minimum {MIN_RESEARCH_LINES})"
        )

    # Check for required sections
    content_lower = content.lower()
    required_sections = ["项目", "技术", "调研"]
    for section in required_sections:
        if section not in content_lower:
            errors.append(
                f"phase0-research.md missing section keyword: {section}"
            )

    return errors


def run_gate(project_dir: str) -> None:
    """Run Phase 0 gate checks."""
    all_errors = []

    all_errors.extend(check_phase0_data(project_dir))
    all_errors.extend(check_phase0_research(project_dir))

    if not all_errors:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_marker(GATE_NAME, project_dir, code)
        gu.output_result(GATE_NAME, True, code=code)
    else:
        gu.output_result(GATE_NAME, False, errors=all_errors)


def main():
    if len(sys.argv) < 2:
        gu.output_result(GATE_NAME, False,
                         errors=["Usage: gate-phase0.py <project_dir>"])

    project_dir = sys.argv[1]
    if not Path(project_dir).is_dir():
        gu.output_result(GATE_NAME, False,
                         errors=[f"Project directory not found: {project_dir}"])

    run_gate(project_dir)


if __name__ == "__main__":
    main()
