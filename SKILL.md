---
name: mimo-clsh-project
description: >
  规格驱动项目开发工作流 — 需求 → 设计 → 计划 → 执行。
  DO 触发：用户说"我想做一个X"、"开发一个X系统"、多步骤项目、新项目创建、大规模重构。
  Do NOT 触发：简单查询、单步操作、bug修复、小改动、纯信息性请求。
  Review 模式：用户说"review这个项目"或"审计已完成的工作"。
---

# 规格驱动项目开发

文档优先的刚性工作流：从模糊想法到交付代码。协调者协调，子代理执行，人类把关。无例外。

---

## Iron Law（铁律）

```
NO PHASE TRANSITION WITHOUT GATE APPROVAL
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
NO TASK MARKED DONE WITHOUT REVIEWER APPROVAL
```

违反铁律 = 说谎，不是高效。这不是建议，是绝对规则。

---

## 技能复用

本技能**复用** compose 已验证的工作流技能，不重复造轮子：

| Phase | 复用的 compose 技能 | 用途 |
|-------|---------------------|------|
| Phase 0-1 | `compose:brainstorm` | 需求探索、设计文档、用户确认 |
| Phase 2 | `compose:brainstorm` | 方案设计、权衡分析 |
| Phase 5 | `compose:plan` | 实施计划、任务分解、TDD 步骤 |
| Phase 6 | `compose:subagent` 或 `compose:execute` | 任务执行、子代理派发、两阶段 review |
| Phase 7 | `compose:review` + `compose:verify` | 代码审查、完成前验证 |
| Phase 8 | `compose:merge` | 分支收尾、合并决策 |

**使用方式：** 每个 phase 开始时，先加载 `mimo-clsh-project` 获取工作流上下文，再加载对应的 `compose:*` 技能执行具体操作。

---

## 核心原则

1. **协调者不写代码。** 用 Plan agent（`edit: deny`）强制执行此约束。
2. **角色分工。** 概念角色 ≠ MiMoCode agent 类型，见下方映射表。
3. **反理性化。** 7 层防御机制，详见下方。权限硬隔离 + prompt 软约束混合策略。
4. **文档优先。** 每个 phase 产出文档后才能进入下一 phase。决策写入文件，不依赖对话记忆。
5. **人类把关。** 每个 phase gate 用 `question` 工具获取用户确认。
6. **文件化进度。** 进度写入 ledger 文件，compaction 后从文件恢复，不从记忆恢复。
7. **持续执行。** Phase 内部不要暂停询问用户，除非遇到不可解决的阻塞。
8. **复用 compose。** 不重复造轮子，复用已验证的技能。

---

## 角色与 MiMoCode Agent 映射

| 概念角色 | 职责 | MiMoCode Agent | 权限配置 |
|---------|------|---------------|---------|
| **协调者** | 协调 phase、文档决策、委派任务、审查产出 | Plan agent | `edit: deny`, `bash: deny` |
| **编码者** | 实现功能、写代码、调试、重构 | Build agent | 全工具权限 |
| **艺术家** | UI/UX、前端实现、视觉设计 | Build agent（prompt 隔离） | 全工具权限 |
| **测试者** | 测试、代码审查、验证、质量保证 | 自定义 subagent | `edit: deny` |
| **侦察兵** | 调研、分析、技术评估 | Explore agent | 只读 |

**委派模板（使用 actor 工具）：**

```javascript
// 侦察兵调研 — explore 只读
actor({ operation: { action: "run", subagent_type: "explore",
  prompt: "调研任务描述", description: "简短描述" } })

// 编码者实现 — general 可写入
actor({ operation: { action: "run", subagent_type: "general",
  prompt: "实现任务描述", description: "简短描述", task_id: "T1" } })

// 测试者验证 — general 可读写
actor({ operation: { action: "run", subagent_type: "general",
  prompt: "测试任务描述", description: "简短描述" } })
```

---

## 目录结构

```
projects/<project-name>/
├── ledger.md                      # 进度账本（防 compaction 丢失）
├── overview.md                    # 状态跟踪
├── source-of-truth/
│   └── constitution.md            # 约束、禁止模式、验收标准
├── changes/
│   └── <YYYY-MM-DD>-<description>/
│       ├── conversation.md        # 需求决策与理由
│       ├── proposal.md            # 技术方案（2-3个）
│       ├── PRODUCT.md             # 产品不变量
│       ├── TECH.md                # 技术规范
│       └── tasks.md               # 实施计划与验证
└── archive/
    ├── completion-summary.md
    ├── retrospective.md
    └── handoff.md
```

### 文档映射表

