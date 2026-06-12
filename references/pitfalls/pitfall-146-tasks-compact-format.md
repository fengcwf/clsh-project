# Pitfall #146: tasks.md 紧凑格式实战解法

## 问题
tasks.md ≤ 80 行限制。直觉是每个 Task 用 4-5 行（文件/功能/验收标准/不在范围内），但 16 个 Task × 5 行 = 80 行，加上标题、依赖图、Self-Review、Phase 4 确认节，实际超限。

**根因：** phase5-tasks.md 参考文件说"每个 Task 用 bullet-point 摘要（5-8 行）"，这与 80 行总限制矛盾。16 Task 项目的真实预算是 ~3 行/Task。

## 解法：Pipe 分隔单行格式

每个 Task 压缩为 **2 行**：标题行 + 详情行（pipe 分隔）。

```markdown
### T1: 项目脚手架 | 角色：coder | skills: test-driven-development, incremental-implementation
文件: /path/{a.ts,b.ts} | 功能: 一句话描述 | 验收标准: ✅ GIVEN...WHEN...THEN... | 不在范围内: 一句话
```

**行数预算（16 Task 项目）：**
| 内容 | 行数 |
|------|------|
| 标题 + Phase 4 确认 + 依赖图 | ~8 行 |
| 16 Tasks × 2 行 | 32 行 |
| Self-Review | 3 行 |
| **总计** | **~43 行**（余量 37 行） |

## 验证方法
写完后先 `wc -l tasks.md`，超过 75 行就开始压缩（留 5 行余量）。

## 反例
```
### Task 1: 项目脚手架 | 角色：coder | skills: test-driven-development, incremental-implementation
- 文件: /tmp/collaborative-editor/{package.json,tsconfig.json,docker-compose.yml,.env.example}
- 功能: monorepo 初始化，配置 TypeScript strict + ESLint + Prettier，Docker Compose 含 PostgreSQL + Redis
- 验收标准: ✅ GIVEN 项目目录 WHEN 运行 npm install + npm run build THEN 零错误
- 不在范围内: 不配置 CI/CD
```
= 5 行/Task → 16×5 + 8 + 3 = 91 行 → ❌ 超限

## 正例
```
### T1: 项目脚手架 | 角色：coder | skills: test-driven-development, incremental-implementation
文件: /tmp/collaborative-editor/{package.json,tsconfig.json,docker-compose.yml,.env.example} | 功能: monorepo初始化 TS strict+ESLint+Prettier Docker Compose(PG+Redis) | 验收标准: ✅ GIVEN npm install+build WHEN运行 THEN零错误; ✅ GIVEN docker-compose up -d THEN PG+Redis运行 | 不在范围内: 不配置CI/CD
```
= 2 行/Task → 16×2 + 8 + 3 = 43 行 → ✅

## 关键技巧
1. **去掉缩进 bullet（`-`）** — 直接写字段名+值
2. **合并字段到一行** — 用 ` | ` 分隔
3. **验收标准用分号分隔多条** — `; ✅` 而非换行
4. **功能描述去空格压缩** — "monorepo初始化" 而非 "monorepo 初始化"
5. **Task 编号用 T1-T16** — 而非 Task 1-Task 16（省字符）
6. **Phase 4 确认合并为 1 行** — 不用列表格式
