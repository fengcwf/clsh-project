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
  10. conversation.md must have >= 5 rounds of discussion
  11. Questions must cover >= 3 of 5 dimensions (功能/边界/异常/性能/安全)
  12. No fake confirmations (user must give substantive answers)
  13. (v2.1) User-initiated transition: >= 3 USER lines containing
      没有了/足够了/确认进入下一阶段 — mechanical proxy for the stop condition.
      Prevents the coordinator from requesting the confirmation code
      mid-clarification (IL-9 / IL-NEW-4; openwrt-agent Round 2/13 lesson).
  14. (v2.1) Round cap safety valve: rounds > 15 FAIL unless the project root
      contains .cp-human-intervention (with a written reason).

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
MIN_ROUNDS = 5
MAX_ROUNDS = 15  # v2.1 safety valve
MIN_DIMENSIONS = 3  # out of 5
MIN_SUBSTANTIVE_ANSWERS = 3  # user must give >= 3 real answers
MIN_TRANSITION_STATEMENTS = 3  # v2.1 user-initiated transition
HUMAN_INTERVENTION_MARKER = ".cp-human-intervention"  # v2.1 round-cap exemption

# v2.1: user lines that explicitly authorize moving to the next phase
USER_TRANSITION_PATTERN = r"(?:没有了|足够了|确认进入|进入下一阶段|可以进入|进入 Phase\s*[23]|开始下一阶段)"

# Question dimension patterns for Phase 1
QUESTION_DIMENSIONS = {
    "功能": [
        r"功能", r"用户故事", r"US-", r"feature", r"workflow",
        r"角色", r"操作", r"场景", r"需求",
    ],
    "边界/异常": [
        r"边界", r"异常", r"错误", r"失败", r"超时", r"回滚",
        r"edge.case", r"fallback", r"降级", r"重试", r"如何处理",
    ],
    "性能": [
        r"性能", r"并发", r"数据量", r"上限", r"响应时间",
        r"performance", r"延迟", r"吞吐", r"缓存",
    ],
    "安全/权限": [
        r"安全", r"权限", r"认证", r"授权", r"加密", r"security",
        r"permission", r"auth", r"敏感", r"脱敏",
    ],
    "兼容/集成": [
        r"兼容", r"接口", r"API", r"集成", r"integration",
        r"迁移", r"版本", r"依赖", r"第三方",
    ],
}

# Patterns that indicate exploration (not pure Q&A)
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

# Fake confirmation patterns (user saying "continue" without answering)
FAKE_CONFIRMATION_PATTERNS = [
    r"^\s*(继续|没问题|好的|OK|可以|行|嗯|对|ok|yes|是的)\s*$",
    r"^\s*(继续|没问题|好的)([。，,.]|\s*$)",
]

USER_LINE_PATTERN = re.compile(r"(用户|大佬|User|>)\s*[:：]")


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

def check_round_count(project_dir: str) -> list[str]:
    """Check that conversation.md has >= 5 rounds of discussion."""
    errors = []
    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path is None:
        return []

    content = conv_path.read_text(encoding="utf-8", errors="replace")
    # Count rounds: lines matching "## Round N" pattern
    round_count = len(re.findall(r"##\s+Round\s+\d+", content, re.IGNORECASE))
    if round_count < MIN_ROUNDS:
        errors.append(
            f"conversation.md has only {round_count} rounds (need >= {MIN_ROUNDS}). "
            "Phase 1 requires sufficient discussion rounds before proceeding. "
            "Continue asking questions from different angles."
        )

    return errors

def check_round_cap(project_dir: str) -> list[str]:
    """v2.1 safety valve: rounds > 15 require human intervention marker."""
    errors = []
    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path is None:
        return []

    content = conv_path.read_text(encoding="utf-8", errors="replace")
    round_count = len(re.findall(r"##\s+Round\s+\d+", content, re.IGNORECASE))

    if round_count > MAX_ROUNDS:
        marker = Path(project_dir) / HUMAN_INTERVENTION_MARKER
        if not marker.exists():
            errors.append(
                f"conversation.md has {round_count} rounds "
                f"(safety valve: > {MAX_ROUNDS}). "
                "Phase 1 硬上限已触发：必须暂停并请求人工介入。"
                f"若用户已知情并同意继续，在项目根创建 {HUMAN_INTERVENTION_MARKER} "
                "并写明原因后重跑 gate。"
            )

    return errors

