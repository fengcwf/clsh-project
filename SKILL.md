---
name: clsh-project
aliases: [cp]
description: "需求驱动的项目开发工作流 — 从需求澄清到设计文档到实现计划到执行。灵感来自 Kiro 的 Spec-Driven Development、Superpowers 的 Brainstorming 方法论、Phoenix 的状态机执行模式。DO trigger: 用户说'我要做一个 XXX'、'开发一个 XXX 系统'、'/clsh-project'、'/cp'、'按 Kiro 流程走'、需求明显是多步骤项目。Do NOT trigger: 简单查询、单步操作、修 bug（用 systematic-debugging）、已有明确方案的小改动、用户说'简单做一下'、代码质量审查（PR review）。"
version: 5.66.0
author: 灵犀
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [workflow, project, spec-driven, planning, kanban, methodology]
    related_skills:
      - kanban-orchestrator
      - obsidian-operations
      - plan
      - test-driven-development
      - incremental-implementation
      - code-review-and-quality
      - doubt-driven-development
---

# /clsh-project — 需求驱动项目开发

## 📁 路径约定

> **Vault 根目录:** `/mnt/unraid_data/Obsidian`
> 本 skill 中所有 `/mnt/unraid_data/Obsidian/raw/projects/` 路径均以 Vault 根目录为基准。
> 迁移时全局替换此前缀即可。

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
- 调试方法论 → `systematic-debugging` skill
- 代码质量规则 → `code-principles` skill
- UI/样式设计不属于灵犀职责 → `artist` 角色自行决定
- 测试用例编写不包含在灵犀 review 范围 → `tester` 角色自行设计

### 膨胀阈值
- SKILL.md: ≤ 350 行（确认模板内嵌 +80 行是合理开销）
- Common Pitfalls: ≤ 120 条（以 `## Pitfall #XX:` 格式计数）
- references/: 已迁移到 Vault `raw/projects/clsh-project/references/`

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


## ⛔ 流程规则（三层架构）

> **设计原则（来自大佬的两条核心铁律）：**
> 1. **能纯机械不用 LLM** — 有脚本检查的用脚本，不靠 LLM 自觉
> 2. **角色严格分离** — 灵犀只做信息传递（记录现象+文件+验收标准），coder/artist 自己分析+执行

### Layer 1: Gate（门禁，违反 = 流程阻断）

> **⚠️ Gate 的机械性分两类：**（2026-06-10 调研确认：没有任何框架能纯靠 prompt 实现真机械防偏离）
> - **真机械**（G0/G1/G6）：LLM 执行流程时必然触发（读文件、ls 验证）
> - **脚本门禁**（G2/G3/G4）：⛔ 必须用门禁脚本（前置检查+码生成原子化），不能拆成两步靠 LLM 自觉串联（Pitfall #142：LLM 会跳过检查直接生成码）。Gate Enforcer Plugin（pre_tool_call hook）可物理阻断，详见 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/gate-enforcer-plugin.md`
> - **行业验证的 3 种真机械策略**：工具调用拦截（GSD PreToolUse = Gate Enforcer）、进程隔离（Ralph Loop）、不信任 review（Superpowers fresh-context reviewer）。详见 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/anti-deviation-patterns.md`
>
> **Phase Gate 分类（哪些 Phase 需要 Gate 脚本）：**
> | Phase | Gate 类型 | 需要脚本？ |
> |-------|----------|----------|
> | 1 | **人是 Gate（辅助检查）** | **✅ gate-phase1.py（不阻断，仅辅助）** |
> | 2-3 | 人是 Gate（大佬看内容才输入码） | ❌ |
> | 4/5/6/8 | LLM 是 Gate（灵犀可跳过检查直接给码） | ✅ gate-phaseN.py |

| # | 规则 | 机械机制 |
|---|------|---------|
| G0 | **先查进度再行动** — `ls` + 读 overview.md + 读 changes/，从下一个未完成 Phase 继续 | 文件系统检查（真机械） |
| G1 | **文档先于代码** — Phase 3 未完成 + 大佬未确认，禁止写代码 | 文件存在性检查（真机械） |
| G2 | **Phase 4 预检** — ⛔ 必须用 `gate-phase4.py`（内嵌码生成），不能单独跑 `phase4-mechanical-check.py` 再手动生成码。检查文档存在性+关键词+行数。FAIL = 不出码，PASS = 自动出码 | 脚本 PASS/FAIL + 码生成（原子化，Pitfall #142） |
| G3 | **机械确认码脚本生成** — ⛔ 必须用 `gate-phase4.py`/`gate-phase8.py` 门禁脚本生成码（内嵌前置检查），禁止拆成"先检查再生成"两步（LLM 会跳过前者）。无门禁脚本的 Phase 用 `python3 -c "import secrets,string; ..."` 但必须先完成该 Phase 所有检查 | 脚本输出（真机械，前置检查+码生成原子化） |
| G4 | **Phase 8 bugfix spec 门禁** — 跑 `phase8-spec-check.py`，FAIL = 不允许派发。⚠️ 与 G2/G3 同样需要原子化（Pitfall #142），当前独立脚本存在 LLM 跳过风险 | 脚本拦截（待原子化） |
| G6 | **文档路径验证** — 写入后必须 `ls` 验证 | `ls` 输出（真机械） |

### ⚠️ Review Mode 目录结构（2026-06-10 确立）

**Review 项目也必须遵循标准目录结构**，Phase 4 脚本检查不区分开发/Review 项目：

```
raw/projects/<项目>/
├── overview.md                    # 关键词：状态、进度表
├── changes/
│   └── <日期>-<描述>/
│       ├── conversation.md        # 关键词：需求、决策
│       ├── proposal.md            # 关键词：技术方案、不在范围内
│       └── tasks.md               # 关键词：验收标准、不在范围内
└── source-of-truth/
    └── constitution.md            # 关键词：约束、禁止、验收标准
