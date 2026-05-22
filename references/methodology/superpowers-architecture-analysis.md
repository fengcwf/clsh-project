# Superpowers 架构分析 → clsh-project 重构参考

> 来源：https://github.com/obra/superpowers (v5.1.0, 201k stars)
> 分析时间：2026-05-22

## Superpowers 6 条设计原则

| # | 原则 | Superpowers 做法 |
|---|------|-----------------|
| 1 | **一 skill 一职责** | brainstorming 只管需求→设计，writing-plans 只管计划，executing-plans 只管执行 |
| 2 | **SKILL.md ≤ 500 行** | 最大的 subagent-driven-development ~400 行 |
| 3 | **references = 重型辅助文件** | reviewer prompt、工具适配（codex-tools.md）、implementer prompt |
| 4 | **教训内嵌到对应 skill** | 每个 skill 有 "Common Mistakes" 小节（5-10 条），不在别处堆积 |
| 5 | **skill 间用名字互相引用** | "Use superpowers:writing-plans" 而不是嵌入内容 |
| 6 | **流程图定义入口/出口** | 每个 skill 有 dot 流程图，明确何时触发、何时终止 |

## Superpowers Skill 清单（14 个）

| Skill | 职责 | 行数 | references 文件 |
|-------|------|------|----------------|
| using-superpowers | 总入口索引 | ~200 | codex-tools.md, copilot-tools.md, gemini-tools.md |
| brainstorming | 需求→设计 | ~300 | spec-document-reviewer-prompt.md, visual-companion.md |
| writing-plans | 设计→计划 | ~250 | plan-document-reviewer-prompt.md |
| executing-plans | 计划→执行（无 subagent） | ~150 | 无 |
| subagent-driven-development | 计划→执行（有 subagent） | ~400 | implementer-prompt.md, spec-reviewer-prompt.md, code-quality-reviewer-prompt.md |
| finishing-a-development-branch | 完成→合并/PR | ~300 | 无 |
| verification-before-completion | 验证门禁 | ~150 | 无 |
| requesting-code-review | 代码审查 | ~200 | 无 |
| test-driven-development | TDD 方法 | ~200 | 无 |
| systematic-debugging | 调试方法 | ~200 | 无 |
| writing-skills | Skill 编写指南 | ~300 | anthropic-best-practices.md |
| using-git-worktrees | Git worktree | ~150 | 无 |
| dispatching-parallel-agents | 并行 agent | ~150 | 无 |
| receiving-code-review | 接受审查 | ~150 | 无 |

## Superpowers references 模式

**原则：references 只放"重型辅助文件"（100+ 行的模板/prompt），不放知识碎片。**

三类 references：
1. **Reviewer prompt 模板** — spec-document-reviewer-prompt.md、plan-document-reviewer-prompt.md、code-quality-reviewer-prompt.md
2. **Implementer prompt 模板** — implementer-prompt.md（派给 coder 的完整指令）
3. **工具适配** — codex-tools.md、copilot-tools.md、gemini-tools.md（不同 IDE 的工具映射）

**不在 references 里的东西：**
- 教训/踩坑 → 内嵌到对应 skill 的 "Common Mistakes"
- 方法论研究 → 不需要（skill 本身就体现方法论）
- 流程违规案例 → 不需要（skill 的 "Red Flags" 小节覆盖）

## clsh-project 与 Superpowers 的映射

| Superpowers skill | clsh-project Phase | 映射关系 |
|-------------------|-------------------|---------|
| brainstorming | Phase 1 | 几乎 1:1（一次一个问题、多选优先、Visual Companion） |
| writing-plans | Phase 4-5 | 1:1（Self-Review、No Placeholders、Type Consistency） |
| executing-plans | Phase 6 | Ralph Loop + Kanban（clsh 更复杂，多了状态机+超时+归档） |
| subagent-driven-development | Phase 6 | delegate_task + checkpoint + two-stage review |
| finishing-a-development-branch | Phase 7 | 归档+复盘（clsh 多了 wiki 归档检查清单） |
| verification-before-completion | Phase 6 checkpoint | 1:1（"Evidence before claims"） |
| systematic-debugging | Phase 8 | diagnose 6 阶段（clsh 额外有路径 A/B/C） |
| writing-skills | N/A | clsh 不需要（不教别人写 skill） |

## 关键认知

1. **Superpowers 没有"教训堆积"概念** — 每个 skill 自带 Common Mistakes（5-10 条），不跨 skill 共享教训
2. **Superpowers 没有 references/pitfalls/ 目录** — 教训内嵌，不外置
3. **Superpowers 的 SKILL.md 是"自包含"的** — 读一个 skill 就能执行，不需要额外查文件
4. **clsh-project 的膨胀根因** — 把本该分散到各 Phase 的教训全部堆到一个 Common Pitfalls 节

## 重构决策（2026-05-22 确认）

- **不拆分** — 保持单体 skill（clsh 的 Phase 是连续流程，拆分增加切换开销）
- **全部迁移** — 89 条 Pitfalls 去重后 65 条，分三类迁移
- **Methodology references** — 留在 references/methodology/（类比 Superpowers 的 docs/）
- **加 Scope 定义** — 明确"管什么/不管什么/膨胀阈值"
