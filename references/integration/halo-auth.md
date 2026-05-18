# Halo CMS Session-Based Authentication

## 概述

Halo CMS 使用 session-based 认证（表单登录 + RSA 加密密码 + CSRF token），**不支持 Basic Auth**。

## 认证流程

```
1. GET /login → 提取 CSRF token + RSA 公钥 + XSRF-TOKEN cookie
2. 用 RSA 4096 加密密码（PKCS1 v1.5 填充）
3. POST /login → 提交加密后的密码 + CSRF token
4. 保存 SESSION cookie（有效期数小时到数天）
5. 后续 API 调用携带 SESSION cookie + X-XSRF-TOKEN header
```

## 关键代码（Node.js CommonJS）

```javascript
const http = require("http");
const crypto = require("crypto");

// 1. 获取登录页
function fetchLoginPage(baseUrl) {
  return new Promise((resolve, reject) => {
    http.get(`${baseUrl}/login`, (res) => {
      let data = "";
      res.on("data", chunk => data += chunk);
      res.on("end", () => {
        const csrfMatch = data.match(/name="_csrf" value="([^"]+)"/);
        const csrf = csrfMatch ? csrfMatch[1] : null;
        const keyMatch = data.match(/const publicKey = "([^"]+)"/);
        const publicKey = keyMatch ? keyMatch[1].replace(/\\\//g, "/") : null;
        const cookies = res.headers["set-cookie"] || [];
        const xsrfCookie = cookies.find(c => c.startsWith("XSRF-TOKEN="));
        const xsrfToken = xsrfCookie?.split(";")[0]?.split("=")[1];
        resolve({ csrf, publicKey, xsrfToken, cookies });
      });
    }).on("error", reject);
  });
}

// 2. RSA 加密密码
function encryptPassword(password, publicKeyBase64) {
  const pemKey = `-----BEGIN PUBLIC KEY-----\n${publicKeyBase64}\n-----END PUBLIC KEY-----`;
  const buffer = Buffer.from(password, "utf8");
  const encrypted = crypto.publicEncrypt(
    { key: pemKey, padding: crypto.constants.RSA_PKCS1_PADDING },
    buffer
  );
  return encrypted.toString("base64");
}
```

## halo CLI Keyring Patch（无桌面环境）

在 headless Linux 服务器上，halo CLI 的 keyring 不可用。需要 patch `@halo-dev/cli/dist/cli.mjs`：

1. 添加 import：`import { readFileSync, writeFileSync, mkdirSync, existsSync, unlinkSync } from "node:fs";`
2. 替换 `KeyringCredentialStore` 类，使用文件存储（`~/.config/halo/cred_<profile>.json`）

**注意**：使用 ESM import（`import { ... } from "node:fs"`），不要用 `require`（ESM 模块中不可用）。

## Halo Console API 路径

| 资源 | 路径 |
|------|------|
| 文章 | `/apis/api.console.halo.run/v1alpha1/posts` |
| 分类 | `/apis/api.console.halo.run/v1alpha1/categories` |
| 标签 | `/apis/api.console.halo.run/v1alpha1/tags` |
| 评论 | `/apis/api.console.halo.run/v1alpha1/comments` |
| 通知 | `/apis/api.console.halo.run/v1alpha1/notifications` |
| 备份 | `/apis/api.console.halo.run/v1alpha1/backups` |
| 插件 | `/apis/api.console.halo.run/v1alpha1/plugins` |
| 主题 | `/apis/api.console.halo.run/v1alpha1/themes` |
| 页面 | `/apis/api.console.halo.run/v1alpha1/singlepages` |
| 动态 | `/apis/api.console.halo.run/v1alpha1/moments` |
| 健康检查 | `/actuator/health` |

## 注意事项

- 密码使用 RSA 4096 加密，不在磁盘上存储明文
- Session cookie 存储权限 600
- 所有 API 调用需要 `Cookie: SESSION=xxx` + `X-XSRF-TOKEN: xxx` headers
- Session 过期时返回 302 重定向到 `/login?authentication_required`
