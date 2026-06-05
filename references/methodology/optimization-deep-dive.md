# clsh-project 优化深度分析 — 从"借鉴什么"到"怎么改"

> 基于 four-framework-analysis.md 的 5 个高价值模式，本文档聚焦：**当前实现的精确缺口、代码级改动方案、模式依赖链、投入产出比评估、以及"不改什么"的证据辩护。**
>
> 分析时间：2026-06-03

---

## 总览：优化矩阵

| # | 模式 | Impact | Effort | 风险 | 依赖 | 优先级 |
|---|------|--------|--------|------|------|--------|
| 1 | Backpressure Gates | 🔴 极高 | 🟡 中 | 🟢 低 | 无 | **P0** |
| 2 | 自改进 Skill | 🟠 高 | 🟢 低 | 🟡 中 | #1 | P1 |
| 3 | Extension/Preset | 🟡 中 | 🔴 高 | 🟡 中 | 无 | P2 |
| 4 | GBrain 结构化知识 | 🟡 中 | 🟡 中 | 🟢 低 | 无 | P2 |
| 5 | 极简命令入口 | 🟢 低 | 🟢 低 | 🟢 低 | 无 | P3 |

**关键判断：** #1 是系统性缺陷（worker 可绕过验证），其他是体验优化。

---

## 模式 1：Backpressure Gates — 深度分析

### 1.1 当前状态的精确缺口

**现有机制：**
- phase6-execution.md 定义了 5 步验证函数（IDENTIFY → RUN → READ → VERIFY → REPORT）
- phase6-execution.md 定义了 Review Checklist（5 大类逐项填写）
- kanban worker 有 `kanban_complete(summary=...)` 接口

**缺口：这些全是"建议"，不是"强制"。**

具体来说：
1. **Worker 侧：** worker 的 SOUL.md 注入了 5 步验证规则，但 worker 可以选择性跳过，直接调用 `kanban_complete(summary="done")` — 没有任何代码级拦截
2. **灵犀侧：** 灵犀在 Step 7 验证 checkpoint，但验证逻辑是 LLM 判断（读 worker 的输出 → 判断是否 PASS），不是机械检查
3. **Kanban 侧：** `kanban complete` 命令没有 evidence 字段，complete 即完成，不检查任何前置条件

**实际案例（从 pitfalls 提取）：**
- pitfall #34: tester 只读代码就判 PASS，没有浏览器验证
- worker 假装完成（phase6-execution.md §Blocked 状态处理明确提到这个问题）
- 修复速度 ≠ 修复质量（way-c-iron-law pitfalls）

### 1.2 实现方案（3 层防线）

**Layer 1: Worker SOUL.md 强化（零代码改动，立即可做）**

在 worker 的 SOUL.md（`~/.hermes/agents/worker/SOUL.md`）中增加硬规则：

```markdown
## ⛔ 完成前必须做（不可跳过）

调用 kanban_complete() 前，body 必须包含以下证据，缺一不可：

1. **验证命令及输出** — 不是"我跑了测试"，是实际的命令+输出+exit code
2. **产出物路径** — 不是"文件已修改"，是 `ls -la` 的实际输出
3. **验收标准逐条对照** — 不是"满足所有标准"，是"标准1: PASS (证据: xxx)"

如果无法提供证据 → 调用 kanban_block(reason="无法验证")，不要调用 kanban_complete。
```

**效果：** worker 违规时至少会在 summary 中留下证据缺失的痕迹，灵犀验证时更容易拦截。
**局限：** 仍然依赖 worker 遵守，LLM 弱时可能忽略。

**Layer 2: 灵犀验证逻辑强化（SKILL.md 改动）**

在 phase6-execution.md 的 Step 4（灵犀验证 checkpoint）中增加**机械检查项**：

```markdown
### Step 4: 灵犀验证 checkpoint — 机械检查清单

收到 worker 的 checkpoint 后，逐项检查（不依赖 LLM 判断）：

- [ ] checkpoint 中是否有**实际命令输出**（不是"测试通过"，是"exit code: 0, output: ..."）
- [ ] checkpoint 中是否有**产出物路径**（绝对路径，可以 ls 验证）
- [ ] checkpoint 中是否有**验收标准逐条对照**（每条都有 PASS/FAIL + 证据）
- [ ] 产出物文件是否存在且大小 > 0（ls 验证）

任何一项缺失 → FAIL，返回 worker 重做。
**注意：** 这是机械检查（grep/ls），不是 LLM 判断"内容是否充分"。
```

