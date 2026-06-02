# 网络管理子模块模式（2026-06-02）

> 从 network 模块开发提炼 — 多数据源聚合 + Dashboard 设计 + SNMP 监控

## 场景

将多个外部数据源（SNMP 交换机、SSH/OpenWrt、HTTP Lucky API、阿里云 ECS）聚合为 Workspace 统一管理界面。

## 架构

```
src/projects/network/
├── plugin.mjs              ← Fastify 路由（92 行）
├── api/
│   ├── devices.mjs         ← 设备 CRUD + Ping（269 行）
│   ├── overview.mjs        ← 概览聚合（150 行）
│   ├── openwrt.mjs         ← OpenWrt ubus/SSH（64 行）
│   ├── lucky.mjs           ← Lucky HTTP API（168 行）
│   ├── switch.mjs          ← SNMP 交换机（105 行）
│   └── aliyun.mjs          ← 阿里云 ECS（220 行）
├── services/
│   ├── collector.mjs       ← 后台定时采集+缓存（448 行）
│   ├── snmp-client.mjs     ← net-snmp 封装（123 行）
│   ├── ubus-client.mjs     ← ubus RPC 客户端（182 行）
│   └── ssh-client.mjs      ← sshpass 封装（71 行）
└── public/
    └── NetworkView.mjs     ← Vue3 前端（1390 行）
```

总计 3,282 行，12 个文件。

## 混合采集策略

| 数据源 | 协议 | 库/工具 | 缓存 | 超时 |
|--------|------|---------|------|------|
| OpenWrt | SSH + ubus RPC | sshpass + node:http | 60s | 10s |
| Lucky | HTTP API | node:http | 300s | 10s |
| 交换机 | SNMP v2c | net-snmp | 30s | 5s |
| 阿里云 | HTTPS REST | 手动签名 | 120s | 15s |

**原则：** 变化少的数据后台缓存，实时数据（Ping、流量）用户触发。

## Dashboard 设计模式（用户偏好）

用户明确要求：**少 Tab、聚合概览页、低功能模块不独立成 Tab。**

### 演进过程

1. 初版：6 Tab（概览/设备/IP地图/Lucky/OpenWrt/交换机/阿里云）
2. 用户反馈："加多个概览页，不要那么多 tab 页"
3. 优化：3 Tab（概览/设备/网络）

### 最终方案

**Tab 1: 概览（Dashboard）** — 6 个卡片区块：
1. 公网 IP（实时获取，点击复制）
2. 设备统计（在线/离线/分类）
3. 交换机 1 端口可视化图
4. 交换机 2 端口可视化图
5. Lucky + WireGuard（合并展示）
6. 阿里云实例（表格+操作按钮）

**Tab 2: 设备** — 搜索/过滤/排序 + CRUD + 批量操作 + IP 地图

**Tab 3: 网络** — OpenWrt / Lucky / 交换机 详情（折叠面板）

### 设计原则

1. 功能 < 3 个独立页面的模块 → 合并到概览页卡片
2. 概览页 = N 个卡片区块，每块独立刷新
3. 详情页用折叠面板（不用独立 Tab）

## SNMP 交换机监控

### 关键 OIDs

| OID | 名称 | 说明 |
|-----|------|------|
| 1.3.6.1.2.1.2.2.1.2 | ifDescr | 端口名 |
| 1.3.6.1.2.1.2.2.1.8 | ifOperStatus | 状态（1=up, 2=down） |
| 1.3.6.1.2.1.31.1.1.1.15 | ifHighSpeed | 速度（Mbps） |
| 1.3.6.1.2.1.31.1.1.1.6 | ifHCInOctets | 流入字节 |
| 1.3.6.1.2.1.31.1.1.1.10 | ifHCOutOctets | 流出字节 |

### 端口颜色编码（5 级）

用户要求细分，不要合并：

| 颜色 | CSS | 含义 |
|------|-----|------|
| 🟢 绿 | #10b981 | 10G 链接 |
| 🔵 蓝 | #3b82f6 | 2.5G 链接 |
| 🟠 橙 | #f59e0b | 1G 链接 |
| 🟡 黄 | #eab308 | 100M 链接 |
| 🔴 红 | #ef4444 | 端口 Down |

### Node.js SNMP 封装

```javascript
import snmp from 'net-snmp';

export function createSession(ip, community = 'public') {
  return snmp.createSession(ip, community, { timeout: 5000, retries: 1 });
}

export async function walk(session, oid) {
  return new Promise((resolve, reject) => {
    const results = [];
    session.walk(oid, (varbinds) => {
      for (const vb of varbinds) {
        if (snmp.isVarbindError(vb)) continue;
        results.push({ oid: vb.oid, value: vb.value });
      }
    }, (err) => err ? reject(err) : resolve(results));
  });
}
```

## 注册步骤

1. 创建 `src/projects/network/plugin.mjs`
2. 创建 `src/projects/network/api/*.mjs` + `services/*.mjs`
3. 创建 `src/projects/network/public/NetworkView.mjs`
4. 更新 `config/projects.json`（添加 tabs）
5. 更新 `server.mjs`（import + register）
6. 更新 `app.mjs`（import + 条件渲染）
7. `.env` 添加配置（OPENWRT_HOST, LUCKY_HOST, SNMP_COMMUNITY 等）
8. `pnpm add net-snmp --registry https://registry.npmmirror.com`
9. `pm2 restart workspace`

## 教训

- **CodeWhale 上下文膨胀：** 不要在 context 中列 6+ 参考文件路径。先写自包含 spec 文件（`SPEC_BACKEND.md`），告诉 CodeWhale 只读那一个
- **node:http 优于 fetch：** 代理内网服务时，fetch（undici）可能因 HTTP/2 ALPN 挂起
- **execFile 优于 execSync：** execSync 阻塞 Fastify 事件循环
- **阿里云 SDK 可选：** 无 AccessKey 时返回 `{ instances: [], configured: false }`，不影响其他功能
- **SNMP community 默认 public：** 从 .env 读取，不硬编码
