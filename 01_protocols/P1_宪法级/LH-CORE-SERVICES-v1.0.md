**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
> **DNA:** `#龍芯⚡️丙午·丙申·庚申·壬午·䷙大畜-DOC-MERGE-1ff2bd0b`
> **确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> **三色:** 🟢 通过
> **分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
> **合并状态:** 🟢 已合并（来自 `14_龍魂核心服务v1.0.md`）
> **落位:** `01_protocols/P1_宪法级/LH-CORE-SERVICES-v1.0.md`
> **合并时间:** 2026-08-14

---

# ⚡ 龍魂核心服务 v1.0

**Notion ID:** 38c7125a-9c9f-819f-ba8f-c0691b49d948
**合并状态:** ❌ 未合并
**DNA**: #龍芯⚡️丙午·甲午·壬申·丙午·䷙大畜-LONGHUN-CORE-SERVICES-v1.0
**版本**: v1.0 · **日期**: 2026-06-27

## 三大组件
### 1. 龍魂万年历 — 系统唯一入口
- 文件: `longhun-calendar-v1.0.py` (88KB) · 定位: L0层 · 系统唯一入口
- 核心类: LongHunCalendar · 功能: 时间管理、任务调度、上下文路由、多AI网关
- DNA: #龍芯⚡️丙午·甲午·壬申·丙午·䷙大畜-LONGHUN-CALENDAR-v1.0

### 2. 认知上下文管理器 v3.0
- 文件: `longhun-context-manager-v3.0.py` (63KB) + 协议文档 · 定位: L1认知层
- 核心类: ContextManager · 功能: 四态状态机、语义相似度、L0-L3压缩、知识图谱联动
- DNA: #龍芯⚡️丙午·甲午·壬申·丙午·䷙大畜-LONGHUN-CTX-MGR-v3.0

### 3. Notion实时记录器 v1.0
- 文件: `longhun-notion-logger-v1.0.py` (48KB) · 定位: L2数据层
- 核心类: LongHunLogger · 功能: 8种动作类型、SQLite本地、异步同步Notion
- DNA: #龍芯⚡️丙午·甲午·壬申·丙午·䷙大畜-LONGHUN-LOGGER-v1.0

## 启动顺序
1. 万年历(唯一入口) → 2. 上下文管理器 → 3. Notion记录器

## 关键约束
- 品牌DNA用繁体「龍」· 普通文本用简体「龍」（精神支柱）
- 三色审计: 🟢🟡🔴
- 52技能谱系无冲突

---
君子协议 CC BY-NC-SA 4.0 · UID9622