**效果：** 灵犀验证从"LLM 感觉够不够"变成"机械项逐条检查"。
**局限：** worker 可以伪造证据（写假的命令输出），但成本比直接跳过高得多。

**Layer 3: Kanban 完成前校验（需要 Hermes 代码改动，长期）**

在 kanban 的 `complete` 动作中增加 evidence 校验：

```
kanban_complete() 时：
  if summary.length < 100 → reject("summary 太短，必须包含验证证据")
  if summary 不含 "exit code" AND 不含 "PASS" AND 不含 "截图" → reject("缺少客观验证证据")
```

**效果：** 代码级强制，LLM 无法绕过。
**局限：** 需要改 Hermes kanban 模块代码，且规则可能误杀合法的简单任务。

### 1.3 推荐实施路径

```
Layer 1（立即）→ Layer 2（SKILL.md 更新）→ Layer 3（按需，观察 Layer 1+2 效果后再决定）
```

**理由：** Layer 1+2 覆盖了 90% 的场景（worker + 灵犀双重检查）。Layer 3 需要改 Hermes 代码，只有在 Layer 1+2 仍频繁失效时才值得投入。

### 1.4 不改什么 + 理由

| 现有机制 | 保留理由 |
|---------|---------|
| 5 步验证函数 | 已经是正确框架，问题在于执行而非定义 |
| Review Checklist | 已经是机械检查项，与 Backpressure Gates 互补 |
| Auto-Fix 2 轮上限 | 防止无限循环，Backpressure Gates 不替代它 |
| tester 独立 review | Backpressure Gates 针对 worker，tester 是独立验证层 |

---

## 模式 2：自改进 Skill — 深度分析

### 2.1 当前状态的精确缺口

**现有机制：**
- Phase 6 checkpoint 后有微蒸馏（3 问题 → learnings.md + raw fix）
- Phase 7 有蒸馏评估（eval.json 8 项 → learnings.md）
- Phase 7 有执行审计（execution-audit.py → 合规率）
- self-evolution-mechanism.md 定义了 Darwin 9 维 rubric

**缺口：蒸馏结果不自动回流到 SKILL.md。**

具体流程断裂点：
1. 微蒸馏写入 `learnings.md`（project-wrap-up skill 的文件）
2. 蒸馏评估写入 `learnings.md`
3. 执行审计写入 `retrospective.md`
4. **但没有机制把 learnings.md 的教训自动注入到 SKILL.md 对应的 Phase 章节**

**结果：** 教训记录了，但下次执行时灵犀需要"记得去看 learnings.md"—— 这依赖 LLM 记忆，不可靠。

### 2.2 实现方案

**方案 A: Phase 7 归档时自动更新 SKILL.md（推荐）**

在 Phase 7 的步骤 7（蒸馏评估）后增加一个步骤：

```markdown
## Step 7.5: 教训回流（Phase 7 蒸馏后必做）

读取 learnings.md 中本轮新增的教训（[日期] 标记的条目）。
对每条教训：
  1. 判断它属于哪个 Phase（Phase 1-8）
  2. 判断它属于哪个类型：
     - Pitfall → 追加到 references/pitfalls/common.md 对应 Phase 的节
     - Workflow 改进 → 追加到对应 Phase 的 workflow 文件的注意事项
     - 原则变更 → 更新 SKILL.md 对应章节
  3. 写入后 ls 验证文件已更新

❌ 不做：修改 Darwin rubric（需要独立评估流程）
❌ 不做：删除旧教训（保留历史，用日期区分新旧）
```

**与 Ralph Loop "skill 可更新" 的对齐：**
- Ralph Loop: 每次运行后更新 instruction file
- clsh-project: 每次项目归档时更新 SKILL.md/pitfalls
- 差异：clsh-project 不是每次迭代都更新（太频繁），而是每个项目结束时更新（频率合理）

**方案 B: 执行审计结果自动注入（进阶）**

execution-audit.py 的输出已经是结构化的（合规率、pitfall 触发次数）。可以在 Phase 7 步骤 11 后增加：

```markdown
## Step 11.5: 审计结果注入

如果 execution-audit.py 输出的 pitfall 触发次数 > 0：
  对每个触发的 pitfall，在 references/pitfalls/common.md 对应条目中追加：
  `[触发记录] 项目:<项目名> 日期:<日期> 轮次:<N>`

目的：高频触发的 pitfall 自动获得更高的"置信度"，下次执行时灵犀会更重视。
```

