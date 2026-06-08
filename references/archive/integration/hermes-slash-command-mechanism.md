# Hermes 斜杠命令机制与插件化架构 — 调研笔记

> 来源：2026-05-17 MoviePilot MCP 插件化项目 Phase 1 调研
> 目的：搞清楚"零 token 命令路由"的技术可行性

## 核心发现

### 1. Hermes 内置斜杠命令的实现方式

- **硬编码在 gateway 源码中**（`GATEWAY_KNOWN_COMMANDS`），不是插件注册的
- 用户发 `/model`、`/stop`、`/new` 等命令时，Gateway 在 `_handle_message()` 中**直接拦截**
- **完全不经过 LLM 推理循环**，零 token 消耗
- 命令的回复由 gateway 直接发送给用户

### 2. 插件系统的能力边界

- 插件通过 `pre_gateway_dispatch` hook 可以返回三种 action：
  - `rewrite`：修改 event.text，继续走 LLM 流程（**仍消耗 token**）
  - `skip`：丢弃消息，不经过 LLM（**但插件无法直接回复用户**）
  - `allow`：正常通过
- `skip` 只是"吞掉"消息，**插件本身没有直接发消息回复用户的能力**
- `register_command()` API 在 2026-05 时**尚未实现**（见 issue #10495）

### 3. 实现"零 token 直接回复"的三种可能路径

| 方案 | 描述 | 可行性 |
|------|------|--------|
| **方案 A**：给 `skip` 增加 `reply` 字段 | 插件返回 `{"action": "skip", "reply": "结果文本"}` | 需要改 Hermes 源码 |
| **方案 B**：插件通过 gateway delivery 层直接发消息 | 插件调完 MCP 后直接调用 gateway 的消息发送接口 | 需要插件能访问 gateway 内部 API |
| **方案 C**：rewrite + LLM 做复读机 | 插件调完 MCP，把结果注入到 rewrite 文本中，LLM 原样输出 | token 消耗极低但不为零 |

### 4. MoviePilot 现有命令体系

- 17 个斜杠命令，分三类：`system`（内置）、`plugin`（插件注册）、`scheduler`（定时触发）
- 插件命令（`type: "plugin"`）需要 LLM 通过 `run_slash_command` 工具调用
- 系统命令（`type: "system"`）是内置的，但仍经过 LLM 推理循环

### 5. mp-menu 插件的教训

- 当前 mp-menu 使用 `pre_gateway_dispatch` hook，但所有路径都是 `rewrite`
- **所有路径仍经过 LLM 处理**，消耗 token
- 精确匹配的命令（如 `/mp 下载`）被 rewrite 为"调用 MCP 工具 xxx"，LLM 看到后再决定调工具
- 这不是真正的零 token，只是减少了 LLM 的"思考"负担

## 对 MoviePilot MCP 插件化项目的启示

1. **真正的零 token 需要插件能直接回复用户**，目前的 `skip` 做不到
2. **最可行的短期方案是方案 C**：插件在 `pre_gateway_dispatch` 中直接调 MCP 工具，把结果写入 rewrite 文本，LLM 只做复读机
3. **长期方案需要 Hermes 源码支持**：给 `skip` 增加 `reply` 字段，或实现 `register_command()` API
4. **分层设计**：精确匹配 → 零 token（方案 C）/ 匹配不上 → LLM 意图识别（正常 token）

## 参考链接

- [Hermes Agent v0.13 Reference](https://blakecrosley.com/guides/hermes)
- [Gateway Internals](https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-internals)
- [Plugins | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)
- [feat: implement register_command() on plugin context · Issue #10495](https://github.com/NousResearch/hermes-agent/issues/10495)
- [Add pre_gateway_text_send plugin hook for outbound · Issue #22603](https://github.com/NousResearch/hermes-agent/issues/22603)