| Phase | 产出文档 | 存放位置 | 必填/可选 |
|-------|----------|----------|-----------|
| Phase 0 | overview.md | projects/<name>/ | 必填 |
| Phase 0 | ledger.md | projects/<name>/ | 必填 |
| Phase 1 | conversation.md | projects/<name>/changes/<date>-<desc>/ | 必填 |
| Phase 2 | proposal.md | projects/<name>/changes/<date>-<desc>/ | 必填 |
| Phase 3 | PRODUCT.md | projects/<name>/changes/<date>-<desc>/ | 必填 |
| Phase 3 | TECH.md | projects/<name>/changes/<date>-<desc>/ | 必填 |
| Phase 4 | constitution.md | projects/<name>/source-of-truth/ | 必填 |
| Phase 5 | tasks.md | projects/<name>/changes/<date>-<desc>/ | 必填 |
| Phase 7 | completion-summary.md | projects/<name>/archive/ | 必填 |
| Phase 7 | retrospective.md | projects/<name>/archive/ | 必填 |
| Phase 7 | handoff.md | projects/<name>/archive/ | 可选 |

**文档完整性检查：** 使用 `templates/document-checklist.md` 跟踪文档完成状态。

### Ledger 文件格式（防 compaction 丢失）

```markdown
# Progress Ledger

## Completed Tasks
- [x] Phase 0: 需求准备 (commits abc1234..def5678, review clean)
- [x] Phase 1: 需求澄清 (commits def5678..ghi9012, review clean)
- [ ] Phase 2: 方案设计 (in progress)

## Current State
- Current Phase: 2
- Last Updated: 2025-01-15T10:30:00Z
- Human Approved Gates: Phase 0→1 ✓, Phase 1→2 ✓
```

**关键规则：** Compaction 后信任 ledger 和 git log，不信任自己的记忆。

---

## Phase 工作流

### Phase 0: 需求准备

<HARD-GATE>
Do NOT proceed to Phase 1 until: overview.md exists, conversation.md has initial request, and scout research is complete.
</HARD-GATE>

**目标：** 捕获原始请求，搭建项目工作区。

**复用：** 加载 `compose:brainstorm` 技能获取需求探索方法论。

**MUST 完成清单（按顺序）：**
1. 确定项目名称（询问用户或从请求推导）
2. 创建 `projects/<project-name>/` 目录结构
3. 创建 `overview.md`（初始状态）
4. 创建 `ledger.md`（进度账本）
5. 创建 `changes/<date>-<desc>/conversation.md`，记录原始请求
6. 委派侦察兵：调研问题域、现有方案、相关技术
7. **项目规模评估**：使用 `question` 工具询问以下问题，根据评估结果选择标准模式或轻量级模式：
   - 预计开发时间：< 1天 / 1-3天 / 3天以上
   - 预计代码行数：< 500行 / 500-2000行 / > 2000行
   - 团队人数：1人 / 2-3人 / 3人以上
   - 技术复杂度：简单（CRUD）/ 中等（有业务逻辑）/ 复杂（分布式、高并发）
   
   **评估规则：**
   - 如果所有答案都是第一项：建议使用轻量级模式（合并阶段）
   - 如果有任意答案是第三项：建议使用标准模式（完整8阶段）
   - 其他情况：用户自行选择

**产出：** 目录存在，初始请求已记录，侦察兵调研完成。

**Never：**
- 跳过侦察兵调研直接进入需求澄清
- 在 overview.md 中记录虚假的完成状态

**Anti-Pattern: "需求已经在对话里了，不需要记录"**
对话会随 compaction 丢失。conversation.md 是唯一持久化的需求记录。没有 conversation.md = 需求不存在。

**REQUIRED NEXT STEP:** 完成后用 `question` 工具让人类确认进入 Phase 1。确认后执行 `/compact`，然后从文件重读上下文。**Phase 1 需加载 `compose:brainstorm` 技能。**

---

### Phase 1: 需求澄清

<HARD-GATE>
Do NOT proceed to Phase 2 until: conversation.md has complete 5-dimension answers AND human has approved via question tool.
</HARD-GATE>

**目标：** 用 5 维度提问框架将模糊请求转化为精确、可测试的需求。

**MUST 完成清单（按顺序）：**
1. 读取 conversation.md（从文件恢复上下文）
2. 对每个维度提出 3-5 个具体问题
3. 用 `question` 工具逐个向用户提问
4. 将所有回答记录到 conversation.md
5. 生成需求摘要
6. 用 `question` 工具让人类确认需求摘要

| # | 维度 | 要回答的问题 |
|---|------|-------------|
| 1 | **谁** | 用户是谁？谁维护？谁受影响？ |
| 2 | **什么** | 解决什么问题？不变量是什么？边界情况？ |
| 3 | **如何** | 如何集成？如何部署？如何测试？ |
| 4 | **范围** | 明确排除什么？Phase 1 vs 后续？ |
| 5 | **成功** | 如何证明可行？什么指标重要？ |

**产出：** `conversation.md` 包含 5 维度完整需求。

