---
name: clsh-project
description: "需求驱动的项目开发工作流 — 从需求澄清到设计文档到实现计划到执行。灵感来自 Kiro 的 Spec-Driven Development、Superpowers 的 Brainstorming 方法论、Phoenix 的状态机执行模式。"
version: 5.2.0
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
      # 模板（clsh-project 流程模板，保留本地）
      - references/templates/constitution-template.md
      - references/templates/archive-workflow.md
      - references/templates/cloud-server-wireguard.md
      - references/templates/phase7-archive-checklist.md
      - references/templates/phase8-checkpoint-template.md
      # 集成（clsh-project 工具链，保留本地）
      - references/integration/kanban-tasks-bridge.md
      - references/integration/hermes-slash-command-mechanism.md
      - references/integration/hermes-plugin-zero-token.md
      - references/integration/hermes-plugin-hooks-reference.md
      - references/integration/halo-auth.md
      - references/integration/halo-cli-auth.md
      - references/integration/reference-migration-pattern.md
      - references/integration/hermes-pitfalls.md
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

Phase 0 每次项目开始前内化历史教训；Phase 1 一次一个问题、多选优先、先理解目的再讨论细节。UI 项目可选 Visual Companion。含调研前置、提问模板、需求文档格式。

📋 **详细流程:** [references/workflow/phase0-1-requirements.md](references/workflow/phase0-1-requirements.md)

---

## Phase 2+2.5: 方案设计与技术验证

Phase 2 提出 2-3 个方案 + 推荐理由，用对比表格呈现。Phase 2.5 Spike 仅在技术不确定时触发，快速原型验证可行性。

📋 **详细流程:** [references/workflow/phase2-design.md](references/workflow/phase2-design.md)

---

## Phase 3+4: 设计文档与自检

Phase 3 写 proposal.md + constitution.md（含轻量版和完整版模板）。UI 项目**必做设计发散**（2-3 个 HTML mockup 变体，截图发飞书供大佬选择方向）。Phase 4 流程合规检查 + 文档质量自检 + 大佬 Review Gate + 自动路径验证。

📋 **详细流程:** [references/workflow/phase3-spec.md](references/workflow/phase3-spec.md)

---

## Phase 5: 实现计划

tasks.md 单文件 ≤3000 字，超出必须拆分。每个任务 = 一个 kanban 卡，粒度 2-5 分钟。No Placeholders + Type Consistency 必做。含文件依赖图、垂直切片策略、Self-Review 四项检查。

📋 **详细流程:** [references/workflow/phase5-tasks.md](references/workflow/phase5-tasks.md)

---

## Phase 6: Ralph Loop 分发执行

角色分配（coder/artist/tester）+ Ralph Loop 状态机 + Blocked 状态处理 + 任务派发 + Wave 并行 + 三层超时机制 + 执行红线。**新增：** UI 项目必做 Browser QA（浏览器自动化测试）、Pre-Commit 安全自检（代码提交前检查）。

📋 **详细流程:** [references/workflow/phase6-execution.md](references/workflow/phase6-execution.md)

---

## Phase 7: 完成归档与流程复盘

wiki 归档检查清单（必做）+ 归档 9 步 + 流程合规复盘 7 项 + 蒸馏评估。

📋 **详细流程:** [references/workflow/phase7-archive.md](references/workflow/phase7-archive.md)

---

## Phase 8: 反馈循环

执行规范（角色分离 + tester 浏览器验证 + 每轮归档）+ 上下文溢出防护（每轮 ≤3-4 bug）+ Diagnose 6 阶段 + Bugfix Spec + 路径 A/B/C + 反馈循环红线。

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

### 角色分离（铁律）
1. **禁止灵犀直接写代码** — 即使"很快能做完"也必须派 agent
2. **禁止 Phase 8 "顺手修了"** — 大佬反馈问题必须走完整反馈循环
**角色分离违规** — worker 卡住时不能自己动手，创建 fix 卡或 escalate
4. **Phase 8 必须走角色分离** — 小修复用 delegate_task，大修复用 kanban
5. **delegate_task 不是 kanban 的替代品（2026-05-24 教训，用户明确纠正）。** 用户要求走 kanban 时，不得用 `delegate_task` 替代。两者差异见 kanban-orchestrator skill。**判断规则：** 如果任务来自 clsh-project 流程或用户明确要求 kanban → 必须用 kanban。只有纯推理子任务（代码审查、调试分析、对比）才用 delegate_task。

### 流程完整性
5. **方向变化不回 Phase 1** — 核心定位变化必须回 Phase 1，不能回 Phase 3
6. **跳过 Phase 2.5 Spike** — 有技术不确定性的方案必须先验证
7. **Phase 5 缺少 Self-Review** — tasks.md 写完后必须 4 项自检
8. **Phase 6 不做 Spec-Code 同步** — 每个 Task 完成后更新 proposal.md
9. **Phase 7 归档不完整** — 必须检查 overview.md + completion-summary + retrospective + Phase 8 归档

