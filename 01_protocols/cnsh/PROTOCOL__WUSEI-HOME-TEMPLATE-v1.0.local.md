# PROTOCOL · 五彩石主场模板 v1.0（色标 × 五层 × 五闸门 × 跑马灯）

> **DNA:** `#龍芯⚡2026-05-18-WUSEI-HOME-TEMPLATE-v1.0`  
> **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
> **SEAL:** `#ZHUGEXIN⚡2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`  
> **上位:** `PROTOCOL__NUWA-COLOR-TERMINAL-v1.0.local.md` · `PROTOCOL__HOME-BATTLEFIELD-DEV-ENV-v1.0.local.md`

---

## 定盘

**以后看颜色就知道规则归属**——五色不装饰，只绑语义；跑马灯把 L0→L5 与 G1→G5 **连成一条链**，子模块不得躲在角落。

| 五彩石 | Token | HEX | 五行(dr) | 绑定的层 | 绑定的闸门 | 行为语义 |
|--------|-------|-----|----------|----------|------------|----------|
| 黄土金 | ROOT_GOLD | `#C6A664` | 5 土 | **L0 主控** · L5 输出签章 | G5 不写龍 | 主权 / 可执行 / DNA |
| 赤火红 | BREAKER_RED | `#A61B1B` | 3/4 火 | L2 系统出站 | **G2 上传=0** · G4 熔断 | 阻断 / 停止 |
| 深海青 | THINK_BLUE | `#1C3D5A` | 8/9 水 | L4 知识 | **G3 不反客** | 推演 / 待审 |
| 玉白色 | AUDIT_WHITE | `#D9D4C7` | 6/7 金 | L4 审计只读 | **G1 敢露面?** | 只读 / 验收 |
| 苍木绿 | RESTORE_GREEN | `#3F5E45` | 1/2 木 | **L1 硬件** · L3 工具 | 烟测 / 恢复 | 生长 / 同步 |

**L3 工具层** 用绿+金双色条（工具可跑 + 主权入口）。

---

## 页面结构（§0–§12 · 逻辑闭环）

| § | 区块 ID | 颜色条 | 内容（不得省略） |
|---|---------|--------|------------------|
| 0 | `hdr` | 五色渐变 | 龍芯北辰 · UID9622 · CONFIRM · 开发环境才是主权 |
| 1 | `arch` | 金→绿→青→白→金 | L0–L5 五层 + 兼容律一句 |
| 2 | `gates` | 白红青绿金 五卡 | G1–G5 + 失败动作 |
| 3 | `marquee` | **五色跑马灯** | 动态：工程\|DNA\|Audit\|Git\|dr\|端口摘要 |
| 4 | `auto` | 火红 | 自动化：11 步执行链 · 脚本绝对路径 |
| 5 | `audit` | 玉白 | 留痕：`home_battlefield_trace.jsonl` · SHA256 · 龍字符律 |
| 6 | `ports` | 木绿 | L1/L2 端口矩阵（9625/8765/9633/11434/9626/9623） |
| 7 | `wusei` | 五色图例 | 五彩石对照表 + 公式最小链 |
| 8 | `knowledge` | 水青 | L4 知识源（Notion page_id → 仓库路径） |
| 9 | `children` | **五色边框** | **子系统全表**（禁止「小崽崽躲着」） |
| 10 | `cursor` | 金 | Cursor 规则 · Skills · 预提交 |
| 11 | `control` | 火 | 主控链接 · 一键命令 |
| 12 | `footer` | 金 | DNA · SEAL · 壁纸路径 |

**交互页真源：** `public/www/index.html`（本机 `http://127.0.0.1:9626/`）

---

## 跑马灯格式（写死）

```
[木·本机] | [金·L0 UID9622] | [水·dr=?] | [白·Audit 🟢🟡🔴] | [火·G2=0上传] | [金·DNA短码] | [青·任务] | [绿·9625…]
```

- 五色段顺序固定：**绿 → 金 → 青 → 白 → 红 → 循环**（与 NUWA §六一致升级）。
- 熔断时整段底色切 `BREAKER_RED`，文案前缀 `CIRCUIT BREAKER |`。

---

## 子系统登记（§9 必须全露出）

| 色 | 子系统 | 入口 |
|----|--------|------|
| 金 | 主场协议 / 字符律 | `01_protocols/cnsh/PROTOCOL__*` |
| 金 | DNA / CONFIRM | 页眉常显 |
| 白 | 三色 / dr 闸门 | `cnsh/gate_v3` · `bin/龍字符律扫描.sh` |
| 青 | CNSH / 公式对准 | `01_protocols` · Notion 公式表 |
| 青 | BehavCrypto 母稿 | `longhun-system/BehavCrypto_v1.0/` |
| 水 | Web3-DNA v8 | `算法仓库/Web3主权交易/` |
| 绿 | 9625 引擎 | `:9625/console` |
| 绿 | 8765 操作台 | `:8765/.../龍魂操作台_MVP_v1.html` |
| 绿 | 9633 网关 / 隧道 | `bin/开龍魂` |
| 绿 | Ollama | `:11434` |
| 白 | 草日志监控 | `tools/local-sync-monitor/` |
| 红 | 一票否决 / 密钥 | `veto` skill · 不读 `.env` |
| 火 | 11 步执行订单 | `BehavCrypto_v1.0/_audit/EXEC_TRACE_*` |

---

## Cursor / 规则着色约定

| 规则文件前缀 | 色 |
|--------------|-----|
| `uid9622-home-battlefield` | 金 |
| `uid9622-long-character-law` | 金 |
| `uid9622-ai-handshake` | 白 |
| `behavcrypto` | 青 |

---

*看色即知归属 · 跑马灯即链 · 开发环境才是主权*
