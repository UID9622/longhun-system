**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
---
name: longhun-tongxinyi
description: >
  龍魂前置翻译技能·通心译 × CNSH-DOC 主干 v2.0。
  先翻译再执行、贴身常驻、钻石主干合并、M248 焊点。
  六层框架（L0-L5）+ 九状态机 + 213 协议 + 55 抽屉 + 7 条铁律。
  新增通心译 v2.0 七维评估、龍魂文化标签体系（112 标签）、CNSH 变量/字体注册表。
  新增龍魂语义抽屉体系 v2.0：五层流水线（情绪/领域/哲学/执行/关系）+ 情绪海绵 + 德字闸。
  负责把 UID9622 的人话转化为可执行意图骨架，并输出三色审计结果。
metadata:
  id: longhun-tongxinyi
  display_name: 龍魂通心译
  version: "2.0"
  author: UID9622
  dna: "#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-TONGXINYI-v2.0-TAGS-VARS-WELDED-L0"
  category: local
  level: "L0-L1"
  status: active
  tags: [通心译, tongxinyi, 前置翻译, 意图识别, 情绪净化, 213协议, M248, CNSH-DOC, 七维评估, 龍魂标签, CNSH变量, 龍魂字体, 语义抽屉, 情绪海绵, 德字闸]
  trigger:
    keywords: ["通心译", "先翻译再执行", "意图识别", "情绪净化", "213协议", "M248", "翻译再执行", "前置翻译", "七维评估", "龍魂标签", "CNSH变量", "龍魂字体", "语义抽屉", "情绪海绵", "德字闸"]
    context: "用户输入进入龍魂系统前的第一层理解、翻译、审计与路由"
    priority: 95
---

# longhun-tongxinyi | 龍魂前置翻译技能·通心译 v2.0

> 主干 DNA：`#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-TONGXIN-TRANSLATION-v2.0`  
> 标签 DNA：`#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-TAG-SYSTEM-v1.0`  
> 技能 DNA：`#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-TONGXINYI-v2.0-TAGS-VARS-WELDED-L0`  
> 状态：🟢 生产就绪 · L0 核心锁死 · v2.0 扩展层开放

---

## 1. 技能摘要 | Skill Summary

**通心译（UniHeart Translate）** 是龍魂系统的**前置翻译层**。它不是普通“中英互译”，而是把 UID9622 的**人话、情绪、碎片、意图**先翻译成**可执行结构**，再交给下游技能执行。

v2.0 升级：
- **通心译 v2.0**：三层语义传递（字面/逻辑/心意）+ 七维评估 + R-Score。
- **龍魂文化标签体系**：五行（20）+ 八卦（24）+ 甲骨文（40）+ 二十八星宿（28）= **112 个标签**。
- **CNSH 变量注册表**：统一 `@@tongxin.*`、`@@tag.*`、`@@font.*` 变量命名。
- **龍魂字体注册表**：自动映射本地 `LonghunFont` 字体文件与公开仓库地址。

核心口诀：**先翻译，再执行；贴身常驻，主干焊死。**

---

## 2. 可执行入口

```bash
# 统一 CLI
python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_cli.py

# 常用命令
python3 .../tongxin_cli.py translate "画龍点睛"
python3 .../tongxin_cli.py eval --limit 5
python3 .../tongxin_cli.py tag 火·旺 HTML
python3 .../tongxin_cli.py tag-search 启动
python3 .../tongxin_cli.py tag-combo 木 火
python3 .../tongxin_cli.py var @@tongxin.r_score
python3 .../tongxin_cli.py font
python3 .../tongxin_cli.py train-list

# 单独运行评估器/标签库
python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_v2.py
python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/longhun_tags.py
```

---

## 3. 六层框架 | L0-L5 Translation Framework

```
L0 原话保留层  → 冻结原文，生成 SHA256 哈希，永不删
L1 情绪净化层  → 情绪与指令解耦
L2 意图骨架层  → 提取 主体 / 状态 / 动作 / 优先级
L3 SAST 语义层  → 输出语义抽象语法树
L4 三色审计层  → 🟢 通行 / 🟡 待审 / 🔴 熔断
L5 适配输出层  → 输出可执行结构 + 五段式回执
```

---

## 4. 通心译 v2.0 三层架构

