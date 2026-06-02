# Raw Fix 记录模板

> Phase 6/8 修复非平凡问题时随手记录。写入 `raw/projects/<项目名>/YYYY-MM-DD-<简述>.md`。
> 后续由 Phase 7 ingest 管道编译为 `wiki/solutions/` 结构化方案。

## 使用场景

- Phase 6 Task 完成后微蒸馏发现问题 → 记录
- Phase 8 Bug 修复完成后 → 记录
- 只有**非平凡修复**才记录（不是 typo/配置错误）

## 模板

```markdown
---
project: <项目名>
date: YYYY-MM-DD
phase: 6 | 8
task: <Task 名称或 bug 描述>
tech: [vue, fastify, css, ...]          # 灵犀填写，ingest 时 LLM 补充
domain: frontend | backend | devops | auth | ui | database
---

## 问题现象
<1-2 句话描述大佬反馈或发现的问题>

## 根因
<如果已知，写根因。不知道就写"待分析">

## 修复方案
<改了什么、为什么这样改>

## 关键代码/配置
<涉及的文件路径、关键行号、代码片段（可选）>

## 预防措施
<如何避免再次发生（可选）>
```

## 示例

```markdown
---
project: moviepilot
date: 2026-06-01
phase: 8
task: fetch API 调用同域 Fastify 不带 cookie
tech: [vue, fastify]
domain: auth
---

## 问题现象
token 自动登录成功设置了 session cookie，但后续 fetch API 请求不带 cookie → 401。

## 根因
默认 fetch 的 credentials 是 same-origin，但某些场景下（跨子路径）仍不自动发送 cookie。

## 修复方案
apiGet/apiPost helper 加 `credentials: 'include'`。

## 关键代码/配置
- /opt/Workspace/src/projects/moviepilot/public/MovieView.mjs（apiGet 函数）

## 预防措施
新建 Workspace 子模块时，检查所有 fetch 调用是否带 credentials。
```

## 写入规则

1. **路径**：`raw/projects/<项目名>/YYYY-MM-DD-<简述>.md`
2. **命名**：日期 + 简短描述（英文 kebab-case），如 `2026-06-01-fetch-cookie-missing.md`
3. **时机**：Phase 6 checkpoint 后 / Phase 8 单个 bug 修复后
4. **谁写**：灵犀（不是 worker）
5. **内容**：只记录根因和方案，不需要完整代码（ingest 时 LLM 会补充）
