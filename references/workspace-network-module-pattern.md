# 网络管理子模块模式（2026-06-02）

> 从 network 模块开发提炼 — 多数据源聚合 + Dashboard 设计 + SNMP 监控

## 场景

将多个外部数据源（SNMP 交换机、SSH/OpenWrt、HTTP Lucky API、阿里云 ECS）聚合为 Workspace 统一管理界面。

## 硬编码端口配置模式（2026-06-05）

消费级交换机 SNMP walk 返回的端口列表不可靠（包含虚拟端口、CPU 接口等）。**解决方案：硬编码物理端口配置，SNMP 数据只用于匹配状态。**

### 前端常量定义（NetworkView.mjs 顶部）

```javascript
const SWITCH_PORT_CONFIGS = {
  '192.168.0.3': {
    model: 'ZX530S-8T4XS',
    ports: [
      // 8T = 8 RJ45 电口
      { index: 1, type: 'rj45', label: '1' }, { index: 2, type: 'rj45', label: '2' },
      { index: 3, type: 'rj45', label: '3' }, { index: 4, type: 'rj45', label: '4' },
      { index: 5, type: 'rj45', label: '5' }, { index: 6, type: 'rj45', label: '6' },
      { index: 7, type: 'rj45', label: '7' }, { index: 8, type: 'rj45', label: '8' },
      // 4XS = 4 SFP+ 光口
      { index: 9, type: 'sfp', label: '9' }, { index: 10, type: 'sfp', label: '10' },
      { index: 11, type: 'sfp', label: '11' }, { index: 12, type: 'sfp', label: '12' },
    ],
  },
  '192.168.0.4': {
    model: 'ZX-SWTGW2224AS',
    ports: [
      ...Array.from({ length: 24 }, (_, i) => ({ index: i + 1, type: 'rj45', label: String(i + 1) })),
      { index: 25, type: 'sfp', label: '25' }, { index: 26, type: 'sfp', label: '26' },
    ],
  },
};
```

### 渲染逻辑（switchPanel 函数）

```javascript
const switchPanel = (ports, ip) => {
  const config = SWITCH_PORT_CONFIGS[ip];
  if (!config) return h('div', { class: 'net-muted' }, `未知交换机 ${ip}`);

  // SNMP 数据 → index 映射（只用于匹配状态，不决定布局）
  const portMap = {};
  for (const p of (ports || [])) {
    portMap[p.index || p.port || p.id] = p;
  }

  // 按 type 分组：SFP+ 和 RJ45 分开显示
  const sfpPorts = config.ports.filter(p => p.type === 'sfp');
  const rj45Ports = config.ports.filter(p => p.type === 'rj45');

  // 每组显示 up/down 计数
  const sfpUp = sfpPorts.filter(p => portMap[p.index]?.status === 'up').length;
  const rj45Up = rj45Ports.filter(p => portMap[p.index]?.status === 'up').length;
};
```

**关键：** `config.ports` 决定显示哪些端口和布局，`portMap` 只提供运行时状态。两者解耦。

## IP 地图视觉区分（2026-06-05 教训）

已用/未用 IP 的背景色必须有**明显区分**，否则用户看不出哪些 IP 被占用。

用户明确要求：**用绿色统一标识已占用 IP**（不用分类颜色），未用 IP 用浅灰。

| 状态 | 背景 | 边框 | 编号色 |
|------|------|------|--------|
| 在线 | `rgba(16,185,129,0.25)` | `1.5px solid rgba(16,185,129,0.5)` | `#065f46` |
| 离线 | `rgba(16,185,129,0.12)` | `1.5px solid rgba(16,185,129,0.25)` | `#065f46` |
| 未用 | `rgba(248,250,252,0.5)` | `1px solid rgba(0,0,0,0.06)` | `#cbd5e1` |

## WireGuard Peer 名称（2026-06-05）

`wg show` 不输出 peer 名称。Peer 描述存在 OpenWrt UCI 配置（`option description`）。collector 需额外 `uci show network` 按 public_key 匹配。

## 路由器端口 CSS（2026-06-05）

路由器端口必须和交换机端口用相同尺寸（44px/min-width/38px 高度），用 `.rp-ports-row` 子容器避免水平拖拉条。

## IPv4/IPv6 显示（2026-06-05）

用户要求：用**圆角边框包裹**，IPv4 蓝色标签（`#3b82f6`）+ 蓝色边框，IPv6 紫色标签（`#8b5cf6`）+ 紫色边框，统一 16px 等宽字体。

## Lucky Token 过期处理（2026-06-05）

API 返回 `ret: -1` 时前端区分"未配置"和"认证失败"，显示提示让用户更新 `.env` 的 `LUCKY_TOKEN`。