**Never：**
- 跳过任何维度
- 用"我认为用户想要..."代替直接询问
- 在需求未确认前开始设计

**Anti-Pattern: "需求很明确了，不需要 5 维度"**
"明确"的需求是最可能出错的需求。5 维度框架是强制的，不是可选的。

**REQUIRED NEXT STEP:** 完成后用 `question` 工具让人类确认。确认后执行 `/compact`，然后读取 conversation.md 和 overview.md。

---

### Phase 2: 方案设计

<HARD-GATE>
Do NOT proceed to Phase 3 until: proposal.md has 2+ approaches with trade-offs AND human has selected via question tool.
</HARD-GATE>

**目标：** 生成 2-3 个技术方案，含权衡分析。

**MUST 完成清单（按顺序）：**
1. 读取 conversation.md 和 overview.md（从文件恢复上下文）
2. 头脑风暴 2-3 个不同技术路径
3. 每个方案记录：架构、技术选型理由、权衡、风险、工作量
4. 可选：委派侦察兵做技术 spike（`--fork` 分叉探索）
5. 用 `question` 工具让用户选择方案
6. 将选择记录到 proposal.md

**产出：** `proposal.md` 含 2-3 个分析方案，最终选择已记录。

**Never：**
- 只提出一个方案
- 跳过权衡分析
- 在用户选择前自行决定方案

**Anti-Pattern: "只有一种合理方案，不需要比较"**
LLM 倾向于输出最熟悉的方案。强制比较 2-3 个方案是为了暴露隐含假设。

**REQUIRED NEXT STEP:** 完成后用 `question` 工具让人类选择。确认后执行 `/compact`，然后读取 proposal.md、conversation.md、overview.md。**Phase 3 需加载 `compose:brainstorm` 技能（设计文档部分）。**

---

### Phase 2.5: 技术 Spike（可选）

**触发：** 选定方案涉及不确定技术或高风险。

委派侦察兵或编码者，范围严格限定，时间盒约束。结果记录在 `conversation.md`。

---

### Phase 3: 设计文档

<HARD-GATE>
Do NOT proceed to Phase 4 until: PRODUCT.md and TECH.md are complete AND human has approved via question tool.
</HARD-GATE>

**目标：** 产出权威设计文档。

**MUST 完成清单（按顺序）：**
1. 读取 conversation.md、proposal.md、overview.md（从文件恢复上下文）
2. 委派编码者起草 TECH.md
3. 协调者审查 TECH.md 完整性
4. 起草 PRODUCT.md（功能需求、非功能需求、用户故事、验收标准）
5. 用 `question` 工具让人类审批两个文档
6. 将批准记录到 overview.md

**产出：** `PRODUCT.md` 和 `TECH.md` 已获人类批准。

**Never：**
- PRODUCT.md 和 TECH.md 未经人类批准就进入 Phase 4
- TECH.md 缺少架构图或数据模型
- PRODUCT.md 缺少验收标准

**Anti-Pattern: "设计文档太长了，我先写代码"**
设计文档是实施的唯一依据。没有批准的设计文档 = 没有设计 = 不能开始编码。

**REQUIRED NEXT STEP:** 完成后用 `question` 工具让人类批准。确认后执行 `/compact`，然后读取 PRODUCT.md、TECH.md、conversation.md、proposal.md、overview.md。**Phase 4 需要自检，无需额外 compose 技能。**

---

### Phase 4: 宪法与自检

<HARD-GATE>
Do NOT proceed to Phase 5 until: constitution.md exists AND self-check checklist passes AND human has approved via question tool.
</HARD-GATE>

**目标：** 创建不可协商的约束文档，验证所有前期工作。

**MUST 完成清单（按顺序）：**
1. 读取所有前序文档（从文件恢复上下文）
2. 创建 `constitution.md`（使用 constitution-template.md 作为模板），必须包含：
   - 硬约束
   - **软偏好处理**：每个软偏好必须标记为"升级为硬约束"或"排除+理由"，不允许"暂时搁置"
   - 禁止模式
   - **环境约束**：development/staging/production 配置差异表
   - 通用验收标准
3. 运行自检清单（逐项验证）
4. 修复所有失败项
5. 用 `question` 工具让人类确认自检结果

**自检清单（MUST 全部通过）：**
```
[ ] overview.md 存在且状态最新
[ ] conversation.md 有完整 5 维度回答
[ ] proposal.md 有 2+ 方案及选择理由
[ ] PRODUCT.md 列出所有功能和非功能需求
[ ] TECH.md 指定架构、数据模型、集成点
[ ] constitution.md 定义约束和验收标准
[ ] 所有文档一致（无矛盾）
[ ] 所有用户确认的决策已记录
[ ] 范围边界明确（IN 和 OUT）
[ ] PRODUCT.md 每个用户故事在 tasks.md 中有对应任务（双向追溯）
[ ] constitution.md 包含环境约束（dev/staging/production）
[ ] constitution.md 软偏好已明确处理（升级为硬约束 or 明确排除+理由）
```

