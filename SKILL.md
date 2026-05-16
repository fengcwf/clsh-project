---
name: clsh-project
description: "需求驱动的项目开发工作流 — 从需求澄清到设计文档到实现计划到执行。灵感来自 Kiro 的 Spec-Driven Development、Superpowers 的 Brainstorming 方法论、Phoenix 的状态机执行模式。"
version: 2.4.0
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
    references:
      - references/methodology/ralph-loop-analysis.md
      - references/methodology/openspec-comparison.md
      - references/methodology/kiro-superpowers-analysis.md
      - references/methodology/agent-skill-execution-research.md
      - references/methodology/superpowers-v5-changes.md
      - references/templates/constitution-template.md
      - references/integration/kanban-tasks-bridge.md
      - references/integration/github-sync-guide.md
      - references/integration/lucky-api-format.md
      - references/integration/php-env-pattern.md
      - references/pitfalls/violation-case-2026-05-15.md
      - references/pitfalls/violation-case-2026-05-15-self-coding.md
---

# /clsh-project — 需求驱动项目开发

## 概述

当大佬提出新的项目或功能需求时，**不直接写代码**，而是走完整的 需求→设计→计划→执行 流程。

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

1. **文档先于代码** — Phase 3（设计文档）未完成 + 大佬未确认，禁止写任何代码
2. **分阶段审批** — 每个 Phase 必须有大佬确认输出才能进入下一 Phase
3. **独立测试** — 代码任务必须有 tester review 卡，禁止自己测自己验收
4. **角色分离** — 灵犀是协调者，不直接改代码。后端→coder，前端逻辑→coder，UI/样式→artist，测试→tester。**效率不是跳过角色分离的理由**。
5. **流程合规自检** — Phase 4 自检必须包含流程合规检查
6. **文档写入路径验证** — 文档必须写入 `wiki/projects/<项目名>/changes/<变更名>/` 目录，写入后必须 `ls` 验证
7. **反馈走流程** — 大佬测试反馈问题后，走 Phase 8 反馈循环，禁止"顺手修了"
8. **Checkpoint 机制** — 每个 Task 执行后必须输出 checkpoint（产出物验证），未通过验证不得进入下一 Task
9. **安全扫描** — Phase 6 每个 Task 的 review 必须包含安全扫描（硬编码密钥、SQL 注入、shell 注入等）
10. **Auto-Fix 上限** — review 发现问题后派 fix agent 修复并重新 review，最多 2 轮后 escalate 给大佬

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
Phase 1: 需求澄清（一次一个问题，多选优先；UI项目可选 Visual Companion）→ conversation.md
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

---

## Phase 1: 需求澄清

**目标：** 理解大佬真正想要什么，发现大佬没想到的需求点。

### 规则
- **一次只问一个问题** — 不要一次抛出 5 个问题
- **多选题优先** — 比如"这个通知方式你倾向哪种？A.飞书 B.邮件 C.短信 D.都要"
- **先理解目的，再讨论细节** — 问"这个功能主要解决什么问题？"而不是"数据库用什么字段？"
- **主动提出大佬没想到的需求**
- **如果需求太大，先帮助拆分子项目"

### 🎨 Visual Companion（UI/视觉项目专用）

**触发条件：** Phase 1 涉及视觉/UI 问题（布局、交互流程、页面结构）时，在提出第一个视觉相关问题前提供。

**模板：**
> "这个项目涉及 UI/视觉设计。我可以启动一个 Visual Companion 帮助你：
> - 启动本地 HTML 页面展示设计方案
> - 实时对比不同布局/交互方案
> - 你可以直接在浏览器中点击反馈
> 
> 需要吗？（默认：否）"

**执行方式：**
- 大佬同意 → 使用 `sketch` skill（`references/../creative/sketch/SKILL.md`）生成 2-3 个 HTML 设计方案
- 启动本地 HTTP 服务（`python3 -m http.server`），在浏览器中展示
- 大佬在浏览器中查看并反馈，灵犀根据反馈调整方案
- 完成后关闭服务

**⚠️ 注意：** 仅用于视觉/UI 讨论。纯后端/API 项目不需要。