### 质量保障
10. **agent 自判完成** — 必须通过 CHECKPOINT 客观验证
11. **Auto-Fix 无限循环** — 2 轮后必须 escalate 给大佬
12. **Placeholder 污染 tasks.md** — TBD/TODO/similar to N = 计划缺陷
13. **写入文件后不验证路径** — write_file 后必须 `ls` 确认
14. **UI 项目跳过 Browser QA** — 有前端 UI 的项目，tester 必须用浏览器自动化验证，不能只读代码
15. **Pre-Commit 自检缺失** — agent context 必须包含安全自检清单，不依赖 agent 自觉
16. **设计发散跳过** — UI 项目且无明确设计参考时，Phase 3 应触发设计发散，不能直接画页面
17. **html-anything 做复杂 UI mockup** — html-anything 通用模板效果差（扁平、缺乏层次感），只适合封面图/卡片。复杂 UI 必须用 Open Design 设计系统 tokens 生成
18. **飞书发送 HTML 文件路径** — 飞书无法打开 HTML 文件。必须用 chromium-browser 截图后发送 PNG 图片
19. **chromium 截图路径 /tmp** — snap 版 chromium 受 AppArmor 限制，无法写入 /tmp。截图路径用 /root/mockups/ 等非受限目录
20. **AGENTS.md 参考其他项目** — AGENTS.md 应基于本项目自身架构（architecture.md），不能照搬其他项目的文档结构
17. **发送 HTML 路径给大佬** — 飞书无法打开 HTML 文件路径，必须用 chromium-browser 截图后发送图片（MEDIA: 前缀）
18. **设计发散用错工具** — 不用 sketch skill（已归档），用 html-anything/Open Design 生成 HTML mockup
20. **UI 设计跳过调研** — 大佬无明确视觉偏好时，应先调研主流设计方向再生成 mockup
21. **通过 agent CLI 间接调自己** — Open Design 的 agent 调 hermes CLI = 冗余。直接读设计系统 tokens.css 渲染 HTML 即可，不需要绕一圈
22. **等外部 API 生成效果图** — Stitch API 长 prompt 通过代理容易超时。用 Open Design tokens 本地渲染更快更稳定

### 执行纪律
17. **超时后提交半成品** — 子 agent 超时后 git stash/revert
18. **Phase 8 上下文溢出** — 每轮最多修 3-4 个 bug，用 execute_code 批量读代码
19. **Bugfix Spec 不列出调用点** — Spec 说"修复 X 功能"但没列出所有函数/端点 → coder 只修一处漏其他。**正例：** Spec 列出 `createShare()`, `listShares()`, `findShareByPath()` 三个函数都需要传 baseUrl → coder 全部改完。**反例：** Spec 只说"修复 URL"→ coder 改了 createShare，漏了 listShares
20. **Fastify 获取端口用 req.server.config.port** — Fastify 没有这个属性。正确方式：`req.headers.host`（包含 host:port）或 `req.hostname`（仅 host）。集成场景（旧服务合并到新服务）必须用 `req.headers.host` 才能拿到正确端口
21. **代码分散在多个目录（2026-05-24 教训）** — 集成项目代码应集中在项目文件夹（如 `/opt/Workspace/src/projects/obsidian/`），不要分散在旧目录（如 `/opt/obsidian-workbench/src/`）。迁移步骤：(1) 备份旧目录 (2) 迁移到项目文件夹 (3) 更新导入路径为相对路径 (4) 删除旧目录 (5) 重启验证
22. **UI 状态管理条件判断错误（2026-05-24 教训）** — 条件 `(!loading && !error && !link)` 导致元素一闪而过。**根因：** 异步操作立即设置 `link`，条件瞬间变为 false。**修复方案：** 分离"显示条件"和"操作条件"——先显示 UI 元素（让用户选择），再在按钮点击后执行异步操作。**反例：** 点击分享按钮 → 立即创建分享 → link 有值 → 期限选择器消失。**正例：** 点击分享按钮 → 显示期限选择器 → 用户选择后点击"生成链接" → 创建分享

## Verification Checklist（每次使用此 skill 前）

- [ ] 确认不是简单查询/单步操作（否则不应触发 clsh-project）
- [ ] 确认 Phase 1 已执行调研前置（调研摘要已写入 conversation.md 或大佬明确跳过）
- [ ] 确认 Phase 1-3 已完成且有文档产出（conversation.md / proposal.md / constitution.md）
- [ ] 确认 UI 项目 Phase 3 是否需要设计发散（2-3 mockup 变体，截图发飞书）
- [ ] 确认大佬已明确回复"确认"才进入下一 Phase
- [ ] 确认 tasks.md 中每个 Task 有验收标准 + 完整代码（无 TBD/TODO）
- [ ] 确认代码任务已派给 coder/artist，不是灵犀直接写
- [ ] 确认每个 Task 有 tester 卡
- [ ] 确认 Phase 6 有 Security Scan 步骤
- [ ] 确认 UI 项目 Phase 6 tester 卡包含 Browser QA 检查清单
- [ ] 确认 agent 派发 context 包含 Pre-Commit 安全自检清单
- [ ] 确认 Phase 8 反馈走流程而非"顺手修了"
- [ ] 确认 Auto-Fix 不超过 2 轮后 escalate
- [ ] 确认每个 kanban task body 包含 proposal 相关章节 + constitution 约束 + 不在范围内声明

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
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

### 📋 模板
- `references/templates/constitution-template.md` — Constitution 模板
- `references/templates/archive-workflow.md` — Phase 7 归档操作手册
- `references/templates/phase7-archive-checklist.md` — 归档快速检查清单

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
- `references/integration/image-generation-api-notes.md` — **图片生成 API 调用笔记**（OpenRouter/Gemini/fal.ai 实测）
- `references/integration/stitch-mcp-workflow.md` — **Stitch MCP 集成**（连接、prompt、已知限制、替代方案）
- `references/integration/ui-prompt-frameworks.md` — **UI 设计 Prompt 框架**（RTCF/v0/Stitch/DESIGN.md）
- `references/integration/kanban-tasks-bridge.md` — Kanban bridge
- `references/integration/hermes-plugin-hooks-reference.md` — 插件 hook 能力边界
- `references/integration/hermes-plugin-zero-token.md` — 零令牌路由
- `references/integration/halo-auth.md` — Halo 认证
- `references/integration/reference-migration-pattern.md` — Reference 迁移模式
- `references/integration/fastify-url-port.md` — **Fastify URL/端口获取**（req.headers.host 正确用法）

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
