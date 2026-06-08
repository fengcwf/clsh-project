# Fastify 请求对象参考

## 获取客户端 URL

### 正确方式

```javascript
// 获取完整 host:port（推荐，适用于反代/集成场景）
const host = req.headers.host;  // "192.168.0.254:8080" 或 "example.com"

// 构建 baseUrl
const baseUrl = `${req.protocol}://${req.headers.host || req.hostname}`;
// → "http://192.168.0.254:8080"
```

### 错误方式

```javascript
// ❌ req.server.config.port — 不存在
const port = req.server?.config?.port;  // undefined

// ❌ req.hostname — 只有 host，没有 port
const host = req.hostname;  // "192.168.0.254"（缺少 :8080）
```

## 适用场景

| 场景 | 推荐方式 | 原因 |
|------|---------|------|
| 生成分享链接 | `req.headers.host` | 需要正确的端口 |
| 回调 URL | `req.headers.host` | 反代场景端口可能不同 |
| 内部路由 | `req.hostname` | 不需要端口 |
| 日志记录 | `req.headers.host` | 完整信息 |

## 注意事项

- `req.headers.host` 在反代后面可能不含端口（只有域名）
- 如果需要默认端口（80/443），可以 fallback：
  ```javascript
  const host = req.headers.host || req.hostname;
  const baseUrl = `${req.protocol}://${host}`;
  ```
- 集成场景（旧服务合并到新服务）必须用 `req.headers.host`，不能依赖环境变量或配置文件
