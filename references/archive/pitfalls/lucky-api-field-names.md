# Lucky API 字段名陷阱（2026-06-05）

## 问题
Lucky API 各端点返回的 JSON 结构不统一，字段名容易猜错。

## 实际返回结构

| 端点 | 返回格式 | 注意事项 |
|------|---------|---------|
| `/api/webservice/rules` | `{ret:0, ruleList:[...]}` | 字段名是 `ruleList` 不是 `rules` |
| `/api/ssl` | `{list:[...]}` | **无 `ret` 字段**，直接取 `list` |
| `/api/ddnstasklist` | `{ret:0, data:[...]}` | 字段名是 `data` 不是 `tasks` |

## 前端解析

- Lucky 卡片应检测 `ret === -1`（token 失效），显示配置提示而非空白
- `arr()` helper 需兼容 `{data: [...]}` 和嵌套结构两种格式

## 教训

第一次接入 Lucky API 时，必须先 `curl` 看实际返回结构，不能假设字段名。整个 session 因字段名不匹配导致 Lucky 卡片空白了很长时间。
