#!/usr/bin/env python3
"""
clsh-project 执行审计器
=======================
在 Phase 7 项目归档时运行。从最近的 session 日志中提取合规指标。

用法：python3 execution-audit.py <项目名>
输出：合规报告（stdout）+ pitfall 触发计数更新

依赖：hermes_tools（session_search, search_files, terminal）
"""

import sys
import json
import re
from datetime import datetime

try:
    from hermes_tools import session_search, search_files, terminal
except ImportError:
    print("ERROR: hermes_tools not available. Run inside Hermes execute_code.")
    sys.exit(1)


def search_project_sessions(project_name, limit=5):
    """搜索项目相关的最近 session"""
    result = session_search(query=project_name, limit=limit)
    if not result.get("success"):
        return []
    return result.get("results", [])


def check_role_separation(session_messages):
    """检查角色分离合规：灵犀是否直接写了代码"""
    violations = []
    for msg in session_messages:
        if msg.get("role") != "assistant":
            continue
        content = msg.get("content", "")
        tool_calls = msg.get("tool_calls", [])
        for tc in tool_calls:
            func = tc.get("function", {})
            name = func.get("name", "")
            if name in ("write_file", "patch"):
                # 灵犀直接写文件 = 潜在角色分离违规
                args = func.get("arguments", "")
                # 排除 wiki/docs 文件（灵犀可以写文档）
                if any(skip in args for skip in [
                    "wiki/", "/syntheses/", ".md", "SKILL.md",
                    "conversation.md", "proposal.md", "constitution.md",
                    "tasks.md", "retrospective.md", "overview.md"
                ]):
                    continue
                # 排除 project-wrap-up 相关
                if "learnings" in args or "wrap-up" in args:
                    continue
                violations.append({
                    "tool": name,
                    "args_preview": args[:100],
                    "message_id": msg.get("id")
                })
    return violations


def check_verification_execution(session_messages):
    """检查验证是否被执行：checkpoint 前是否有 terminal 调用"""
    skips = []
    for i, msg in enumerate(session_messages):
        content = msg.get("content", "")
        # 检测 checkpoint 声明
        if "CHECKPOINT" in content and "PASS" in content:
            # 向前看是否有 terminal 调用
            has_terminal = False
            for prev in session_messages[max(0, i-5):i]:
                for tc in prev.get("tool_calls", []):
                    if tc.get("function", {}).get("name") == "terminal":
                        has_terminal = True
                        break
            if not has_terminal:
                skips.append({
                    "type": "checkpoint_without_verification",
                    "message_id": msg.get("id"),
                    "preview": content[:80]
                })
    return skips


def check_tester_browser_verification(session_messages):
    """检查 tester 是否用了浏览器验证"""
    browser_calls = 0
    tester_reviews = 0
    for msg in session_messages:
        content = msg.get("content", "")
        tool_calls = msg.get("tool_calls", [])
        
        # 检测 tester review 活动
        if any(kw in content for kw in ["Review:", "review", "tester", "验证"]):
            if any(kw in content for kw in ["PASS", "FAIL", "approved"]):
                tester_reviews += 1
        
        # 检测浏览器调用
        for tc in tool_calls:
            func = tc.get("function", {})
            if "browse" in func.get("name", "").lower() or \
               "browser" in func.get("name", "").lower() or \
               "screenshot" in func.get("name", "").lower():
                browser_calls += 1
    
    return {
        "tester_reviews": tester_reviews,
        "browser_calls": browser_calls,
        "browser_rate": browser_calls / max(tester_reviews, 1)
    }


def check_fix_rounds(session_messages):
    """统计 Phase 8 修复轮次"""
    fix_indicators = 0
    for msg in session_messages:
        content = msg.get("content", "")
        # 检测 fix 相关信号
        if re.search(r'Round\s*\d+|fix\s+agent|修复.*轮|Auto-Fix', content, re.IGNORECASE):
            fix_indicators += 1
    return fix_indicators


def check_pitfall_triggers(session_messages, pitfalls):
    """检查已知 pitfall 是否被触发"""
    triggers = {}
    for pitfall in pitfalls:
        keywords = pitfall.get("keywords", [])
        count = 0
        for msg in session_messages:
            content = msg.get("content", "")
            for kw in keywords:
                if kw in content:
                    count += 1
                    break
        if count > 0:
            triggers[pitfall["id"]] = {
                "title": pitfall["title"],
                "count": count,
                "confidence": pitfall.get("confidence", 0.5)
            }
    return triggers


