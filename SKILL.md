---
name: clsh-project
description: "需求驱动的项目开发工作流 — 从需求澄清到设计文档到实现计划到执行。灵感来自 Kiro 的 Spec-Driven Development、Superpowers 的 Brainstorming 方法论、Phoenix 的状态机执行模式。"
version: 3.8.0
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
      # 方法论（clsh-project 流程知识，保留本地）
      - references/methodology/ralph-loop-analysis.md
      - references/methodology/openspec-comparison.md
      - references/methodology/kiro-superpowers-analysis.md
      - references/methodology/agent-skill-execution-research.md
      - references/methodology/superpowers-v5-changes.md
      # 模板（clsh-project 流程模板，保留本地）
      - references/templates/constitution-template.md
      - references/templates/archive-workflow.md
      - references/templates/cloud-server-wireguard.md
      - references/templates/phase7-archive-checklist.md
      # 集成（clsh-project 工具链，保留本地）
      - references/integration/kanban-tasks-bridge.md
      - references/integration/hermes-slash-command-mechanism.md
      - references/integration/hermes-plugin-zero-token.md
      - references/integration/hermes-plugin-hooks-reference.md
      - references/integration/halo-auth.md
      - references/integration/halo-cli-auth.md
      - references/integration/reference-migration-pattern.md
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

### ⛔ 文件大小控制（不可违反）

**tasks.md 单文件不得超过 3000 字。** 超过时必须拆分：

```
tasks.md          ← 汇总版（依赖图 + 任务索引 + Self-Review）
tasks-slice1.md   ← Slice 1 详细任务（~2000字）
tasks-slice2.md   ← Slice 2 详细任务（~2000字）
tasks-slice3.md   ← Slice 3 详细任务（~2000字）
tasks-slice4.md   ← Slice 4 详细任务（~2000字）
```

**拆分规则：**
1. tasks.md 写汇总：依赖图 + 每个 Slice 的简要描述 + 任务索引 + Self-Review
2. 每个 slice 文件写该 Slice 的完整任务（含代码片段）
3. 每个文件控制在 2000-3000 字
4. 分多次 write_file 写入，每次写一个文件
5. 写入后必须 `ls` 验证文件存在且大小 > 0

**⛔ 禁止：** 一次性 write_file 写入 >5000 字的内容（会被截断导致文件损坏）

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

### ⚠️ Blocked 状态处理协议（必须遵守）

**核心规则：`blocked ≠ done`，blocked 状态不触发依赖引擎 promote 子任务。**

```
worker 遇到问题无法继续
  ↓
Step B1: worker 调用 kanban_block(reason="具体阻塞原因")
Step B2: worker 调用 kanban_comment(body="完整上下文 + 已尝试的方案")
  ↓
Step B3: 灵犀收到通知后介入
  ├─ 产出物已完成 → hermes kanban complete <id>（标记 done，依赖引擎继续）
  ├─ 产出物部分完成 → hermes kanban complete <id> + 创建新卡处理剩余工作
  └─ 产出物不可用 → hermes kanban complete <id> + 创建 fix 卡（parents=[原卡]）
  ↓
Step B4: 创建 fix 卡（如需要）
  → assignee = 原 worker 或另一个 coder（不是灵犀自己）
  → parents = [原实现卡]（必须等原卡 done 后 fix 卡才 promoted）
  → body 包含：具体问题描述 + B2 的 comment 上下文
```

**⛔ 禁止：**
- worker 调用 `kanban_block()` 后，灵犀不 complete 原卡就直接创建 fix 子卡
  → 结果：fix 卡永远卡在 todo（parent 未 done）
- worker 遇到问题直接 `kanban_complete(summary="...")` 假装完成
  → 结果：产出物缺失但状态为 done，后续步骤踩坑
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

```
对于计划中的每个 Task:
  1. 读取 constitution.md
  2. 根据任务类型选择 agent（coder/artist/tester）
  3. kanban_create 创建实现卡（绝对路径 + 验收标准 + 不在范围内）
  4. dispatcher 自动派发 ready 状态的卡
  5. worker 执行任务
  6. worker 完成后输出 CHECKPOINT（产出物自检）
  7. 灵犀验证 checkpoint（产出物 ls 验证）
     ├─ FAIL → 返回 Step 5（重试），最多 2 轮 → 仍 FAIL → 创建 fix 卡
     └─ PASS ↓
  8. kanban_create 创建 review 卡（assignee=tester, parents=[实现卡]）
     ⚠️ Review 卡必须在 Step 7 验证 PASS 后才能创建
  9. dispatcher 自动派发 review 卡
  10. tester 执行 Security Scan + Quality Review
  11. PASS → 标记 Task 完成
  12. FAIL → 创建 fix 卡（不是实现者本人）→ 重新 review（max 2轮）
  13. 全部 Task 完成 → Final Integration Review
```

**Review 卡创建规范：**
```bash
hermes kanban create "[项目名] Review: <任务名>" \
  --assignee tester \
  --body "...审查维度...\
PASS/FAIL 输出要求..." \
  --parent <实现卡ID> \
  --json
```
- Review 卡依赖实现卡（parents），实现卡完成后自动 promoted → ready
- Review 卡 body 必须包含：审查维度 + PASS/FAIL 输出格式 + 上下文（实现卡ID）

