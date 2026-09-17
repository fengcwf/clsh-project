---
name: clsh-project
aliases: [cp]
description: "需求驱动的项目开发工作流 — 从需求澄清到设计文档到实现计划到执行。DO trigger: 用户说'我要做一个 XXX'、'/clsh-project'、'/cp'。Do NOT trigger: 简单查询、修 bug、已有明确方案的小改动。"
version: 9.5.0
author: clsh
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [workflow, project, spec-driven, planning, methodology]
    pinned: true
    related_skills:
      - kanban-worker
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

> **v9.1 Superpowers 6.0 优化**：
> - P1: 预生成 Review Package（`gen-review-package.sh`）→ tester 不跑 git，-10% token
> - P2: 简洁审查合同（tester-report 双轴判定+证据）→ -40% 输出
> - P3: Task Brief 文件化（`task-N-brief.md`）→ 主会话 -30% 上下文

> **v9.2 MoA 优化**（Superpowers v6.2.0 对标）：
> - P4: Ledger 进度追踪（`ledger.md`）→ 填补 compaction 信息丢失空白
> - P5: Scoped Re-Review（`re-review-prompt.md`）→ 修复后范围审查，-50-70% token
> - P6: 合理化表格（Excuse/Reality）→ 对撞式拦截，行为遵从率 +30%
> - P7: Fix Loop 升级机制（R1-R5 circuit breaker）→ 防止无限循环

> **v9.3 Phase 8 Optimization Loop**（Ralph Loop + Superpowers 对标）：
> - P8: Fresh Context Per Iteration → 每个任务 delegate_task（子 agent 天然 fresh context）
> - P9: One Thing Per Iteration → 每轮优化只处理一个反馈（Ralph 铁律）
> - P10: Two-Phase → Gap Analysis（只读不改）→ Implementation（fresh context）
> - P11: 全局 Circuit Breaker → max_rounds=10 + timeout=15min + stuck=3 轮
> - P12: Skill Anchoring → 每次处理反馈时声明"我在使用 clsh-project 的优化循环"

> **v9.4 项目基础设施初始化（Init）**：
> - I1: Init 前置门禁 → Phase 0 前必须完成目录确认 + project/board/项目 bot 创建，gate-init.py 机械验证
> - I2: 目录每次与用户确认（IL-INIT-1）→ 禁止静默使用默认目录
> - I3: 项目专用 bot（5 角色，从 artist/coder/scout/tester/reviewer 克隆）→ kanban 派活禁用全局 profile
> - I4: Phase 6 不再创建 project/board → 基础设施只在 init 创建一次

> **v9.5 视觉定稿（Phase 2.5 视觉 Spike）**：
> - V1: UI 类项目参考图 2-3 候选 → 用户定稿 1 张（visual/final.png）+ DESIGN.md token 化
> - V2: gate-phase2.py 机械检查（PRODUCT.md UI 关键词触发；非 UI 项目用 .cp-visual-skip 显式跳过）
> - V3: Phase 6 tester 视觉保真检查（截图 vs 定稿图 + token 对比）——修复 Superpowers #1783 实证的"文字决策→实现漂移"
> - V4: gate-phase1.py v2.1 加固——用户过渡声明 ≥3 次（IL-9 停止条件机械代理）+ 15 轮安全阀拦截（.cp-human-intervention 豁免）+ IL-NEW-4 中途禁要码（openwrt-agent 17 轮教训）

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

> 合理化是 LLM 本能偏差。合理例外不存在。对撞式表格拦截跳步想法（Superpowers v6.2.0 实证：表格形式比 prose 段落行为遵从率高 30%）。
> 如果你发现自己在引用本表格来确认跳步 → **你在合理化，立即停止。**

| 你的想法 | 真相 |
|----------|------|
| "这只是一个简单问题，先做再说" | 问题是任务，先查 skill |
| "我先需要更多上下文" | skill 检查在澄清之前 |
| "让我先看看代码库" | skill 告诉你怎么看 |
| "我记得这个 skill" | skill 会演进，读最新版 |
| "这不需要正式流程" | 大佬说"简单做一下"才跳流程 |
| "我在用这个表格确认我的做法" | 你在合理化，立即停止 |

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

- `status: "blocked"` + `current_phase: "init"` → 项目未初始化，加载 `init-project.md` 执行初始化
  （⛔ 目录必须每次与用户确认；gate-init.py 验证 + 用户确认码通过后才能进 Phase 0）
- `status: "continue"` + `current_phase: N` → 执行 Phase N
- `status: "blocked"`（其他） → 被拦截，回到正确 Phase
- `status: "complete"` → 进入 Phase 8 或结束

**⛔ 禁止：** 不跑脚本直接写码 | 忽略 current_phase | 在脚本前做实际工作 | 跳过 init 直接进 Phase 0

---

## Phase 路由表

| Phase | 核心产出 | Gate 脚本 | 详细指令 |
|-------|---------|-----------|---------|
| init | .cp-init.json（目录确认 + project/board/5 bot） | gate-init.py | `init-project.md` |
| 0 | phase0-data.json + phase0-research.md | gate-phase0.py | `phase0-research.md` |
| 1 | PRODUCT.md + conversation.md | gate-phase1.py | `phase1-exploration.md` |
| 2 | TECH.md（UI 类 + DESIGN.md/定稿图，Phase 2.5） | gate-phase2.py | `phase2-spec.md` |
| 3 | proposal.md + constitution.md | gate-phase3.py | `phase3-design.md` |
| 4 | 6 文件合规 | gate-phase4.py | `phase4-review.md` |
| 5 | tasks.md | gate-phase5.py | `phase5-plan.md` |
| 6 | 任务执行 + tester 验证 | gate-phase6.py | `phase6-execute.md` |
| 7 | completion + retrospective + handoff | gate-phase7.py | `phase7-archive.md` |
| 8 | 优化循环（Fresh Context + One Thing + Circuit Breaker） | gate-phase8.py | `phase8-optimization-loop.md` |

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
