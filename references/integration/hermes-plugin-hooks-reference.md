# Hermes 插件机制关键发现

> 来源：2026-05-18 MoviePilot MCP 插件项目调研

## pre_gateway_dispatch hook 能力边界

**源码确认**（`hermes_cli/plugins.py`）：
- `{"action": "skip", "reason": "..."}` → 丢弃消息，**不能回复用户**
- `{"action": "rewrite", "text": "..."}` → 替换 event.text，**继续走 LLM**（~50-100 token）
- `{"action": "allow"}` → 正常通过 LLM

**结论**：`skip` 可以丢弃消息但不能直接回复。`rewrite` 必须经 LLM 一圈。

## register_command 限制

- handler 签名：`fn(raw_args: str) -> str | None`
- **只对斜杠命令**（`/mp`）生效
- 纯数字消息（`"9 功夫足球"`）不是斜杠命令，不会被拦截

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