**并行派发策略：**
- 无依赖的任务同时创建 Kanban 卡
- Review 卡必须在实现卡 checkpoint 验证 PASS 后创建（不是同时创建）
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

#### Worker Heartbeat（长任务可选）
- 预计 >5 分钟的任务，worker 应每 2-3 分钟调用 `kanban_heartbeat(note="进度描述")`
- dispatcher 的 passive heartbeat 每 60s 检查 PID 是否存活（自动延长 claim）
- heartbeat 不能替代显式超时机制，只是辅助监控

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

### ⛔ wiki 归档检查清单（必做，不可跳过）

Phase 7 归档时，必须确认以下文件已写入 wiki：

**项目文档：**
- [ ] `wiki/projects/<项目名>/overview.md` → 更新 status 为 `done`
- [ ] `wiki/projects/<项目名>/changes/archive/<变更名>/completion-summary.md` → 完成摘要
- [ ] `wiki/projects/<项目名>/changes/archive/<变更名>/retrospective.md` → 流程复盘
- [ ] `wiki/projects/<项目名>/changes/archive/<变更名>/conversation.md` → 需求对话
- [ ] `wiki/projects/<项目名>/changes/archive/<变更名>/proposal.md` → 设计提案
- [ ] `wiki/projects/<项目名>/changes/archive/<变更名>/tasks.md` → 实现计划
- [ ] `wiki/projects/<项目名>/source-of-truth/constitution.md` → 项目约束

**Phase 8 各轮归档（每轮必须）：**
- [ ] `wiki/projects/<项目名>/changes/archive/round<N>-feedback/conversation.md` → 测试反馈记录
- [ ] `wiki/projects/<项目名>/changes/archive/round<N>-feedback/fixes.md` → 修复方案记录

**⛔ 如果 Phase 8 已完成多轮测试，必须将每轮的 feedback 目录归档到 archive/，不能只保留在 changes/ 下。**

### 归档步骤

1. 更新提案状态 → `status: done`
2. 归档所有变更 → `changes/<变更名>/` → `changes/archive/`
3. 归档 Phase 8 每轮 feedback → `changes/round<N>-feedback/` → `changes/archive/round<N>-feedback/`
4. 更新 Source of Truth
5. 写入完成摘要 + 流程复盘
6. 同步 wiki + GitHub（见 `wiki/reference/integration/github-sync-guide.md`）
7. 向大佬汇报
8. `ls` 验证所有归档文件存在且大小 > 0

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

### ⛔ Phase 8 执行规范（不可违反）

#### 1. 必须用 delegate_task 派发修复任务

**Phase 8 修复 = Phase 6 执行，必须角色分离。**

| 修复类型 | 必须派给 | 工具集 |
|---------|---------|--------|
| 后端 API 修复 | coder | terminal, file |
| 前端逻辑修复 | coder | terminal, file |
| UI/CSS 修复 | artist | terminal, file |
| **测试验证** | **tester** | **terminal, file, web, browser** |

**⛔ 禁止灵犀直接改代码。** 即使"很快能做完"也必须派 delegate_task。

#### 2. Tester 必须使用浏览器工具

**tester 的 toolsets 必须包含 `web` 和 `browser`（或 `computer_use`）。**

tester 验证时：
- **必须用浏览器访问页面**，不能用 curl/API 替代
- 浏览器工具：`mcp_mp_browse_webpage` 或 `browser` toolset
- 验证内容：页面渲染、交互功能、CSS 样式、响应式布局
- 如果浏览器工具不可用，向大佬报告，不要降级为 curl 测试

**tester 派发模板：**
```
toolsets: ["terminal", "file", "web", "browser"]
```

#### 3. 每轮必须归档 wiki

**每轮 Phase 8 修复完成后，必须创建变更目录并归档：**

```
wiki/projects/<项目名>/changes/round<N>-feedback/
├── conversation.md    ← 大佬反馈的问题列表
├── diagnosis.md       ← diagnose 6 阶段记录
├── fixes.md           ← 每个问题的修复方案 + 派发记录
└── test-report.md     ← tester 验证报告
```

**全部修复完成后，归档到 archive/：**
```
wiki/projects/<project>/changes/archive/round<N>-feedback/
```

**⛔ 禁止只在对话中修复，不写 wiki 记录。**

#### 4. 大修复用 kanban，小修复用 delegate_task

| 场景 | 方式 |
|------|------|
| ≤3 个简单修复 | delegate_task 直接派发 |
| >3 个修复 或 需要追踪 | kanban 创建卡 + delegate_task |
| 跨 session 的大修复 | kanban（状态持久化） |

**kanban 创建规范：**
```bash
# 创建修复卡
hermes kanban create "[项目名] Round<N>: <问题简述>" \
  --assignee coder/artist \
  --body "问题描述 + 验收标准" \
  --json

# 创建 review 卡（依赖修复卡）
hermes kanban create "[项目名] Review: <问题简述>" \
  --assignee tester \
  --body "验证步骤 + PASS/FAIL 标准" \
  --parent <修复卡ID> \
  --json
```

### ⚠️ 上下文溢出防护（2026-05-21 教训，2026-05-21 强化）

