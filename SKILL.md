---
name: clsh-project
aliases: [cp]
description: "需求驱动的项目开发工作流 — 从需求澄清到设计文档到实现计划到执行。DO trigger: 用户说'我要做一个 XXX'、'/clsh-project'、'/cp'。Do NOT trigger: 简单查询、修 bug、已有明确方案的小改动。"
version: 7.0.0
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

## 概述

当用户提出新的项目或功能需求时，**不直接写代码**，走完整 需求→设计→计划→执行 流程。

**核心理念：** 需求不能跳到编码 | 文档是锚点 | 分阶段审批 | 一次只问一个问题 | 两阶段 review | 状态机执行

## 路径约定

> **所有路径通过 config.json 的 `project_docs_dir` 配置，默认 `./project-docs/`。**

## 边界

- **管：** 流程编排（Phase 1-8 门禁）、角色分离、质量保障、文档管理
- **不管：** 技术实现 → `pitfalls-common.md` | 调试 → `systematic-debugging` | 代码质量 → `code-principles`

## 🛡️ 能力无关性

> 流程控制不依赖 LLM 判断力。机械判断（脚本）→ 门禁/状态流转；用户判断 → 方案选择；LLM 判断 → 内容生成。**LLM 不得用于流程控制或质量门禁。**

## ⛔ 三层架构

> **能纯机械不用 LLM | 角色严格分离（协调者 ≠ coder）**

### Layer 1: Gate（违反 = 流程阻断）

| # | 规则 | 机制 |
|---|------|------|
| G0 | **先查进度再行动** — `ls` + 读 overview + changes/ | 文件系统检查 |
| G1 | **Phase 1 预检** — gate-phase1.py: PRODUCT.md + US-*/INV-* + conversation.md | PASS/FAIL + 码 |
| G2 | **Phase 2 预检** — gate-phase2.py: TECH.md + 关键词 + 行数 | PASS/FAIL + 码 |
| G3 | **Phase 3 预检** — gate-phase3.py: proposal.md + constitution.md | PASS/FAIL + 码 |
| G4 | **Phase 4 预检** — gate-phase4.py: 6 文件存在性 + 关键词 + 行数 | PASS/FAIL + 码 |
| G5 | **机械确认码** — sha256(project+phase+time+salt), TTL 30 分钟 | 不可伪造 |
| G6 | **文档路径验证** — 写入后 `ls` 验证 | `ls` 输出 |
| G7 | **C7 review 门禁** — gate-phase7.py: fresh-context reviewer 报告 | PASS/FAIL |

### Layer 2: Convention

| # | 规则 | 机制 |
|---|------|------|
| C3 | **独立测试** — 代码任务必须有 tester，禁止自测自验 | gate-phase6.py |
| C6 | **Task 标注角色** — `(coder)`/`(tester)`/`(artist)` | gate-phase5.py |
| C7 | **spawn fresh-context reviewer** — 协调者不可自判，必须独立验证 | gate-phase7.py |
| C8 | **注入 skills** — coder→TDD+incremental, artist→frontend, tester→review+debug | gate-phase5.py(结构) + gate-phase6.py(执行) |

### Layer 3: Pitfall（Top 5）

| # | 教训 | 规则 |
|---|------|------|
| 1 | 协调者做代码推理 | Way C：给目标+路径+约束，不做推理 |
| 2 | 跳过 tester 验证 | worker done ≠ 已验证 |
| 7 | 跳过 Phase 3 直接写码 | Phase 3 未完成禁止写代码 |
| 14 | fire-and-forget | 派发 ≠ 完成，必须跟踪+验证 |
| 22 | 写入错误路径 | task body 必须指定绝对输出路径 |
| 23 | Phase 1 跳过五维度追问 | E2E 实测：LLM 只覆盖 2/5 维度就确认需求，缺技术/性能/数据调研 |

> 完整 pitfalls → `references/pitfalls-common.md`

## 何时触发

`/clsh-project` 或 `/cp` | "我要做一个 XXX" | 多步骤项目需求 | "按 Kiro 流程走"

**不触发：** 简单查询、修 bug、小改动、"简单做一下"

---

## ⚡ 触发后第一步

> **LLM 第一个 tool call 必须运行 `gate-workflow.py`。LLM 只是脚本输出的执行器。**

```bash
python3 scripts/gate-workflow.py <项目目录>
```

- `status: "continue"` + `current_phase: N` → 执行 Phase N
- `status: "blocked"` → 被拦截，回到正确 Phase
- `status: "complete"` → 进入 Phase 8 或结束

**⛔ 禁止：** 不跑脚本直接写码 | 忽略 current_phase | 忽略 blocked | 在脚本前做实际工作

**Iron Laws（仅在 gate-workflow.py 未运行时）：**
- **IL-1: NO CODE WITHOUT PHASE 1-3 COMPLETED**
- **IL-2: NO SELF-JUDGMENT ON QUALITY**
- **IL-3: COORDINATOR DOES NOT CODE**

---

## Phase 路由表

