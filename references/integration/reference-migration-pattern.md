# References 架构迁移模式（2026-05-21 验证）

## 问题

Skill 的 `references/` 目录随项目增长，混入了项目专属内容和流程知识。导致：
1. **跨项目耦合** — A 项目的陷阱文件存在 skill 里，B 项目执行时读不到
2. **过期粒度错误** — A 项目代码变更不触发 B 项目引用文档的过期检测
3. **没有项目级归属** — references 缺少 `projects` 字段标记属于哪些项目

## 分类决策树

```
对每个 reference 文件问：
│
├─ 它描述的是"怎么做"（方法论/流程）？
│   → 留在 skill/references/（本地）
│   例：methodology/, templates/, violation-case-*
│
├─ 它描述的是"用什么工具"（Hermes/Halo/Kanban 集成）？
│   → 留在 skill/references/integration/（本地）
│   例：hermes-plugin-*, halo-auth, kanban-tasks-bridge
│
├─ 它描述的是"某个项目的具体技术问题"？
│   → 迁移到 wiki/projects/<项目名>/references/
│   例：trap-case-2026-05-20-share-html（obsidian-workbench 专属）
│   例：halo-obsidian-ref（clsh-content 专属）
│
└─ 它被多个项目共享（如 GitHub 同步指南）？
    → 迁移到 wiki/reference/integration/（跨项目共享）
    例：github-sync-guide, lucky-api-format, php-env-pattern
```

## 迁移步骤

### 1. 盘点所有 references
```bash
find <skill>/references/ -type f -name "*.md" | sort
```

### 2. 按决策树分类
读每个文件前 10 行判断归属（标题通常说明用途）。

### 3. 创建目标目录
```bash
# 项目专属
mkdir -p wiki/projects/<项目名>/references/{integration,pitfalls}
# 跨项目共享
mkdir -p wiki/reference/integration
```

### 4. 复制文件到新位置
```python
import shutil
shutil.copy2(src, dst)  # 保留元数据
```

### 5. 创建 `.references-meta.json`
```json
{
  "description": "<项目名> 项目级 references 追踪",
  "last_audit": "YYYY-MM-DD",
  "references": {
    "relative/path/to/file.md": {
      "source": "clsh-project skill (migrated YYYY-MM-DD)",
      "projects": ["project-a", "project-b"],
      "last_verified": "YYYY-MM-DD",
      "staleness_threshold_days": 30,
      "status": "current"
    }
  }
}
```

**staleness_threshold_days 参考：**
- 7 天：API 格式、外部服务接口（变化快）
- 14 天：GitHub 同步指南、部署配置（偶尔变）
- 30 天：技术模式、认证方案（较稳定）
- 90 天：架构陷阱、CSS/前端模式（很少变）

### 6. 从 skill 目录删除已迁移文件
```bash
rm <skill>/references/<migrated-file>
```

### 7. 更新 SKILL.md
- frontmatter `references:` 列表：移除旧路径，按类别分组加注释
- 正文"参考文件"章节：新增架构说明表格 + 新路径
- Common Pitfalls 中引用旧路径的条目：更新为 wiki 路径
- 版本号 + 版本历史

### 8. 验证
```bash
# 确认迁移文件在新位置存在
ls -la wiki/projects/<项目名>/references/
# 确认 skill 目录不再有已迁移文件
find <skill>/references/ -name "<migrated-file>"
# 确认 SKILL.md 无残留旧路径（版本历史除外）
grep -n "old-path" <skill>/SKILL.md
```

## 过期检测逻辑（Phase 4 自检时）

```
执行项目 A 时：
  读 wiki/projects/A/.references-meta.json
  过滤 projects 包含 A 的条目
  检查 last_verified + staleness_threshold_days
  过期 → 标记需要重新验证
  不相关 → 跳过

全局 cron 审计：
  扫描所有 .references-meta.json
  按 last_expired 排序，报告最旧的 N 条
```

## 注意事项

- **版本历史中的旧路径保留原样** — 这是历史记录，不应修改
- **Common Pitfalls 中的路径必须更新** — 这是运行时读取的
- **迁移后推送 GitHub** — skill 和 wiki 都需要同步
- **不要迁移"概念性"内容** — methodology/ 里的分析文档与项目代码无关，留本地
