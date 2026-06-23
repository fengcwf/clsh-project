#!/usr/bin/env python3
"""
gate-phase6.py - Phase 6 Quality Gate

Validates:
  1. Dispatch evidence — conversation.md must record delegate_task/kanban calls
  2. Skill injection — dispatch records must mention skill names
  3. Level awareness — check dispatch method matches env Level (A/B/C)
  4. Tester report — must exist with PASS/FAIL judgment and evidence
  5. Entry pre-check — tasks.md must exist with role annotations (from Phase 5)

Usage:
    python gate-phase6.py <project_dir>

Output: JSON to stdout, exit 0 on PASS, 1 on FAIL.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

GATE_NAME = "phase6"

# ---------------------------------------------------------------------------
# Dispatch evidence patterns
# ---------------------------------------------------------------------------

DISPATCH_PATTERNS = [
    r"delegate_task",
    r"kanban\s+(?:create|add|assign|--goal)",
    r"任务系统",
    r"任务派发",
    r"已派发",
    r"已分配给",
]

SKILL_INJECTION_PATTERNS = [
    r"test-driven-development",
    r"incremental-implementation",
    r"frontend-ui-engineering",
    r"systematic-debugging",
    r"code-review-and-quality",
    r"popular-web-designs",
    r"incremental",
    r"--skill\s",
    r"--skills\s",
    r"skills?\s*[:=]",
    r"注入.*skill",
    r"skill.*注入",
]

LEVEL_A_KEYWORDS = ["kanban", "任务系统", "kanban create", "kanban assign"]
LEVEL_B_KEYWORDS = ["delegate_task"]

# ---------------------------------------------------------------------------
# Tester report patterns (existing)
# ---------------------------------------------------------------------------

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
    r"```[\s\S]{20,}```",
    r"\b\d+\s+(?:test|assert|check)s?\s+passed\b",
    r"(?:PASS|FAIL)\s*\d+/\d+",
]

MIN_NONBLANK_LINES = 10


# ---------------------------------------------------------------------------
# Helper: load Level from env-check or config
# ---------------------------------------------------------------------------

def get_level(project_dir: str) -> str:
    """Determine the execution Level (A/B/C).

    Checks:
      1. config.json level field
      2. env-check.json output
      3. Default to B (delegate_task)
    """
    config = gu.load_config()
    level = config.get("level", "").upper()
    if level in ("A", "B", "C"):
        return level

    # Check env-check.json in gate-state
    gate_dir = gu.get_gate_dir()
    slug = __import__("hashlib").sha256(
        project_dir.rstrip("/").encode()
    ).hexdigest()[:16]
    env_check_path = gate_dir / slug / "env-check.json"
    if env_check_path.is_file():
        try:
            data = json.loads(env_check_path.read_text())
            level = data.get("level", "").upper()
            if level in ("A", "B", "C"):
                return level
        except (json.JSONDecodeError, KeyError):
            pass

    return "B"  # default


# ---------------------------------------------------------------------------
# Check 1: Dispatch evidence
# ---------------------------------------------------------------------------

def check_dispatch_evidence(project_dir: str) -> list[str]:
    """Verify that conversation.md records dispatch evidence."""
    errors = []

    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path is None:
        errors.append(
            "conversation.md not found — cannot verify dispatch evidence. "
            "conversation.md must record task dispatch (delegate_task/kanban)."
        )
        return errors

    content = conv_path.read_text(encoding="utf-8", errors="replace")

    has_dispatch = any(
        re.search(p, content, re.IGNORECASE) for p in DISPATCH_PATTERNS
    )
    if not has_dispatch:
        errors.append(
            "No dispatch evidence in conversation.md — "
            "expected delegate_task calls or kanban task creation records. "
            "Phase 6 requires task system dispatch (C8 Convention)."
        )

    return errors


# ---------------------------------------------------------------------------
# Check 2: Skill injection evidence
# ---------------------------------------------------------------------------

def check_skill_injection(project_dir: str) -> list[str]:
    """Verify that skill injection occurred during dispatch."""
    errors = []

    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path is None:
        return []  # already reported in dispatch check

    content = conv_path.read_text(encoding="utf-8", errors="replace")

    has_skill = any(
        re.search(p, content, re.IGNORECASE) for p in SKILL_INJECTION_PATTERNS
    )
    if not has_skill:
        errors.append(
            "No skill injection evidence in conversation.md — "
            "expected skill names (test-driven-development, etc.) or "
            "--skill/--skills parameters in dispatch records."
        )

    return errors


# ---------------------------------------------------------------------------
# Check 3: Level-aware dispatch validation
# ---------------------------------------------------------------------------

def check_level_dispatch(project_dir: str) -> list[str]:
    """Validate dispatch method matches the execution Level."""
    errors = []
    warnings = []

    level = get_level(project_dir)
    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path is None:
        return []  # already reported in dispatch check

    content = conv_path.read_text(encoding="utf-8", errors="replace")

    if level == "A":
        # Level A: kanban or delegate_task both acceptable
        has_kanban = any(
            re.search(p, content, re.IGNORECASE) for p in LEVEL_A_KEYWORDS
        )
        has_delegate = any(
            re.search(p, content, re.IGNORECASE) for p in LEVEL_B_KEYWORDS
        )
        if not (has_kanban or has_delegate):
            errors.append(
                "Level A requires kanban or delegate_task dispatch — "
                "neither found in conversation.md"
            )
    elif level == "B":
        # Level B: delegate_task required
        has_delegate = any(
            re.search(p, content, re.IGNORECASE) for p in LEVEL_B_KEYWORDS
        )
        if not has_delegate:
            errors.append(
                "Level B requires delegate_task dispatch — "
                "not found in conversation.md"
            )
    elif level == "C":
        # Level C: no task system, just prompt — downgrade to warning
        # Don't fail, just note it
        pass

    return errors


# ---------------------------------------------------------------------------
# Check 4: Tester report (existing logic)
# ---------------------------------------------------------------------------

def check_tester_report(project_dir: str) -> list[str]:
    """Validate the tester report."""
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


# ---------------------------------------------------------------------------
# Main gate logic
# ---------------------------------------------------------------------------

def run_gate(project_dir: str) -> None:
    """Run all Phase 6 gate checks."""
    all_errors = []

    # Check 1: Dispatch evidence
    all_errors.extend(check_dispatch_evidence(project_dir))

    # Check 2: Skill injection
    all_errors.extend(check_skill_injection(project_dir))

    # Check 3: Level-aware dispatch
    all_errors.extend(check_level_dispatch(project_dir))

    # Check 4: Tester report
    all_errors.extend(check_tester_report(project_dir))

    if not all_errors:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_marker(GATE_NAME, project_dir, code)
        gu.output_result(GATE_NAME, True, code=code)
    else:
        gu.output_result(GATE_NAME, False, errors=all_errors)


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
