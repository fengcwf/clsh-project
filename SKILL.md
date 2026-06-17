---
name: clsh-project
aliases: [cp]
description: "需求驱动的项目开发工作流 — 从需求澄清到设计文档到实现计划到执行。灵感来自 Kiro Spec-Driven Development、Superpowers Brainstorming、Phoenix 状态机执行。DO trigger: 用户说'我要做一个 XXX'、'开发一个 XXX 系统'、'/clsh-project'、'/cp'、需求明显是多步骤项目。Do NOT trigger: 简单查询、单步操作、修 bug（用 systematic-debugging）、已有明确方案的小改动、用户说'简单做一下'、代码质量审查。"
version: 6.0.0-generic
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

## 概述

当用户提出新的项目或功能需求时，**不直接写代码**，走完整 需求→设计→计划→执行 流程。

**核心理念（Kiro + Superpowers + Phoenix）：**
- 需求不能跳到编码 — 必须经过需求澄清 → 设计 → 计划
- 文档是锚点 — 防止进度丢失和跑偏
- 分阶段审批 — 每阶段需用户确认后才进入下一阶段
- 一次只问一个问题 — 不要一次性抛出多个问题
- 两阶段 review（Superpowers）：先 spec compliance，再 code quality
- 状态机执行（Phoenix）：每个 Task 有 checkpoint、验证条件、失败阻断

## 📁 路径约定

> **所有路径通过 config.json 的 `project_docs_dir` 配置，默认 `./project-docs/`。**
> 迁移时修改 config.json 即可，无需改 SKILL.md。

## 边界定义

### 管什么
- 流程编排（Phase 1-8 门禁和流转）
- 角色分离（协调者 ≠ coder）
- 质量保障（checkpoint + review）
- 文档管理

### 不管什么
- 具体技术实现细节 → `references/pitfalls-common.md`
- 调试方法论 → `systematic-debugging` skill
- 代码质量规则 → `code-principles` skill

### 膨胀阈值
- SKILL.md: ≤ 700 行
- Pitfalls: ≤ 30 条（内嵌高频 + 外置完整版）

## 🛡️ LLM 能力无关性原则

**流程控制不依赖 LLM 判断力。** LLM 强时和 LLM 弱时，流程应产出一致的结果。

| 类型 | 谁判断 | 用于 | 不得用于 |
|------|--------|------|---------|
| **机械判断** | 代码/脚本/硬编码 | 门禁检查、轮次上限、状态流转、文件存在性 | — |
| **用户判断** | 需求方 | 方案选择、设计确认、优先级裁决 | 可自动化的验证步骤 |
| **LLM 判断** | agent | 内容生成、格式化、信息整理 | 流程控制、质量门禁 |

## ⛔ 流程规则（三层架构）

> **设计原则：**
> 1. **能纯机械不用 LLM** — 有脚本检查的用脚本，不靠 LLM 自觉
> 2. **角色严格分离** — 协调者只做信息传递，coder/artist 自己分析+执行

### Layer 1: Gate（门禁，违反 = 流程阻断）

> **Gate 脚本随 skill 分发（`scripts/gate-phase*.py`），用户运行 `python3 scripts/env-check.py` 即可验证环境。**

| # | 规则 | 机械机制 |
|---|------|---------|
| G0 | **先查进度再行动** — `ls` + 读 overview.md + 读 changes/，从下一个未完成 Phase 继续 | 文件系统检查 |
| G1 | **文档先于代码** — Phase 3 未完成 + 用户未确认，禁止写代码 | 文件存在性检查 |
| G2 | **Phase 4 预检** — 必须用 `gate-phase4.py`（内嵌码生成），检查 Phase 3 产出物存在性+关键词+行数 | 脚本 PASS/FAIL + 码生成（原子化） |
| G3 | **机械确认码** — 必须用门禁脚本生成码（hash(检查结果)+salt），禁止手动生成 | 脚本输出（不可伪造） |
| G6 | **文档路径验证** — 写入后必须 `ls` 验证 | `ls` 输出 |
| G7 | **C7 review 报告门禁** — 跑 `gate-phase7.py`，检查 fresh-context reviewer 报告 | 脚本 PASS/FAIL |

### Layer 2: Convention（架构约束）

