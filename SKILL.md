---
name: clsh-project-mimo
description: Spec-driven project workflow for MiMo Desktop with Obsidian vault integration — classify spike/bounded/architectural, phase gates, design approval, subagent execution. Use when the user says "我要做一个 XXX", "/clsh-project-mimo", "clsh", "spec-driven", "需求驱动", or starts a multi-step feature/project. Do NOT use for simple bugfixes, one-line changes, or pure Q&A.
license: MIT
compatibility: Requires Python 3.8+ (prefer $env:MIMO_PYTHON) and access to the Obsidian vault at UNC path //192.168.0.123/data/Obsidian. Uses task + actor tools when available.
metadata:
  author: MiMo Desktop
  version: 2.3.0
  category: workflow
  tags: [spec-driven, planning, workflow, obsidian, project-management, brainstorming]
  inspired-by: [clsh-project, obra/superpowers]
  vault: "\\\\192.168.0.123\\data\\Obsidian"
---

# clsh-project-mimo — MiMo Spec-Driven Flow（Obsidian 仓库版）

综合 **clsh-project**（阶段门禁 + 反合理化 + 机械脚本）与 **obra/superpowers**（路径分类 + 审批硬门 + TDD + 子代理执行），并落到本机 Obsidian 项目容器。

## Core Principle

**No production code before an approved design. Approval gate never shrinks — only the artifact does.**

**项目文档落在 Obsidian 仓库，不落在临时目录。** 仓库是记忆与复利的锚点。

## Vault 常量

| 常量 | 路径 |
|------|------|
| VAULT_ROOT | `\\192.168.0.123\data\Obsidian` |
| PROJECTS | `%VAULT_ROOT%\raw\projects` |
| WIKI | `%VAULT_ROOT%\wiki` |
| SOLUTIONS | `%VAULT_ROOT%\wiki\solutions` |
| TEMPLATES_VAULT | `%VAULT_ROOT%\_templates` |
| SCHEMA | `%VAULT_ROOT%\SCHEMA.md` |
| AGENTS | `%VAULT_ROOT%\AGENTS.md` |
| SKILL | `%USERPROFILE%\.claude\skills\clsh-project-mimo` |

项目容器（与仓库 OpenSpec 风格一致）：

```
raw/projects/<project-name>/
├── overview.md
├── source-of-truth/
│   └── constitution.md
└── changes/
    └── YYYY-MM-DD-<change-slug>/
        ├── conversation.md      # Phase 1
        ├── proposal.md          # Phase 2（方案对比 + 审批）
        ├── delta-specs/         # 可选
        ├── tasks.md             # Phase 3 计划
        ├── ledger.md            # Phase 4 执行账本
        ├── briefs/task-N-brief.md
        ├── reviews/task-N-review.md
        └── reports/task-N-report.md
    └── archive/<change>/        # Phase 6 归档
        └── completion-summary.md
```

## Iron Laws

1. **NO CODE WITHOUT PATH CLASSIFICATION + USER APPROVAL** — 两句设计也要点头。
2. **NO SELF-JUDGMENT ON QUALITY** — 脚本门禁 + 独立审查决定。
3. **COORDINATOR DOES NOT CODE** — 主会话规划/门禁/审查；`actor` 实现。
4. **ONE QUESTION AT A TIME** — 澄清期一次一问。
5. **LEDGER BEFORE DISPATCH** — 进度写文件，不只靠会话记忆。
6. **DOCS IN VAULT** — 阶段产出写进 `raw/projects/<project>/`，禁止散落在 cwd。
7. **CONSULT WIKI FIRST** — 开工前查 `wiki/INDEX.md` / `wiki/solutions/`，避免重复造轮子。
8. **NO GOAL PURSUIT IN PHASE 1–6** — Phase 1–6 禁止开启 Desktop goal pursuit / 自动继续；终止权在门禁与用户审批（对齐 clsh 对 /goal 的结论）。仅 Spike 探针或明确的 Phase8 类「迭代到收敛」且用户点头时可考虑。

## Role Agents（近似 Hermes bot）

模板在 `agents/clsh-*.md`（coder/artist/tester/reviewer/scout）。安装到项目 `.mimocode/agent/` 后可 `actor` spawn 专用角色。  
**无 bot-to-bot**：由主会话编排，或用 `session-chat` 建常驻命名会话。详见 `references/mimo-capabilities.md`。

