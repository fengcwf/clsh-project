# 验证框架与棘轮机制

> 日期：2026-05-29
> 来源：Superpowers（验证门禁）+ darwin-skill（棘轮机制）+ ECC（置信度评分）
> 用途：clsh-project 自进化方案的核心组件

---

## 一、5 步验证函数（来自 Superpowers）

### 核心原则

**"没证据不许声称完成"** — 验证必须是独立的、客观的、不可跳过的。

### 函数定义

```
BEFORE 声称任务完成/修复成功/测试通过：
  Step 1: IDENTIFY — 什么命令/证据能证明声明成立？
  Step 2: RUN — 执行验证命令（新鲜的，不复用之前的输出）
  Step 3: READ — 完整读取输出 + exit code
  Step 4: VERIFY — 输出是否符合预期？（逐条对照验收标准）
  Step 5: REPORT — 带证据汇报。跳过任何一步 = 违规
```

### 应用场景

| 场景 | Step 1 (IDENTIFY) | Step 2 (RUN) | Step 4 (VERIFY) |
|------|-------------------|--------------|-----------------|
| CodeWhale 修复完成 | `node -c` + 功能测试命令 | 执行 | exit code 0 + 功能正常 |
| UI 修改完成 | 浏览器访问页面 | 截图 | 截图符合设计稿 |
| API 修复完成 | curl 调用端点 | 执行 | 返回预期格式+数据 |
| 文件创建完成 | `ls` + `cat` 头部 | 执行 | 文件存在且内容正确 |
| 依赖安装完成 | `npm list` / `pip list` | 执行 | 版本匹配 |

### 铁律

- **验证命令必须新鲜执行** — 不能用"之前测试过"替代
- **验证输出必须完整读取** — 不能只看 exit code，忽略 stderr
- **验证必须逐条对照** — 不能"整体看起来对"
- **没有验证证据的 PASS = 违规** — 必须记录到 ERRORS.md

---

## 二、防辩解表（来自 Superpowers）

### 核心洞察

Agent 总会找到借口跳过验证。必须预先堵住所有借口。

| 灵犀/Agent 的借口 | 现实 | 正确做法 |
|-------------------|------|---------|
| "CodeWhale 说改好了" | CodeWhale ≠ 功能验证 | 跑验证命令 |
| "代码看起来对" | 代码 ≠ 运行中的系统 | 浏览器/curl 实际验证 |
| "之前测试过了" | 之前的测试 ≠ 当前的代码 | 重新执行验证 |
| "应该可以了" | 应该 ≠ 验证过 | IDENTIFY → RUN → VERIFY |
| "这次改动很小" | 小改动也会引入回归 | 跑回归测试 |
| "没有环境测试" | 缺环境 ≠ 可以跳过验证 | escalate 给大佬 |
| "agent 自己验证过了" | 自己验自己 = 不独立 | 灵犀独立验证或派 tester |
| "时间来不及了" | 赶进度 ≠ 可以跳质量 | 超时回滚，不交半成品 |

### 使用方式

- Phase 6 每个 Task 的 checkpoint 时，对照检查
- Phase 8 每轮修复后的验证时，对照检查
- 发现自己/agent 正在使用表中的借口 → 立即停止，改用正确做法

---

## 三、Pitfall 置信度评分（来自 ECC Instinct）

### 评分标准

| 置信度 | 含义 | 触发条件 | 行为 |
|--------|------|---------|------|
| 0.3 | 新发现，观察中 | 只出现过 1 次 | 记录到 pitfall，不强制检查 |
| 0.5 | 初步确认 | 出现过 2-3 次，或有明确反例 | Phase 4 自检时提醒 |
| 0.7 | 确认有效 | 出现过 3+ 次，或导致过严重后果 | Phase 6 派发时强制注入 task body |
| 0.9 | 系统性问题 | 反复出现，已确认不可绕过 | 升级为铁律，不可违反 |

### 进化路径

```
事件发生 → 记录 pitfall（置信度 0.3）
  ↓
再次发生 → 置信度升至 0.5
  ↓
第 3 次发生 → 置信度升至 0.7 → 强制注入 task body
  ↓
反复发生 → 置信度升至 0.9 → 升级为铁律
  ↓
铁律写入 SKILL.md 流程铁律 section
```

### 降级路径

```
pitfall 置信度 0.7+ 但连续 5 个项目未触发
  ↓
降级为 0.5（观察）
  ↓
连续 10 个项目未触发
  ↓
标记为"候选淘汰"，大佬确认后移除
```

### 初始置信度（现有 pitfalls）

基于历史触发频率的初始评估：

| 置信度 | Pitfalls |
|--------|---------|
| **0.9**（铁律级） | #1（角色分离）、#2（禁止顺手修）、#39（不做代码推理）、#40（跳过 tester 验证）、#49（告诉 CodeWhale 怎么改） |
| **0.7**（高优先） | #5（delegate_task 替代 kanban）、#11（方案注入）、#13（Context File Pattern）、#23（Bugfix Spec 不列调用点）、#34（tester 只读代码）、#47（CodeWhale 文件损坏） |
| **0.5**（标准） | #6-#10（流程完整性类）、#14-#20（质量保障类）、#25-#30（技术陷阱类）、#41-#46（CodeWhale/Vue 类） |
| **0.3**（观察中） | #18-#19（飞书/chromium 路径）、#27-#28（agent CLI/API 等待）、#42（Vue 响应式） |

---

## 四、棘轮机制（来自 darwin-skill）

### 核心理念

**"只保留可测量的改进，其余回滚"** — 分数只升不降。

### 评分维度（满分 100）

#### 结构评分（60 分）— 可自动化