```

**proposal.md 必须包含"实现细节规范"节**（含"编码规范"和"错误处理规范"关键词）。Review 项目可声明"本项目不产出代码"但必须有该节标题。

### ⛔ Anti-Rationalization Guard（2026-06-10 硬编码）

LLM 会创造"合理例外"跳过规则。以下情况 **不是** 跳过规则的理由：

| LLM 合理化 | 真实规则 |
|------------|---------|
| "review 项目不适配" | 所有项目必须通过 Phase 4，目录结构统一 |
| "review 不需要 skills" | 所有 kanban 卡必须 --skill 注入 |
| "这个太简单不需要流程" | 大佬说"简单做一下"才跳流程 |
| "我先检查再决定" | 检查结果不能覆盖规则 |
| "之前通过了不需要再跑" | 每次都是独立检查 |
| "脚本不支持这种项目" | 脚本报错 = 改项目结构适配脚本，不是跳过脚本 |

**验证方法**：每次灵犀说"不需要"/"不适配"/"例外"时，查以上表格。匹配 → 强制执行规则。

### 禁止行为（⛔ 灵犀硬编码，不可例外）

| 禁止行为 | 替代方案 | 违反 = |
|---------|---------|--------|
| 自己跑 phase4-mechanical-check.py | 必须跑 gate-phase4.py（原子化） | 流程违规 |
| 自己写 tasks.md 内容 | 派 coder 写，灵犀只 review 格式 | 流程违规 |
| 自己判断 C7 "全部通过" | spawn fresh-context reviewer | 流程违规 |
| 用 delegate_task 替代 kanban | 必须用 hermes kanban create --skill | 流程违规 |
| 不跑脚本直接生成确认码 | 必须跑对应 gate 脚本 | Gate Enforcer 阻断 |
| 说"review 项目不适配" | 查 Anti-Rationalization Guard 表 | 流程违规 |

### Layer 2: Convention（架构约束，通过设计而非自觉强制）

| # | 规则 | 执行方式 |
|---|------|---------|
| C0 | **角色分离：灵犀只记录，不分析** — Phase 8 灵犀只记录现象+文件+验收标准，coder/artist 自己分析根因+设计方案+执行。灵犀不是分析者 | 架构约束（task body 只含信息，不含分析） |
| C1 | **Phase 5 派 coder 写 tasks** — 灵犀派 kanban 卡（body 含 proposal + constitution 路径），coder 自己写 tasks.md，灵犀 review 格式合规但不改内容 | kanban 派发 |
| C2 | **proposal 只写设计决策** — 功能清单/API 合约/数据模型/架构约束/文件范围，不写实现细节 | 评分器检测（clsh-unified-scorer.py） |
| C3 | **独立测试** — 代码任务必须有 tester kanban 卡，禁止自己测自己验收 | `hermes kanban list --assignee tester` 非空 |
| C4 | **方案注入** — Phase 6 建卡时 body 必须注入 proposal + constitution + scope | task body 关键词检查 |
| C5 | **Phase 确认用模板** — 每个 Phase 结束使用对应确认模板，`[CODE]` 由脚本生成。飞书渠道自动渲染为流式卡片（Card JSON 2.0），微信渠道保持纯文本。**码必须独占一行，前后无 emoji/前缀/说明文字**（方便复制）。**⛔ 确认码格式存在于 4+ 个文件中，更新时必须全局 grep 同步** | 模板路径索引 + 确认码格式校验 |
| C6 | **每个 Task 标注角色** — tasks.md 中每个 Task 必须标注 `(coder)` / `(tester)` / `(artist)` / `(reviewer)`（Review 项目用 reviewer） | 角色标注检查 |
| C7 | **spawn fresh-context reviewer（不可自判）** — ⛔ 灵犀不可自己做 C7 review。必须 spawn `delegate_task`，goal 包含审查 prompt（见下方）。reviewer 零上下文，独立验证一切，输出直接转发大佬，灵犀不可修改。参考 Superpowers 不信任模型。**C7 审查 checklist：** 1) tasks.md skills 字段存在 2) 角色标注正确 3) 验收标准可执行（无 TBD/placeholder） 4) scope 对照：产出物覆盖 proposal 范围 5) 验证证据（命令输出）存在 | delegate_task + 不信任 prompt |
|| C8 | **kanban 派发必须注入 skills** — 每个 kanban 卡的 `--skill` 参数必须包含角色默认技能。不指定 = 流程违规。映射：coder→test-driven-development+incremental-implementation, artist→popular-web-designs+frontend-ui-engineering, tester→code-review-and-quality+systematic-debugging | kanban_create 前检查 task.skills |

### Layer 3: Pitfall（降级为教训，存 common.md）

11 条旧铁律已降级为 Pitfall（分阶段审批、角色分离总纲、反馈走流程、Checkpoint 机制、安全扫描、Auto-Fix 上限、代码交叉验证、Context File Pattern、渠道匹配、Watchdog cron、Phase 确认模板）。详见 `common.md`。

**违反以上任何一条 = 流程违规，必须记 ERRORS.md。**

## 何时触发

1. 大佬发送 `/clsh-project` 或 `/project`
2. 大佬说"我要做一个 XXX"、"开发一个 XXX 系统"、"实现 XXX 功能"
3. 大佬提出的需求明显是多步骤项目
4. 大佬说"按 Kiro 流程走"、"先做需求分析"
5. 大佬说"review 项目"、"检查实现效果"、"对比设计方案" → **Review Mode**

**不触发：** 简单查询、单步操作、修复 bug（用 systematic-debugging）、已有明确方案的小改动、大佬说"简单做一下"、代码质量审查（PR review）。

### ⚠️ Review Mode 审查范围（2026-06-10 确立）

**Review 项目的审查范围必须覆盖整个项目目录**，不只是 `src/`。根目录配置文件（ecosystem.config.cjs、package.json）、scripts/、config/、临时脚本都是审查对象。大佬说"只覆盖 src/"时立即修正，不要等 Phase 2 才发现。

### ⚠️ C7 灵犀 review 必须真实执行（2026-06-10 确立）

**C7 review 不能自己打勾了事。** 必须：
1. 实际读取 tasks.md 检查每个 Task 的 skills 字段
2. 实际加载 doubt-driven-development skill
3. 如果发现缺失（如 skills 未注入），必须修复后才能确认 Phase 5

**自己说"全部通过"但实际未检查 = 流程违规。** 大佬会追问细节来验证。

**⚠️ 歧义提醒："测试 X" vs "创建新项目"**
- "测试 XX，需求：A+B+C" → **新项目**，"测试"是项目类型，走完整流程
- "帮我测试一下 XX"、"跑一遍测试"、"验证 XX 功能" → **测试现有代码**，用 systematic-debugging 或直接执行

## Review Mode（规格合规审查）

7 步：读项目文档 → 读所有代码 → 验证运行状态 → 功能合规矩阵 → Constitution 合规 → 代码质量（P1-P6） → 汇报。

📋 详细流程: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase-review.md`
📋 审计维度框架: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/review-audit-dimensions.md`（skill-local）或 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase-review-audit-dimensions.md`（Vault）

