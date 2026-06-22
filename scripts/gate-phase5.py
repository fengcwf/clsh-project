#!/usr/bin/env python3
"""
gate-phase5.py - Phase 5 Quality Gate

Validates tasks.md for proper structure, skill annotations, acceptance
criteria, and coverage from PRODUCT.md (both INV-* and US-*). This gate
runs after task planning is complete.

Checks performed:
  1. tasks.md must exist
  2. Each task must have a skills field (or equivalent annotation)
  3. Each task must have role annotations
  4. Each task must have acceptance criteria
  5. No placeholder text (TODO, FIXME, TBD, <placeholder>, etc.)
  6. INV-* items from PRODUCT.md must be covered in tasks.md
  7. US-* items from PRODUCT.md must be covered:
     - P0 stories MUST appear in tasks.md (no exceptions)
     - P1/P2 stories must appear in tasks.md OR be explicitly excluded
       in TECH.md's "Out of Scope" section

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
    r"(?:skill|skills|agent|需要技能|技能)\s*[:=]",
    r"(?:skill[s]?/|agent[s]?/)\S+",
]

ROLE_ANNOTATION_PATTERNS = [
    r"(?:role|assignee|owner|responsible|角色).*?[:=]",
    r"@[\w-]+",
    r"(?:AI|human|agent)\s+task",
]

ACCEPTANCE_CRITERIA_PATTERNS = [
    r"(?:acceptance|criteria|done|verif|验收|pass\s*:=)",
    r"(?:AC|Given|When|Then)\b",
]


def extract_inv_refs(product_md: str) -> set[str]:
    """Extract all INV-* identifiers from PRODUCT.md content."""
    return set(re.findall(r"\bINV-\d+\b", product_md))


def extract_task_inv_refs(tasks_md: str) -> set[str]:
    """Extract all INV-* references from tasks.md content."""
    return set(re.findall(r"\bINV-\d+\b", tasks_md))


def extract_us_refs(product_md: str) -> set[str]:
    """Extract all US-* identifiers from PRODUCT.md content."""
    return set(re.findall(r"\bUS-\d+\b", product_md))


def extract_task_us_refs(tasks_md: str) -> set[str]:
    """Extract all US-* references from tasks.md content."""
    return set(re.findall(r"\bUS-\d+\b", tasks_md))


def extract_us_priorities(product_md: str) -> dict[str, str]:
    """Extract US-* identifiers with their priority levels from PRODUCT.md.

    Parses markdown table rows like:
        | US-1 | role | story | value | P0 |

    Returns dict mapping US-ID -> priority (e.g. {"US-1": "P0", "US-2": "P1"}).
    Falls back to empty priority if not parseable.
    """
    us_priority = {}
    # Match table rows with US-* in first column and P0/P1/P2 in last column
    pattern = r"\|\s*(US-\d+)\s*\|[^|]*\|[^|]*\|[^|]*\|\s*(P\d)\s*\|"
    for match in re.finditer(pattern, product_md):
        us_id = match.group(1)
        priority = match.group(2)
        us_priority[us_id] = priority

    # Fallback: if no table rows matched, just extract US-* without priority
    all_us = extract_us_refs(product_md)
    for us in all_us:
        if us not in us_priority:
            us_priority[us] = "P1"  # default to P1 if unparseable

    return us_priority


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
    # Support both ## and ### heading levels
    task_blocks = [b for b in task_blocks if re.match(r"^#{2,3}\s+", b, re.MULTILINE)]

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

    # --- Load PRODUCT.md for coverage checks ---
    product_path = gu.find_file_in_changes(project_dir, ["PRODUCT.md"])
    if not product_path:
        return errors

    product_content = product_path.read_text(encoding="utf-8", errors="replace")

    # --- INV-* coverage ---
    inv_refs = extract_inv_refs(product_content)
    if inv_refs:
        task_inv_refs = extract_task_inv_refs(content)
        missing_inv = inv_refs - task_inv_refs
        if missing_inv:
            errors.append(
                f"INV-* items not covered in tasks.md: "
                f"{', '.join(sorted(missing_inv))}"
            )

    # --- US-* coverage (with priority awareness) ---
    us_priorities = extract_us_priorities(product_content)
    if us_priorities:
        task_us_refs = extract_task_us_refs(content)

        # Load TECH.md for out-of-scope check (P1/P2 only)
        tech_path = gu.find_file_in_changes(project_dir, ["TECH.md"])
        tech_content = ""
        if tech_path:
            tech_content = tech_path.read_text(encoding="utf-8", errors="replace")
        tech_us_refs = set(re.findall(r"\bUS-\d+\b", tech_content))

        missing_p0 = []
        missing_other = []

        for us_id, priority in sorted(us_priorities.items()):
            if us_id in task_us_refs:
                continue  # covered in tasks.md

            if priority == "P0":
                # P0 MUST be in tasks.md — no exceptions
                missing_p0.append(us_id)
            else:
                # P1/P2 must be in tasks.md OR explicitly excluded in TECH.md
                if us_id not in tech_us_refs:
                    missing_other.append(us_id)

        if missing_p0:
            errors.append(
                f"P0 user stories MUST have tasks in tasks.md: "
                f"{', '.join(sorted(missing_p0))}"
            )

        if missing_other:
            errors.append(
                f"User stories not covered in tasks.md and not in TECH.md Out of Scope: "
                f"{', '.join(sorted(missing_other))} "
                f"(add tasks or explicitly exclude in TECH.md)"
            )

    return errors


def run_gate(project_dir: str) -> None:
    """Run the Phase 5 gate checks."""
    errors = check_tasks_md(project_dir)

    # Build coverage summary for output
    coverage = {}
    product_path = gu.find_file_in_changes(project_dir, ["PRODUCT.md"])
    if product_path:
        product_content = product_path.read_text(encoding="utf-8", errors="replace")
        all_us = extract_us_refs(product_content)
        task_path = gu.find_file_in_changes(project_dir, ["tasks.md"])
        if task_path:
            task_content = task_path.read_text(encoding="utf-8", errors="replace")
            covered = extract_task_us_refs(task_content)
            uncovered = sorted(all_us - covered)
            coverage = {
                "total_stories": len(all_us),
                "covered": len(all_us) - len(uncovered),
                "uncovered": uncovered,
            }

    if not errors:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_marker(GATE_NAME, project_dir, code)
        gu.output_result(GATE_NAME, True, code=code, meta={"coverage": coverage})
    else:
        gu.output_result(GATE_NAME, False, errors=errors, meta={"coverage": coverage})


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
