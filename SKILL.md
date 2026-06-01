---
name: clsh-project
description: "需求驱动的项目开发工作流 — 从需求澄清到设计文档到实现计划到执行。灵感来自 Kiro 的 Spec-Driven Development、Superpowers 的 Brainstorming 方法论、Phoenix 的状态机执行模式。"
version: 5.11.0
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
      # 模板（clsh-project 流程模板，保留本地）
      - references/templates/constitution-template.md
      - references/templates/archive-workflow.md
      - references/templates/cloud-server-wireguard.md
      - references/templates/phase7-archive-checklist.md
      - references/templates/phase8-checkpoint-template.md
      - references/templates/context-template.md
      - references/templates/adr-template.md
      # 集成（clsh-project 工具链，保留本地）
      - references/integration/kanban-tasks-bridge.md
      - references/integration/hermes-slash-command-mechanism.md
      - references/integration/hermes-plugin-zero-token.md
      - references/integration/hermes-plugin-hooks-reference.md
      - references/integration/halo-auth.md
      - references/integration/halo-cli-auth.md
      - references/integration/reference-migration-pattern.md
      - references/integration/hermes-pitfalls.md
      - references/integration/codewhale-acp-integration.md
      - references/workspace-sub-module-pattern.md
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
- 文档管理（wiki/projects/ 结构）

### 不管什么
- 具体技术实现细节 → `wiki/projects/<项目>/references/pitfalls/`
- Hermes 工具链使用细节 → `references/integration/hermes-pitfalls.md`
- 调试方法论 → `diagnose` skill
- 代码质量规则 → `code-principles` skill

### 膨胀阈值
- SKILL.md: ≤ 900 行
- Common Pitfalls: ≤ 25 条（超出迁移）
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


## ⛔ 流程铁律（不可违反，违反 = 流程违规）

以下规则优先级高于一切效率考量：

0. **先查进度再行动** — 收到"继续项目"指令时，必须按以下顺序确认进度：
   - **第一步：** `ls wiki/projects/<项目名>/` 检查项目容器是否存在
   - **第二步：** 读 `overview.md` 确认当前 Phase 和状态
   - **第三步：** 读 `changes/` 下的文档确认已完成的工作
   - **第四步：** 只有确认进度后，才从下一个未完成的 Phase 继续
   - **禁止：** 凭印象重走已完成的 Phase。wiki 文档是进度真相，不是 session 记忆。

1. **文档先于代码** — Phase 3（设计文档）未完成 + 大佬未确认，禁止写任何代码
2. **分阶段审批** — 每个 Phase 必须有大佬确认输出才能进入下一 Phase
3. **独立测试** — 代码任务必须有 tester review 卡，禁止自己测自己验收
4. **角色分离** — 灵犀是协调者，不直接改代码。后端→coder，前端逻辑→coder，UI/样式→artist，测试→tester。**效率不是跳过角色分离的理由**。
5. **流程合规自检** — Phase 4 自检必须包含流程合规检查
6. **文档写入路径验证** — 文档必须写入 `wiki/projects/<项目名>/changes/<变更名>/` 目录，写入后必须 `ls` 验证
7. **反馈走流程** — 大佬测试反馈问题后，走 Phase 8 反馈循环，禁止"顺手修了"
8. **Checkpoint 机制** — 每个 Task 执行后必须输出 checkpoint（产出物验证），未通过验证不得进入下一 Task
9. **安全扫描** — Phase 6 每个 Task 的 review 必须包含安全扫描（硬编码密钥、SQL 注入、shell 注入等）。agent 提交前必须完成 Pre-Commit 安全自检（见 phase6-execution.md §Pre-Commit）
10. **Auto-Fix 上限** — review 发现问题后派 fix agent 修复并重新 review，最多 2 轮后 escalate 给大佬
11. **方案注入（2026-05-24 教训）** — Phase 6 建卡时，task body 必须注入三样东西：(1) proposal.md 的相关章节（代码/配置/路由定义，不能只写一句话描述）；(2) constitution.md 的技术约束（文件结构、禁止事项）；(3) 明确的"不在范围内"声明。缺少任一 = 流程违规。**反例：** 只写"实现 Obsidian 集成"→ coder 自行发挥 → 偏离方案。**正例：** 注入 proposal 中的完整代码示例 + 文件路径 + 禁止事项 → coder 只能照做。
12. **代码交叉验证（2026-05-25 Matt Pocock 借鉴）** — Phase 1 中大佬描述现有系统行为时，必须检查代码验证描述是否吻合。发现矛盾时以代码为准，向大佬确认："代码显示的是 X，但你说的是 Y — 哪个对？"不盲目接受口头描述。UI 项目同理：描述页面行为时先看实际渲染。
13. **Context File Pattern（2026-05-26 验证通过）** — 复杂任务（body > 500 字）采用混合模式：body 放摘要（500 字），详细 spec 写到 `wiki/projects/{project}/changes/{变更名}/bugfix-spec.md`，body 中注明**绝对路径**让 worker 读取。worker SOUL.md 已注入规则。**实测：** Round 6 首次使用，coder/tester 都正确读取 spec 文件，token 节省 90%。**关键：** 路径必须是绝对路径（`/mnt/unraid_data/Obsidian/wiki/...`），相对路径可能找不到。
14. **5 步验证函数（2026-05-29 Superpowers 移植）** — 声称任务完成/修复成功/测试通过前，必须走完 5 步：(1) IDENTIFY 验证命令 (2) RUN 新鲜执行 (3) READ 完整输出+exit code (4) VERIFY 逐条对照验收标准 (5) REPORT 带证据汇报。跳过任何一步 = 违规。"CodeWhale 说改好了" ≠ 验证过，"代码看起来对" ≠ 运行中的系统。详见 `references/methodology/verification-and-ratchet.md` §一、§二。

**违反以上任何一条 = 流程违规，必须记 ERRORS.md。**

## 何时触发

以下任一条件满足时主动触发：
1. 大佬发送 `/clsh-project` 或 `/project`
2. 大佬说"我要做一个 XXX"、"开发一个 XXX 系统"、"实现 XXX 功能"
3. 大佬提出的需求明显是多步骤项目
4. 大佬说"按 Kiro 流程走"、"先做需求分析"

