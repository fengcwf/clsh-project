# 云服务器 + Wireguard 参考

## 云主机信息（clsh-content 项目）

| 项目 | 值 |
|------|-----|
| 公网 IP | `<CLOUD_SERVER_IP>` |
| SSH 端口 | `<SSH_PORT>` |
| 用户名/密码 | `root` / `<CLOUD_PASSWORD>` |
| 系统 | CentOS 8 (5.10.134) |
| Wireguard IP | `<WG_CLIENT_IP>` |

## SSH 连接

```bash
sshpass -p '<CLOUD_PASSWORD>' ssh -p <SSH_PORT> root@<CLOUD_SERVER_IP> "命令"
```

## Wireguard 配置（云主机客户端）

```ini
[Interface]
PrivateKey = <客户端私钥>
Address = <WG_CLIENT_IP>
ListenPort = 51820
DNS = 192.168.0.1

[Peer]
PublicKey = <服务端公钥>
PresharedKey = <预共享密钥>
AllowedIPs = 192.168.0.0/24
Endpoint = <DOMAIN>:51820
PersistentKeepAlive = 25
```

## 家庭网络拓扑

```
云主机 (<CLOUD_SERVER_IP>) ←──Wireguard──→ 家庭 OpenWrt (10.10.0.1)
                                      │
                                      ├── 192.168.0.1 (路由器)
                                      ├── 192.168.0.254 (Unraid)
                                      └── 192.168.0.x (其他设备)
```

## 注意事项

1. **SSH 端口**：云主机 SSH 端口是 <SSH_PORT>（非默认 22）
2. **Wireguard 方向**：云主机是客户端，家庭 OpenWrt 是服务端
3. **AllowedIPs**：`192.168.0.0/24` 表示只有家庭网络流量走隧道
4. **PersistentKeepAlive**：25 秒保活，防止 NAT 超时