### 2.3 风险分析

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| 自动更新引入错误规则 | 中 | 高 | 每次更新后 ls 验证 + 大佬可随时回滚（git） |
| SKILL.md 膨胀超过 900 行 | 低 | 中 | 膨胀阈值检查 + 自动迁移到 references/ |
| 教训误分类（Phase 归属错误） | 中 | 低 | 分类错误不影响执行，只是检索效率下降 |

### 2.4 不改什么 + 理由

| 现有机制 | 保留理由 |
|---------|---------|
| Darwin 9 维 rubric | 用于 SKILL.md 整体质量评估，不是单条教训的注入机制 |
| 微蒸馏 3 问题 | 已经是正确的触发条件，只是后续回流缺失 |
| execution-audit.py | 已经产出结构化数据，只需要增加注入步骤 |

---

## 模式 3：Extension/Preset 系统 — 深度分析

### 3.1 当前状态的精确缺口

**现有机制：**
- 所有 Phase 流程硬编码在 SKILL.md + references/workflow/ 中
- 无项目类型区分（web-app、content-site、cli-tool 走完全相同的流程）
- constitution.md 是唯一的项目定制点

**缺口：无法按项目类型裁剪 Phase。**

**实际案例：**
- content-site（如 clsh-content）：Phase 2.5（Spike）几乎不需要，因为技术栈固定
- cli-tool：Phase 3 的 UI 设计发散完全不需要
- web-app：Phase 8 的 Browser QA 必须做，但 content-site 可能不需要

### 3.2 实现方案

**方案：Project Profile 机制**

在 `references/templates/` 下新增 `project-profiles.md`：

```markdown
# Project Profiles

## web-app（Web 应用）
- 必做 Phase: 0-8 全部
- Phase 2.5: 可选（技术栈不确定时做）
- Phase 3 UI 设计发散: 必做
- Phase 6 Browser QA: 必做
- Phase 8 tester: 必须浏览器验证
- constitution 默认模板: web-app-constitution.md

## content-site（内容站点）
- 必做 Phase: 0, 1, 2, 3, 5, 6, 7
- 可跳过 Phase: 2.5（技术栈已知）, 4（轻量项目可合并到 3）
- Phase 3 UI 设计发散: 可选（用现有模板）
- Phase 6 Browser QA: 必做
- constitution 默认模板: content-site-constitution.md

## cli-tool（命令行工具）
- 必做 Phase: 0, 1, 2, 3, 5, 6, 7
- 可跳过 Phase: 2.5, 4, 8
- Phase 3 UI 设计发散: 不需要
- Phase 6 Browser QA: 不需要
- constitution 默认模板: cli-tool-constitution.md

## workspace-module（Workspace 子模块）
- 继承 web-app profile
- 额外约束: 必须遵循 workspace-development skill 的文件布局
- Phase 3: 必须参考 workspace-development 的设计系统
```

**使用方式：**
- Phase 0 时灵犀根据需求判断 project profile
- Phase 门禁检查时参考 profile 的"必做 Phase"列表
- 跳过的 Phase 在 overview.md 中记录原因

### 3.3 不实施 Extension 系统的理由

Spec Kit 的 Extension 系统（100+ 扩展）是为**社区生态**设计的 — 第三方可以发布扩展。clsh-project 是**单人使用**的工具，不需要社区扩展机制。

**替代方案：** Project Profile 是"轻量版 Preset"，覆盖了 80% 的需求（按项目类型裁剪），而不需要 Extension 的复杂性（安装/卸载/依赖管理/版本兼容）。

### 3.4 风险分析

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| Profile 判断错误（选错类型） | 中 | 中 | Phase 0 时向大佬确认 profile |
| 跳过 Phase 导致遗漏 | 低 | 中 | 跳过的 Phase 必须在 overview.md 记录原因 |
| Profile 维护成本 | 低 | 低 | 4 种 profile 覆盖 95% 场景 |

---

## 模式 4：GBrain 结构化知识 — 深度分析

### 4.1 当前状态的精确缺口

**现有机制：**
- `wiki/solutions/` 存储跨项目方案（自由文本 markdown）
- `wiki/solutions/INDEX.md` 有 tag taxonomy（10 初始方案）
- `raw/projects/<项目>/` 存储项目特定的 raw fix 记录
- Phase 7 步骤 9 触发 Solutions Ingest（raw → wiki/solutions/）

**缺口：solutions/ 的匹配靠全文搜索，没有结构化过滤。**