| 维度 | 分值 | 评分方式 |
|------|------|---------|
| 流程完整性 | 15 | Phase 1-8 定义是否完整、门禁是否明确、workflow 文档是否齐全 |
| 引用完整性 | 10 | references/ 文件是否存在、SKILL.md 中的链接是否断 |
| Pitfall 质量 | 10 | 有反例/正例？有验证方法？有触发关键词？格式一致？ |
| 铁律一致性 | 10 | 铁律之间不矛盾、铁律与 pitfalls 不冲突、编号连续无重复 |
| Checklist 覆盖 | 5 | Verification Checklist 覆盖所有铁律和高置信度 pitfalls |
| 模板覆盖 | 10 | templates/ 覆盖所有需要模板的场景 |

#### 效果评分（40 分）— 需要采样数据

| 维度 | 分值 | 评分方式 |
|------|------|---------|
| 执行合规率 | 25 | 从 session 日志中统计规则被执行的比例（抽样最近 5 个项目） |
| 回归防护 | 15 | 新版本是否引入退化（对比上次评分） |

### 棘轮规则

```
patch SKILL.md 或 workflow 文档
  ↓
运行结构评分（自动化）
  ↓
结构分 ≥ 上次基线？ → PASS → 保存 + 更新基线
结构分 < 上次基线？ → BLOCK → 报告哪些维度退化
  ↓
（每 5 版一次）运行效果评分（采样）
  ↓
效果分 ≥ 上次基线？ → PASS
效果分 < 上次基线？ → WARNING → 大佬决定是否保留
```

### 自动化脚本设计

```python
#!/usr/bin/env python3
"""clsh-project 质量评分器 — 结构评分部分"""

import re
import os
from pathlib import Path

SKILL_DIR = Path("/root/.hermes/skills/productivity/clsh-project")
SKILL_MD = SKILL_DIR / "SKILL.md"
WORKFLOW_DIR = SKILL_DIR / "references" / "workflow"
TEMPLATES_DIR = SKILL_DIR / "references" / "templates"
METHODOLOGY_DIR = SKILL_DIR / "references" / "methodology"

def score_flow_completeness():
    """流程完整性 (15分) — Phase 1-8 定义是否完整"""
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
            score += 2  # 每个 Phase 2 分
        else:
            score -= 1  # 缺失扣分
    # 检查 SKILL.md 中是否有流程总览
    content = SKILL_MD.read_text()
    if "Phase 1:" in content and "Phase 8:" in content:
        score += 1
    return max(0, min(15, score))

def score_reference_integrity():
    """引用完整性 (10分) — references/ 文件是否存在"""
    content = SKILL_MD.read_text()
    # 提取所有 references/ 引用
    refs = re.findall(r'references/[^\s\)`]+\.md', content)
    score = 10
    for ref in refs:
        filepath = SKILL_DIR / ref
        if not filepath.exists():
            score -= 1
    return max(0, score)

def score_pitfall_quality():
    """Pitfall 质量 (10分) — 有反例？有验证方法？"""
    content = SKILL_MD.read_text()
    pitfalls = re.findall(r'^\d+\.\s+\*\*.*?\*\*\s+—\s+(.+)$', content, re.MULTILINE)
    if not pitfalls:
        return 0
    score = 0
    for p in pitfalls:
        has_example = "反例" in p or "正例" in p or "案例" in p
        has_rule = "**规则：" in p or "**修复：" in p or "**正确做法" in p
        if has_example:
            score += 0.1
        if has_rule:
            score += 0.1
    # 归一化到 0-10
    return min(10, score * 10 / len(pitfalls) * 5)

def score_ironclad_consistency():
    """铁律一致性 (10分) — 不矛盾、编号连续"""
    content = SKILL_MD.read_text()
    # 提取流程铁律编号
    ironclad = re.findall(r'^(\d+)\.\s+\*\*', content, re.MULTILINE)
    score = 10
    # 检查编号连续性
    nums = [int(x) for x in ironclad if int(x) < 100]
    for i in range(len(nums)-1):
        if nums[i+1] - nums[i] > 2:  # 允许小间隔
            score -= 1
    # 检查重复编号
    from collections import Counter
    dupes = {k: v for k, v in Counter(nums).items() if v > 1}
    score -= len(dupes) * 2
    return max(0, score)

def score_checklist_coverage():
    """Checklist 覆盖 (5分) — 覆盖铁律和高置信度 pitfalls"""
    content = SKILL_MD.read_text()
    checklist_match = re.search(r'## Verification Checklist.*?(?=##|\Z)', content, re.DOTALL)
    if not checklist_match:
        return 0
    checklist = checklist_match.group(0)
    items = re.findall(r'- \[.\]', checklist)
    # 每个检查项 0.3 分，最多 5 分
    return min(5, len(items) * 0.3)

def score_template_coverage():
    """模板覆盖 (10分)"""
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
    return round(score, 1)

def run_structural_score():
    """运行完整结构评分"""
    scores = {
        "流程完整性": score_flow_completeness(),
        "引用完整性": score_reference_integrity(),
        "Pitfall 质量": score_pitfall_quality(),
        "铁律一致性": score_ironclad_consistency(),
        "Checklist 覆盖": score_checklist_coverage(),
        "模板覆盖": score_template_coverage(),
    }
    total = sum(scores.values())
    return scores, total

if __name__ == "__main__":
    scores, total = run_structural_score()
    print("=== clsh-project 结构评分 ===")
    for dim, score in scores.items():
        print(f"  {dim}: {score:.1f}")
    print(f"  ─────────────────")
    print(f"  总分: {total:.1f} / 60")