**Review Mode Phase 1 流程：** 初始扫描（并行子任务覆盖代码级维度）→ 保存初始报告到项目根目录 → 调研扩展（安全/架构维度）→ 向大佬确认范围 → ⚠️ 初始报告是参考，不是执行依据。

**⚠️ Review Mode 适配注意：**
- **G2 (Phase 4 机械检查) 适用于所有项目类型，包括 Review** — `phase4-mechanical-check.py` 期望标准目录结构（`changes/*/conversation.md`、`source-of-truth/constitution.md`）。**Review 项目也必须用这个结构**，不能用扁平结构。constitution.md 必须包含 `## 实现细节规范` 节（含"编码"关键词）。（Pitfall #139: 不要假设"Review 项目结构不同"就跳过 G2）
- **C6 角色标注**: Review 项目用 `(reviewer)` 而非 `(coder)/(tester)/(artist)`
- **审查范围必须包含项目根目录全部代码** — 不只是 `src/`，还要包含根目录脚本、config/、scripts/、ecosystem.config.cjs、package.json 等（Pitfall #138）
- **C7 review 不可自判** — 加载 doubt-driven-development skill 是必要条件，但不是充分条件。灵犀不能自己打勾通过 C7，必须有外部验证（spawn fresh-context reviewer 或大佬确认）。自己做的 review = 流程违规（Pitfall #140）

**红线：** 产出报告，不直接修复。修复走 Phase 8。

---

📋 流程总览 + Session Launch Guidance + 项目暂存: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/overview.md`

---

## Phase 0+1: 需求准备与澄清

### Phase 入口（每次进入必须执行）
1. ⛔ 重新读取本 SKILL.md（不依赖记忆中的规则）
2. ⛔ 读取: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase0-1-requirements.md`
3. ⛔ 读取: `raw/projects/<项目>/overview.md`（确认项目状态）

调研循环模式：每个决策点走 `L0→L1→L2` 分层调研→提问→确认微循环。机械确认门禁 + 代码交叉验证 + CONTEXT.md 术语表。

### ⛔ 调研维度覆盖检查（Phase 1 完成后必须执行）

**Phase 1 完成后，必须运行 `gate-phase1.py` 自检：**

```bash
python3 /root/.hermes/scripts/gate-phase1.py <项目目录>
```

**脚本输出：**
- ✅ PASS：覆盖率 ≥ 80%，大佬应当通过
- ❌ FAIL：覆盖率 < 80%，必须补充调研

**⚠️ 脚本不阻断流程（Phase 1 的 Gate 是人）**
脚本只是辅助检查工具，帮大佬发现遗漏。最终是否通过，由大佬决定。

**向大佬汇报时，必须附带：**
1. 调研内容摘要
2. gate-phase1.py 检查报告
3. 未覆盖维度及风险提示

### ⛔ 5 维度追问框架（苏格拉底式）

| 维度 | 关键词 | 追问方向 |
|------|--------|---------|
| 用户与场景 | 用户/场景/角色/目标 | 谁用？怎么用？边界在哪？ |
| 功能与流程 | 功能/流程/核心/异常 | 核心流程？异常流程？闭环？ |
| 安全与威胁 | 安全/威胁/攻击/漏洞 | 攻击面？数据泄露？权限越界？ |
| 合规与隐私 | 合规/隐私/法规/个保法 | 适用法规？数据处理？用户权利？ |
| 行业与技术 | 行业/技术/竞品/选型 | 同类产品？技术选型？数据方案？ |

**追问深度：**
- L0 概览：首次接触需求，一句话理解本质
- L1 细化：用户给了基本描述，追问"怎么做"和"边界"
- L2 攻防：涉及安全/隐私/权限，追问"怎么防"和"怎么测"

**⚠️ 用户跳过维度时的处理：**
1. 必须追问确认："你确认跳过 XX 维度吗？"
2. 必须记录到 conversation.md："⏭️ XX: 用户确认跳过"
3. 必须提示风险："该维度涉及 XX 要求，跳过可能导致 XX 问题"

📋 详细流程: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase0-1-requirements.md`
📋 Gate 辅助方案: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase1-gate-auxiliary.md`
📋 确认模板: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/phase-confirmations.md` → Phase 1

### ⛔ Phase 1 产出物（SDD 优化）

**Phase 1 完成后，必须产出 PRODUCT.md（产品规格）：**

```markdown
# PRODUCT.md — 产品规格

## 用户故事（记录大佬确认的需求）
- 作为 [角色]，我希望 [功能]，以便 [价值]

## 产品不变量（记录大佬确认的规则）
- INV-1: [无论什么情况都必须成立的规则]
- INV-2: [无论什么情况都必须成立的规则]

## 可验证性（记录如何验证不变量）
- INV-1: [验证方法：单元测试/集成测试/E2E/监控]
- INV-2: [验证方法：单元测试/集成测试/E2E/监控]
```

**⚠️ 角色分离：**
- 灵犀**只记录**大佬确认的内容，不分析、不定义、不设计
- 产品不变量必须由大佬确认，灵犀不能自行定义
- PRODUCT.md 是 Phase 5 coder 写 tasks.md 的重要参考

**📋 产出路径：** `raw/projects/<项目>/changes/<日期>-<描述>/PRODUCT.md`

---

## Phase 2+2.5: 方案设计与技术验证

### Phase 入口（每次进入必须执行）
1. ⛔ 重新读取本 SKILL.md（不依赖记忆中的规则）
2. ⛔ 读取: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase2-design.md`
3. ⛔ 确认 Phase 1 已完成（overview.md 进度表）

2-3 个方案 + 推荐理由 + 对比表格。Phase 2.5: 技术 Spike + 设计 Prototype。

📋 详细流程: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase2-design.md`
📋 确认模板: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/phase-confirmations.md` → Phase 2

### ⛔ Phase 2 产出物（SDD 优化）

**Phase 2 完成后，必须产出 TECH.md（技术规格）：**

```markdown
# TECH.md — 技术规格

## 架构决策（记录大佬确认的技术方案）
- [技术选型1]：[选择理由]
- [技术选型2]：[选择理由]

## 文件变更范围（记录预期变更的文件）
- `src/xxx/xxx.ts` — [变更内容]
- `src/xxx/xxx.ts` — [变更内容]

## 实现注意事项（记录技术约束）
- [注意事项1]
- [注意事项2]

## 不在范围内（记录明确排除的内容）
- [排除项1]
- [排除项2]
```

