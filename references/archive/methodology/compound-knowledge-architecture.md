# 复利知识架构 — CE 借鉴分析

> 来源：2026-06-02 对 [Compound Engineering Plugin](https://github.com/EveryInc/compound-engineering-plugin) 的深度调研。

## 核心问题

**记录不是瓶颈，注入才是。** 写在 wiki 里的 solutions 如果没有在正确时间注入到正确项目，等于不存在。

## CE 的 Compound 机制

CE 的 `/ce-compound` 解决方案：
- **双轨分类**：Bug Track（问题→症状→无效尝试→方案→预防）vs Knowledge Track（上下文→指南→何时用→示例）
- **并行子 agent**：Context Analyzer + Solution Extractor + Related Docs Finder
- **重叠检测**：5 维度打分（问题/根因/方案/文件/预防规则），High→合并，Low→新建
- **Discoverability Check**：确保 AGENTS.md 指向 solutions/ 目录
- **`/ce-compound-refresh`**：定期审计（Keep/Update/Consolidate/Replace/Delete）

## clsh-project 的正确架构

### 不该做：raw/projects/<项目>/solutions/

这只是项目私有存档，llm-wiki ingest 不会碰，其他项目也不会扫。

### 该做：raw → wiki ingest 管道

```
raw/projects/<项目>/              ← 修复时随手记（30秒，原始素材）
  ├── 2026-06-01-fetch-cookie.md
  └── 2026-06-01-get-handler.md
     ↓ ingest pipeline (LLM 分类 + 打标签)
wiki/solutions/                   ← 结构化，可检索，跨项目
  ├── fetch-credentials-fastify.md
  ├── css-backdrop-filter-containing-block.md
  └── INDEX.md
     ↓ Phase 0 读取
新项目启动 → 自动注入匹配的历史方案
```

### Tagging 机制（wiki SCHEMA.md taxonomy 新增）

```yaml
# 解决方案标签
- domain: frontend | backend | devops | database | auth | ui
- tech: vue | fastify | css | node | python | shell
- error-type: timeout | auth-failure | rendering | data-loss | race-condition
- severity: critical | high | medium | low
- reusability: cross-project | project-specific | one-time
```

**`reusability` 决定注入范围：**
- `cross-project`：任何项目可能踩（如 CSS containing block）→ Phase 0 自动注入
- `project-specific`：仅本项目（如 MoviePilot 特定 API）→ 不跨项目注入
- `one-time`：一次性问题 → 不注入

### 三个注入时机

| 时机 | 注入什么 | 怎么注入 |
|------|---------|---------|
| Phase 0 | 匹配当前 domain/tech 的 cross-project solutions | 读 wiki/solutions/INDEX.md + search_files |
| Phase 6 task body | 与当前 task 标签匹配的历史教训 | kanban 卡 body 注入「历史教训」字段 |
| Phase 7 compound | 本轮修复的非平凡问题 | 写 raw/projects/ → 触发 ingest |

### 跨项目复利的前置条件

1. **Tagging 必须准确** — ingest 时 LLM 分类，人工不干预
2. **reusability 标签必须有** — 否则 Phase 0 注入全是噪音
3. **solutions 必须有 INDEX.md** — llm-wiki 自动维护
4. **先积累再启动** — 至少 5-10 个 raw solutions 后再开 ingest，否则 LLM 分类样本不足

## CE 其他值得借鉴的机制（暂不落地）

### ce-optimize（量化迭代优化）
metric-driven 迭代循环：定义指标 → 建基线 → 并行实验 → 评分 → 保留改进。当前 clsh-project 只有 bug-driven Phase 8，没有 metric-driven 优化。使用频率低，暂不做。

### ce-product-pulse（产品健康报告）
read-only 查询 analytics/tracing/payments，生成 30-40 行 pulse report。需数据源，暂不做。

### ce-debug causal chain gate
Phase 2 强制因果链完整性门禁 + assumption audit + 预测机制。比 diagnose-6 更严格。可考虑在 Phase 8 bugfix-spec 新增「因果链」字段。

### Multi-Agent Review（20+ 专业审查 agent）
拆 3 个核心 persona（security/performance/architecture）即可覆盖 80% 场景。Phase 6 已通过显式加载 requesting-code-review + code-principles 部分解决。
