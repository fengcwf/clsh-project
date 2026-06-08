# MoviePilot API 集成笔记

> 2026-06-02 Phase 8 实测总结

## 认证方式（关键）

MoviePilot 有两套 API，认证方式不同：

| API 类型 | 端点前缀 | 认证方式 | 用途 |
|---------|---------|---------|------|
| REST API | `/api/v1/*` | Bearer token（登录获取） | 推荐、订阅、下载、系统管理 |
| MCP | `/api/v1/mcp/*` | X-API-KEY header | 搜索媒体、工具调用 |

### Bearer token 获取
```
POST /api/v1/login/access-token
Content-Type: application/x-www-form-urlencoded

username=admin&password=xxx
→ { access_token: "eyJ...", token_type: "bearer" }
```
Token 有效期 24h，建议缓存 23h 后自动刷新。

### X-API-KEY
直接在 header 中传：`X-API-KEY: <API_TOKEN>`
**注意：REST API 不接受 X-API-KEY，只接受 Bearer token。**

## 搜索：MCP vs REST

| 端点 | 返回内容 | 适用场景 |
|------|---------|---------|
| MCP `search_media` | TMDB 媒体信息（title, poster, overview, tmdb_id） | UI 搜索、浏览 |
| REST `/api/v1/search/title` | 种子资源（meta_info, torrent_info） | 种子搜索、下载 |

**UI 搜索必须用 MCP `search_media`，不用 REST search/title。**

MCP 返回格式：`{success: true, result: "JSON string"}` — 需要 `JSON.parse(result)`。

## 订阅 API 字段映射

MCP 搜索返回 `type: "movie"`（英文），REST 推荐返回 `type: "电影"`（中文）。
订阅 API `/api/v1/subscribe/` 期望中文类型。

```javascript
const typeMap = { movie: '电影', tv: '电视剧', '电影': '电影', '电视剧': '电视剧' };
```

订阅数据字段：
- `type`: "电影" | "电视剧"
- `total_episode` / `lack_episode` / `completed_episode`: 进度
- `description`: 简介
- `poster`: 海报 URL
- `vote`: 评分
- `state`: 状态（R=运行中）

## 网络注意事项

Node.js `fetch()`（undici）在某些局域网环境下因 HTTP/2 协议协商挂起。
**解决方案：用 `node:http` 的 `request()` 替代 `fetch()`。**

```javascript
import http from 'node:http';

function httpRequest(method, urlStr, headers, bodyStr) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlStr);
    const req = http.request({
      hostname: url.hostname,
      port: url.port || 80,
      path: url.pathname + url.search,
      method, headers, timeout: 15000,
    }, (res) => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        let parsed;
        try { parsed = JSON.parse(data); } catch { parsed = data; }
        resolve({ status: res.statusCode, body: parsed });
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    if (bodyStr) req.write(bodyStr);
    req.end();
  });
}
```

## MCP 工具列表（70 个，常用）

| 工具 | 说明 |
|------|------|
| `search_media` | TMDB 媒体搜索 |
| `search_person` | 演员/导演搜索 |
| `search_person_credits` | 演员作品列表 |
| `query_media_detail` | TMDB 媒体详情 |
| `add_subscribe` | 新增订阅 |
| `query_subscribes` | 查询订阅列表 |
| `delete_subscribe` | 删除订阅 |
| `search_torrents` | 种子搜索 |
| `get_search_results` | 获取搜索结果 |
| `add_download` | 添加下载 |
| `query_download_tasks` | 查询下载任务 |
| `query_episode_schedule` | 剧集播出日历 |
| `query_library_exists` | 检查媒体库 |
| `get_recommendations` | 推荐 |
| `query_sites` | 站点管理 |
| `query_installed_plugins` | 插件列表 |