| 角色 | 用途 |
|------|------|
| clsh-scout | Phase 0/1 调研证据 |
| clsh-coder | Phase 4 TDD 实现 |
| clsh-artist | UI 抛光（coder 之后） |
| clsh-reviewer | 双轴审查 |
| clsh-tester | 独立验收 |

## Anti-Rationalization Guard

引用本表来确认跳步 → **你在合理化。立即停止。**

| 你的想法 | 真相 |
|----------|------|
| "这太简单，不需要设计" | 简单 = 短设计，不是零设计。两句 + 审批。 |
| "我边写边让他们看设计" | 门禁是审批，不是文档长度。呈现后 STOP。 |
| "我熟悉这类项目" | 按仓库范围分类，不按熟悉度。新项目 = architectural。 |
| "修 bug 不用走流程" | 简单修复可跳全阶段，但仍先写失败测试。 |
| "用户说了继续/没问题" | 不是对具体方案的确认。要求确认方案内容。 |
| "我自己修更快，不派 actor" | 控制器修复跳过审查。恢复 implementer。 |
| "这阶段对本项目可选" | 隐性复杂度只允许升级路径，不允许降级。 |
| "先不查 wiki，我知道怎么做" | 铁律 7：先查 INDEX/solutions 再动手。 |
| "产出放项目目录就行，不用进 Obsidian" | 铁律 6：仓库是唯一文档锚点。 |

---

## Path Classification（第一步，始终）

宣布分类，再动手。复杂度只升不降。

| Path | 何时 | 流程 |
|------|------|------|
| **Spike** | 可行性探针，产出是结论不是保留代码 | 2-3 句探针计划 → 点头 → 调查 → 汇报建议 |
| **Bounded** | 已有仓库内的小范围改动 | 关键澄清 → **聊天里**短设计 → 审批 → TDD 实现 |
| **Architectural** | 新项目/子系统/接口变更/多组件 | 完整 Phase 0–6，文档进 Obsidian |

---

## Architectural Phases

用 `task` 工具登记阶段；`start`/`done` 同步推进。

| Phase | 目标 | 产出（相对 change 目录） | 门禁 |
|-------|------|-------------------------|------|
| 0 Research | 上下文 + wiki 复利查询 | `overview.md` 骨架 + 待确认问题 | script 0 |
| 1 Clarify | 一次一问澄清 | `conversation.md` | script 1 + 用户叫停 |
| 2 Spec | 方案对比 + 设计审批 | `proposal.md` | script 2 + **用户批准** |
| 3 Plan | 可执行任务清单 | `tasks.md` | script 3 |
| 4 Execute | actor 子代理逐任务实现 | code + `ledger.md` | 每任务审查 |
| 5 Verify | 整分支独立审查 + 修复循环 | reviews + ledger rulings | 无 Critical |
| 6 Archive | 归档 + 复盘 | `archive/.../completion-summary.md` | script 6 |

### Phase 0 — Research（机械扫描 + Wiki + 探索证据）

**IL-4：先跑机械扫描，禁止编造技术栈。**

1. **机械扫描（零 LLM）**：
   ```powershell
   & $env:MIMO_PYTHON "$env:USERPROFILE\.claude\skills\clsh-project-mimo\scripts\phase0_scan.py" <代码项目或容器路径>
   ```
   产出 `phase0-data.json`（top_level / tech_stack / git / seed questions）。
2. **先查 wiki**（铁律 7）：`hot.md` → `INDEX.md` → `solutions/`（cross-project）。
3. 探索代码库：`glob`/`grep`/`read`/`git log`（结构以 scan JSON 为准）。
4. **外部/竞品调研（IL-7）**——至少 2 类来源：
   - `webfetch` 抓官方文档/竞品页
   - 若 `websearch` 可用则先搜再 fetch
   - 若 Browser Use / Playwright 可用，用于 JS 重站点
   - 复杂调研 → `actor` spawn（`clsh-scout` 或 `general`），报告写入 change 目录
5. 建立/更新项目容器与 change 目录。
6. 写 `phase0-research.md`（或并入 overview）**必须**：
   - 引用 `phase0-data.json` 的 tech_stack/结构（**禁止编造**）
   - **≥10** 条编号问题，覆盖 ≥3 维度（功能/技术/边界/约束/异常/安全），格式：`1. [功能] ...?`