**产出：** `constitution.md` 创建，自检通过，人类批准。

**Never：**
- 自检清单有失败项但继续前进
- constitution.md 缺少可执行的验证命令
- 跳过人工确认

**Anti-Pattern: "自检只是形式，核心是编码"**
自检是防止前期错误传播到实施阶段的最后机会。跳过自检 = 允许错误进入代码。

**REQUIRED NEXT STEP:** 完成后用 `question` 工具让人类确认。确认后执行 `/compact`，然后读取 PRODUCT.md、TECH.md、constitution.md、overview.md。**Phase 5 需加载 `compose:plan` 技能。**

---

### Phase 5: 实施计划

<HARD-GATE>
Do NOT proceed to Phase 6 until: tasks.md has complete acceptance criteria with verification commands AND human has confirmed via question tool.
</HARD-GATE>

**目标：** 将设计分解为有序、可执行的任务。

**复用：** 加载 `compose:plan` 技能获取任务分解方法论（bite-sized tasks、TDD 步骤、exact file paths）。

**MUST 完成清单（按顺序）：**
1. 读取 PRODUCT.md、TECH.md、constitution.md、overview.md（从文件恢复上下文）
2. 委派编码者生成 `tasks.md`（遵循 writing-plans 的任务格式）
3. 审查 tasks.md：
   - 每个任务有 ID、角色、依赖、验收标准、验证命令
   - 任务按依赖排序
   - 每个任务有范围排除
   - 每个任务有 exact file paths（来自 writing-plans）
   - **双向追溯验证**：PRODUCT.md 每个用户故事在 tasks.md 有对应任务（检查追溯矩阵）
   - **双向追溯验证**：tasks.md 每个任务关联到 PRODUCT.md 的用户故事（无孤立任务）
4. 用 `question` 工具让人类确认任务计划
5. 更新 ledger.md

**任务格式：**
```markdown
## Task T001: <标题>
- **Role:** coder | artist | tester | scout
- **Dependencies:** none | T001, T002
- **Goal:** <目标>
- **Scope:** <做什么>
- **Exclusions:** <不做什么>
- **Acceptance Criteria:**
  1. <可测试标准>
  2. <验证命令>
- **Files:** <涉及文件>
```

**产出：** `tasks.md` 已获人类批准。

**Never：**
- 任务没有验证命令
- 任务范围排除为空
- 任务之间依赖关系不清晰

**Anti-Pattern: "任务太简单不需要验收标准"**
没有验收标准的任务 = 无法验证完成 = 永远不会真正完成。

**REQUIRED NEXT STEP:** 完成后用 `question` 工具让人类确认。确认后执行 `/compact`，然后读取 tasks.md、constitution.md、TECH.md、overview.md。**Phase 6 需加载 `compose:subagent` 和 `compose:verify` 技能。**

---

### Phase 6: 执行

<HARD-GATE>
Do NOT mark any task as done without: (1) verification evidence from bash output, (2) reviewer approval, (3) ledger update.
</HARD-GATE>

**目标：** 按依赖顺序执行任务。

**复用：**
- 加载 `compose:subagent` 技能获取子代理派发和两阶段 review 方法论
- 加载 `compose:verify` 技能获取验证铁律

**MUST 完成清单（每个任务）：**
1. 验证所有依赖已完成（检查 ledger.md）
2. 读取 tasks.md、constitution.md、TECH.md、overview.md
3. 委派编码者（使用 actor 工具，指定 subagent_type）
4. 接收编码者产出：diff、测试输出、自审结果
5. **验证证据**：运行验证命令，检查 bash 输出（Iron Law: 没有证据 = 没有完成）
6. **两阶段 Review**（来自 subagent-driven-development）：
   - 规格合规审查：实现是否符合 tasks.md 的验收标准
   - 代码质量审查：代码是否符合 TECH.md 的架构约束
7. 更新 ledger.md：`- [x] Task T001: 完成 (commits abc..def, review clean)`
8. 更新 overview.md

**委派 prompt 模板（强制格式）：**
```
## 强制前置步骤（不可跳过）
1. 使用 skill 工具加载 "mimo-clsh-project"
2. 使用 skill 工具加载 "compose:plan" 或 "compose:verify"（根据任务类型）
3. 读取 tasks.md、constitution.md、TECH.md 获取上下文

## 角色
你是 <角色>。

## Task <ID>: <标题>
### 目标
<要实现什么>

### 上下文
<嵌入 PRODUCT.md、TECH.md、constitution.md 相关部分>

### 约束
<从 constitution.md 列出相关约束>

### 验收标准
<从 tasks.md 列出>

### 范围排除
<从 tasks.md 列出>

### 验证（必须执行并返回输出）
<完成后的验证命令>

## 完成后必须返回
1. 验证命令的完整 bash 输出（不是摘要，是原始输出）
2. 修改的文件列表
3. 是否通过自检：是/否
```

