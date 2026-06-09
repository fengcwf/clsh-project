---
name: clsh-project
aliases: [cp]
description: "需求驱动的项目开发工作流 — 从需求澄清到设计文档到实现计划到执行。灵感来自 Kiro 的 Spec-Driven Development、Superpowers 的 Brainstorming 方法论、Phoenix 的状态机执行模式。DO trigger: 用户说'我要做一个 XXX'、'开发一个 XXX 系统'、'/clsh-project'、'/cp'、'按 Kiro 流程走'、需求明显是多步骤项目。Do NOT trigger: 简单查询、单步操作、修 bug（用 systematic-debugging）、已有明确方案的小改动、用户说'简单做一下'、代码质量审查（PR review）。"
version: 5.49.0
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
- 调试方法论 → `diagnose` skill
- 代码质量规则 → `code-principles` skill

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

### Layer 1: Gate（机械硬阻断，违反 = 流程阻断）

| # | 规则 | 机械机制 |
|---|------|---------|
| G0 | **先查进度再行动** — `ls` + 读 overview.md + 读 changes/，从下一个未完成 Phase 继续 | 文件系统检查 |
| G1 | **文档先于代码** — Phase 3 未完成 + 大佬未确认，禁止写代码 | 文件存在性检查 |
| G2 | **Phase 4 机械自检** — 调用 `phase4-mechanical-check.py` | 脚本 PASS/FAIL |
| G3 | **机械确认码脚本生成** — `python3 -c "import secrets,string; ..."`，禁止 LLM 编造 | 脚本输出 |
| G4 | **Phase 8 bugfix spec 门禁** — 跑 `phase8-spec-check.py`，FAIL = 不允许派发 | 脚本拦截 |
| G5 | **Phase 8 结束前机械自检** — 执行 `~/.hermes/scripts/phase8-pre-close-check.py <项目目录>`。检查文档完整性+代码语法+确认码格式+角色分离+测试产出 | 脚本 PASS/FAIL |
| G6 | **文档路径验证** — 写入后必须 `ls` 验证 | `ls` 输出 |
| G7 | **完成声明前验证** — 执行 `~/.hermes/scripts/phase6-5step-verify.py --file <checkpoint>`。检查 checkpoint 是否包含 5 步结构：IDENTIFY→RUN→READ→VERIFY→REPORT。跳过任何一步 = lying, not verifying | 脚本 PASS/FAIL |
| G8 | **角色标注检查** — 执行 `~/.hermes/scripts/check-role-annotations.py <tasks.md>`。检查每个 Task 标注 (coder)/(tester)/(artist)，无 TBD/TODO，有验收标准 | 脚本 PASS/FAIL |

### Layer 2: Convention（架构约束，通过设计而非自觉强制）