### 提问模板（按顺序探索）

1. **目的和用户** — "这个功能主要是给谁用的？解决什么问题？"
2. **核心功能** — "核心要做什么？最小可用版本包含哪些功能？"
3. **输入输出** — "用户输入什么？系统输出什么？"
4. **边界条件** — "异常情况怎么处理？"
5. **非功能需求** — "性能要求？安全要求？需要兼容什么环境？"
6. **优先级** — "如果时间紧，哪些功能可以后做？"

### 需求文档格式

**文件位置：** `wiki/projects/<项目名>/changes/YYYY-MM-DD-<变更名>/conversation.md`

---

## Phase 2: 方案设计

**目标：** 提出多个技术方案，让大佬做选择题。

### 规则
- **提出 2-3 个方案** — 不要只给一个"推荐方案"
- **每个方案说清楚：** 优点、缺点、工作量估算
- **给出推荐理由**
- **用对比表格呈现**

### ⛔ 技术不确定性检查

如果方案中存在以下情况，**必须进入 Phase 2.5 Spike**，不可直接跳到 Phase 3：
- 使用从未在项目中用过的框架/协议/库
- 性能要求可能无法满足（需要基准测试验证）
- 多方案技术路线差异大，无法凭经验判断
- 依赖第三方服务的稳定性/兼容性未知

---

## Phase 2.5: Technical Spike（可选）

**目标：** 在写设计文档前验证技术可行性，降低设计返工风险。

**参考：** `spike` skill

### 何时触发（满足任一）
- Phase 2 的方案存在技术不确定性
- 新框架/新协议首次引入
- 性能/兼容性需要实际验证
- 大佬明确要求"先确认能不能做"

### 流程

```
1. 分解为 2-5 个独立可行性问题（Given/When/Then 格式）
2. 按风险排序，最高风险的 spike 先做
3. 每个 spike：研究 → 快速原型 → 裁决
4. 输出：VALIDATED / PARTIAL / INVALIDATED
5. 更新 Phase 2 方案
```

### 裁决格式

```markdown
## Verdict: VALIDATED | PARTIAL | INVALIDATED

### What worked
- ...

### What didn't
- ...

### Surprises
- ...

### Recommendation for the real build
- ...
```

**文件位置：** `wiki/projects/<项目名>/changes/<变更名>/spikes/NNN-question/`

### ⛔ Spike 铁律
- **快速原型 ≠ 生产代码** — spike 代码写完就扔，不要"顺手合并"
- **每个 spike 独立目录** — 不互相干扰
- **有 PARTIAL 或 INVALIDATED 时** — 必须更新方案，不能假装没看到

---

## Phase 3: 写设计文档 + Constitution

**目标：** 将需求和选定方案转化为详细的技术设计文档。

### 文件位置

```
wiki/projects/<项目名>/
├── overview.md
├── source-of-truth/
│   ├── constitution.md
│   └── <capability>.md
└── changes/
    └── YYYY-MM-DD-<变更名>/
        ├── proposal.md
        ├── conversation.md
        ├── spikes/          ← Phase 2.5 产出
        └── tasks.md
```

### 创建 Constitution（Phase 3 必做）

Constitution 是项目级的"宪法"，定义 AI worker 必须遵守的技术约束。

**轻量版（小项目）：**
```markdown
---
title: "[项目名] 项目约束"
date: YYYY-MM-DD
type: constitution
project: "[项目名]"
---

# [项目名] 项目约束

- **技术栈：** [一句话描述]
- **代码规范：** [关键规则]
- **架构：** [核心约束]
- **禁止：** [最重要的 2-3 条]
```

**完整版模板：** 见 `references/templates/constitution-template.md`

---

## Phase 4: 设计文档自检 + 大佬 Review

### ⛔ 流程合规检查

1. Phase 1 是否完成？
2. Phase 2 是否完成？
3. Phase 2.5（如触发）是否完成？
4. Phase 3 是否完成？
5. 是否有跳步？
6. 代码是否已提前编写？

**如果以上任何一项为 NO → 停止，补全缺失的 Phase。**