**协调者审查时 MUST 检查：**
- [ ] 子代理是否加载了正确的技能
- [ ] 返回的验证输出是否包含实际命令执行结果（不是"测试通过"文字）
- [ ] 如果是测试任务，输出必须包含测试运行结果，不是"测试文件已创建"

**两阶段 Review 流程：**
```
编码者完成 → 生成 diff → 派发审查者 subagent
审查者报告：
  - 规格合规: ✅ 或 ❌
  - 代码质量: ✅ 或 ❌
两个维度都 ✅ 才能标记完成
任何 ❌ 必须修复后重新审查
```

**子代理契约：**
- 返回：完成摘要、修改文件、验证输出
- 不得：做架构决策、跳过测试、忽略范围排除
- 遇到歧义：必须停止并报告，不得猜测

**Never：**
- 接受编码者"应该能工作"的声明而没有运行验证命令
- 接受"测试文件已创建"作为测试完成的证据（必须运行测试并返回输出）
- 跳过 review 直接标记完成
- 在 review 有 Critical/Important 问题时继续下一个任务
- 用对话记忆判断任务状态，必须查 ledger.md

**Anti-Pattern: "测试通过了，代码看起来没问题"**
"看起来没问题" 不是证据。运行验证命令，检查输出，然后才能声称完成。

**Anti-Pattern: "测试文件已创建"**
创建测试文件 ≠ 测试通过。必须运行 `phpunit`/`vitest` 并返回实际输出。没有输出 = 测试未执行 = 任务未完成。

**REQUIRED NEXT STEP:** 所有任务完成后，派发最终 whole-branch review（使用 `compose:review` 模板）。然后执行 `/compact`。**Phase 7 需加载 `compose:review`、`compose:verify` 和 `compose:merge` 技能。**

---

### Phase 7: 归档与复盘

<HARD-GATE>
Do NOT close the project until: completion-summary.md, retrospective.md exist AND human has confirmed via question tool.
</HARD-GATE>

**目标：** 清理、文档化、准备未来参考。

**复用：**
- 加载 `compose:review` 技能获取最终 whole-branch review 方法论
- 加载 `compose:verify` 技能获取完成前验证铁律
- 加载 `compose:merge` 技能获取分支收尾流程

**MUST 完成清单（按顺序）：**
1. 读取 overview.md、ledger.md、changes/ 下所有文档
2. 派发最终 whole-branch review（使用 requesting-code-review 模板）
3. 创建 `archive/completion-summary.md`（交付内容 vs 计划、偏差、已知问题）
4. 创建 `archive/retrospective.md`（做得好/不好、改进项）
5. 更新 `overview.md` 为"已完成"
6. 创建 `archive/handoff.md`（如需维护）
7. 用 `question` 工具让人类确认归档完成

**产出：** 项目完整文档化，已归档。

**Never：**
- 没有 completion-summary 就归档
- retrospective 只写"做得好"不写"做得不好"

**REQUIRED NEXT STEP:** 完成后用 `question` 工具让人类确认。进入 Phase 8。

---

### Phase 8: 反馈循环

**目标：** 捕获经验，决定下一步。

**模式选择：**
- **单次决策**：用 `question` 工具询问：新项目（→Phase 0）| 迭代（→Phase 1）| 审查（Review 模式）| 结束
- **迭代收敛**：使用 `/goal` 命令设置停止条件，LLM 自动判断何时完成（适用于多轮修复、反馈循环）

**`/goal` 使用场景：**
| 场景 | 适合 | 原因 |
|------|:---:|------|
| Phase 8 反馈循环 | ✅ | 多轮迭代，LLM 判断"还有问题吗" |
| 修复卡（bug fix） | ✅ | 迭代直到收敛，节省来回开销 |
| Review 模式修复 | ✅ | 同 Phase 8 结构 |
| Phase 1-6 完整流程 | ❌ | 终止权在人（确认码），单次任务 |

---

## 7 层防跳步机制

### 第 1 层：HARD-GATE 标签

每个 phase 转换处标记 `<HARD-GATE>`，明确列出不可跳过的前置条件。

### 第 2 层：MUST 检查清单

每个 phase 有编号的 MUST 完成清单，必须按顺序完成。

### 第 3 层：REQUIRED NEXT STEP

每个 phase 结尾声明下一个必须执行的步骤，形成链式调用。

### 第 4 层：Anti-Pattern 显式禁用

每个 phase 有 Anti-Pattern 小节，直接引用 LLM 的常见理性化借口并禁用。

### 第 5 层：文件化进度 Ledger

