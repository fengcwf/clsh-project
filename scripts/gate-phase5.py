#!/usr/bin/env python3
"""
gate-phase5.py - Phase 5 Quality Gate

Validates tasks.md for proper structure, skill annotations, acceptance
criteria, and INV-* coverage from PRODUCT.md. This gate runs after task
planning is complete.

Checks performed:
  1. tasks.md must exist
  2. Each task must have a skills field (or equivalent annotation)
  3. Each task must have role annotations
  4. Each task must have acceptance criteria
  5. No placeholder text (TODO, FIXME, TBD, <placeholder>, etc.)
  6. INV-* items from PRODUCT.md must be covered in tasks.md

Usage:
    python gate-phase5.py <project_dir>

Output: JSON to stdout, exit 0 on PASS, 1 on FAIL.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

GATE_NAME = "phase5"

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\bTBD\b",
    r"<placeholder>",
    r"<fill in>",
    r"<add here>",
    r"\.\.\.\s*$",
]

SKILL_ANNOTATION_PATTERNS = [
    r"(?:skill|skills|agent)\s*[:=]",
    r"(?:skill[s]?/|agent[s]?/)\S+",
]

ROLE_ANNOTATION_PATTERNS = [
    r"(?:role|assignee|owner|responsible)\s*[:=]",
    r"@[\w-]+",
    r"(?:AI|human|agent)\s+task",
]

ACCEPTANCE_CRITERIA_PATTERNS = [
    r"(?:acceptance|criteria|done|verif|pass\s*:=)",
    r"(?:AC|Given|When|Then)\b",
]


def extract_inv_refs(product_md: str) -> set[str]:
    """Extract all INV-* identifiers from PRODUCT.md content."""
    return set(re.findall(r"\bINV-\d+\b", product_md))


def extract_task_refs(tasks_md: str) -> set[str]:
    """Extract all INV-* references from tasks.md content."""
    return set(re.findall(r"\bINV-\d+\b", tasks_md))


def check_tasks_md(project_dir: str) -> list[str]:
    """Validate tasks.md structure and content.

    Returns a list of error strings (empty = pass).
    """
    errors = []

    # --- File existence ---
    tasks_path = gu.find_file_in_changes(project_dir, ["tasks.md"])
    if tasks_path is None:
        errors.append("Missing file: tasks.md")
        return errors

    content = tasks_path.read_text(encoding="utf-8", errors="replace")

    # Split into task blocks: look for lines starting with ## or ### as delimiters
    task_blocks = re.split(r"(?=^##?\s+)", content, flags=re.MULTILINE)

    # Filter out non-task blocks (preamble, etc.)
    task_blocks = [b for b in task_blocks if re.match(r"^##\s+", b, re.MULTILINE)]

    if not task_blocks:
        errors.append("No task sections found (expected ## headings)")
        return errors

    for i, block in enumerate(task_blocks, 1):
        block_lower = block.lower()
        heading = block.split("\n")[0].strip()

        # Skills check
        has_skill = any(re.search(p, block_lower) for p in SKILL_ANNOTATION_PATTERNS)
        if not has_skill:
            errors.append(f"Task {i} ({heading}): missing skill/agent annotation")

        # Role check
        has_role = any(re.search(p, block, re.IGNORECASE) for p in ROLE_ANNOTATION_PATTERNS)
        if not has_role:
            errors.append(f"Task {i} ({heading}): missing role/owner annotation")

        # Acceptance criteria check
        has_ac = any(re.search(p, block, re.IGNORECASE) for p in ACCEPTANCE_CRITERIA_PATTERNS)
        if not has_ac:
            errors.append(f"Task {i} ({heading}): missing acceptance criteria")

    # --- Placeholder check (full document) ---
    for pattern in PLACEHOLDER_PATTERNS:
        matches = re.findall(pattern, content, re.MULTILINE)
        if matches:
            errors.append(
                f"Placeholder found: '{matches[0]}' "
                f"({len(matches)} occurrence(s))"
            )

    # --- INV-* coverage ---
    product_path = gu.find_file_in_changes(project_dir, ["PRODUCT.md"])
    if product_path:
        product_content = product_path.read_text(encoding="utf-8", errors="replace")
        inv_refs = extract_inv_refs(product_content)
        if inv_refs:
            task_refs = extract_task_refs(content)
            missing = inv_refs - task_refs
            if missing:
                errors.append(
                    f"INV-* items not covered in tasks.md: "
                    f"{', '.join(sorted(missing))}"
                )

    return errors


def run_gate(project_dir: str) -> None:
    """Run the Phase 5 gate checks."""
    errors = check_tasks_md(project_dir)

    if not errors:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_marker(GATE_NAME, project_dir, code)
        gu.output_result(GATE_NAME, True, code=code)
    else:
        gu.output_result(GATE_NAME, False, errors=errors)


def main():
    if len(sys.argv) < 2:
        gu.output_result(GATE_NAME, False,
                         errors=["Usage: gate-phase5.py <project_dir>"])

    project_dir = sys.argv[1]
    if not Path(project_dir).is_dir():
        gu.output_result(GATE_NAME, False,
                         errors=[f"Project directory not found: {project_dir}"])

    run_gate(project_dir)


if __name__ == "__main__":
    main()
