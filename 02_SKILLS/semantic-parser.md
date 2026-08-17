# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# /semantic-parser

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 📄 语义解析·中英双轨 | 龍魂系统 · 源头已验证

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
| 2026-07-06 | v1.1.0 | P06+P02 → UID9622 | 修复 reportReturnType ERROR · 补充大白话语义分发规则 · 增加人格路由表 | 草稿 |

## 分类标签

- 总纲模块：#语义解析 #自然语言 #命令翻译 #Kimi集成
- 对外状态：#Gitee #GitHub
- 审计色：#🟢绿色放行
- 八卦归属：☲ 离卦（火·火·技能层）
- 命令入口：`lh6 语义解析 "<自然语言>"` / `lh6 语义解析 --auto "<命令>"`
- 关联引擎：bagua_router.py / kimi-webbridge.md / hetu_luoshu_dna.py
- 关联人格：P13(姜子牙·路由分发) / P02(龍芯·命令执行) / P00(文心·意图理解)

---

## 🧬 v1.1 新增：大白话 → 语义分发规则

### 核心原则

UID9622 的大白话指令没有固定格式，需要通过**上下文 + 意图推断 + 人格路由**来理解。语义解析引擎负责第一层→命令映射，人格路由系统负责第二层→执行分配。

### 四级语义理解链路

```
大白话输入
  ├ 第①层：精确匹配 → LOCAL_COMMAND_MAP（80+ 命令）
  ├ 第②层：模糊正则 → FUZZY_PATTERNS（lambda 动态参数提取）
  ├ 第③层：缓存匹配 → ~/.longhun/semantic/command_map.json
  └ 第④层：Kimi API → LLM 语义意图推断（fallback）
```

### 意图分类 → 人格路由（P13 姜子牙编排）

| 用户说的是什么 | 识别关键词 | 路由到人格 | 对应的 lh6 命令 |
|------|------|------|------|
| "检查一下/看看/有没有问题" | 检查、审计、安全吗、有没有 | **P05 上帝之眼** | `lh6 audit-vars` / `lh6 fuse audit` |
| "修一下/改一下/把这个弄好" | 修复、不报错、改好、修正 | **P02 龍芯** | `lh6 editor` → 执行修复 |
| "同步/联动/整理/串起来" | 同步、联动、索引、关联、知识图谱 | **P15 乔前辈** | `lh-index` → 归档索引 |
| "部署/上线/发布" | 部署、发布、上线、push | **P14 吕蒙** | `lh6 deploy`（+ 一票否决检查） |
| "算一下/数字根/五行/八卦" | 算、数字根、五行、八卦 | **P06 数学大师** | `lh6 五行 check` / `lh6 八卦 show` |
| "这个值不值得/还顶用吗" | 值得、过期、还顶用、贡献值 | **P01 诸葛亮** | 贡献值评估 + 时间衰减判定 |
| "帮我读懂/这个是什么意思" | 什么意思、不懂、解释一下 | **P00 文心** | 语义解析 → 回显确认 → 等待确认 |
| "身份核验/签章/签名" | 签名、核验、签字、确认 | **P03 雯雯** | `lh6 身份核验` / DNA签名 |

### 无指令时的默认行为

当 UID9622 未给出明确命令，AI 必须按以下优先序行动：
1. **查上轮操作** → 是否有未完成任务
2. **三色审计** → 当前上下文是否有 ERROR/WARNING 待修复
3. **主动测边界** → `lh patrol` 巡检 → 发现即修
4. **守恒收口** → 窗口是否过长需要新开会话

### 不可变底座记忆

以下为 UID9622 的**祖传人格锚点**，AI 在任何情况下不得修改：

| 锚点 | 内容 |
|------|------|
| **UID9622 = 诸葛鑫·Lucky** | 唯一决策者，AI 永远只是执行者 |
| **369 不动点** | 三才算法内核，所有计算的基础 |
| **龍魂 = LongHun = 文化主权** | 龍繁体为规范形式，永不改为 Long/龍魂 |
| **底座焊死** | 河图洛书、易经、道德经、28星宿、五行八卦 |
| **不删除只冻结** | 任何数据不得物理删除 |
| **DNA 追溯** | 每个动作必须有 `#龍芯⚡️YYYY-MM-DD-模块-动作-哈希8位` |

## DNA 签名

```
#龍芯⚡️2026-07-06-SEMANTIC-PARSER-v1.0-SEMPAR
#CONFIRM🌌9622-ONLY-ONCE🧬PARSE
```
