---
name: clsh-project
description: "需求驱动的项目开发工作流 — 从需求澄清到设计文档到实现计划到执行。灵感来自 Kiro 的 Spec-Driven Development、Superpowers 的 Brainstorming 方法论、Phoenix 的状态机执行模式。"
version: 3.2.0
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
      - references/integration/hermes-slash-command-mechanism.md
      - references/integration/hermes-plugin-zero-token.md
      - references/pitfalls/violation-case-2026-05-15.md
      - references/pitfalls/violation-case-2026-05-15-self-coding.md
      - references/pitfalls/violation-case-2026-05-18.md
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

### 🔄 Phase 中断恢复（Restart Protocol）

如果 session 中断后重启（如新会话、网关重启等），**不要从头开始 Phase 1**，而是：

1. `session_search` 搜索最近 3 个 session，关键词用项目名
2. 读取历史 session 的 summary，恢复上下文
3. 检查 `wiki/projects/<项目名>/` 是否已有文档产出
4. 从上次中断的 Phase 继续，**不要重复已完成的工作**
5. 向大佬确认恢复的上下文是否正确，再继续提问

### 🔍 调研前置（Phase 1 必问）

在开始提问之前，先问大佬是否需要调研：

> "在讨论需求之前，要不要我先调研一下类似项目的常见做法、行业方案或技术趋势？这样讨论时能有更多参考依据。（默认：是）"

- **大佬说"是"或"需要"** → 用 `web_search` 调研 2-3 个类似项目/产品，总结关键发现和启示，再开始 Phase 1 提问
- **大佬说"不用"或"直接聊"** → 跳过调研，直接进入提问模板
- **大佬未明确回答** → 默认执行调研（主动权在灵犀）

**调研输出格式：**
```markdown
## 调研摘要
- 调研方向：[类似产品/技术方案/行业实践]
- 关键发现：[3-5 条]
- 对本项目启示：[2-3 条]
```

调研结果写入 `conversation.md` 顶部，作为需求讨论的参考上下文。

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

### 🔍 自动路径检查（Q1 改进 — 2026-05-19）

**每次写入文件后，必须执行路径验证：**

```bash
# 写入文件后立即验证
ls -la <声明路径>
# 确认文件存在且大小 > 0
```

**Phase 3 写入验证清单：**
- [ ] `proposal.md` 已写入 `wiki/projects/<项目名>/changes/<变更名>/` → `ls` 验证
- [ ] `constitution.md` 已写入 `wiki/projects/<项目名>/source-of-truth/` → `ls` 验证
- [ ] 文件大小 > 0（非空文件）

**Phase 6 产出物验证清单：**
- [ ] 代码文件已写入声明的绝对路径 → `ls` 验证
- [ ] 测试文件已写入 → `ls` 验证
- [ ] 产出物路径使用绝对路径（禁止相对路径）

**⛔ 路径错误 = 流程违规，必须记 ERRORS.md**

> ⚠️ **教训（2026-05-15）：** write_file 使用相对路径，文件落到 skill references/ 目录而不是 wiki/projects/ 目录。写入后未 `ls` 验证，导致虚假汇报。

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

### 🔍 Phase 5 Self-Review（Superpowers v5 — 必做）

写完全部 tasks.md 后，执行以下自检，**全部通过才能进入 Phase 6**：

**1. Spec Coverage（需求覆盖）**
- 逐条扫描 Phase 1 conversation.md 中的每个需求
- 确认每个需求都有对应的 Task
- 遗漏 → 补充 Task，不能"后面再说"

**2. Placeholder Scan（占位符扫描）**
搜索 tasks.md 中的以下模式，**全部修复**：
| ❌ 错误模式 | ✅ 修复方式 |
|------------|------------|
| `TBD`、`TODO`、`稍后实现` | 写实际代码 |
| `添加错误处理` | 写具体的 try/catch |
| `类似 Task N` | 复制实际代码 |
| `写测试覆盖上述` | 写实际测试代码 |
| `填充详情` | 直接写详情 |

**3. Type Consistency（类型一致性）**
- Task 3 定义的函数签名，Task 5/7 调用时是否匹配？
- 类型定义（interface/type/class）前后是否一致？
- 命名风格是否统一？

**4. File Isolation（文件隔离）**
- 是否有多个 Task 修改同一文件？
- 如果有，确认顺序和依赖关系已标注

