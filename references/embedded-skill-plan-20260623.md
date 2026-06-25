# clsh-project 内嵌 skill 拆分方案（最终版 v2）

**日期**: 2026-06-25  
**状态**: 待执行  
**基于**: R1-R4 四轮分析 + 旧版路径策略回溯 + Superpowers 模式对齐

## 背景

SKILL.md 302 行（v8.0.0），4 轮审查结论：
- 拆分理由是**按需加载+可维护性**（不是"太长"）
- 拆分净收益 ~15,000 tokens/会话
- v8.0.0 模板路径偏离了旧版"Obsidian 绝对路径"策略，需回归

## 方案

Phase 指令拆为 SKILL.md 同级扁平文件（Superpowers 风格），模板回归 Obsidian 绝对路径。

```
clsh-project/
├── SKILL.md              (~110行, 路由+红线)
├── phase0-research.md    ← 与 SKILL.md 同级（扁平）
├── phase1-exploration.md
├── phase2-spec.md
├── phase3-design.md
├── phase4-review.md
├── phase5-plan.md
├── phase6-execute.md
├── phase7-archive.md
├── phase8-feedback.md
├── scripts/              (不变)
└── references/           (只保留静态参考)
    ├── pitfalls-common.md
    └── llm-review-guide.md

Obsidian raw/projects/clsh-project/references/templates/  ← 模板唯一真相源
```

## 加载机制

- 主 SKILL.md：自动注入（红线+路由表）
- Phase 文件：gate-workflow.py 返回 current_phase → LLM 调用 `skill_view("clsh-project", file_path="phaseN-xxx.md")`
- **L6 强制**：gate-enforcer v5.0 新增 Phase 加载拦截（纯机械）
- 模板：Obsidian 绝对路径，子 agent 直接 read_file()

## 主 SKILL.md 保留（~110行）

YAML frontmatter + 概述 + 边界 + 能力无关性 + 三层架构精简表 + 触发条件 + gate-workflow.py 路由 + Phase 路由表 + L6 说明 + 参考索引

## 各 Phase 文件（20-30行）

YAML frontmatter(phase/name/gate_script/output_files) + 前置依赖 + 步骤 + 铁律 + 产出物(绝对路径模板) + 验收标准 + 常见陷阱

## 与旧版对齐

| 项目 | 旧版策略 | v8.0.0 偏离 | v9.0.0 修正 |
|------|---------|------------|------------|
| 模板存放 | Obsidian raw/ 单副本 | skill-local templates/ | 回归 Obsidian |
| 模板引用 | 绝对路径 | 相对路径 | 回归绝对路径 |
| 生成物存放 | Obsidian raw/projects/ | references/ 混放 | 回归 Obsidian |
| 子 agent 路径 | 绝对路径无歧义 | 需知 skill 目录 | 回归绝对路径 |

## gate-enforcer v5.0

新增 L6（Phase 加载拦截）：
- 复用已有 `workflow-initialized.json` marker（gate-workflow.py 写入）
- 内存状态 `_phase_state` 字典（不需要额外文件）
- 扁平匹配：`file_path.startswith("phase") and file_path.endswith(".md")`
- L1-L5 完全不变

## 迁移

~5.5h。Phase A(提取文件 2h) + Phase B(SKILL.md 精简 1h) + Phase C(gate-enforcer L6 1.5h) + Phase D(验证 1h)。

## 参考

- R1-R4 详细分析：`/root/clsh-project-r2-analysis.md`, `/root/clsh-project-r3-analysis.md`, `/root/clsh-project-r4-synthesis.md`
- 旧版路径策略：`references/embedded-vs-external-workflow-pattern.md`
- Superpowers 结构分析：`/root/.hermes/skills/devops/skill-management/references/superpowers-structure-analysis.md`
