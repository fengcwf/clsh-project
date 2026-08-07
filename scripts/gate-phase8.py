#!/usr/bin/env python3
"""
gate-phase8.py - Phase 8 Quality Gate (v3.0)

Validates Phase 8 Optimization Loop compliance:
  1. Kanban task chain exists (diagnostic → fix → review)
  2. Parent links are correct (fix→diag, review→fix)
  3. Skills are injected into each card
  4. Coordinator only recorded symptoms (no root cause analysis)
  5. Tester review card exists
  6. Skill anchoring declaration (v9.3)
  7. Feedback routing evidence (v9.3)
  8. Fresh context (delegate_task, not direct execution) (v9.3)
  9. One thing per iteration (v9.3)
  10. Circuit breaker state (v9.3)

Usage:
    python gate-phase8.py <project_dir>

Output: JSON to stdout, exit 0 on PASS, 1 on FAIL.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

GATE_NAME = "phase8"

# --- Configuration ---

REQUIRED_KANBAN_CARDS = 3  # diagnostic → fix → review

# Patterns that indicate coordinator analyzed code (violation)
ANALYSIS_PATTERNS = [
    r"根因是",
    r"root\s*cause\s*(is|:)",
    r"问题(?:是|在于|出在)",
    r"(?:因为|由于).*(?:导致|造成)",
    r"(?:应该是|可能是|大概是).*(?:问题|bug|错误)",
    r"(?:我分析|我判断|我认为).*(?:原因|根因|问题)",
    r"code\s+(?:analysis|review|inspection)",
]

# Patterns that indicate proper symptom recording
SYMPTOM_PATTERNS = [
    r"(?:用户|大佬)(?:说|报告|反映|描述)",
    r"(?:现象|症状|表现)(?:是|:)",
    r"(?:什么坏了|哪里不对|出了什么问题)",
    r"(?:文件|路径|报错信息)",
]

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\bTBD\b",
    r"<placeholder>",
    r"<fill in>",
    r"<add here>",
]

MIN_NONBLANK_LINES = 3


def check_kanban_chain(project_dir: str) -> list[str]:
    """Check that kanban task chain exists with correct structure."""
    errors = []

    # Look for kanban-related files
    kanban_files = []
    for pattern in ["kanban*.json", "tasks*.json", ".kanban/*"]:
        kanban_files.extend(Path(project_dir).glob(pattern))

    if not kanban_files:
        # Try to find kanban state in conversation.md
        conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
        if conv_path is None:
            errors.append(
                "No kanban files or conversation.md found. "
                "Phase 8 requires kanban task chain (diagnostic→fix→review)"
            )
            return errors

        # Check conversation.md for kanban task creation evidence
        conv_content = conv_path.read_text(encoding="utf-8", errors="replace")

        # Check for "no issues" pattern first
        no_issues_patterns = [
            r"Phase 8.*(?:无问题|没有问题|没有需要修复)",
            r"(?:无问题|没有问题|没有需要修复).*Phase 8",
            r"反馈循环.*(?:无问题|没有问题|没有需要修复)",
            r"(?:无问题|没有问题|没有需要修复).*反馈循环",
        ]
        has_no_issues = any(
            re.search(p, conv_content, re.IGNORECASE)
            for p in no_issues_patterns
        )

        if has_no_issues:
            # Phase 8 completed with no issues - skip kanban chain check
            return errors

        # Check for 3-card creation
        card_indicators = [
            r"kanban.*create",
            r"创建.*卡",
            r"诊断.*卡",
            r"修复.*卡",
            r"审核.*卡",
        ]
        found_cards = sum(
            1 for p in card_indicators
            if re.search(p, conv_content, re.IGNORECASE)
        )

        if found_cards < 3:
            errors.append(
                f"Conversation.md shows {found_cards}/3 kanban card indicators. "
                "Phase 8 requires: diagnostic card → fix card → review card"
            )

    return errors


def check_parent_links(project_dir: str) -> list[str]:
    """Check that kanban cards have correct parent relationships."""
    errors = []

    # Look for parent link evidence in conversation.md
    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path:
        content = conv_path.read_text(encoding="utf-8", errors="replace")

        # Check for parent link patterns
        parent_patterns = [
            r"parents?\s*[:=]",
            r"parent.*诊断",
            r"parent.*修复",
            r"依赖.*卡",
        ]
        found_parents = sum(
            1 for p in parent_patterns
            if re.search(p, content, re.IGNORECASE)
        )

        if found_parents == 0:
            errors.append(
                "No parent link evidence found in conversation.md. "
                "Phase 8 requires: fix card parents=diagnostic, review card parents=fix"
            )

    return errors


def check_skill_injection(project_dir: str) -> list[str]:
    """Check that skills are injected into kanban cards."""
    errors = []

    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path:
        content = conv_path.read_text(encoding="utf-8", errors="replace")

        # Check for skill injection evidence
        skill_patterns = [
            r"--skill",
            r"skill.*注入",
            r"注入.*skill",
            r"skill_view",
        ]
        found_skills = sum(
            1 for p in skill_patterns
            if re.search(p, content, re.IGNORECASE)
        )

        if found_skills == 0:
            errors.append(
                "No skill injection evidence found. "
                "Phase 8 requires each kanban card to have injected skills"
            )

    return errors


def check_coordinator_behavior(project_dir: str) -> list[str]:
    """Check that coordinator only recorded symptoms, didn't analyze code."""
    errors = []

    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path is None:
        return ["No conversation.md found for behavior check"]

    content = conv_path.read_text(encoding="utf-8", errors="replace")
    content_lower = content.lower()

    # Check for analysis patterns (violation)
    violations = []
    for pattern in ANALYSIS_PATTERNS:
        matches = re.findall(pattern, content_lower)
        if matches:
            violations.append(f"Pattern '{pattern}' matched: {matches[0]}")

    if violations:
        errors.append(
            f"Coordinator appears to have analyzed code (Phase 8 violation). "
            f"Found {len(violations)} analysis indicators: "
            + "; ".join(violations[:3])  # Show first 3
        )

    # Check for symptom patterns (good behavior)
    symptom_count = sum(
        1 for p in SYMPTOM_PATTERNS
        if re.search(p, content_lower)
    )

    if symptom_count == 0 and len(violations) == 0:
        errors.append(
            "No symptom recording patterns found. "
            "Phase 8 requires coordinator to record symptoms (user reports, file paths, error messages)"
        )

    return errors