**Self-Review 结果写入 tasks.md 末尾：**
```markdown
## Self-Review 结果
- Spec Coverage: ✅/❌ (N 个需求全部覆盖 / 遗漏: xxx)
- Placeholder Scan: ✅/❌ (无占位符 / 发现: xxx)
- Type Consistency: ✅/❌
- File Isolation: ✅/❌
```

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
  ↓
Step 9: Spec-Code 同步（Kiro — 必做）
  检查 proposal.md 中的设计是否与实际代码一致：
  - 读取 proposal.md 中该 Task 对应的设计描述
  - 对比实际代码实现
  - 如有偏差 → 更新 proposal.md（不是"后面再补"）
  - 更新内容：接口变更、架构调整、新增/删除的功能点
```

**Checkpoint 格式（每个 Task 完成后必须输出）：**

```
CHECKPOINT: <任务名称>
产出物: <文件路径/内容摘要>
自检: <是否满足验收标准>
状态: PASS / FAIL
如 FAIL: <具体问题描述>
```

**⚠️ Checkpoint 输出截断规则（Q2 改进 #4）：**
- Checkpoint 输出限制在 **200 字以内**
- 编译日志、测试输出等长文本 → 写入 `/tmp/<project>-<task>.log`，Checkpoint 只写文件路径
- 禁止将完整编译输出/测试日志直接输出到上下文
- 原因：一个 Task 的往返可能消耗 2000-5000 token，截断可节省 50-80%

### 任务派发流程

```python
对于计划中的每个 Task:
  1. 读取 constitution.md
  2. 根据任务类型选择 agent（coder/artist/tester）
  3. kanban_create 创建实现卡（绝对路径 + 验收标准 + 不在范围内）
  4. kanban_create 创建 review 卡（assignee=tester, parents=[实现卡]）
  5. 通知订阅（可选，当前 notify-subscribe 命令可能返回空）
  6. dispatcher 自动派发 ready 状态的卡
  7. 灵犀验证 checkpoint（产出物 ls 验证）
  8. PASS → Security Scan + Quality Review（由 tester 执行）
  9. 有问题 → 创建 fix 卡（不是实现者本人）→ 重新 review（max 2轮）
  10. tester 通过 → 标记 Task 完成
  11. 全部 Task 完成 → Final Integration Review
```

### ⚡ Phase 6 执行规范（2026-05-18 验证）

**Kanban 创建必须使用绝对路径：**
- 产出物路径：`~/.hermes/skills/productivity/<project>/scripts/xxx.cjs`
- 报告路径：`/mnt/unraid_data/Obsidian/wiki/projects/<项目名>/changes/<变更名>/`
- 测试输出：`/tmp/<project>-test/`

**Review 卡创建规范：**
```bash
hermes kanban create "[项目名] Review: <任务名>" \
  --assignee tester \
  --body "...审查维度...\nPASS/FAIL 输出要求..." \
  --parent <实现卡ID> \
  --json
