---
name: clsh-project
description: "需求驱动的项目开发工作流 — 从需求澄清到设计文档到实现计划到执行。灵感来自 Kiro 的 Spec-Driven Development、Superpowers 的 Brainstorming 方法论、Phoenix 的状态机执行模式。"
version: 5.19.0
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
    references:
      # 方法论（clsh-project 流程知识，保留本地）
      - references/methodology/ralph-loop-analysis.md
      - references/methodology/openspec-comparison.md
      - references/methodology/kiro-superpowers-analysis.md
      - references/methodology/agent-skill-execution-research.md
      - references/methodology/superpowers-v5-changes.md
      - references/methodology/superpowers-architecture-analysis.md
      - references/methodology/matt-pocock-patterns.md
      - references/methodology/external-framework-evaluation.md
      - references/methodology/self-evolution-mechanism.md
      - references/methodology/four-framework-analysis.md
      - references/methodology/optimization-deep-dive.md
      # 模板（clsh-project 流程模板，保留本地）
      - references/templates/constitution-template.md
      - references/templates/archive-workflow.md
      - references/templates/cloud-server-wireguard.md
      - references/templates/phase7-archive-checklist.md
      - references/templates/phase8-checkpoint-template.md
      - references/templates/context-template.md
      - references/templates/adr-template.md
      - references/templates/verification-checklist.md
      - references/templates/version-history.md
      # 集成（clsh-project 工具链，保留本地）
      - references/integration/kanban-tasks-bridge.md
      - references/integration/hermes-slash-command-mechanism.md
      - references/integration/hermes-plugin-zero-token.md
      - references/integration/hermes-plugin-hooks-reference.md
      - references/integration/halo-auth.md
      - references/integration/halo-cli-auth.md
      - references/integration/reference-migration-pattern.md
      - references/integration/hermes-pitfalls.md
      - references/workspace-sub-module-pattern.md
      - references/workspace-network-module-pattern.md
      - references/pitfalls/common.md
      - references/templates/version-history.md
      - references/templates/verification-checklist.md
      - references/methodology/self-evolution-mechanism.md
      # 教训（流程违规案例，保留本地）
      - references/pitfalls/violation-case-2026-05-15.md
      - references/pitfalls/violation-case-2026-05-15-self-coding.md
      - references/pitfalls/violation-case-2026-05-18.md
      - references/pitfalls/violation-case-2026-05-20.md
      - references/pitfalls/phase8-context-management.md
      - references/pitfalls/phase8-session-management.md
      - references/pitfalls/phase8-frontend-debug-patterns.md
      - references/pitfalls/memory-tool-traps-2026-05-21.md
      - references/pitfalls/technical-traps-2026-05-20.md
      - references/pitfalls/ui-design-open-design-enforcement.md
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
- Hermes 工具链使用细节 → `references/integration/hermes-pitfalls.md`
- 调试方法论 → `diagnose` skill
- 代码质量规则 → `code-principles` skill

### 膨胀阈值
- SKILL.md: ≤ 900 行
- Common Pitfalls: ≤ 24 条（超出迁移）
- references/: ≤ 25 个文件（超出归档）

**核心理念（来自 Kiro + Superpowers + Phoenix + Ralph Loop）：**（详见 `references/methodology/kiro-superpowers-analysis.md` 和 `references/methodology/ralph-loop-analysis.md`）
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

**来源教训：** Superpowers v5.0.6 用 inline self-review 替代独立 tester（"质量没差"），前提是 Claude 足够强。Harness 用 Team Debate 做多视角 review，依赖 LLM 能区分严重性。两者都是"用 LLM 能力换效率"，clsh-project 不走这条路。

#### 判断力分配框架

所有流程决策必须按以下三类分配，不得混用：

| 类型 | 谁判断 | 用于 | 不得用于 |
|------|--------|------|---------|
| **机械判断** | 代码/脚本/硬编码 | 门禁检查、轮次上限、状态流转、文件存在性 | — |
| **大佬判断** | clsh | 方案选择、设计确认、优先级裁决、方向变更 | 可自动化的验证步骤 |
| **LLM 判断** | 灵犀/agent | 内容生成、格式化、信息整理、低风险草稿 | 流程控制、质量门禁、严重性分级 |