**Phase 8 大量 bug 修复时，必须控制节奏。两次中断 = 必须更激进地控制上下文：**

#### 核心原则：每轮最多修 3-4 个 bug（不是 5-6 个）

1. **每轮最多修 3-4 个 bug** — 超过 4 个时必须分批，每批修完先重启测试
2. **后端和前端分开修** — 先修后端（通常少），再修前端
3. **Agent 反复超时后向大佬报告** — 不要全部 fallback 到灵犀直接改代码（违反角色分离 + 上下文爆炸）
4. **每批修完后写 checkpoint** — 记录已修复项，防止 session 断开后丢失进度
5. **修完一批先 `pm2 restart` + 基础测试** — 确确无回归再继续下批

#### 上下文节省策略（每次修复必做）

6. **用 `execute_code` 批量读代码** — 不要在主对话中逐个 read_file，用 execute_code 一次读多个文件并输出关键片段
7. **每个 bug 只读相关代码片段** — 不加载整个文件，用 offset/limit 或 grep 定位
8. **修一个验证一个** — 不要一次性修改所有文件再验证
9. **长输出写入 /tmp/ 而非主对话** — 测试结果、日志等写入文件，只在对话中放结论
10. **进度写入 checkpoint 文件** — `/tmp/<project>-round<N>-checkpoint.md`，记录已修/待修/阻塞项

#### 中断恢复协议

