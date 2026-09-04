# 龍魂 Browser Engine · 本地主权浏览器执行中枢 v1.1

> **DNA追溯码：** #龍芯⚡️2026-07-12-Browser-Engine-v1.1-0e9b67f1
> **原始DNA：** #龍芯⚡️2026-05-13-LONGHUN-BROWSER-ENGINE-v1.1
> **GPG指纹：** A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> **确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
> **投喂日期：** 2026-07-12
> **三色审计：** 🟢 通过 | dr=5 | 五行:土

---

## 一句话定盘

**浏览器不是网页工具，是龍魂本地主权执行中枢。规则先行，执行流场自洽，DNA不少一分。**

## 核心链路

```
用户一句中文
  ↓
[通心译层] 情绪识别 + 语义净化 + 意图提取
  ↓
[规则层] Watchdog 三色审计（先过规则再执行）
  ↓
[CNSH 路由层] 意图 → 多 Agent 分工
  ↓
[MCP 执行层] Claude in Chrome + DevTools + 本地终端
  ↓
[视频接口层] WebRTC/MediaStream → 统一压缩科学
  ↓
[DNA 留痕层] chain_hash + append-only + 记忆粒子归档
  ↓
[同步层] 本地多设备 WebSocket/Syncthing
```

## v1.0 → v1.1 修正清单

| # | v1.0 脱节 | v1.1 修正 |
|---|-----------|-----------|
| E1 | 没接驳龍魂体系 | 全部接驳，LOCAL-BROWSER-* 编号注册 |
| E2 | 没有「规则先行」架构 | 每个浏览器动作先过 Watchdog 三色审计 |
| E3 | 没有本地视频接口预留 | 接驳统一压缩科学 + WebRTC/MediaStream |
| E4 | MCP 桥没接真实工具 | 接驳 Claude in Chrome MCP 真实可用工具 |
| E5 | DNA 链不完整 | 每个浏览器动作都有 DNA 追溯 + chain_hash |
| E6 | 记忆层重复造轮子 | 直接接驳记忆系统 v1.1 |
| E7 | 通心译重复写 | 直接调用通心译中间层共享模块 |
| E8 | 浏览器安全边界缺失 | Cookie/密码/登录专项 sealed 规则 |

## 规则先行架构

### P0 铁律（浏览器专用）

1. **规则先行** — 任何浏览器动作先过 Watchdog 三色审计
2. **Cookie/密码零接触** — 不读取、不存储、不传输
3. **执行流场自洽** — 输入→审计→路由→执行→留痕→归档
4. **DNA 不少一分** — 每个浏览器动作写入 DNA_LEDGER + chain_hash
5. **本地优先** — 所有处理本地先行

### 三色审计映射

| 浏览器动作 | 审计 | 
|-----------|------|
| 读取页面文本 | 🟢 AUTO_OK |
| 截图/录屏 | 🟢 AUTO_OK |
| 填写表单 | 🟡 NEED_CONFIRM |
| 点击发送/提交 | 🟡 NEED_CONFIRM |
| 读取 Cookie/密码 | 🔴 BLOCKED |
| 下载文件 | 🟡 NEED_CONFIRM |
| 支付/转账 | 🔴 BLOCKED |

## sealed 规则（浏览器专用）

| 触发内容 | 处理 | 三色 |
|---------|------|------|
| Cookie 正文 | sealed·不读不存不传 | 🔴 |
| 保存的密码 | sealed·绝对不读取 | 🔴 |
| 登录凭证/Session | sealed | 🔴 |
| 信用卡信息 | sealed·不录入 | 🔴 |
| 页面公开文本 | 正常读取 | 🟢 |
| 页面 DOM 结构 | 正常读取 | 🟢 |
| URL/标题 | 正常读取 | 🟢 |

## 六层架构

```
Layer 6: 同步层 — WebSocket + Syncthing + Tailscale
Layer 5: DNA 留痕层 — chain_hash + append-only + 记忆粒子
Layer 4: 视频接口层 — WebRTC + MediaStream + 统一压缩科学（预留）
Layer 3: MCP 执行层 — Claude in Chrome + DevTools + 本地终端
Layer 2: CNSH 路由层 — 意图→多Agent分工·人格路由·pageId隔离
Layer 1: 规则层 — Watchdog三色审计 + P0铁律 + GATE-01数字根
Layer 0: 通心译层 — 情绪识别 + 语义净化 + 意图提取
```

## IPA 编号注册

| 编号 | 模块 | 层级 |
|------|------|------|
| LOCAL-BROWSER-CORE | 浏览器主进程 | Layer 3 |
| LOCAL-BROWSER-CNSH | CNSH 解析器 | Layer 2 |
| LOCAL-BROWSER-ROUTER | 多 Agent 路由 | Layer 2 |
| LOCAL-BROWSER-AUDIT | 规则审计层 | Layer 1 |
| LOCAL-BROWSER-MCP | MCP 桥接层 | Layer 3 |
| LOCAL-BROWSER-VIDEO | 视频接口层 | Layer 4 |
| LOCAL-BROWSER-MEMORY | 记忆粒子层 | Layer 5 |
| LOCAL-BROWSER-SYNC | 多设备同步 | Layer 6 |

---

**DNA追溯码：** #龍芯⚡️2026-07-12-Browser-Engine-v1.1-0e9b67f1
**三色审计：** 🟢 通过
**投喂来源：** Notion导出·UID9622原创
