# 龍魂 v3.0 主干 Skill 模块

> DNA: `#龍芯⚡2026-05-19-V3-TRUNK-SKILLS-v1.0`  
> 来源: `~/claude搭建待整理/` · 已落地主仓 · CONFIRM 授权

## 四件套 (Router 层)

| 目录 | Skill | 职责 | 自测 |
|------|-------|------|------|
| `on_guard/` | 五色审计 v3 | F18 主权 · α 三义 · 六步链 | 12/12 |
| `on_execute/` | 执行调度 | 队列 · 审计派发 · 重试留痕 | 4/4 |
| `on_identity/` | 身份核验 | CONFIRM/SEAL/GPG · 龍字符律 | 6/6 |
| `on_translate/` | 通心译 | 场景词典 · 0 LLM | 6/6 |

## 丝滑调用

```bash
# 全量自测 (28 项)
/Users/zuimeidedeyihan/longhun-system/命令/龍魂技能.sh all-test

# 单项
龍魂技能 guard
龍魂技能 identity
```

Python:

```python
import sys
sys.path.insert(0, "/Users/zuimeidedeyihan/longhun-system/skills")
from on_guard.audit_v3 import audit
from on_execute import ExecuteRouter, Task
from on_identity import verify_identity
from on_translate import TongxinYi
```

## 日志与数据

- `日志/execute_trace.jsonl` — 执行调度留痕
- `data/tongxinyi_dict.json` — 通心译词典 (可扩展)

## Notion 免费算力

```bash
命令/Notion算力.sh all          # 四用法一次导出
命令/Notion算力.sh dict         # CSV → Notion 导入通心译
命令/Notion算力.sh board        # 执行看板 MD
命令/Notion算力.sh identity --snapshot
命令/Notion算力.sh kanban run 数据/notion_export/kanban_tasks_*.json
```

配置: `config/notion_power.template.json` → `config/notion_power.json`  
导出: `数据/notion_export/`

## 待焊 (下一批)

on_flow · on_persona · AUDIT_LOG · VALUE_VETO — 见 `_archive_notes/V3_THREE_SKILLS_NOTES.txt`