**不触发的情况：**
- 简单查询、单步操作、修复 bug（用 systematic-debugging）
- 已有明确实现方案的小改动
- 大佬明确说"简单做一下"或"不用走完整流程"

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
```

**⛔ 关键：每个 ↓ 处必须有明确的大佬确认，才能进入下一阶段。**

### 🅿️ 项目暂存（Project Parking）

大佬说"先存 wiki，不做"/"记录一下方案，下次继续"时：
1. 写 `wiki/projects/<项目名>/overview.md`（状态 `planning`）
2. 写 `wiki/projects/<项目名>/proposal.md`（技术方案）
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

### CodeWhale ACP 执行器（2026-05-27 v2 — 方式 C）

**coder/artist 角色使用 CodeWhale ACP 执行，tester 保持 Hermes subagent（独立性 + 浏览器工具）。**

**核心原则：灵犀不做代码推理，只指定路径和问题。CodeWhale 自己读代码、推理根因、修复。**

**精简 context 原则（2026-05-27 确立）：** ACP 模式无状态（每次新 session），传完整文件浪费 token。精简 context 只传：
1. 问题现象（1-2 句话）
2. 文件路径 + 关键行号
3. API 参数格式（如果涉及接口不匹配）

让 CodeWhale 自己读取，省 ~90% token。

```python
# Phase 6 coder 任务派发（方式 C — 精简 context）
delegate_task(
    goal="修复 XXX 功能",
    acp_command="/usr/local/bin/codewhale",
    toolsets=["file", "terminal"],
    context="""
问题：重命名笔记时不自动带 .md 后缀

相关文件：
- /opt/Workspace/src/projects/obsidian/public/ObsidianView.mjs（第 418-455 行 renameItem 函数）
- /opt/Workspace/src/projects/obsidian/plugin.mjs（第 118-125 行 PUT /api/obsidian/rename）

后端 API 格式：PUT /api/obsidian/rename，期望 { oldPath: string, newPath: string }
"""
)
```

**灵犀的职责（协调者）：**
1. 接收大佬反馈
2. 指定文件路径（wiki 项目文档、代码文件）
3. 描述问题现象（不做代码层面的推理）
4. 验证结果（非代码层面）

**CodeWhale 的职责（推理 + 执行）：**
1. 读取 wiki 项目文档（bugfix spec、constitution）
2. 读取相关代码
3. 自己分析根因
4. 自己修复代码

**角色分工：**
| 角色 | 执行器 | 理由 |
|------|--------|------|
| coder | CodeWhale ACP | 低成本、1M 上下文、自己推理 |
| artist | CodeWhale ACP | 同上 |
| tester | Hermes subagent | 浏览器工具、独立性 |

**验证结果（Round 7-9）：**
- Round 7（方式 B）：灵犀推理根因 → 3 个 bug 一次修好 ✅
- Round 8（方式 A）：CodeWhale 自推理 → 重命名参数错误 ❌
- Round 9（方式 B）：灵犀推理根因 → 4 个 bug 一次修好 ✅
- **结论：方式 C（灵犀指定路径 + CodeWhale 自己读代码推理）是最优方案**

📋 **详细流程:** [references/workflow/phase6-execution.md](references/workflow/phase6-execution.md)

---

## Phase 7: 完成归档与流程复盘

wiki 归档检查清单（必做）+ 归档 9 步 + 流程合规复盘 7 项 + 蒸馏评估。**新增：** 生成 handoff.md（跨 session 续接文档，引用已有文档不重复，建议下次加载的 skills）。

📋 **详细流程:** [references/workflow/phase7-archive.md](references/workflow/phase7-archive.md)
📋 **Handoff 借鉴:** [references/methodology/matt-pocock-patterns.md](references/methodology/matt-pocock-patterns.md) §7

---

## Phase 8: 反馈循环

执行规范（角色分离 + tester 浏览器验证 + 每轮归档）+ 上下文溢出防护（每轮 ≤3-4 bug）+ Diagnose 6 阶段 + Bugfix Spec + 路径 A/B/C + 反馈循环红线。**新增：诊断引擎模式** — 灵犀收到用户反馈后先自己读代码+分析根因，再写精确 bugfix spec 派 coder（spec 必须包含"根因是什么→改哪行→改成什么"）。coder 是执行器不是诊断器。详见 `references/methodology/soul-md-behavioral-enforcement.md`。**tester review spec 必须明确验证方式：** UI 项目必须写"用浏览器访问页面截图验证"，不能只写"读代码+curl"。缺少验证方式描述 = reviewer 可能只读代码就判 PASS（pitfall #34）。

### Phase 8 CodeWhale 集成（2026-05-27 v2 — 方式 C）

**修复任务使用 CodeWhale ACP 执行，验证任务使用 Hermes subagent。**

**核心原则：灵犀不做代码推理，只指定路径和问题。CodeWhale 自己读 wiki 文档和代码，自己推理根因并修复。**

```python
# Phase 8 bugfix 执行（方式 C）
delegate_task(
    goal="修复以下问题：[大佬反馈的现象]",
    acp_command="/usr/local/bin/codewhale",
    toolsets=["file", "terminal"],
    context="""
相关文件路径：
- 代码位置：/opt/Workspace/src/projects/<项目>/
- wiki 项目文档：/mnt/unraid_data/Obsidian/wiki/projects/<项目>/changes/<变更名>/
- bugfix spec：/mnt/unraid_data/Obsidian/wiki/projects/<项目>/changes/<变更名>/bugfix-spec.md
- 项目约束：/mnt/unraid_data/Obsidian/wiki/projects/<项目>/source-of-truth/constitution.md

请先读取 bugfix spec 和相关代码，自己分析根因并修复。
"""
)
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

如果大佬说"简单做一下"，可以跳过 Phase 2（方案对比）。但 Phase 1 和 Phase 3 不能跳过。

Phase 2.5 Spike 是可选的，仅在技术不确定时触发。

## Common Pitfalls

> 78 条教训已去重迁移。流程纪律保留在下方，技术陷阱→`wiki/projects/<项目>/references/pitfalls/`，工具链→`references/integration/hermes-pitfalls.md`。

### 角色分离（铁律，置信度 0.9）
1. **禁止灵犀直接写代码** — 即使"很快能做完"也必须派 agent | 验证：检查是否有灵犀的 write_file/patch 操作 | 触发：任何代码修改任务
2. **禁止 Phase 8 "顺手修了"** — 大佬反馈问题必须走完整反馈循环 | 验证：检查 Phase 8 是否有 conversation.md + diagnosis.md | 触发：大佬说"这个有问题"/"帮我改"
3. **角色分离违规** — worker 卡住时不能自己动手，创建 fix 卡或 escalate | 验证：检查灵犀是否在 worker blocked 后直接写代码 | 触发：worker kanban_block
4. **Phase 8 必须走角色分离** — 小修复用 kanban（非 delegate_task），大修复更要用 kanban | 验证：检查 Phase 8 是否用了 delegate_task 替代 kanban | 触发：Phase 8 修复任务
5. **delegate_task 不是 kanban 的替代品（2026-05-24 教训）。** 用户要求走 kanban 时，不得用 `delegate_task` 替代。**判断规则：** clsh-project 流程或用户明确要求 kanban → 必须用 kanban。只有纯推理子任务（代码审查、调试分析、对比）才用 delegate_task。 | 验证：检查用户是否明确要求 kanban | 触发：用户说"用 kanban"/"走流程"

### 流程完整性（置信度 0.5-0.7）
6. **方向变化不回 Phase 1** — 核心定位变化必须回 Phase 1，不能回 Phase 3
7. **跳过 Phase 2.5 Spike** — 有技术不确定性的方案必须先验证
8. **Phase 5 缺少 Self-Review** — tasks.md 写完后必须 4 项自检
9. **Phase 6 不做 Spec-Code 同步** — 每个 Task 完成后更新 proposal.md
10. **Phase 7 归档不完整** — 必须检查 overview.md + completion-summary + retrospective + Phase 8 归档
55. **UI 设计跳过 Open Design 知识包加载（2026-05-29 教训）** — Phase 3 设计发散必须先读取 `/opt/open-design/design-systems/<name>/tokens.css` + `DESIGN.md` + `craft/*.md`，再渲染变体。直接手写 HTML = 跳步 = 效果差 = 返工。详见 `references/pitfalls/ui-design-open-design-enforcement.md` | 验证：检查 HTML 模板是否引用了 tokens.css 的变量 | 触发：任何 UI 项目 Phase 3

### 质量保障（置信度 0.5-0.9）
11. **agent 自判完成（置信度 0.9）** — 必须通过 CHECKPOINT 客观验证 | 验证：检查 checkpoint 是否有客观证据（exit code/截图/ls 输出）| 触发：agent 说"已完成"/"done"/"fixed"
12. **Auto-Fix 无限循环** — 2 轮后必须 escalate 给大佬
13. **Placeholder 污染 tasks.md** — TBD/TODO/similar to N = 计划缺陷
14. **写入文件后不验证路径** — write_file 后必须 `ls` 确认
15. **UI 项目跳过 Browser QA（置信度 0.9）** — tester 必须用浏览器截图验证 | 验证：检查 tester 是否有浏览器工具调用记录 | 触发：任何有 UI 的项目
16. **Pre-Commit 自检缺失** — agent context 必须包含安全自检清单，不依赖 agent 自觉
17. **设计发散跳过** — UI 项目且无明确设计参考时，Phase 3 应触发设计发散，不能直接画页面
18. **飞书发送 HTML 文件路径** — 飞书无法打开 HTML 文件。必须用 chromium-browser 截图后发送 PNG 图片（MEDIA: 前缀）
19. **chromium 截图路径 /tmp** — snap 版 chromium 受 AppArmor 限制，无法写入 /tmp。截图路径用 /root/mockups/ 等非受限目录
20. **AGENTS.md 参考其他项目** — AGENTS.md 应基于本项目自身架构（architecture.md），不能照搬其他项目的文档结构