### 文档质量自检

1. **Placeholder 扫描** — 有无 "TBD"、"TODO"、"implement later"？
2. **内部一致性** — 各章节是否矛盾？架构与功能描述是否匹配？
3. **范围检查** — 是否过大需要拆分？
4. **歧义检查** — 是否有需求可被两种解读？
5. **需求覆盖** — Phase 1 的每个需求是否都有对应设计？
6. **Type Consistency** — 跨章节的类型/接口/命名是否一致？

### 大佬 Review Gate

自检通过后，向大佬确认：

> "设计文档已写入 `wiki/projects/<项目名>/changes/<变更名>/`，请 review。确认无误后我开始写实现计划。"

**等待大佬确认后才进入 Phase 5。**

---

## Phase 5: 写实现计划

**文件位置：** `wiki/projects/<项目名>/changes/YYYY-MM-DD-<变更名>/tasks.md`

**参考：** `plan` skill（前身 writing-plans）

### 关键原则
- **每个任务 = 一个 kanban 卡**
- **任务粒度：2-5 分钟**（一个任务 = 一个动作：写测试/运行/实现/提交）
- **包含完整代码片段**（可复制粘贴到文件中）
- **包含精确文件路径**（`exact/path/to/file.py:123-145`）
- **包含验证步骤**（精确命令 + 预期输出）
- **标注依赖关系**（哪些任务必须等别的任务完成）
- **标注完整的测试代码**（不是"写个测试"，而是实际测试代码）

### ⛔ Superpowers v5 — No Placeholders

以下写法 = **计划缺陷**，必须修复：

| ❌ 错误 | ✅ 正确 |
|---------|---------|
| "TBD"、"TODO"、"稍后实现" | 写实际代码 |
| "添加错误处理" | 写具体的 try/catch 代码 |
| "类似 Task 3" | 复制实际代码（开发者可能跳读） |
| "写测试覆盖上述" | 写实际测试代码 |
| "填充详情" | 直接写详情 |

### ⛔ Superpowers v5 — Type Consistency

写完全部任务后，检查跨任务一致性：
- Task 3 定义的函数签名，Task 5/7 调用时是否匹配？
- 类型定义（interface/type/class）前后是否一致？
- 命名风格是否统一？

### Superpowers v5 — Self-Review

写完全部任务后执行：
1. **Spec Coverage** — 逐条扫描 spec 需求，确认每个需求都有对应任务。列出遗漏。
2. **Placeholder Scan** — 搜索 No Placeholders 表中的模式，全部修复。
3. **Type Consistency** — 跨任务检查签名一致性。
4. **File Isolation** — 是否有任务修改了相同的文件？（如果有，确认顺序和依赖关系已标注）

### 📋 文件依赖图

在 tasks.md 开头标注任务间依赖，确保无冲突的并行执行：

```
# [功能名] 实现计划

## 依赖图
Task 1: 创建数据模型（无依赖）
Task 2: 创建 API 层（依赖 Task 1）
Task 3: 创建 UI 组件（依赖 Task 2）
Task 4: 集成测试（依赖 Task 1, 2, 3）

依赖图:
Task 1 → Task 2 → Task 3
  ↓              ↓
  └──── Task 4 ←─┘

可并行: 无（线性依赖）
```

**规则：**
- 有依赖的任务必须等父任务完成
- 无依赖的任务可并行派发
- 修改同一文件的任务必须串行，且依赖关系明确

### 📋 垂直切片策略（incremental-build）

**参考：** `incremental-build` skill

将功能拆分为可独立交付的端到端切片，每个切片完成后系统处于可工作状态。

**三种切片策略：**

| 策略 | 适用场景 | 示例 |
|------|---------|------|
| **垂直切片**（推荐） | 完整功能路径 | 切片1: 创建任务(DB+API+UI) → 切片2: 列表任务 → 切片3: 编辑任务 |
| **契约优先** | 前后端并行开发 | 切片0: API契约 → 切片1a: 后端 + 切片1b: 前端(并行) → 切片2: 集成 |
| **风险优先** | 技术不确定性高 | 切片1: 验证最风险的技术点 → 切片2: 核心功能 → 切片3: 增强功能 |