```
- Review 卡依赖实现卡（parents），实现卡完成后自动 promoted → ready
- Review 卡 body 必须包含：审查维度 + PASS/FAIL 输出格式 + 上下文（实现卡ID）

**并行派发策略：**
- 无依赖的任务同时创建 Kanban 卡
- Review 卡与实现卡同时创建（通过 parents 依赖）
- dispatcher 自动并行执行 ready 状态的任务

**进展监控：**
```bash
hermes kanban list --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for t in data:
    if '项目名' in t.get('title',''):
        print(f\"{t['id']} | {t['status']} | {t['title'][:60]}\")
"
```

### ⚡ Phase 6 超时机制（Q5 方案 C — 2026-05-19 实施）

**三层防护：子 agent 自带超时 + 产出物预检 + 灵犀 5 分钟轮询**

#### 第 1 层：子 agent 自带超时
派活时在 delegate_task 的 context 中写明：
```
## 超时规则
- 本任务必须在 N 分钟内完成（coder: 10分钟, worker: 5分钟, tester: 5分钟）
- 超时则输出 TIMEOUT 并退出，不要继续尝试
- 产出物写到 /tmp/<project>-<task>/ 目录
```

#### 第 2 层：产出物预检
- agent 开始工作前先创建产出物目录：`mkdir -p /tmp/<project>-<task>/`
- 灵犀通过 `ls /tmp/<project>-<task>/` 判断 agent 是否在工作
- **5 分钟内产出物目录无任何变化 → 判定为卡死**，不再等待

#### 第 3 层：灵犀 5 分钟轮询
Phase 6 执行过程中，灵犀每 5 分钟检查一次：
```bash
hermes kanban list --json | python3 -c "
import json, sys, time
data = json.load(sys.stdin)
now = time.time()
for t in data:
    if t['status'] == 'running' and '项目名' in t.get('title',''):
        started = t.get('started_at', 0)
        elapsed = (now - started) / 60
        print(f\"{t['id']} | {elapsed:.0f}min | {t['assignee']} | {t['title'][:50]}\")
"
```
- running 超过 5 分钟 → 检查产出物目录
- 产出物存在 → `hermes kanban complete <id>` 手动标记完成
- 产出物不存在 → 执行超时自动回滚（Phoenix）→ escalate 给大佬

#### 超时自动回滚（Phoenix — 2026-05-19 实施）

子 agent 超时/卡死后，灵犀执行以下回滚流程：

```bash
# 1. 检查未提交的改动
cd <项目目录>
git diff --stat
git status --short

# 2. 如果有未提交的改动 → stash（不直接提交半成品）
git stash save "auto-rollback: <task-name> timeout at $(date +%Y%m%d-%H%M)"

# 3. 如果有未 stash 的改动 → 记录到日志
echo "TIMEOUT_ROLLBACK: <task-name> | $(date) | $(git diff --stat)" >> /tmp/<project>-timeout.log

# 4. 通知大佬
# 发送飞书告警：任务超时 + 已自动回滚 + 需要人工介入
```

**回滚原则：**
- ⛔ 禁止直接提交半成品代码
- ✅ 未提交改动 → `git stash`，保留现场供大佬检查
- ✅ 已提交改动 → `git revert <commit>`，回滚到超时前状态
- ✅ 回滚后通知大佬，不自行重试

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

### 路径 C：需求变更
大佬提出新需求/方向变化
  → 判断变更级别：
     ├─ 功能追加（在现有方向上增加功能）
     │   → 能追加：更新 proposal.md，回到 Phase 3
     │   → 不能追加：新变更目录，从 Phase 1 开始
     │
     └─ 方向变化（核心定位/架构/目标用户变化）
         → ⛔ 禁止回到 Phase 3
         → 必须：新变更目录 + 从 Phase 1 开始
         → 必须：归档旧变更（status: superseded）
         → 必须：更新 overview.md 说明方向变化
         → 必须：更新 conversation.md 记录变更原因

> ⚠️ **教训（2026-05-19）：** 项目做到一半，大佬说"不做博客了，改做内容引擎"。灵犀直接在旧代码上修改，跳过 Phase 1-5，导致项目文档和实际代码不一致。**方向变化 = 必须回 Phase 1，不能回 Phase 3。**

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

1. **灵犀直接写代码** — 即使"很快能做完"也必须派 agent
2. **跳过 Phase 2.5 Spike** — 有技术不确定性的方案必须先验证再写设计文档
3. **Phase 6 没有安全扫描** — 每个 Task 的 review 必须包含安全扫描
4. **tester 只做功能测试** — tester 应运行完整的 requesting-code-review 流水线
5. **攒到最后一起提交** — 每个 Task 后必须 commit
6. **Phase 8 "顺手修了"** — 大佬反馈问题必须走完整反馈循环
7. **agent 自判完成** — 必须通过 CHECKPOINT 客观验证
8. **Auto-Fix 无限循环** — 2 轮后必须 escalate 给大佬
9. **Placeholder 污染 tasks.md** — TBD/TODO/similar to N = 计划缺陷
10. **忽略 Type Consistency** — 跨任务的函数签名/类型必须一致
11. **写入文件后不验证路径** — write_file 后必须 `ls` 确认（2026-05-15 教训）
12. **方向变化不回 Phase 1** — 核心定位变化必须回 Phase 1（2026-05-19 教训）
13. **超时后提交半成品** — 子 agent 超时后 git stash/revert（2026-05-19 教训）
14. **Phase 5 缺少 Self-Review** — tasks.md 写完后必须 Self-Review（2026-05-19 教训）
15. **Phase 6 不做 Spec-Code 同步** — 每个 Task 完成后更新 proposal.md（2026-05-19 教训）
16. **公众号检查不走云主机** — 必须 SSH 到 <WG_CLIENT_IP>:<SSH_PORT>（2026-05-19 教训）
17. **巡检报告写本地** — cron prompt 必须指定 Obsidian 路径（2026-05-19 教训）
18. **MCP 重复调用归因错误** — 是工具映射问题，不是项目问题（2026-05-19 教训）
11. **`register_command` 只对斜杠命令有效** — `register_command("/mp", handler)` 只拦截 `/mp` 前缀。纯数字消息不是斜杠命令，不会被拦截。**这是唯一的零 token 路径。**
12. **hook 只拦截特定前缀消息** — `pre_gateway_dispatch` hook 只拦截你配置的前缀（如 `"mp "`、`"/mp"`）。纯数字消息（`"9 功夫足球"`）不经过插件直接进 LLM。要让 hook 支持数字匹配，必须在 `on_pre_dispatch` 里显式处理（正则匹配数字前缀）。
13. **飞书 Card 按钮点击不会发送消息到对话** — 飞书 Interactive Card 按钮点击后触发 `card.action.trigger` 回调（POST 到开发者服务器），**不会**把按钮 value 作为消息发送到对话。Hermes 飞书 adapter 会把回调转换为 `/card` 命令（GitHub issue #7675）。飞书 Card 按钮 value 不会作为消息发送到对话，只触发 callback。
14. **插件指令一次性化** — 插件执行完就结束，没有上下文保持。搜索完结果后，用户想订阅/下载第一个结果，需要重新发指令。应设计状态机或上下文保持机制。
15. **调研时不要反复重启 gateway** — 每次重启都中断 session，导致重复分析。调研阶段只读文档和搜索，不要修改运行中的代码。
16. **需求范围可能在 Phase 2 调整** — 大佬可能在方案设计阶段调整项目核心定位（如从"博客管理"改为"文章生成+多渠道发布"）。此时应回到 Phase 1 更新 conversation.md，重新确认需求，而不是继续在旧方案上推进。**需求变更 = 回到 Phase 1。**
17. **图片生成方案调研** — 当项目涉及图片生成时，优先推荐免费 API 方案（Nano Banana 2 / Gemini、FLUX.2 Schnell / fal.ai、Seedream V4），不要推荐付费方案（DALL-E 3）或需要本地 GPU 的方案（Stable Diffusion）作为首选。用户偏好免费、可切换模型的 API 方案。
18. **Phase 6 Kanban 卡创建后状态为 running 而非 ready** — dispatcher 会自动将 ready 状态的卡标记为 running。如果卡创建后立即显示 running，说明 dispatcher 已自动领取。这是正常行为，不需要手动干预。
19. **notify-subscribe 命令可能返回空** — `hermes kanban notify-subscribe` 命令在某些版本中可能返回空输出（exit code 1）。这不影响 Kanban 功能，只是通知订阅失败。可以跳过此步骤，不影响任务执行。
20. **Kanban 状态同步问题（2026-05-18）** — coder/worker 完成工作后可能未正确调用 `kanban_complete`，导致状态停留在 running/blocked。灵犀应：(1) 等待 5 分钟后检查 running 状态的卡 (2) 用 `ls` 检查产出物是否存在 (3) 产出物存在则手动 `hermes kanban complete <id>` 标记完成 (4) 不等 dispatcher 通知，主动推进流程。
21. **角色分离违规（2026-05-18）** — worker 卡住时灵犀直接创建了 cron 任务，违反了角色分离原则。正确做法：(1) 创建 fix 卡派给另一个 worker (2) 或 escalate 给大佬 (3) 即使\"看起来很小\"也不能自己动手。效率不是跳过角色分离的理由。
22. **Review 卡应由灵犀创建而非依赖 agent（2026-05-18）** — 实现卡完成后，灵犀应主动创建 Review 卡，不依赖 agent 自判。agent 可能完成工作但忘记创建 review 卡。灵犀在验证 checkpoint 后立即创建 review 卡。
23. **超时机制缺失（2026-05-18）** — worker 任务无超时，导致灵犀等待过长（>2 分钟）。建议：(1) coder 任务超时 10 分钟 (2) worker 任务超时 5 分钟 (3) tester 任务超时 5 分钟 (4) 超时后自动 escalate 给灵犀介入。
24. **巡检 cron 报告写入本地而非 Obsidian（2026-05-19）** — 巡检 cron prompt 中报告路径写的是 `~/.hermes/cron/output/`，没有写 Obsidian。导致巡检结果只在本地，大佬在 Obsidian 看不到。修复：prompt 中同时写入 Obsidian `wiki/projects/clsh-content/changes/`。
25. **公众号 API 检查未走云主机 SSH（2026-05-19）** — 巡检脚本在本地调用 `wechat-publish.cjs` 检查微信 API，但本地出口 IP 不在微信白名单中。云主机固定 IP 已在白名单中。修复：公众号检查通过 SSH 到云主机（WG IP: <WG_CLIENT_IP>:<SSH_PORT>）执行。
26. **delegation-protocol 重复加载浪费 token（2026-05-19）** — 每次派活前都读完整 delegation-protocol（3000+ 字），同一个 session 中重复加载。修复：session 内缓存（只加载一次）+ 快速检查清单（80% 场景只需读 200 字摘要）。
27. **Phase 6 Checkpoint 输出过长（2026-05-19）** — agent 的 Checkpoint 输出包含完整编译日志/测试输出，单个 Task 往返消耗 2000-5000 token。修复：Checkpoint 限制 200 字以内，长文本写入 `/tmp/<project>-<task>.log`。

## Verification Checklist（每次使用此 skill 前）

- [ ] 确认不是简单查询/单步操作（否则不应触发 clsh-project）
- [ ] 确认 Phase 1 已执行调研前置（调研摘要已写入 conversation.md 或大佬明确跳过）
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
| v3.2.0 | 2026-05-19 | Phase 5 新增 Self-Review（Spec Coverage + Placeholder Scan + Type Consistency + File Isolation）；Phase 6 新增 Step 9 Spec-Code 同步（Kiro）；Phase 6 超时机制新增自动回滚（Phoenix）：git stash/revert，禁止提交半成品；delegation-protocol session 内缓存 + 快速检查清单 |
| v3.1.0 | 2026-05-19 | Phase 4 新增自动路径检查；Phase 6 新增 Checkpoint 输出截断规则（200字限制）+ 三层超时防护（子agent自带超时 + 产出物预检 + 灵犀5分钟轮询）；Phase 8 路径 C 明确方向变化必须回 Phase 1；Common Pitfalls 新增巡检 cron 报告写入本地而非 Obsidian、公众号检查未走云主机 SSH |
| v3.0.0 | 2026-05-19 | github-sync-guide 补充 clsh-content 仓库；Common Pitfalls 补充 Wireguard 运维、Hermes 插件注册、小红书 MCP 部署 |
| v2.9.0 | 2026-05-19 | Common Pitfalls 新增 3 条：需求范围调整回 Phase 1、图片生成方案偏好、notify-subscribe 返回空 |
| v2.5.0 | 2026-05-17 | Phase 1 新增"调研前置"环节 |
| v2.4.0 | 2026-05-16 | P0-P3 全面优化 |
| v2.3.0 | 2026-05-15 | 铁律 8 条 + Phase 6 状态机 + Phase 8 反馈循环 |
| v2.2.0 | 2026-05-13 | Kanban bridge + tasks.md 回写 |
| v2.1.0 | 2026-05-12 | Constitution 模板 + Phase 4 自检 |
| v2.0.0 | 2026-05-11 | 初始版本 |

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
- `references/integration/hermes-slash-command-mechanism.md` — Hermes 斜杠命令机制与插件化架构调研（2026-05-17）：内置命令硬编码、插件 hook 能力边界、零 token 三方案、mp-menu 教训
- `references/integration/hermes-plugin-zero-token.md` — Hermes 插件零令牌路由架构（2026-05-17）：pre_gateway_dispatch 能力边界、register_command 零 token 路径、双层路由方案、菜单状态管理、命令匹配逻辑

### ⚠️ 教训
- `references/pitfalls/violation-case-2026-05-15.md` — 流程违规案例：跳步 + 自测
- `references/pitfalls/violation-case-2026-05-15-self-coding.md` — 灵犀直接写代码违规案例

## 流程说明

详见 `README.md`（skill 根目录）— 包含流程总览、各 Phase 详解、速查表、版本历史。
