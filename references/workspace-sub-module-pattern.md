# 内容管理子模块模式 — clsh-content → Workspace 集成案例

> 2026-05-28 — 从 clsh-content Workspace 集成提炼

## 场景

将已有的 Hermes 插件（clsh-content，含多个 Node.js 脚本）集成为 Workspace 子模块。

## 架构

```
src/projects/content/
├── plugin.mjs              ← Fastify 路由（776 行，9 个 API）
├── api/
│   ├── articles.mjs        ← 文章 CRUD（扫描 raw/articles/）
│   ├── channels.mjs        ← 渠道状态 + 历史
│   └── overview.mjs        ← KPI + 活动时间线
├── services/
│   ├── article-scanner.mjs ← 目录扫描 + frontmatter 解析
│   ├── channel-checker.mjs ← 渠道健康检查
│   └── script-runner.mjs   ← subprocess 调用封装
├── public/
│   └── ContentView.mjs     ← Vue3 前端（785 行，3 个 Tab）
└── README.md
```

## 关键设计决策

### 1. 脚本集成方式

不重写已有脚本，通过 `child_process.execFile` 调用：
- `halo-publish.cjs` → Halo 发布
- `wechat-publish.cjs` → 微信发布
- `xhs-publish.cjs` → 小红书发布
- `channel_check.py` → 渠道健康检查

设置 `NODE_PATH` 让脚本找到同目录的 node_modules。

### 2. 文件系统数据源

数据来自 `/mnt/unraid_data/Obsidian/raw/articles/`（drafts/published/materials）。
手动解析 YAML frontmatter（零依赖），提取 title/tags/status/date。

### 3. 三 Tab 结构

| Tab | 内容 |
|-----|------|
| 概览 | KPI 卡片 + 渠道健康 + 快捷操作 + 活动时间线 |
| 文章管理 | 左侧文件夹树 + 右侧文章列表 + 发布/删除 |
| 渠道管理 | 渠道状态卡片 + 发布历史 + 连接测试 |

### 4. 渐进式交付（三 Wave）

| Wave | 内容 | 耗时 |
|------|------|------|
| Wave 1 | 基础架构 + Tab1 概览 | ~160s |
| Wave 2 | Tab2 文章管理 API + 前端 | ~240s |
| Wave 3 | Tab3 渠道管理 | ~600s（超时但代码已写入） |

## API 端点清单

```
GET    /api/content/overview                              → KPI 数据
POST   /api/content/trigger/:type                         → 触发巡检
GET    /api/content/articles?folder=&status=&search=      → 文章列表
GET    /api/content/articles/:folder/:filename            → 文章详情
POST   /api/content/articles/:folder/:filename/publish    → 发布
DELETE /api/content/articles/:folder/:filename            → 删除（移至 .trash）
GET    /api/content/channels                              → 渠道状态
GET    /api/content/channels/:name/history                → 发布历史
POST   /api/content/channels/:name/test                   → 测试连接
```

## 注册步骤

1. 创建 `src/projects/content/plugin.mjs`
2. 更新 `config/projects.json`（添加 tabs 配置）
3. 更新 `server.mjs`（import + register）
4. 更新 `app.mjs`（import ContentView + 条件渲染）
5. 删除旧视图文件（如有 `src/public/views/ClshContent.mjs`）

## 教训

- CodeWhale ACP 处理 3+ 文件可能超时 600s，但代码通常在超时前已写入
- **CodeWhale 超时后文件可能损坏** — 69+ API 调用可能导致多次部分 patch，括号嵌套错乱。超时后先 `node -c` 检查，损坏则直接重写
- 文件系统 API 必须校验 `..` 路径遍历
- 迁移到子模块后必须删除旧位置的视图文件
- **Vue3 解构完整性** — 新组件默认 `const { ref, computed, watch, onMounted, onUnmounted, h, defineComponent } = Vue;`
- **execSync 阻塞事件循环** — Fastify handler 中禁止用 execSync，改用 execFile + await
- **数据源一致性** — 多个 API 检查同一数据时，共用同一个底层函数

## 外部 API 代理模式（MoviePilot 案例，2026-05-31）

当子模块需要代理外部 API（如 MoviePilot 192.168.0.71:3001）时：

### 认证方式探索

```bash
# 第一步：获取 OpenAPI spec
curl -s http://host:port/api/v1/openapi.json | python3 -c "
import sys,json; spec=json.load(sys.stdin)
for p in sorted(spec.get('paths',{})): print(f'  {p} [{\"|\".join(spec[\"paths\"][p])}]')
"

# 第二步：测试认证方式
curl -s -H "X-API-KEY: $KEY" http://host:port/api/v1/xxx  # API Key
curl -s -H "Authorization: Bearer $TOKEN" http://host:port/api/v1/xxx  # JWT
```

### 代理架构

```
前端 callTool() → POST /api/moviepilot/recommend
  → plugin.mjs proxyToMp()
  → GET http://192.168.0.71:3001/api/v1/recommend/tmdb_movies
  → Header: X-API-KEY: $MP_API_KEY
```

### 环境变量传递

pm2 进程读的是项目 `.env`（`/opt/Workspace/.env`），不是 shell 环境变量。
如果 API key 在 Hermes `.env` 中，需要手动复制到 Workspace `.env`。

### 教训

- 不要假设认证方式（JWT vs API Key vs session），先查 OpenAPI spec
- 不要假设端点路径（`/tools/call` vs `/mcp/tools/call` vs `/recommend`）
- 代理层处理认证，前端只调 Workspace API（session cookie 已够）
- **前端 fetch 必须加 `credentials: 'include'`** — 默认 `fetch` 的 `credentials` 是 `same-origin`，但在 Fastify session 认证场景下可能不自动发送 cookie。症状："API 通了但界面没有内容"。修复：`apiGet`/`apiPost`/`apiDelete` helper 的 fetch 调用必须带 `{ credentials: 'include' }`

## 内容管理子模块模式（2026-05-28）

将已有的 Hermes 插件（含 Node.js 脚本）集成为 Workspace 子模块的模式：

**架构：** `plugin.mjs`（路由）+ `public/ContentView.mjs`（前端），通过 `child_process` 调用已有脚本

**文章目录结构（文件夹=文章）：**
```
raw/articles/drafts/2026-05-28-主题/
├── article.md    ← 原始素材
├── halo.md       ← Halo 版
├── wechat.md     ← 微信版
├── xhs.md        ← 小红书版
├── covers/       ← 封面图
└── meta.json     ← 发布状态
```

**前端 Tab 模式：** `props: { activeTab }` 接收工作台 tab → 组件内用 `defineComponent` 拆分子 Tab

**渐进式交付：** 三 Wave（基础+Tab1 → Tab2 → Tab3），每 Wave 一个 CodeWhale ACP 任务

## 模板预览 API 模式（2026-06-06）

当子模块需要"预览不同渲染效果"时，采用 iframe + 后端渲染方案：

```
前端 iframe src → GET /api/<module>/:id/preview?theme=xxx
  → 后端读取内容 + 应用 CSS 主题 → 返回完整 HTML
  → iframe 隔离渲染，不污染宿主页面
```

**设计要点：**
- CSS 主题在后端管理（`THEME_CSS` 对象），前端只传 theme 参数
- iframe 天然隔离 CSS，且能模拟真实浏览器渲染
- 切换主题 = 更新 iframe src，无需刷新页面
- 优先读取渠道文件（`{channel}.md`），回退到源文件（`article.md`）

**适用场景：** 多渠道内容预览、主题切换、排版效果对比

详见 clsh-content skill 的 `references/workspace-preview-api.md`