进度写入 `ledger.md`，compaction 后从文件恢复。规则：信任 ledger 和 git log，不信任记忆。

### 第 6 层：两阶段 Review

每个任务完成后：规格合规审查 + 代码质量审查。两个维度都 ✅ 才能继续。

### 第 7 层：Never 列表

每个 phase 有明确的 Never 列表，列出绝对禁止的行为。

### 第 8 层：反理性化扩展机制

**目标：** 持续维护反理性化表格，防御新出现的 LLM 跳步借口。

**机制：**
1. **定期审查：** 每个项目复盘时，检查是否有新的 LLM 合理化借口出现。
2. **扩展流程：** 发现新借口时，按以下格式添加到 `references/anti-rationalization-patterns.md`：
   ```
   ### Pattern N: "新借口标题"
   **触发场景：** 描述触发条件
   **LLM 逻辑：** LLM 如何合理化跳步
   **真实后果：** 实际危害
   **阻止方式：** 具体防御措施
   ```
3. **同步更新：** 同步更新 SKILL.md 中的“Anti-Pattern”小节（如有必要）。
4. **社区贡献：** 鼓励用户提交新的反理性化模式。

**维护责任：** 协调者负责在 Phase 8（反馈循环）中审查并更新反理性化表格。

---

## 硬规则 vs 软规则分离

**核心原则：** 确定性交给代码，判断力交给被代码显式调用的模型。

### 规则分类

| 规则类型 | 性质 | 本技能对应 | 验证方式 |
|----------|------|------------|----------|
| **硬规则** | 确定性机判 | 文件存在性、关键词匹配、文档完整性 | bash 命令验证 |
| **软规则** | LLM 判断 | 需求合理性、代码质量、架构决策 | compose:verify / /goal |

### 硬规则验证（推荐）

每个 phase 的关键检查点，优先使用可执行的 bash 命令验证：

| Phase | 硬规则验证示例 |
|-------|----------------|
| Phase 0 | `ls projects/<name>/overview.md` |
| Phase 1 | `grep -c "维度" conversation.md` |
| Phase 2 | `grep -c "方案" proposal.md` |
| Phase 3 | `ls PRODUCT.md TECH.md` |
| Phase 4 | `grep -c "MUST" constitution.md` |
| Phase 5 | `grep -c "验收标准" tasks.md` |
| Phase 6 | `git diff --stat` |
| Phase 7 | `ls archive/completion-summary.md` |

### 软规则判断

以下场景使用 LLM 判断，不应用脚本模拟：
- 需求是否合理
- 代码质量是否达标
- 架构决策是否正确
- 用户是否满意

---

## MiMoCode 环境集成

### 项目配置

在项目根目录创建 `.mimocode/config.json` 集中管理配置：

```json
{
  "project_docs_dir": "./projects/<project-name>",
  "mode": "standard",
  "verify_method": "bash",
  "goal_enabled": true
}
```

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `project_docs_dir` | 项目文档目录 | `./projects/<project-name>` |
| `mode` | 工作流模式（standard/lightweight） | `standard` |
| `verify_method` | 验证方式（bash/script） | `bash` |
| `goal_enabled` | 是否启用 /goal 停止条件 | `true` |

### 上下文管理（/compact + 文件重读）

每个 phase gate 确认后执行 `/compact`，然后从文件重读上下文：

```
1. /compact（压缩前一 phase 对话）
2. Read ledger.md（从文件恢复进度）
3. Read overview.md（确认当前状态）
4. Read 本 phase 所需全部文档
5. 确认无遗漏
6. 开始执行
```

每个 phase 需读取的文件：

| Phase | 需读取的文件 |
|-------|-------------|
| 0 | （新建项目，无需恢复） |
| 1 | conversation.md, ledger.md |
| 2 | conversation.md, overview.md, ledger.md |
| 3 | conversation.md, proposal.md, overview.md, ledger.md |
| 4 | PRODUCT.md, TECH.md, conversation.md, proposal.md, overview.md, ledger.md |
| 5 | PRODUCT.md, TECH.md, constitution.md, overview.md, ledger.md |
| 6 | tasks.md, constitution.md, TECH.md, overview.md, ledger.md |
| 7 | overview.md, ledger.md, tasks.md, changes/ 下所有文档 |
| 8 | overview.md, ledger.md, retrospective.md |

### Session 管理

| 场景 | 操作 |
|------|------|
| 跨天项目 | `mimo --continue` 恢复 |
| 尝试新方案 | `mimo --continue --fork` 分叉 |
| 长上下文 | `/compact` 压缩 |

### 权限与反理性化混合策略

| 层级 | 策略 | 配置 |
|------|------|------|
| **权限硬隔离** | 协调者不写代码 | `agent.plan.permission.edit: "deny"` |
| **权限硬隔离** | 测试者不改代码 | 自定义 agent `edit: deny` |
| **Prompt 软约束** | 每任务必须有验证命令 | task 模板硬编码 Acceptance Criteria 格式 |
| **Prompt 软约束** | 独立 review | 角色定义 + 反理性化表 |
| **Prompt 软约束** | Gate 审批 | question 工具 + phase gate 检查 |