**垂直切片模板：**
```
Slice 1: 创建任务（DB + API + 基础UI）
  验证: 测试通过，用户可通过 UI 创建任务
Slice 2: 列表任务（查询 + API + UI）
  验证: 测试通过，用户可看到任务列表
Slice 3: 编辑任务（更新 + API + UI）
  验证: 测试通过，用户可修改任务
Slice 4: 删除任务（删除 + API + 确认UI）
  验证: 测试通过，完整 CRUD
```

**切片原则：**
- 每个切片 = 一个可独立验证的端到端功能
- 切片完成后**立即 commit**，不攒到最后
- 未完成的功能用**功能标志**隐藏（`FEATURE_NEW_UI=false`）
- 每个切片可独立回滚（`git revert`）

---

## Phase 6: Ralph Loop 分发执行

### ⚠️ 角色分配规则（不可违反）

| 任务类型 | 必须派给 | 灵犀能做吗 |
|---------|---------|-----------|
| 后端 API | coder | ❌ |
| 前端逻辑 | coder | ❌ |
| UI 模板 | artist | ❌ |
| CSS 样式 | artist | ❌ |
| 测试验证 | tester | ❌ |
| 文档编写 | 灵犀 | ✅ |
| 协调汇报 | 灵犀 | ✅ |

### ⚠️ Ralph Loop 执行模式（核心）

**参考：** `references/methodology/ralph-loop-analysis.md`

**核心原则：**
- 灵犀是循环编排者，agent 是单步执行器
- 每轮通过 CHECKPOINT 客观验证，不依赖 agent 自判
- 失败反馈注入重试，最多 2 轮后 escalate 给大佬
- 文件系统 + git 作为记忆层（不是 agent 的上下文）

每个 Task 必须按以下状态机执行：

```
Task 开始
  ↓
Step 1: agent 读取任务描述 + constitution
  ↓
Step 2: agent 执行任务（TDD：先写失败测试 → 实现 → 通过测试）
  ↓
Step 3: 输出 CHECKPOINT（产出物自检）
  ↓
Step 4: 灵犀验证 checkpoint
  ├─ FAIL → 返回 Step 2（重试），最多 2 轮 → 仍 FAIL → 派 fix agent
  └─ PASS ↓
  ↓
Step 5: Security Scan（安全扫描）
  硬编码密钥、SQL 注入、shell 注入、eval/pickle、路径遍历
  ├─ 有问题 → 派 fix agent → 重新 Step 5（最多 2 轮）
  └─ PASS ↓
  ↓
Step 6: Quality Review（代码质量）
  命名、DRY、错误处理、测试覆盖
  ├─ 有问题 → 派 fix agent → 重新 Step 6（最多 2 轮）
  └─ PASS ↓
  ↓
Step 7: Tester 验证（功能测试 + 回归测试）
  ↓
Step 8: CHECKPOINT: PASS → 标记 Task 完成 → 进入下一 Task
```

**Checkpoint 格式（每个 Task 完成后必须输出）：**

```
CHECKPOINT: <任务名称>
产出物: <文件路径/内容摘要>
自检: <是否满足验收标准>
状态: PASS / FAIL
如 FAIL: <具体问题描述>
```

### 任务派发流程

```python
对于计划中的每个 Task:
  1. 读取 constitution.md
  2. 根据任务类型选择 agent（coder/artist/tester）
  3. delegate_task 派发（context 中包含验收标准 + TDD 要求）
  4. agent 完成后，灵犀验证 checkpoint
  5. PASS → Security Scan + Quality Review
  6. 有问题 → fix agent（不是实现者本人）→ 重新 review（max 2轮）
  7. 全部通过 → tester 验证
  8. tester 通过 → 标记 Task 完成
  9. 全部 Task 完成 → Final Integration Review
```

### ⛔ 执行红线

