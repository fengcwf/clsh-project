# Halo 认证 + Obsidian CLI 参考

## Halo 认证方式优先级

### 1. PAT（Personal Access Token）— 推荐
- Halo 2.11+ 支持
- 在个人中心 → 个人令牌页面创建
- 权限选择 `Post Manage`
- 得到 `pat_` 开头的字符串
- 请求头：`Authorization: Bearer pat_xxx`
- **无需 session cookie，无需 RSA 加密**

```bash
curl -s "$HALO_URL/apis/content.halo.run/v1alpha1/posts" \
  -H "Authorization: Bearer $HALO_PAT"
```

### 2. Session Cookie（备用）
- 表单登录 + RSA 4096 加密 + CSRF token
- 脚本：`node scripts/halo-login.cjs`
- 保存到 `~/.config/halo-blog/session.json`

### 3. Basic Auth（不推荐）
- Halo 2.20+ 默认关闭
- 需要手动开启：`halo.security.basic-auth.disabled=false`

## Obsidian CLI 使用

### 环境
- Obsidian 1.12.7+ 已安装（`/opt/Obsidian/obsidian`）
- Xvfb 提供虚拟显示（`:99`）
- Socket 路径：`/run/user/0/.obsidian-cli.sock`

### 配置
- 全局配置：`~/.config/obsidian/obsidian.json`（需包含 `"cli": true`）
- Vault 配置：`<vault>/.obsidian/app.json`（需包含 `"cliEnabled": true`）

### CLI 命令
```bash
obsidian-cli vault                   # vault 信息
obsidian-cli files limit=10          # 文件列表
obsidian-cli read file="My Note"     # 读笔记
obsidian-cli create name="New Note" content="# Hello"
obsidian-cli append file="My Note" content="New line"
obsidian-cli search query="keyword" limit=10
obsidian-cli tags                    # 列出标签
obsidian-cli backlinks file="My Note"  # 反链
obsidian-cli daily:read              # 读日记
obsidian-cli daily:append content="- [ ] 任务"  # 写日记
```

### ⚠️ 已知问题
- CLI 连接 socket 成功但可能返回 "Vault not found"
- **替代方案**：直接文件系统操作 vault 目录
- Obsidian 文件 watcher 自动检测外部变更并重建索引

### 文件系统操作（推荐）
```bash
# 直接写入 vault
cp article.md /mnt/unraid_data/Obsidian/01-文章/已发布/

# 创建新笔记
cat > /mnt/unraid_data/Obsidian/01-文章/新笔记.md << 'EOF'
---
title: 新笔记
date: 2026-05-18
tags: [test]
---

# 新笔记内容
EOF
```

## 发布渠道参考

### Halo
- **obsidian-halo 插件**：社区插件，PAT 认证，GUI 操作（服务器端不可用）
- **直接 API 调用**：PAT 或 session cookie 调 Console API

### 微信公众号
- **obsidian-wechat-public-platform 插件**：社区插件，GUI 操作
- **md2wechat-skill**：CLI 工具，Markdown → 微信排版 → 发布
- **微信公众平台 API**：直接调用 API 发布

### 其他渠道
- 知乎、掘金等：通过各平台 API 或浏览器自动化发布
