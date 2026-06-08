# Hermes 插件零令牌路由 — 研究笔记

> 来源：MoviePilot MCP 插件化项目调研（2026-05-17）
> 关键词：pre_gateway_dispatch, register_command, 零 token, 斜杠命令, 菜单状态

## 核心发现

### pre_gateway_dispatch 的能力边界

`pre_gateway_dispatch` hook 只支持三种 action：

| Action | 效果 | 能回复用户？ |
|--------|------|-------------|
| `{"action": "skip"}` | 丢弃消息，不经过 LLM | ❌ 静默丢弃 |
| `{"action": "rewrite", "text": "..."}` | 替换 event.text，继续走 LLM | ✅ 但消耗 token |
| `{"action": "allow"}` / `None` | 正常走 LLM | ✅ 正常消耗 |

**结论：`skip` 不能直接回复用户。** 插件没有"拦截命令 + 直接回复"的能力。

### register_command 才是零令牌路径

`ctx.register_command(name, handler, description="", args_hint="")` 注册的命令：

- **触发条件**：用户输入以 `/命令名` 开头
- **handler 签名**：`fn(raw_args: str) -> str | None`
- **返回值**：直接作为回复发给用户，**完全不经过 LLM**
- **raw_args**：命令名后面的完整字符串（含参数）

**这是实现零 token 斜杠命令的唯一方式。**

### 纯文本消息的局限

用户直接回复 `1 黑客帝国`（不带 `/mp` 前缀）**不会触发** `register_command` 的 handler。
只能通过 `pre_gateway_dispatch` 拦截，但 `skip` 不能回复，只能 `rewrite` 后走 LLM（极低 token，不为零）。

## 推荐架构：双层路由

```
用户输入
  ├─ /mp ... 前缀 → register_command handler（零 token）
  │   ├─ 精确匹配命令 → 直接调 MCP → 返回结果
  │   └─ 匹配不上 → 返回 None → fallback LLM
  └─ 纯文本（如 "1 黑客帝国"）→ pre_gateway_dispatch hook
      ├─ 60s 内有菜单状态 → rewrite 为 MCP 调用指令 → LLM 执行（极低 token）
      └─ 无菜单状态 → 正常 LLM 意图识别
```

## 菜单状态管理

```python
_menu_state: dict[str, float] = {}  # {session_key: expires_timestamp}
MENU_TIMEOUT = 60  # 秒

def is_menu_active(session_key: str) -> bool:
    expires = _menu_state.get(session_key, 0)
    if expires > time.time():
        return True
    _menu_state.pop(session_key, None)
    return False

def activate_menu(session_key: str):
    _menu_state[session_key] = time.time() + MENU_TIMEOUT
```

## 命令匹配逻辑（register_command handler 内）

```python
def mp_handler(raw_args: str) -> str | None:
    content = raw_args.strip()
    if not content:
        activate_menu(get_session_key())
        return MENU_TEXT
    parts = content.split(None, 1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    if cmd in MENU_INDEX:
        return execute_mcp(MENU_INDEX[cmd], args)
    if cmd in MENU_ALIAS:
        return execute_mcp(MENU_ALIAS[cmd], args)
    return None  # fallback to LLM
```

## 与 mp-menu 插件的关系

现有 mp-menu 插件使用 `pre_gateway_dispatch` + `rewrite` 路径，所有消息都经过 LLM。
新方案：
1. 保留 mp-menu 的菜单定义（MENU_ITEMS、别名表）
2. 核心路由迁移到 `register_command`
3. `pre_gateway_dispatch` 仅用于纯文本菜单选项 fallback

## 参考

- Hermes 源码：`hermes_cli/plugins.py` — PluginContext.register_command()
- Hermes 源码：`gateway/run.py` — 内置斜杠命令拦截逻辑
- Hermes 文档：`docs/developer-guide/gateway-internals`
- Hermes 文档：`docs/user-guide/features/plugins`
- Hermes 文档：`docs/user-guide/features/hooks`
- MoviePilot 源码：`skills/command-dispatch/SKILL.md`