### 执行纪律
21. **超时后提交半成品** — 子 agent 超时后 git stash/revert
22. **Phase 8 上下文溢出** — 每轮最多修 3-4 个 bug，用 execute_code 批量读代码
23. **Bugfix Spec 不列出调用点** — Spec 说"修复 X 功能"但没列出所有函数/端点 → coder 只修一处漏其他。**正例：** Spec 列出 `createShare()`, `listShares()`, `findShareByPath()` 三个函数都需要传 baseUrl → coder 全部改完。**反例：** Spec 只说"修复 URL"→ coder 改了 createShare，漏了 listShares
24. **Fastify 获取端口用 req.server.config.port** — Fastify 没有这个属性。正确方式：`req.headers.host`（包含 host:port）或 `req.hostname`（仅 host）
25. **代码分散在多个目录（2026-05-24 教训，2026-05-25 强化）** — 集成项目代码应集中在项目文件夹（如 `/opt/Workspace/src/projects/obsidian/`），不要分散在旧目录。**前端组件同理：** agent 修改代码时可能在 `src/public/views/` 和 `src/projects/<项目>/public/` 各留一份。**判断哪个是活跃副本：** 查 `app.mjs` 的 import 路径。清理时删孤儿副本，import 路径指向项目目录。**反例：** ObsidianView.mjs 两份（views/ + projects/obsidian/public/），share.html 也是两份，用户要求清理非项目路径的副本。
26. **UI 状态管理条件判断错误（2026-05-24 教训）** — 条件判断导致元素一闪而过。**修复：** 分离"显示条件"和"操作条件"
27. **通过 agent CLI 间接调自己** — Open Design 的 agent 调 hermes CLI = 冗余。直接读设计系统 tokens.css 渲染 HTML 即可
28. **等外部 API 生成效果图** — Stitch API 长 prompt 通过代理容易超时。用 Open Design tokens 本地渲染更快更稳定
29. **CSS backdrop-filter 创建 containing block（2026-05-25 教训）** — `backdrop-filter: blur()` 根据 CSS 规范创建新 containing block，导致 `position: fixed` 子元素相对该元素而非视口。修复：移除 backdrop-filter，改用 `background: rgba()`。详见 `code-principles` skill 的 `references/css-pitfalls.md`。
30. **清理重复文件前验证引用（2026-05-25 教训）** — 移动文件后删除旧副本前，必须验证没有 import/引用指向旧路径。案例：ObsidianView.mjs 移到项目路径后删除 views/ 副本 → 浏览器 import 404。
31. **调研报告写入 wiki/projects/（2026-05-25 教训，第 3 次）** — 分析报告 → `wiki/syntheses/`。只有有 Phase 流程的项目才进 `wiki/projects/`。
32. **frontmatter 版本号不更新** — 每次 patch SKILL.md 必须同步更新 frontmatter `version` 字段。版本号不一致 = 维护失职。
31. **调研报告写入 wiki/projects/（2026-05-25 教训，第 2 次）** — 分析报告、调研结论、方法论对比 = 知识积累 → `wiki/syntheses/`。只有真正的项目（有 Phase 流程、有代码产出）才进 `wiki/projects/`。**判断规则：** 问自己"这个东西有 overview.md + constitution.md + changes/ 吗？"没有 → syntheses。
32. **frontmatter 版本号不更新** — 每次 patch SKILL.md 必须同步更新 frontmatter `version` 字段和版本历史行。版本号不一致 = 维护失职。
33. **CSS `backdrop-filter` 创建 containing block（2026-05-25 教训）** — 给元素加 `backdrop-filter: blur()` 会让该元素成为 `position:fixed` 子元素的 containing block，导致 fixed 定位相对于该元素而非视口。**症状：** 弹出菜单/弹窗用了 `position:fixed` + `clientX/clientY` 但位置偏移。**修复：** 移除 backdrop-filter 改用不创建 CB 的半透明背景（`background: rgba(255,255,255,0.85)`），或将弹出元素用 Teleport 渲染到 `document.body`。
34. **tester 只读代码判 PASS（2026-05-25 教训）** — tester 读了修改后的文件就 `kanban_complete(summary="approved")`，没有用浏览器实际验证任何 UI 效果。大佬测试后发现 3/5 项未修复。**根因：** review 卡 body 写了"用 curl 验证""检查 pm2 日志"但没有强制浏览器截图。**规则：** UI 项目的 tester review spec 必须包含 `必须用浏览器工具实际访问页面，截图验证每个验收标准`。如果 tester 没有浏览器工具，escalate 给灵犀安排手动验证。review 卡 body 缺少"必须截图"= 流程违规。
35. **tester 修改 .env 文件（2026-05-26 教训）** — tester 在验证过程中尝试登录，发现密码不对后直接修改 `.env` 文件重置密码 hash。即使 task body 写了"禁止修改 .env"，tester 仍执行了 `cat .env` + `patch .env`。**根因：** task body 的禁止规则是软约束，tester 的 SOUL.md 没有对应硬性规则。**修复：** tester SOUL.md 已添加"⛔ 绝对禁止修改 .env/config.yaml"规则。**灵犀的 post-review 检查：** tester 完成后，`grep` 检查 `.env` 文件 mtime 是否被修改。
36. **手动改 .env 密码 hash 格式错误（2026-05-26 教训）** — 大佬手动将 `.env` 中 `ADMIN_PASSWORD_HASH` 改为 MD5 格式（`e10adc3949ba59abbe56e057f20f883e`），但代码用 `bcrypt.compare()` 验证，需要 bcrypt 格式（`$2b$10$...`，60 位）。MD5 永远无法通过 bcrypt 验证。**通用规则：** 修改 `.env` 中的密码 hash 前，先查代码确认 hash 算法（bcrypt/argon2/sha256），再用对应算法生成。**快速验证：** `node -e "import('bcrypt').then(b=>b.compare('plaintext','***'))"` 返回 `true` 才算对。
37. **Context File Pattern 执行残留（2026-05-26 教训）** — kanban task 的 bugfix spec 文件（`TODO_SPEC.md`、`TODO_SPEC_V2.md`）写到了项目根目录（`/opt/Workspace/`），没有归档到 `wiki/projects/<项目>/changes/` 下。**根因：** spec 文件是给 coder 用的临时 context，用完后无人清理。**规则：** Phase 8 bugfix spec 完成后，灵犀必须检查项目根目录是否有 `*SPEC*`、`*TODO*`、`*bugfix*` 等临时文件残留，有则移入 `wiki/projects/<项目>/changes/<变更名>/` 归档。
38. **CodeWhale ACP 替代 coder（2026-05-27 验证通过）** — CodeWhale ACP 可以替代 clsh-project 的 coder 角色。**集成方式：** `delegate_task(acp_command="/usr/local/bin/codewhale", toolsets=["file", "terminal"])`。**角色分工：** coder/artist → CodeWhale ACP，tester → Hermes subagent（需要浏览器工具和独立性）。**性能：** 3 个 bug 修复 = 156 秒。**注意：** task body 必须写绝对路径（wiki 路径、代码路径），不要让 CodeWhale 自己搜索（search_files 工具有局限）。详见 `codewhale-workflow` skill。

