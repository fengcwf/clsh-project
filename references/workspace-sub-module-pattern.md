# Workspace 子模块开发模式

> 2026-05-27 总结 — 从 cron-monitor 增强项目提炼

## 前置检查（必须）

1. **读 `AGENTS.md`** — 确认目录结构、命名规范、路由前缀规范
2. **读 `config/projects.json`** — 确认项目注册格式
3. **读现有子模块** — `src/projects/obsidian/` 是参考模板

## 文件结构（与 obsidian 对齐）

```
src/projects/<id>/
├── plugin.mjs          ← Fastify 路由注册 + API 实现
└── public/
    └── <ViewName>.mjs  ← Vue3 CDN 前端组件
```

**反模式：**
- ❌ 把前端放在 `src/public/views/`（与后端分离，不利于模块内聚）
- ❌ 把路由放在 `src/api/`（应放在 `plugin.mjs` 中）

## Fastify 双静态根配置

当需要同时服务 `src/public/`（主前端）和 `src/projects/*/public/`（子模块前端）时：

```javascript
// ❌ 错误：root 数组会 double-prefix
await fastify.register(fastifyStatic, {
  root: [join(__dirname, 'public'), join(__dirname, 'projects')],
  prefix: '/',
});

// ✅ 正确：两次注册，第二次不装饰 reply
await fastify.register(fastifyStatic, {
  root: join(__dirname, 'public'),
  prefix: '/',
  decorateReply: true,
  wildcard: true,
});
await fastify.register(fastifyStatic, {
  root: join(__dirname, 'projects'),
  prefix: '/projects/',
  decorateReply: false,
});
```

**关键：** `decorateReply: false` 防止重复装饰 Fastify reply 对象。

## 前端 import 路径

```javascript
// app.mjs 中导入子模块前端
import CronMonitorView from '../projects/cron/public/CronMonitor.mjs';
```

浏览器会请求 `/projects/cron/public/CronMonitor.mjs`，由第二个静态根处理。

## Hermes CLI 非交互式用法

```bash
# 编辑调度
hermes cron edit <id> --schedule "*/30 * * * *"

# 创建（prompt 是位置参数，schedule 也是位置参数）
hermes cron create "*/5 * * * *" "任务描述" --name "名称" --deliver local

# 触发
hermes cron run <id>

# 暂停/恢复
hermes cron pause <id>
hermes cron resume <id>

# 删除
hermes cron remove <id>
```

## Cron 数据源

`~/.hermes/cron/jobs.json` 包含所有 cron 任务的完整定义：
- `id`, `name`, `schedule.expr`, `enabled`, `paused_at`
- `prompt`, `script`, `model`, `provider`, `skills`, `deliver`
- `repeat.completed`（执行次数）

## Phase 8 反馈循环模式（多点反馈）

当大佬一次提出 7+ 个反馈点时：
1. 逐条回应（不跳过任何一条）
2. 区分类型：分析（#3 废弃 cron）、修复（#2 文件结构）、新增（#6 #7）
3. 修复和新增可以并行执行（自己做修复，CodeWhale 做新增）
4. 删除操作优先（`hermes cron remove`），无依赖
