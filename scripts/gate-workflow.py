#!/usr/bin/env python3
"""
gate-workflow.py - Workflow Entry Gate (机械流程控制器)

这是 clsh-project 工作流的唯一入口。LLM 触发 clsh-project 后必须首先运行此脚本。
脚本扫描项目状态，决定当前 Phase，输出下一步操作指令。
LLM 只是脚本输出的执行器，不自行决定流程状态。

Usage:
    python gate-workflow.py <project_dir>

Output: JSON to stdout
    - status: "continue" | "complete" | "error"
    - current_phase: int (0-8)
    - action: 具体指令（LLM 必须执行）
    - gate_exit: 当前 Phase 完成后需要运行的 gate 脚本
    - blocked: 如果 LLM 试图跳到错误的 Phase，此字段说明原因

Exit codes:
    0: 正常，LLM 应按 action 执行
    1: 项目目录无效或不可达
"""

import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

# Phase 定义：每个 Phase 的入口 gate（检查前置条件）和出口 gate（生成确认码）
PHASES = {
    0: {
        "name": "内化历史教训 + 机械扫描",
        "entry_requires": None,  # Phase 0 无前置要求
        "exit_gate": "gate-phase0.py",
        "output_files": ["phase0-data.json", "phase0-research.md"],
    },
    1: {
        "name": "需求澄清",
        "entry_requires": 0,     # 需要 Phase 0 完成
        "exit_gate": "gate-phase1.py",
        "output_files": ["PRODUCT.md", "conversation.md"],
    },
    2: {
        "name": "方案设计",
        "entry_requires": 1,
        "exit_gate": "gate-phase2.py",
        "output_files": ["TECH.md"],
    },
    3: {
        "name": "设计文档",
        "entry_requires": 2,
        "exit_gate": "gate-phase3.py",
        "output_files": ["proposal.md", "constitution.md"],
    },
    4: {
        "name": "自检",
        "entry_requires": 3,
        "exit_gate": "gate-phase4.py",
        "output_files": [],
    },
    5: {
        "name": "实现计划",
        "entry_requires": 4,
        "exit_gate": "gate-phase5.py",
        "output_files": ["tasks.md"],
    },
    6: {
        "name": "分发执行",
        "entry_requires": 5,
        "exit_gate": "gate-phase6.py",
        "output_files": [],
    },
    7: {
        "name": "归档复盘",
        "entry_requires": 6,
        "exit_gate": "gate-phase7.py",
        "output_files": ["completion-summary.md", "retrospective.md", "handoff.md"],
    },
    8: {
        "name": "反馈循环",
        "entry_requires": 7,
        "exit_gate": "gate-phase8.py",
        "output_files": [],
    },
}


def find_project_dir(raw_path: str) -> Path | None:
    """Resolve project directory. Returns None if invalid."""
    p = Path(raw_path).expanduser().resolve()
    if p.is_dir():
        return p
    return None


def get_completed_phases(project_dir: str) -> dict[int, dict]:
    """Scan gate-state for completed phase markers. Returns {phase: marker}."""
    completed = {}
    gate_dir = gu.get_gate_dir()
    slug = hashlib.sha256(project_dir.rstrip("/").encode()).hexdigest()[:16]
    marker_dir = gate_dir / slug

    if not marker_dir.is_dir():
        return completed

    for marker_file in sorted(marker_dir.glob("*.json")):
        try:
            marker = json.loads(marker_file.read_text(encoding="utf-8"))
            phase_name = marker.get("phase", "")
            # phase names are like "phase1", "phase2", etc.
            if phase_name.startswith("phase"):
                phase_num = int(phase_name.replace("phase", ""))
                # Verify HMAC if present
                if "hmac" in marker:
                    valid, reason = gu.verify_marker_with_expiry(marker)
                    if valid:
                        completed[phase_num] = marker
                    # Note: expired codes still count as "completed" for workflow
                    # (the phase was done, just the code expired)
                    elif "expired" in reason:
                        completed[phase_num] = marker
                else:
                    completed[phase_num] = marker
        except (json.JSONDecodeError, ValueError):
            continue

    return completed


