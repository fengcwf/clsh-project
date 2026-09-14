# Phase Recipes（Obsidian 容器版）

SKILL.md 是路由；本文件是配方。所有路径相对于
`\\192.168.0.123\data\Obsidian\raw\projects\<project>\`。

## Phase 0 — Research

**Do**
1. 读 wiki hot/INDEX/solutions（见 wiki-search.md）。
2. 清点代码库与技术栈。
3. 列开放问题标签：`[功能][边界][异常][性能][安全][技术]`。
4. 创建/更新 `overview.md`（含开放问题或约束）。
5. 创建 `source-of-truth/constitution.md`（硬约束）。
6. 创建变更目录 `changes/YYYY-MM-DD-<slug>/`。

**Gate:** `gate_phase.py <project_dir> <slug> 0`

---

## Phase 1 — Clarify

**Do**
1. 选最高价值开放问题。
2. 一次一问（优先 `question` 工具）。
3. 复述理解后再问下一题。
4. 覆盖 ≥3 维度。
5. 追加到 `conversation.md`。

**停止仅当**：用户明确「需求确认/足够了/进入设计」且 ≥3 条实质回答。  
**硬上限**：15 问后暂停请示。

**Gate:** `gate_phase.py <project_dir> <slug> 1`

---

## Phase 2 — Design

**Do**
1. 2-3 方案 + 推荐 + 权衡。
2. YAGNI；写清 Non-goals。
3. 按 `templates/proposal.md` 写 `proposal.md`。
4. 自检后 **请用户审阅全文**。
5. 批准后把 frontmatter `status: approved`。

**批准用语**：批准 / 同意这个方案 / approved  
**不算批准**：继续 / 好的 / 你看着办

**Gate:** `gate_phase.py <project_dir> <slug> 2`

---

## Phase 3 — Plan

**Do**
1. 先做 file map。
2. 任务粒度：每步 2-5 分钟可执行。
3. 具体测试代码与命令；禁止占位符。
4. 自检跨任务命名。
5. 选择 actor 执行或内联执行。

**Gate:** `gate_phase.py <project_dir> <slug> 3`

---

## Phase 4 — Execute

**Setup**：feature branch → `ledger.md` → 预检冲突表 → `task` 工具建项。

**Loop**
1. `briefs/task-N-brief.md`（仅本任务）。
2. `actor` general 派发；报告写 `reports/task-N-report.md`。
3. BASE commit → review package 文件 → reviewer 子代理。
4. 双轴：spec 合规 + 质量。
5. 修复 ≤3 轮 → 裁决 + ledger。
6. `Task N: complete (...)`。

**仅停下问用户**：不可逆 / 安全 / 共享副作用 / 计划全毁。

**Gate:** `gate_phase.py <project_dir> <slug> 4`

---

## Phase 5 — Verify

1. 整分支审查。
2. 一次 fix + 一次 scoped re-review。
3. park 或修复 load-bearing。
4. 汇总全部 Ruling 给用户。

**Gate:** `gate_phase.py <project_dir> <slug> 5`

---

## Phase 6 — Archive

1. `changes/<slug>/` → `changes/archive/<slug>/`。
2. 写 `completion-summary.md`。
3. 更新 `overview.md` 状态与变更历史。
4. （可选）写 `wiki/solutions/` 跨项目条目。
5. `source-of-truth/` 若系统状态有变则增量更新。

**Gate:** `gate_phase.py <project_dir> <slug> 6`

---

## 路径升级

| 触发 | 动作 |
|------|------|
| Bounded 发现新子系统 | 升级 architectural，停止并告知 |
| Spike 代码要保留 | 新请求，重新分类 |
| 一 spec 跨多独立子系统 | 拆成多轮 plan→execute |