| # | 规则 | 执行方式 |
|---|------|---------|
| C0 | **角色分离：灵犀只记录，不分析** — Phase 8 灵犀只记录现象+文件+验收标准，coder/artist 自己分析根因+设计方案+执行。灵犀不是分析者 | 架构约束（task body 只含信息，不含分析） |
| C1 | **Phase 5 派 coder 写 tasks** — 灵犀派 kanban 卡（body 含 proposal + constitution 路径），coder 自己写 tasks.md，灵犀 review 格式合规但不改内容 | kanban 派发 |
| C2 | **proposal 只写设计决策** — 功能清单/API 合约/数据模型/架构约束/文件范围，不写实现细节 | 评分器检测（clsh-unified-scorer.py） |
| C3 | **独立测试** — 代码任务必须有 tester kanban 卡，禁止自己测自己验收 | `hermes kanban list --assignee tester` 非空 |
| C4 | **方案注入** — Phase 6 建卡时 body 必须注入 proposal + constitution + scope | task body 关键词检查 |
| C5 | **Phase 确认用模板** — 每个 Phase 结束使用对应确认模板，`[CODE]` 由脚本生成。飞书渠道自动渲染为流式卡片（Card JSON 2.0），微信渠道保持纯文本。**码必须独占一行，前后无 emoji/前缀/说明文字**（方便复制） | 模板路径索引 + 确认码格式校验 |
| C6 | **每个 Task 标注角色** — tasks.md 中每个 Task 必须标注 `(coder)` / `(tester)` / `(artist)` | 角色标注检查 |
| C7 | **灵犀 review = 流程合规 + Buildability review** — Phase 5-6 执行后灵犀 review 的是：文件存在、角色标注、验收标准、scope 对照、**Buildability**（task 是否可执行：步骤是否清晰、有没有模糊到 coder 会卡住、有没有 placeholder/TBD）。不是代码 review（代码 review 由 tester 做）。借鉴 Superpowers plan-document-reviewer 的 Completeness + Decomposition + Buildability 检查 | 流程合规 checklist |
| C8 | **kanban 派发必须注入 skills** — 每个 kanban 卡的 `--skill` 参数必须包含角色默认技能（coder: TDD+调试, artist: 设计+前端, tester: 审查+调试）。不指定 = 流程违规 | phase6-dispatch-template.md 技能注入映射表 |

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

**⚠️ 歧义提醒："测试 X" vs "创建新项目"**
- "测试 XX，需求：A+B+C" → **新项目**，"测试"是项目类型，走完整流程
- "帮我测试一下 XX"、"跑一遍测试"、"验证 XX 功能" → **测试现有代码**，用 systematic-debugging 或直接执行

## Review Mode（规格合规审查）

7 步：读项目文档 → 读所有代码 → 验证运行状态 → 功能合规矩阵 → Constitution 合规 → 代码质量（P1-P6） → 汇报。

📋 详细流程: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase-review.md`

**红线：** 产出报告，不直接修复。修复走 Phase 8。

---

## 流程总览

```
Phase 1: 需求澄清（调研循环 + 机械确认码）→ conversation.md
    ↓ [大佬确认]
Phase 2: 提出 2-3 个方案 + 推荐理由 → 大佬选择
    ↓ [大佬确认]
Phase 2.5: Technical Spike（可选）
    ↓ [VALIDATED]
Phase 3: 设计文档 → proposal.md + constitution.md
    ↓ [大佬确认]
Phase 4: 自检 + 大佬确认
    ↓ [大佬确认进入执行]
Phase 5: 实现计划 → 派 coder 写 tasks.md → 灵犀 review → 进入 Phase 6
    ↓
Phase 6: Ralph Loop 分发执行（coder/artist/tester）
    ↓ [tester 通过]
Phase 7: 归档 + 流程复盘
    ↓
Phase 8: 反馈循环 → 回到 Phase 1 或 Phase 6
```

### 🚀 Session Launch Guidance

| 完成 Phase | 下一步 | 建议 |
|-----------|--------|------|
| Phase 1-5 | `/clsh-project 继续 <项目名>` | 当前 session 继续 |
| Phase 6 | `/clsh-project 继续 <项目名>` | 3+ Task 建议新 session |
| Phase 7 | 等待大佬测试反馈 | — |
| Phase 8 | `/clsh-project 继续 <项目名>` | 每轮修复建议新 session |

### 🅿️ 项目暂存

大佬说"先存 wiki，不做"时：写 overview.md（状态 `planning`）+ proposal.md → 向大佬确认 → **不进入 Phase 2+**。

---

## Phase 0+1: 需求准备与澄清

调研循环模式：每个决策点走 `L0→L1→L2` 分层调研→提问→确认微循环。机械确认门禁 + 代码交叉验证 + CONTEXT.md 术语表。

📋 详细流程: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase0-1-requirements.md`
📋 确认模板: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/phase-confirmations.md` → Phase 1

---

## Phase 2+2.5: 方案设计与技术验证

2-3 个方案 + 推荐理由 + 对比表格。Phase 2.5: 技术 Spike + 设计 Prototype。

📋 详细流程: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase2-design.md`
📋 确认模板: `…/templates/phase-confirmations.md` → Phase 2