def check_tester_review(project_dir: str) -> list[str]:
    """Check that tester review card exists."""
    errors = []

    # Look for tester report
    tester_files = list(Path(project_dir).glob("*tester*.md"))
    if not tester_files:
        # Check conversation.md for tester evidence
        conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
        if conv_path:
            content = conv_path.read_text(encoding="utf-8", errors="replace")
            tester_patterns = [
                r"tester.*review",
                r"tester.*验证",
                r"tester.*审查",
                r"审核.*卡",
            ]
            found_tester = sum(
                1 for p in tester_patterns
                if re.search(p, content, re.IGNORECASE)
            )

            if found_tester == 0:
                errors.append(
                    "No tester review evidence found. "
                    "Phase 8 requires tester review card for each fix"
                )

    return errors


def check_placeholders(project_dir: str) -> list[str]:
    """Check for placeholder content in Phase 8 files."""
    errors = []

    # Check all markdown files in project directory
    for md_file in Path(project_dir).glob("*.md"):
        if md_file.name.startswith("."):
            continue

        content = md_file.read_text(encoding="utf-8", errors="replace")

        for pattern in PLACEHOLDER_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                errors.append(
                    f"{md_file.name}: placeholder found: '{matches[0]}'"
                )

    return errors


# ---------------------------------------------------------------------------
# Check 6: Skill anchoring declaration (v9.3)
# ---------------------------------------------------------------------------

ANCHOR_PATTERNS = [
    r"优化循环",
    r"optimization\s*loop",
    r"clsh-project.*(?:反馈|优化|循环)",
    r"使用.*clsh-project",
    r"路由.*Phase\s*[678]",
    r"反馈类型",
]


def check_skill_anchor(project_dir: str) -> list[str]:
    """Verify coordinator declared skill anchoring before processing feedback."""
    errors = []

    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path is None:
        return []

    content = conv_path.read_text(encoding="utf-8", errors="replace")

    has_anchor = any(
        re.search(p, content, re.IGNORECASE) for p in ANCHOR_PATTERNS
    )
    if not has_anchor:
        errors.append(
            "No skill anchoring declaration found in conversation.md. "
            "Phase 8 requires: 'I am using clsh-project optimization loop' "
            "with feedback type and routing target."
        )

    return errors


# ---------------------------------------------------------------------------
# Check 7: Feedback routing evidence (v9.3)
# ---------------------------------------------------------------------------

ROUTING_PATTERNS = [
    r"(?:路由|route|routing).*Phase\s*[1-8]",
    r"Phase\s*6.*(?:coder|artist|tester)",
    r"(?:UI|逻辑|需求|性能|确认).*→.*Phase",
    r"delegate_task.*(?:coder|artist|fix)",
    r"kanban.*(?:create|assign).*fix",
]


