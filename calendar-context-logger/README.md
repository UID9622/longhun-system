# 龍魂万年历 · 认知上下文 · Notion记录器 集成包

**DNA:** `#龍芯⚡️2026-06-28-LONGHUN-CALENDAR-CONTEXT-LOGGER-v1.0`

本目录存放龙魂系统第三轮三个核心组件的主系统集成版本：

| 文件 | 说明 |
|------|------|
| `calendar_core.py` | 龍魂万年历：系统唯一入口、时间管理、任务调度、AI网关 |
| `context_manager.py` | 龍魂认知上下文管理器 v3.0：状态机、压缩、知识图谱联动 |
| `notion_logger.py` | 龍魂Notion实时记录器 v1.0：本地SQLite + Notion双写 |
| `cli.py` | 统一命令行入口 |


## 命令

```bash
lh-calendar status                 # 查看系统状态
lh-calendar enter code "写快排"    # 通过万年历入口进入系统
lh-calendar demo                   # 运行完整演示
lh-context list                    # 列出最近会话
lh-logger recent --limit 5         # 查看最近记录
```


## 数据目录

- 运行数据：`~/.longhun/calendar-context-logger/`
- 日历数据：`~/.longhun/calendar-context-logger/calendar/`
- 日志数据库：`~/.longhun/calendar-context-logger/action_log.db`


## 品牌约定

- DNA 追溯码使用繁体 **龍**：`#龍芯⚡️...`
- 普通用户可见文本使用简体 **龙**
- 所有路径统一在 `~/.longhun/calendar-context-logger/`
