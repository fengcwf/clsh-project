# lark-cli 飞书消息桥接（Card-First 架构）

> 2026-06-09 建立，2026-06-09 升级为 Card-First。
> 解决飞书消息 markdown 渲染质量问题：表格/代码块/标题/列表全部原生渲染。

## 架构演进

| 阶段 | 方案 | 触发条件 | 渲染效果 |
|------|------|---------|---------|
| v1 (已弃用) | lark-cli `--markdown` | 检测到 markdown 特征 | post+md 格式，表格原生但标题被重写 |
| **v2 (当前)** | **Card JSON 2.0** | **所有非短消息** | **交互式卡片，表格/标题/代码块全部原生** |

## 当前架构：Card-First

**核心原则：** 飞书渠道的所有结构化内容默认以交互式卡片（Card JSON 2.0）发送。

### 发送流程

```
feishu.py send()
  → should_use_card(content)?
    → YES → send_as_interactive_card()  ← 主通道
              ↓ 失败
            try_send_via_lark_cli()      ← 降级
              ↓ 失败
            原生 post/text               ← 兜底
    → NO  → 原生 post/text（短消息/纯 emoji）
```

### 文件位置

| 文件 | 作用 |
|------|------|
| `gateway/platforms/lark_cli_bridge.py` | 桥接模块：card 转换 + lark-cli 封装 |
| `gateway/platforms/feishu.py` | 切入点：send() 方法中的路由逻辑 |

## Card JSON 2.0 要点

### 支持的元素标签

| 标签 | 用途 | 备注 |
|------|------|------|
| `markdown` | 正文内容 | 支持加粗/列表/代码/链接 |
| `table` | 表格组件 | 原生渲染，带分页 |
| `hr` | 分割线 | **⚠️ 不是 `divider`！** |
| `plain_text` | 标题文本 | header.title 专用 |

### ⚠️ 关键 Pitfalls（已验证，2026-06-09 实测）

1. **`divider` 标签不存在** — 用 `hr` 替代。`divider` 返回 `not support tag: divider`（code 230099）。✅ 已验证。
2. **`config.update_multi` 必须为 true** — 否则流式卡片 PATCH 更新会静默失败。
3. **中文消息阈值 ~30 字符** — 中文信息密度高，30 字符已是完整句子。`should_use_card()` 默认阈值 30。
4. **表格用 dict rows** — Card 2.0 table 组件 rows 是 `[{col_name: value}]` 格式，不是数组。✅ 已验证。
5. **lark-cli 路径** — venv 内 npm 包路径：`venv/lib/python3.11/site-packages/nodejs_wheel/lib/node_modules/@larksuite/cli/bin/lark-cli`
6. **确认码卡片中码必须独占一行** — 用户反馈：码周围有 emoji/文字时不方便复制（容易选中附近内容）。✅ 用户纠正。

### 卡片颜色自动映射

```python
_COLOR_MAP = {
    "phase1": "turquoise",   # 需求澄清
    "phase2": "blue",        # 方案设计
    "phase3": "purple",      # 设计文档
    "phase4": "orange",      # 自检
    "phase5": "indigo",      # 实现计划
    "phase6": "green",       # 执行
    "phase7": "wathet",      # 归档
    "phase8": "red",         # 反馈循环
    "success": "green",
    "error": "red",
    "warning": "orange",
}
```

## lark-cli 命令参考

```bash
# 发送交互式卡片
lark-cli im +messages-send \
  --chat-id "oc_xxx" \
  --msg-type interactive \
  --content '{"schema":"2.0","header":{...},"body":{...}}' \
  --as bot --format json

# PATCH 更新卡片（流式）
lark-cli api PATCH /open-apis/im/v1/messages/{message_id} \
  --data '{"content":"{\"schema\":\"2.0\",...}"}'

# 上传图片
lark-cli im +messages-send --chat-id "oc_xxx" --image /path/to/img.png --as bot

# 上传文件
lark-cli im +messages-send --chat-id "oc_xxx" --file /path/to/file --as bot
```

## 飞书消息格式限制（更新）

| 格式 | 表格 | 加粗/列表/代码 | 标题 | 上限 |
|------|------|-------------|------|------|
| `text` | ❌ | ❌ | ❌ | 150KB |
| `post + tag: md` | ❌ | ✅ | ❌（重写为 `####`） | 30KB |
| **`interactive` (Card 2.0)** | **✅ 原生 table** | **✅ markdown 元素** | **✅ bold** | **30KB** |

## 微信渠道对比

微信不支持交互式卡片，保持纯文本发送。确认码模板等跨渠道内容格式不变，gateway 层自动处理渲染差异。