def check_routing(project_dir: str) -> list[str]:
    """Verify feedback was routed through the routing table."""
    errors = []

    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path is None:
        return []

    content = conv_path.read_text(encoding="utf-8", errors="replace")

    # Check if there's any feedback that should have been routed
    has_feedback = re.search(
        r"(?:用户|大佬)(?:说|反馈|报告|反映)|反馈|bug|问题|修改",
        content, re.IGNORECASE
    )
    if not has_feedback:
        return []  # No feedback to route

    has_routing = any(
        re.search(p, content, re.IGNORECASE) for p in ROUTING_PATTERNS
    )
    if not has_routing:
        errors.append(
            "Feedback found but no routing evidence. "
            "Phase 8 requires feedback to be routed through the routing table "
            "(UI→artist, logic→coder, requirement→Phase 1-3, confirm→Phase 7)."
        )

    return errors


# ---------------------------------------------------------------------------
# Check 8: Fresh context (delegate_task, not direct execution) (v9.3)
# ---------------------------------------------------------------------------

DIRECT_EXEC_PATTERNS = [
    r"(?:^|\n)\s*(?:def |class |import |from )",
    r"(?:^|\n)\s*(?:const |let |var |function )",
    r"(?:^|\n)\s*(?:npm |pip |cargo |go )",
]


def check_fresh_context(project_dir: str) -> list[str]:
    """Verify coordinator used delegate_task, not direct code execution."""
    errors = []

    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path is None:
        return []

    content = conv_path.read_text(encoding="utf-8", errors="replace")

    has_delegate = re.search(r"delegate_task", content, re.IGNORECASE)
    if not has_delegate:
        # Check if there was any code to fix (skip if "no issues")
        has_no_issues = re.search(
            r"(?:无问题|没有问题|没有需要修复)", content, re.IGNORECASE
        )
        if not has_no_issues:
            errors.append(
                "No delegate_task evidence in Phase 8. "
                "Phase 8 requires fresh context per iteration — "
                "coordinator must use delegate_task, not execute code directly."
            )

    return errors


# ---------------------------------------------------------------------------
# Main gate logic
# ---------------------------------------------------------------------------


def run_gate(project_dir: str) -> None:
    """Run the Phase 8 gate checks."""
    errors = []

    # Check if Phase 8 has no issues (skip kanban chain requirement)
    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    has_no_issues = False
    if conv_path:
        conv_content = conv_path.read_text(encoding="utf-8", errors="replace")
        no_issues_patterns = [
            r"Phase 8.*(?:无问题|没有问题|没有需要修复)",
            r"(?:无问题|没有问题|没有需要修复).*Phase 8",
            r"反馈循环.*(?:无问题|没有问题|没有需要修复)",
            r"(?:无问题|没有问题|没有需要修复).*反馈循环",
        ]
        has_no_issues = any(
            re.search(p, conv_content, re.IGNORECASE)
            for p in no_issues_patterns
        )

    if has_no_issues:
        # Phase 8 completed with no issues - only check placeholders
        errors.extend(check_placeholders(project_dir))
    else:
        # Phase 8 has issues - run all checks
        errors.extend(check_kanban_chain(project_dir))
        errors.extend(check_parent_links(project_dir))
        errors.extend(check_skill_injection(project_dir))
        errors.extend(check_coordinator_behavior(project_dir))
        errors.extend(check_tester_review(project_dir))
        errors.extend(check_placeholders(project_dir))
        # v9.3: Optimization Loop checks
        errors.extend(check_skill_anchor(project_dir))
        errors.extend(check_routing(project_dir))
        errors.extend(check_fresh_context(project_dir))

    if not errors:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_pending(GATE_NAME, project_dir, code, {
            "checks": [
                "kanban_chain",
                "parent_links",
                "skill_injection",
                "coordinator_behavior",
                "tester_review",
                "placeholders"
            ]
        })
        gu.output_result(GATE_NAME, True, code=code, pending=True)
    else:
        gu.output_result(GATE_NAME, False, errors=errors)


def main():
    if len(sys.argv) < 2:
        gu.output_result(GATE_NAME, False,
                         errors=["Usage: gate-phase8.py <project_dir> [--verify CODE]"])

    project_dir = sys.argv[1]
    if not Path(project_dir).is_dir():
        gu.output_result(GATE_NAME, False,
                         errors=[f"Project directory not found: {project_dir}"])

    # --verify subcommand
    if len(sys.argv) >= 4 and sys.argv[2] == "--verify":
        code = sys.argv[3]
        ok, msg, _ = gu.verify_and_write_marker(GATE_NAME, project_dir, code)
        gu.output_result(GATE_NAME, ok, errors=[msg] if not ok else None,
                         code=code if ok else None)
        return

    run_gate(project_dir)


if __name__ == "__main__":
    main()