当 session 因上下文过大中断后重启：
1. 读取 `/tmp/<project>-round<N>-checkpoint.md` 恢复进度
2. 如果 checkpoint 不存在，从项目文档 `changes/` 目录恢复
3. **从上次中断的 bug 继续，不重做已完成的修复**
4. 向大佬确认恢复的上下文是否正确

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
16. **Phase 5 write_file 大文件截断** — tasks.md 等实现计划文件内容过大（>5000字）时，write_file 会因输出长度限制被截断，导致文件写入失败或内容丢失。**解决方案：** 拆分为多个子文件（tasks-slice1.md, tasks-slice2.md...），每个文件控制在 2000-3000 字，分多次写入。汇总版 tasks.md 只写依赖图 + 任务索引 + Self-Review。（2026-05-20 教训）
17. **Phase 8 测试阶段没有用 kanban 派发任务** — Phase 8 修复必须用 delegate_task 派给 coder/artist/tester，不能灵犀直接改。小修复用 delegate_task，大修复用 kanban 创建卡。Phase 8 = Phase 6 执行，角色分离不可跳过。（2026-05-21 教训）
18. **Phase 8 tester 没有使用浏览器工具** — tester 验证时必须用浏览器访问页面（toolsets 包含 web + browser），不能用 curl/API 替代。浏览器才能验证页面渲染、交互功能、CSS 样式。（2026-05-21 教训）
19. **Phase 8 每轮测试结果和修复方案没有归档 wiki** — 每轮 Phase 8 修复完成后，必须在 wiki/projects/<项目名>/changes/round<N>-feedback/ 创建 conversation.md（问题列表）、diagnosis.md（诊断记录）、fixes.md（修复方案）、test-report.md（验证报告），然后归档到 archive/。（2026-05-21 教训）
20. **Phase 7 归档不完整** — Phase 7 归档时必须检查：overview.md 已更新为 done、completion-summary.md 已写入、retrospective.md 已复盘、Phase 8 每轮 feedback 已归档到 archive/、所有文件 ls 验证存在。（2026-05-21 教训）
21. **Phase 8 delegate_task 不等于 kanban** — delegate_task 是派发方式，kanban 是任务追踪方式。两者不互斥：小修复直接 delegate_task，大修复/跨 session 修复用 kanban 创建卡 + delegate_task 派发。kanban 的优势是状态持久化，session 断开后仍可恢复。（2026-05-21 教训）
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
28. **大规模文件索引策略（2026-05-19）** — 14229 个文件全量扫描 >120s 不可接受。必须用 grep 预过滤（只处理含目标内容的文件）。SQLite FTS5 trigram 分词器对中文更友好。反链索引用 grep + 标题匹配，<1s。
29. **Phase 8 大量 bug 修复时上下文溢出（2026-05-21）** — 13 个 bug 全部灵犀直接修复，导致上下文过长，session 断开。应：(1) 每轮最多修 5-6 个 bug (2) agent 超时后分批重试而非全量自修 (3) 后端和前端分开修 (4) 每修完一批先重启测试再继续。
30. **agent 超时后退化为灵犀直接改代码（2026-05-21）** — 3 个并行 agent 全部超时/失败后，灵犀 fallback 到直接写代码。违反角色分离但 session 断开代价更大。正确做法：(1) 先缩小任务范围重试 (2) 如果 agent 反复失败，向大佬报告瓶颈 (3) 至少分 2 个 session 完成。
31. **ESM 变量遮蔽导致 500 错误（2026-05-21）** — `createShare({ path })` 的解构参数 `path` 遮蔽了顶部 `import path from 'path'` 的模块。函数体内 `path.resolve()` 调用的是参数而非模块，导致 `require is not defined`。修复：参数重命名为 `sharePath`。教训：ESM 模块中，任何参数名不应与 import 的模块名冲突。
32. **Markdown 表格正则匹配非表格行（2026-05-21）** — 正则 `/(^.*\|.*$)/gm` 匹配所有含 `|` 的行，包括代码块内和非表格行。修复：(1) 先匹配有 separator 行的标准表格 (2) 再匹配无 separator 的连续 `|` 行 (3) 确保 separator 行格式 `|---|---|` 正确解析。lessons: `buildTable` 函数用 `function` 声明（会被 hoisting）避免定义顺序问题。
33. **前端 z-index 层级管理（2026-05-21）** — Toast z-index=2000 被 modal z-index=3000 遮挡。规则：Toast ≥ 5000 > Modal ≥ 3000 > Context menu ≥ 1000 > Content。
34. **TOC 在 flex 容器中不悬浮（2026-05-21）** — `position: sticky` 在 flex item 上需要 `align-self: flex-start` 才生效。滚动容器必须是 `.content-inner`（有 overflow-y: auto），TOC 的 `max-height: calc(100vh - 60px)` 防止溢出。
29. **write_file 大文件截断（2026-05-20）** — tasks.md 等实现计划文件内容过大（>5000字）时，write_file 会因输出长度限制被截断，导致文件写入失败或内容丢失。**解决方案：** (1) 拆分为多个子文件（如 tasks-slice1.md, tasks-slice2.md...），每个文件控制在 3000 字以内；(2) 再写一个汇总版 tasks.md 引用各子文件。Phase 5 的 tasks.md 已成功用此方案（4 个 slice 文件 + 1 个汇总，总计 2180 行分 5 次写入成功）。
30. **delegate_task coder 超时根因（2026-05-20）** — coder agent 超时（600s）不一定是代码逻辑问题，常见根因是：(1) 验证阶段启动服务器时，同步 I/O（如 `readdirSync` 扫描 15K 文件）阻塞事件循环，导致 curl 请求无响应；(2) npm install 网络慢；(3) Docker Hub 超时。**解决方案：** (1) 在 agent 任务描述中明确"不要运行验证命令，只写文件"，验证由灵犀在主线程执行；(2) 代码中优先使用异步 I/O（`fs/promises`）；(3) 如果 agent 超时但产出物文件已存在且内容正确，直接标记 PASS，不重派。T08 coder 超时但 tree.mjs 产出物完整即为典型案例。
31. **端口冲突积累（2026-05-20）** — Phase 6 多次测试中，background 服务器进程（`node src/server.mjs`）可能未正常退出，导致 EADDRINUSE。**解决方案：** 每次启动新服务器前，先执行 `lsof -ti:3456 | xargs kill -9 2>/dev/null` 清理旧进程。建议在测试脚本开头统一加此步骤。
32. **模块导出缺失（2026-05-20）** — 跨文件导入时（如 tags.mjs 从 search.mjs 导入 `getTitleIndex`），如果导出方忘记 `export`，运行时报 `SyntaxError: The requested module does not provide export`。**解决方案：** 写完所有模块后，用 `node -e "import { X } from './path'"` 逐个验证导出。或在 server.mjs 启动时加 try/catch 捕获 import 错误。
33. **环境路径差异（2026-05-20）** — Docker 容器内路径（`/app/data`、`/vault`）与本地开发路径（`/opt/obsidian-workbench/data`、`/mnt/unraid_data/Obsidian`）不同。**解决方案：** 所有路径通过环境变量（`VAULT_PATH`、`DB_PATH`）注入，默认值用 Docker 路径，本地测试时显式传环境变量。indexer.mjs 的 DB_PATH 应改为条件路径：`process.env.DB_PATH || path.join(VAULT_PATH.startsWith('/vault') ? '/app/data' : '/opt/obsidian-workbench/data', 'index.db')`。
34. **execSync 扫描大文件集超时（2026-05-20）** — backlinks.mjs 用 `execSync('grep -rl ...')` 扫描 15K 文件时，10s 超时不够。**解决方案：** (1) 增大 timeout 到 30000ms；(2) 更好的方案是用 `fs.promises.readdir` 递归扫描 + `fs.promises.readFile` 批量读取（并行，每批 100 个），避免 shell 命令开销。实测纯 Node.js 方案扫描 14K 文件约 25s，无超时风险。
35. **server.mjs 路由注册遗漏（2026-05-20）** — 用 patch 分步修改 server.mjs 时，可能只加了 import 但忘记加路由注册代码，导致 404。**解决方案：** 修改 server.mjs 时，一次性完成 `import` + `路由注册` + `ensureSharesTable()` 等所有相关改动，避免分步 patch 遗漏。写完后用 `grep -n "app.get\|app.post"` 验证路由是否全部注册。
36. **getTree() 缺少 await（2026-05-20）** — tree.mjs 的 `getTree()` 改为 async 后，server.mjs 中调用时忘记加 `await`，导致返回 Promise 对象而非实际数据。**解决方案：** 所有 async 函数调用处必须检查是否有 `await`。用 `node -e "import { getTree } from './tree.mjs'; console.log(typeof getTree())"` 验证返回类型应为 `object` 而非 `promise`。
37. **write_file 覆盖导致内容丢失（2026-05-20）** — write_file 会完全覆盖文件。当需要追加内容时（如 style.css 多次追加样式），必须先读取现有内容再合并写入，或使用 patch 工具。**解决方案：** 对需要增量修改的文件，用 `patch` 工具而非 `write_file`；或在 write_file 前先 `read_file` 获取现有内容，合并后写入。
38. **write_file 大文件截断（2026-05-20）** — tasks.md 等实现计划文件内容过大（>5000字）时，write_file 会因输出长度限制被截断。**解决方案：** 拆分为多个子文件（每个控制在 3000 字以内），再写汇总版引用。Phase 5 已成功用此方案（4 个 slice + 1 个汇总，2180 行分 5 次写入）。
39. **delegate_task coder 超时根因（2026-05-20）** — 验证阶段同步 I/O 阻塞、npm 网络慢、Docker Hub 超时。**解决方案：** 任务描述中明确"不要运行验证命令，只写文件"；优先异步 I/O；超时但产出物正确则直接 PASS。
40. **端口冲突积累（2026-05-20）** — 启动服务器前执行 `lsof -ti:3456 | xargs kill -9 2>/dev/null` 清理旧进程。
41. **模块导出缺失（2026-05-20）** — 写完后用 `node -e "import { X } from './path'"` 逐个验证导出。
42. **execSync 扫描大文件集超时（2026-05-20）** — 用 `fs.promises` 批量读取替代 shell 命令，每批 100 个并行。
43. **server.mjs 路由注册遗漏（2026-05-20）** — 一次性完成 import + 路由注册 + ensureSharesTable()，用 grep 验证。
44. **async 函数调用缺少 await（2026-05-20）** — 所有 async 函数调用处必须检查是否有 await。
45. **部署方式切换 Docker→本地 pm2（2026-05-20）** — Docker Hub 网络超时，切换为本地 pm2 部署。VAULT_PATH 默认值改为 `/mnt/unraid_data/Obsidian`。
46. **子 agent 超时零容忍（2026-05-20）** — 拆小任务(<10min)，不派验证命令，直接写更快就直接写。
47. **Phase 8 修复必须走角色分离（2026-05-20）** — 大佬测试反馈问题后，即使是"小修复"也必须派 coder/artist/tester，禁止灵犀直接改代码。第一轮修复（6个问题全部灵犀自己写）已记 ERRORS.md。第二轮严格按角色分离执行（coder + 3个artist + tester），9/9 通过。
53. **ESM 模块中禁止使用 require()（2026-05-21）** — 当 agent 修改 .mjs 文件时，可能错误地引入 `require('path')` 或 `require('fs')`，但 ESM 模块不支持 `require`。**症状：** 运行时 `ReferenceError: require is not defined`，HTTP 500。**解决方案：** 所有 `.mjs` 文件使用 `import` 语句，文件顶部已有 `import path from 'path'` 和 `import fs from 'fs'`，直接使用即可。**验证：** 修改后用 `node -e "import { X } from './path'"` 验证导入是否正常。share.mjs 中 `createShare` 函数的参数名 `path` 与 import 的 `path` 模块同名，需重命名为 `sharePath` 避免冲突。
54. **delegate_task 全部超时的应急方案（2026-05-21）** — 当一轮中 3+ 个 delegate_task 全部超时（600s）时，不要重复派发。**应急方案：** (1) 灵犀直接用 `write_file`/`patch` 修改前端文件（app.mjs template、style.css）；(2) 记录为流程偏差；(3) 修改后必须通过 tester 验证。**根因：** 任务描述过于复杂、agent 启动开销大、网络延迟。**预防：** 每个 agent 任务控制在 2-3 个文件修改，不要求 agent 运行验证命令。
55. **TOC 在 flex 容器中 sticky 不生效（2026-05-21）** — `position: sticky` 在 flex item 上可能不生效。**症状：** 滚动笔记时 TOC 跟随滚动而不是固定在右侧。**解决方案：** (1) 确保 `.note-with-toc` 的父容器 `.content-inner` 有 `overflow-y: auto`；(2) TOC 的 `max-height` 设为 `calc(100vh - 60px)` 而非 `100vh`；(3) 如果 sticky 仍不生效，改用 `position: fixed` + JS 计算 top 位置。
56. **Toast z-index 被 modal 遮挡（2026-05-21）** — Toast 默认 z-index 2000，modal-overlay z-index 3000，导致 toast 被遮罩挡住。**解决方案：** Toast z-index 设为 5000+，并添加 `pointer-events: none` 防止遮挡交互。
57. **用户偏好：任务拆分防超时（2026-05-21）** — 大佬明确指出"注意任务太大子 agent 或者 sub-agent 超时，看能否拆分"。**规则：** 派活前必须评估任务粒度，单个 agent 任务不超过 5 分钟。前端任务按职责拆分（CSS/样式、功能修复、新增功能），后端任务按 API/模块拆分。宁可多派几个小任务，不要一个大任务。
58. **CSS 全局变量 alpha 值对 Toast 不可见（2026-05-21）** — CSS 变量 `--success-bg: rgba(22,163,74,0.08)` 的 alpha 仅 0.08，toast 使用此变量时背景几乎透明。**修复：** Toast/notification 背景使用独立实色 hex 值（如 `#DCFCE7`），不引用全局 alpha 变量。详见 `wiki/projects/obsidian-workbench/references/pitfalls/trap-case-2026-05-21-round6-frontend-patterns.md`。
59. **Markdown 渲染器必须在后端生成 Heading ID（2026-05-21）** — `renderMarkdown()` 生成的 `<h1>` 无 `id` 属性导致 TOC 无法跳转。前端 `applyTocIds()` 补充 ID 存在时序问题。**修复：** 后端渲染器直接用 slugify 生成带 ID 的标题标签。详见 `wiki/projects/obsidian-workbench/references/pitfalls/trap-case-2026-05-21-round6-frontend-patterns.md`。
60. **API 响应遗漏前端所需属性（2026-05-21）** — `getFolderShares()` 返回 folder 项缺 `path` 属性，前端无法展开子文件夹。**规则：** API 返回后用 python3 检查每个 item 是否包含前端需要的全部字段。新增 API 响应时，列清楚前端需要哪些字段。详见 `wiki/projects/obsidian-workbench/references/pitfalls/trap-case-2026-05-21-round6-frontend-patterns.md`。
61. **独立 HTML 页面功能遗漏检查（2026-05-21）** — 主 SPA 有文件夹展开+TOC，但 folder.html/share.html 缺失。**规则：** 新增独立 HTML 页面时，对照主 SPA 功能清单检查：文件树展开、TOC、搜索、深色主题、移动端响应式。
62. **Phase 8 修复两次中断的教训（2026-05-21）** — 大佬第七轮测试反馈后，修复任务因上下文过大中断了两次。根因：(1) 一轮修太多 bug（>10 个）；(2) 在主对话中逐个 read_file，上下文膨胀；(3) 没有写 checkpoint 文件保存进度。**规则：** (1) 每轮最多修 3-4 个 bug；(2) 用 `execute_code` 批量读代码，不在主对话中逐个 read_file；(3) 每批修完写 checkpoint 到 `/tmp/<project>-round<N>-checkpoint.md`；(4) 中断后先读 checkpoint 恢复进度；(5) 向大佬确认恢复的上下文再继续。
63. **blocked 状态不触发依赖引擎（2026-05-21）** — worker 调用 `kanban_block()` 后，blocked 状态不等于 done，依赖引擎不会 promote 子任务。如果灵犀不 `hermes kanban complete <id>` 原卡就直接创建 fix 子卡，fix 卡永远卡在 todo。**规则：** worker block → 灵犀 complete 原卡 → 灵犀创建 fix 卡（parents=[原卡]）。详见 Phase 6 Blocked 状态处理协议。
64. **Review 卡必须在 checkpoint 验证后创建（2026-05-21）** — 旧版流程写"同时创建实现卡和 Review 卡"，但 kan-orchestrator 的 Review Gate Protocol 要求：灵犀验证 checkpoint PASS 后才能创建 Review 卡。虽然 parents 依赖会阻止 Review 卡提前被 claim，但提前创建会浪费 dispatcher 的调度资源，且不符合"验证后再审查"的语义。**规则：** Step 7 验证 PASS → Step 8 创建 Review 卡。
48. **Artist 大任务拆分模式（2026-05-20）** — 当 artist 任务包含 5+ 个前端变更时，单个 artist 容易超时（10min 限制）。**解决方案：** 按职责拆分为多个并行 artist 子任务：artist-1 负责 CSS/样式重写，artist-2 负责功能修复（Modal/右键菜单等），artist-3 负责新增功能（TOC/iframe 等）。每个子任务控制在 5-8 分钟内。并行派发，各自写同一个文件的不同部分（通过 append 模式），最后由灵犀合并验证。
49. **UI/UX Pro Max 使用模式（2026-05-20）** — 当需要专业 UI 设计系统时：(1) `uipro init --ai all --force` 安装到项目；(2) `python3 .cursor/skills/ui-ux-pro-max/scripts/search.py "项目类型 风格关键词" --design-system -p "项目名" -f markdown` 生成设计系统；(3) 把生成的色板/字体/原则写入 `design-system/MASTER.md`；(4) artist 按 MASTER.md 规范写 CSS。注意：uipro-cli 命令名是 `uipro`，不是 `uipro-cli`。
50. **Coder 任务描述精确性（2026-05-20）** — coder 完成任务后可能遗漏小字段（如 findShareByPath 返回值缺少 fullLink）。**解决方案：** 在任务描述中明确列出每个函数的返回值格式，包括计算字段（如 fullLink = `${BASE_URL}/s/${token}`）。验证步骤中明确检查每个返回字段。
51. **delegate_task 多 agent 同时超时的根因（2026-05-20）** — 当派发 3+ 个 delegate_task 时，可能全部超时（600s）。根因：(1) 任务描述过于复杂（包含多文件修改+验证步骤）；(2) agent 启动开销大；(3) 网络/API 延迟。**解决方案：** (1) 每个 agent 任务控制在 2-3 个文件修改以内；(2) 不要求 agent 运行验证命令，验证由灵犀在主线程执行；(3) 如果连续 2 个 agent 超时，转为灵犀直接修改（记录为流程偏差）；(4) 对于纯前端 CSS/JS 修改，灵犀直接 patch 比派 agent 更高效。
52. **Phase 8 角色分离的务实权衡（2026-05-20）** — 当 agent 连续超时时，灵犀直接修改前端文件（CSS/JS template）是务实选择，但必须：(1) 记录为流程偏差；(2) 修改后必须通过 tester 验证（不能自验）；(3) 优先尝试派 agent，超时 2 次后才转为直接修改。本轮第四轮修复中，3 个 delegate_task 全部超时，灵犀直接 patch 了 app.mjs 和 style.css，最终通过 tester 验证。

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

