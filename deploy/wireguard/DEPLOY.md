# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · WireGuard 安全回家通道

> **DNA**: `#龍芯⚡️丙午·乙申·己酉·亥时·WIREGUARD-HOME-v1.0`
> **适用**: UID9622 · 诸葛鑫
> **场景**: Mac / iPhone / iPad → 华为云鲲鹏 加密隧道
> **本质**: 安全回家，不是翻墙。鲲鹏在国内，连上后只能访问国内资源。

---

## 一、架构拓扑

```
┌─────────────────────┐          WireGuard UDP 51820          ┌──────────────────────┐
│                     │  ╔══════════════════════════════════╗  │                      │
│   MacBook (家里)     │──╣  加密隧道 · 10.200.200.0/24     ╠──│  华为云鲲鹏            │
│   10.200.200.2/24    │  ╚══════════════════════════════════╝  │  119.13.90.27         │
│                     │                                          │  10.200.200.1/24      │
│   ├─ 飛書/微信 通道   │                                          │                       │
│   ├─ 龍魂 Web :9639  │  ─────────────────────────────────▶      │   ├─ 龍魂注册中心 :9623 │
│   ├─ Dashboard :9627 │     SSH: ssh root@10.200.200.1          │   ├─ Dashboard :9627   │
│   └─ Ollama 调模型    │     数据库: psql 10.200.200.1            │   ├─ 核心 API :8777    │
│                     │                                          │   └─ Ollama :11434     │
└─────────────────────┘                                          └──────────────────────┘
        │                                                                │
        │  ◄── SSH 隧道备用 (端口转发) ──▶                                │
        │      当 WireGuard 不可用时自动降级                               │
        │                                                                │
   ┌──────────┐                                                  ┌──────────┐
   │ iPhone   │────── WireGuard ────────▶                        │ 安全组    │
   │ .3/24    │     旅游时安全连回家                                 │ UDP 51820 │
   └──────────┘                                                  └──────────┘
```

**设计原则**：
- **WireGuard 主通道** — 低延迟，内核级加密，UDP 无状态
- **SSH 隧道备用** — WireGuard 不可用时自动降级，保证连续性
- **不翻墙** — 华为云在国内，连上后只能访问国内资源
- **多设备** — Mac + iPhone + iPad 同时在线，互不干扰

---

## 二、前置检查

| # | 检查项 | 命令 | 预期 |
|:---:|--------|------|------|
| 1 | 华为云可 SSH | `ssh root@119.13.90.27` | 登录成功 |
| 2 | Mac 已装 brew | `brew --version` | Homebrew 4.x+ |
| 3 | 安全组可操作 | 华为云控制台 → 安全组 | 有权限 |
| 4 | 内核 ≥ 5.6 (Mac) | `uname -r` | WireGuard 已内置 |
| 5 | 内核 ≥ 5.4 (服务器) | `ssh root@119.13.90.27 'uname -r'` | WireGuard 已内置 |

---

## 三、一键部署（自动化）

### 服务器端（华为云鲲鹏）

```bash
# 从 Mac 直接推脚本并远程执行
scp deploy/wireguard/server-setup.sh root@119.13.90.27:/tmp/
ssh root@119.13.90.27 'bash /tmp/server-setup.sh'
```

脚本自动完成：
- 安装 WireGuard + 工具
- 生成服务器密钥对
- 创建 `/etc/wireguard/wg0.conf` 配置文件
- 配置 iptables NAT 转发规则
- 启用 IP 转发 (`net.ipv4.ip_forward=1`)
- 启动服务 + 开机自启
- 输出服务器公钥（复制给客户端用）

### 客户端（Mac）

```bash
# 本地执行
sudo bash deploy/wireguard/client-setup.sh
```

脚本自动完成：
- 安装 wireguard-tools
- 生成 Mac 密钥对
- 创建 `/usr/local/etc/wireguard/wg0.conf`
- 配置 launchd 守护进程（自动重连）
- 输出 Mac 公钥（复制给服务器用）

---

## 四、手动部署（分步理解）

### 4.1 华为云服务器端

