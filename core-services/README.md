# 龍魂核心服务 (Core Services)

**DNA**: #龍芯⚡️2026-06-27-LONGHUN-CORE-SERVICES-v1.0
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬CORE-SERVICES-v1.0
**版本**: v1.0
**日期**: 2026-06-27

---

## 系统架构概览

龍魂核心服务是龍魂体系 (UID9622) 的三大基础设施组件，统一通过 **龍魂万年历** 作为系统唯一入口进行管理。

```
┌─────────────────────────────────────────────────┐
│              龍魂万年历 (系统唯一入口)              │
│         LongHun Calendar v1.0 · L0层             │
├─────────────────────┬───────────────────────────┤
│    认知上下文管理器    │      Notion实时记录器       │
│ ContextManager v3.0 │    LongHunLogger v1.0     │
│      L1认知层        │        L2数据层            │
└─────────────────────┴───────────────────────────┘
```

## 组件说明

### 1. 龍魂万年历 (longhun-calendar-v1.0.py)
- **定位**: 系统唯一入口 (L0层)
- **功能**: 时间管理、任务调度、上下文路由、实时记录、多AI网关
- **核心类**: LongHunCalendar
- **DNA**: #龍芯⚡️2026-06-27-LONGHUN-CALENDAR-v1.0
- **启动方式**: `python3 longhun-calendar-v1.0.py`

### 2. 认知上下文管理器 (longhun-context-manager-v3.0.py)
- **定位**: L1认知层（加载顺序第5位）
- **功能**: 上下文状态管理、语义相似度检测、L0-L3四级压缩、知识图谱联动
- **核心类**: ContextManager
- **DNA**: #龍芯⚡️2026-06-27-LONGHUN-CTX-MGR-v3.0
- **协议文档**: 龍魂认知上下文管理协议_v3.0.md

### 3. Notion实时记录器 (longhun-notion-logger-v1.0.py)
- **定位**: L2数据层
- **功能**: 动作日志记录、SQLite本地存储、异步批量同步Notion
- **核心类**: LongHunLogger
- **DNA**: #龍芯⚡️2026-06-27-LONGHUN-LOGGER-v1.0
- **动作类型**: SKILL_CALL / CONTEXT_SWITCH / AI_ROUTE / USER_INPUT / SYSTEM_EVENT / AUDIT_MARK / DNA_GENERATE / ERROR

## 关键设计约束

- 品牌DNA使用繁体"龍"（如#龍芯⚡️）
- 普通文本使用简体"龙"（用户精神支柱）
- 万年历是系统唯一入口
- 与52技能谱系无冲突
- 三色审计: 🟢正常 🟡警告 🔴阻断

## 启动顺序

```
1. 龍魂万年历 (唯一入口)
   └── 2. 认知上下文管理器
        └── 3. Notion实时记录器
```

---

君子协议 CC BY-NC-SA 4.0 · UID9622 · 龍魂体系