## 版本历史（续）

| 版本 | 日期 | 变更 |
|------|------|------|
| v3.8.0 | 2026-05-21 | **Phase 6 与 Hermes Kanban 对齐**：(1) 新增 Blocked 状态处理协议（blocked ≠ done，灵犀必须先 complete 原卡再创建 fix 子卡）；(2) 修正 Review 卡创建时机（必须在 checkpoint 验证 PASS 后创建，不是同时创建）；(3) 补充 Worker Heartbeat 说明（长任务可选，dispatcher passive heartbeat 每 60s 检查 PID）；(4) Common Pitfalls 新增 #63-64（blocked 状态、Review 卡时机） |
| v3.7.0 | 2026-05-21 | **References 架构重构**：项目相关 references 从 clsh-project skill 迁移到 wiki 项目目录。跨项目共享（github-sync-guide, lucky-api, php-env）→ `wiki/reference/integration/`；项目专属技术陷阱 → `wiki/projects/<项目名>/references/pitfalls/`；项目专属集成参考 → `wiki/projects/<项目名>/references/integration/`。每个目录有 `.references-meta.json` 追踪归属+过期状态。SKILL.md frontmatter references 列表完整更新，正文所有路径指向新位置。 |
| v3.6.0 | 2026-05-21 | Phase 5 新增文件大小控制（tasks.md ≤3000字，必须拆分为子文件）；Phase 7 新增 wiki 归档检查清单（含 Phase 8 每轮归档）；Phase 8 新增执行规范（必须 delegate_task 派发、tester 必须用浏览器工具、每轮必须归档 wiki、大修复用 kanban）；Common Pitfalls 新增 #16-21（write_file 截断、kanban 派发、tester 浏览器、Phase 8 归档、Phase 7 归档、delegate_task vs kanban） |
| v3.4.0 | 2026-05-21 | Common Pitfalls 新增 4 条（#58-61）：CSS alpha 变量对 Toast 不可见、Markdown 渲染器后端生成 Heading ID、API 响应遗漏前端属性、独立 HTML 页面功能遗漏检查。新增 references/pitfalls/trap-case-2026-05-21-round6-frontend-patterns.md |
| v3.3.0 | 2026-05-21 | Phase 8 新增"上下文溢出防护"铁律 + 3 条新 pitfalls（ESM 变量遮蔽、Markdown 表格正则、前端调试三件套）+ Phase 8 大量 bug 修复节奏控制 |