**行动规则：**
1. 优化流程时，先判断改动是否引入新的 LLM 依赖。如果是 → 需要大佬确认
2. 机械判断优先于 LLM 判断 — 即使 LLM 判断"更智能"
3. 大佬判断优先于 LLM 判断 — 大佬是最终裁决者
4. Review 的价值在于 checklist 的质量，不在于 reviewer 的数量（保留独立 tester，不改 inline self-review）


## ⛔ 流程铁律（不可违反，违反 = 流程违规）

以下规则优先级高于一切效率考量：

0. **先查进度再行动** — 收到"继续项目"指令时，必须按以下顺序确认进度：
   - **第一步：** `ls raw/projects/<项目名>/` 检查项目容器是否存在
   - **第二步：** 读 `overview.md` 确认当前 Phase 和状态
   - **第三步：** 读 `changes/` 下的文档确认已完成的工作
   - **第四步：** 只有确认进度后，才从下一个未完成的 Phase 继续
   - **禁止：** 凭印象重走已完成的 Phase。wiki 文档是进度真相，不是 session 记忆。

1. **文档先于代码** — Phase 3（设计文档）未完成 + 大佬未确认，禁止写任何代码
2. **分阶段审批** — 每个 Phase 必须有大佬确认输出才能进入下一 Phase
3. **独立测试** — 代码任务必须有 tester review 卡，禁止自己测自己验收
4. **角色分离** — 灵犀是协调者，不直接改代码。后端→coder，前端逻辑→coder，UI/样式→artist，测试→tester。**效率不是跳过角色分离的理由**。
5. **流程合规自检** — Phase 4 自检必须包含流程合规检查
6. **文档写入路径验证** — 文档必须写入 `raw/projects/<项目名>/changes/<变更名>/` 目录，写入后必须 `ls` 验证
7. **反馈走流程** — 大佬测试反馈问题后，走 Phase 8 反馈循环，禁止"顺手修了"
8. **Checkpoint 机制** — 每个 Task 执行后必须输出 checkpoint（产出物验证），未通过验证不得进入下一 Task
9. **安全扫描** — Phase 6 每个 Task 的 review 必须包含安全扫描（硬编码密钥、SQL 注入、shell 注入等）。agent 提交前必须完成 Pre-Commit 安全自检（见 phase6-execution.md §Pre-Commit）
10. **Auto-Fix 上限** — review 发现问题后派 fix agent 修复并重新 review，最多 2 轮后 escalate 给大佬
11. **方案注入（2026-05-24 教训）** — Phase 6 建卡时，task body 必须注入三样东西：(1) proposal.md 的相关章节（代码/配置/路由定义，不能只写一句话描述）；(2) constitution.md 的技术约束（文件结构、禁止事项）；(3) 明确的"不在范围内"声明。缺少任一 = 流程违规。**反例：** 只写"实现 Obsidian 集成"→ coder 自行发挥 → 偏离方案。**正例：** 注入 proposal 中的完整代码示例 + 文件路径 + 禁止事项 → coder 只能照做。
12. **代码交叉验证（2026-05-25 Matt Pocock 借鉴）** — Phase 1 中大佬描述现有系统行为时，必须检查代码验证描述是否吻合。发现矛盾时以代码为准，向大佬确认："代码显示的是 X，但你说的是 Y — 哪个对？"不盲目接受口头描述。UI 项目同理：描述页面行为时先看实际渲染。
13. **Context File Pattern（2026-05-26 验证通过）** — 复杂任务（body > 500 字）采用混合模式：body 放摘要（500 字），详细 spec 写到 `raw/projects/{project}/changes/{变更名}/bugfix-spec.md`，body 中注明**绝对路径**让 worker 读取。worker SOUL.md 已注入规则。**实测：** Round 6 首次使用，coder/tester 都正确读取 spec 文件，token 节省 90%。**关键：** 路径必须是绝对路径（`/mnt/unraid_data/Obsidian/wiki/...`），相对路径可能找不到。
14. **5 步验证函数（2026-05-29 Superpowers 移植）** — 声称任务完成/修复成功/测试通过前，必须走完 5 步：(1) IDENTIFY 验证命令 (2) RUN 新鲜执行 (3) READ 完整输出+exit code (4) VERIFY 逐条对照验收标准 (5) REPORT 带证据汇报。跳过任何一步 = 违规。"CodeWhale 说改好了" ≠ 验证过，"代码看起来对" ≠ 运行中的系统。详见 `references/methodology/verification-and-ratchet.md` §一、§二。

