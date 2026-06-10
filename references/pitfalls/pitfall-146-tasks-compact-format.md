# Pitfall #146: tasks.md 紧凑格式（80 行限制实战解法）

## 日期
2026-06-10

## 问题
tasks.md 有 80 行硬限制（phase4-mechanical-check.py 检查）。但 16 个 Task 用多行 markdown 格式（每个 Task 6-8 行 + 标题/依赖图/Self-Review）会达到 120+ 行，超出限制。

## 根因
tasks.md 模板默认用多行 markdown（每个 Task 有 `### Task N:` 标题 + 4 个 bullet point），行数膨胀快。

## 实战解法：一行 pipe 分隔格式
每个 Task 压缩为一行，用 `|` 分隔：
```
### Task N: 标题 | 角色：coder | skills: test-driven-development, incremental-implementation
文件: path1, path2 | 功能: 一句话描述 | 验收标准: 可测量的验收条件 | 不在范围内: 不做什么
```

16 个 Task ≈ 60 行（含标题/依赖图/Self-Review），远低于 80 行限制。

## 注意
- "验收标准"和"不在范围内"必须保持完整（Pitfall #105）
- 代码片段不写在 tasks.md 中，Phase 6 派发时注入 kanban body
- 依赖图用 ASCII art 一行表示，不用多行缩进