详细反理性化模式见 references/anti-rationalization.md。

---

## 优化方案详细说明

### 方案1：文档结构优化

**问题：** 文档存放位置说明可以更清晰，模板可增加灵活性。

**解决方案：**

1. **文档映射表：** 在 SKILL.md 中增加“文档映射表”，明确每阶段产出与存放位置的对应关系。
2. **可选字段标记：** 在模板中增加“可选字段”标记（如 `[optional]`），让用户根据项目规模选择。
3. **文档清单模板：** 创建 `templates/document-checklist.md`，帮助用户跟踪文档完整性。

**实施步骤：**
1. 在 SKILL.md 的“目录结构”部分增加文档映射表。
2. 修改 `templates/` 目录下的模板文件，增加可选字段标记。
3. 创建 `templates/document-checklist.md`。

**示例文档映射表：**
```markdown
| Phase | 产出文档 | 存放位置 | 必填/可选 |
|-------|----------|----------|-----------|
| Phase 0 | overview.md | projects/<name>/ | 必填 |
| Phase 0 | ledger.md | projects/<name>/ | 必填 |
| Phase 1 | conversation.md | projects/<name>/changes/<date>-<desc>/ | 必填 |
| Phase 2 | proposal.md | projects/<name>/changes/<date>-<desc>/ | 必填 |
| Phase 3 | PRODUCT.md | projects/<name>/changes/<date>-<desc>/ | 必填 |
| Phase 3 | TECH.md | projects/<name>/changes/<date>-<desc>/ | 必填 |
| Phase 4 | constitution.md | projects/<name>/source-of-truth/ | 必填 |
| Phase 5 | tasks.md | projects/<name>/changes/<date>-<desc>/ | 必填 |
| Phase 7 | completion-summary.md | projects/<name>/archive/ | 必填 |
| Phase 7 | retrospective.md | projects/<name>/archive/ | 必填 |
| Phase 7 | handoff.md | projects/<name>/archive/ | 可选 |
```

### 方案2：流程简化

**问题：** 9阶段流程对小项目可能过重。

**解决方案：**

1. **轻量级模式：** 增加“轻量级模式”选项，合并某些阶段。
2. **项目规模评估：** 在 Phase 0 增加项目规模评估，根据评估结果选择标准模式或轻量级模式。

**轻量级模式阶段合并：**
- **标准模式：** Phase 0-8（完整9阶段流程）
- **轻量级模式：** 
  - Phase 0-2 → “需求与设计”（合并为1个阶段）
  - Phase 3-4 → “约束与分析”（合并为1个阶段）
  - Phase 5-6 → “计划与执行”（合并为1个阶段）
  - Phase 7-8 → “归档与反馈”（合并为1个阶段）

**实施步骤：**
1. 在 SKILL.md 的“Phase 工作流”部分增加“轻量级模式”说明。
2. 在 Phase 0 增加项目规模评估问题。
3. 根据评估结果，指导用户选择标准模式或轻量级模式。

**项目规模评估问题：**
```
项目规模评估：
1. 预计开发时间：< 1天 / 1-3天 / 3天以上
2. 预计代码行数：< 500行 / 500-2000行 / > 2000行
3. 团队人数：1人 / 2-3人 / 3人以上
4. 技术复杂度：简单（CRUD）/ 中等（有业务逻辑）/ 复杂（分布式、高并发）

根据评估结果：
- 如果所有答案都是第一项：建议使用轻量级模式
- 如果有任意答案是第三项：建议使用标准模式
- 其他情况：用户自行选择
```

### 方案3：团队协作

**问题：** 当前主要面向单人开发者，缺乏团队协作指导。

**解决方案：**

1. **角色分配指南：** 增加团队角色分配指南。
2. **冲突处理机制：** 增加并行任务冲突处理机制。
3. **协作工具集成：** 增加与协作工具（如 GitHub Issues、Jira）的集成建议。

**团队角色分配指南：**
```markdown
## 团队角色分配

### 小型团队（2-3人）
- **协调者：** 项目经理或技术负责人
- **编码者：** 1-2名开发人员
- **测试者：** 开发人员兼任（但必须独立于编码者）
- **侦察兵：** 开发人员兼任

### 中型团队（4-6人）
- **协调者：** 项目经理
- **编码者：** 2-3名开发人员
- **艺术家：** 1名UI/UX设计师
- **测试者：** 1名QA工程师
- **侦察兵：** 1名技术研究员

### 大型团队（7人以上）
- **协调者：** 项目经理 + 技术负责人
- **编码者：** 多个开发小组
- **艺术家：** UI/UX设计团队
- **测试者：** QA团队
- **侦察兵：** 技术研究小组
```