**实际场景：**
- Phase 0 准备阶段需要"查找相关方案"
- 当前做法：灵犀读 INDEX.md → 扫描 tag → 人工判断相关性
- 问题：INDEX.md 的 tag 是手动维护的，可能遗漏；全文搜索噪音大

### 4.2 实现方案

**方案：solutions/ frontmatter 结构化**

在 Solutions Ingest 流程中，新增 raw fix 记录时自动提取结构化 frontmatter：

```yaml
---
title: "Python urllib SSL 代理修复"
domain: proxy-networking
tech: python
error-type: ssl-handshake-failure
reusability: cross-project  # cross-project | project-specific
first-seen: 2026-05-24
last-used: 2026-06-01
times-triggered: 3
related-skills: [python-curl-proxy-fix, proxy-workarounds]
---
```

**Phase 0 匹配逻辑改进：**

当前：
```
灵犀读 INDEX.md → 扫描全文 → LLM 判断相关性
```

改进后：
```
灵犀读 INDEX.md → 按 domain/tech 过滤 → 只读相关 frontmatter → LLM 判断
```

**与 fact_store 的协同：**

Hermes 已有 Holographic Memory（fact_store），solutions/ 的结构化 frontmatter 可以作为 fact_store 的数据源：

```
Phase 7 Ingest 时：
  1. 写入 solutions/ markdown 文件（含 frontmatter）
  2. 同步写入 fact_store（domain/tech/error-type/reusability 作为 tags）
  
Phase 0 匹配时：
  1. 先查 fact_store（结构化查询，快）
  2. 未命中再查 solutions/ 全文（兜底）
```

### 4.3 与现有机制的关系

| 现有机制 | 与 GBrain 模式的关系 |
|---------|-------------------|
| wiki/solutions/ | 保留，增加 frontmatter |
| INDEX.md tag taxonomy | 保留，frontmatter 的 domain 与 tag 对齐 |
| fact_store | 新增数据源，不替代 solutions/ |
| Phase 7 Solutions Ingest | 扩展，增加 frontmatter 提取 + fact_store 同步 |
| Phase 0 准备 | 扩展，增加结构化查询步骤 |

### 4.4 不实施完整 GBrain 的理由

gstack 的 GBrain 有 8 种实体类型 + TTL + 字节预算 + 缓存层。这是为**大型团队 + 多产品线**设计的。clsh-project 是单人工具，不需要：
- TTL（知识不会过期到需要自动删除）
- 字节预算（个人 wiki 没有大小限制）
- 缓存层（LLM context 足够装下所有 solutions/ 的 frontmatter）

**替代方案：** frontmatter 结构化 + fact_store 同步覆盖了 90% 的需求（结构化匹配），而不需要 GBrain 的复杂性。

---

## 模式 5：极简命令入口 — 深度分析

### 5.1 当前状态

**已有：**
- `/clsh-project` = 注册的斜杠命令（SKILL.md frontmatter name: clsh-project → 注册 /clsh-project）
- `/clsh-project 继续 <项目名>` = 从上次中断的 Phase 继续
- `/clsh-project 归档 <项目名>` = Phase 7 归档

**⚠️ 注意：** `/cp` 从未被技术实现！skill_commands.py 只根据 `name` 字段注册命令，没有别名机制。如需 `/cp` 别名，需创建 skill bundle（见 `references/pitfalls/skill-alias-documentation-gap.md`）。

**缺口：** 这已经基本实现了 OpenSpec 的三命令极简（propose → apply → archive）。差距在于：
1. `/clsh-project` 触发完整流程，用户可能只想快速查看进度
2. 无 `/clsh-project 状态` 命令（查看当前 Phase + 下一步建议）

### 5.2 实现方案

在 SKILL.md 的触发条件中增加：

```markdown
## 快捷命令

| 命令 | 功能 | 内部行为 |
|------|------|---------|
| `/clsh-project` | 开始新项目 | 触发 Phase 0 → Phase 1 |
| `/clsh-project 继续 <项目名>` | 续做 | 读 overview.md → 从当前 Phase 继续 |
| `/clsh-project 状态 <项目名>` | 查看进度 | 读 overview.md + changes/ → 输出当前 Phase + 下一步建议 + 卡住的 blocker |
| `/clsh-project 归档 <项目名>` | 收尾 | 触发 Phase 7 |
```

### 5.3 投入产出比

