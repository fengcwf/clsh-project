---
name: clsh-project
aliases: [cp]
description: "需求驱动的项目开发工作流 — 从需求澄清到设计文档到实现计划到执行。灵感来自 Kiro 的 Spec-Driven Development、Superpowers 的 Brainstorming 方法论、Phoenix 的状态机执行模式。"
version: 5.39.0
author: 灵犀
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [workflow, project, spec-driven, planning, kanban, methodology]
    related_skills:
      - kanban-orchestrator
      - kanban-worker
      - subagent-driven-development
      - obsidian-operations
      - requesting-code-review
      - plan
      - test-driven-development
      - incremental-build
      - spike
      - diagnose
      - project-wrap-up
---

# /clsh-project — 需求驱动项目开发

## 概述

当大佬提出新的项目或功能需求时，**不直接写代码**，而是走完整的 需求→设计→计划→执行 流程。

## 边界定义

### 管什么
- 流程编排（Phase 1-8 门禁和流转）
- 角色分离（灵犀 ≠ coder）
- 质量保障（checkpoint + review + security scan）
- 文档管理（raw/projects/ 结构）

### 不管什么
- 具体技术实现细节 → `raw/projects/<项目>/references/pitfalls/`
- 调试方法论 → `diagnose` skill
- 代码质量规则 → `code-principles` skill

### 膨胀阈值
- SKILL.md: ≤ 300 行（瘦身后）
- Common Pitfalls: ≤ 80 条
- references/: 详见 `raw/projects/clsh-project/references/INDEX.md`

**核心理念（来自 Kiro + Superpowers + Phoenix + Ralph Loop）：**
- 需求不能跳到编码 — 必须经过需求澄清 → 设计 → 计划
- 文档是锚点 — 需求和设计必须写成文档，防止进度丢失和跑偏
- 分阶段审批 — 每个阶段需要大佬确认后才进入下一阶段
- 一次只问一个问题 — 不要一次性抛出多个问题让大佬回复压力大
- **两阶段 review**（Superpowers）：先检查 spec compliance，再检查 quality
- **刚性管道**（Kiro）：Requirements → Design → Tasks，每阶段有强制审批门禁
- **状态机执行**（Phoenix/MiMo/Qwen）：每个 Task 有明确的 checkpoint、验证条件、失败阻断。流程控制权在代码，不在 LLM
- **Ralph Loop 原则**：灵犀是循环编排者，agent 是单步执行器；客观验证不自判；文件系统+git 是记忆层

### 🛡️ LLM 能力无关性原则（2026-06-02 确立）

**clsh-project 的流程控制不依赖 LLM 判断力。** LLM 强时和 LLM 弱时，流程应产出一致的结果。

**判断标准：** 一个机制如果"LLM 强时正常、LLM 弱时静默失败"，则不得用于流程控制。

#### 判断力分配框架

| 类型 | 谁判断 | 用于 | 不得用于 |
|------|--------|------|---------|
| **机械判断** | 代码/脚本/硬编码 | 门禁检查、轮次上限、状态流转、文件存在性 | — |
| **大佬判断** | clsh | 方案选择、设计确认、优先级裁决、方向变更 | 可自动化的验证步骤 |
| **LLM 判断** | 灵犀/agent | 内容生成、格式化、信息整理、低风险草稿 | 流程控制、质量门禁、严重性分级 |


## ⛔ 流程铁律（不可违反，违反 = 流程违规）

