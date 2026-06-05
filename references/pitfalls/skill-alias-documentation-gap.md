# Pitfall: Skill 别名文档与实现脱节 [已解决]

**日期：** 2026-06-05
**严重性：** 中
**状态：** ✅ 已解决（v7.0.0 — 2026-06-05）

## 问题描述

~~clsh-project 的 SKILL.md 和多个 references 文档中建议使用 `/cp` 作为 `/clsh-project` 的快捷别名。但 `/cp` **从未被技术实现** — skill_commands.py 只根据 SKILL.md frontmatter 的 `name` 字段注册命令，没有别名机制。~~

## 解决方案（已落地）

在 `agent/skill_commands.py` 中实现了 `aliases` frontmatter 字段支持：

1. `scan_skill_commands()` 读取 SKILL.md frontmatter `aliases` 列表，规范化后存入 `_skill_commands[key]["aliases"]`
2. `resolve_skill_command_key()` 先查直接匹配，再遍历所有 skill 的 aliases 列表
3. SKILL.md 中声明 `aliases: [cp]` 即可让 `/cp` 路由到 `/clsh-project`

```yaml
---
name: clsh-project
aliases: [cp]
---
```

**验证：** `resolve_skill_command_key("cp")` → `/clsh-project` ✅

## 相关文件

- `/root/.hermes/hermes-agent/agent/skill_commands.py` — `scan_skill_commands()` 解析 `aliases` + `resolve_skill_command_key()` 检查别名
- SKILL.md frontmatter — `aliases: [短名]` 声明
- `references/integration/slash-command-architecture.md` — 完整路由分析（含 aliases 机制）
