---
name: clsh-project
aliases: [cp]
description: "需求驱动的项目开发工作流 — 从需求澄清到设计文档到实现计划到执行。DO trigger: 用户说'我要做一个 XXX'、'/clsh-project'、'/cp'。Do NOT trigger: 简单查询、修 bug、已有明确方案的小改动。"
version: 8.0.0
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

## ⚠️ LLM 必读（Review/执行前必看）

> **完整指南：** `references/llm-review-guide.md`（gate-enforcer 机制、subagent 盲区、Profile 隔离、已知缺陷）
>
> **关键机制速查：**
> - **gate-enforcer 插件 v4.0**：五层机械门禁（L1 码拦截 + L2 写入拦截 + L3 顺序拦截 + L4 delegate_task toolset 拦截 + L5 PRODUCT.md 前置拦截）
> - **Phase 0 纯机械扫描**：phase0-scan.py 输出 JSON，LLM 不参与扫描
> - **Phase 1 缺口驱动探索追问**：基于 phase0-research.md 的信息缺口，探索→追问交替
> - **tester profile 无 terminal**：物理限制，tester 不能 curl/shell，只能用浏览器工具
> - **确认码 4 位**，输出带 `📋 确认码（复制用）: XXXX`

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

## Phase 0: 内化历史教训 + 机械扫描

**两步执行（先机械后 LLM）：**

### Step 0: 机械扫描（零 LLM 依赖）

```bash
python3 scripts/phase0-scan.py <项目目录>
```

输出 `phase0-data.json`（项目结构/技术栈/Obsidian 匹配/历史教训），**LLM 不参与此步骤**。

### Step 1: LLM 分析（基于 JSON 数据）

读取 `phase0-data.json` → 分析信息缺口 → 写 `phase0-research.md`。
📋 `templates/phase0-research-template.md`

```bash
python3 scripts/gate-phase0.py <项目目录>
```

**⛔ 铁律：**
- IL-4: **必须先运行 phase0-scan.py** — 无 phase0-data.json 不得进入 Phase 1
- IL-5: **必须写 phase0-research.md** — 无调研摘要不得进入 Phase 1
- IL-6: **phase0-research.md 必须引用 phase0-data.json 数据** — 不得编造

## Phase 1: 需求澄清（缺口驱动探索追问）

**基于 Phase 0 的 phase0-research.md 中的信息缺口，探索+追问交替进行。**

### 执行节奏

```
Round 1-3:  探索缺口（web_search/竞品/技术调研）→ 追问确认
Round 4-6:  针对回答中的新缺口 → 定向探索 → 追问补充
Round 7+:   纯追问澄清（不再探索，信息已充分）
```

### 每轮工作流

1. **read_file phase0-research.md** — 注入信息缺口清单（不是全部 context 累积）
2. **探索**（前 3 轮必须）：web_search / 竞品分析 / Obsidian 相关文档深度阅读
3. **追问**：基于探索结果，从不同角度追问用户
4. **持久化**：追问记录写入 conversation.md（不是留在 context 中）

### 停止条件

- **正常停止**：用户主动确认"材料足够" / 连续 3 轮无新信息
- **安全阀**：硬上限 15 轮 → 暂停，请求人工介入（不强制推进）
- **⛔ LLM 不得主动建议进入下一阶段** — 只追问，不推进

### 范围蔓延拦截

用户提出新功能想法 → 记录到 backlog.md → 不纳入当前阶段

### 铁律

- IL-7: **Round 1-3 必须使用探索工具**（web_search/grep/browser）— 纯问答不算
- IL-8: **每轮必须 read_file phase0-research.md** — 确保缺口清单在 context 中
- IL-9: **停止条件由用户控制** — LLM 不得主动建议"可以进入 Phase 2"

### 产出

📋 `templates/product-md-template.md`

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
| **LLM Review 指南** | `references/llm-review-guide.md` |
| Pitfalls | `references/pitfalls-common.md` |
| Gate 脚本 | `scripts/gate-phase*.py` |
| 环境自检 | `scripts/env-check.py` |
| 模板 | `templates/` (9 个模板) |

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v8.0.0 | 2026-06-24 | Phase 0-1 重构：机械扫描(phase0-scan.py)+缺口驱动探索追问+Phase0门禁+五层gate-enforcer(L5 PRODUCT.md拦截) |
| v7.4.0 | 2026-06-24 | 四层门禁(L4 delegate_toolset) + 确认码4位 + Phase6 coordinator review + tester禁terminal + 3模板补齐 + LLM review guide |
| v7.0.0 | 2026-06-23 | 机械流程控制：gate-workflow.py 唯一入口；Iron Laws 降级为最后防线 |
| v7.2.0 | 2026-06-23 | 偏离分析 + 五框架对比：偏离根因是插件 Layer 3 从未实现 |
| v7.3.0 | 2026-06-23 | 8 轮审查结论：先瘦身 446→~220 行观察偏离率 |