def check_dimension_coverage(project_dir: str) -> list[str]:
    """Check that questions cover >= 3 of 5 dimensions."""
    errors = []
    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path is None:
        return []

    content = conv_path.read_text(encoding="utf-8", errors="replace")

    # Extract LLM questions (lines with "?" that look like questions)
    llm_lines = []
    in_llm = False
    for line in content.splitlines():
        # Track LLM vs user turns based on markers
        if re.match(r"##\s*Round", line):
            in_llm = True
        elif re.match(r"(用户|大佬|User|>)\s*[:：]", line):
            in_llm = False
        if in_llm and "?" in line:
            llm_lines.append(line)

    questions_text = "\n".join(llm_lines)

    # Check dimension coverage
    covered_dims = []
    uncovered_dims = []
    for dim_name, keywords in QUESTION_DIMENSIONS.items():
        found = False
        for kw in keywords:
            if re.search(kw, questions_text, re.IGNORECASE):
                found = True
                break
        if found:
            covered_dims.append(dim_name)
        else:
            uncovered_dims.append(dim_name)

    if len(covered_dims) < MIN_DIMENSIONS:
        errors.append(
            f"追问维度不足：只覆盖 {len(covered_dims)}/5 个维度 "
            f"(需要 >= {MIN_DIMENSIONS}). "
            f"已覆盖: {', '.join(covered_dims)}. "
            f"缺失: {', '.join(uncovered_dims)}. "
            f"请从缺失维度中追问更多问题。"
        )

    return errors

def check_confirmation_quality(project_dir: str) -> list[str]:
    """Check that user gave substantive answers, not just 'continue'."""
    errors = []
    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path is None:
        return []

    content = conv_path.read_text(encoding="utf-8", errors="replace")

    # Extract user responses (lines after user markers)
    user_lines = []
    for line in content.splitlines():
        # Match user response markers
        if USER_LINE_PATTERN.match(line):
            response = USER_LINE_PATTERN.sub("", line, count=1).strip()
            if response:
                user_lines.append(response)

    # Count substantive answers (not fake confirmations)
    substantive = 0
    fake_count = 0
    for resp in user_lines:
        is_fake = any(
            re.match(p, resp, re.IGNORECASE) for p in FAKE_CONFIRMATION_PATTERNS
        )
        if is_fake:
            fake_count += 1
        elif len(resp) > 5:  # at least 5 chars = substantive
            substantive += 1

    if substantive < MIN_SUBSTANTIVE_ANSWERS:
        errors.append(
            f"用户实质性回答不足：只有 {substantive} 个 "
            f"(需要 >= {MIN_SUBSTANTIVE_ANSWERS}). "
            f"检测到 {fake_count} 个假确认（'继续'/'没问题'等不算回答). "
            f"Phase 1 要求用户对具体问题给出实质性回答。"
        )

    return errors

def check_user_initiated_transition(project_dir: str) -> list[str]:
    """v2.1: stop condition must be user-initiated (mechanical proxy).

    IL-9 says the stop condition is controlled by the user, but nothing
    verified it — the coordinator could request the confirmation code after
    only a few rounds (observed in openwrt-agent: code requested at
    Round 2/13, 17 rounds total). This check requires >= 3 USER lines
    explicitly authorizing the transition before the gate emits a code.
    """
    errors = []
    conv_path = gu.find_file_in_changes(project_dir, ["conversation.md"])
    if conv_path is None:
        return []

    content = conv_path.read_text(encoding="utf-8", errors="replace")

    # Only count transition statements inside USER lines (not LLM prose)
    transition_count = 0
    for line in content.splitlines():
        if USER_LINE_PATTERN.match(line):
            response = USER_LINE_PATTERN.sub("", line, count=1).strip()
            if response and re.search(USER_TRANSITION_PATTERN, response):
                transition_count += 1

    if transition_count < MIN_TRANSITION_STATEMENTS:
        errors.append(
            f"用户过渡声明不足：只检测到 {transition_count} 次 "
            f"(需要 >= {MIN_TRANSITION_STATEMENTS}). "
            "停止条件由用户控制（IL-9）：必须有用户明确说"
            "'没有了'/'足够了'/'确认进入下一阶段'。"
            "继续从轮转表缺失维度追问，⛔ 不得请求确认码。"
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

    # Check round count (>= 5 rounds)
    errors.extend(check_round_count(project_dir))

    # v2.1: round cap safety valve (> 15 requires human intervention marker)
    errors.extend(check_round_cap(project_dir))

    # Check dimension coverage (>= 3/5)
    errors.extend(check_dimension_coverage(project_dir))

    # Check confirmation quality (no fake confirmations)
    errors.extend(check_confirmation_quality(project_dir))

    # v2.1: user-initiated transition (stop condition mechanical proxy)
    errors.extend(check_user_initiated_transition(project_dir))

    if not errors:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_pending(GATE_NAME, project_dir, code,
                         meta={"checked": list(REQUIRED_DOCS.keys())})
        gu.output_result(GATE_NAME, True, code=code, pending=True)
    else:
        gu.output_result(GATE_NAME, False, errors=errors)


def main():
    if len(sys.argv) < 2:
        gu.output_result(GATE_NAME, False,
                         errors=["Usage: gate-phase1.py <project_dir> [--verify CODE]"])

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