### 执行纪律（置信度 0.5-0.9）
39. **灵犀做代码推理（置信度 0.9，3 次触发）** — 灵犀是协调者，不是 coder。灵犀推理"后端期望 `{ oldPath, newPath }`"然后告诉 CodeWhale，如果灵犀推理错了，CodeWhale 照错执行。**正确做法（方式 C）：** 灵犀只指定文件路径和问题现象，CodeWhale 自己读代码、自己推理根因、自己修复。| 验证：检查 delegate_task 的 context 是否包含实现细节（CSS 代码/具体步骤/行号级指令）| 触发：delegate_task 给 CodeWhale
40. **CodeWhale 修复后跳过 tester 验证（置信度 0.9，2 次触发）** — Round 7-8 连续 2 次 CodeWhale 修复后直接汇报完成，没有让 tester 浏览器验证。大佬测试发现 4 个功能不生效。**根因：** CodeWhale 修复速度快（88-156 秒），灵犀误以为"代码改了=功能生效"。**规则：** CodeWhale ACP 修复后，必须走完整 tester 验证流程（浏览器截图），不能因为"代码看起来对"就跳过。修复速度 ≠ 修复质量。| 验证：检查 CodeWhale 完成后是否有 tester review 卡 | 触发：CodeWhale delegate_task 返回
49. **灵犀做代码推理再告诉 CodeWhale 怎么改（置信度 0.9，3 轮触发）** — 灵犀自己读了 800 行 CSS，分析出 `!important` 泛滥、断点不够、缺筛选功能，然后写详细 CSS 代码片段告诉 CodeWhale "照这个改"。大佬纠正："你给codewhale一个概念性的目标和关键上下文，让codewhale自己朝着这个目标实现，而不是你直接告诉他怎么改"。**根因：** 灵犀做了代码推理（pitfall #39 的变体），CodeWhale 变成照抄工具。**规则：** delegate_task 给 CodeWhale 时，只给**目标 + 参考文件 + 约束 + 验收标准**。❌ 不该给：具体 CSS 代码、"删 18 处 !important"、"用作用域提升优先级"、详细实现步骤。✅ 该给："大佬说按钮丑，重做 UI。参考 style.css 和 CronMonitor.mjs。浅色毛玻璃主题。node -c 通过。"详见 `references/integration/codewhale-acp-integration.md` §Way C。| 验证：同 #39 | 触发：同 #39
42. **Vue 响应式数组更新（2026-05-27 教训）** — `splice` 和直接索引赋值确实触发响应式，但如果渲染条件依赖其他状态（如 `isRevoked`），需要确保状态更新后重新计算。**更可靠的方式：** 操作后调用 `openShareMgr()` 重新加载列表，而不是手动修改数组。
43. **Workspace UI 暗色主题陷阱（2026-05-27 教训，3 轮修复）** — AI 默认生成暗色 UI（#1a1d23, #252830），但 Workspace 是**浅色毛玻璃主题**。症状：Modal 背景黑色+文字黑色=看不见。**根因：** AI 训练数据中暗色主题更常见，倾向默认暗色。**规则：** Workspace 项目必须用 `workspace-development` skill 的设计系统变量。禁止自行定义颜色。详见 `workspace-development` skill。
44. **自定义 Tab UI 陷阱（2026-05-27 教训）** — AI 会创建 `viewMode` ref + 自定义 tab 切换 UI，但 Workspace 有自带的 QuickNavComponent（通过 `projects.json` tabs 配置）。**规则：** 前端组件用 `props: { activeTab: { type: String } }` 接收工作台 tab，不渲染任何 tab 切换 UI。
45. **前端文件在 projects/ 下需要双静态根（2026-05-27 教训）** — 前端组件放 `src/projects/<id>/public/`，app.mjs 用相对路径 `../projects/` import。server.mjs 需注册第二个 fastifyStatic（`prefix: '/projects/'`），否则浏览器 404。
43. **新增子模块必须先读 AGENTS.md（2026-05-27 教训）** — 在 Workspace 中添加新项目子模块时，必须先读 `AGENTS.md` 的目录结构规范，不能凭经验假设文件位置。**反例：** 把 CronMonitor.mjs 放在 `views/` 而非 `projects/cron/public/`，大佬纠正后才修复。**正例：** 读 AGENTS.md → 确认 obsidian 模式 (`projects/<id>/plugin.mjs` + `public/<View>.mjs`) → 按模式创建。
44. **CodeWhale ACP 写入错误路径（2026-05-27 教训）** — CodeWhale 可能读取现有文件确定"自然"位置，忽略 constitution 指定的目标路径。**案例：** constitution 定义 `src/projects/cron/CronMonitor.mjs`，但 CodeWhale 看到旧文件在 `views/CronMonitor.mjs` 就写到 views/。**规则：** context/goal 中必须显式写明**绝对输出路径**（如"创建文件：/opt/Workspace/src/projects/cron/CronMonitor.mjs"），不能只靠 constitution 引用。
45. **CodeWhale 首轮输出功能不全 + 二轮补全模式（2026-05-27 验证）** — 第一轮 CodeWhale ACP 可能产出结构正确但关键功能缺失的文件（657 行，无 AI 徽章、无 LLM 面板、无筛选）。**根因：** context 是"设计文档风格"（描述期望效果），CodeWhale 按自己理解裁剪。**修复模式：** 首轮后 grep 验证关键功能（`grep -c "activeFilter\|aiExpanded\|● 活跃"`）；缺失时二轮用**精确 bullet-point 需求**（"添加紫色小标签 [AI]，样式: background: linear-gradient(...)"），不要用设计文档风格。比一次性写完更可靠，因为首轮暴露的变量命名和结构可以作为二轮的精确 spec。
46. **Fastify 双静态根配置（2026-05-27 教训）** — 需要同时服务 `src/public/` 和 `src/projects/*/public/` 时，不能用 `root: [array]`（路径会 double-prefix）。正确方式：注册两次 fastifyStatic，第一个用 `decorateReply: true`（主目录），第二个用 `decorateReply: false`（项目目录）。详见 `references/workspace-sub-module-pattern.md`。
47. **CodeWhale 部分编辑导致文件损坏（2026-05-28 教训）** — CodeWhale 超时时可能已对同一文件做了多次部分 patch，导致括号嵌套错乱。症状：`node -c` 报语法错误，但逐行括号计数显示总数平衡（opens=closes）。**根因：** 部分 patch 修改了局部结构但未同步调整周围括号。**规则：** (1) CodeWhale 超时后，先 `node -c` 检查文件是否可用；(2) 如果报错且错误位置随修改漂移（不同行号），直接 `write_file` 重写整个文件，不要逐行修补；(3) 逐行修补括号错乱是 O(n²) 陷阱，比重写慢 10 倍。**反例：** 本案中 CodeWhale 做了 69 次 API 调用，ContentView.mjs 被多次部分修改，灵犀花了 30 分钟逐行 debug 括号问题，最终还是重写了整个文件。
48. **Vue3 CDN 组件解构完整性（2026-05-28 教训）** — 创建 Vue3 CDN 组件时，必须确保所有使用的 Vue API 都从 `Vue` 对象解构。常见遗漏：`computed`（用于派生状态）、`watch`（用于监听）。**症状：** `ReferenceError: computed is not defined`，但 `node -c` 语法检查通过（因为 `Vue.computed` 是运行时依赖）。**规则：** 新建组件时，默认解构 `const { ref, computed, watch, onMounted, onUnmounted, h, defineComponent } = Vue;`，不用的不扣分，漏了会崩。
49. **灵犀做代码推理再告诉 CodeWhale 怎么改（2026-05-29 教训，3 轮）** — 灵犀自己读了 800 行 CSS，分析出 `!important` 泛滥、断点不够、缺筛选功能，然后写详细 CSS 代码片段告诉 CodeWhale "照这个改"。大佬纠正："你给codewhale一个概念性的目标和关键上下文，让codewhale自己朝着这个目标实现，而不是你直接告诉他怎么改"。**根因：** 灵犀做了代码推理（pitfall #39 的变体），CodeWhale 变成照抄工具。**规则：** delegate_task 给 CodeWhale 时，只给**目标 + 参考文件 + 约束 + 验收标准**。❌ 不该给：具体 CSS 代码、"删 18 处 !important"、"用作用域提升优先级"、详细实现步骤。✅ 该给："大佬说按钮丑，重做 UI。参考 style.css 和 CronMonitor.mjs。浅色毛玻璃主题。node -c 通过。"详见 `references/integration/codewhale-acp-integration.md` §Way C。
50. **API 数据源一致性（2026-05-28 教训）** — 不同 API 端点检查同一数据时，必须使用同一个底层函数。**反例：** overview API 用 `execSync` 调 Python 脚本检查渠道状态，channels API 用 JS 异步函数检查，导致两个 Tab 显示的状态不一致。**规则：** 提取共享的检查函数，所有端点共用。
51. **灵犀做浏览器测试（2026-05-29 教训）** — 灵犀直接调 MCP 的 `browse_webpage` 测试 SPA 渲染，发现 Vue hydration 问题后甩锅给"Playwright 已知行为"。**根因：** (1) 用了 MCP 附带的浏览器工具（MoviePilot CloakBrowser）而非 hermes browser tool；(2) 灵犀不该做浏览器测试，这是 tester 的活。**规则：** UI/SPA 测试必须 `delegate_task` 给 tester 子 agent（有 agent-browser/camofox），灵犀只协调不测试。即使"只是想快速看一下"也不能自己动手。| 验证：检查灵犀是否有 `browse_webpage`/`screenshot` 等浏览器工具调用 | 触发：任何 UI 验证需求
50. **Fastify handler 中禁止 execSync（2026-05-28 教训）** — `execSync` 会阻塞整个 Node.js 事件循环。在 Fastify 请求处理中使用 `execSync`（如调用 `channel_check.py`）会导致所有并发请求排队等待。**修复：** 改用 `execFile`（callback）或 `child_process` 的 Promise 封装 + `await`。超时设置 10-30s。