7. 写 `research-evidence.md`：
   ```markdown
   ## 探索证据
   - tool: webfetch | URL
   - tool: wiki | path
   - query: ...
   ## Findings
   ## Gaps
   ```
8. 运行门禁（会检查 scan JSON、问题数、证据节）。

### Phase 1 — Clarify（含 Scout）

1. 读 phase0 开放问题 + research-evidence。
2. **Scout（P0 强制）**：若问题含 `[技术]`/`[调研]`，或证据不足 → 先 `actor` spawn `clsh-scout`，报告落盘 `scout-report.md` / 更新 `research-evidence.md`，**再**向用户追问。
3. **一次一个**具体问题；优先 `question` 工具带选项。
4. 回答后复述（「你的意思是 X，对吗？」）再问下一个。
5. 维度轮转，至少覆盖 3 项：功能边界 / 异常 / 性能 / 安全 / 兼容。
6. 全部 Q&A 追加写入 `conversation.md`。
7. 停止条件：用户明确「需求确认 / 足够了 / 进入设计」且 ≥3 条实质回答。
   - 单独「继续」「好的」不算材料充分。
8. 范围蔓延 → backlog 小节。
9. 门禁（含探索证据检查）。

### Phase 2 — Spec / Design

1. 提出 **2-3 个方案**，带权衡与推荐（推荐放前）。
2. 无情 YAGNI；非目标写进 proposal。
3. 按 `templates/proposal.md` 写 `proposal.md`：概述 / 背景 / 方案对比表 / 影响范围 / 非范围 / 风险 / 测试策略 / 成功标准。
4. 方案必须能追溯到 phase0 证据；禁止发明未调研过的关键依赖。
5. 自检：无 TBD、内部一致、成功标准可测。
6. **用户审批门**：明确批准才进 Phase 3；批准后 `status: approved`。
7. 门禁。

### Phase 3 — Plan

按 `templates/tasks.md` 写 `tasks.md`：

- 精确文件路径（Create/Modify/Test）
- 接口 Consumed/Produced
- 步骤勾选：写失败测试 → 跑测失败 → 最小实现 → 跑测通过 → commit
- **禁止占位**：TBD / TODO / similar to Task N / 适当处理
- 每任务可有 `Kanban ID: [待创建]`（本环境无 kanban 时保留占位）

自检：spec 覆盖、跨任务命名一致。提供执行方式选择，默认 actor 子代理。

门禁。

### Phase 4 — Execute（A″：主会话治理 + workflow 流水线）

**Setup（主会话，不可委托）**
1. 确认 feature branch / 建议 worktree；禁止未同意直接改共享 main。
2. 从 `templates/ledger.md` 创建 change 下 `ledger.md`；首行写 plan 路径。
3. 预检冲突任务；`task` 工具建项。
4. 确认 Bootstrap：`check_agents.py <code_proj>`；缺 `clsh-coder.md` → 先 bootstrap 或 pipeline `useRoleAgents:false`。
5. 抽取本任务 brief → `<code>/.clsh/briefs/task-N-brief.md`（不要整份 plan）。
6. **禁止**两个 Phase4 task 并行改同一文件集。

**执行引擎（二选一）**

| 模式 | 何时 | 做法 |
|------|------|------|
| **默认 A″ workflow** | 角色已安装、任务独立 | 见下方 Pipeline |
| 降级 B actor | 无自定义 agent / 需逐步人工卡点 | 主会话 `actor` spawn/wait 串行 coder→artist?→tester→reviewer，契约同 schema 字段 |

**Pipeline（每任务一次，主会话在 workflow 外跑 gate/ledger）**

1. 记录 BASE `git rev-parse HEAD`。
2. 可选：生成 diff 包 `.clsh/reviews/task-N-diff.txt`。
3. 运行 workflow `clsh-task-pipeline`，传入：
   - `taskN`, `briefPath`, `reportDir=.clsh/reports`
   - `needUI`（无 UI 则 false，跳过 artist）
   - `maxFix=2`（可 3；超限必须交人）
   - `fromStage`（中断续跑）
   - `modelBase`（默认 standard）；`modelUpgrade`（有则用，**没有就传 null/省略，禁止写死不存在的组名**）
   - `useRoleAgents`（agent 未注册时 false → general+契约）