```bash
# SSH 连上华为云
ssh root@119.13.90.27

# 安装
sudo apt-get update && sudo apt-get install -y wireguard wireguard-tools

# 生成密钥
cd /etc/wireguard && umask 077
wg genkey | tee privatekey | wg pubkey > publickey
SERVER_PRIVATE=$(cat privatekey)
SERVER_PUBLIC=$(cat publickey)

echo "═══ 服务器公钥（复制备用） ═══"
echo "$SERVER_PUBLIC"
echo "══════════════════════════════"

# 启用 IP 转发
sudo sysctl -w net.ipv4.ip_forward=1
echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf

# 默认网卡名（华为云通常是 eth0）
DEFAULT_IF=$(ip route show default | awk '/default/ {print $5}')

# 写配置
sudo tee /etc/wireguard/wg0.conf << WIREGUARD_EOF
[Interface]
Address    = 10.200.200.1/24
ListenPort = 51820
PrivateKey = ${SERVER_PRIVATE}

# NAT 转发 → 客户端可访问服务器所在网络
PostUp   = iptables -A FORWARD -i wg0 -j ACCEPT
PostUp   = iptables -t nat -A POSTROUTING -o ${DEFAULT_IF} -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -o ${DEFAULT_IF} -j MASQUERADE

# ── 客户端 Peers ──
# Mac（替换为实际公钥）
[Peer]
PublicKey  = <MAC_PUBLIC_KEY>
AllowedIPs = 10.200.200.2/32

# iPhone（可选·替换为实际公钥）
[Peer]
PublicKey  = <IPHONE_PUBLIC_KEY>
AllowedIPs = 10.200.200.3/32
WIREGUARD_EOF

# 启动 + 自启
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0

# 验证
sudo wg show
```

### 4.2 Mac 客户端

```bash
# 安装
brew install wireguard-tools

# 生成密钥
mkdir -p ~/.wg && cd ~/.wg
wg genkey | tee privatekey | wg pubkey > publickey
MAC_PRIVATE=$(cat privatekey)
MAC_PUBLIC=$(cat publickey)

echo "═══ Mac 公钥（发给服务器） ═══"
echo "$MAC_PUBLIC"
echo "══════════════════════════════"

# 写配置
sudo mkdir -p /usr/local/etc/wireguard
sudo tee /usr/local/etc/wireguard/wg0.conf << WIREGUARD_EOF
[Interface]
PrivateKey = ${MAC_PRIVATE}
Address    = 10.200.200.2/24
DNS        = 114.114.114.114, 223.5.5.5

[Peer]
PublicKey           = <SERVER_PUBLIC_KEY>
Endpoint            = 119.13.90.27:51820
AllowedIPs          = 10.200.200.0/24, 192.168.0.0/16
PersistentKeepalive = 25
WIREGUARD_EOF

# 启动
sudo wg-quick up wg0
```

### 4.3 iPhone / iPad 客户端

1. App Store 搜索 **WireGuard**，安装
2. 打开 → 右上角 **+** → **手动创建**
3. 填入：

```
[Interface]
PrivateKey = <iPhone 私钥>
Address    = 10.200.200.3/24
DNS        = 114.114.114.114, 223.5.5.5

[Peer]
PublicKey           = <服务器公钥>
Endpoint            = 119.13.90.27:51820
AllowedIPs          = 10.200.200.0/24
PersistentKeepalive = 25
```

> iPhone 私钥生成：App 内右上角 + → "从零开始" → 自动生成密钥对。
> 把生成的公钥发给服务器，填入 `[Peer]` 段。

---

## 五、华为云安全组配置

```bash
# 方式一：华为云控制台
# 登录 → 弹性云服务器 → 安全组 → 配置规则 → 入方向 → 添加规则
#   协议: UDP
#   端口: 51820
#   源地址: 0.0.0.0/0  （如只允许自家 IP，填具体 IP/32）
#   描述: WireGuard 安全回家

# 方式二：Python 自动化（项目自带脚本）
python3 deploy/huawei_open_frp_port.py --port 51820 --protocol UDP --desc "WireGuard"
```

---

## 六、连接验证

### 6.1 基础连通