0. **先查进度再行动** — 收到"继续项目"指令时：`ls raw/projects/<项目名>/` → 读 `overview.md` → 读 `changes/` → 从下一个未完成 Phase 继续。禁止凭印象重走已完成的 Phase。
1. **文档先于代码** — Phase 3 未完成 + 大佬未确认，禁止写任何代码
2. **分阶段审批** — 每个 Phase 必须有大佬确认输出才能进入下一 Phase
3. **独立测试** — 代码任务必须有 tester review 卡，禁止自己测自己验收
4. **角色分离** — 灵犀是协调者，不直接改代码。后端→coder，前端逻辑→coder，UI/样式→artist，测试→tester。**效率不是跳过角色分离的理由**。
5. **流程合规自检** — Phase 4 自检必须包含流程合规检查
6. **文档写入路径验证** — 文档必须写入 `raw/projects/<项目名>/changes/<变更名>/`，写入后必须 `ls` 验证
7. **反馈走流程** — 大佬测试反馈问题后，走 Phase 8 反馈循环，禁止"顺手修了"
8. **Checkpoint 机制** — 每个 Task 执行后必须输出 checkpoint（产出物验证），未通过验证不得进入下一 Task
9. **安全扫描** — Phase 6 每个 Task 的 review 必须包含安全扫描
10. **Auto-Fix 上限** — review 发现问题后派 fix agent 修复并重新 review，最多 3 轮后 escalate 给大佬
11. **方案注入** — Phase 6 建卡时，task body 必须注入：(1) proposal.md 相关章节 (2) constitution.md 技术约束 (3) "不在范围内"声明。缺少任一 = 流程违规。
12. **代码交叉验证** — Phase 1 大佬描述现有系统行为时，必须检查代码验证。矛盾时以代码为准。
13. **Context File Pattern** — 复杂任务（body > 500 字）：body 放摘要，详细 spec 写到 `raw/projects/{project}/changes/{变更名}/bugfix-spec.md`，body 中注明**绝对路径**。
14. **5 步验证函数** — 声称完成前必须：(1) IDENTIFY (2) RUN (3) READ (4) VERIFY (5) REPORT。跳过任何一步 = 违规。
15. **渠道匹配用 key 不用 name** — 前后端数据匹配必须用稳定的 key 字段，不能用 name 字段。
16. **Watchdog cron 模式** — 周期性检查类 cron 必须用 `no_agent=true` + 脚本模式。
17. **机械确认码必须脚本生成** — 用 `python3 -c "import secrets,string; ..."` 生成，禁止 LLM 编造。
18. **Phase 确认模板内嵌** — 每个 Phase 结束必须使用对应内嵌模板，`[CODE]` 必须替换为脚本生成的确认码。**例外：** 大佬回复中包含 Phase 所需数据/凭据，可视为隐式确认。
19. **Phase 6 派发必须用模板** — 使用 `phase6-dispatch-template.md` 逐项打勾。
20. **Phase 8 反馈必须用模板** — 使用 `phase8-feedback-template.md` 执行。灵犀直接改代码 = 流程违规。

### ⛔ Phase 8 结束前必须跑机械自检

每轮 Phase 8 修复完成后、向大佬汇报前，必须执行 `phase8-pre-close-checklist.md` 中的 shell 检查脚本。

**违反以上任何一条 = 流程违规，必须记 ERRORS.md。**

## 何时触发

1. 大佬发送 `/clsh-project` 或 `/project`
2. 大佬说"我要做一个 XXX"、"开发一个 XXX 系统"、"实现 XXX 功能"
3. 大佬提出的需求明显是多步骤项目
4. 大佬说"按 Kiro 流程走"、"先做需求分析"
5. 大佬说"review 项目"、"检查实现效果"、"对比设计方案" → **Review Mode**

**不触发：** 简单查询、单步操作、修复 bug（用 systematic-debugging）、已有明确方案的小改动、大佬说"简单做一下"、代码质量审查（PR review）。

## Review Mode（规格合规审查）

7 步：读项目文档 → 读所有代码 → 验证运行状态 → 功能合规矩阵 → Constitution 合规 → 代码质量（P1-P6） → 汇报。

📋 详细流程: `raw/projects/clsh-project/references/workflow/phase-review.md`

**红线：** 产出报告，不直接修复。修复走 Phase 8。

---

## 流程总览

```
Phase 1: 需求澄清（调研循环 + 机械确认码）→ conversation.md
    ↓ [大佬确认]
Phase 2: 提出 2-3 个方案 + 推荐理由 → 大佬选择
    ↓ [大佬确认]
Phase 2.5: Technical Spike（可选）
    ↓ [VALIDATED]
Phase 3: 设计文档 → proposal.md + constitution.md
    ↓ [大佬确认]
Phase 4: 自检 + 大佬确认
    ↓ [大佬确认进入执行]
Phase 5: 实现计划 → tasks.md → 展示给大佬
    ↓
Phase 6: Ralph Loop 分发执行（coder/artist/tester）
    ↓ [tester 通过]
Phase 7: 归档 + 流程复盘
    ↓
Phase 8: 反馈循环 → 回到 Phase 1 或 Phase 6
```

### 🚀 Session Launch Guidance