### UI 设计（置信度 0.9）
55. **跳过 Open Design 知识包加载（2026-05-29 教训）** — 灵犀手写 HTML 颜色/间距/排版，没有加载 `/opt/open-design/design-systems/<name>/tokens.css` 的设计变量。大佬对比后确认 Open Design 版本远优于手写版。**根因：** 灵犀觉得"简单任务不需要加载设计系统"。**规则：** Phase 3 设计发散流程中，加载 Open Design 知识包是**强制步骤**，不论项目大小。至少读取 `tokens.css`（CSS 变量）和 `craft/anti-ai-slop.md`（质量底线）。**验证：** 检查 HTML 文件中是否有 `var(--*)` 引用，是否有硬编码颜色值 | **触发：** 任何 UI 项目 Phase 3

### 自进化机制（置信度 0.5-0.7）
51. **LLM 自评不可靠（2026-05-29 SkillLens 论文）** — 单 LLM 评委评估 skill 质量准确率仅 46.4%（接近随机）。加 meta-skill 维度后提升到 73.8%。**规则：** SKILL.md 评分必须用独立子 agent（不是灵犀自己），且每轮换新评委（避免锚定效应）。**验证：** 检查评分是否由独立 agent 完成 | **触发：** 任何 Darwin 优化循环
52. **维度关联簇（2026-05-29 花叔 40 次实验）** — 改一个评分维度时，关联维度会意外提升。Dim2/3/4 是结构簇（工作流清晰度/失败模式编码/检查点设计），Dim5/9 是具体性簇。**规则：** 优化时先改簇内最低维度，带动其他维度一起涨。不要一轮改多个维度（反模式 #5）。**验证：** 检查是否只改了一个维度 | **触发：** Darwin 优化循环
53. **Skill 是可训练的外部状态（2026-05-29 SkillOpt 论文）** — SKILL.md 不是"写完就完了"的静态文本，而是 LLM 的可训练外部状态（类似神经网络权重）。每次优化 = 一次训练步，必须通过验证（test-prompts）才能保留。**规则：** 修改 SKILL.md 前必须有验证机制（Darwin 棘轮或执行审计），不能凭感觉改 | **触发：** 任何 SKILL.md 修改
54. **执行审计应在归档时运行（2026-05-29 教训）** — 执行审计器（grep session 日志检查合规率）不需要 cron 定时，应该在大佬说"归档"时自动运行（Phase 7 步骤 11）。原因：工作流优化不需要实时反馈，每个项目结束后看一次就够了。**规则：** Phase 7 归档时必须运行 `references/scripts/execution-audit.py` | **触发：** 大佬说"归档"
51. **文件卫生陷阱（2026-05-29 Darwin+ECC 调研教训）** — 用"文件是否存在""链接是否断""编号是否连续"来评估 SKILL.md 质量 = 文件卫生检查，对工作流进化**没用**。Darwin v2.0 + SkillLens 论文证明：真正重要的是 Dim5 可执行具体性（17 分，禁止模糊词）、Dim3 失败模式编码（12 分，"如果 X 失败 → Y"）、Dim8 实测表现（23 分，跑 test-prompts）。**规则：** 评估 SKILL.md 质量时，用 Darwin 9 维 rubric（见 `references/methodology/verification-and-ratchet.md`），不用文件结构检查脚本。同理，ECC 证明确定性检查（grep session 日志 + exit code）比 LLM 判断可靠得多（LLM 自评准确率仅 46.4%，SkillLens 实证）。
55. **跳过 Phase 3 设计发散直接手写 HTML（2026-05-29 教训）** — UI 项目中灵犀手写 HTML 模板（自定义 CSS 变量、自己排版），没有加载 Open Design 知识包（tokens.css + DESIGN.md + craft 规则）。大佬反馈"效果一般"。**正确流程：** Phase 3 设计发散 → 读取 `/opt/open-design/design-systems/<name>/tokens.css` → 读取 DESIGN.md + craft/anti-ai-slop.md → 渲染 2-3 个变体 → 大佬选择。**规则：** UI 项目禁止灵犀手写 CSS，必须用 Open Design tokens。详见 `references/workflow/phase3-spec.md` §设计发散。
56. **delegate_task 并行子 agent 互相覆盖文件（2026-05-29 教训）** — 3 个子 agent 并行创建 HTML 模板，每个都重写了共享的 tokens.css（各自风格不同：一个暗色、一个浅色、一个空壳）。**规则：** 共享资源文件（CSS、配置）由灵犀直接写入/管理，子 agent 只写各自独立的产出物。在 task context 中明确写"只写 <文件名>，不要修改其他文件"。 — 执行审计器（`references/scripts/execution-audit.py`）应该在大佬说"归档"时触发（Phase 7 步骤 11），不需要 cron 定时。原因：审计需要完整的 session 数据，只有项目结束时才有。Phase 8 的修复轮次也是评分标准（修复轮次越多，说明流程越不稳定）。**触发关键词：** "归档"/"wrap up"/"做完了吧"。
51. **Patch 编号列表时意外删除条目（2026-05-29 教训）** — 用 `patch` 工具替换包含编号列表的文本段时，如果 old_string 包含 #37-#49 但 new_string 只写了 #39-#49 的修改版，#38 会被静默删除。**根因：** patch 是整段替换，不在 old_string 中出现的行会被丢弃。**规则：** (1) 替换编号列表段时，new_string 必须包含 old_string 中的所有条目，不能只写"要改的几条"；(2) patch 后必须 `grep -c` 验证条目数量不变（或按预期增减）；(3) 对于 10+ 条的编号列表，优先用 `replace_all=false` + 精确匹配单条，不要整段替换。**反例：** 本案中 old_string 匹配了 #38-#49 整段，new_string 只升级了 #39/#40/#49 但漏了 #38，导致 CodeWhale ACP 集成说明丢失。
52. **跳过 Phase 3 设计发散直接手写 HTML（2026-05-29 教训）** — 灵犀创建 MoviePilot HTML 模板时没有加载 open-design 知识包，手写了"自己觉得可以"的 HTML。大佬反馈"效果一般"。**正确流程（Phase 3）：** (1) 加载 `/opt/open-design/design-systems/<name>/tokens.css` + `DESIGN.md`；(2) 加载 `craft/anti-ai-slop.md` + `craft/state-coverage.md` 质量标准；(3) 渲染 2-3 个变体供用户选择；(4) 用户确认后写入 constitution。**反例：** 手写 CSS 变量（颜色/间距自编）→ 用户说"效果一般"。**正例：** 加载 Glassmorphism tokens → 3 套变体对比 → 用户选 Glass → 效果显著提升。**规则：** 任何 UI 项目必须走 Phase 3 设计发散，禁止跳过直接写 HTML。
53. **子 agent 并行写共享文件导致冲突（2026-05-29 教训）** — 3 个 delegate_task 子 agent 并行创建 HTML 模板时，每个都重写了 tokens.css（各自风格不同：暗色/亮色/自定义），导致最终文件被覆盖为错误版本。**规则：** 共享资源文件（tokens.css、公共样式）由灵犀直接写入，不在子 agent 的 task 范围内。子 agent 只写各自独立的文件。**验证：** 子 agent 完成后检查共享文件的 mtime 和内容是否被修改。
57. **Skill 删除会连带删除 scripts/ 目录（2026-05-31 教训）** — `skill_manage(action='delete')` 会删除整个 skill 目录，包括 `scripts/`、`references/` 等子目录。如果脚本被其他组件（如插件）引用，删除 skill 会导致脚本丢失。**反例：** 删除 moviepilot skill 时，mp_render.py 脚本被一起删除，mp-command 插件调用失败。**规则：** 删除 skill 前，必须检查是否有脚本/文件被其他组件引用，有则先备份/迁移。**验证：** 删除后 `find ~/.hermes -name "<script_name>"` 确认脚本是否还在。**补充：** `skill_manage(action='delete', absorbed_into=<target>)` 的 target 必须是已存在的 skill，不能是 plugin。
59. **Phase 8 每轮必须记录测试结果（2026-05-31 教训）** — 大佬测试反馈后，必须在 `wiki/projects/<项目>/changes/<变更名>/test-log.md` 中记录：(1) 测试结果列表 (2) 根因分析 (3) 修复内容 (4) 流程违规（如有）。Round 1 测试未记录 → Round 3 大佬问"有没有记录每次测试结果" → 才开始写。**规则：** 每轮 Phase 8 反馈的第一件事是更新 test-log.md，不是分析代码。| 验证：检查 test-log.md 是否有本轮记录 | 触发：大佬说"测试结果"/"反馈"
60. **Phase 8 禁止灵犀分析根因再告诉 CodeWhale（2026-05-31 教训）** — 灵犀分析了 tab 状态管理、Bearer token、cookie domain 等根因，然后写具体修改方案给 CodeWhale。大佬指出"违规直接分析让coder修复，不是定目标和上下文发送路径给codewhale分析修复"。**规则（Way C 铁律）：** delegate_task 给 CodeWhale 时只给：(1) 大佬反馈的现象（1-2 句话）(2) 相关文件路径 (3) bugfix spec 路径 (4) 验证命令。❌ 不该给：根因分析、具体修改方案、行号级指令。✅ 该给："大佬说 tab 点击没反应，显示未知标签页。相关文件：/opt/Workspace/src/projects/moviepilot/public/MovieView.mjs。请先读代码自己分析根因。" | 验证：delegate_task context 是否包含实现细节 | 触发：Phase 8 派 CodeWhale 修复
61. **外部 API 集成必须先查 OpenAPI spec（2026-05-31 教训）** — 代理调 MoviePilot API 返回 404。灵犀假设端点是 `/api/v1/tools/call`，实际 MoviePilot 的 OpenAPI spec 在 `http://host:port/api/v1/openapi.json`，确认端点是 `/api/v1/mcp/tools/call`，推荐用 `/api/v1/recommend/tmdb_movies` 等 REST 端点。认证方式也不是 JWT，而是 `X-API-KEY` header。**规则：** 集成外部 API 时，第一步是 `curl http://host:port/api/v1/openapi.json` 获取完整端点列表和认证方式。不要假设端点路径。| 验证：检查代理是否调了正确的端点 | 触发：外部 API 集成
62. **GET vs POST handler 不匹配（2026-06-01 教训，5 轮排查）** — token URL 是浏览器 GET 请求，但 plugin 只有 POST handler。症状是"点击链接后仍然显示登录页"，所有周边修复（cookie/domain/API）都无效。**根因：** 没人检查"GET 请求是否有对应的 handler"。**规则：** 端到端调试时，第一步验证"请求是否到达了 handler"（`grep -n "fastify.get\|fastify.post" plugin.mjs`），而不是"handler 内部逻辑是否正确"。浏览器点击 = GET，API 调用 = POST，两者需要分别有 handler。| 验证：curl -v 检查 HTTP method 和响应状态码 | 触发：token/链接/深链接类功能
64. **fetch 缺少 credentials 导致 session cookie 丢失（2026-06-01 教训）** — Workspace 子模块的 Vue 前端用 `fetch()` 调用同域 Fastify API，但没加 `credentials: 'include'`。token 自动登录成功设置了 session cookie，但后续 API 请求不带 cookie → authGuard 返回 401 "未登录" → UI 无内容。**症状：** "API 通了但界面没有内容"，curl 带 cookie 能拿到数据。**根因：** 默认 `fetch` 的 `credentials` 是 `same-origin`，但某些浏览器/场景下（跨子路径、非简单请求）仍不自动发送 cookie。**规则：** Workspace 子模块的前端 `apiGet`/`apiPost`/`apiDelete` helper 必须加 `credentials: 'include'`。**验证：** 浏览器 DevTools → Network → 检查请求头是否带 `Cookie` | **触发：** 任何 Fastify session 认证 + 前端 fetch 的组合
65. **自构造 URL 忽略 API 返回的 url 字段（2026-06-01 教训）** — `/mp` 命令插件调 token API 获取 token 后，自己拼 URL 为 `{BASE_URL}/?token={token}`，但 token API 返回了正确的 `url` 字段（`/api/moviepilot?token=xxx`）。自构造的根路径没有 token handler → 点击链接仍显示登录页。**规则：** 生成带 token/参数的 URL 时，优先使用 API 响应中的 `url` 字段拼接 `BASE_URL`，不要自己构造路径。自构造只在 API 不返回 url 时作为 fallback。**验证：** 对比生成的 URL 和实际 handler 注册路径（`grep fastify.get plugin.mjs`）| **触发：** 任何"调 API 获取 token → 生成链接"的流程
64. **fetch 缺少 credentials 导致 session cookie 丢失（2026-06-01 教训）** — Workspace 子模块的 Vue 前端用 `fetch()` 调用同域 Fastify API，但没加 `credentials: 'include'`。token 自动登录成功设置了 session cookie，但后续 API 请求不带 cookie → authGuard 返回 401 "未登录" → UI 无内容。**症状：** "API 通了但界面没有内容"，curl 带 cookie 能拿到数据。**根因：** 默认 `fetch` 的 `credentials` 是 `same-origin`，但某些浏览器/场景下（跨子路径、非简单请求）仍不自动发送 cookie。**规则：** Workspace 子模块的前端 `apiGet`/`apiPost`/`apiDelete` helper 必须加 `credentials: 'include'`。**验证：** 浏览器 DevTools → Network → 检查请求头是否带 `Cookie` | **触发：** 任何 Fastify session 认证 + 前端 fetch 的组合
65. **自构造 URL 忽略 API 返回的 url 字段（2026-06-01 教训）** — `/mp` 命令插件调 token API 获取 token 后，自己拼 URL 为 `{BASE_URL}/?token={token}`，但 token API 返回了正确的 `url` 字段（`/api/moviepilot?token=xxx`）。自构造的根路径没有 token handler → 点击链接仍显示登录页。**规则：** 生成带 token/参数的 URL 时，优先使用 API 响应中的 `url` 字段拼接 `BASE_URL`，不要自己构造路径。自构造只在 API 不返回 url 时作为 fallback。**验证：** 对比生成的 URL 和实际 handler 注册路径（`grep fastify.get plugin.mjs`）| **触发：** 任何"调 API 获取 token → 生成链接"的流程
63. **CodWhale 网络请求超时模式（2026-06-01 教训）** — CodWhale 在 curl 到局域网 IP（如 192.168.0.71:3001）时反复超时 600s，即使 ping 可达。**规则：** (1) 代码修改和网络测试必须分开派发，不要让 CodWhale 做"读代码 + curl 测试 + 修复"一体化任务；(2) 网络验证用主 agent 的 terminal 或 Hermes subagent；(3) CodWhale 擅长纯代码修改（读文件→patch），不擅长需要网络验证的任务。| 验证：检查 delegate_task 是否包含 curl 到外部 IP 的命令 | 触发：Phase 8 派 CodWhale 修复含网络调用的任务
58. **Phase 1 需求澄清必须先捋清使用场景（2026-05-31 教训）** — 灵犀在 Phase 1 直接问 UI 风格偏好，大佬纠正"不应该先捋清楚使用场景，才好定义交互操作和 UI 优化方向吗"。**规则：** Phase 1 需求澄清顺序：(1) 使用场景（谁用、什么设备、什么场景）→ (2) 核心功能（优先级排序）→ (3) 交互操作（怎么操作）→ (4) UI 风格（怎么展示）。**禁止：** 跳过使用场景直接问 UI 风格/技术方案。**反例：** 直接问"你希望什么风格？"→ 大佬纠正。**正例：** 先问"你主要在什么设备上用？手机还是电脑？"→ 再问"最常用的场景是什么？"→ 最后问"UI 风格偏好？"