### ⛔ Phase 8 结束前必须跑机械自检

每轮 Phase 8 修复完成后、向大佬汇报前，必须执行 `references/pitfalls/phase8-pre-close-checklist.md` 中的 shell 检查脚本。缺少 conversation.md / diagnosis.md / fixes.md / test-report.md 任一文件 = 不允许汇报完成。3 次违规证明纯靠自觉无效。

**违反以上任何一条 = 流程违规，必须记 ERRORS.md。**

## 何时触发

以下任一条件满足时主动触发：
1. 大佬发送 `/clsh-project` 或 `/project`
2. 大佬说"我要做一个 XXX"、"开发一个 XXX 系统"、"实现 XXX 功能"
3. 大佬提出的需求明显是多步骤项目
4. 大佬说"按 Kiro 流程走"、"先做需求分析"
5. 大佬说"review 项目"、"检查实现效果"、"对比设计方案" → **Review Mode**

**不触发的情况：**
- 简单查询、单步操作、修复 bug（用 systematic-debugging）
- 已有明确实现方案的小改动
- 大佬明确说"简单做一下"或"不用走完整流程"
- 代码质量审查（PR review、linting、重复检查）— 直接用 execute_code 分析 + 出报告
- **注意：** 功能规格合规审查（对比设计方案检查实现）→ 走 Review Mode

## Review Mode（规格合规审查）

当大佬要求 review 已有项目的代码和实现效果时，不走完整 Phase 1-8，而是执行规格合规审查。

### 触发条件
- "review 项目代码和实现效果"
- "检查一下 XX 项目做得怎么样"
- "对比设计方案看看实现"

### 流程（7 步）
1. **读取项目文档** — proposal.md、constitution.md、tasks.md、test-log.md、round*-feedback.md + overview.md
2. **读取所有代码** — 逐文件阅读，不跳过（代码重复/路径不一致只在全量阅读时发现）
3. **验证运行状态** — pm2 list、依赖检查、.env 配置、API 实际调用
4. **产出合规矩阵** — 功能 × 实现状态（✅完整/⚠️部分/❌未实现）
5. **Constitution 合规检查** — 逐条对比约束 vs 实际代码
6. **代码质量分析** — 按严重性分级（P1 数据一致性/P2 代码重复/P3 架构/P4 死代码/P5 性能/P6 风格）
7. **汇报** — 结构化报告，优先级排序

### 输出格式
- 功能合规矩阵（表格：功能 | 后端 | 前端 | 状态）
- Constitution 合规检查（表格：约束 | 是否遵守 | 备注）
- 代码质量问题（P1-P6 分级）
- 未实现功能清单 + 复杂度评估
- 建议下一步

### 红线
- Review Mode 产出报告，不直接修复 — 修复走 Phase 8 反馈循环
- 大佬说"顺便修了" → 提醒走角色分离流程
- 不创建 kanban 卡，不派发任务

📋 **详细流程:** [references/workflow/phase-review.md](references/workflow/phase-review.md)

---

## 流程总览