| 完成 Phase | 下一步 | 建议 |
|-----------|--------|------|
| Phase 1-5 | `/clsh-project 继续 <项目名>` | 当前 session 继续 |
| Phase 6 | `/clsh-project 继续 <项目名>` | 3+ Task 建议新 session |
| Phase 7 | 等待大佬测试反馈 | — |
| Phase 8 | `/clsh-project 继续 <项目名>` | 每轮修复建议新 session |

### 🅿️ 项目暂存

大佬说"先存 wiki，不做"时：写 overview.md（状态 `planning`）+ proposal.md → 向大佬确认 → **不进入 Phase 2+**。

---

## Phase 0+1: 需求准备与澄清

调研循环模式：每个决策点走 `L0→L1→L2` 分层调研→提问→确认微循环。机械确认门禁 + 代码交叉验证 + CONTEXT.md 术语表。

📋 详细流程: `raw/projects/clsh-project/references/workflow/phase0-1-requirements.md`

**Phase 1 确认模板：**
```
需求澄清完成。

决策点：
- [决策1]: [结果]
...

---

🔑 `[CODE]`
📋 复制上面的码回复即可
---
```

---

## Phase 2+2.5: 方案设计与技术验证

2-3 个方案 + 推荐理由 + 对比表格。Phase 2.5: 技术 Spike + 设计 Prototype。

📋 详细流程: `raw/projects/clsh-project/references/workflow/phase2-design.md`

**Phase 2 确认模板：**
```
方案设计完成。

推荐方案：[方案名]
- [关键决策]

📄 详情：raw/projects/<项目>/changes/<变更>/proposal.md

---

🔑 `[CODE]`
📋 复制上面的码回复即可
---
```

---

## Phase 3+4: 设计文档与自检

Phase 3: proposal.md + constitution.md + 可选 ADR。UI 项目必做设计发散。Phase 4: 机械检查 + 流程合规 + 大佬 Review Gate。

### ⛔ Phase 3 模板关键词（机械门禁）

| 文档 | 必须包含的关键词 | 行数上限 |
|------|----------------|---------|
| overview.md | `状态`, `进度表` | ≤ 60 行 |
| conversation.md | `需求`, `决策` | ≤ 60 行 |
| proposal.md | `技术方案`, `不在范围内` | ≤ 70 行 |
| constitution.md | `约束`, `禁止`, `验收标准` | ≤ 60 行 |
| tasks.md | `验收标准`, `不在范围内` | ≤ 80 行 |

📋 详细流程: `raw/projects/clsh-project/references/workflow/phase3-spec.md`
📋 机械自检脚本: `~/.hermes/scripts/phase4-mechanical-check.py`

**Phase 3 确认模板：**
```
设计文档完成。

已输出：
- proposal.md（[行数] 行）
- constitution.md（[行数] 行）

📄 详情：raw/projects/<项目>/changes/<变更>/

---

🔑 `[CODE]`
📋 复制上面的码回复即可
---
```

**Phase 4 确认模板：**
```
自检完成。

文档质量：[PASS/FAIL]
流程合规：[PASS/FAIL]
机械检查：[PASS/FAIL]

---

🔑 `[CODE]`
📋 复制上面的码回复即可
---
```

---

## Phase 5: 实现计划

tasks.md ≤3000 字。每个 Task = kanban 卡，粒度 2-5 分钟。Vertical Slice + No Placeholders + Type Consistency。

📋 详细流程: `raw/projects/clsh-project/references/workflow/phase5-tasks.md`

---

## Phase 6: Ralph Loop 分发执行

### Kanban 派发执行器（Way C — 给路径和目标，不做代码推理）

**task body = Context Engineering 五层架构：**

```
## Context Brain Dump（L1：项目快照）
## Task（L2：任务定义）
## Relevant Files（L3：Selective Include + Trust Levels）
## Pattern to Follow（L3：参考实现）
## Constraints
## Acceptance Criteria
## Not in Scope
```

**角色分工：** coder → kanban worker | artist → kanban worker（+ taste-skill） | tester → kanban review 卡

📋 详细流程: `raw/projects/clsh-project/references/workflow/phase6-execution.md`

---

## Phase 7: 完成归档与流程复盘

归档 9 步 + 流程合规复盘 7 项 + handoff.md。**使用 `handoff` skill。**

### ⛔ 归档文档关键词（机械门禁）