**⚠️ 角色分离：**
- 灵犀**只记录**大佬确认的技术决策，不设计、不实现
- 技术规格必须由大佬确认，灵犀不能自行决定
- TECH.md 是 Phase 5 coder 写 tasks.md 的重要参考

**📋 产出路径：** `raw/projects/<项目>/changes/<日期>-<描述>/TECH.md`

---

## Phase 3+4: 设计文档与自检

### Phase 入口（每次进入必须执行）
1. ⛔ 重新读取本 SKILL.md（不依赖记忆中的规则）
2. ⛔ 读取: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase3-spec.md`
3. ⛔ 确认 Phase 2 已完成（overview.md 进度表）

Phase 3: proposal.md + constitution.md + 可选 ADR。**⛔ proposal 只写设计决策（铁律 #22）。** Phase 4: 机械检查 + 流程合规 + Review Gate。

📋 流程: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase3-spec.md` | 📋 门禁: `/root/.hermes/scripts/gate-phase4.py`（前置检查+码生成原子化，Pitfall #142） | 📋 确认模板: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/phase-confirmations.md`

---

## Phase 5: 实现计划（派 coder 执行）

### Phase 入口（每次进入必须执行）
1. ⛔ 重新读取本 SKILL.md（不依赖记忆中的规则）
2. ⛔ 读取: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase5-tasks.md`
3. ⛔ 确认 Phase 4 已完成（overview.md 进度表 + gate-phase4 标记文件）

灵犀派 kanban 卡（body 含 proposal + constitution 路径），coder 自己写 tasks.md。**⛔ 每个 Task 标注角色（铁律 #22）。⛔ 灵犀只 review 格式，不改内容。⛔ review 前加载 `doubt-driven-development` skill。**

### ⛔ Phase 5 规格参考（SDD 优化）

**coder 写 tasks.md 时，必须参考以下规格文件：**

| 文件 | 路径 | 用途 |
|------|------|------|
| **PRODUCT.md** | `raw/projects/<项目>/changes/<日期>-<描述>/PRODUCT.md` | 产品不变量，确保 tasks 覆盖所有不变量 |
| **TECH.md** | `raw/projects/<项目>/changes/<日期>-<描述>/TECH.md` | 技术规格，确保 tasks 遵循技术约束 |
| **proposal.md** | `raw/projects/<项目>/changes/<日期>-<描述>/proposal.md` | 设计决策，确保 tasks 符合设计方案 |
| **constitution.md** | `raw/projects/<项目>/source-of-truth/constitution.md` | 约束条件，确保 tasks 不违反约束 |

**coder 写 tasks.md 的 checklist：**
```
- [ ] 已读取 PRODUCT.md，理解所有产品不变量
- [ ] 已读取 TECH.md，理解技术规格和文件变更范围
- [ ] 已读取 proposal.md，理解决策决策
- [ ] 已读取 constitution.md，理解约束条件
- [ ] tasks.md 覆盖所有 PRODUCT.md 中的不变量
- [ ] tasks.md 遵循 TECH.md 中的技术规格
- [ ] tasks.md 不违反 constitution.md 中的约束
```

**⚠️ 角色分离：**
- 灵犀**只提供**规格文件路径，不分析、不设计
- coder **自己读取**规格文件，自己写 tasks.md
- 灵犀**只 review 格式**，不改内容

📋 流程: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase5-tasks.md`

---

## Phase 6: Ralph Loop 分发执行

### Phase 入口（每次进入必须执行）
1. ⛔ 重新读取本 SKILL.md（不依赖记忆中的规则）
2. ⛔ 读取: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase6-execution.md`
3. ⛔ 确认 Phase 5 已完成（overview.md 进度表 + gate-phase5 标记文件）

Way C 铁律：灵犀给目标+路径+约束，不做代码推理。**角色分工：** coder/artist → kanban worker | tester → kanban review 卡。**⛔ tester 必须产出持久化测试文件。** 执行后灵犀做**流程合规 review**（C7）：文件存在、角色标注、验收标准、scope 对照。代码质量由 tester review。**⛔ review 前加载 `doubt-driven-development` skill。**

### ⛔ Phase 6 一致性校验（SDD 优化）

**tester 验证时，必须执行规格一致性校验：**

**校验内容：**
1. **读取 PRODUCT.md** — 检查所有产品不变量是否实现
2. **读取 TECH.md** — 检查技术规格是否遵循
3. **读取 proposal.md** — 检查设计决策是否符合
4. **读取 constitution.md** — 检查约束条件是否违反

**校验报告模板：**
```markdown
## 规格一致性校验报告

### ✅ 符合规格
- [x] INV-1: [不变量描述] — [验证证据]
- [x] INV-2: [不变量描述] — [验证证据]

### ❌ 不符合规格
- [ ] INV-3: [不变量描述]
  - 当前实现：[实际行为]
  - 规格要求：[预期行为]
  - 偏移原因：[分析]

### ⚠️ 部分实现
- [~] INV-4: [不变量描述]
  - 当前实现：[实际行为]
  - 规格要求：[预期行为]
  - 差距：[差距描述]

### 📊 校验统计
- 总不变量数：[N]
- 完全符合：[N] ([百分比]%)
- 不符合：[N] ([百分比]%)
- 部分实现：[N] ([百分比]%)
```

**⚠️ 角色分离：**
- tester **自己读取**规格文件，自己做校验
- tester **自己产出**校验报告，灵犀不干预
- 灵犀**只 review** 校验报告的格式合规性

**📋 产出路径：** `raw/projects/<项目>/changes/<日期>-<描述>/validation-report.md`

### ⛔ Phase 6 执行方式铁律（2026-06-10 确立）

**必须用 `hermes kanban create --skill` 派发，禁止用 `delegate_task` 替代。**

| 方式 | 是否合规 | 原因 |
|------|---------|------|
| `hermes kanban create --skill <name>` | ✅ | skills 注入到 worker 环境，角色隔离 |
| `delegate_task` | ❌ | 无 skills 注入，无角色隔离，绕过 C8 |

**事后补 tasks.md 的 skills 字段不算合规** — skills 必须在执行前注入到 worker 环境，不是写在文档里。

**Review 项目也必须走 kanban**，不能因为"不产出代码"就用 delegate_task 替代。

📋 流程: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase6-execution.md`

**⛔ Phase 6 派发 checklist（每步必须打勾）**