| # | 规则 | 执行方式 |
|---|------|---------|
| C0 | **角色分离：协调者只记录，不分析** — Phase 8 协调者只记录现象+文件+验收标准，coder 自己分析根因 | 架构约束 |
| C1 | **Phase 5 派 coder 写 tasks** — 协调者派任务（body 含 proposal + constitution 路径），coder 自己写 tasks.md | 任务派发 |
| C2 | **proposal 只写设计决策** — 功能清单/API 合约/数据模型/架构约束/文件范围，不写实现细节 | 评分器检测 |
| C3 | **独立测试** — 代码任务必须有 tester 任务，禁止自己测自己验收 | gate-phase6.py |
| C4 | **方案注入** — Phase 6 建任务时 body 必须注入 proposal + constitution + scope | task body 关键词检查 |
| C5 | **Phase 确认用模板** — 每个 Phase 结束使用对应确认模板，`[CODE]` 由脚本生成。码必须独占一行 | 模板路径索引 |
| C6 | **每个 Task 标注角色** — tasks.md 中每个 Task 必须标注 `(coder)` / `(tester)` / `(artist)` | gate-phase5.py |
| C7 | **spawn fresh-context reviewer（不可自判）** — 协调者不可自己做 C7 review。必须 spawn delegate_task，reviewer 零上下文独立验证 | gate-phase7.py |
| C8 | **任务派发必须注入 skills** — 每个任务包含角色默认技能。映射：coder→test-driven-development+incremental-implementation, artist→frontend-ui-engineering, tester→code-review-and-quality+systematic-debugging | gate-phase5.py |

### Layer 3: Pitfall（高频教训，内嵌 Top 10）

| # | 教训 | 规则 |
|---|------|------|
| 1 | 协调者做代码推理 | Way C：给目标+路径+约束，不做代码推理 |
| 2 | 跳过 tester 验证 | worker done ≠ 质量已验证 |
| 3 | 写入错误路径 | task body 必须指定绝对输出路径 |
| 4 | task body 列举太多参考文件 | 预读→自包含 SPEC→worker 只读 SPEC |
| 5 | 声称修复但未改 | grep -c 验证实际变更 |
| 6 | fire-and-forget | 派发 ≠ 完成，必须跟踪+验证+解锁 |
| 7 | 先问用户再查 skill/memory | 优先级：skill → memory → ask user |
| 8 | 跳过 Phase 3 设计直接写代码 | G1：Phase 3 未完成禁止写代码 |
| 9 | 修改后不重启服务就验证 | 重启服务后再验证 |
| 10 | Phase 8 文档规范执行不力 | 文档写入是门禁条件，不是"做完再补" |

> 完整 pitfalls → `references/pitfalls-common.md`

### ⛔ Anti-Rationalization Guard

LLM 会创造"合理例外"跳过规则。以下情况 **不是** 跳过规则的理由：

| LLM 合理化 | 真实规则 |
|------------|---------|
| "这个太简单不需要流程" | 用户说"简单做一下"才跳流程 |
| "我先检查再决定" | 检查结果不能覆盖规则 |
| "之前通过了不需要再跑" | 每次都是独立检查 |
| "脚本不支持这种项目" | 脚本报错 = 改项目结构适配脚本 |
| "需求很清楚不用问了" | 必须走完 5 维度追问 |
| "这个 Phase 很简单可以快进" | 每个 Phase 入口第一步必须重新读 SKILL.md |
| "方案 A 明显更好直接用" | 必须呈现 2-3 个方案 + 推荐理由 |
| "先跑一下看看再说" | G1：Phase 3 未完成禁止写代码 |

### 禁止行为

| 禁止行为 | 替代方案 |
|---------|---------|
| 自己写 tasks.md 内容 | 派 coder 写，协调者只 review 格式 |
| 自己判断 C7 "全部通过" | spawn fresh-context reviewer |
| 不跑脚本直接生成确认码 | 必须跑对应 gate 脚本 |
| 用 delegate_task 替代任务派发 | 必须用任务系统 + skill 注入 |

## ⚙️ 环境与能力等级

### 安装后第一步：环境自检

```bash
python3 scripts/env-check.py [--config config.json]
```

输出能力等级：
- **Level A（完整）**：kanban + gate-enforcer + 机械门禁 → 全功能
- **Level B（标准）**：delegate_task + 机械门禁 → 核心流程完整
- **Level C（轻量）**：仅 prompt 约束 → 退化为 Superpowers 级防偏离

### 配置文件 config.json

```json
{
  "project_docs_dir": "./project-docs",
  "level": "auto",
  "confirm_code_method": "hash"
}
```

## 何时触发

1. 用户发送 `/clsh-project` 或 `/cp`
2. 用户说"我要做一个 XXX"、"开发一个 XXX 系统"
3. 需求明显是多步骤项目
4. 用户说"按 Kiro 流程走"

**不触发：** 简单查询、单步操作、修 bug、已有明确方案的小改动、用户说"简单做一下"。

---

## Phase 0+1: 需求准备与澄清

### Phase 0: 内化历史教训

| 步骤 | 动作 |
|------|------|
| A | 读取 learnings（如有）→ 提取相关教训 |
| B | 读取项目已知 pitfalls → 匹配 tech/domain 标签 |

### Phase 1: 需求澄清

**5 维度追问框架（苏格拉底式）：**

