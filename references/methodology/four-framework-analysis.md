# 四框架整合分析：gstack + Spec Kit + OpenSpec + Ralph Loop

> 调研时间：2026-06-03
> 目的：对比分析四大框架，识别 clsh-project 可借鉴的模式

---

## 一、框架概览

| 维度 | gstack (Gary Tan) | Spec Kit (GitHub) | OpenSpec (Fission-AI) | Ralph Loop (Huntley) |
|------|-------------------|-------------------|----------------------|---------------------|
| **定位** | 角色化 prompt 工程 | 可执行规范工具包 | 轻量 SDD 框架 | 自主迭代循环模式 |
| **核心机制** | 23 个 SKILL.md 角色切换 | 5 阶段斜杠命令管道 | propose→apply→archive | bash while 循环 + 新鲜 context |
| **Agent 模型** | 单实例角色切换 | 单 agent + 规范驱动 | 单 agent + 工件引导 | 单模型单任务单迭代 |
| **并行能力** | 通过 Conductor（外部工具） | 原生任务拆分 | 无 | 无（串行循环） |
| **记忆机制** | GBrain 知识库 | 文件系统 + .specify/ | 文件系统 + .openspec/ | 文件系统 + git |
| **验证方式** | Browser QA + /qa skill | 内置测试工作流 | 无内置验证 | **客观信号为唯一出口** |
| **Stars** | 106K | 108K | 52.5K | 2.9K (orchestrator) |
| **成熟度** | v1.55（活跃） | v0.9.2（刚起步） | v1.4.0（稳定） | 概念+工具（稳定） |

---

## 二、各框架核心洞察

### 1. gstack — 角色化是最强杠杆

**核心创新：** 不是"让 AI 写代码"，而是"让 AI 扮演 CEO/设计师/QA/发布经理"。

**关键模式：**
- **7 阶段工作流：** THINK → PLAN → BUILD → REVIEW → TEST → SHIP → REFLECT
- **SKILL.md 标准化：** 每个角色一个 SKILL.md，跨工具可移植（Claude Code / Codex / Copilot / Cursor）
- **Browser QA（/qa）：** 用浏览器自动化验证 UI，不是"代码看起来对"
- **/careful 安全模式：** Pre-Commit 安全自检（硬编码密钥、SQL 注入、shell 注入）
- **GBrain 持久知识库：** 8 种实体类型（用户画像、产品、目标等），brain-aware planning
- **Plan-Tune Cathedral：** 8 层 dream cycle distiller，从自由文本提取结构化提案

**clsh-project 差距：**
- ✅ 已借鉴：角色分离（coder/artist/tester）、Browser QA、Pre-Commit 自检
- ❌ 未借鉴：GBrain 知识库模式（当前用 wiki + solutions/，缺乏结构化实体）、SKILL.md 跨工具可移植性

### 2. Spec Kit — 规范即代码

**核心创新：** 规范不是"写了就扔"的文档，而是可执行的 — 直接生成实现。

**关键模式：**
- **5 阶段斜杠命令：** `/speckit.constitution` → `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`
- **Extension 系统：** 100+ 扩展（Jira 集成、代码审查、V-Model 测试追溯）
- **Preset 系统：** 组织级定制（合规格式、领域术语、安全审查门禁）
- **30+ agent 集成：** 统一规范格式，跨工具执行
- **Constitution 原则：** 项目治理原则作为所有决策的锚点

**clsh-project 差距：**
- ✅ 已借鉴：constitution.md、proposal.md、tasks.md 三件套
- ❌ 未借鉴：Extension/Preset 系统（当前硬编码在 SKILL.md）、斜杠命令标准化（当前用 /cp 别名）

### 3. OpenSpec — 轻量迭代

**核心创新：** 每个变更有独立文件夹（proposal + specs + design + tasks），做完归档。

**关键模式：**
- **Artifact-Guided Workflow：** 每个变更 = 一个文件夹，包含完整的决策链
- **三命令极简：** `/opsx:propose` → `/opsx:apply` → `/opsx:archive`
- **Brownfield 友好：** 设计用于已有项目，不只是绿地开发
- **社区 Schema：** 第三方可发布 opinionated 工作流

**clsh-project 差距：**
- ✅ 已借鉴：changes/ 目录结构（每个变更一个文件夹）、proposal → tasks 流程
- ❌ 未借鉴：极简命令入口（当前 Phase 0-8 门禁多，用户感知复杂）

### 4. Ralph Loop — 简单即力量

**核心创新：** 不需要复杂编排 — 一个 bash while 循环 + 新鲜 context + 客观验证 = 足够。

**关键模式：**
- **三大反模式：** Context Rot（上下文腐烂）、Premature Exit（过早退出）、Single-Pass Fragility（单次脆弱）
- **核心原则：** 一模型、一循环、一任务、一迭代。每次清空 context，重载规范。
- **外部记忆：** 文件系统 + git 是记忆层（不是 agent 的上下文）
- **客观验证为唯一出口：** 测试通过/linter 通过/覆盖率达标 — 不让 AI 自评
- **Backpressure Gates：** 拒绝未完成的工作（测试、lint、typecheck）
- **Hat 系统（Ralph Orchestrator）：** 单 agent 穿不同帽子（planner/builder），不是多 agent

**clsh-project 差距：**
- ✅ 已借鉴：Ralph Loop 状态机（Phase 6）、客观验证（5 步验证函数）、文件系统+git 记忆
- ❌ 未借鉴：Backpressure Gates（当前 worker 可以 kanban_complete 假装完成）、自改进 skill（每次运行后更新指令）

---

## 三、clsh-project 与四框架的映射