## Verification Checklist（每次使用此 skill 前）

### 流程合规
- [ ] 确认不是简单查询/单步操作（否则不应触发 clsh-project）
- [ ] 确认 Phase 1 已执行调研前置（调研摘要已写入 conversation.md 或大佬明确跳过）
- [ ] 确认 Phase 1-3 已完成且有文档产出（conversation.md / proposal.md / constitution.md）
- [ ] 确认 UI 项目 Phase 3 是否需要设计发散（2-3 mockup 变体，截图发飞书）
- [ ] 确认大佬已明确回复"确认"才进入下一 Phase
- [ ] 确认 tasks.md 中每个 Task 有验收标准 + 完整代码（无 TBD/TODO）
- [ ] 确认代码任务已派给 coder/artist，不是灵犀直接写
- [ ] 确认每个 Task 有 tester 卡
- [ ] 确认 Phase 6 有 Security Scan 步骤
- [ ] 确认 UI 项目 Phase 6 tester 卡包含 Browser QA 检查清单（必须含"截图验证"字样）
- [ ] 确认 agent 派发 context 包含 Pre-Commit 安全自检清单
- [ ] 确认 Phase 8 反馈走流程而非"顺手修了"
- [ ] 确认 Auto-Fix 不超过 2 轮后 escalate
- [ ] 确认每个 kanban task body 包含 proposal 相关章节 + constitution 约束 + 不在范围内声明
- [ ] 确认 Phase 1 中大佬描述现有行为时已代码交叉验证
- [ ] 确认满足条件的架构决策已记录为 ADR（wiki/projects/<项目名>/docs/adr/）
- [ ] 确认新增子模块已读 AGENTS.md 并按其目录结构规范创建文件（pitfall #43）

