#!/usr/bin/env python3
"""
gate-phase0.py - Phase 0 Quality Gate

Validates that Phase 0 mechanical scan was completed.
Checks:
  1. phase0-data.json must exist
  2. phase0-data.json must have valid structure (project, obsidian, learnings)
  3. phase0-research.md must exist (LLM analysis output)
  4. phase0-research.md must have minimum content
  5. phase0-research.md must contain structured question list (>= 10 questions)
  6. Questions must cover multiple dimensions (功能/技术/业务/约束)

Usage:
    python gate-phase0.py <project_dir>

Output: JSON to stdout, exit 0 on PASS, 1 on FAIL.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

GATE_NAME = "phase0"
MIN_RESEARCH_LINES = 10
MIN_QUESTIONS = 10
MIN_DIMENSIONS = 3  # out of 4

# Question dimension patterns (at least 3 of 4 must be covered)
QUESTION_DIMENSIONS = {
    "功能/业务": [
        r"功能", r"业务", r"用户", r"场景", r"需求", r"feature",
        r"workflow", r"流程", r"角色", r"权限", r"操作",
    ],
    "技术/架构": [
        r"技术", r"架构", r"框架", r"数据库", r"API", r"接口",
        r"部署", r"性能", r"并发", r"缓存", r"存储",
    ],
    "边界/异常": [
        r"边界", r"异常", r"错误", r"失败", r"超时", r"回滚",
        r"edge.case", r"fallback", r"降级", r"重试",
    ],
    "约束/兼容": [
        r"约束", r"限制", r"兼容", r"迁移", r"依赖", r"版本",
        r"安全", r"合规", r"数据量", r"上限",
    ],
}


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


def check_question_list(project_dir: str) -> list[str]:
    """Check that phase0-research.md contains a structured question list."""
    errors = []

    research_path = gu.find_file_in_changes(project_dir, ["phase0-research.md"])
    if research_path is None:
        return []  # already reported in check_phase0_research

    content = research_path.read_text(encoding="utf-8", errors="replace")

    # Check for question list section header
    section_patterns = [
        r"##\s*(待确认|问题清单|信息缺口|Questions|待澄清)",
        r"###\s*(待确认|问题清单|信息缺口|Questions|待澄清)",
    ]
    has_section = any(
        re.search(p, content, re.IGNORECASE) for p in section_patterns
    )
    if not has_section:
        errors.append(
            "phase0-research.md missing question list section — "
            "must have '## 待确认问题' or '## 信息缺口' section with numbered questions"
        )

    # Count numbered questions (lines like "1. xxx?" or "- xxx?" or "* xxx?")
    question_patterns = [
        r"^\s*\d+\.\s*.+\?",  # "1. What is...?"
        r"^\s*[-*]\s*.+\?",   # "- What is...?"
    ]
    questions = []
    for line in content.splitlines():
        for pat in question_patterns:
            if re.match(pat, line.strip()):
                questions.append(line.strip())
                break

    if len(questions) < MIN_QUESTIONS:
        errors.append(
            f"phase0-research.md has only {len(questions)} questions "
            f"(need >= {MIN_QUESTIONS}). Add more questions covering "
            f"功能/技术/边界/约束 dimensions."
        )

    # Check question dimension coverage
    covered_dims = 0
    for dim_name, keywords in QUESTION_DIMENSIONS.items():
        for kw in keywords:
            if re.search(kw, "|".join(questions), re.IGNORECASE):
                covered_dims += 1
                break

    if covered_dims < MIN_DIMENSIONS:
        errors.append(
            f"Questions only cover {covered_dims}/{len(QUESTION_DIMENSIONS)} "
            f"dimensions (need >= {MIN_DIMENSIONS}). "
            f"Missing dimensions: {', '.join(d for d in QUESTION_DIMENSIONS if not any(re.search(kw, '|'.join(questions), re.IGNORECASE) for kw in QUESTION_DIMENSIONS[d]))}"
        )

    return errors


def run_gate(project_dir: str) -> None:
    """Run Phase 0 gate checks."""
    all_errors = []

    all_errors.extend(check_phase0_data(project_dir))
    all_errors.extend(check_phase0_research(project_dir))
    all_errors.extend(check_question_list(project_dir))

    if not all_errors:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_pending(GATE_NAME, project_dir, code)
        gu.output_result(GATE_NAME, True, code=code, pending=True)
    else:
        gu.output_result(GATE_NAME, False, errors=all_errors)


def main():
    if len(sys.argv) < 2:
        gu.output_result(GATE_NAME, False,
                         errors=["Usage: gate-phase0.py <project_dir> [--verify CODE]"])

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
