# Superpowers v5 关键变更及对 clsh-project 的影响

> 来源：https://github.com/obra/superpowers RELEASE-NOTES.md
> 整理时间：2026-05-16

## v5.1.0 (2026-04-30) 关键变更

### 1. writing-plans — Self-Review 从 subagent 改为 inline

**变更：** 不再派 subagent 做 Spec Review，改为 agent 自身 inline 检查（更快：30s vs ~25s，且避免 subagent 启动开销）。

**对 clsh-project Phase 5 的影响：** 写 tasks.md 时需要做 3 项 inline self-review：
1. **Spec Coverage** — 逐条扫描 spec 需求，确认每个需求都有对应任务
2. **Placeholder Scan** — 搜索 TBD/TODO/vague/similar to N 模式
3. **Type Consistency** — 跨任务检查函数签名/类型/命名一致性

### 2. writing-plans — "No Placeholders" 规则强化

**明确列出的计划缺陷模式：**
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "handle edge cases"
- "Write tests for the above"（不含实际测试代码）
- "Similar to Task N"（重复代码，开发者可能跳读）
- 引用未定义的类型/函数/方法

### 3. requesting-code-review — 合并 persona + checklist 到 code-reviewer.md

**变更：** 不再使用独立的 code-reviewer named agent，改为 `Task(general-purpose)` + 模板。

**对 clsh-project Phase 6 的影响：** review 步骤改为：
```python
# 不再需要：Task(subagent="code-reviewer")
# 改为：dispatch delegate_task with general-purpose + code-reviewer.md 模板
```

### 4. requesting-code-review — 行为测试

**变更：** 植入 SQL 注入、明文密码、凭据日志等 bug，reviewer 必须全部捕获才通过。

**对 clsh-project Phase 6 的影响：** Security Scan 应包含相同的检测模式。

### 5. subagent-driven-development — 不再每 3 任务暂停

**变更：** 从"每 3 批次 review"改为"每任务或自然 checkpoint + 连续执行指令"。

**对 clsh-project Phase 6 的影响：** 确认 Phase 6 不需要人为的批次暂停，每 Task 一个 checkpoint 即可。

### 6. Design-for-isolation 指导增强

**变更：** brainstorming + writing-plans + sdd 都增加了文件边界和隔离设计指导。

**对 clsh-project 的影响：**
- Phase 5 写 tasks.md 时应包含文件依赖图
- 每个 Task 修改的文件尽量不重叠（重叠时标注依赖顺序）
- 文件设计原则：单一职责、清晰接口、可独立理解

### 7. Legacy slash commands 移除

**变更：** `/brainstorm`、`/execute-plan`、`/write-plan` 已移除。

**对 clsh-project 的影响：** 无影响（clsh-project 不依赖 superpowers slash commands）。

## 版本对照

| clsh-project 版本 | 兼容 Superpowers 版本 | 关键对应 |
|------------------|---------------------|---------|
| v2.3.0 | v4.x | 初始集成 |
| v2.4.0 | v5.1.0 | 本文件覆盖的变更 |