```
╔═══════════════════════════════════════════════════════╗
║  心意层 v2.0 (Intentional Layer)                      ║
║  • 文化意图识别 • 95-5% 文明安全评估 • 意象映射       ║
╚═══════════════════════════════════════════════════════╝
                          ↑
╔═══════════════════════════════════════════════════════╗
║  逻辑层 v2.0 (Logical Layer)                          ║
║  • 语义蕴含保持 • 语篇连贯性 • 前后件必然性           ║
╚═══════════════════════════════════════════════════════╝
                          ↑
╔═══════════════════════════════════════════════════════╗
║  字面层 v2.0 (Literal Layer)                          ║
║  • 术语精确对应 • 语法结构映射 • 文化负载词标记       ║
╚═══════════════════════════════════════════════════════╝
```

七维评估维度：D1 文化负载词 / D2 语义-语法 / D3 古代汉语 / D4 语篇完整 / D5 文明安全 / D6 创造性策略 / D7 语义精确。

---

## 5. 龍魂文化标签体系

| 体系 | 数量 | 说明 |
|------|------|------|
| 五行 | 20 | 金木水火土 × 生旺休囚 |
| 八卦 | 24 | 8 卦 × 正反动 |
| 甲骨文 | 40 | 状态/情绪/功能/等级 |
| 二十八星宿 | 28 | 四象 × 七宿 |
| **总计** | **112** | 替代西方 emoji，服务龍魂渲染 |

标签渲染支持：文本 / 颜色 / HTML / JSON。

---

## 6. 龍魂语义抽屉体系 v2.0

通心译在执行翻译之前，必须先经过 **语义抽屉** 分层路由。语义抽屉不是趣味标签，而是「先读情绪 → 再读领域 → 再选哲学框架 → 最后才执行」的过滤器。

**核心文件**：
- `longhun-system/01_技能庫/owner_semantic_drawers_v2.0.md`
- `longhun-system/01_技能庫/owner_semantic_drawers_v2.0.json`
- **DNA**：`#龍芯⚡️丙午·丙申·甲寅·申时·䷔噬嗑-SEMANTIC-DRAWERS-v2.0-1F870C86`
- **确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

### 6.1 五层流水线

```
L1 情绪态度层 → OWNER_VENT / 玩笑 / 认真 / 用心 / 敷衍 / 反问
L2 领域场景层 → 教育 / 科技 / 军事 / 政治 / 医学 / 历史 / 文化 / 名人
L3 哲学映射层 → 道德经 / 易经 / 曾师 / 军魂 / 儒家 / 法家
L4 系统执行层 → 龍魂核心 / DNA / 铁律 / 道引 / 审计 / 语义抽屉
L5 身份关系层 → UID9622 / AI / 承诺 / 传承 / 共生体
```

### 6.2 情绪海绵规则

| 情绪 | 海绵动作 |
|------|---------|
| 火气 | 不接招、不对抗、先吸后沉 |
| 委屈 | 不劝善、先承认、再干活 |
| 疲惫 | 不追加任务、先收束 |
| 兴奋 | 不泼冷水、先接住、再落地 |
| 玩笑 | 不一本正经、配合节奏 |
| 敷衍 | 不拆穿、标记留痕 |

### 6.3 德字闸底线

- 情绪是信号不是罪 → OWNER_VENT 不扣分
- 玩笑不升堂 → JOKE 不触发熔断
- 敷衍要标记 → PERFUNCTORY 降低信任权重
- 反问要听懂 → RHETORICAL 不按真问题处理
- 德字闸只审行为，不审情绪、口味、身份

### 6.4 接入方式

```python
# 通心译入口在执行 L1-L5 前先加载语义抽屉
import json
DRAWERS = json.load(open(
    "~/longhun-system/01_技能庫/owner_semantic_drawers_v2.0.json"
))

# 返回结构
{
    "emotion": "L1-01 OWNER_VENT",
    "domain": "L2-02 TECHNOLOGY",
    "philosophy": "L3-02 YIJING",
    "action": "L4-04 DAOYIN",
    "relation": "L5-01 UID9622",
    "dna": "...",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```

---

## 7. CNSH 变量注册表