```
大佬: "我要做一个 XXX 系统"
           ↓
Phase 1: 需求澄清（调研前置 + 一次一个问题，多选优先；UI项目可选 Visual Companion）→ conversation.md
           ↓ [大佬确认需求]
Phase 2: 提出 2-3 个方案 + 推荐理由 → 大佬选择
           ↓ [大佬确认方案]
Phase 2.5: Technical Spike（可选，技术不确定时）→ 快速原型 → 裁决
           ↓ [VALIDATED]
Phase 3: 写设计文档 → proposal.md + constitution.md
           ↓ [大佬确认设计]
Phase 4: 设计文档自检（含流程合规检查） + 大佬确认
           ↓ [大佬确认进入执行]
Phase 5: 写实现计划 → tasks.md（bite-sized + TDD + No Placeholders + Type Consistency）
           ↓
Phase 6: Ralph Loop 分发执行（coder/artist/tester + Security Scan + Auto-Fix）
           ↓ [tester 通过]
Phase 7: 完成归档 + 流程复盘
           ↓
Phase 8: 反馈循环（大佬测试后，diagnose 6 阶段）→ 回到 Phase 1 或 Phase 6
### 🚀 Session Launch Guidance

| 完成 Phase | 下一步 | 建议 |
|-----------|--------|------|
| Phase 1-5 | `/cp 继续 <项目名>` | 当前 session 继续 |
| Phase 6 | `/cp 继续 <项目名>` | 3+ Task 建议新 session |
| Phase 7 | 等待大佬测试反馈 | — |
| Phase 8 | `/cp 继续 <项目名>` | 每轮修复建议新 session |
| Phase 8 | `/clsh-project 继续 <项目名>` | 每轮修复建议新 session（避免 context 溢出） |

**为什么必须做：** 大佬可能在不同 session 间切换。没有衔接提示，大佬需要自己记住"上次做到哪了"。这是机械输出，不消耗额外判断力。

### 🅿️ 项目暂存（Project Parking）

大佬说"先存 wiki，不做"/"记录一下方案，下次继续"时：
1. 写 `raw/projects/<项目名>/overview.md`（状态 `planning`）
2. 写 `raw/projects/<项目名>/proposal.md`（技术方案）
3. 向大佬确认已存档
4. **不进入 Phase 2+**，等大佬下次确认后再继续

这是合法的项目状态 — 不是每个需求都需要立即执行。

---

## Phase 0+1: 需求准备与澄清

Phase 0 每次项目开始前内化历史教训；Phase 1 一次一个问题、多选优先、先理解目的再讨论细节。**新增：** 代码交叉验证（大佬描述现有行为时必须查代码）+ CONTEXT.md 领域术语表（自然积累项目术语）。UI 项目可选 Visual Companion。含调研前置、提问模板、需求文档格式。

📋 **详细流程:** [references/workflow/phase0-1-requirements.md](references/workflow/phase0-1-requirements.md)
📋 **术语模板:** [references/templates/context-template.md](references/templates/context-template.md)

---

## Phase 2+2.5: 方案设计与技术验证

Phase 2 提出 2-3 个方案 + 推荐理由，用对比表格呈现。Phase 2.5 扩展为两种模式：**技术 Spike**（验证技术可行性）+ **设计 Prototype**（可运行原型探索设计方向，分逻辑原型和 UI 原型两个分支）。Prototype 规则：一条命令运行、无持久化、做完就删。

📋 **详细流程:** [references/workflow/phase2-design.md](references/workflow/phase2-design.md)
📋 **原型借鉴:** [references/methodology/matt-pocock-patterns.md](references/methodology/matt-pocock-patterns.md) §5

---

## Phase 3+4: 设计文档与自检

Phase 3 写 proposal.md + constitution.md（含轻量版和完整版模板）。**新增：** 满足 3 条件（难逆转+令人意外+有取舍）的架构决策记录为 ADR。UI 项目**必做设计发散**（2-3 个 HTML mockup 变体，**交互原型优先**通过 nginx :8088 发链接，截图备选）。Phase 4 流程合规检查 + 文档质量自检 + **Module Depth 评估**（删除测试+接口深度）+ 大佬 Review Gate + 自动路径验证。

📋 **详细流程:** [references/workflow/phase3-spec.md](references/workflow/phase3-spec.md)
📋 **ADR 模板:** [references/templates/adr-template.md](references/templates/adr-template.md)

---

## Phase 5: 实现计划

tasks.md 单文件 ≤3000 字，超出必须拆分。每个任务 = 一个 kanban 卡，粒度 2-5 分钟。**新增：Vertical Slice 规范** — 每个 Task 是端到端薄切片（非水平层），完成后可独立验证。分 HITL（需人工）和 AFK（可自动）两类，优先 AFK。No Placeholders + Type Consistency 必做。含文件依赖图、垂直切片策略、Self-Review 四项检查。

📋 **详细流程:** [references/workflow/phase5-tasks.md](references/workflow/phase5-tasks.md)
📋 **Vertical Slice 借鉴:** [references/methodology/matt-pocock-patterns.md](references/methodology/matt-pocock-patterns.md) §4

---

## Phase 6: Ralph Loop 分发执行

角色分配（coder/artist/tester）+ Ralph Loop 状态机 + Blocked 状态处理 + 任务派发 + Wave 并行 + 三层超时机制 + 执行红线。**新增：** UI 项目必做 Browser QA（浏览器自动化测试）、Pre-Commit 安全自检（代码提交前检查）。

### Kanban 派发执行器（Way C — 给路径和目标，不做代码推理）

**coder/artist 角色通过 kanban 派发，tester 保持 kanban review 卡。**

**核心原则（Way C 铁律）：** 灵犀不做代码推理，只指定路径和问题。worker 自己读代码、推理根因、修复。

**kanban task body 精简原则：** 传完整文件浪费 token。task body 只传：
1. 问题现象（1-2 句话）
2. 文件路径 + 关键行号
3. API 参数格式（如果涉及接口不匹配）

让 worker 自己读取相关文件，省 ~90% token。

```bash
# Phase 6 coder 任务派发（Way C — 精简 body）
hermes kanban create "[项目名] 实现: <任务名>" \
  --assignee coder \
  --body "## 问题
