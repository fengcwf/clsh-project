# Pitfall Catalog 维护指南

> 何时写、怎么写、怎么编号、怎么防膨胀。

## 添加新 Pitfall 的标准流程

### Step 1: 确定编号
```bash
# 查 common.md 最后一条 pitfall 的编号
grep "^## Pitfall #" /mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/pitfalls/common.md | tail -3
```
新 pitfall 编号 = 最大编号 + 1。**绝不复用已有编号。**

### Step 2: 写入 common.md
追加到文件末尾的 `---` 之前。格式：
```markdown
## Pitfall #N: 标题（YYYY-MM-DD 教训）

**场景：** 触发条件描述
**根因：** 为什么发生
**铁律：** 防止再犯的规则
**验证：** 怎么检查
```

### Step 3: 更新 SKILL.md 索引（不是内联！）
SKILL.md 的"近期 Pitfalls 索引"节只放表格行：
```
| #N | 标题 | 来源 |
```
**禁止在 SKILL.md 中内联 pitfall 完整内容。** 完整内容只在 common.md。

### Step 4: 同步 frontmatter version
每次修改 SKILL.md（包括 pitfall 索引更新）必须同步 `version` 字段。

## 编号冲突预防

**已知冲突案例（2026-06-09）：** 两批独立添加的 pitfalls（v5.41 和 v5.42）各自从 #117 开始编号，导致 #117-#118 各出现两次。

**根因：** 添加时没查 common.md 的当前最大编号。

**铁律：** 添加前 `grep "^## Pitfall #" ... | tail -1` 确认当前最大编号。

## ⛔ 双位置同步铁律（2026-06-09 教训）

**common.md 存在于两个位置，添加 pitfall 时必须同步更新：**

| 位置 | 路径 |
|------|------|
| **raw**（权威） | `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/pitfalls/common.md` |
| **skill-local** | `~/.hermes/skills/productivity/clsh-project/references/pitfalls/common.md` |

**⛔ 只更新一个 = 另一个会被覆盖或丢失。**

**操作流程：** 先改 raw → 再 `cp raw skill-local` → `diff` 验证行数一致。

**反例（2026-06-09）：** common.md 从 433 行截断到 25 行。git diff 显示文件被删除后重建为子集。根因：只改了 skill-local，raw 完整内容没有同步过来。

**同理适用于：** templates/ 目录下的文件（phase-confirmations.md 等同时存在于 raw 和 skill-local）。

## SKILL.md 膨胀控制

| 内容 | 放哪里 | 原因 |
|------|--------|------|
| Pitfall 完整内容（场景+根因+铁律+验证） | common.md | SKILL.md 行数预算有限 |
| Pitfall 一行索引（编号+标题+来源） | SKILL.md "近期 Pitfalls 索引" | 快速扫描，链接到 Vault |
| Phase 描述（详细流程） | workflow/*.md | SKILL.md 只放摘要+链接 |
| Phase 模板关键词表 | workflow 文件 + 机械检查脚本 | 不在 SKILL.md 中重复 |
| Anti-Rationalization 表 / 旧铁律降级表 | common.md 或一行摘要+指针 | ~15-30 行 |

**阈值：** SKILL.md ≤ 350 行，common.md ≤ 150 条。

### 瘦身操作模式

超限时按优先级迁移：Pitfall 完整表→一行摘要+`详见 common.md`。不丢失信息（common.md 有完整内容），只减少 SKILL.md 行数。

**已验证的瘦身案例（2026-06-09）：** 391→333 行（-58 行）。
- 移除 Anti-Rationalization 表（7 行）→ 一行摘要
- 移除旧铁律降级表（11 行）→ 一行摘要
- 移除 Phase 8 Pitfalls 表（4 行）→ 链接到 common.md #126-#136
- 移除近期 Pitfalls 索引（18 行）→ 一行指针

**⛔ 瘦身后必须重新 `wc -l` 验证。** 不能凭估算。

---

## 审计方法论

详见 `references/skill-audit-methodology.md` — 5 种偏差模式 + 审计清单 + SKILL.md 瘦身技术。

## 版本历史规范

SKILL.md 只保留最近 3 版（一行摘要）。完整历史在 Vault `references/templates/version-history.md`。

**铁律：** frontmatter `version` 必须与版本历史表最新版本一致。不一致 = 流程违规。