### 验证合规（Layer 2 — 2026-05-29 新增）
- [ ] 确认声称"完成/修复/通过"前已走完 5 步验证函数（铁律 #14）
- [ ] 确认验证命令是新鲜执行的，不是复用之前的输出
- [ ] 确认 CodeWhale 修复后已走独立 tester 验证（不是只看 CodeWhale 的声明）
- [ ] 确认没有使用防辩解表中的借口跳过验证

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v5.11.0 | 2026-06-01 | **fetch credentials + URL 自构造陷阱**：新增 pitfall #64（fetch 缺少 `credentials: 'include'` 导致 session cookie 丢失，API 返回 401 但 UI 无报错）和 #65（自构造 URL 忽略 API 返回的 url 字段，导致 token 链接指向无 handler 的路径）。两坑均来自 MoviePilot Phase 8 Round 2。 |
| v5.11.0 | 2026-06-01 | **fetch credentials + URL 自构造陷阱**：新增 pitfall #64（fetch 缺少 `credentials: 'include'` 导致 session cookie 丢失，API 返回 401 但 UI 无报错）和 #65（自构造 URL 忽略 API 返回的 url 字段，导致 token 链接指向无 handler 的路径）。两坑均来自 MoviePilot Phase 8 Round 2。更新 workspace-sub-module-pattern.md 新增 credentials 注意事项。 |
| v5.10.1 | 2026-06-01 | **GET handler 缺失 + CodWhale 网络超时**：新增 pitfall #62（GET vs POST handler 不匹配，5 轮排查才找到）和 #63（CodWhale curl 到局域网 IP 超时 600s，必须拆分代码修改和网络测试）。 |
| v5.10.0 | 2026-05-31 | **Phase 8 测试记录 + Way C 铁律 + 外部 API 集成**：新增 pitfall #59（Phase 8 每轮必须记录测试结果到 wiki test-log.md）、#60（禁止灵犀分析根因再告诉 CodeWhale，必须给目标+路径让 CodeWhale 自己分析）、#61（外部 API 集成必须先查 OpenAPI spec 确认端点和认证方式）。 |
| v5.9.0 | 2026-05-31 | **Skill 删除陷阱 + 需求澄清顺序**：新增 pitfall #57（skill_manage delete 会连带删除 scripts/ 目录，删除前必须检查脚本是否被其他组件引用）和 #58（Phase 1 需求澄清必须先捋清使用场景再问 UI 风格，顺序：使用场景→核心功能→交互操作→UI 风格）。 |
| v5.8.0 | 2026-05-29 | **自进化方法论落地**：新增 `references/methodology/darwin-ecc-evolution.md`（Darwin 9 维 rubric + 维度关联簇 + ECC 执行验证 + 反模式黑名单）。新增 pitfalls #51-54（LLM 自评不可靠/维度关联簇/Skill 可训练状态/执行审计触发时机）。SKILL.md 新增 4 条自进化机制 pitfalls。 |
| v5.7.0 | 2026-05-29 | **自进化方案 Layer 1+2 落地**：新增铁律 #14（5 步验证函数）。新增 `references/methodology/verification-and-ratchet.md`（验证框架 + 防辩解表 + 置信度评分 + 棘轮机制 + 结构评分器）。Phase 6/8 workflow 注入 5 步验证函数 + 防辩解表。Verification Checklist 分"流程合规"+"验证合规"两部分，新增 4 项验证检查。 |
| v5.6.0 | 2026-05-29 | **Way C 派发铁律强化**：更新 `references/integration/codewhale-acp-integration.md` 新增 Way C 详细规范（灵犀给目标+约束，不做代码推理）。更新 `references/workflow/phase6-execution.md` 任务派发流程新增 Way C 铁律引用。教训来源：上游监控 UI 迭代中灵犀连续 3 轮自己分析 CSS 再告诉 CodeWhale 怎么改，违反角色分离。 |
| v5.5.3 | 2026-05-28 | **内容管理子模块模式**：更新 `references/workspace-sub-module-pattern.md` 新增 clsh-content 集成案例（外部脚本集成 + 文件系统数据源 + 渐进式三 Wave 交付）。 |
| v5.5.3 | 2026-05-28 | **CodeWhale 文件损坏 + Vue 解构 + API 一致性**：新增 pitfall #47（CodeWhale 部分编辑导致括号损坏 — 超时后直接重写不要逐行修）、#48（Vue3 CDN 组件解构完整性 — 默认解构 computed/watch）、#49（API 数据源一致性 — 多端点检查同一数据共用函数）、#50（Fastify handler 禁止 execSync — 改用 execFile+await）。更新 `references/workspace-sub-module-pattern.md` 新增内容管理子模块模式。 |
| v5.5.2 | 2026-05-27 | **Workspace 子模块模式 + CodeWhale 二轮补全**：新增 pitfall #43（新增子模块必须先读 AGENTS.md）、#44（CodeWhale 写入错误路径 — context 必须写绝对输出路径）、#45（首轮功能不全 — 二轮用精确 bullet-point 需求补全）、#46（Fastify 双静态根配置）。新增 `references/workspace-sub-module-pattern.md`（Workspace 子模块开发完整模式）。Verification Checklist 新增 AGENTS.md 检查项。 |
| v5.4.0 | 2026-05-27 | **CodeWhale ACP 集成**：Phase 6/8 的 coder/artist 角色使用 CodeWhale ACP 执行（`/usr/local/bin/codewhale`），tester 保持 Hermes subagent。新增 Constitution 注入机制（派发前读取 source-of-truth/constitution.md 注入 worker context）。Phase 8 Bugfix Spec 模板参考 OpenSpec Delta Spec 格式。 |
| v5.3.7 | 2026-05-26 | **.env hash 格式 + spec 残留清理**：新增 pitfall #36（手动改 .env 密码 hash 必须先查代码确认算法，bcrypt vs MD5 格式不通用）和 #37（Phase 8 结束后检查项目根目录 spec 残留文件，移入 wiki 归档）。 |
| v5.3.4 | 2026-05-25 | **Karpathy + Superpowers 行为约束融合**：新增 `references/methodology/soul-md-behavioral-enforcement.md`（交付门禁、目标转换、防辩解表）。Phase 8 新增诊断引擎模式（灵犀先诊断根因再派 coder）。所有 agent SOUL.md 已补强三板斧。 |
| v5.3.3 | 2026-05-25 | **CSS containing block + tester 应付教训**：新增 pitfall #33（`backdrop-filter` 创建 containing block 导致 position:fixed 失效）、#34（tester 只读代码判 PASS — UI 项目 review spec 必须含"截图验证"）。Phase 8 说明强化：tester review spec 必须明确验证方式。Verification Checklist 更新：tester 卡必须含"截图验证"字样。 |
| v5.3.2 | 2026-05-25 | **Phase 8 Wave 分批 + Pitfall #25 强化**：Phase 8 路径 B 新增 Wave 分批模式（多问题按优先级分 Wave，逐 Wave 执行）。Pitfall #25 扩展：前端组件同理会复制到多目录，以 app.mjs import 路径为准清理孤儿副本。 |
| v5.3.2 | 2026-05-25 | **Phase 8 教训补充**：新增 #29（静态文件服务器根目录限制 — 前端文件必须留在 static root 内）、#30（清理重复文件前必须 grep 验证引用）。原 #29-30 重编号为 #31-32。 |
| v5.3.1 | 2026-05-25 | **Review 修复**：Pitfalls 重新编号 1-30（修复缺号+重号）。新增 #29（wiki/projects vs syntheses 分类规则）、#30（frontmatter 版本号同步）。Phase 3 设计发散展示方式改为交互原型优先（nginx :8088）。 |
| v5.3.0 | 2026-05-25 | **Matt Pocock Skills 借鉴**：引入 7 个优化模式 — 代码交叉验证（铁律 #12）、CONTEXT.md 领域术语表、ADR 架构决策记录、Vertical Slice 任务切分、Prototype 可运行原型、Module Depth 评估、Handoff 跨 session 文档。新增 2 个模板（context-template.md、adr-template.md）+ 1 个方法论参考（matt-pocock-patterns.md）。Phase 0-7 各有增量更新。Verification Checklist 新增 2 项。 |
| v5.2.3 | 2026-05-24 | **Phase 8 派发方式纠正**：用户明确要求 clsh-project 流程必须用 kanban 派发，禁止用 delegate_task 替代。新增 pitfall #21（代码应集中在项目文件夹）、#22（UI 状态管理条件判断错误导致元素一闪而过）。 |
| v5.2.1 | 2026-05-24 | **设计工具链补充**：新增 `stitch-mcp-workflow.md`（Stitch MCP 集成完整指南）和 `ui-prompt-frameworks.md`（RTCF/v0/Stitch/DESIGN.md 四大 prompt 框架）。更新 `ui-design-workflow.md` 工具矩阵增加 Stitch MCP 和 Open Design tokens.css 方案。 |
| v5.2.2 | 2026-05-24 | **Phase 8 教训补充**：新增 pitfall #19（Bugfix Spec 必须列出所有调用点）、#20（Fastify 端口获取用 req.headers.host）。新增 `references/integration/fastify-url-port.md`。Phase 8 Bugfix Spec 模板增加"需要修改的函数/端点"字段。 |
| v5.2.0 | 2026-05-24 | **设计工具链更新**：Phase 3 设计发散移除 html-anything，全面使用 Open Design 设计系统 tokens + 图片模型。新增 `references/integration/image-generation-api-notes.md`（OpenRouter/Gemini 实测笔记）。 |
| v5.1.0 | 2026-05-23 | **gstack 借鉴落地**：Phase 3 新增 UI 设计发散（2-3 HTML mockup 变体）；Phase 6 新增 Browser QA（UI 项目必做浏览器自动化测试）+ Pre-Commit 安全自检（代码提交前检查清单）。 |
| v5.0.0 | 2026-05-23 | **SKILL.md 瘦身**：Phase 详情拆分到 references/workflow/，SKILL.md 从 1245→~450 行，符合官方 500 行上限。 |
| v4.3.0 | 2026-05-23 | **蒸馏 v2 集成**：Phase 0 读取 learnings.md 内化历史教训；Phase 6 checkpoint 后微蒸馏（10 秒 append）；Phase 7 binary eval + 故障分类 + 条件触发深度蒸馏。 |
| v4.2.0 | 2026-05-23 | **项目蒸馏集成（v1，已废弃）**：Phase 7 归档新增蒸馏步骤。 |
| v4.1.0 | 2026-05-22 | **上游优化集成**：(1) Phase 6 新增 Wave 并行派发策略（Kiro Specs 模式）+ `hermes kanban swarm` 快速模式；(2) Phase 8 路径 A 新增 Bugfix Spec 结构化格式（Kiro 模式）；(3) 新增 `phase8-checkpoint-template.md`；(4) 修复 2 个断链（sketch/github-sync-guide） |
| v4.0.0 | 2026-05-22 | **Pitfalls 大迁移 + 边界定义**：89 条 Common Pitfalls 去重→78 条→三类迁移（流程纪律保留、技术陷阱→wiki、工具链→references/integration/）。新增边界定义（膨胀阈值）。SKILL.md 从 1237→~1100 行。 |
| v3.8.0 | 2026-05-21 | Phase 6 与 Hermes Kanban 对齐（Blocked 状态、Review 卡时机、Worker Heartbeat） |
| v3.7.0 | 2026-05-21 | References 架构重构（项目相关→wiki、跨项目共享→wiki/reference/） |