- **禁止灵犀直接写代码** — 即使"很快能做完"也必须派
- **禁止跳过 checkpoint** — 每个 Task 必须有产出物验证
- **禁止自己测自己写的代码**
- **禁止跳过 tester 卡**
- **禁止在 Phase 4 确认前开始编码**
- **禁止跳过 artist 做 UI**
- **禁止跳过 Security Scan** — 即使"代码很简单"
- **禁止 fix agent 超过 2 轮** — 2 轮后必须 escalate 给大佬
- **禁止 agent 自判完成** — 必须通过客观验证

---

## Phase 7: 完成归档 + 流程复盘

### 归档步骤

1. 更新提案状态 → `status: done`
2. 归档变更 → `changes/<变更名>/` → `changes/archive/`
3. 更新 Source of Truth
4. 写入完成摘要
5. 同步 wiki + GitHub（见 `references/integration/github-sync-guide.md`）
6. 向大佬汇报

### ⛔ 流程合规复盘（必做）

1. 是否有跳步？
2. 是否有提前编码？
3. 是否有自测自验？
4. 文档是否前置？
5. Security Scan 是否执行？
6. Auto-Fix 是否超过 2 轮？
7. 改进措施

**复盘结果写入** `retrospective.md`

---

## Phase 8: 反馈循环（大佬测试后）

**触发条件：** 大佬测试后反馈问题

### ⚠️ Diagnose 6 阶段循环

**参考：** `diagnose` skill

每个阶段有明确入口/出口条件。不满足出口条件不能进入下一阶段。

```
Stage 1: 建循环（Build the Loop）
  入口：大佬反馈了 bug/异常
  操作：固化复现命令（单命令 pass/fail）
  出口：有一键复现命令，输出明确 pass/fail 信号
  ↓
Stage 2: 复现（Reproduce）
  入口：复现命令已建立
  操作：运行 3 次确认稳定性
  出口：稳定复现 或 确认非确定性（统计复现率）
  ↓
Stage 3: 假设（Hypothesize）
  入口：问题已稳定复现
  操作：读完整错误 → 查 git log → 追踪数据流 → 形成具体假设
  出口："我认为 X 是 root cause，因为 Y，如果做 Z 应能观察到 W"
  ↓
Stage 4: 插桩（Instrument）
  入口：有具体假设
  操作：选最快反馈方法（类型检查<1s → 单测1-5s → 断点5-30s → 集成测试）
  出口：有证据支持或否定假设
  ↓
Stage 5: 修复（Fix）
  入口：证据确认 root cause
  操作：先写回归测试（FAIL → 修复 → PASS → 全量测试无回归）
  出口：回归测试通过，全量套件无回归
  Rule of Three：第3次修复失败 → 停止，质疑架构
  ↓
Stage 6: 复盘（Retrospect）
  入口：bug 已修复
  操作：为什么这个 bug 存在？防御措施？清理插桩？记录教训？
  出口：防御措施已添加/已评估不需要
```

**非确定性 bug 时**：Stage 2 → 统计复现（跑 N 次算失败率），Stage 4 → 用断言而非 print（失败立即停止，不被日志淹没）。

### 路径 A：Bug 修复
```
大佬反馈 bug
  → 记录 conversation.md
  → diagnose 6 阶段（Stage 1-6）
  → 创建修复任务 → 派 coder/artist
  → tester 验证 → 汇报
```

### 路径 B：体验优化
```
大佬反馈体验问题
  → 记录 conversation.md
  → 评估影响范围
  → 创建优化任务 → 派 artist
  → tester 验证 → 汇报
```

### 路径 C：新需求
```
大佬提出新需求
  → 评估范围（能否追加到当前变更？）
  → 能追加：更新 proposal.md，回到 Phase 3
  → 不能追加：新变更目录，从 Phase 1 开始
```

### ⛔ 反馈循环红线
- **禁止"顺手修了"**
- **禁止跳过 tester**
- **禁止不记录就修**
- **禁止跳过 diagnose 的 Stage 1-2**（不复现就修 = 瞎猜）

> ⚠️ **教训（2026-05-15）：** 大佬说"测试有问题"，灵犀直接自己修复了，跳过了 Phase 8 的全部流程。

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

## 快捷方式