---

## Phase 3+4: 设计文档与自检

Phase 3: proposal.md + constitution.md + 可选 ADR。**⛔ proposal 只写设计决策（铁律 #22）。** Phase 4: 机械检查 + 流程合规 + Review Gate。

📋 流程: `…/workflow/phase3-spec.md` | 📋 自检: `~/.hermes/scripts/phase4-mechanical-check.py` | 📋 确认模板: `…/templates/phase-confirmations.md`

---

## Phase 5: 实现计划（派 coder 执行）

灵犀派 kanban 卡（body 含 proposal + constitution 路径），coder 自己写 tasks.md。**⛔ 每个 Task 标注角色（铁律 #22）。⛔ 灵犀只 review 格式，不改内容。**

📋 流程: `…/workflow/phase5-tasks.md`

---

## Phase 6: Ralph Loop 分发执行

Way C 铁律：灵犀给目标+路径+约束，不做代码推理。**角色分工：** coder/artist → kanban worker | tester → kanban review 卡。**⛔ tester 必须产出持久化测试文件。** 执行后灵犀做**流程合规 review**（C7）：文件存在、角色标注、验收标准、scope 对照。代码质量由 tester review。

📋 流程: `…/workflow/phase6-execution.md`

---

## Phase 7: 完成归档与流程复盘

归档 9 步 + 流程合规复盘 7 项 + handoff.md。**使用 `handoff` skill。**

### ⛔ 归档文档关键词（机械门禁）

| 文档 | 关键词 | 行数上限 |
|------|--------|---------|
| completion-summary.md | `概述`, `技术`, `功能`, `限制` | ≤ 40 行 |
| retrospective.md | `合规`, `教训`, `改进`, `角色` | ≤ 40 行 |
| handoff.md | `状态`, `建议` | ≤ 30 行 |