```
Phase 6 派发自检：
- [ ] tasks.md 已读取，每个 Task 的 skills 字段已确认
- [ ] ⛔ 每个 kanban_create 传入 `--skill <name>`（可重复多次，从 Task 定义复制。注意是 `--skill` 不是 `--skills`）
- [ ] ⛔ 技能映射（内嵌，不可省略）：
      coder  → test-driven-development, incremental-implementation
      artist → popular-web-designs, frontend-ui-engineering
      tester → code-review-and-quality, systematic-debugging
      reviewer → code-review-and-quality, systematic-debugging（Review Mode 专用）
      灵犀   → doubt-driven-development（Phase 5/6/8 review 时加载）
- [ ] ⛔ 每个 skill 存在于 assignee profile（ls /root/.hermes/profiles/<assignee>/skills/）
- [ ] ⛔ skill 无重复副本 — 同一 SKILL.md 出现在多个 category 目录时 worker 无法解析（Pitfall #143）
- [ ] review 卡已创建（assignee=tester, parents=[实现卡]）
- [ ] ⛔ unblock 前必须先修复根因 — 读 crash log 定位问题，修复后验证，再 unblock（Pitfall #144）
- [ ] 每张卡 notify-subscribe 已执行
```

**⛔ Review Mode 特别规则**：
- Review 项目用 `reviewer` 角色（映射 tester skills）
- Phase 6 必须用 kanban 派发，**禁止用 delegate_task**（delegate_task 绕过 skill 注入，质量下降 40-186%）
- task body 必须包含文件产出路径（如 `/tmp/workspace-review-<task_id>.md`），防止 worker 只写截断的 kanban summary
- 详见 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/review-mode-lessons.md`

**tasks.md Task 格式（含 skills 字段）：**
```markdown
### Task N: 标题 | 角色：coder | skills: test-driven-development, incremental-implementation
### Task N: 标题 | 角色：artist | skills: popular-web-designs, frontend-ui-engineering
### Task N: 标题 | 角色：tester | skills: code-review-and-quality, systematic-debugging
```
灵犀派活时直接从 Task 定义读 skills，不查外部映射表。

📋 详细派发模板: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/phase6-dispatch-template.md`
📋 Review Mode 教训: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/review-mode-lessons.md`（10 条教训，含定量对比）

---

## Phase 7: 完成归档与流程复盘

### Phase 入口（每次进入必须执行）
1. ⛔ 重新读取本 SKILL.md（不依赖记忆中的规则）
2. ⛔ 读取: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase7-archive.md`
3. ⛔ 确认 Phase 6 已完成（overview.md 进度表 + gate-phase6 标记文件）
4. ⛔ **归档路径强制检查** — completion-summary.md / retrospective.md / handoff.md 必须写入 `changes/archive/` 目录，**不是项目根目录**。评分器检查路径：`changes/archive/completion-summary.md`

### ⛔ 归档文档路径（机械门禁，不可变更）

| 文档 | 必须路径 | 错误路径 |
|------|---------|---------|
| completion-summary.md | `changes/archive/completion-summary.md` | ❌ 项目根目录 |
| retrospective.md | `changes/archive/retrospective.md` | ❌ 项目根目录 |
| handoff.md | `changes/archive/handoff.md` | ❌ 项目根目录 |

**写入前必须：** `mkdir -p changes/archive/`

归档 9 步 + 流程合规复盘 7 项 + handoff.md。**使用 `handoff` skill。**

### ⛔ 归档文档关键词（机械门禁）

| 文档 | 关键词 | 行数上限 |
|------|--------|---------|
| completion-summary.md | `概述`, `技术`, `功能`, `限制` | ≤ 40 行 |
| retrospective.md | `合规`, `教训`, `改进`, `角色` | ≤ 40 行 |
| handoff.md | `状态`, `下一步行动` | ≤ 30 行 |

📋 详细流程: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase7-archive.md`

---

## Phase 8: 反馈循环

### Phase 入口（每次进入必须执行）
1. ⛔ 重新读取本 SKILL.md（不依赖记忆中的规则）
2. ⛔ 读取: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase8-feedback.md`
3. ⛔ 确认项目当前状态（overview.md）

**信息传递模式（C0）：** 灵犀只记录现象+文件+验收标准，coder/artist 自己分析根因+设计方案+执行。tester 浏览器验证。每轮归档 + 上下文溢出防护（每轮 ≤3-4 bug）。**⛔ 灵犀 review 前加载 `doubt-driven-development` skill。**

**⛔ Phase 8 fix 卡也必须注入 skills（C8 补充）：** Phase 8 创建的 fix kanban 卡同样需要 `--skill` 参数。Phase 6 派发 checklist 不适用于 Phase 8（Phase 8 有自己的流程），但 C8 规则适用于所有 kanban 卡创建。

### ⚠️ Phase 8 测试需求超出原始范围

当项目 Phase 7 已归档（状态 `done`），大佬要求"测试"但需求包含原始 `proposal.md` "不在范围内"的功能时：

先验证现有代码 → 识别差距 → 向大佬确认意图（A)回归 B)新需求 C)部分接受）。**铁律：** 超出 scope 禁止自行扩展，必须先确认。

