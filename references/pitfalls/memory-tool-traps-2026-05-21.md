# Memory 工具使用陷阱与容量管理（2026-05-21）

## 陷阱 1: memory 工具没有 probe 动作

**描述：** 尝试调用 `memory(action="probe", entity="xxx")` 时报错 `Unknown action 'probe'`。

**正确动作：**
- `memory(action="add", target="memory"|"user", content="...")` — 新增条目
- `memory(action="replace", target="memory"|"user", old_text="...", content="...")` — 替换条目
- `memory(action="remove", target="memory"|"user", old_text="...")` — 删除条目

**没有的动作：** `probe`、`list`、`search`、`get` 等。

**教训：** 不要凭印象猜 memory 的动作名。如果不确定，先试 `add`（最安全），或用 `session_search` 替代实体查询。

## 陷阱 2: Memory 容量上限 2200 字符

**描述：** memory 总容量 2200 字符。当占用率 >90% 时，新增/替换操作可能因超限失败。

**症状：** `Replacement would put memory at 2,380/2,200 chars.`

**解决方案（按优先级）：**
1. **先删除再添加** — 用 `remove` 删除过时条目，腾出空间后再 `replace` 或 `add`
2. **压缩内容** — 新条目写得更精简，只保留关键事实
3. **合并条目** — 将多个相关条目合并为一条

**预防规则：**
- 每次 session 开始时检查 memory 占用率（系统 prompt 显示 `MEMORY [XX%]`）
- 占用率 >85% 时，优先清理过时条目
- 项目完成后，将详细进度替换为精简摘要

## 陷阱 3: replace 的 old_text 必须精确匹配

**描述：** `replace` 的 `old_text` 参数必须是现有条目中的精确子串。

**解决方案：** 替换前先通过系统 prompt 中的 MEMORY 区块确认条目内容，确保 `old_text` 是精确子串。

## Memory vs Session Search 分工

| 工具 | 用途 | 容量 |
|------|------|------|
| `memory` | 持久化事实（用户偏好、环境、教训） | 2200 字符 |
| `session_search` | 搜索历史 session 内容 | 无限制 |
| `fact_store` | 全息记忆（实体解析、信任评分） | 独立存储 |

**规则：**
- 用户偏好、环境配置 → `memory`
- 项目进度、技术细节 → `session_search`（通过 wiki 文档索引）
- 实体关系、跨 session 事实 → `fact_store`