| Phase | 核心产出 | Gate 脚本 | 关键约束 |
|-------|---------|-----------|---------|
| 0 | learnings + pitfalls 匹配 | 无出口 gate | 读历史教训 |
| 1 | PRODUCT.md + conversation.md | gate-phase1.py | 5 维度追问 |
| 2 | TECH.md | gate-phase2.py | 2-3 方案对比 |
| 3 | proposal.md + constitution.md | gate-phase3.py | proposal 只写决策 |
| 4 | 6 文件合规 | gate-phase4.py | 机械检查 |
| 5 | tasks.md | gate-phase5.py | 协调者只 review |
| 6 | 任务执行 + tester 验证 | gate-phase6.py | 任务系统 + skill |
| 7 | completion + retrospective + handoff | gate-phase7.py | 归档 3 文档 |
| 8 | 反馈循环 | gate-phase8.py | 标准/goal/kanban-goal |

---

## Phase 0: 内化历史教训

读 `learnings/` + `pitfalls-common.md`，匹配 tech/domain 标签。无出口 gate。

## Phase 1: 需求澄清

**5 维度追问框架：** 用户与场景 | 功能与流程 | 安全与威胁 | 合规与隐私 | 行业与技术

追问深度：L0 概览 → L1 细化 → L2 攻防。停止条件：连续 2 维度 L0 无新信息 / 用户说"就这些" / 完成 3 维度 L1。

**产出：** PRODUCT.md（用户故事 + INV-* + 可验证性，📋 `templates/product-md-template.md`）+ conversation.md

```bash
python3 scripts/gate-phase1.py <项目目录>
```

## Phase 2: 方案设计

2-3 方案 + 推荐理由 + 对比表格。Phase 2.5: 技术 Spike。

**产出：** TECH.md（架构决策 + 文件变更范围 + 不在范围内，📋 `templates/tech-md-template.md`）

```bash
python3 scripts/gate-phase2.py <项目目录>
```

## Phase 3+4: 设计文档与自检

Phase 3: proposal.md + constitution.md。**⛔ proposal 只写设计决策。** 📋 `templates/constitution-template.md`

```bash
python3 scripts/gate-phase3.py <项目目录>
```

Phase 4: 6 文件机械检查 + 流程合规。

```bash
python3 scripts/gate-phase4.py <项目目录>
```

## Phase 5: 实现计划

协调者派任务（body 含 proposal + constitution 路径），coder 自己写 tasks.md。**⛔ 协调者只 review 格式。**

- INV-* 全覆盖 | P0 故事必须有任务 | P1/P2 须在 tasks.md 或 TECH.md "范围外"显式排除
- 📋 `templates/tasks-template.md`

```bash
python3 scripts/gate-phase5.py <项目目录>
```

## Phase 6: 分发执行

**角色：** coder/artist → 执行 | tester → 验证。

**执行协议（gate-phase6.py 检查）：**
1. **dispatch 方式**：conversation.md 必须记录派发证据（`delegate_task` 调用 或 `kanban create`）
2. **skill 注入**：派发时必须注入 skills（coder→TDD+incremental, artist→frontend, tester→review+debug）
3. **Level 适配**：Level A 用 kanban/delegate_task，Level B 用 delegate_task，Level C 降级为 WARN
4. **tester 独立验证**：tester-report.md 必须存在且含 PASS/FAIL + 证据

```bash
python3 scripts/gate-phase6.py <项目目录>
```

## Phase 7: 归档与复盘

**产出（不可变更路径）：**
- `changes/archive/completion-summary.md`
- `changes/archive/retrospective.md`
- `changes/archive/handoff.md`

```bash
python3 scripts/gate-phase7.py <项目目录>
```

## Phase 8: 反馈循环

协调者只记录现象+文件+验收标准，coder/artist 自己分析根因+执行。

| 方式 | 适用场景 |
|------|---------|
| 标准模式 | Gateway、简单 bug → fix 卡 + tester 验证 |
| /goal 模式 | CLI/TUI、复杂 bug → judge + gate-phase8 |
| kanban --goal | Gateway fix 卡 → worker 自动迭代 |

**⛔ /goal 限制：** judge 不能替代 tester（C3）| 不能绕过 gate-phase8 | Phase 1-6 禁用

```bash
python3 scripts/gate-phase8.py <项目目录>
```

---

## 📚 参考文件

| 分类 | 路径 |
|------|------|
| Pitfalls | `references/pitfalls-common.md` |
| Gate 脚本 | `scripts/gate-phase*.py` |
| 环境自检 | `scripts/env-check.py` |
| 五框架偏离分析 | `references/five-framework-deviation-analysis-20260623.md` |
| 偏离率度量 | `references/deviation-metrics-20260623.md` |
| 内嵌 skill 拆分 | `references/embedded-skill-plan-20260623.md` |
| Loop Engineering | `references/loop-engineering-framework.md` |

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v7.0.0 | 2026-06-23 | 机械流程控制：gate-workflow.py 唯一入口；Iron Laws 降级为最后防线 |
| v7.2.0 | 2026-06-23 | 偏离分析 + 五框架对比：偏离根因是插件 Layer 3 从未实现 |
| v7.3.0 | 2026-06-23 | 8 轮审查结论：先瘦身 446→~220 行观察偏离率 |