| 版本 | 日期 | 变更 |
|------|------|------|
| v3.2.0 | 2026-05-19 | Phase 5 新增 Self-Review（Spec Coverage + Placeholder Scan + Type Consistency + File Isolation）；Phase 6 新增 Step 9 Spec-Code 同步（Kiro）；Phase 6 超时机制新增自动回滚（Phoenix）：git stash/revert，禁止提交半成品；delegation-protocol session 内缓存 + 快速检查清单 |
| v3.3.0 | 2026-05-20 | Common Pitfalls 新增 write_file 大文件截断解决方案（拆分为多个子文件，每个控制在 3000 字以内） |
| v3.9.0 | 2026-05-21 | Common Pitfalls 新增 5 条：ESM 模块禁止 require()（agent 引入的 require 导致 500 错误）；delegate_task 全部超时应急方案（灵犀直接 patch + tester 验证）；TOC sticky 在 flex 容器不生效（max-height + overflow 修复）；Toast z-index 被 modal 遮挡（z-index 5000+pointer-events:none）；用户偏好任务拆分防超时（单个 agent ≤5 分钟） |
| v3.5.0 | 2026-05-20 | Common Pitfalls 新增 5 条：execSync 扫描大文件集超时（改用 fs.promises 批量读取）；server.mjs 路由注册遗漏（一次性完成 import + 路由注册）；getTree() 缺少 await（async 函数调用必须检查 await）；write_file 覆盖导致内容丢失（增量修改用 patch 而非 write_file） |
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