📋 详细流程: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase7-archive.md`

---

## Phase 8: 反馈循环

**信息传递模式（C0）：** 灵犀只记录现象+文件+验收标准，coder/artist 自己分析根因+设计方案+执行。tester 浏览器验证。每轮归档 + 上下文溢出防护（每轮 ≤3-4 bug）。

### ⚠️ Phase 8 测试需求超出原始范围

当项目 Phase 7 已归档（状态 `done`），大佬要求"测试"但需求包含原始 `proposal.md` "不在范围内"的功能时：

1. **先验证** — 启动服务 + 跑基础功能测试，确认现有代码可用
2. **识别差距** — 对比测试需求 vs 原始 scope，列出缺失功能
3. **向大佬确认意图** — 三种可能：
   - A) 只测试现有功能（回归测试）
   - B) 先补充缺失功能再测试（需求变更，需新 Phase 1+）
   - C) 全部功能都要但接受部分未实现
4. **不假设** — 即使 90% 确定大佬意图，也必须确认

**铁律：** 测试需求超出原始 scope 时，禁止自行扩展实现。必须先向大佬确认意图，再决定走 Phase 8 bugfix 还是新需求 Phase 1。

📋 详细流程: `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/workflow/phase8-feedback.md`
📋 完整 pitfalls: `references/pitfalls/common.md` #126-#136

---

## E2E 自动化测试

| 组件 | 路径 |
|------|------|
| 主脚本 | `~/.hermes/scripts/clsh-e2e-test.py` |
| Cron wrapper | `~/.hermes/scripts/clsh-e2e-cron.sh` |

---

## 流程门禁

| 门禁 | 检查内容 | 未通过 → |
|------|---------|---------|
| Phase 3→4 | proposal.md 已写入 + `ls` 验证 | 不允许写代码 |
| Phase 4→5 | 机械确认码 | 不允许写 tasks.md |
| Phase 5→6 | tasks.md 已写入 + 每 Task 有验收标准 | 不允许创建 kanban 卡 |
| Phase 6 执行 | 代码任务必须有 tester 卡 | 不允许标记完成 |
| Phase 6 安全 | tester Security Scan 通过 | 不允许进入 Quality Review |
| Phase 6 修复 | Auto-Fix 最多 3 轮 | escalate 给大佬 |
| Phase 6 测试 | tester 验证通过 | 不允许汇报完成 |
| Phase 6 Browser QA | UI 项目 tester 必须浏览器验证 | 不允许汇报完成 |

## 核心规则精选

**角色分离（C0）：** 灵犀只做信息传递，不分析根因、不设计方案、不写代码。coder/artist 自己分析+执行。Phase 8 task body 只含现象+文件+验收标准。

**Way C 铁律（C1）：** 灵犀只给目标+路径+约束，不做代码推理。Pattern to Follow 必做。worker 修复后必须走 tester 验证。

**流程合规 + Buildability review（C7）：** 灵犀 review 的是流程合规（文件存在、角色标注、验收标准、scope）和 Buildability（task 可执行性：步骤清晰、无 placeholder/TBD、不会让 coder 卡住）。不是代码质量。代码质量由 tester review。

> 完整 pitfalls 词典 → `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/pitfalls/common.md`

## ⚠️ Skill 别名

`/cp` 通过 frontmatter `aliases: [cp]` 注册为 `/clsh-project` 的别名。

> 完整 pitfalls 词典（#1-#136）→ `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/pitfalls/common.md`

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v5.49.0 | 2026-06-09 | **机械执行器补全**：G5/G7/G8 获得脚本（phase8-pre-close-check.py / phase6-5step-verify.py / check-role-annotations.py）。Security Scan 归属从灵犀改为 tester（铁律 2）。Gate 从 8 个扩展到 9 个（+G8 角色标注检查）。Pitfalls #137-#139。 |
| v5.48.0 | 2026-06-09 | **飞书 Card-First 架构**：lark-cli bridge 升级为交互式卡片为主通道。表格/标题/代码块原生渲染。Pitfalls #135-#136（divider→hr, update_multi）。C5 确认模板渠道适配。参考文件重写。 |
| v5.47.0 | 2026-06-09 | **角色分离大重构（本次 session）**：(1) 铁律三层架构：23 条→Gate(8)/Convention(8)/Pitfall 降级 (2) C0 灵犀只记录不分析 (3) C1 Phase 5 派 coder 写 tasks (4) C2 proposal 只写设计决策 (5) G4 Phase 8 bugfix spec 门禁脚本 (6) C7 流程合规 review (7) C8 kanban skill 注入 (8) coder 移除 vision toolset (9) Anti-Rationalization 表 (10) Pitfalls #1-#50 归档。借鉴 Superpowers brainstorming/writing-plans + gstack /design-consultation + Ralph Loop backpressure。 |


---

> 完整版本历史 → `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/version-history.md`

---

## 📚 参考文件

| 分类 | 路径 |
|------|------|
| **工作流** | `…/references/workflow/` |
| **模板** | `…/references/templates/` |
| **教训** | `…/references/pitfalls/common.md` |
| **方法论** | `…/references/methodology/` |
| **集成** | `…/references/integration/` |
| **归档** | `…/references/archive/` |

> `…` = `/mnt/unraid_data/Obsidian/raw/projects/clsh-project`

## 🔧 Skill 维护

| 指南 | 路径 |
|------|------|
| Pitfall 编号/膨胀/版本维护 | `references/pitfall-catalog-maintenance.md` |
| Skill 审计方法论 | `references/skill-audit-methodology.md` |
| **机械脚本** | `~/.hermes/scripts/phase4-mechanical-check.py` (G2), `phase6-5step-verify.py` (G7), `phase8-pre-close-check.py` (G5), `check-role-annotations.py` (G8) |