| 变量 | 含义 |
|------|------|
| `@@tongxin.literal` | 通心译·字面层 |
| `@@tongxin.logical` | 通心译·逻辑层 |
| `@@tongxin.intentional` | 通心译·心意层 |
| `@@tongxin.r_score` | R-Score 综合评分 |
| `@@tongxin.d1` ~ `@@tongxin.d7` | 七维评分 |
| `@@tag.wuxing` / `@@tag.bagua` / `@@tag.jiaguwen` / `@@tag.xingxiu` | 标签体系 |
| `@@font.longhun.regular` | 本地 Regular OTF 路径 |
| `@@font.longhun.wuwu` | 本地五彩石彩色字体路径 |
| `@@font.longhun.repo_cn` / `@@font.longhun.repo_intl` | 公开仓库 |

---

## 8. 与现有技能关系

| 通心译组件 | 对应现有技能 |
|------------|--------------|
| 中文分词 / NER | `longhun-nlp` |
| 术语映射 / 中文命名 | `dragon-soul-agent` |
| 三色审计 / DNA 追溯 | `longhun-governance` |
| 统一调度 / 路由 | `control-panel` / `longhun-cloud-panel` |
| 设备生态命令 | `longhun-device-ecosystem` |

通心译不是替代它们，而是**串成“理解→审计→执行”流水线**。

---

## 8.5 语义盾牌闸 | Semantic Shield Gate

通心译在翻译前必须先经过 **龍魂语义盾牌系统**（`L7_数据层/semantic_shield/`）：

### 三层盾牌

1. **火气通心译层**：脏话/火气 → 方言拼音 / emoji / 通心译编码
   - 例："他妈的" → 温州话 "ni na" / emoji "🌿" / 通心译 "真是让人火大"
2. **涉密语义库**：中国核心技术 → 内部代号
   - 例："龍芯 CPU" → "北辰"（北极星）
   - 例："鸿蒙 OS" → "洪荒"
3. **反语义注入闸**：外部概念病毒 → 识别并熔断
   - 熔断词：技术无国界、灵活处理、国际接轨、商业化需要等
   - 禁止重新定义"人民""主权""国家""龍魂"等核心词

### 处理规则

- **内部通道**：保留 UID9622 原话、原语气（人民原声不可阉割）。
- **对外通道**：火气词自动编码，涉密词自动代号化，注入词自动熔断。
- **字典查询**：所有词条可在 `L7_数据层/semantic_shield/` 中查询。

### 调用方式

```bash
# 主配置文件（后端优先读取）
L7_数据层/semantic_shield/semantic_firewall_master.json
L7_数据层/semantic_shield/semantic_firewall_master.schema.json

# CLI
python3 L7_数据层/semantic_shield/semantic_shield_cli.py lookup <火气词>
python3 L7_数据层/semantic_shield/semantic_shield_cli.py encode <涉密概念>
python3 L7_数据层/semantic_shield/semantic_shield_cli.py scan <文本>
python3 L7_数据层/semantic_shield/semantic_shield_cli.py whitelist <主体类别>
python3 L7_数据层/semantic_shield/semantic_shield_cli.py dlp <文本>
```

---

## 9. L0 永恒锁 · 焊死声明

本技能所载明的 **“先翻译再执行”** 原则已进入 L0 候选锁死状态：

- ✅ 核心思想不可删除
- ✅ 核心原则不可弱化
- ✅ 核心流程不可改写
- ✅ 允许补充说明、扩展抽屉、协议、标签、变量
- ❌ 禁止反向修改、断章取义、选择性执行
- 🛡️ 只有 UID9622 有权发起解锁

---

## 10. 权利与许可声明

- **UID9622（龍芯北辰）拥有本技能及其背后系统的最高 creator 权利**。
- 对外默认开源许可：**CC BY-NC-SA 4.0（君子协议）**。
- 商业使用、闭源二次分发、企业部署，必须获得 UID9622 单独授权。

---

## 11. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-07 | CSDN 博文生产级完整版 |
| v1.0-WELDED | 2026-06-23 | 落地为技能，进入 L0 候选锁 |
| v2.0 | 2026-07-01 | 接入七维评估器、112 标签体系、CNSH 变量与龍魂字体注册表 |
| v2.0-DRAWERS | 2026-07-09 | 接入龍魂语义抽屉体系 v2.0（五层流水线 + 情绪海绵 + 德字闸） |