| 维度 | 追问方向 |
|------|---------|
| 用户与场景 | 谁用？怎么用？边界在哪？ |
| 功能与流程 | 核心流程？异常流程？闭环？ |
| 安全与威胁 | 攻击面？数据泄露？权限越界？ |
| 合规与隐私 | 适用法规？数据处理？用户权利？ |
| 行业与技术 | 同类产品？技术选型？数据方案？ |

**追问深度：** L0 概览 → L1 细化 → L2 攻防

**Phase 1 产出物：**
1. **PRODUCT.md** — 用户故事 + 产品不变量（INV-1/INV-2...）+ 可验证性
   - 📋 模板: `templates/product-md-template.md`
2. **conversation.md** — 需求澄清对话记录

### ⛔ Phase 1 门禁

```bash
python3 scripts/gate-phase1.py <项目目录>
```

---

## Phase 2+2.5: 方案设计与技术验证

2-3 个方案 + 推荐理由 + 对比表格。Phase 2.5: 技术 Spike。

**Phase 2 产出物：**
- **TECH.md** — 架构决策 + 文件变更范围 + 实现注意事项 + 不在范围内
  - 📋 模板: `templates/tech-md-template.md`

---

## Phase 3+4: 设计文档与自检

Phase 3: proposal.md + constitution.md。**⛔ proposal 只写设计决策。**

- 📋 constitution 模板: `templates/constitution-template.md`

Phase 4: 机械检查 + 流程合规。

```bash
python3 scripts/gate-phase4.py <项目目录>
```

---

## Phase 5: 实现计划（派 coder 执行）

协调者派任务（body 含 proposal + constitution 路径），coder 自己写 tasks.md。

**⛔ 协调者只 review 格式，不改内容。**

- 📋 tasks 模板: `templates/tasks-template.md`

```bash
python3 scripts/gate-phase5.py <项目目录>
```

---

## Phase 6: 分发执行

**角色分工：** coder/artist → 任务执行 | tester → 验证任务

**⛔ 执行方式铁律：** 必须用任务系统派发（kanban 或 delegate_task），每个任务注入 skills。

**tasks.md Task 格式：**
```markdown
### Task N: 标题 | 角色：coder | skills: test-driven-development, incremental-implementation
```

**⛔ Phase 6 一致性校验：** tester 验证时必须读取 PRODUCT.md + TECH.md + proposal.md + constitution.md，逐项检查实现是否符合。

```bash
python3 scripts/gate-phase6.py <项目目录>
```

---

## Phase 7: 完成归档与流程复盘

归档 9 步 + 流程合规复盘 7 项 + handoff.md。

**归档文档路径（不可变更）：**
| 文档 | 必须路径 |
|------|---------|
| completion-summary.md | `changes/archive/completion-summary.md` |
| retrospective.md | `changes/archive/retrospective.md` |
| handoff.md | `changes/archive/handoff.md` |

---

## Phase 8: 反馈循环

**信息传递模式（C0）：** 协调者只记录现象+文件+验收标准，coder/artist 自己分析根因+设计方案+执行。

```bash
python3 scripts/gate-phase8.py <项目目录>
```

---

## 流程门禁总览

| 门禁 | 检查内容 | 未通过 → |
|------|---------|---------|
| Phase 1-3 | 用户确认码（人是 Gate，看内容才输入码） | 不进入下一 Phase |
| Phase 4 | gate-phase4.py → 用户确认码 | 不进入 Phase 5 |
| Phase 5→6 | gate-phase5.py → 用户确认码 | 不允许创建任务 |
| Phase 6 tester 后 | gate-phase6.py → 用户确认码 | 不允许汇报完成 |
| Phase 6 C7 | gate-phase7.py → 用户确认码 | 不允许汇报完成 |

## 失败模式与兜底

| 失败现象 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| 确认码绕过前置检查 | Gate 脚本 hash 码机制 | 记录违规，回退到正确 Phase |
| 目录结构不符脚本预期 | 改为 `changes/日期-话题/` 标准结构 | 参考 pitfalls-common.md |
| 任务 Done ≠ 已验证 | 执行独立产出 review | Phase 7 前强制验证 |
| C7 review 自判 | spawn fresh-context reviewer | 加载 doubt-driven-development |
| LLM 合理化跳步 | 查 Anti-Rationalization Guard 表 | 物理阻断 |

## 📚 参考文件

| 分类 | 路径 |
|------|------|
| **Pitfalls** | `references/pitfalls-common.md` |
| **模板** | `templates/*.md` |
| **Gate 脚本** | `scripts/gate-phase*.py` |
| **环境自检** | `scripts/env-check.py` |

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v6.0.0 | 2026-06-18 | **通用版**：解耦 Obsidian/Hermes/lark-cli 环境依赖；gate 脚本随 skill 分发；env-check.py 环境自检；config.json 能力等级分层；pitfalls 精简 120→30 |