**Effort：** 极低 — 只需在 SKILL.md 的触发条件中增加一个 case
**Impact：** 低 — `/clsh-project 继续` 已经覆盖了主要场景，`/clsh-project 状态` 是锦上添花
**优先级：** P3 — 有空再做

---

## 模式依赖链

```
Backpressure Gates (P0)
    ↓ 教训回流依赖"有可靠的验证结果"
自改进 Skill (P1)
    ↓ Profile 系统需要知道哪些教训属于哪种项目类型
Extension/Preset (P2)
    ↓ 结构化知识需要稳定的 Ingest 流程
GBrain 结构化知识 (P2)
    ↓ 独立
极简命令入口 (P3)
```

**关键路径：** Backpressure Gates → 自改进 Skill → 其他

---

## 不借鉴的模式 — 证据辩护

### 1. 单实例角色切换（gstack）

**gstack 做法：** 一个 agent 通过 SKILL.md 切换角色（CEO → 设计师 → QA）
**clsh-project 做法：** kanban worker 物理隔离（coder/artist/tester 是独立 agent）

**为什么不改：**
- 物理隔离 = 独立 context → 不会互相污染
- kanban 状态机 = 可追踪 → 每个 worker 的状态、耗时、产出物都有记录
- LLM 能力无关性原则 → 角色切换依赖 LLM 正确读取 SKILL.md，物理隔离不依赖

**数据支撑：** pitfall 案例中没有"因为物理隔离导致的问题"，但有"因为 LLM 判断力不足导致的问题"（pitfall #34 tester 自判 PASS）。

### 2. 可执行规范生成代码（Spec Kit）

**Spec Kit 做法：** 规范文件直接生成实现代码
**clsh-project 做法：** 规范给 worker 看，worker 自己写代码

**为什么不改：**
- 大佬的核心原则："人审代码" — 生成的代码无法保证质量
- Way C 铁律：worker 自己推理 → 更好的代码理解 → 更好的维护性
- 生成代码 = LLM 做代码推理 → 违反 LLM 能力无关性原则

### 3. bash while 循环（Ralph Loop）

**Ralph Loop 做法：** `while true; do claude < prompt.md; done`
**clsh-project 做法：** kanban 状态机 + dispatcher 自动派发

**为什么不改：**
- kanban 有 blocked/blocked/timeout 状态 → 比 bash 循环的 break/continue 更丰富
- kanban 有依赖链（parents）→ 自动 promote 子任务
- kanban 有 heartbeat + 超时 → 比 bash 循环的 sleep + check 更可靠
- kanban 有持久化 → 重启后继续，bash 循环重启后丢失状态

---

## 实施建议

### 立即执行（本周）

1. **Backpressure Gates Layer 1+2**
   - 更新 worker SOUL.md：完成前必须附带证据
   - 更新 phase6-execution.md Step 4：增加机械检查清单
   - 预计耗时：30 分钟

### 短期（本月）

2. **自改进 Skill — Phase 7 教训回流**
   - 更新 phase7-archive.md：增加 Step 7.5 教训回流
   - 预计耗时：20 分钟

3. **极简命令入口 — /cp 状态**
   - 更新 SKILL.md 触发条件
   - 预计耗时：10 分钟

### 中期（需要设计）

4. **Project Profile 系统**
   - 新增 references/templates/project-profiles.md
   - 更新 Phase 0 增加 profile 判断
   - 预计耗时：1 小时

5. **GBrain 结构化 — solutions/ frontmatter**
   - 更新 Phase 7 Solutions Ingest 流程
   - 更新 Phase 0 匹配逻辑
   - 预计耗时：1 小时

### 长期（观察后决定）

6. **Backpressure Gates Layer 3** — 只在 Layer 1+2 频繁失效时实施

---

## 总结

**clsh-project 的核心优势不在工具复杂度，而在流程门禁 + 角色分离 + LLM 能力无关性。** 四框架调研的最大价值不是"引入新工具"，而是"强化现有流程"：

1. **Backpressure Gates** = 强化已有的验证流程（从建议→强制）
2. **自改进 Skill** = 补上蒸馏→回流的断点（已有蒸馏，缺回流）
3. **Extension/Preset** = 轻量化（Profile 替代 Extension 系统）
4. **GBrain** = 结构化（frontmatter 替代完整知识库）
5. **极简命令** = 锦上添花（已有 /clsh-project，只需微调）

**核心判断：clsh-project 不缺框架，缺的是执行层面的"强制力"。** Backpressure Gates 是唯一的 P0。