4. 读 `.clsh/reports/task-N-pipeline-result.json`：
   - `GREEN` → 生成 diff 包若尚未有 → 继续
   - `NEEDS_HUMAN` → 停止该 task，**必须**在 ledger 写 `NEEDS_HUMAN`，禁止静默忽略
5. **双写契约（P0）**：`.clsh/` 结果摘要 + Obsidian change `ledger.md`；gate 会用 `--code-project` 核对。
6. ledger：`Task N: complete (GREEN, fixRounds=…)` 或 blocked。
7. 完成前不启动下一任务；Phase 5 整分支审查不在此流水线内。

**卡死语义**

- `agent()` 超时/失败 → `null`（不会永久挂死 barrier）。
- 脚本用 `timeoutMs` + 最多 N 次升档重试；仍 null → `NEEDS_HUMAN`。
- 伪完成靠 **JSON schema 字段** + tester 真实 command 输出，不信散文自称 DONE。

**循环语义**

- tester FAIL / reviewer Critical → findings 写入 `task-N-open-findings.json` → 回 coder（纯 UI 可回 artist）并要求 `fixed_finding_ids` 覆盖 open ids。
- `maxFix` 熔断 → `NEEDS_HUMAN`。
- 每轮 ledger 追加 `fix round R`。

**交付模板（防幻觉，L1–L3）**

| 层 | 手段 |
|----|------|
| L1 | agent body + brief 钉死模板标题 |
| L2 | 主会话检查 JSON/MD 标题块 |
| L3 | workflow `schema` 强制字段（推荐） |

人读模板：`templates/reports/{coder,artist,tester,reviewer}-report.md`。流水线内以 **JSON schema** 为准。

**仅这四种情况停下问用户**：不可逆破坏、安全敏感、影响工作区外共享状态、计划彻底失效。其余 → 裁决、记账、继续。

### Phase 5 — Final Verify

1. 整分支独立审查（最强可用模型）。
2. **一次** fix 派发覆盖全部 findings。
3. **一次** scoped re-review。
4. 残余：park + ruling，或 load-bearing 则修复。
5. 最终回复列出所有 `Ruling:`。

### Phase 6 — Archive

1. 移动变更目录 → `changes/archive/<change>/`。
2. 写 `completion-summary.md`：交付物、变更文件、如何验证、遗留、流程复盘。
3. 更新 `overview.md`：状态、进度、变更历史表。
4. 若有可跨项目复利的修复教训 → 写入 `wiki/solutions/`（frontmatter 含 reusability/source_project）——**仅在此归档步骤允许写 wiki**；日常执行只读。
5. 门禁。

---

## Bounded / Spike（短路径）

**Bounded**：探索 → 必要澄清 → 聊天短设计 → **STOP 审批** → TDD 实现 → 验证。无强制 plan 文档；若用户要求，可仍写入 change 目录。

**Spike**：探针计划 2-3 句 → 点头 → 尽可能廉价地验证 → 汇报建议。产出标注 throwaway；要保留 = 新请求，重新分类。

---

## Architectural Bootstrap（角色安装，Phase 0 之前）

分类为 **Architectural** 后、跑 Phase 0 **之前**，在**代码项目**（不是 Obsidian 容器）执行一次：

```powershell
& $env:MIMO_PYTHON "$env:USERPROFILE\.claude\skills\clsh-project-mimo\scripts\bootstrap_roles.py" <code_project_dir>
```

会复制：

| 源（skill） | 目标（代码项目） |
|-------------|------------------|
| `agents/clsh-*.md` | `.mimocode/agent/` |
| `workflows/clsh-task-pipeline.js` | `.mimocode/workflows/` |
| （创建） | `.clsh/reports/` `.clsh/reviews/` |

**多项目并行：** 每个代码项目都要各自 bootstrap 一次；角色以**项目级** `.mimocode/agent/` 为准（可与全局 base 叠加，项目优先）。禁止在全局 SOUL 写死单一项目路径。

**验证：** 新对话或 `mimo agent list` / `@` 补全应出现 `clsh-coder` 等。Phase 4 入口若缺 `clsh-coder.md` → BLOCKED 或降级 `general`+角色契约。

