# Halo CLI 认证方案：Linux 无桌面环境

## 问题

Halo CLI 在 Linux 无桌面环境上 keyring 不可用，`halo auth login` 失败。

## 根因

`@napi-rs/keyring` 需要 D-Bus/Secret Service，服务器上不可用。

## 解决方案：Patch 为文件存储

1. 添加 import：`import { readFileSync, writeFileSync, mkdirSync, existsSync, unlinkSync } from "node:fs";`
2. 替换 `KeyringCredentialStore` 类为文件操作
3. 凭证存储：`~/.config/halo/cred_<profile>.json`

## Halo 认证机制

- Basic Auth 默认不启用（302 重定向到 /login）
- Session Cookie 认证：GET /login → CSRF + XSRF + RSA 公钥 → RSA 加密密码 → POST /login → SESSION cookie
- jsencrypt 在 Node.js 24 ESM 下不可用，用 `crypto.publicEncrypt` 替代

## API 端点

见 https://docs.halo.run/ 开发者文档
