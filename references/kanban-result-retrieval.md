# Kanban Worker 结果检索

当 kanban worker 只写了 summary（被截断）而没有完整文件时，通过 SQL 查询 DB 获取完整结果。

## 方法 1: 读 kanban comment

```bash
# 找到评论
sqlite3 ~/.hermes/kanban.db \
  "SELECT body FROM task_comments WHERE task_id = '<id>' ORDER BY created_at DESC LIMIT 1;"

# 批量导出
for id in t_xxx t_yyy t_zzz; do
  echo "=== $id ===" >> /tmp/kanban-results.md
  sqlite3 ~/.hermes/kanban.db \
    "SELECT body FROM task_comments WHERE task_id = '$id' ORDER BY created_at DESC LIMIT 1;" \
    >> /tmp/kanban-results.md
done
```

## 方法 2: 读 kanban log

```bash
# 从 worker 输出中提取完成报告
hermes kanban log <id> | grep -A500 "CRITICAL" | head -100
```

log 中的完整报告在 terminal 输出块之后，格式为：
```
╭─ ⚕ Hermes ───────────────────╮
    [完成报告内容]
╰────────────────────────────────╯
```

## 方法 3: 读 kanban show summary

```bash
# 从 events 中提取 completed 事件的 summary
hermes kanban show <id> 2>&1 | grep "completed" | head -1
```

summary 通常在 200 字符左右，被截断时只有部分信息。

## 方法 4: 查询所有 task events

```bash
# 从 DB 直接查
sqlite3 ~/.hermes/kanban.db \
  "SELECT task_id, kind, json_extract(payload, '$.summary') as summary 
   FROM task_events 
   WHERE task_id IN ('t_xxx','t_yyy') AND kind='completed'
   ORDER BY created_at DESC;"
```

## 预防

在 kanban 卡 body 中明确要求文件产出：
```
**产出**: 将完整报告写入 /tmp/workspace-review-{task_id}.md
```

这样即使 kanban summary 被截断，也能从文件中恢复完整结果。