Bounded/Spike 可不装；需要 UI 流水线时再补。

---

## TDD（一切写代码的路径）

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

先测试 → 看到正确失败 → 最小实现 → 通过 → 重构。先写实现？删掉重来。Spike 除外且保持 throwaway 标签。

---

## Gate Script

机械判断，LLM 从不充当门禁。

```powershell
& $env:MIMO_PYTHON "$env:USERPROFILE\.claude\skills\clsh-project-mimo\scripts\gate_phase.py" `
  "<vault>\raw\projects\<project>" "<change-slug>" <phase> [--code-project <code_proj>]
```

Phase 4/5 **应**传 `--code-project`：检查角色文件、pipeline-result 状态、NEEDS_HUMAN 是否写入 ledger、Phase5 是否全 GREEN。

```powershell
& $env:MIMO_PYTHON "...\gate_phase.py" `
  "\\192.168.0.123\data\Obsidian\raw\projects\my-app" "2026-09-09-notes-sync" 4 `
  --code-project "D:\code\my-app"
```

输出 `PASS` + confirm_code，或 `BLOCKED` + 原因。禁止编造确认码。

环境自检：

```powershell
& $env:MIMO_PYTHON "$env:USERPROFILE\.claude\skills\clsh-project-mimo\scripts\env_check.py"
```

---

## MiMo Desktop 工具映射

| 需求 | 工具 |
|------|------|
| 阶段/任务进度 | `task` create/start/done/block |
| 澄清选项 | `question` |
| 实现/审查 | `actor` spawn（`clsh-coder` / `clsh-reviewer`，或 `general`+角色契约） |
| UI | `actor` spawn（`clsh-artist`） |
| 调研 Scout | `actor` spawn（`clsh-scout`）+ webfetch/websearch/browser |
| 代码探索 | `actor` spawn（explore）或 glob/grep/read |
| 外部资料 | `websearch`（若可用）、`webfetch`、Browser/Playwright（若可用） |
| 常驻角色会话 | `session-chat`：`create_session` + `talk_to_session` |
| 门禁脚本 | `bash` + `$env:MIMO_PYTHON` |
| Wiki 只读查询 | 本 skill Phase 0 内流程；独立深度检索用 `obsidian-wiki-query` skill |
| 用户可见交付 | `present_files` |

---

## Examples

**用户：** 我要做一个本地笔记同步工具  
→ 宣布 architectural。查 wiki solutions。在 `raw/projects/notes-sync/` 建容器。Phase 0→6，文档进仓库。

**用户：** 给现有 API 加 `--dry-run`  
→ Bounded。聊天短设计。批准后 TDD。

**用户：** SQLite 做离线缓存可行吗？  
→ Spike。探针 → 结论。

**用户：** 空指针报错，修一下  
→ 不走全阶段；失败测试 → 修复 → 验证。

---

## Troubleshooting

| 症状 | 处理 |
|------|------|
| Vault UNC 不可达 | 检查网络/凭据；`Test-Path \\192.168.0.123\data\Obsidian` |
| 门禁缺 Python | 用 `$env:MIMO_PYTHON` 全路径 |
| BLOCKED missing file | 按 change 目录结构补齐，勿写 cwd |
| 用户对设计说「继续」 | 要求确认方案内容本身 |
| actor 返回 BLOCKED | 补上下文或升模型；禁止原样重试 |
| 会话 compact | 先读 change 目录 `ledger.md`，信它不信记忆 |
| 范围膨胀 | 停止、升级分类、告知用户 |

---

## 详细参考

- 阶段配方与停止条件：`references/phases.md`
- Wiki 检索顺序与工具：`references/wiki-search.md`
- MiMo 多角色/actor 对照：`references/mimo-capabilities.md`
- Superpowers 逐步对比：`references/superpowers-diff.md`
- Phase4 流水线与卡死/循环：`references/pipeline-runtime.md`
- 历史陷阱：`references/pitfalls.md`
- 角色 agent 模板：`agents/clsh-*.md`
- 交付模板：`templates/reports/`
- 流水线：`workflows/clsh-task-pipeline.js`
- 角色安装：`scripts/bootstrap_roles.py`
- 角色自检：`scripts/check_agents.py`
- 产出模板：`templates/`