### 📍 Reference 架构说明（2026-05-21 迁移）

**原则：项目相关的 references 存在 wiki 项目目录里，不在 clsh-project skill 里。**

| 参考类型 | 位置 | 原因 |
|---------|------|------|
| 方法论 | `references/methodology/`（本地） | 流程知识，与项目代码无关 |
| 模板 | `references/templates/`（本地） | 流程模板，所有项目共用 |
| 工具链集成 | `references/integration/`（本地） | Hermes/Halo/Kanban 工具使用指南 |
| 流程违规案例 | `references/pitfalls/violation-case-*`（本地） | 流程纪律，与项目无关 |
| 流程管理指南 | `references/pitfalls/phase8-*, memory-*`（本地） | Phase 8 管理方法论 |
| **跨项目共享** | **`wiki/reference/integration/`** | github-sync-guide, lucky-api, php-env |
| **项目专属技术陷阱** | **`wiki/projects/<项目名>/references/pitfalls/`** | obsidian-workbench 的前端模式等 |
| **项目专属集成参考** | **`wiki/projects/<项目名>/references/integration/`** | clsh-content 的 halo-obsidian-ref |

**过期检测：** 每个项目目录有 `.references-meta.json`，记录 `projects`（归属）、`last_verified`（最后验证时间）、`staleness_threshold_days`（过期阈值）。执行项目时只检查该项目相关的 references。