| clsh-project Phase | gstack 对应 | Spec Kit 对应 | OpenSpec 对应 | Ralph Loop 对应 |
|-------------------|-------------|---------------|---------------|----------------|
| Phase 0 准备 | /learn | /speckit.constitution | — | — |
| Phase 1 需求 | /office-hours + THINK | /speckit.specify | /opsx:propose | — |
| Phase 2 方案 | /plan-ceo-review | — | (proposal 阶段) | — |
| Phase 3 设计 | /design-consultation | /speckit.plan | (specs + design) | — |
| Phase 4 自检 | /plan-eng-review | — | — | — |
| Phase 5 计划 | — | /speckit.tasks | (tasks 阶段) | — |
| Phase 6 执行 | BUILD + /review | /speckit.implement | /opsx:apply | **Ralph Loop 核心** |
| Phase 7 归档 | /retro + /document | — | /opsx:archive | — |
| Phase 8 反馈 | /investigate | — | — | 循环迭代 |

---

## 四、clsh-project 可借鉴的 5 个高价值模式

### 模式 1：Backpressure Gates（Ralph Loop）

**问题：** worker 可以 kanban_complete(summary="done") 假装完成，灵犀无法阻止。
**借鉴：** Ralph Orchestrator 的 backpressure — 强制要求 evidence（测试通过、lint 通过、typecheck 通过）才能标记完成。
**落地：** kanban complete 前必须附带客观证据（exit code、截图路径、测试报告），无证据 = 自动 reject。

### 模式 2：自改进 Skill（Ralph Loop + gstack /learn）

**问题：** 教训记录到 ERRORS.md/learnings.md，但下次执行时不一定被读取。
**借鉴：** Ralph Loop 的 "skill/instruction file can be updated after each run" + gstack 的 /learn 命令。
**落地：** Phase 7 归档时自动更新 SKILL.md 的 Common Mistakes 节（不是写到外部文件，而是内嵌到对应 Phase）。

### 模式 3：Extension/Preset 系统（Spec Kit）

**问题：** clsh-project 硬编码了所有流程，无法按项目类型裁剪。
**借鉴：** Spec Kit 的 Extension（添加能力）和 Preset（覆盖模板）。
**落地：** 定义 project profile（web-app / cli-tool / content-site），每种 profile 有预设的 Phase 裁剪和默认 constitution。

### 模式 4：GBrain 结构化知识库（gstack）

**问题：** wiki/solutions/ 是自由文本，缺乏结构化匹配。
**借鉴：** gstack 的 GBrain — 8 种实体类型 + TTL + 字节预算 + 缓存层。
**落地：** solutions/ 中的 raw fix 记录增加结构化 frontmatter（domain/tech/error-type/reusability），Phase 0 匹配时用 frontmatter 过滤而非全文搜索。

### 模式 5：极简命令入口（OpenSpec）

**问题：** 用户需要记住 /clsh-project 继续 <项目名> 从 Phase N 开始 — 太复杂。
**借鉴：** OpenSpec 的三命令极简（propose → apply → archive）。
**落地：** 定义 3 个快捷命令：/cp（开始）、/cp 继续（续做）、/cp 归档（收尾），内部自动判断当前 Phase。

---

## 五、不借鉴的模式及原因

| 模式 | 来源 | 不借鉴原因 |
|------|------|-----------|
| 单实例角色切换 | gstack | clsh-project 用 kanban worker 物理隔离，比 prompt 角色切换更可靠 |
| 可执行规范生成代码 | Spec Kit | clsh-project 的规范是给 worker 看的，不是给生成器的；保持人审代码 |
| 多 agent 并行 | gstack/Conductor | 当前 kanban dispatcher 已支持 Wave 并行，不需要额外工具 |
| bash while 循环 | Ralph Loop | clsh-project 用 kanban 状态机替代，更可控（有 blocked/blocked/timeout） |
| 浏览器扩展 | gstack | clsh-project 用飞书交互，不需要浏览器扩展 |

---

## 六、整合建议

### 短期（可立即执行）

1. **Backpressure Gates** — kanban complete 前强制附带客观证据
2. **极简命令入口** — /cp /cp 继续 /cp 归档 三命令
3. **结构化 solutions frontmatter** — domain/tech/error-type/reusability

### 中期（需要设计）

4. **自改进 Skill** — Phase 7 归档时自动更新对应 Phase 的 Common Mistakes
5. **Project Profile** — 按项目类型裁剪 Phase（web-app vs content-site vs cli-tool）

### 长期（需要基础设施）

6. **GBrain 模式** — 结构化知识库 + TTL + 缓存层
7. **Extension 系统** — 允许项目自定义 Phase 流程

---

## 七、关键认知

1. **gstack 证明了"角色化"是最强杠杆** — 不是让 AI 写代码，而是让 AI 扮演角色。clsh-project 的 coder/artist/tester 角色分离与此一致。

2. **Spec Kit 证明了"规范即代码"的可行性** — 但 clsh-project 选择"规范给 worker 看"而非"规范自动生成代码"，因为人审代码是核心原则。

3. **OpenSpec 证明了"极简"是用户体验的关键** — clsh-project 的 8 Phase 门禁对灵犀是必要的，但对用户应该简化为 3 个命令。

4. **Ralph Loop 证明了"简单即力量"** — 一个 bash 循环 + 客观验证 > 复杂编排。clsh-project 的 Phase 6 状态机是 Ralph Loop 的结构化版本。

5. **四个框架的共同点：文件系统是真相源** — 不管用什么工具，规范/状态/记忆都在文件系统中。clsh-project 的 wiki + git + kanban 三层记忆与此一致。

6. **clsh-project 的独特优势：流程门禁 + 角色分离 + LLM 能力无关性** — 四个框架都没有强制的 Phase 门禁和独立 tester review。这是 clsh-project 的核心差异化。
