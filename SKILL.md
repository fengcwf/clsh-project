---
name: clsh-project
aliases: [cp]
description: "需求驱动的项目开发工作流 — 从需求澄清到设计文档到实现计划到执行。DO trigger: 用户说'我要做一个 XXX'、'/clsh-project'、'/cp'。Do NOT trigger: 简单查询、修 bug、已有明确方案的小改动。"
version: 9.0.0
author: clsh
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [workflow, project, spec-driven, planning, methodology]
    related_skills:
      - kanban-orchestrator
      - plan
      - test-driven-development
      - incremental-implementation
      - code-review-and-quality
      - doubt-driven-development
---

# /clsh-project — 需求驱动项目开发（通用版）

## ⚠️ LLM 必读

> **gate-enforcer v5.0**：六层机械门禁（L1-L5 不变 + L6 Phase 加载拦截）
> **Phase 文件按需加载**：执行 Phase N 前必须 `skill_view("clsh-project", file_path="phaseN-xxx.md")`
> **模板路径**：Obsidian 绝对路径 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/`
> **完整指南：** `references/llm-review-guide.md`

## 概述

需求驱动项目开发工作流。Phase 0-8 顺序执行，每 Phase 有独立门禁。
**核心理念：** 需求不能跳到编码 | 文档是锚点 | 分阶段审批 | 机械判断优先

## 路径约定

> **模板**：Obsidian raw/ 单副本 + 绝对路径（旧版铁律）
> **产出物**：项目目录下（由 config.json 的 project_docs_dir 配置）

## ⛔ 能力无关性

> 机械判断（脚本）→ 门禁/状态流转 | 用户判断 → 方案选择 | LLM 判断 → 内容生成
> **LLM 不得用于流程控制或质量门禁。**

## ⛔ 三层架构（精简版）

| Layer | 规则 | 违反后果 |
|-------|------|---------|
| **Gate** | G0-G7 机械门禁 | 流程阻断 |
| **Convention** | C3/C6/C7/C8 角色约束 | 警告+修复 |
| **Pitfall** | Top 6 历史教训 | 参考规避 |

## 🛡️ Anti-Rationalization Guard

> 合理化是 LLM 本能偏差。合理例外不存在。6 个 Red Flag（命令性语气）拦截跳步想法。
> RF-6: 如果你发现自己在引用本 Guard 来确认跳步 → **你在合理化，立即停止。**

## ⛔ Iron Laws

- IL-1: **NO CODE WITHOUT PHASE 1-3 COMPLETED**
- IL-2: **NO SELF-JUDGMENT ON QUALITY**
- IL-3: **COORDINATOR DOES NOT CODE**

## 何时触发

`/clsh-project` 或 `/cp` | "我要做一个 XXX" | 多步骤项目需求
**不触发：** 简单查询、修 bug、小改动、"简单做一下"

---

## ⚡ 触发后第一步

> **LLM 第一个 tool call 必须运行 `gate-workflow.py`。**

```bash
python3 scripts/gate-workflow.py <项目目录>
```

- `status: "continue"` + `current_phase: N` → 执行 Phase N
- `status: "blocked"` → 被拦截，回到正确 Phase
- `status: "complete"` → 进入 Phase 8 或结束

**⛔ 禁止：** 不跑脚本直接写码 | 忽略 current_phase | 在脚本前做实际工作

---

## Phase 路由表

| Phase | 核心产出 | Gate 脚本 | 详细指令 |
|-------|---------|-----------|---------|
| 0 | phase0-data.json + phase0-research.md | gate-phase0.py | `phase0-research.md` |
| 1 | PRODUCT.md + conversation.md | gate-phase1.py | `phase1-exploration.md` |
| 2 | TECH.md | gate-phase2.py | `phase2-spec.md` |
| 3 | proposal.md + constitution.md | gate-phase3.py | `phase3-design.md` |
| 4 | 6 文件合规 | gate-phase4.py | `phase4-review.md` |
| 5 | tasks.md | gate-phase5.py | `phase5-plan.md` |
| 6 | 任务执行 + tester 验证 | gate-phase6.py | `phase6-execute.md` |
| 7 | completion + retrospective + handoff | gate-phase7.py | `phase7-archive.md` |
| 8 | 反馈循环 | gate-phase8.py | `phase8-feedback.md` |

**⛔ Phase 加载规则（L6 强制）：**
执行任何 Phase 前，必须先加载对应指令：
```
skill_view("clsh-project", file_path="phaseN-xxx.md")
```
未加载直接执行 → gate-enforcer L6 拦截。

---

## 📚 参考文件

| 分类 | 路径 |
|------|------|
| LLM Review 指南 | `references/llm-review-guide.md` |
| Pitfalls | `references/pitfalls-common.md` |
| Gate 脚本 | `scripts/gate-phase*.py` |
| 模板 | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/` |