**迁移模式详见：** `references/integration/reference-migration-pattern.md`（分类决策树 + 8 步迁移流程 + 过期检测逻辑）

### 📐 方法论（本地）
- `references/methodology/kiro-superpowers-analysis.md` — Kiro + Superpowers + Phoenix 工作流分析
- `references/methodology/ralph-loop-analysis.md` — Ralph Loop 调研：原理 + 与 Phase 6 映射
- `references/methodology/openspec-comparison.md` — OpenSpec 对比分析
- `references/methodology/agent-skill-execution-research.md` — Agent Skill 执行跑偏问题：根因分析 + 5种解决方案
- `references/methodology/superpowers-v5-changes.md` — Superpowers v5 关键变更及对 clsh-project 的影响

### 📋 模板（本地）
- `references/templates/constitution-template.md` — Constitution 模板（Phase 3 使用）
- `references/templates/archive-workflow.md` — Phase 7 归档操作手册
- `references/templates/cloud-server-wireguard.md` — 云服务器 + Wireguard 参考
- `references/templates/phase7-archive-checklist.md` — Phase 7 归档快速检查清单

### 🔌 集成（本地）
- `references/integration/kanban-tasks-bridge.md` — Kanban bridge 说明
- `references/integration/hermes-slash-command-mechanism.md` — Hermes 斜杠命令机制与插件化架构调研
- `references/integration/hermes-plugin-zero-token.md` — Hermes 插件零令牌路由架构
- `references/integration/hermes-plugin-hooks-reference.md` — Hermes 插件 hook 能力边界
- `references/integration/halo-auth.md` — Halo CMS Session-Based 认证
- `references/integration/halo-cli-auth.md` — Halo CLI Linux 无桌面环境认证
- `references/integration/reference-migration-pattern.md` — Reference 架构迁移模式：分类决策树 + 8 步迁移 + 过期检测

### 🔌 跨项目共享（wiki/reference/integration/，2026-05-21 迁移）
- `wiki/reference/integration/github-sync-guide.md` — GitHub 同步指南（仓库地址 + 推送命令）
- `wiki/reference/integration/lucky-api-format.md` — Lucky API 格式
- `wiki/reference/integration/php-env-pattern.md` — PHP 环境模式
- 追踪文件：`wiki/reference/.references-meta.json`

### ⚠️ 教训 — 流程违规（本地）
- `references/pitfalls/violation-case-2026-05-15.md` — 流程违规案例：跳步 + 自测
- `references/pitfalls/violation-case-2026-05-15-self-coding.md` — 灵犀直接写代码违规
- `references/pitfalls/violation-case-2026-05-18.md` — Phase 6 Kanban 状态同步 + 角色分离
- `references/pitfalls/violation-case-2026-05-20.md` — Phase 8 灵犀直接写代码违规

### ⚠️ 教训 — 流程管理指南（本地）
- `references/pitfalls/phase8-context-management.md` — Phase 8 上下文管理：批量读代码、checkpoint、中断恢复
- `references/pitfalls/phase8-session-management.md` — Phase 8 Session 管理：分批修复、避免上下文溢出
- `references/pitfalls/phase8-frontend-debug-patterns.md` — Phase 8 前端调试模式参考
- `references/pitfalls/memory-tool-traps-2026-05-21.md` — Memory 工具使用陷阱
- `references/pitfalls/technical-traps-2026-05-20.md` — 技术陷阱合集

### ⚠️ 教训 — 项目专属技术陷阱（wiki，2026-05-21 迁移）
- `wiki/projects/obsidian-workbench/references/pitfalls/trap-case-2026-05-20-share-html-and-emit.md` — share.html 风格遗漏 + Vue emit 陷阱
- `wiki/projects/obsidian-workbench/references/pitfalls/trap-case-2026-05-21-round6-frontend-patterns.md` — 前端修复模式（Toast/Heading ID/API 属性/独立页面）
- `wiki/projects/obsidian-workbench/references/pitfalls/trap-case-2026-05-21-round7-regex-dom-css.md` — Regex/DOM/CSS 陷阱
- 追踪文件：`wiki/projects/obsidian-workbench/.references-meta.json`

### 📎 项目专属集成参考（wiki，2026-05-21 迁移）
- `wiki/projects/clsh-content/references/integration/halo-obsidian-ref.md` — Halo 认证 + Obsidian CLI 参考
- 追踪文件：`wiki/projects/clsh-content/.references-meta.json`

## 流程说明

详见 `README.md`（skill 根目录）— 包含流程总览、各 Phase 详解、速查表、版本历史。
