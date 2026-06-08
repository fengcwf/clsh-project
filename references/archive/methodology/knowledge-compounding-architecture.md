# Knowledge Compounding Architecture: raw → wiki/solutions

> 2026-06-02 建立。灵感来源：CE compound-engineering plugin。

## 核心问题

项目化管理中，修复记录只在当前项目内沉淀，新项目不会查其他项目的教训。需要一个机制让跨项目知识**自动注入**到正确的时间点。

## 架构

```
raw/projects/<项目>/YYYY-MM-DD-<简述>.md   ← Phase 6/8 修复时随手记录（30秒）
     ↓ Phase 7 ingest（LLM 分类 + 打标签）
wiki/solutions/<solution-slug>.md          ← 结构化方案（含 tags、cross-reference）
     ↓ Phase 0 匹配注入
新项目启动 → 自动获得历史教训（最多 5 条）
```

## Tagging 机制

SCHEMA.md 定义 solutions tag taxonomy：
- `domain`：frontend | backend | devops | auth | ui | database
- `tech`：vue | fastify | css | node | python | shell
- `error-type`：timeout | auth-failure | rendering | data-loss | race-condition
- `reusability`：cross-project | project-specific | one-time

**关键 tag：`reusability`**
- `cross-project`：任何项目可能踩的坑 → Phase 0 跨项目注入
- `project-specific`：仅本项目 → 存在 solutions/ 但不自动注入
- `one-time`：一次性问题 → 不编译，留在 raw/

## 注入时机

| 时机 | 做法 |
|------|------|
| Phase 0 启动 | 读 wiki/solutions/INDEX.md，按 tech/domain 匹配 cross-project 条目 |
| Phase 6 派活 | kanban task body 注入相关 solutions 摘要 |
| Phase 7 归档 | 触发 ingest：raw fix 记录 → wiki/solutions/ |

## 用户核心洞察

> "主要问题点不是记录，是如何注入。新项目不会主动查其他项目的知识复利。"

记录是手段，注入到正确时间点才是目的。跨项目复利需要 tagging 机制支撑，不能靠人工检索。

## CE 借鉴点

| CE 概念 | clsh-project 落地 |
|---------|-------------------|
| `/ce-compound` per-solution 文档 | wiki/solutions/ + raw fix 记录 |
| `/ce-compound-refresh` 知识库审计 | 待实现（Phase 7 可加） |
| `/ce-optimize` metric-driven 优化 | 未引入（使用频率低） |
| `/ce-product-pulse` 健康报告 | 未引入 |
| 20+ review agents | 3 核心 persona（security/performance/architecture） |
| causal chain gate | Phase 8 bugfix-spec 可加 |
| session history 集成 | Phase 0 已有隐式行为，不强制写入流程 |
