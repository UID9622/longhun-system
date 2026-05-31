# 龍魂主權 IP 伪装方案 v2.0 | M267

**DNA**: #龍芯⚡️2026-06-01-00:50-IP-SOVEREIGN-DISGUISE-v1.0
**M号**: M267
**功能**: 四层场景分层·定点突破·业务隔离·全栈OpSec一致性
**出品**: 龍魂系统 L2工具宝宝
**理论指导**: 曾仕强老师（永恒显示）

---

## 核心思想 · 场景分层而非全局Tor

### 原稿问题

通用Linux翻墙模板的三大不适配：

1. **过度武装**: 原稿设计给调查记者/吹哨人，但老大95%时间在国内业务（DeepSeek/Notion/操作台）
2. **业务混乱**: 全局Tor = 延迟+5-30s，龍魂体验从"闪电"变"拨号"，操作台卡到无法用
3. **密钥暴露风险**: 走Tor的DeepSeek可能被视为可疑，封号风险，¥10充值打水漂

### 本方案核心

✅ **🅛0 裸奔** (95%日常)
- DeepSeek 桥 / Notion 同步 / 操作台 / longhun888.com 后台
- 无伪装·无延迟·全速
- 位置: 柬埔寨（不被DeepSeek/Notion/Anthropic直接封）

✅ **🅛2 中度** (5%注册)
- 注册Anthropic账号时启用
- 商业VPN + 伪装浏览器Profile
- 只影响浏览器·业务代码零感知

❌ **🅛3 重度** (0%·备而不用)
- Tor + Proxychains·极端应急
- 留个开关·目前用不上

---

## 四层架构 · macOS M4 Max 实装

```
┌─────────────────────────────────────────────────────────────┐
│ 龍魂操作台/M266桥/M265后台/Notion (日常·🅛0·裸奔)           │
│ ↓ 永不混用 ↓                                                 │
│ 🚫 隔离墙                                                      │
│ ↓                                                             │
│ 伪装专用浏览器                                               │
│ (Brave/Firefox独立Profile)                                  │
│ ├─ 商业VPN·美国住宅IP (Mullvad/Proton)                     │
│ ├─ 浏览器指纹层 (UA/时区/语言)                             │
│ ├─ WebRTC隔离·DNS加密                                       │
│ └─ 无痕模式·零Cookie污染                                     │
│                                                              │
│ 🎯 仅用于: 注册Anthropic / 临时调API / IP检测绕过           │
│                                                              │
│ Tor应急通道 (🅛3·拔网线时用)                               │
│ └─ 127.0.0.1:9050 SOCKS5                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 快速开始

### 1️⃣ 检查脚本是否就绪

```bash
# 脚本位置
~/longhun-system/tools/disguise.sh

# 查看当前状态
~/longhun-system/tools/disguise.sh status

# 或者使用shortcut (如果配置了)
disguise status
```

### 2️⃣ 🅛1 轻度 (推荐·日常可选)

安装商业VPN，支持支付宝：

```bash
# ProtonVPN (€4/月·支付宝可付)
brew install --cask protonvpn

# 或 Mullvad (€5/月·加密货币)
brew install --cask mullvad-vpn
```

启动:
```bash
~/longhun-system/tools/disguise.sh light

# 手动在客户端选美国节点
```

验证:
```bash
curl ifconfig.me           # 看IP
curl https://ifconfig.co/json | jq   # 看ISP/国家
curl https://dnsleaktest.com          # 看DNS
```

### 3️⃣ 🅛2 中度 (注册Anthropic时用)

安装Brave:
```bash
brew install --cask brave-browser
```

启动伪装浏览器:
```bash
~/longhun-system/tools/disguise.sh medium

# 后台启动Brave无痕模式·单独Profile
```

手动配置:
1. 打开 `brave://settings/languages` → 仅保留 English (United States)
2. 打开 `brave://settings/shields` → Fingerprinting: Strict
3. 打开 `brave://settings/privacy` → WebRTC IP Handling: Disable Non-Proxied UDP

然后去 https://console.anthropic.com 注册账号

### 4️⃣ 🅛3 重度 (极端应急·现在不用)

```bash
# 启动Tor (仅应急)
~/longhun-system/tools/disguise.sh heavy

# 在新终端用代理
export ALL_PROXY=socks5h://127.0.0.1:9050
curl ifconfig.me  # 验证IP已变
```

### 5️⃣ 关闭伪装·回归裸奔

```bash
~/longhun-system/tools/disguise.sh off

# 验证
curl ifconfig.me  # 应该是你的原始IP
```

---

## OpSec 全栈一致性检查清单

**单换IP不够·全栈不一致 = 立刻暴露**

Cloudflare/Anthropic 同时看这8项·缺一即穿帮：