def generate_report(project_name, violations, verification_skips, 
                    tester_data, fix_rounds, pitfall_triggers):
    """生成合规报告"""
    report = []
    report.append(f"# 执行审计报告: {project_name}")
    report.append(f"**审计时间:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    
    # 总分计算
    total_checks = 4
    passed_checks = 0
    
    # 1. 角色分离
    report.append("## 1. 角色分离合规")
    if not violations:
        report.append("✅ **PASS** — 未检测到灵犀直接写代码")
        passed_checks += 1
    else:
        report.append(f"❌ **FAIL** — 检测到 {len(violations)} 次潜在违规：")
        for v in violations[:3]:
            report.append(f"  - `{v['tool']}` → `{v['args_preview']}`")
    report.append("")
    
    # 2. 验证执行
    report.append("## 2. 验证执行合规")
    if not verification_skips:
        report.append("✅ **PASS** — 所有 checkpoint 前有验证命令")
        passed_checks += 1
    else:
        report.append(f"❌ **FAIL** — {len(verification_skips)} 个 checkpoint 缺少验证：")
        for s in verification_skips[:3]:
            report.append(f"  - message #{s['message_id']}: {s['preview']}")
    report.append("")
    
    # 3. Tester 浏览器验证
    report.append("## 3. Tester 浏览器验证")
    if tester_data["browser_rate"] >= 0.5 or tester_data["tester_reviews"] == 0:
        report.append(f"✅ **PASS** — 浏览器调用率 {tester_data['browser_rate']:.0%}")
        if tester_data["tester_reviews"] == 0:
            report.append("  (未检测到 tester review 活动)")
        passed_checks += 1
    else:
        report.append(f"❌ **FAIL** — 浏览器调用率 {tester_data['browser_rate']:.0%} (review {tester_data['tester_reviews']} 次, browser {tester_data['browser_calls']} 次)")
    report.append("")
    
    # 4. 修复轮次
    report.append("## 4. 修复轮次")
    if fix_rounds <= 4:
        report.append(f"✅ **PASS** — 修复轮次 {fix_rounds} (阈值 ≤4)")
        passed_checks += 1
    else:
        report.append(f"⚠️ **WARN** — 修复轮次 {fix_rounds} 偏高 (阈值 ≤4)")
    report.append("")
    
    # 5. Pitfall 触发
    report.append("## 5. Pitfall 触发统计")
    if pitfall_triggers:
        report.append(f"⚠️ 检测到 {len(pitfall_triggers)} 个 pitfall 触发：")
        for pid, info in pitfall_triggers.items():
            report.append(f"  - #{pid} [{info['confidence']}] {info['title'][:50]} — 触发 {info['count']} 次")
    else:
        report.append("✅ 未检测到已知 pitfall 触发")
    report.append("")
    
    # 总分
    score = passed_checks / total_checks * 100
    report.append(f"## 总分: {passed_checks}/{total_checks} ({score:.0f}%)")
    
    if score >= 75:
        report.append("**结论: ✅ 流程合规**")
    elif score >= 50:
        report.append("**结论: ⚠️ 部分合规，需关注**")
    else:
        report.append("**结论: ❌ 合规率低，需改进**")
    
    return "\n".join(report)


# Pitfall 关键词映射（用于自动检测触发）
PITFALL_KEYWORDS = [
    {"id": "1", "title": "灵犀直接写代码", "keywords": ["灵犀直接", "write_file", "自己写"], "confidence": 0.9},
    {"id": "2", "title": "顺手修了", "keywords": ["顺手修", "直接修了", "quick fix"], "confidence": 0.9},
    {"id": "39", "title": "灵犀做代码推理", "keywords": ["后端期望", "改成什么", "具体代码"], "confidence": 0.9},
    {"id": "40", "title": "跳过tester验证", "keywords": ["代码看起来对", "应该可以了", "已修复"], "confidence": 0.9},
    {"id": "49", "title": "告诉CodeWhale怎么改", "keywords": ["删.*处", "改成.*代码", "照这个改", "用.*提升"], "confidence": 0.9},
]


def main():
    project_name = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    
    print(f"🔍 审计项目: {project_name}")
    print(f"搜索最近 session...")
    
    sessions = search_project_sessions(project_name, limit=3)
    if not sessions:
        print("未找到相关 session，跳过审计。")
        return
    
    print(f"找到 {len(sessions)} 个相关 session")
    
    # 收集所有消息
    all_messages = []
    for s in sessions:
        msgs = s.get("messages", [])
        all_messages.extend(msgs)
    
    # 运行各项检查
    violations = check_role_separation(all_messages)
    skips = check_verification_execution(all_messages)
    tester_data = check_tester_browser_verification(all_messages)
    fix_rounds = check_fix_rounds(all_messages)
    triggers = check_pitfall_triggers(all_messages, PITFALL_KEYWORDS)
    
    # 生成报告
    report = generate_report(
        project_name, violations, skips, 
        tester_data, fix_rounds, triggers
    )
    
    print("\n" + report)


if __name__ == "__main__":
    main()