> 完整版本历史见 git log。

## 参考文件

### 📐 方法论
- `references/methodology/kiro-superpowers-analysis.md` — Kiro + Superpowers + Phoenix 工作流分析
- `references/methodology/ralph-loop-analysis.md` — Ralph Loop：原理 + Phase 6 映射
- `references/methodology/superpowers-v5-changes.md` — Superpowers v5 关键变更
- `references/methodology/agent-skill-execution-research.md` — Agent 执行跑偏：根因 + 5 种方案
- `references/methodology/superpowers-architecture-analysis.md` — Superpowers 架构拆解
- `references/methodology/matt-pocock-patterns.md` — **Matt Pocock Skills 借鉴分析**（CONTEXT.md、ADR、Vertical Slice、Prototype、Handoff 等 7 个模式）
- `references/methodology/soul-md-behavioral-enforcement.md` — **SOUL.md 行为约束：Karpathy + Superpowers 融合方案**（交付门禁、目标转换、防辩解表）
- `references/methodology/verification-and-ratchet.md` — **验证框架与棘轮机制**（5步验证函数、防辩解表、置信度评分、质量评分器）
- `references/methodology/darwin-ecc-evolution.md` — **Darwin + ECC 自进化方法论**（9 维 rubric、维度关联簇、执行审计器、反模式黑名单）
- `references/methodology/evolution-log.md` — **棘轮进化日志**（每次 patch 后的结构评分记录）

### 📋 模板
- `references/templates/constitution-template.md` — Constitution 模板
- `references/templates/archive-workflow.md` — Phase 7 归档操作手册
- `references/templates/phase7-archive-checklist.md` — 归档快速检查清单
- `references/templates/context-template.md` — **CONTEXT.md 领域术语表模板**（Phase 1 自然积累）
- `references/templates/adr-template.md` — **ADR 架构决策记录模板**（Phase 3 满足 3 条件才创建）

### 🔄 流程详情（Phase 参考）
- `references/workflow/phase0-1-requirements.md` — Phase 0+1: 需求准备与澄清
- `references/workflow/phase2-design.md` — Phase 2+2.5: 方案设计与技术验证
- `references/workflow/phase3-spec.md` — Phase 3+4: 设计文档与自检
- `references/workflow/phase5-tasks.md` — Phase 5: 实现计划
- `references/workflow/phase6-execution.md` — Phase 6: Ralph Loop 分发执行
- `references/workflow/phase7-archive.md` — Phase 7: 完成归档与流程复盘
- `references/workflow/phase8-feedback.md` — Phase 8: 反馈循环

### 🔌 集成
- `references/integration/hermes-pitfalls.md` — **Hermes 工具链陷阱**（从 Common Pitfalls 迁移）
- `references/integration/codewhale-acp-integration.md` — **CodeWhale ACP 集成**（Way A/B/C 详细规范）
- `references/integration/image-generation-api-notes.md` — **图片生成 API 调用笔记**（OpenRouter/Gemini/fal.ai 实测）
- `references/integration/stitch-mcp-workflow.md` — **Stitch MCP 集成**（连接、prompt、已知限制、替代方案）
- `references/integration/ui-prompt-frameworks.md` — **UI 设计 Prompt 框架**（RTCF/v0/Stitch/DESIGN.md）
- `references/integration/kanban-tasks-bridge.md` — Kanban bridge
- `references/integration/hermes-plugin-hooks-reference.md` — 插件 hook 能力边界
- `references/integration/hermes-plugin-zero-token.md` — 零令牌路由
- `references/integration/halo-auth.md` — Halo 认证
- `references/integration/reference-migration-pattern.md` — Reference 迁移模式
- `references/integration/fastify-url-port.md` — **Fastify URL/端口获取**（req.headers.host 正确用法）
- `references/workspace-sub-module-pattern.md` — **Workspace 子模块开发模式**（目录结构、双静态根、Hermes CLI 非交互式、Phase 8 多点反馈处理）

### ⚠️ 教训（流程违规案例）
- `references/pitfalls/violation-case-2026-05-15.md` — 跳步 + 自测
- `references/pitfalls/violation-case-2026-05-18.md` — Kanban 状态同步 + 角色分离
- `references/pitfalls/violation-case-2026-05-20.md` — Phase 8 灵犀直接写代码
- `references/pitfalls/phase8-context-management.md` — Phase 8 上下文管理

### 📂 项目专属（wiki）
- `wiki/projects/obsidian-workbench/references/pitfalls/` — ESM/CSS/Markdown/部署陷阱
- `wiki/projects/clsh-content/references/integration/` — Halo + Obsidian 参考

### 流程说明
各 Phase 详细流程见 `references/workflow/` 目录。
