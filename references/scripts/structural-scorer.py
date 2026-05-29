#!/usr/bin/env python3
"""clsh-project 结构评分器 — 棘轮机制的核心组件

用法：python3 structural-scorer.py [--baseline N]
输出：各维度得分 + 总分 + 与基线对比

评分维度（满分 60）：
  流程完整性 (15) | 引用完整性 (10) | Pitfall 质量 (10)
  铁律一致性 (10) | Checklist 覆盖 (5) | 模板覆盖 (10)
"""

import re
import os
import sys
import json
from pathlib import Path
from collections import Counter

SKILL_DIR = Path(os.path.expanduser("~/.hermes/skills/productivity/clsh-project"))
SKILL_MD = SKILL_DIR / "SKILL.md"
WORKFLOW_DIR = SKILL_DIR / "references" / "workflow"
TEMPLATES_DIR = SKILL_DIR / "references" / "templates"

# --- 评分函数 ---

def score_flow_completeness():
    """流程完整性 (15分) — Phase 1-8 workflow 文件是否齐全"""
    score = 0
    checks = {
        "Phase 0+1": "phase0-1-requirements.md",
        "Phase 2": "phase2-design.md",
        "Phase 3": "phase3-spec.md",
        "Phase 5": "phase5-tasks.md",
        "Phase 6": "phase6-execution.md",
        "Phase 7": "phase7-archive.md",
        "Phase 8": "phase8-feedback.md",
    }
    for phase, filename in checks.items():
        filepath = WORKFLOW_DIR / filename
        if filepath.exists() and filepath.stat().st_size > 500:
            score += 2
        else:
            score -= 1
            print(f"  ⚠️  缺失或过小: {phase} ({filename})")
    # SKILL.md 中有流程总览
    content = SKILL_MD.read_text(errors="replace")
    if "Phase 1:" in content and "Phase 8:" in content:
        score += 1
    return max(0, min(15, score))

def score_reference_integrity():
    """引用完整性 (10分) — SKILL.md 中的引用是否断链"""
    content = SKILL_MD.read_text(errors="replace")
    refs = re.findall(r'references/[^\s\)`]+\.md', content)
    if not refs:
        return 10  # 没有引用 = 不扣分
    score = 10
    seen = set()
    for ref in refs:
        if ref in seen:
            continue
        seen.add(ref)
        filepath = SKILL_DIR / ref
        if not filepath.exists():
            score -= 1
            print(f"  ⚠️  断链: {ref}")
    return max(0, score)

def score_pitfall_quality():
    """Pitfall 质量 (10分) — 有反例/正例？有验证方法？有置信度？"""
    content = SKILL_MD.read_text(errors="replace")
    # 提取 Common Pitfalls 区域
    pitfall_section = re.search(
        r'## Common Pitfalls.*?(?=## Verification|\Z)', content, re.DOTALL
    )
    if not pitfall_section:
        return 0

    text = pitfall_section.group(0)
    # 匹配所有 pitfall 条目（编号. **标题** — 内容）
    pitfalls = re.findall(
        r'^\d+\.\s+\*\*.*?\*\*\s+—\s+(.+)$', text, re.MULTILINE
    )
    if not pitfalls:
        return 0

    score = 0
    for p in pitfalls:
        has_example = any(kw in p for kw in ["反例", "正例", "案例"])
        has_rule = any(kw in p for kw in ["**规则", "**修复", "**正确做法"])
        has_confidence = "置信度" in p
        has_verify = "验证：" in p
        if has_example:
            score += 0.08
        if has_rule:
            score += 0.08
        if has_confidence:
            score += 0.04
        if has_verify:
            score += 0.05

    # 归一化到 0-10
    max_possible = len(pitfalls) * 0.25
    normalized = (score / max_possible * 10) if max_possible > 0 else 0
    return min(10, round(normalized, 1))

def score_ironclad_consistency():
    """铁律一致性 (10分) — 编号连续、无重复、格式一致"""
    content = SKILL_MD.read_text(errors="replace")
    # 提取流程铁律区域
    ironclad_section = re.search(
        r'## ⛔ 流程铁律.*?(?=## |\Z)', content, re.DOTALL
    )
    if not ironclad_section:
        return 0

    text = ironclad_section.group(0)
    nums = [int(m) for m in re.findall(r'^(\d+)\.\s+\*\*', text, re.MULTILINE)]

    score = 10
    # 检查编号连续性
    for i in range(len(nums) - 1):
        gap = nums[i + 1] - nums[i]
        if gap > 2:
            score -= 1
            print(f"  ⚠️  铁律编号跳跃: {nums[i]} → {nums[i+1]}")

    # 检查重复编号
    dupes = {k: v for k, v in Counter(nums).items() if v > 1}
    for num, count in dupes.items():
        score -= 2
        print(f"  ⚠️  铁律编号重复: #{num} 出现 {count} 次")

    return max(0, score)

def score_checklist_coverage():
    """Checklist 覆盖 (5分) — 检查项数量"""
    content = SKILL_MD.read_text(errors="replace")
    items = re.findall(r'- \[.\]', content)
    count = len(items)
    # 每项 0.25 分，20 项 = 5 分
    return min(5, round(count * 0.25, 1))

def score_template_coverage():
    """模板覆盖 (10分) — 必需模板是否存在"""
    required = [
        "constitution-template.md",
        "archive-workflow.md",
        "context-template.md",
        "adr-template.md",
        "phase7-archive-checklist.md",
        "phase8-checkpoint-template.md",
    ]
    score = 0
    for tmpl in required:
        if (TEMPLATES_DIR / tmpl).exists():
            score += 10 / len(required)
        else:
            print(f"  ⚠️  缺失模板: {tmpl}")
    return round(score, 1)

# --- 主函数 ---

def run_structural_score():
    """运行完整结构评分"""
    print("=" * 40)
    print("clsh-project 结构评分")
    print("=" * 40)

    scores = {}
    scorers = [
        ("流程完整性", score_flow_completeness, 15),
        ("引用完整性", score_reference_integrity, 10),
        ("Pitfall 质量", score_pitfall_quality, 10),
        ("铁律一致性", score_ironclad_consistency, 10),
        ("Checklist 覆盖", score_checklist_coverage, 5),
        ("模板覆盖", score_template_coverage, 10),
    ]

    for name, fn, max_score in scorers:
        result = fn()
        scores[name] = {"score": result, "max": max_score}
        bar = "█" * int(result / max_score * 20)
        print(f"\n  {name}: {result:.1f}/{max_score}")
        print(f"  {bar}")

    total = sum(v["score"] for v in scores.values())
    max_total = sum(v["max"] for v in scores.values())

    print(f"\n{'=' * 40}")
    print(f"  总分: {total:.1f} / {max_total}")
    print(f"{'=' * 40}")

    return scores, total

if __name__ == "__main__":
    scores, total = run_structural_score()

    # 输出 JSON（供程序读取）
    if "--json" in sys.argv:
        print("\n--- JSON ---")
        print(json.dumps({"scores": scores, "total": total}, indent=2, ensure_ascii=False))
