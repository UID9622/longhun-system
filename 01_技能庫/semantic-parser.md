# /semantic-parser

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️2026-07-06-SEMANTIC-PARSER-v1.0-SEMPAR`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬PARSE`

---

<!--#龍芯⚡️2026-07-06-SEMANTIC-PARSER-v1.0-SEMPAR -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

---
skill_id: /semantic-parser
synced_at: 2026-07-06
source: bin/semantic_parser.py
---

# /semantic-parser · 语义解析引擎

## 摘要

语义解析引擎（semantic-parser）是龍魂系统的自然语言到lh6命令的翻译桥梁。提供四级解析链路：① 精确匹配——内置80+常用命令映射表（"检查共生体服务状态"→"lh6 status symbiote"等）；② 模糊正则匹配——20+条正则模式覆盖多种自然语言表达变体（支持lambda动态参数如域名/IP提取）；③ 缓存匹配——JSON持久化命令映射缓存（~/.longhun/semantic/command_map.json）；④ Kimi API降级解析——本地Kimi服务API fallback（http://127.0.0.1:8000/kimi/parse-command）。执行前必须通过语义回显确认（echo_confirm），防止误操作。支持--auto模式跳过确认直接执行。

## 关键词

自然语言解析 Natural Language Parsing, 命令映射 Command Mapping, 语义回显 Semantic Echo, 模糊匹配 Fuzzy Pattern Match, Kimi API降级 Kimi API Fallback, 命令缓存 Command Cache, 确认机制 Confirmation, NL2CMD

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] 知识矩阵总纲 v3.0 · 命令体系 (#UID9622⚡️2026-06-16-KNOWLEDGE-MATRIX-MASTER-v3.0)
  - [2] 六十四卦路由引擎·命令语义映射
- 相关龍魂系统源码：
  - `bin/semantic_parser.py` — 语义解析引擎 v1.0
  - `bin/bagua_router.py` — 六十四卦路由（解析目标）
  - `bin/longhun-command-registry.json` — 命令注册表（解析参考）

## 诚实局限

1. Kimi API fallback依赖本地Kimi服务运行，服务不可用时自动降级为本地匹配。
2. 模糊正则匹配基于特定正则模式，对新颖或复杂表达可能无法识别。
3. 当前未集成LLM推理能力，纯基于规则匹配+API fallback。

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-06 | v1.0.0 | UID9622 | 初始创建，四级解析链路+语义回显确认+Kimi API fallback | 草稿 |

## 分类标签

- 总纲模块：#语义解析 #自然语言 #命令翻译 #Kimi集成
- 对外状态：#Gitee #GitHub
- 审计色：#🟢绿色放行
- 八卦归属：☲ 离卦（火·火·技能层）
- 命令入口：`lh6 语义解析 "<自然语言>"` / `lh6 语义解析 --auto "<命令>"`
- 关联引擎：bagua_router.py / kimi-webbridge.md / hetu_luoshu_dna.py

## DNA 签名

```
#龍芯⚡️2026-07-06-SEMANTIC-PARSER-v1.0-SEMPAR
#CONFIRM🌌9622-ONLY-ONCE🧬PARSE
```