📋 详细流程: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase8-feedback.md`
|| **教训** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/pitfalls/common.md` |
||| **Review Mode 教训** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/review-mode-lessons.md`（10 条，含 delegate_task vs kanban 定量对比） |
||| **方法论**
---

## E2E 自动化测试
主脚本: `/root/.hermes/scripts/clsh-e2e-test.py` | Cron: `/root/.hermes/scripts/clsh-e2e-cron.sh`

---

## 流程门禁

| 门禁 | 检查内容 | 未通过 → |
|------|---------|---------|
| Phase 1-3 | 大佬确认码（人是 Gate，看内容才输入码） | 不进入下一 Phase |
| Phase 4 | gate-phase4.py（文件+关键词+行数）→ 大佬确认码 | 不进入 Phase 5 |
| Phase 5→6 | gate-phase5.py（skills+角色+验收）→ 大佬确认码 | 不允许创建 kanban 卡 |
| Phase 6 执行 | 代码任务必须有 tester 卡 | 不允许标记完成 |
| Phase 6 tester 后 | gate-phase6.py（tester 报告+证据）→ 大佬确认码 | 不允许汇报完成 |
| Phase 6 Browser QA | UI 项目 tester 必须浏览器验证 | 不允许汇报完成 |

> **铁律设计原则：** Phase 1-3 的 Gate 是**人**（大佬看内容后输入码），LLM 无法伪造。Phase 4/5/6/8 的 Gate 是**灵犀**（灵犀跑检查后给码），必须用 Gate Enforcer Plugin（pre_tool_call hook）物理阻断跳过检查的码生成。详见 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/gate-enforcer-plugin.md` 和 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/anti-deviation-patterns.md`。

## 失败模式与兜底

| 失败现象 | 触发条件 | 一线修复 | 仍失败兜底 | Pitfall |
|---------|---------|---------|-----------|---------|
| 确认码绕过前置检查 | 如果 LLM 跳过 gate 脚本直接生成码 | Gate Enforcer Plugin 物理阻断 | 记录违规，回退到正确 Phase | #142 |
| 目录结构不符脚本预期 | 当机械检查 FAIL 报"文件不存在"时 | 改为 `changes/日期-话题/` 标准结构 | 参考 Pitfall #138 | #138 |
| kanban Done ≠ 已验证 | 如果所有卡 done 但 tester 未验证 | 执行独立产出 review（逐项 grep） | Phase 7 前强制验证 | #143 |
| unblock 未修根因 | 当 unblock 前未读 crash log 时 | 先定位根因、修复、验证，再 unblock | 升级给大佬 | #144 |
| delegate_task 替代 kanban | 如果用 delegate_task 绕过 skill 注入 | 必须用 `hermes kanban create --skill` | 质量下降 40-186% | Review #2 |
| C7 review 自判 | 当灵犀自己说"全部通过"时 | spawn fresh-context reviewer | 加载 doubt-driven-development | Review #3 |
| 审查范围不足 | 如果只覆盖 src/ 不含根目录 | 扩展到项目根目录全部代码 | 包含 config/scripts/ecosystem | Review #5 |
| Phase 4 预期 FAIL | 如果 tasks.md 不存在就视为预期 | 先跑底层检查，忽略 tasks.md | 参考 Pitfall #145 | #145 |
| 大佬未给确认码 | 当大佬不在或延迟时 | 等待，不跳过门禁 | 暂停流程，记录状态 | — |
| LLM 合理化跳步 | 当灵犀说"不需要"/"不适配"/"例外"时 | 查 Anti-Rationalization Guard 表 | Gate Enforcer 物理阻断 | — |

> 完整 pitfalls 词典 → `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/pitfalls/`

**角色分离（C0）：** 灵犀只做信息传递，不分析根因、不设计方案、不写代码。coder/artist 自己分析+执行。Phase 8 task body 只含现象+文件+验收标准。
**Way C 铁律（C1）：** 灵犀只给目标+路径+约束，不做代码推理。Pattern to Follow 必做。worker 修复后必须走 tester 验证。
**流程合规 + Buildability review（C7）：** 灵犀 review 的是流程合规（文件存在、角色标注、验收标准、scope）和 Buildability（task 可执行性：步骤清晰、无 placeholder/TBD、不会让 coder 卡住）。不是代码质量。代码质量由 tester review。**⛔ Security Scan + Quality Review 由 tester 执行（C3 独立测试），灵犀不做代码分析。**

## 维度相关簇

基于 8 框架调研（Superpowers/GSD/Ralph Loop/Kiro/gstack/Spec Kit/OpenSpec/Trellis）的防偏离机制映射：

| 簇 | 包含维度 | 依赖关系 | 已实现机制 |
|----|---------|---------|-----------|
| 流程簇 | Phase 完整性 → Gate 脚本 → 检查点标记 | 改 Phase 流程会带动 Gate 和检查点变化 | gate-phaseN.py 原子化门禁 |
| 边界簇 | 职责边界 → 禁止行为 → 信息传递 | 改职责定义会带动禁止行为和信息流变化 | C0 角色分离 + 禁止行为表 |
| 防偏离簇 | Anti-Rationalization → 机械门禁 → 验证机制 | 改防偏离策略会带动门禁和验证变化 | Gate Enforcer + Fresh-Context Reviewer |
| 文档簇 | 模板关键词 → 行数限制 → 版本一致性 | 改模板格式会带动版本和行数约束变化 | phase-confirmations.md 模板 |

**防偏离三层架构**（源自 anti-deviation-patterns.md）：
- **Tier 1 真机械**：Gate Enforcer Plugin（pre_tool_call hook 拦截码生成）→ 对标 GSD PreToolUse
- **Tier 2 结构性约束**：C7 Fresh-Context Reviewer（零上下文启动）→ 对标 Superpowers 不信任模型
- **Tier 3 Prompt 约束**：Anti-Rationalization Guard（合理化对照表）→ 对标 GSD 包合法性门禁

**应用**：每轮优化后检查相邻维度是否退化。如果退化 >2%，回滚本轮改动。

## ⚠️ Skill 别名

`/cp` 通过 frontmatter `aliases: [cp]` 注册为 `/clsh-project` 的别名。

### #145 Phase 4 gate 脚本检查 tasks.md 导致预期 FAIL
**规则：** `gate-phase4.py` 调用 `phase4-mechanical-check.py`，后者检查 `changes/*/tasks.md`。但 tasks.md 是 Phase 5 产出，Phase 4 时尚不存在。**处理方式：** Phase 4 自检时先跑 `phase4-mechanical-check.py`（底层检查），tasks.md 的 FAIL 为预期行为。Phase 5 完成后再跑 `gate-phase4.py` 生成确认码。不能因为 tasks.md FAIL 就认为 Phase 4 自检失败。

### #146 tasks.md 紧凑格式（80 行限制实战解法）
**规则：** tasks.md ≤ 80 行。每个 Task 用 **2 行** pipe 分隔格式：标题行（含角色+skills）+ 详情行（`文件: ... | 功能: ... | 验收标准: ... | 不在范围内: ...`）。**行数预算：** 16 Task × 2 行 = 32 行 + 标题/依赖图 ~8 行 + Self-Review 3 行 = ~43 行。**⚠️ 禁止用 4-5 行/Task 的 bullet 格式**（16×5 + 8 + 3 = 91 行，超限）。代码片段在 Phase 6 派发时注入 kanban body，不写在 tasks.md 中。**模板：** `references/templates/tasks-md-compressed-template.md` | **详细解法：** `references/pitfalls/pitfall-146-tasks-compact-format.md`

### #147 调研模板必须覆盖安全/隐私/体验维度（2026-06-10 E2E 复盘）
**规则：** Phase 0-1 调研必须覆盖 5 个维度（用户与场景/功能与流程/安全与威胁/合规与隐私/行业与技术）。只覆盖"功能实现"和"技术选型"会导致：
- **安全威胁分析** — 攻击面识别+缓解措施（借鉴 Phoenix 12-Role 系统）
- **数据隐私合规** — 适用法规+具体条款（数据删除权、匿名化、PIPL）
- **用户体验异常场景** — 断网、加载失败、操作中断怎么办
- **权限隔离规则** — 角色间数据边界（A 角色能否访问 B 角色的数据）
**反例：** 在线教育平台 E2E 测试，15 个问题点中 11 个被遗漏，根因是调研模板没有"安全威胁"和"合规隐私"维度。
**修复：** Phase 0-1 使用苏格拉底式追问 + 5 维度框架 + gate-phase1.py 辅助检查。
**参考：** `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/enhanced-research-template.md` + `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/research-methodology-comparison.md`

### #148 验收标准用 GIVEN...WHEN...THEN 格式（2026-06-10 借鉴 Kiro）
**规则：** tasks.md 的验收标准必须使用 GWT 格式：`✅ GIVEN [前置条件] WHEN [触发事件] THEN [预期结果]`。每个 Task 至少 3 条（正常+异常+安全）。安全相关 Task 必须有🔒标记。
**示例：**
- ❌ "教师创建+学生提交+教师批改"
- ✅ "GIVEN 教师是课程所有者 WHEN 批改作业 THEN 更新 score+feedback；GIVEN 教师不是课程所有者 WHEN 批改作业 THEN 返回 403"
**根因：** 自然语言验收标准无法验证权限约束，导致作业批改权限漏洞未发现。GWT 格式可直接转测试用例，提高可测试性。

> 完整 pitfalls 词典（#51-#146 活跃 + #1-#50 已归档）→ `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/pitfalls/common.md` + `archive/`

### #149 SDD 角色分离：灵犀只记录产品不变量，不定义（2026-06-12）
**规则：** PRODUCT.md 由灵犀在 Phase 0-1 产出，但灵犀**只记录**大佬确认的不变量，不分析、不定义、不设计。不变量必须由大佬确认，灵犀不能自行定义。
**反例：** 灵犀自行分析用户需求，定义「根据安全最佳实践，密码必须 bcrypt 加密」— 这是分析，不是记录。
**正确：** 大佬说「密码必须 bcrypt 加密」，灵犀记录「INV-1: 用户密码必须 bcrypt 加密存储」。

### #150 TECH.md 由灵犀记录，不是 coder 写（2026-06-12）
**规则：** TECH.md 由灵犀在 Phase 2 产出，记录大佬确认的技术决策。coder 在 Phase 5 写 tasks.md 时**参考** TECH.md，但不写 TECH.md。
**原因：** 技术决策是大佬确认的，不是 coder 设计的。coder 是实现者，不是设计者。
**流程：** Phase 2 灵犀记录 TECH.md → Phase 5 coder 参考 TECH.md 写 tasks.md → Phase 6 tester 对照 TECH.md 校验。

### #151 PRODUCT.md + TECH.md 是 SDD 核心产出物（2026-06-12）
**规则：** Phase 0-1 必须产出 PRODUCT.md，Phase 2 必须产出 TECH.md。这两个文件是 SDD（Spec-Driven Development）的核心产出物，与 proposal.md + constitution.md 并行存在。
**区别：**
- PRODUCT.md = 产品规格（做什么，用户视角，不变量）
- TECH.md = 技术规格（怎么做，架构，实现细节）
- proposal.md = 设计决策（功能清单/API 合约/数据模型）
- constitution.md = 约束条件（禁止事项/代码规范/测试要求）

### #152 validation-report.md 是 Phase 6 tester 的必要产出（2026-06-12）
**规则：** Phase 6 tester 验证时，必须产出 validation-report.md（规格一致性校验报告），对照 PRODUCT.md 和 TECH.md 检查所有不变量是否实现。
**校验内容：** 读取 PRODUCT.md 检查不变量 + 读取 TECH.md 检查技术规格 + 读取 proposal.md 检查设计决策 + 读取 constitution.md 检查约束条件。
**报告格式：** 符合规格 / 不符合规格 / 部分实现 + 校验统计 + 校验结论。

---

## 版本历史（最近 5 版）

| 版本 | 日期 | 变更 |
|------|------|------|
| v5.66.0 | 2026-06-12 | **SDD 优化落地**：Phase 0-1 产出 PRODUCT.md、Phase 2 产出 TECH.md、Phase 6 产出 validation-report.md；新增 Pitfall #149-#152（角色分离/产出物定义）；gate-phase1.py 增加 PRODUCT.md 检查；新增 /validate-changes-match-specs Skill；E2E 测试适配 SDD 流程 |
| v5.65.0 | 2026-06-11 | **P0+P1+P2 修复**：合并重复 Pitfall #147/#148、修复版本号冲突、瘦身 SKILL.md（流程总览/版本历史迁移到 references）、统一所有路径为绝对路径（含 `~/.hermes` → `/root/.hermes`） |
| v5.64.0 | 2026-06-11 | **Phase 1 Gate 辅助检查**：新增 gate-phase1.py 调研维度覆盖检查脚本（5 维度）、苏格拉底式追问框架、用户跳过维度确认机制 |
| v5.63.0 | 2026-06-10 | **调研方法论增强**：新增 Pitfall #147（调研模板必须覆盖安全/隐私/体验维度）、#148（验收标准用 GIVEN...WHEN...THEN 格式） |
| v5.62.0 | 2026-06-10 | **E2E 漂移修复**：Phase 7 归档路径强制检查（changes/archive/）、Phase 0-1 调研深度强化（5 维度检查） |
| v5.61.0 | 2026-06-10 | **Pitfall #145-#146**: Phase 4 gate 脚本检查 tasks.md 导致预期 FAIL；tasks.md 紧凑格式实战解法 |
| v5.60.0 | 2026-06-10 | **防偏离体系落地实施**：Gate Enforcer Plugin 创建、4 个 gate 脚本、Phase 入口重载块、灵犀禁止行为表 |

> 完整版本历史（v5.47.0+）→ `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/version-history.md`

---

## 📚 参考文件

| 分类 | 路径 |
|------|------|
| **教训** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/pitfalls/common.md` |
| **Review Mode 教训** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/review-mode-lessons.md`（10 条，含 delegate_task vs kanban 定量对比） |
| **方法论** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/embedded-vs-external-workflow-pattern.md` |
| **Phase 8 精度** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/phase8-spec-precision-learnings.md` |
| **飞书桥接** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/lark-cli-feishu-bridge.md` |
| **Kanban 产出** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/kanban-result-retrieval.md` |
| **审计维度** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/review-audit-dimensions.md` |
| **Pitfall #144** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/pitfalls/pitfall-144-unblock-before-root-cause-fix.md` |
| **Gate Enforcer** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/gate-enforcer-plugin.md`（pre_tool_call hook 真机械门禁，已实现） |
| **防偏离调研** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/anti-deviation-patterns.md`（8 框架调研：Superpowers/GSD/Ralph Loop/Kiro/gstack/Spec Kit/OpenSpec/Trellis） |
| **防偏离模式库** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/anti-deviation-patterns.md`（8 框架调研 + 3 种真机械策略 + clsh-project 采用映射） |
| **调研方法论对比** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/research-methodology-comparison.md`（8 框架调研阶段方法论对比：Superpowers/Spec Kit/Kiro/OpenSpec/Ralph Loop/GSD/Phoenix/Trellis） |
| **增强调研模板** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/enhanced-research-template.md`（借鉴 Phoenix 威胁建模 + Kiro GIVEN...WHEN...THEN 验收标准） |
| **SDD 方法论研究** | `references/sdd-methodology-research.md`（邵猛 Spec-Driven Development 三 Skills：PRODUCT.md + TECH.md + validate-changes-match-specs） |
| **SDD 优化落地方案** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/sdd-optimization-plan.md`（SDD vs clsh-project 对比 + 优化落地优先级） |

## 🔧 Skill 维护

| 指南 | 路径 |
|------|------|
|| Pitfall 编号/膨胀/版本维护 | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/pitfall-catalog-maintenance.md` |
|| Skill 审计方法论 | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/skill-audit-methodology.md` |
| **机械脚本** | `/root/.hermes/scripts/gate-phase1.py` (Phase 1 调研维度覆盖检查), `/root/.hermes/scripts/gate-phase4.py` (G2+G3 原子化门禁), `/root/.hermes/scripts/gate-phase5.py` (tasks.md 合规), `/root/.hermes/scripts/gate-phase6.py` (tester 报告), `/root/.hermes/scripts/gate-phase8.py` (bugfix spec), `/root/.hermes/scripts/phase4-mechanical-check.py` (底层检查) |
| **Gate Enforcer** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/gate-enforcer-plugin.md`（pre_tool_call hook 真机械门禁，已实现） |
| **Phase 1 Gate 辅助** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase1-gate-auxiliary.md`（调研维度覆盖检查，5 维度 + 苏格拉底追问） |
| **调研方法论研究** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/requirements-research-methodology.md`（8 框架调研方法论对比：Superpowers/Spec Kit/Kiro/OpenSpec/Ralph/GSD/Phoenix/Trellis） |
| **防偏离调研** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/anti-deviation-patterns.md`（8 框架调研：Superpowers/GSD/Ralph Loop/Kiro/gstack/Spec Kit/OpenSpec/Trellis） |
| **防偏离机制对比** | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/anti-deviation-patterns.md`（8 框架调研：Superpowers/Kiro/Ralph Loop/GSD/gstack/Spec Kit/OpenSpec/Trellis，3 种真机械策略） |
| **描述层评分工具** | `python3 /root/.hermes/skills/clsh-darwin/scripts/darwin-scorer.py <SKILL.md>` — 9 维度文档质量评分器 |

### ⛔ 模板路径铁律（2026-06-10 确立）
模板只存 raw/ Vault，skill-local 不存副本。SKILL.md 用绝对路径指引，灵犀按需 `read_file()` 读取。新增引用文件同理。
### #153 验收标准必须含异常+边界场景（2026-06-12 E2E 复盘，普适）
**规则：** tasks.md 每个 Task 的验收标准不能只有功能正常路径。必须包含至少 1 条异常/边界场景的 GIVEN...WHEN...THEN。
**适用范围：** 所有项目类型。
**按项目类型补充：**
- 有网络 I/O → 必须有断连/超时/重试场景
- 有认证/权限 → 必须有未认证/越权/边界权限场景
- 有并发 → 必须有同位置/重叠/竞态场景
- 有数据处理 → 必须有空输入/超大输入/格式错误场景
**示例：**
- ❌ "GIVEN 用户 WHEN 提交表单 THEN 保存成功"
- ✅ "GIVEN 用户 WHEN 提交表单 THEN 保存成功；GIVEN 用户 WHEN 提交空表单 THEN 返回 400；GIVEN 用户 WHEN 提交他人资源 THEN 返回 403"
**根因：** 协同编辑器 E2E，T7 PUT 路由缺权限校验，T11 重连不回放 pendingOps — 都是因为验收标准只覆盖了正常路径。
### #154 TECH.md 必须覆盖外部交互异常路径（2026-06-12 E2E 复盘，条件触发）
**规则：** 如果项目有外部 I/O（网络请求、WebSocket、文件系统、外部 API），TECH.md 的"实现注意事项"必须覆盖异常路径。
**触发条件：** 项目涉及网络通信 / WebSocket / 外部 API 调用 / 文件 I/O。
**必须覆盖的异常路径：**
- 连接断开时客户端行为（丢弃/缓存/持久化？）
- 重连时双向同步协议（谁推给谁？顺序？）
- 超时处理策略（重试/降级/报错？）
- 操作持久化策略（内存/LocalStorage/IndexedDB？）
**反例：** 协同编辑器 TECH.md 只写"从服务端获取离线操作"，未写"客户端 pendingOps 如何处理" → coder 实现 send() 断连静默丢弃。
### #155 不变量必须拆到可验证子属性（2026-06-12 E2E 复盘，条件触发）
**规则：** 如果项目有并发/状态机/多角色交互等复杂行为，PRODUCT.md 的不变量不能用聚合描述，必须拆到可验证的子属性。
**触发条件：** 项目涉及并发编辑 / 状态机流转 / 多角色权限交互 / 分布式一致性。
**示例：**
- ❌ INV-2: "操作不丢失"（聚合，无法验证边界）
- ✅ INV-2a: "transform(op1, op2) 满足 TP1 属性"
- ✅ INV-2b: "compose 处理所有重叠情况，不静默丢弃"
- ✅ INV-2c: "并发删除同一区域时结果可确定"
**不需要拆的项目：** L1 CLI 工具（"输出正确"足够）、简单 CRUD（"数据不丢"足够）。