def determine_next_phase(completed: dict[int, dict]) -> int:
    """Determine the next phase to execute based on completed phases."""
    for phase_num in sorted(PHASES.keys()):
        if phase_num not in completed:
            return phase_num
    return -1  # All phases complete


def build_action(phase_num: int, project_dir: str) -> dict:
    """Build the action instruction for a given phase."""
    phase = PHASES[phase_num]

    actions = {
        0: {
            "step": "内化历史教训 + 机械扫描",
            "instructions": [
                "1. 运行机械扫描: python3 scripts/phase0-scan.py <项目目录>",
                "2. 读取 phase0-data.json（项目结构/技术栈/Obsidian 匹配/历史教训）",
                "3. 基于 JSON 数据写 phase0-research.md（信息缺口清单 + 追问建议）",
                f"4. 完成后运行: python3 {gu.get_gate_dir().parent}/skills/productivity/clsh-project/scripts/gate-phase0.py {project_dir}",
            ],
            "gate_exit": "gate-phase0.py",
        },
        1: {
            "step": "需求澄清（缺口驱动探索追问）",
            "instructions": [
                "1. 读取 phase0-research.md 中的信息缺口清单",
                "2. Round 1-3: 对缺口做探索调研（web_search/竞品/技术调研）→ 追问用户",
                "3. Round 4-6: 针对回答中的新缺口 → 定向探索 → 追问补充",
                "4. Round 7+: 纯追问澄清（不再探索）",
                "5. 用户确认材料足够后，生成 PRODUCT.md + conversation.md",
                f"6. 完成后运行: python3 {gu.get_gate_dir().parent}/skills/productivity/clsh-project/scripts/gate-phase1.py {project_dir}",
            ],
            "gate_exit": "gate-phase1.py",
        },
        2: {
            "step": "方案设计（2-3 方案对比）",
            "instructions": [
                "1. 基于 PRODUCT.md 设计 2-3 个技术方案",
                "2. 生成 TECH.md（架构决策 + 文件变更范围 + 实现注意事项）",
                "3. TECH.md 必须包含方案对比表格",
                f"4. 完成后运行: python3 {gu.get_gate_dir().parent}/skills/productivity/clsh-project/scripts/gate-phase2.py {project_dir}",
            ],
            "gate_exit": "gate-phase2.py",
        },
        3: {
            "step": "设计文档（proposal + constitution）",
            "instructions": [
                "1. 基于 TECH.md 生成 proposal.md（设计决策，不写实现细节）",
                "2. 生成 constitution.md（不可违反的约束）",
                f"3. 完成后运行: python3 {gu.get_gate_dir().parent}/skills/productivity/clsh-project/scripts/gate-phase3.py {project_dir}",
            ],
            "gate_exit": "gate-phase3.py",
        },
        4: {
            "step": "机械自检",
            "instructions": [
                "1. 运行 gate-phase4.py 检查所有前置文档",
                "2. 修复 gate 脚本报出的问题",
                f"3. 运行: python3 {gu.get_gate_dir().parent}/skills/productivity/clsh-project/scripts/gate-phase4.py {project_dir}",
            ],
            "gate_exit": "gate-phase4.py",
        },
        5: {
            "step": "实现计划（派 coder 写 tasks.md）",
            "instructions": [
                "1. 派 coder 任务写 tasks.md（body 含 proposal + constitution 路径）",
                "2. 协调者只 review 格式，不改内容",
                "3. tasks.md 中每个 Task 必须标注角色 (coder)/(tester)/(artist)",
                f"4. 完成后运行: python3 {gu.get_gate_dir().parent}/skills/productivity/clsh-project/scripts/gate-phase5.py {project_dir}",
            ],
            "gate_exit": "gate-phase5.py",
        },
        6: {
            "step": "分发执行",
            "instructions": [
                "1. 按 tasks.md 派发任务（必须用任务系统 + skill 注入）",
                "2. coder 执行 + tester 独立验证",
                "3. 确保每个 Task 有对应 tester 验证",
                f"4. 完成后运行: python3 {gu.get_gate_dir().parent}/skills/productivity/clsh-project/scripts/gate-phase6.py {project_dir}",
            ],
            "gate_exit": "gate-phase6.py",
        },
        7: {
            "step": "归档复盘",
            "instructions": [
                "1. 生成 completion-summary.md, retrospective.md, handoff.md",
                "2. 归档到 changes/archive/",
                f"3. 完成后运行: python3 {gu.get_gate_dir().parent}/skills/productivity/clsh-project/scripts/gate-phase7.py {project_dir}",
            ],
            "gate_exit": "gate-phase7.py",
        },
        8: {
            "step": "反馈循环",
            "instructions": [
                "1. 根据用户反馈修复问题",
                "2. 派 fix 卡 → tester 验证 → 人工确认",
                f"3. 完成后运行: python3 {gu.get_gate_dir().parent}/skills/productivity/clsh-project/scripts/gate-phase8.py {project_dir}",
            ],
            "gate_exit": "gate-phase8.py",
        },
    }

    action = actions.get(phase_num, {})
    action["phase"] = phase_num
    action["phase_name"] = PHASES[phase_num]["name"]
    return action


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "message": "Usage: python gate-workflow.py <project_dir>"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    raw_path = sys.argv[1]
    project_dir = find_project_dir(raw_path)

    if project_dir is None:
        # Project doesn't exist yet — this is a new project
        # Phase 0 can start immediately
        print(json.dumps({
            "status": "continue",
            "current_phase": 0,
            "project_dir": raw_path,
            "project_exists": False,
            "action": build_action(0, raw_path),
            "message": f"新项目: {raw_path}。从 Phase 0 开始。",
        }, ensure_ascii=False, indent=2))
        sys.exit(0)

    project_dir_str = str(project_dir)
    completed = get_completed_phases(project_dir_str)
    next_phase = determine_next_phase(completed)

    # Write workflow-initialized marker (gate-enforcer checks this)
    try:
        code = gu.generate_code(project_dir_str, "workflow-initialized")
        gu.write_marker("workflow-initialized", project_dir_str, code, {
            "next_phase": next_phase,
            "total_completed": len(completed),
        })
    except Exception:
        pass  # Non-fatal: marker is for gate-enforcer, not for flow control

    if next_phase == -1:
        # All phases complete
        print(json.dumps({
            "status": "complete",
            "project_dir": project_dir_str,
            "completed_phases": list(completed.keys()),
            "message": "所有 Phase 已完成。进入 Phase 8 反馈循环或结束项目。",
        }, ensure_ascii=False, indent=2))
        sys.exit(0)

    action = build_action(next_phase, project_dir_str)

    # Check if user requested a specific phase (optional 2nd arg)
    requested_phase = None
    if len(sys.argv) >= 3:
        try:
            requested_phase = int(sys.argv[2])
        except ValueError:
            pass

    if requested_phase is not None and requested_phase != next_phase:
        # User or LLM requested a different phase than what's next
        if requested_phase > next_phase:
            # Trying to skip ahead — BLOCKED
            missing = []
            for p in range(next_phase, requested_phase):
                if p not in completed:
                    missing.append(f"Phase {p} ({PHASES[p]['name']})")
            print(json.dumps({
                "status": "blocked",
                "requested_phase": requested_phase,
                "required_phase": next_phase,
                "missing_phases": missing,
                "message": f"⛔ 不能跳到 Phase {requested_phase}。缺少: {', '.join(missing)}",
                "action": build_action(next_phase, project_dir_str),
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
        elif requested_phase < next_phase:
            # Going back to a previous phase — allowed but noted
            print(json.dumps({
                "status": "continue",
                "current_phase": requested_phase,
                "project_dir": project_dir_str,
                "note": f"回退到 Phase {requested_phase}（已完成 {len(completed)} 个 Phase）",
                "action": build_action(requested_phase, project_dir_str),
            }, ensure_ascii=False, indent=2))
            sys.exit(0)

    # Normal flow: next phase
    completed_summary = {str(k): v.get("timestamp", "unknown") for k, v in completed.items()}
    print(json.dumps({
        "status": "continue",
        "current_phase": next_phase,
        "project_dir": project_dir_str,
        "completed_phases": completed_summary,
        "total_completed": len(completed),
        "action": action,
        "message": f"Phase {next_phase}: {PHASES[next_phase]['name']}。已完成 {len(completed)}/9 个 Phase。",
    }, ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