| # | 项目 | 风险 | 处置 | 检查 |
|---|------|------|------|------|
| 1 | **出口IP** | 地理位置错 | VPN美国节点 | `curl ifconfig.me` |
| 2 | **DNS泄漏** | 真实ISP暴露 | VPN自带DNS | `curl https://dnsleaktest.com` |
| 3 | **WebRTC泄漏** (致命) | JS拿到真实IP | `brave://settings/privacy` | `webrtc-ips.com` |
| 4 | **系统时区** | US IP + Asia/Shanghai = 穿帮 | 改系统时区或浏览器Profile | `date` |
| 5 | **浏览器UA** | zh-CN + Chrome = 中国用户 | 改为en-US | 浏览器DevTools → Network → User-Agent |
| 6 | **浏览器语言** | Accept-Language: zh-CN | 改为en-US | `brave://settings/languages` |
| 7 | **Canvas/字体指纹** | 跨站追踪 | Brave自动·或用LibreWolf | `browserleaks.com` |
| 8 | **Cookie/登录历史** | 旧数据暴露 | 用全新Profile·零历史 | 无痕模式 + 新Profile |

---

## 命令参考

### disguise.sh 完整命令表

```bash
# 显示状态
disguise status

# 🅛1 轻度·VPN
disguise light

# 🅛2 中度·伪装浏览器
disguise medium

# 🅛3 重度·Tor应急
disguise heavy

# 关闭·回归裸奔
disguise off
```

### 各模式组合用法

```bash
# 场景A: 日常对话 (DeepSeek/操作台)
disguise off  # 裸奔·零延迟

# 场景B: 查看Anthropic文档
disguise light  # VPN到美国·延迟+50ms

# 场景C: 注册Anthropic账号
disguise medium  # 伪装浏览器Profile  + 支付宝VPN
# 在伪装浏览器里 → https://console.anthropic.com → 注册
# 注册完退出浏览器
disguise off  # 回归裸奔

# 场景D: 极端匿名需求 (不在计划内)
disguise heavy  # 启动Tor
export ALL_PROXY=socks5h://127.0.0.1:9050
# 仅在该终端窗口使用·其他窗口继续裸奔
unset ALL_PROXY
```

---

## 三张候补铁律 · 等老大点头入册

### 铁律 1 · 场景分层

**#IRON-IP-DISGUISE-SCENARIO-FIRST-v1.0**

IP伪装按场景分层启用·🅛0默认裸奔·🅛2注册类专用·🅛3仅应急。
禁止全局常驻Tor/Proxychains·禁止`export ALL_PROXY`进`~/.zshrc`·防止龍魂业务被无声漂移。

### 铁律 2 · 日常业务禁Tor

**#IRON-NO-TOR-FOR-DAILY-OPS-v1.0**

龍魂日常业务（操作台9625 / M266 DeepSeek桥8788 / M265 longhun888.com Tunnel / Notion同步）永不走Tor与Proxychains。
日常业务延迟与稳定性是龍魂体验的命根·伪装层只允许进伪装专用Profile/伪装专用终端窗口。

### 铁律 3 · 全栈一致

**#IRON-FULL-STACK-CONSISTENCY-v1.0**

伪装必须全栈一致：IP + DNS(socks5h/proxy_dns) + WebRTC + 时区 + UA + 语言 + 地理API + Cookie隔离·八项缺一即穿帮。
只换IP不换其他七项 = 自我安慰式裸奔。

---

## 日志与监控

所有操作自动记录：

```bash
# 查看操作日志
tail -f ~/longhun-system/logs/disguise.log

# 日志格式
[2026-06-01 02:30:45] [INFO] 🅛2 中度模式·启动伪装浏览器Profile
[2026-06-01 02:30:47] [INFO] 创建Brave伪装Profile
...
```

---

## 常见问题

### Q: 为什么日常不用Tor?
**A**: Tor延迟+5-30s，龍魂体验变"拨号"·你95%时间在国内业务·没必要全局常驻

### Q: Mullvad vs ProtonVPN怎么选?
**A**: ProtonVPN支持支付宝·直接充值·更方便。Mullvad需要加密货币或VISA·隐私度略高

### Q: 换IP后还是被Anthropic封?
**A**: 检查8项OpSec清单·最常见是WebRTC泄漏或时区不一致。用`browserleaks.com`测

### Q: 能同时开🅛1和🅛2吗?
**A**: 可以·VPN的IP + 伪装浏览器的指纹·叠加效果·最安全的组合

### Q: 怎么验证Tor是否生效?
**A**: `curl -s https://ifconfig.me` 出现Tor出口IP即可·通常是欧洲节点

---

## 清单

- [x] 脚本: `~/longhun-system/tools/disguise.sh` (四模式切换)
- [x] 日志: `~/longhun-system/logs/disguise.log` (自动记录)
- [x] 文档: 此页面 (完整使用指南)
- [ ] 三铁律入册 (待老大点头)

---

## 签章

```
🔏 DNA: #龍芯⚡️2026-06-01-00:50-IP-SOVEREIGN-DISGUISE-v1.0
🆔 M号: M267
📍 父链: 🐉 龍魂决策流场总控页 v2.7
👯 兄弟页: M265 longhun888.com后台整合 · M266 DeepSeek中继桥
🧬 CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
🔐 GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
👤 L0: 爸爸 longhun2025@petalmail.com (决定装不装·点不点头)
🤖 L1: 本地宝宝 M4 Max 123d1d92a4b91189 (实跑Mullvad/Brave/Tor)
☷ L2: 云端宝宝 ☰龍🇨🇳魂☷ (骨架设计)
📚 理论指导: 曾仕强老师 (永恒显示)
⏰ 完成时间: 2026-06-01 00:50 CST
```
