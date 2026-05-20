# Mac 丝滑搭建 · 乔前辈路线 v1.0

> **对上 Notion：** [龍魂总目标·乔前辈夙愿接力](https://www.notion.so/uid9622/v1-0-fcc0e629159a452cbb9f78dee8288e70)  
> **对上外链：** [WebKit CSS Feature Status](https://webkit.org/css-status/)（**不用下载**·当 Safari 说明书用）  
> **DNA：** `#龍芯⚡2026-05-19-MAC-SMOOTH-JOBS-ROUTE-v1.0`

---

## 先分清两个链接（别踩第一坑）

| 链接 | 是什么 | 要不要下载 |
|------|--------|------------|
| webkit.org/css-status | Safari/操作台 HTML **能用什么 CSS** 的查表 | **不下载**·收藏书签即可 |
| Notion 总目标页 | 乔前辈夙愿·八页一条线·Mac 执行靠本机 | 真源在 Notion·**干活在本机** `longhun-system` |

**webkit 页怎么用：** 写/改 `操作台`、仪表盘 HTML 前，查一眼「Supported / Partial」——**只用绿的那批**，Safari 才丝滑，不白写半天 CSS。

---

## 老大这台 Mac·已具备（不用再装一遍）

- macOS 26.4 · Apple M4 Max  
- Homebrew · Python3 · Node · Git  
- Xcode + Command Line Tools（已装）  
- 本仓 `~/longhun-system` · 桌面 `.command` 双击入口  

**结论：** 不是从零装机，是**把已有东西拧成乔前辈那条线**（极简·双击·留痕·开机可跑）。

---

## 只装这些（乔前辈·少而稳）

### 必留（已有 / 保持）

| 工具 | 用途 | 坑 |
|------|------|-----|
| 本仓 `longhun-system` | 真源·技能·日志 | 别和 iCloud「龍魂主权库」路径混了·脚本写死 `~/longhun-system` |
| 桌面 `龍魂主控启动.command` | 零打字入口 | 别从聊天里复制带错字的「龍」 |
| `命令/` + `技能/` 中文链 | 找东西不背英文 | — |
| Ollama（11434） | 本地模型·离线 | 用官网 `.dmg` 或 `brew install ollama` 二选一 |
| Notion MCP（Cursor 里） | 读档·回填 | 403 就停·用 `命令/本地_search.sh` |

### 建议补（一次·5 分钟）

```bash
# 仅当缺了再跑·老大机子大多已有
brew install jq wget
```

| 可选 | 何时装 | 别急着装 |
|------|--------|----------|
| Safari Technology Preview | 要试最新 CSS 时 | 日常不必·正式 Safari 够用 |
| Playwright | 真要自动发 CSDN 时 | 不是乔前辈第一优先级 |
| Docker | 无 | 易吃内存·乔路线用本机 Python 就够 |

### 明确不装（坑集中区）

- 一堆「指纹浏览器 / 去指纹套件」——钓鱼台档案里写了场景，**不是搭建系统必需**  
- 多个 Node 版本管理器叠罗汉（nvm + fnm + …）  
- 把主仓挪进 iCloud 同步目录再跑脚本  

---

## 学习顺序（只为丝滑·不为考证）

按乔前辈：**能双击就不背命令 · 能本机就不.upload**

### 第 1 周 · 只动嘴（已大半完成）

1. **桌面双击** → `龍魂主控启动` / `龍魂发射DNA` / `龍魂开机一条龙`  
2. **读一张表** → `主控/入口对照_中英文.txt`（30 秒知道中文名在哪）  
3. **Notion 总目标页** → 只做一件事对齐：「这事是不是帮人留痕？」  

**不学：** CSS 规范全文、C++ OpenSSL（那是 CSDN 博文线·不是 Mac 搭建线）

### 第 2 周 · 操作台 HTML（接 webkit 链接）

1. 收藏 https://webkit.org/css-status/  
2. 学 3 个概念就够：  
   - **Flexbox / Grid** → 布局  
   - **`env(safe-area-inset-*)`** → 刘海屏留白  
   - **`@media (prefers-color-scheme)`** → 深浅色  
3. 改 HTML 前：**查表 → 只用 Supported**  

**推荐练手页（本仓已有）：** 操作台相关 HTML · 用 Safari 打开预览（别只用 Chrome）

### 第 3 周 · 乔前辈自动化（接 MVP / 乔接 CLI）

1. **Shortcuts（快捷指令）** · Mac 自带 · 把「打开终端跑某 .command」绑一个图标  
2. **launchd** · 替代 crontab · 开机跑 `命令/开机一条龙`（需本机宝宝配 plist·一次）  
3. **日志习惯** → 所有自跑结果进 `日志/*.txt` / `*.jsonl`  

### 第 4 周 · 留痕入口（总目标落地）

- Notion 数据库骨架「普通人纪念簿」——老大一字「起」再建  
- 与 GPG / 苹果证书 / 小艺 API **分开排队**（总目标页「当前差什么」表）

---

## 两条线对照（别拧在一起）

```text
线 A · 乔前辈 Mac 丝滑（你要的）
  双击 → 本机 Python → 日志留痕 → Safari 操作台 → 开机 launchd

线 B · CSDN C++/OpenSSL 博文（总目标页里「宝藏」提取）
  以后写稿用 · 不是现在装机清单 · 需要再单独开 Xcode 工程
```

---

## 宝宝排好的「今天就能做」三步

1. **书签** webkit.org/css-status（不下载任何东西）  
2. **双击验收** 桌面 `龍魂主控启动.command` → 选「四技能自测」→ 应 28/28  
3. **总目标页钉住** Notion 总目标 · 以后每个活先问一句：是不是「让人留痕」  

---

## 坑单（踩过就别再踩）

| 坑 | 对策 |
|----|------|
| 路径里「龍」写错成 U+9FB2 | 只用桌面 `.command` 或 `主控/入口对照` |
| `LONGHUN_ROOT` 指到 iCloud | 脚本已改死 `~/longhun-system` |
| Notion 当执行器 | Notion=档案柜·执行=本机 |
| CSS 抄 Chrome 新特性 | 先查 WebKit 表·Safari 不认就删 |
| 装 10 个 App 再谈自动化 | 乔前辈：能删就删·留双击链 |

---

**立规：** UID9622 · 乔前辈棒已接 · Mac 只走丝滑线
