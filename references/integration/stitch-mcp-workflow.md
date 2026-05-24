# Stitch MCP 集成工作流

## 概述

通过 MCP (Model Context Protocol) 调用 Google Stitch API 生成 UI 设计稿。适用于 Phase 3 设计发散阶段。

## 前置条件

- Node.js 18+
- Stitch API Key（stitch.withgoogle.com → Settings → API Key）
- 代理访问 `stitch.googleapis.com`（国内需要）

## 连接方式

### HTTP Transport（推荐）

```bash
# 安装 MCP server
npm install -g @_davideast/stitch-mcp

# 验证连接
curl -s --proxy http://192.168.0.41:7890 --max-time 10 -X POST https://stitch.googleapis.com/mcp \
  -H "X-Goog-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

### 注册到 Hermes（需重启网关）

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  stitch:
    url: https://stitch.googleapis.com/mcp
    headers:
      X-Goog-Api-Key: YOUR_API_KEY
    timeout: 300
```

**注意：** 需要代理才能访问。Hermes 的 mcp_servers 不支持 proxy 配置，可能需要系统级代理。

## 可用 MCP 工具

| 工具 | 用途 | 关键参数 |
|------|------|---------|
| `create_project` | 创建设计项目 | `title` |
| `list_projects` | 列出项目 | — |
| `get_project` | 获取项目详情 | `name` (格式: `projects/{id}`) |
| `generate_screen_from_text` | 生成 UI 设计 | `projectId`, `prompt`, `deviceType`, `modelId` |
| `list_screens` | 列出设计稿 | `projectId` |
| `get_screen` | 获取设计稿详情 | `name` (格式: `projects/{id}/screens/{id}`) |
| `edit_screens` | 编辑设计稿 | `projectId`, `prompt` |
| `generate_variants` | 生成变体 | `projectId`, `prompt` |
| `upload_design_md` | 上传设计系统 | `projectId`, `designMd` |
| `create_design_system` | 创建设计系统 | `projectId`, `theme` |

## Prompt 最佳实践（Stitch 官方指南）

### 高层 vs 细节
- 高层：`"An app for marathon runners."`
- 细节：`"An app for marathon runners to engage with a community, find partners, get training advice."`

### 用形容词定调性
- `"A vibrant and encouraging fitness tracking app."`
- `"A minimalist and focused app for meditation."`

### 逐屏迭代
- 一次改一两处，不要一次改太多
- 用 UI/UX 术语：`navigation bar`、`call-to-action button`、`card layout`
- 精确引用元素：`"primary button on sign-up form"`

### 控制主题
- 颜色：`"Change primary color to forest green."` 或 `"Update theme to a warm, inviting color palette."`
- 字体：`"Use a playful sans-serif font."` 或 `"Change headings to a serif font."`
- 按钮：`"Make all buttons have fully rounded corners."`

## 已知限制

1. **无截图下载 API** — 生成的设计只有 400×400 缩略图，无高清截图导出
2. **长 prompt 超时** — 通过代理的长 prompt 请求容易 60 秒超时（exit code 56）
3. **无 REST API 创建** — 创建功能只能通过 MCP，不能直接 REST 调用
4. **API Key 认证** — HTTP transport 用 `X-Goog-Api-Key` header，不用 env var

## 替代方案：本地渲染

当 Stitch API 不可用或超时时，用 Stitch 导出的设计系统 token 本地渲染 HTML：

1. 从 `get_project` 响应中提取 `designTheme` 和 `designMd`
2. 用 token 写 HTML/CSS
3. `chromium-browser --headless --screenshot` 截图

## 与 Open Design 配合

Open Design 的设计系统（`/opt/open-design/design-systems/`）提供 152 套 DESIGN.md + tokens.css，可直接用于本地渲染：

```bash
# 查看可用设计系统
ls /opt/open-design/design-systems/

# 推荐：glassmorphism（毛玻璃）、linear-app（极简深色）、vercel、shadcn
cat /opt/open-design/design-systems/glassmorphism/tokens.css
```