重命名笔记时不自动带 .md 后缀

## 相关文件
- /opt/Workspace/src/projects/obsidian/public/ObsidianView.mjs（第 418-455 行 renameItem 函数）
- /opt/Workspace/src/projects/obsidian/plugin.mjs（第 118-125 行 PUT /api/obsidian/rename）

## 验收标准
1. 后端 API 格式：PUT /api/obsidian/rename，期望 { oldPath: string, newPath: string }
2. node -c 语法通过

## 不在范围内
- 不修改其他 API 端点" \
  --json
```

**灵犀的职责（协调者）：**
1. 接收大佬反馈
2. 指定文件路径（wiki 项目文档、代码文件）
3. 描述问题现象（不做代码层面的推理）
4. 验证结果（非代码层面）

**worker 的职责（推理 + 执行）：**
1. 读取 wiki 项目文档（bugfix spec、constitution）
2. 读取相关代码
3. 自己分析根因
4. 自己修复代码

**角色分工：**
| 角色 | 执行器 | 理由 |
|------|--------|------|
| coder | kanban worker | 持久化、依赖链、状态跟踪 |
| artist | kanban worker | 同上 |
| tester | kanban review 卡 | 浏览器工具、独立性 |

📋 **详细流程:** [references/workflow/phase6-execution.md](references/workflow/phase6-execution.md)

---

## Phase 7: 完成归档与流程复盘

wiki 归档检查清单（必做）+ 归档 9 步 + 流程合规复盘 7 项 + 蒸馏评估。**新增：** 生成 handoff.md（跨 session 续接文档，引用已有文档不重复，建议下次加载的 skills）。

📋 **详细流程:** [references/workflow/phase7-archive.md](references/workflow/phase7-archive.md)
📋 **Handoff 借鉴:** [references/methodology/matt-pocock-patterns.md](references/methodology/matt-pocock-patterns.md) §7

---

## Phase 8: 反馈循环

执行规范（角色分离 + tester 浏览器验证 + 每轮归档）+ 上下文溢出防护（每轮 ≤3-4 bug）+ Diagnose 6 阶段 + Bugfix Spec + 路径 A/B/C + 反馈循环红线。**新增：诊断引擎模式** — 灵犀收到用户反馈后先自己读代码+分析根因，再写精确 bugfix spec 派 coder（spec 必须包含"根因是什么→改哪行→改成什么"）。coder 是执行器不是诊断器。详见 `references/methodology/soul-md-behavioral-enforcement.md`。**tester review spec 必须明确验证方式：** UI 项目必须写"用浏览器访问页面截图验证"，不能只写"读代码+curl"。缺少验证方式描述 = reviewer 可能只读代码就判 PASS（pitfall #34）。

### Phase 8 Kanban 派发（Way C — 给路径和目标）

**修复任务通过 kanban 派发给 coder/artist，验证任务通过 kanban review 卡派给 tester。**

**核心原则（Way C 铁律）：** 灵犀不做代码推理，只指定路径和问题。worker 自己读代码、分析根因、修复。

```bash
# Phase 8 bugfix 执行（Way C）
hermes kanban create "[项目名] Round<N>: <问题简述>" \
  --assignee coder \
  --body "## 问题描述