| 文档 | 关键词 | 行数上限 |
|------|--------|---------|
| completion-summary.md | `概述`, `技术`, `功能`, `限制` | ≤ 40 行 |
| retrospective.md | `合规`, `教训`, `改进`, `角色` | ≤ 40 行 |
| handoff.md | `状态`, `建议` | ≤ 30 行 |

📋 详细流程: `raw/projects/clsh-project/references/workflow/phase7-archive.md`

---

## Phase 8: 反馈循环

角色分离 + tester 浏览器验证 + 每轮归档 + 上下文溢出防护（每轮 ≤3-4 bug）。**诊断引擎模式：** 灵犀先读代码+分析根因，写精确 bugfix spec 派 coder。

📋 详细流程: `raw/projects/clsh-project/references/workflow/phase8-feedback.md`

---

## E2E 自动化测试

| 组件 | 路径 |
|------|------|
| 主脚本 | `~/.hermes/scripts/clsh-e2e-test.py` |
| Cron wrapper | `~/.hermes/scripts/clsh-e2e-cron.sh` |

---

## 流程门禁

| 门禁 | 检查内容 | 未通过 → |
|------|---------|---------|
| Phase 3→4 | proposal.md 已写入 + `ls` 验证 | 不允许写代码 |
| Phase 4→5 | 机械确认码 | 不允许写 tasks.md |
| Phase 5→6 | tasks.md 已写入 + 每 Task 有验收标准 | 不允许创建 kanban 卡 |
| Phase 6 执行 | 代码任务必须有 tester 卡 | 不允许标记完成 |
| Phase 6 安全 | Security Scan 通过 | 不允许进入 Quality Review |
| Phase 6 修复 | Auto-Fix 最多 3 轮 | escalate 给大佬 |
| Phase 6 测试 | tester 验证通过 | 不允许汇报完成 |
| Phase 6 Browser QA | UI 项目 tester 必须浏览器验证 | 不允许汇报完成 |

## 核心规则精选

**角色分离：** 禁止灵犀直接写代码 | 禁止 Phase 8 "顺手修了" | 禁止跳过 tester 卡 | Phase 8 必须用 kanban 派发

**Way C 铁律：** 灵犀只给目标+路径+约束，不做代码推理。Pattern to Follow 必做。worker 修复后必须走 tester 验证。

**Phase 8 诊断铁律：** 大佬反馈 bug → 灵犀只记录现象+文件路径 → 创建 kanban 卡让 worker 分析根因。

> 96+ 条完整 pitfalls → `raw/projects/clsh-project/references/pitfalls/common.md`

## ⚠️ Skill 别名

`/cp` 通过 frontmatter `aliases: [cp]` 注册为 `/clsh-project` 的别名。

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v5.39.0 | 2026-06-08 | **references 外迁 + SKILL.md 瘦身**：57 个 active references 迁移到 `raw/projects/clsh-project/references/`。SKILL.md 从 752 行瘦身到 ~280 行（只保留流程摘要+确认模板+路径索引）。frontmatter 清空 references 数组。版本历史只留最近 3 版。 |
| v5.38.0 | 2026-06-08 | **Phase 8 执行教训**：新增 3 条 pitfalls — #111-#113。phase8-feedback.md 新增 pm2 restart 规则。 |
| v5.37.0 | 2026-06-08 | **Kanban CLI 操作模式文档化**：新增 kanban-cli-operational-patterns.md。 |

> 完整版本历史 → `raw/projects/clsh-project/references/templates/version-history.md`

---

## 📚 参考文件索引

所有详细文档已迁移到 `raw/projects/clsh-project/references/`。

📋 **完整索引:** `raw/projects/clsh-project/references/INDEX.md`

### 按需加载路径

| 分类 | 路径 |
|------|------|
| **方法论** | `raw/projects/clsh-project/references/methodology/` |
| **模板** | `raw/projects/clsh-project/references/templates/` |
| **工作流** | `raw/projects/clsh-project/references/workflow/` |
| **教训** | `raw/projects/clsh-project/references/pitfalls/common.md` |
| **集成** | `raw/projects/clsh-project/references/integration/` |
| **E2E 测试** | `raw/projects/clsh-project/references/testing/` |
| **脚本** | `raw/projects/clsh-project/references/scripts/` |
| **归档** | `references/archive/`（仍在 skill 目录） |
