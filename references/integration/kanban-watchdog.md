# Kanban Watchdog — 按需监控机制

## 概述

Kanban Watchdog 是一个**按需启用**的 cron 监控，只在有 `in_progress` 状态的 kanban 任务时运行，全部完成后自动暂停。

## 机制

```
派活（kanban create + assignee）→ 启用 watchdog cron
  ↓
watchdog 每 5 分钟轮询 in_progress 任务
  ↓
发现任务完成 → 输出摘要（cron 自动发送到当前 chat）
  ↓
所有任务完成 → watchdog 自动暂停自身
```

## 脚本

- 路径：`~/.hermes/scripts/kanban-watchdog.py`
- 行为：
  - 有 in_progress 任务 + 有新完成 → 输出摘要
  - 有 in_progress 任务 + 无新完成 → 静默
  - 无 in_progress 任务 → 暂停自身 + 静默
- 状态文件：`~/.hermes/scripts/.kanban-watchdog-state`（记录上次检查时间）

## Cron 配置

- 名称：`kanban-watchdog`
- Job ID：`1d04104d3ca9`
- 调度：`every 5m`
- 模式：`no_agent=true`（脚本直接输出，不走 LLM）
- 投递：`origin`（发送到触发 chat）

## 工作流集成（Phase 6）

### 派活时

```bash
# 1. 派活
hermes kanban create "..." --assignee coder --json

# 2. 启用 watchdog
hermes cronjob resume 1d04104d3ca9
```

### 收尾时

watchdog 检测到所有任务完成后自动暂停，无需手动操作。

## 与其他 cron 的关系

| Cron | 用途 | 触发方式 |
|------|------|---------|
| kanban-watchdog | 监控任务完成通知 | 派活时启用，完成后自动暂停 |
| kanban → raw 归档 | 归档已完成任务到 Obsidian | 每小时自动 |
| channel-health-check | 渠道健康检查 | 每 30 分钟自动 |

## 注意事项

- watchdog 不替代 `notify-subscribe`（用户通知），两者并行
- watchdog 通知发送到发起派活的 chat，不是全局广播