[大佬反馈的现象，不做代码层面的推理]

## 相关文件
- 代码位置：/opt/Workspace/src/projects/<项目>/
- wiki 项目文档：/mnt/unraid_data/Obsidian/raw/projects/<项目>/changes/<变更名>/
- bugfix spec：/mnt/unraid_data/Obsidian/raw/projects/<项目>/changes/<变更名>/bugfix-spec.md
- 项目约束：/mnt/unraid_data/Obsidian/raw/projects/<项目>/source-of-truth/constitution.md

## 验收标准
1. [具体验证命令/条件]

## 不在范围内
- [禁止修改的文件/功能]" \
  --json
```

**Bugfix Spec 模板（参考 OpenSpec Delta Spec）：**
```markdown
## 问题描述
[大佬反馈的现象，不做代码层面的推理]

## 相关文件
- 代码位置：...
- API 定义：...
- 前端组件：...

## 验证方式
[如何验证修复成功]
```

📋 **详细流程:** [references/workflow/phase8-feedback.md](references/workflow/phase8-feedback.md)

---

## 流程门禁

| 门禁 | 检查内容 | 未通过 → |
|------|---------|---------|
| Phase 3→4 | proposal.md 已写入 + `ls` 验证 | 不允许写代码 |
| Phase 4→5 | 大佬明确回复"确认" | 不允许写 tasks.md |
| Phase 5→6 | tasks.md 已写入 + 每 Task 有验收标准 | 不允许创建 kanban 卡 |
| Phase 6 执行 | 代码任务必须有 tester 卡 | 不允许标记完成 |
| Phase 6 安全 | 每个 Task 必须通过 Security Scan | 不允许进入 Quality Review |
| Phase 6 修复 | Auto-Fix 最多 2 轮 | 2 轮后必须 escalate 给大佬 |
| Phase 6 测试 | 修复后必须 tester 验证 | 不允许汇报完成 |
| Phase 6 Browser QA | UI 项目 tester 必须浏览器验证 | 不允许汇报完成 |

## 快捷方式

### ⚠️ 核心规则（精选，完整版见 `references/pitfalls/common.md`）

**角色分离（铁律，不可违反）：**
1. 禁止灵犀直接写代码 — 即使"很快能做完"也必须派 kanban worker
2. 禁止 Phase 8 "顺手修了" — 大佬反馈问题必须走完整反馈循环
3. 禁止跳过 tester 卡 — 每个 Task 必须有独立 tester review
4. Phase 8 必须用 kanban 派发 — delegate_task 不是 kanban 的替代品
5. 禁止只测脚本就说"修好了" — Python 脚本直接运行 OK ≠ API 端点 OK。必须通过实际 API（curl/fetch）验证完整链路
6. 禁止不测试就汇报"已修复" — 每次修完必须跑端到端验证，拿到实际输出再汇报

**Way C 铁律（kanban task body 规范）：**
38. 灵犀只给目标+路径+约束，不做代码推理。worker 自己读代码、推理根因、修复
39. ❌ 不该给：具体 CSS 代码、详细实现步骤、行号级指令
40. ✅ 该给："大佬说按钮丑，重做 UI。参考 style.css。浅色毛玻璃主题。"
49. worker 修复后必须走 tester 验证 — 修复速度 ≠ 修复质量

**Phase 8 诊断铁律：**
60. 大佬反馈 bug → 灵犀只记录现象+文件路径 → 创建 kanban 卡让 worker 分析根因
69. 禁止灵犀自己分析 5 个可能原因再告诉 worker — 这是 worker 的活

> 78+ 条完整 pitfalls（含历史案例、验证方法、触发条件）→ `references/pitfalls/common.md`

### ✅ Verification Checklist

📋 **完整验证清单（流程合规 + 验证合规）:** [references/templates/verification-checklist.md](references/templates/verification-checklist.md)


## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v5.20.0 | 2026-06-04 | **Review Mode**：新增规格合规审查模式 — 对比设计方案检查实现，产出功能合规矩阵 + Constitution 合规 + 代码质量分级（P1-P6）。参考 `references/workflow/phase-review.md`。 |
| v5.19.0 | 2026-06-03 | **Phase 8 机械自检**：新增 `references/pitfalls/phase8-pre-close-checklist.md` — 每轮 Phase 8 结束前必须跑 shell 检查脚本，确认 conversation/diagnosis/fixes/test-report 4 个文件存在。3 次违规后确立的机械强制机制。 |
| v5.18.0 | 2026-06-03 | **Tester 卡优化**：Phase 6 新增 tester 优化方案（拆分 tester 卡 / 灵犀机械预检 / Lite Checklist）。解决迭代预算耗尽问题。 |
| v5.17.0 | 2026-06-03 | **派发后追踪协议**：Phase 6 新增 Post-Dispatch Tracking（cron 轮询/session 内等待/notify_on_complete），禁止 fire-and-forget。Pitfall #77。 |
| v5.16.0 | 2026-06-03 | **SKILL.md 整合瘦身**：Pitfalls 迁到 references/pitfalls/common.md（SKILL.md 只留核心规则 19 行）；版本历史只留最近 3 版；自进化机制迁到 references/methodology/；验证清单迁到 references/templates/。四框架调研（gstack/Spec Kit/OpenSpec/Ralph Loop）写入 references/methodology/four-framework-analysis.md。 |
| v5.13.0 | 2026-06-02 | **LLM 能力无关性原则**：流程控制不依赖 LLM 判断力。Phase 6 新增 Review Checklist + Spec Delta。Session Launch Guidance。 |

> 完整版本历史 → [references/templates/version-history.md](references/templates/version-history.md)


## 参考文件

### 📐 方法论
- `references/methodology/kiro-superpowers-analysis.md` — Kiro + Superpowers + Phoenix 工作流分析
- `references/methodology/ralph-loop-analysis.md` — Ralph Loop：原理 + Phase 6 映射
- `references/methodology/superpowers-architecture-analysis.md` — Superpowers 架构拆解
- `references/methodology/four-framework-analysis.md` — **四框架整合分析**（gstack/Spec Kit/OpenSpec/Ralph Loop）
- `references/methodology/optimization-deep-dive.md` — **优化深度分析**（5 模式的实现方案、依赖链、投入产出比）
- `references/methodology/matt-pocock-patterns.md` — Matt Pocock Skills 借鉴（CONTEXT.md、ADR、Vertical Slice 等 7 模式）
- `references/methodology/soul-md-behavioral-enforcement.md` — SOUL.md 行为约束（Karpathy + Superpowers）
- `references/methodology/verification-and-ratchet.md` — 验证框架与棘轮机制
- `references/methodology/self-evolution-mechanism.md` — **自进化机制**（Darwin 9 维 rubric、ECC 执行验证）
- `references/methodology/external-framework-evaluation.md` — 外部框架评估方法论

### 📋 模板
- `references/templates/constitution-template.md` — Constitution 模板
- `references/templates/verification-checklist.md` — **验证清单完整版**（流程合规 + 验证合规）
- `references/templates/version-history.md` — **完整版本历史**
- `references/templates/context-template.md` — CONTEXT.md 领域术语表模板
- `references/templates/adr-template.md` — ADR 架构决策记录模板

### ⚠️ 教训
- `references/pitfalls/common.md` — **Common Pitfalls 完整版**（78+ 条，含历史案例 + 验证方法 + 触发条件）
- `references/pitfalls/violation-case-2026-05-15.md` — 跳步 + 自测案例
- `references/pitfalls/violation-case-2026-05-18.md` — Kanban 状态同步 + 角色分离案例

### 🔄 流程详情
- `references/workflow/phase0-1-requirements.md` — Phase 0+1: 需求准备与澄清
- `references/workflow/phase2-design.md` — Phase 2+2.5: 方案设计与技术验证
- `references/workflow/phase3-spec.md` — Phase 3+4: 设计文档与自检
- `references/workflow/phase5-tasks.md` — Phase 5: 实现计划
- `references/workflow/phase6-execution.md` — Phase 6: Ralph Loop 分发执行
- `references/workflow/phase7-archive.md` — Phase 7: 完成归档与流程复盘
- `references/workflow/phase8-feedback.md` — Phase 8: 反馈循环

### 🔌 集成
- `references/integration/hermes-pitfalls.md` — Hermes 工具链陷阱
- `references/workspace-sub-module-pattern.md` — Workspace 子模块开发模式