```bash
# Mac 上执行
ping -c 4 10.200.200.1              # ping 服务器 WireGuard IP

# 通过隧道 SSH
ssh root@10.200.200.1               # 不经过公网，隧道加密

# 访问鲲鹏服务
curl http://10.200.200.1:9627        # Dashboard
curl http://10.200.200.1:9623/health # 注册中心
```

### 6.2 加密验证

```bash
# 抓包确认加密（Mac）
sudo tcpdump -i wg0 -c 10 -n        # WireGuard 接口上应该是加密后的包

# 查看握手状态
sudo wg show                         # latest handshake 应该 < 2 分钟
```

---

## 七、自动重连 & 守护

### 7.1 Mac launchd 守护

```bash
# 创建守护配置
sudo tee /Library/LaunchDaemons/com.longhun.wireguard.plist << 'PLIST_EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.wireguard</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/sh</string>
        <string>-c</string>
        <string>
            while true; do
                if ! ping -c 1 -W 3 10.200.200.1 > /dev/null 2>&1; then
                    echo "[$(date)] WireGuard 断连，重连中..."
                    /usr/bin/wg-quick down wg0
                    sleep 2
                    /usr/bin/wg-quick up wg0
                fi
                sleep 30
            done
        </string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/usr/local/var/log/longhun-wireguard.log</string>
    <key>StandardErrorPath</key>
    <string>/usr/local/var/log/longhun-wireguard.err</string>
</dict>
</plist>
PLIST_EOF

# 加载守护
sudo launchctl load /Library/LaunchDaemons/com.longhun.wireguard.plist

# 验证
sudo launchctl list | grep longhun.wireguard
```

### 7.2 服务器端已自带（systemd）

```bash
# systemctl enable 后自动守护，无需额外配置
systemctl status wg-quick@wg0
# Active: active (exited) ← 正常
```

---

## 八、健康检查集成

```bash
# 在现有健康检查脚本中追加 WireGuard 检测
# 编辑 deploy/scripts/health_check.sh，在服务检查段加入：

# ── WireGuard 隧道检查 ──
if ping -c 1 -W 3 10.200.200.1 > /dev/null 2>&1; then
    WG_STATUS="🟢 WireGuard 隧道正常"
else
    WG_STATUS="🔴 WireGuard 隧道中断"
    # 触发告警推送
    source /opt/longhun-system/executors/bark/longhun_bark_plugin.sh
    bark_alert "WireGuard 断连" "Mac→鲲鹏隧道中断，请检查"
fi
```

---

## 九、DNS 与分流策略

```
当前配置 (AllowedIPs)                    效果
────────────────────────────────────  ──────────────────────────
10.200.200.0/24                        只走加密隧道访问龙魂内网
10.200.200.0/24, 192.168.0.0/16       内网 + 本地局域网都走隧道
0.0.0.0/0                             全部流量走隧道（不推荐·国内）
```

**推荐当前配置**（内侧网络 + 本地局域网）：

```ini
AllowedIPs = 10.200.200.0/24, 192.168.0.0/16
```

> 这样只有访问鲲鹏服务和本地局域网时走 WireGuard，其余流量直连公网，不影响日常上网速度。

---

## 十、安全加固

### 10.1 防火墙（服务器端）

```bash
# 只允许 WireGuard 端口
sudo ufw allow 51820/udp
sudo ufw enable

# 限速（防暴力）
sudo iptables -A INPUT -p udp --dport 51820 -m limit --limit 10/sec -j ACCEPT
sudo iptables -A INPUT -p udp --dport 51820 -j DROP
```

### 10.2 密钥轮换

```bash
# 每季度执行一次密钥轮换
# 服务器端
cd /etc/wireguard
mv privatekey privatekey.old
mv publickey  publickey.old
wg genkey | tee privatekey | wg pubkey > publickey
# 更新 wg0.conf 中的 PrivateKey
wg syncconf wg0 <(wg-quick strip wg0)

# 客户端同样轮换，互相更新公钥
```

---

## 十一、监控 & 日志