**冲突处理机制：**
```markdown
## 并行任务冲突处理

### 冲突预防
1. **文件锁机制：** 在 tasks.md 中明确每个任务的“文件锁”（哪些文件只能由该任务修改）。
2. **依赖检查：** 派发任务前，检查新任务与进行中任务的文件重叠。
3. **通信协议：** 团队成员在修改共享文件前，必须通知协调者。

### 冲突解决
1. **识别冲突：** 通过代码审查或文件修改历史发现冲突。
2. **评估影响：** 协调者评估冲突的影响范围。
3. **重新分配：** 根据冲突情况，重新分配任务或调整顺序。
4. **合并变更：** 使用版本控制工具合并变更，解决冲突。
```

### 方案4：反理性化扩展

**问题：** 需要持续维护反理性化表格，防御新出现的 LLM 跳步借口。

**解决方案：** （已在第8层防跳步机制中详细说明）

### 方案5：版本控制集成

**问题：** 缺乏与版本控制工具（如 Git）的集成指导。

**解决方案：**

1. **Git 工作流集成：** 增加与 Git 工作流的集成指导。
2. **提交规范：** 增加提交信息规范。
3. **分支策略：** 增加分支策略建议。

**Git 工作流集成：**
```markdown
## Git 工作流集成

### 分支策略
- **main/master：** 稳定版本，只接受经过 review 的合并
- **develop：** 开发分支，集成所有已完成任务
- **feature/<task-id>：** 每个任务一个分支，任务完成后合并到 develop
- **release/<version>：** 发布分支，用于版本发布

### 提交规范
```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型（type）：**
- feat：新功能
- fix：修复bug
- docs：文档更新
- style：代码格式（不影响功能）
- refactor：重构
- test：测试
- chore：构建过程或辅助工具的变动

**示例：**
```
feat(user): 实现用户登录功能

- 添加用户登录API
- 添加JWT token验证
- 添加用户模型

Closes #123
```

### 工作流程
1. **开始任务：** 从 develop 创建 feature/<task-id> 分支
2. **完成任务：** 在 feature/<task-id> 分支上完成开发
3. **提交更改：** 按照提交规范提交更改
4. **创建PR：** 创建 Pull Request 到 develop 分支
5. **代码审查：** 至少一名团队成员审查
6. **合并：** 审查通过后合并到 develop
7. **删除分支：** 合并后删除 feature/<task-id> 分支

### 版本发布
1. **创建发布分支：** 从 develop 创建 release/<version> 分支
2. **测试：** 在发布分支上进行最终测试
3. **修复问题：** 修复测试中发现的问题
4. **合并到 main：** 测试通过后合并到 main
5. **打标签：** 在 main 分支上打版本标签
6. **合并回 develop：** 将发布分支合并回 develop
```

**实施步骤：**
1. 在 SKILL.md 中增加“版本控制集成”章节。
2. 提供 Git 工作流模板。
3. 提供提交信息规范模板。
4. 提供分支策略模板。

---

## Phase Gates 速查

| 转换 | Gate 条件 |
|------|----------|
| Phase 0 → 1 | overview.md 存在，conversation.md 有初始请求，侦察兵调研完成 |
| Phase 1 → 2 | conversation.md 有完整 5 维度回答，question 工具确认 |
| Phase 2 → 3 | proposal.md 有 2+ 方案，question 工具选择 |
| Phase 3 → 4 | PRODUCT.md 和 TECH.md 完成，question 工具批准 |
| Phase 4 → 5 | constitution.md 存在，自检通过，question 工具确认 |
| Phase 5 → 6 | tasks.md 有完整验收标准和验证命令，question 工具确认 |
| Phase 6 → 7 | 所有任务完成，两阶段 review 通过，最终 review 通过 |
| Phase 7 → 8 | 归档文档完成，question 工具确认 |
| Phase 8 → done | 人类决定停止 |
| Phase 8 → 0 | 人类决定启动新项目 |

---

## 模板与参考

**模板：** 见 `templates/` 目录。

**主要模板：**
- `templates/overview-template.md` — 项目状态跟踪器模板（含项目模式选择）
- `templates/document-checklist.md` — 文档完整性检查清单
- `templates/conversation-template.md` — 需求对谈记录模板（含可选字段）
- `templates/tasks-md-template.md` — 实施计划模板（含可选字段）
- `templates/product-md-template.md` — 产品规格模板（含可选字段）
- `templates/tech-md-template.md` — 技术规格模板（含可选字段）

**详细参考：**
- 反理性化模式 → references/anti-rationalization.md
- 常见陷阱 → references/pitfalls/common.md
- 流程图 → references/workflow/overview.md
- Review 详细流程 → references/workflow/phase-review.md
