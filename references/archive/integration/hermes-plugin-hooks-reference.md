# Hermes 插件机制关键发现

> 来源：2026-05-18 MoviePilot MCP 插件项目调研 + 2026-05-31 插件迁移更新

## pre_gateway_dispatch hook 能力边界

**源码确认**（`hermes_cli/plugins.py`）：
- `{"action": "skip", "reason": "..."}` → 丢弃消息，**不能回复用户**
- `{"action": "rewrite", "text": "..."}` → 替换 event.text，**继续走 LLM**（~50-100 token）
- `{"action": "allow"}` → 正常通过 LLM

**结论**：`skip` 可以丢弃消息但不能直接回复。`rewrite` 必须经 LLM 一圈。

## register_command 机制

- handler 签名：`fn(raw_args: str) -> str | None`
- **只对斜杠命令**（`/mp`）生效
- 纯数字消息（`"9 功夫足球"`）不是斜杠命令，不会被拦截
- 返回 `str` → 直接回复用户，**零 token**
- 返回 `None` → fallback 到 LLM 流程

### provides_hooks 字段

`plugin.yaml` 的 `provides_hooks` 字段应该只列出实际的 hook 名称，**不要包含 `register_command`**：

```yaml
# ✅ 正确：只列出实际 hook
provides_hooks:
  - pre_gateway_dispatch
  - pre_llm_call

# ❌ 错误：register_command 不是 hook
provides_hooks:
  - register_command  # ← 这不是 hook，是方法
```

`register_command` 是在 `register(ctx)` 函数中调用的方法，不是 hook。`provides_hooks` 只是元数据声明，不影响功能，但保持规范很重要。

### Gateway 命令分发顺序

源码确认（`gateway/run.py` ~7887 行）：

1. 内置命令（`/new`, `/quit`, `/help` 等）
2. Quick commands（`/command` 快捷命令）
3. **Plugin-registered commands**（`get_plugin_command_handler()`）
4. Skill slash commands（`/skill-name`）
5. 未识别命令 → "Unrecognized slash command" 警告

插件命令优先级高于 skill 命令。

## 零 token 路径总结

| 路径 | Token 消耗 | 适用场景 |
|------|-----------|---------|
| `register_command` handler | **零 token** | 仅斜杠命令 `/mp` |
| `pre_gateway_dispatch` + `skip` | **零 token** | 丢弃消息，不能回复 |
| `pre_gateway_dispatch` + `rewrite` | **~50-100 token** | 替换文本后经 LLM 复读 |
| `ctx.llm.complete()` | **正常 token** | 插件内部 LLM 调用 |

## 参考

- Hermes 插件文档：https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
- Hermes Hooks 文档：https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks
- 源码：`hermes_cli/plugins.py` — `VALID_HOOKS`、`PluginContext`
- 源码：`gateway/run.py` — L7887 插件命令分发