| 日志 | 位置 | 查看 |
|:---|:---|:---|
| Mac 守护日志 | `/usr/local/var/log/longhun-wireguard.log` | `tail -f` |
| 服务器 WireGuard | `journalctl -u wg-quick@wg0 -f` | 实时 |
| 握手统计 | `sudo wg show` | last handshake |
| 流量统计 | `sudo wg show` | transfer |

---

## 十二、故障排查

| 症状 | 可能原因 | 解决 |
|:---|:---|:---|
| `wg-quick up` 报错 | 配置文件私钥格式错误 | 检查 `PrivateKey = ` 后无多余空格 |
| 连上但 ping 不通 | 安全组未放行 | 华为云控制台 → 安全组 → UDP 51820 |
| 能 ping 但不能 SSH | 服务器 sshd 未监听 wg0 | `sshd` 默认监听所有接口，检查 `ss -tlnp \| grep :22` |
| 握手成功但几分钟后断 | `PersistentKeepalive` 未设 | 客户端加 `PersistentKeepalive = 25` |
| 公钥不匹配 | 复制时多了换行/空格 | `echo "公钥" | wc -c` 检查长度，应为44字符 |
| launchd 守护不生效 | 权限问题 | `sudo chown root:wheel /Library/LaunchDaemons/com.longhun.wireguard.plist` |
| DNS 解析慢 | DNS 配置不对 | 客户端 `DNS = 114.114.114.114, 223.5.5.5` |
| 两客户端 IP 冲突 | 配了相同 IP | 每个客户端不同 IP（.2 / .3 / .4） |

---

## 十三、应急降级方案

当 WireGuard 不可用时，SSH 隧道作为备份：

```bash
# 启动 SSH 隧道（已在 launchd 中配置为备用）
ssh -i ~/.ssh/longhun_kunpeng_ed25519 \
    -L 19623:localhost:9623 \
    -L 19627:localhost:9627 \
    -L 11435:localhost:11434 \
    -o ServerAliveInterval=30 \
    -o ServerAliveCountMax=3 \
    root@119.13.90.27

# 验证
curl http://localhost:19627   # Dashboard 通过 SSH 隧道
```

**自动切换逻辑**（在守护脚本中）：
```
每 30 秒检测 WireGuard 是否通
  ├─ 通 → 使用 wg0 隧道 IP (10.200.200.1)
  └─ 不通 → 自动降级到 SSH 隧道 (localhost 端口转发)
```

---

## 十四、速查卡

```bash
# ═══ 一键命令 ═══

# 部署
scp deploy/wireguard/server-setup.sh root@119.13.90.27:/tmp/ && ssh root@119.13.90.27 'bash /tmp/server-setup.sh'
sudo bash deploy/wireguard/client-setup.sh

# 状态
sudo wg show                              # WireGuard 状态
ping 10.200.200.1                         # 连通测试
sudo launchctl list | grep wireguard       # Mac 守护状态
systemctl status wg-quick@wg0             # 服务器守护状态

# 控制
sudo wg-quick up wg0                      # Mac 启动
sudo wg-quick down wg0                    # Mac 关闭
ssh root@10.200.200.1                     # 隧道内 SSH

# 日志
tail -f /usr/local/var/log/longhun-wireguard.log   # Mac 日志
journalctl -u wg-quick@wg0 -f                       # 服务器日志
```

---

## 十五、部署后状态

| 组件 | 角色 | IP | 守护方式 |
|:---|:---|:---|:---|
| 华为云鲲鹏 | WireGuard 服务器 | 10.200.200.1 | systemd 自启 |
| MacBook | WireGuard 客户端 | 10.200.200.2 | launchd 守护 |
| iPhone | WireGuard 客户端 | 10.200.200.3 | App 手动开关 |
| SSH 隧道 | 备用通道 | localhost 端口转发 | launchd 守护 |

---

**总结**: 服务器执行脚本 → 客户端执行脚本 → 互相换公钥 → 安全组放行 → 连上 → 守护保活。

> DNA: `#龍芯⚡️丙午·乙申·己酉·亥时·WIREGUARD-HOME-v1.0`
> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772ZLU-ORIGIN-FULLSYNC