如果大佬说"简单做一下"，可以跳过 Phase 2（方案对比）。但 Phase 1 和 Phase 3 不能跳过。

Phase 2.5 Spike 是可选的，仅在技术不确定时触发。

## Common Pitfalls

1. **灵犀直接写代码** — 即使"很快能做完"也必须派 agent（详见 `references/pitfalls/violation-case-2026-05-15-self-coding.md`）
2. **跳过 Phase 2.5 Spike** — 有技术不确定性的方案必须先验证再写设计文档
3. **Phase 6 没有安全扫描** — 每个 Task 的 review 必须包含安全扫描
4. **tester 只做功能测试** — tester 应运行完整的 requesting-code-review 流水线
5. **攒到最后一起提交** — 每个 Task 后必须 commit
6. **Phase 8 "顺手修了"** — 大佬反馈问题必须走完整反馈循环
7. **agent 自判完成** — 必须通过 CHECKPOINT 客观验证
8. **Auto-Fix 无限循环** — 2 轮后必须 escalate 给大佬
9. **Placeholder 污染 tasks.md** — TBD/TODO/similar to N = 计划缺陷
10. **忽略 Type Consistency** — 跨任务的函数签名/类型必须一致

## Verification Checklist（每次使用此 skill 前）

- [ ] 确认不是简单查询/单步操作（否则不应触发 clsh-project）
- [ ] 确认 Phase 1-3 已完成且有文档产出（conversation.md / proposal.md / constitution.md）
- [ ] 确认大佬已明确回复"确认"才进入下一 Phase
- [ ] 确认 tasks.md 中每个 Task 有验收标准 + 完整代码（无 TBD/TODO）
- [ ] 确认代码任务已派给 coder/artist，不是灵犀直接写
- [ ] 确认每个 Task 有 tester 卡
- [ ] 确认 Phase 6 有 Security Scan 步骤
- [ ] 确认 Phase 8 反馈走流程而非"顺手修了"
- [ ] 确认 Auto-Fix 不超过 2 轮后 escalate

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.4.0 | 2026-05-16 | P0-P3 全面优化：Security Scan/Auto-Fix Loop/Phase 2.5 Spike/Visual Companion/Common Pitfalls/Verification Checklist/垂直切片策略/Ralph Loop 显式原则 |
| v2.3.0 | 2026-05-15 | 铁律 8 条 + Phase 6 状态机 + Phase 8 反馈循环 |
| v2.2.0 | 2026-05-13 | Kanban bridge + tasks.md 回写 |
| v2.1.0 | 2026-05-12 | Constitution 模板 + Phase 4 自检 |
| v2.0.0 | 2026-05-11 | 初始版本：需求→设计→计划→执行 4 阶段 |

## 参考文件

### 📐 方法论
- `references/methodology/kiro-superpowers-analysis.md` — Kiro + Superpowers + Phoenix 工作流分析
- `references/methodology/ralph-loop-analysis.md` — Ralph Loop 调研：原理 + 与 Phase 6 映射
- `references/methodology/openspec-comparison.md` — OpenSpec 对比分析
- `references/methodology/agent-skill-execution-research.md` — Agent Skill 执行跑偏问题：根因分析 + 5种解决方案
- `references/methodology/superpowers-v5-changes.md` — Superpowers v5 关键变更及对 clsh-project 的影响

### 📋 模板
- `references/templates/constitution-template.md` — Constitution 模板（Phase 3 使用）

### 🔌 集成
- `references/integration/kanban-tasks-bridge.md` — Kanban bridge 说明
- `references/integration/github-sync-guide.md` — GitHub 同步指南（仓库地址 + 推送命令）
- `references/integration/lucky-api-format.md` — Lucky API 格式
- `references/integration/php-env-pattern.md` — PHP 环境模式

### ⚠️ 教训
- `references/pitfalls/violation-case-2026-05-15.md` — 流程违规案例：跳步 + 自测
- `references/pitfalls/violation-case-2026-05-15-self-coding.md` — 灵犀直接写代码违规案例

## 流程说明

详见 `README.md`（skill 根目录）— 包含流程总览、各 Phase 详解、速查表、版本历史。
